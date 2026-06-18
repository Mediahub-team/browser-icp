from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Dict, Tuple
from urllib.parse import parse_qsl, urlsplit, urlunsplit, urlencode

import requests


SAVE_PATH = Path(os.getenv("SAVE_PATH", "../../references"))
LINKS_JSON = Path(os.getenv("LINKS_JSON", "links.json"))
TIMEOUT_SECONDS = int(os.getenv("TIMEOUT_SECONDS", "30"))

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36"
    )
}


def normalize_url(url: str) -> str:
    """
    Remove UTM params and fragments.
    Keep the original path unless a redirect happens on the server.
    """
    parts = urlsplit(url)
    filtered_query = [
        (k, v)
        for k, v in parse_qsl(parts.query, keep_blank_values=True)
        if not k.lower().startswith("utm_")
    ]
    query = urlencode(filtered_query, doseq=True)
    return urlunsplit((parts.scheme or "https", parts.netloc, parts.path, query, ""))


def safe_filename(name: str) -> str:
    """
    Convert domain key into a safe filename.
    Example: 'browser.yandex.ru' -> 'browser.yandex.ru.html'
    """
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", name.strip())
    return f"{cleaned}.html"


def fetch_html(url: str) -> Tuple[str, str]:
    """
    Return final URL after redirects and HTML body.
    """
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
        raise ValueError("links.json must contain a JSON object of {domain: link}")
    return {str(k): str(v) for k, v in data.items()}


def main() -> None:
    SAVE_PATH.mkdir(parents=True, exist_ok=True)
    links = load_links(LINKS_JSON)

    for domain, raw_url in links.items():
        url = normalize_url(raw_url)
        output_file = SAVE_PATH / safe_filename(domain)

        try:
            final_url, html = fetch_html(url)
            output_file.write_text(html, encoding="utf-8")
            print(f"[OK] {domain} -> {final_url} -> {output_file}")
        except Exception as exc:
            print(f"[ERR] {domain} -> {url} :: {exc}")


if __name__ == "__main__":
    main()
