#!/usr/bin/env python3
"""generate_landing.py — собрать статический лендинг из content/<seg>.json + шаблон + CSS.

Zero-dep. Вшивает design-system.css в один HTML-файл (портативно, можно сразу открыть/
залить). Посыл — из content JSON (углы S/A по калибровке). Визуальные ТОКЕНЫ (цвета/шрифты)
живут в design-system.css — заменяются на бренд из Figma-экспортов.

Использование:
  python3 generate_landing.py --content content/icp04.json
  python3 generate_landing.py --content content/icp04.json --out build/landing-icp04.html
"""
from __future__ import annotations
import argparse
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def esc(s):
    return html.escape(s or "")


def render_bullets(items):
    out = []
    for it in items:
        out.append(f'      <li class="bullet"><b>{esc(it["b"])}</b>'
                   f'<span>{esc(it.get("span",""))}</span></li>')
    return "\n".join(out)


def render_opts(opts):
    out = []
    for o in opts:
        out.append(f'        <button type="button" class="opt" aria-pressed="false">{esc(o)}</button>')
    return "\n".join(out)


def render_proof(quotes):
    if not quotes:
        return ""
    qs = "".join(f"<q>{esc(q)}</q>" for q in quotes)
    return f'<section><h2>Говорят</h2><div class="proof">{qs}</div></section>'


def render_demo(demo):
    """Демо-блок «вердикт товара» для мотива S (одна запоминающаяся деталь)."""
    if not demo:
        return ""
    chip_cls = "ok" if demo.get("verdict_ok", True) else "warn"
    rows = "".join(
        f'<div class="demo-row"><span>{esc(r["k"])}</span>'
        f'<span class="bar"><i style="width:{int(r.get("pct",70))}%"></i></span></div>'
        for r in demo.get("rows", [])
    )
    return (f'<section><h2>{esc(demo.get("h2","Как это выглядит"))}</h2>'
            f'<div class="demo"><div class="verdict">'
            f'<span class="chip {chip_cls}">{esc(demo.get("chip","Оригинал ✓"))}</span>'
            f'<span>{esc(demo.get("verdict_text",""))}</span></div>{rows}'
            f'<p class="fine">{esc(demo.get("fine",""))}</p></div></section>')


def main():
    p = argparse.ArgumentParser(description="Собрать лендинг из content JSON.")
    p.add_argument("--content", required=True)
    p.add_argument("--out")
    p.add_argument("--template", default=os.path.join(HERE, "landing.template.html"))
    p.add_argument("--css", default=os.path.join(HERE, "design-system.css"))
    args = p.parse_args()

    with open(args.content, encoding="utf-8") as f:
        c = json.load(f)
    tpl = open(args.template, encoding="utf-8").read()
    css = open(args.css, encoding="utf-8").read()

    repl = {
        "{{CSS}}": css,
        "{{TITLE}}": esc(c.get("title", "Кешбэк Браузер")),
        "{{TONE}}": esc(c.get("tone", "S")),
        "{{EYEBROW}}": esc(c.get("eyebrow", "Кешбэк Браузер")),
        "{{H1}}": esc(c["h1"]),
        "{{LEAD}}": esc(c.get("lead", "")),
        "{{CTA}}": esc(c.get("cta", "Записаться в лист ожидания")),
        "{{CTA_NOTE}}": esc(c.get("cta_note", "")),
        "{{FINE}}": esc(c.get("fine", "")),
        "{{BULLETS}}": render_bullets(c.get("bullets", [])),
        "{{DEMO}}": render_demo(c.get("demo")),
        "{{INTENT_Q}}": esc(c.get("intent_q", "Что для вас главное?")),
        "{{OPTS}}": render_opts(c.get("opts", [])),
        "{{COMMIT}}": esc(c.get("commit", "Готов попробовать первым")),
        "{{PROOF}}": render_proof(c.get("proof", [])),
        "{{FOOT}}": esc(c.get("foot", "© 2025 Кешбэк Браузер")),
    }
    html_out = tpl
    for k, v in repl.items():
        html_out = html_out.replace(k, v)

    out = args.out or os.path.join(HERE, "build",
                                   "landing-" + os.path.splitext(os.path.basename(args.content))[0] + ".html")
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html_out)
    print(f"✓ {out}")


if __name__ == "__main__":
    main()
