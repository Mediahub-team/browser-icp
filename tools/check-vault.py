#!/usr/bin/env python3
"""check-vault.py — валидатор Obsidian-конвенции для browser-icp.

Проверяет (без запуска Obsidian):
  1. frontmatter: если файл начинается с '---', блок должен корректно закрываться '---';
  2. вики-ссылки [[...]]: каждая (вне блоков кода) должна резолвиться в существующую заметку
     по basename — как делает Obsidian при newLinkFormat=shortest.

Что НЕ проверяется здесь (только в приложении Obsidian): рендер графа, бэклинки,
выполнение Dataview-запросов.

Выход: 0 — всё цело; 1 — есть битые ссылки или незакрытый frontmatter.
"""
from __future__ import annotations
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", ".obsidian", "node_modules"}
WIKILINK = re.compile(r"\[\[([^\[\]]+?)\]\]")


def md_files() -> list[str]:
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            if f.endswith(".md"):
                out.append(os.path.join(dirpath, f))
    return out


def note_key(path: str) -> str:
    return os.path.splitext(os.path.basename(path))[0].lower()


def strip_code(text: str) -> str:
    """Убираем код (огороженные блоки и инлайн-спаны), как делает Obsidian:
    внутри кода вики-ссылки не считаются ссылками — это иллюстративные примеры."""
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"`[^`]*`", "", text)
    return text


def check_frontmatter(text: str) -> str | None:
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        return None
    rest = text.split("\n", 1)[1] if "\n" in text else ""
    if "\n---" not in ("\n" + rest):
        return "frontmatter не закрыт '---'"
    return None


def resolve(target: str) -> str:
    # отрезаем алиас |, заголовок #, блок ^
    t = target.split("|", 1)[0].split("#", 1)[0].split("^", 1)[0].strip()
    return os.path.splitext(os.path.basename(t))[0].lower()


def main() -> int:
    files = md_files()
    keys = {note_key(p) for p in files}

    broken: list[tuple[str, str]] = []
    fm_errors: list[tuple[str, str]] = []
    link_count = 0

    for path in files:
        rel = os.path.relpath(path, ROOT)
        with open(path, encoding="utf-8") as fh:
            text = fh.read()

        err = check_frontmatter(text)
        if err:
            fm_errors.append((rel, err))

        body = strip_code(text)
        for m in WIKILINK.finditer(body):
            link_count += 1
            key = resolve(m.group(1))
            if key and key not in keys:
                broken.append((rel, m.group(1)))

    print(f"Файлов .md: {len(files)} · вики-ссылок проверено: {link_count}")
    if fm_errors:
        print(f"\nFRONTMATTER — ошибок: {len(fm_errors)}")
        for rel, e in fm_errors:
            print(f"  ✗ {rel}: {e}")
    if broken:
        print(f"\nБИТЫЕ ВИКИ-ССЫЛКИ: {len(broken)}")
        for rel, link in broken:
            print(f"  ✗ {rel}: [[{link}]]")

    if fm_errors or broken:
        print("\nИТОГ: ✗ есть проблемы")
        return 1
    print("\nИТОГ: ✓ frontmatter и все вики-ссылки целы")
    return 0


if __name__ == "__main__":
    sys.exit(main())
