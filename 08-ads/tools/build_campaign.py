#!/usr/bin/env python3
"""build_campaign.py — собрать и создать кампанию Yandex Direct из декларативного спека.

Две сети раздельно (по требованию): "контекст"/Поиск и РСЯ — каждая своим спеком
(network: "search" | "rsya"). Поиск = Network SERVING_OFF, РСЯ = Search SERVING_OFF.

БЕЗОПАСНОСТЬ:
  --sandbox (по умолчанию)  — песочница, спенда нет.
  --production              — боевой аккаунт (создаёт реальные кампании!).
  --dry-run                 — печатает payload, НЕ отправляет.
  --validate-only           — только локальная проверка char-лимитов спека.
Кампании создаются и сразу suspend (открутка не стартует).

Использование:
  python3 build_campaign.py --spec campaign-spec.search.example.json --validate-only
  python3 build_campaign.py --spec campaign-spec.rsya.example.json --sandbox --dry-run
  YANDEX_DIRECT_TOKEN=... python3 build_campaign.py --spec ... --sandbox
"""
from __future__ import annotations

import argparse
import json
import sys

from yandex_direct import DirectClient, DirectError, Services

NARROW = set('!,.;:"')           # «узкие» символы по справочнику Direct
RUB_TO_MICROS = 1_000_000
RUSSIA = 225                     # GeoRegions: Россия

# Лимиты TextAd (выверено по ref-v5/ads/add): Title 56, Title2 30(+15 узких),
# Text 81(+15 узких), слово в заголовке 22, слово в тексте 23, display-path 20.
LIMITS = {"title": 56, "title2": 30, "text": 81, "title_word": 22,
          "text_word": 23, "narrow_extra": 15, "display_path": 20}


def _narrow_split(s):
    narrow = sum(1 for ch in s if ch in NARROW)
    return len(s) - narrow, narrow


def check_ad(ad, idx):
    """Вернуть список ошибок char-лимитов для одного объявления."""
    errs = []
    title = ad.get("title", "")
    if len(title) > LIMITS["title"]:
        errs.append(f"  ад[{idx}] Title {len(title)}>56: {title!r}")
    for w in title.split():
        if len(w) > LIMITS["title_word"]:
            errs.append(f"  ад[{idx}] слово в Title >22: {w!r}")
    t2 = ad.get("title2", "")
    nn, nw = _narrow_split(t2)
    if nn > LIMITS["title2"] or nw > LIMITS["narrow_extra"]:
        errs.append(f"  ад[{idx}] Title2 {nn}+{nw}узк (лимит 30+15): {t2!r}")
    text = ad.get("text", "")
    nn, nw = _narrow_split(text)
    if nn > LIMITS["text"] or nw > LIMITS["narrow_extra"]:
        errs.append(f"  ад[{idx}] Text {nn}+{nw}узк (лимит 81+15): {text!r}")
    for w in text.split():
        if len(w) > LIMITS["text_word"]:
            errs.append(f"  ад[{idx}] слово в Text >23: {w!r}")
    dp = ad.get("display_path", "")
    if len(dp) > LIMITS["display_path"]:
        errs.append(f"  ад[{idx}] DisplayUrlPath {len(dp)}>20: {dp!r}")
    return errs


def validate_spec(spec):
    errs = []
    for gi, g in enumerate(spec.get("adgroups", [])):
        for ai, ad in enumerate(g.get("ads", [])):
            errs += check_ad(ad, f"{gi}.{ai}")
    return errs


def bidding_strategy(network, weekly_rub):
    wb = {"BiddingStrategyType": "WB_MAXIMUM_CLICKS",
          "WbMaximumClicks": {"WeeklySpendLimit": int(weekly_rub * RUB_TO_MICROS)}}
    off = {"BiddingStrategyType": "SERVING_OFF"}
    if network == "search":
        return {"Search": wb, "Network": off}
    if network == "rsya":
        return {"Search": off, "Network": wb}
    raise SystemExit(f"network должен быть search|rsya, а не {network!r}")


def build_campaign_payload(spec):
    c = spec["campaign"]
    return {
        "Name": c["name"],
        "TextCampaign": {"BiddingStrategy": bidding_strategy(c["network"], c.get("weekly_budget_rub", 7000))},
    }


def run(spec, svc, dry):
    # 1) кампания
    camp = svc.campaigns_add([build_campaign_payload(spec)])
    cid = "DRY" if dry else camp["AddResults"][0]["Id"]
    print(f"campaign -> {cid} ({spec['campaign']['network']})")
    regions = spec["campaign"].get("regions", [RUSSIA])
    neg = spec["campaign"].get("negative_keywords", [])
    for g in spec.get("adgroups", []):
        ag_payload = {"Name": g["name"], "CampaignId": cid, "RegionIds": regions}
        if neg:
            ag_payload["NegativeKeywords"] = {"Items": neg}
        ag = svc.adgroups_add([ag_payload])
        agid = "DRY" if dry else ag["AddResults"][0]["Id"]
        print(f"  adgroup -> {agid} ({g['name']})")
        ads = []
        for ad in g.get("ads", []):
            ta = {"Title": ad["title"], "Text": ad["text"], "Href": ad["href"], "Mobile": "NO"}
            if ad.get("title2"):
                ta["Title2"] = ad["title2"]
            if ad.get("display_path"):
                ta["DisplayUrlPath"] = ad["display_path"]
            if ad.get("image_hash"):          # РСЯ: картинка по AdImageHash
                ta["AdImageHash"] = ad["image_hash"]
            ads.append({"AdGroupId": agid, "TextAd": ta})
        if ads:
            svc.ads_add(ads)
            print(f"    ads += {len(ads)}")
        kws = [{"Keyword": k, "AdGroupId": agid} for k in g.get("keywords", [])]
        if kws:
            svc.keywords_add(kws)
            print(f"    keywords += {len(kws)}")
    # 3) сразу suspend — открутка не стартует
    if not dry and cid != "DRY":
        svc.campaigns_suspend([cid])
        print(f"campaign {cid} suspended (открутка не запущена)")


def main():
    p = argparse.ArgumentParser(description="Создать кампанию Yandex Direct из спека (search|rsya).")
    p.add_argument("--spec", required=True, help="JSON-спек кампании")
    p.add_argument("--production", action="store_true", help="боевой аккаунт (иначе sandbox)")
    p.add_argument("--dry-run", action="store_true", help="печатать payload, не отправлять")
    p.add_argument("--validate-only", action="store_true", help="только проверка char-лимитов")
    args = p.parse_args()

    with open(args.spec, encoding="utf-8") as f:
        spec = json.load(f)

    errs = validate_spec(spec)
    if errs:
        print("CHAR-ЛИМИТЫ: ✗ нарушения:\n" + "\n".join(errs))
        sys.exit(1)
    print(f"CHAR-ЛИМИТЫ: ✓ ({sum(len(g.get('ads', [])) for g in spec.get('adgroups', []))} объявл.)")
    if args.validate_only:
        return

    sandbox = not args.production
    if args.production and not args.dry_run:
        print("⚠️  PRODUCTION: будут созданы реальные кампании (suspended). Ctrl-C для отмены.")
    try:
        client = DirectClient(sandbox=sandbox, dry_run=args.dry_run)
        run(spec, Services(client), args.dry_run)
        if not args.dry_run:
            print(f"units: spent={client.last_units.spent} daily_limit={client.last_units.daily_limit}")
    except DirectError as e:
        print(f"Direct API error: {e} (code={e.code}, detail={e.detail})")
        sys.exit(2)


if __name__ == "__main__":
    main()
