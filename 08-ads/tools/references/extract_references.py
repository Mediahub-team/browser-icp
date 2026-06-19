"""
Extract marketing copy from saved HTML reference snapshots.

For each <domain>.html in 08-ads/references/, produces a <domain-slug>.md file
with structured headings, CTAs, and value-prop bullets.

EN pages: original text kept as-is; marked for adaptation via russian-copywriting
          skill at landing-generation time (no machine translation).
RU pages: copy extracted as-is.

Sources with fewer than MIN_ITEMS total formulations are deleted (too sparse to be useful).

Usage (from repo root):
    python -X utf8 08-ads/tools/references/extract_references.py

Env overrides:
    REFS_PATH   path to references folder  (default: 08-ads/references)
"""

from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path

try:
    from bs4 import BeautifulSoup, Tag
except ImportError:
    raise SystemExit("Установите: pip install beautifulsoup4")


SCRIPT_DIR = Path(__file__).parent
REFS_PATH = Path(os.getenv("REFS_PATH", "08-ads/references"))
MIN_ITEMS = 5   # sources with fewer total items are dropped


# ── helpers ───────────────────────────────────────────────────────────────────

def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def has_cyrillic(text: str) -> bool:
    return bool(re.search(r"[а-яА-ЯёЁ]", text))


def page_language(h1: list[str], headings: list[str]) -> str:
    sample = " ".join(h1 + headings[:5])
    return "ru" if has_cyrillic(sample) else "en"


# ── HTML extraction ───────────────────────────────────────────────────────────

def extract_copy(html: str) -> dict[str, list[str]]:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript", "meta", "link"]):
        tag.decompose()

    seen: set[str] = set()

    def uniq_texts(tags: list[Tag], min_len: int = 3, max_len: int = 300) -> list[str]:
        out = []
        for tag in tags:
            t = clean(tag.get_text())
            if t and min_len < len(t) < max_len and t not in seen:
                seen.add(t)
                out.append(t)
        return out

    h1 = uniq_texts(soup.find_all("h1"))
    headings = uniq_texts(soup.find_all(["h2", "h3"]), max_len=200)[:25]

    cta_tags = [
        tag for tag in soup.find_all(["button", "a"])
        if re.search(r"btn|button|cta|action|sign.?up|get.?start|download|install|join|try",
                     " ".join(tag.get("class", [])), re.I)
    ]
    cta = uniq_texts(cta_tags, min_len=2, max_len=80)

    value_tags = soup.find_all("li") + [
        p for p in soup.find_all("p")
        if any(kw in " ".join(p.get("class", [])).lower()
               for kw in ["feature", "value", "benefit", "hero", "card"])
    ]
    bullets = uniq_texts(value_tags, min_len=15, max_len=220)[:20]

    return {"h1": h1, "headings": headings, "cta": cta, "bullets": bullets}


# ── markdown rendering ────────────────────────────────────────────────────────

def escape_pipe(s: str) -> str:
    return s.replace("|", "\\|")


def render_section(title: str, items: list[str]) -> str:
    if not items:
        return ""
    lines = [f"## {title}\n", "| Формулировка |", "|---|"]
    for item in items:
        lines.append(f"| {escape_pipe(item)} |")
    return "\n".join(lines) + "\n"


def render_md(domain: str, url: str, copy: dict[str, list[str]], lang: str) -> str:
    frontmatter = (
        "---\n"
        f"type: reference-extracted\n"
        f"source: {domain}\n"
        f"lang: {lang}\n"
        "stage: 8\n"
        "tags: [stage/8, reference, cashback]\n"
        "---\n\n"
    )
    header = f"# {domain} — формулировки\n\n**Источник:** {url}  \n"
    if lang == "en":
        header += (
            "**Язык:** EN — при генерации лендинга адаптировать "
            "через скилл `russian-copywriting` (не переводить дословно).  \n"
        )
    header += "\n"

    body = render_section("H1", copy["h1"])
    body += "\n" + render_section("H2 / H3", copy["headings"])
    if copy["cta"]:
        body += "\n" + render_section("CTA", copy["cta"])
    if copy["bullets"]:
        body += "\n" + render_section("Ценности / буллеты", copy["bullets"])

    return frontmatter + header + body


# ── main ──────────────────────────────────────────────────────────────────────

def load_urls() -> dict[str, str]:
    links_file = SCRIPT_DIR / "links.json"
    if not links_file.exists():
        return {}
    data = json.loads(links_file.read_text(encoding="utf-8"))
    return {str(k): str(v) for k, v in data.items()}


def main() -> None:
    html_files = sorted(REFS_PATH.glob("*.html"))
    if not html_files:
        print(f"[WARN] HTML-файлов не найдено в {REFS_PATH.resolve()}")
        print("       Сначала запустите add_references.py")
        return

    urls = load_urls()
    total = len(html_files)
    print(f"HTML-файлов к обработке: {total}  (минимум формулировок: {MIN_ITEMS})\n")

    ok_count, dropped_count, err_count = 0, 0, 0

    for i, path in enumerate(html_files, start=1):
        domain = path.stem                      # "joinhoney.com"
        slug = domain.replace(".", "-")         # "joinhoney-com"
        out_path = path.parent / f"{slug}.md"
        url = urls.get(domain, f"https://{domain.replace('_', '-')}")
        t0 = time.perf_counter()

        try:
            html = path.read_text(encoding="utf-8", errors="replace")
            copy = extract_copy(html)
            n_items = sum(len(v) for v in copy.values())
            elapsed = time.perf_counter() - t0

            if n_items < MIN_ITEMS:
                if out_path.exists():
                    out_path.unlink()
                print(
                    f"[{i:>2}/{total}] DROP {domain:<30} "
                    f"items={n_items:>3}  {elapsed:.1f}s  (< {MIN_ITEMS}, файл удалён)"
                )
                dropped_count += 1
                continue

            lang = page_language(copy["h1"], copy["headings"])
            md = render_md(domain, url, copy, lang)
            out_path.write_text(md, encoding="utf-8")

            print(
                f"[{i:>2}/{total}] OK   {domain:<30} "
                f"lang={lang}  items={n_items:>3}  {elapsed:.1f}s  → {out_path.name}"
            )
            ok_count += 1
        except Exception as exc:
            elapsed = time.perf_counter() - t0
            print(f"[{i:>2}/{total}] ERR  {domain:<30} {elapsed:.1f}s  {exc}")
            err_count += 1

    print(f"\nИТОГ: {ok_count} сохранено / {dropped_count} удалено / {err_count} ошибок")
    md_files = list(REFS_PATH.glob("*.md"))
    print(f"MD-файлов в {REFS_PATH}: {len(md_files)}")


if __name__ == "__main__":
    main()
