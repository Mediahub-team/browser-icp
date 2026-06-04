"""Мини-загрузчик .env (stdlib). Токен берём из файла, не из репозитория.

Ищет .env в: переданном пути → cwd → каталоге 08-ads/tools/. Заполняет os.environ
только для отсутствующих ключей (реальный env имеет приоритет). .env в .gitignore.
"""
from __future__ import annotations
import os


def load_env(path=None):
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 08-ads/tools
    candidates = [path] if path else []
    candidates += [os.path.join(os.getcwd(), ".env"), os.path.join(here, ".env")]
    for p in candidates:
        if p and os.path.isfile(p):
            with open(p, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
            return p
    return None
