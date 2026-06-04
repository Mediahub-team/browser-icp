#!/usr/bin/env python3
"""preview_search.py — превью объявлений для КОНТЕКСТА (Поиск Яндекса), своё, zero-dep.

Рендерит мокап поисковой выдачи Яндекса с нашими объявлениями из campaign-spec JSON
(того же формата, что build_campaign.py). Открой HTML в браузере / сделай скриншот,
чтобы увидеть, как объявление выглядит в выдаче ДО заливки.

Вход: campaign-spec.search.example.json (или любой spec с adgroups[].ads[]).
Ads могут содержать необязательные: sitelinks: [{title,href}], callouts: [str].

Использование:
  python3 preview_search.py --spec ../campaign-spec.search.example.json
  python3 preview_search.py --spec ... --out build/preview-search.html
"""
from __future__ import annotations
import argparse
import html
import json
import os

CSS = """
:root{--bg:#fff;--text:#1a1a1a;--muted:#6b6f76;--link:#0a5cff;--visited:#7b3fc4;
--green:#0f7b2e;--label:#9a9ea6;--line:#e7e8ea;--ad:#1a1a1a}
*{box-sizing:border-box}
body{margin:0;background:#f1f2f4;font:15px/1.45 Arial,'Helvetica Neue',sans-serif;color:var(--text)}
.serp{max-width:560px;margin:24px auto;padding:0 16px}
.note{color:#888;font:12px/1.4 monospace;margin:0 0 16px}
.ad{background:var(--bg);border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin:0 0 12px}
.ad .meta{display:flex;align-items:center;gap:8px;font-size:13px;color:var(--green)}
.ad .fav{width:16px;height:16px;border-radius:4px;background:#dfe3ea;display:inline-block;flex:0 0 16px}
.ad .label{color:var(--label);font-size:12px;border:1px solid var(--line);border-radius:4px;padding:0 5px;margin-left:auto}
.ad .url{color:var(--green);font-size:13px;margin-left:24px}
.ad h3{margin:4px 0 2px 24px;font-size:18px;font-weight:400;color:var(--link);line-height:1.25}
.ad .t2{color:var(--link);font-weight:400}
.ad .text{margin:2px 0 0 24px;color:var(--text);font-size:14px}
.ad .sub{margin:8px 0 0 24px;display:flex;flex-wrap:wrap;gap:14px}
.ad .sub a{color:var(--link);font-size:13px;text-decoration:none}
.ad .callouts{margin:6px 0 0 24px;color:var(--muted);font-size:13px}
.len{font:11px/1 monospace;color:#b00;margin-left:24px}
.ok{color:#0a0}
"""

LIMITS = {"title": 56, "title2": 30, "text": 81, "display_path": 20}


def esc(s):
    return html.escape(s or "")


def lim_badge(ad):
    out = []
    for k, mx in LIMITS.items():
        v = ad.get(k, "")
        n = len(v)
        cls = "ok" if n <= mx else ""
        if v:
            out.append(f'<span class="{cls}">{k}:{n}/{mx}</span>')
    return " · ".join(out)


def render_ad(ad, domain):
    path = esc(ad.get("display_path", ""))
    url = f"{domain}/{path}" if path else domain
    parts = [f'<div class="ad">']
    parts.append('<div class="meta"><span class="fav"></span>'
                 f'<span>{esc(domain)}</span><span class="label">Реклама</span></div>')
    parts.append(f'<div class="url">{esc(url)}</div>')
    title = esc(ad.get("title", ""))
    t2 = ad.get("title2", "")
    h = f'<h3>{title}'
    if t2:
        h += f' — <span class="t2">{esc(t2)}</span>'
    h += "</h3>"
    parts.append(h)
    parts.append(f'<div class="text">{esc(ad.get("text",""))}</div>')
    sl = ad.get("sitelinks") or []
    if sl:
        links = "".join(f'<a href="#">{esc(s.get("title", s) if isinstance(s, dict) else s)}</a>' for s in sl)
        parts.append(f'<div class="sub">{links}</div>')
    co = ad.get("callouts") or []
    if co:
        parts.append(f'<div class="callouts">{" · ".join(esc(c) for c in co)}</div>')
    parts.append(f'<div class="len">{lim_badge(ad)}</div>')
    parts.append("</div>")
    return "".join(parts)


def domain_of(href):
    if not href:
        return "пример.рф"
    h = href.split("//")[-1].split("/")[0]
    return h


def main():
    p = argparse.ArgumentParser(description="Превью объявлений Поиска (мокап выдачи Яндекса).")
    p.add_argument("--spec", required=True)
    p.add_argument("--out", default="build/preview-search.html")
    args = p.parse_args()
    with open(args.spec, encoding="utf-8") as f:
        spec = json.load(f)
    name = spec.get("campaign", {}).get("name", args.spec)
    ads_html = []
    for g in spec.get("adgroups", []):
        for ad in g.get("ads", []):
            ads_html.append(render_ad(ad, domain_of(ad.get("href", ""))))
    doc = (f"<!doctype html><html lang=ru><head><meta charset=utf-8>"
           f"<meta name=viewport content='width=device-width,initial-scale=1'>"
           f"<title>Превью Поиск — {esc(name)}</title><style>{CSS}</style></head><body>"
           f"<div class=serp><p class=note>Мокап выдачи Яндекса · {esc(name)} · "
           f"{len(ads_html)} объявл. (длины полей — снизу каждого)</p>"
           f"{''.join(ads_html)}</div></body></html>")
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"✓ {args.out} — {len(ads_html)} объявл. (открой в браузере)")


if __name__ == "__main__":
    main()
