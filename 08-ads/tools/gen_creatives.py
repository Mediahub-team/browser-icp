#!/usr/bin/env python3
"""gen_creatives.py — генерация вариантов объявлений Yandex Direct через LLM (OpenRouter).

Читает бриф creative-brief.<seg>.json (угол, аудитория, customer language, табу, сеть, n),
просит модель выдать N вариантов, СРАЗУ валидирует char-лимиты Direct и печатает только
проходящие (плюс отбракованные с причиной). Ключ — OPENROUTER_API_KEY из .env.

Использование:
  python3 gen_creatives.py --brief creative-brief.icp04.json
  python3 gen_creatives.py --brief ... --model openai/gpt-4o --n 8
"""
from __future__ import annotations
import argparse
import json
import os
import re
import sys
import urllib.request

from yandex_direct import load_env
from build_campaign import check_ad   # переиспользуем валидатор char-лимитов

API = "https://openrouter.ai/api/v1/chat/completions"

SYS = (
    "Ты — сильный RU-копирайтер перформанс-рекламы Яндекс.Директ. Пишешь живо, без "
    "рекламного пафоса и канцелярита, голосом клиента. Строго соблюдаешь лимиты и табу. "
    "Возвращаешь ТОЛЬКО валидный JSON-массив без пояснений."
)

USER_TMPL = """Сегмент: {segment} (мотив {motive}). Сеть: {network}.
Угол: {angle}
Аудитория: {audience}
Голос клиента (используй живые формулировки, можно дословно): {lang}
ЧЕСТНОСТЬ (не обещай лишнего): {honesty}
Контекст CTA: {cta}
ТАБУ (никогда не используй): {taboo}

Сделай {n} РАЗНЫХ вариантов текстово-графических объявлений Директа.
ЛИМИТЫ (строго, не превышать): Title ≤ 56 симв., Title2 ≤ 30, Text ≤ 81; слово в заголовке ≤ 22, в тексте ≤ 23.
Каждый вариант — объект: {{"title": "...", "title2": "...", "text": "..."}}.
Заголовки цепляющие и разные по приёму (вопрос / история / прямая польза). Без кликбейта-обмана.
Верни JSON-массив из {n} таких объектов. Только JSON."""


def extract_json(s):
    s = s.strip()
    m = re.search(r"```(?:json)?\s*(.*?)```", s, re.DOTALL)
    if m:
        s = m.group(1).strip()
    i, j = s.find("["), s.rfind("]")
    if i >= 0 and j > i:
        s = s[i:j + 1]
    return json.loads(s)


def call_llm(model, system, user, key):
    body = json.dumps({
        "model": model,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "temperature": 0.85,
    }).encode("utf-8")
    req = urllib.request.Request(API, data=body, method="POST", headers={
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/Mediahub-team/browser-icp",
        "X-Title": "browser-icp creatives",
    })
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]


def main():
    ap = argparse.ArgumentParser(description="LLM-генерация объявлений Direct (OpenRouter).")
    ap.add_argument("--brief", required=True)
    ap.add_argument("--model", default="openai/gpt-4o")
    ap.add_argument("--n", type=int)
    args = ap.parse_args()

    load_env()
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        print("✗ нет OPENROUTER_API_KEY в .env"); sys.exit(1)
    brief = json.load(open(args.brief, encoding="utf-8"))
    n = args.n or brief.get("n", 6)
    user = USER_TMPL.format(
        segment=brief.get("segment", ""), motive=brief.get("motive", ""),
        network=brief.get("network", "search"), angle=brief.get("angle", ""),
        audience=brief.get("audience", ""), lang="; ".join(brief.get("customer_language", [])),
        honesty=brief.get("honesty", ""), cta=brief.get("cta_context", ""),
        taboo=", ".join(brief.get("taboo", [])), n=n)

    print(f"модель: {args.model} · сегмент: {brief.get('segment')} · прошу {n} вариантов…")
    try:
        raw = call_llm(args.model, SYS, user, key)
        ads = extract_json(raw)
    except urllib.error.HTTPError as e:
        print(f"✗ OpenRouter HTTP {e.code}: {e.read().decode('utf-8','replace')[:300]}"); sys.exit(2)
    except Exception as e:
        print(f"✗ не удалось разобрать ответ модели: {e}"); sys.exit(2)

    ok, bad = [], []
    for i, ad in enumerate(ads):
        errs = check_ad(ad, i)
        (bad if errs else ok).append((ad, errs))
    print(f"\n✓ В ЛИМИТАХ: {len(ok)} / {len(ads)}\n")
    for ad, _ in ok:
        print(f"  • {ad.get('title','')}  ⟮{len(ad.get('title',''))}/56⟯")
        print(f"    {ad.get('title2','')}  ⟮{len(ad.get('title2',''))}/30⟯")
        print(f"    {ad.get('text','')}  ⟮{len(ad.get('text',''))}/81⟯\n")
    if bad:
        print(f"✗ ОТБРАКОВАНЫ (лимиты): {len(bad)}")
        for ad, errs in bad:
            print(f"  • {ad.get('title','')!r}: {'; '.join(e.strip() for e in errs)}")


if __name__ == "__main__":
    main()
