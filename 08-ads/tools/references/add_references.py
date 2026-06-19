"""
Download HTML snapshots of reference landing pages.

Reads URLs from links.json, saves raw HTML to 08-ads/references/<domain>.html.
Files are temporary — listed in .gitignore, regenerated on demand.

Usage (from repo root):
    python -X utf8 08-ads/tools/references/add_references.py

Env overrides:
    SAVE_PATH        path to save HTML files  (default: 08-ads/references)
    LINKS_JSON       path to links.json        (default: links.json in script dir)
    TIMEOUT_SECONDS  request timeout           (default: 30)
"""

from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path
from typing import Dict, Tuple
from urllib.parse import parse_qsl, urlsplit, urlunsplit, urlencode

import requests


SCRIPT_DIR = Path(__file__).parent
SAVE_PATH = Path(os.getenv("SAVE_PATH", "08-ads/references"))
LINKS_JSON = Path(os.getenv("LINKS_JSON", str(SCRIPT_DIR / "links.json")))
TIMEOUT_SECONDS = int(os.getenv("TIMEOUT_SECONDS", "30"))

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36"
    )
}


def normalize_url(url: str) -> str:
    parts = urlsplit(url)
    filtered_query = [
        (k, v)
        for k, v in parse_qsl(parts.query, keep_blank_values=True)
        if not k.lower().startswith("utm_")
    ]
    query = urlencode(filtered_query, doseq=True)
    return urlunsplit((parts.scheme or "https", parts.netloc, parts.path, query, ""))


def safe_filename(name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", name.strip())
    return f"{cleaned}.html"


def fetch_html(url: str) -> Tuple[str, str]:
    response = requests.get(
        url,
        headers=HEADERS,
        timeout=TIMEOUT_SECONDS,
        allow_redirects=True,
    )
    response.raise_for_status()
    response.encoding = response.encoding or response.apparent_encoding or "utf-8"
    return response.url, response.text


def load_links(path: Path) -> Dict[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("links.json must contain a JSON object of {domain: url}")
    return {str(k): str(v) for k, v in data.items()}


def fmt_bytes(n: int) -> str:
    if n < 1024:
        return f"{n} B"
    if n < 1024 ** 2:
        return f"{n / 1024:.1f} KB"
    return f"{n / 1024 ** 2:.1f} MB"


def main() -> None:
    SAVE_PATH.mkdir(parents=True, exist_ok=True)
    links = load_links(LINKS_JSON)
    total = len(links)

    print(f"Референсов к загрузке: {total}")
    print(f"Сохраняем в:           {SAVE_PATH.resolve()}\n")

    ok_count, err_count, total_bytes = 0, 0, 0

    for i, (domain, raw_url) in enumerate(links.items(), start=1):
        url = normalize_url(raw_url)
        output_file = SAVE_PATH / safe_filename(domain)
        t0 = time.perf_counter()

        try:
            final_url, html = fetch_html(url)
            output_file.write_text(html, encoding="utf-8")
            size = len(html.encode("utf-8"))
            total_bytes += size
            elapsed = time.perf_counter() - t0
            print(
                f"[{i:>2}/{total}] OK   {domain:<30} "
                f"{fmt_bytes(size):>9}  {elapsed:.1f}s"
                + (f"  → {final_url}" if final_url != url else "")
            )
            ok_count += 1
        except Exception as exc:
            elapsed = time.perf_counter() - t0
            print(f"[{i:>2}/{total}] ERR  {domain:<30} {elapsed:.1f}s  {exc}")
            err_count += 1

    print(f"\nИТОГ: {ok_count} загружено / {err_count} ошибок — {fmt_bytes(total_bytes)} на диск")


if __name__ == "__main__":
    main()
