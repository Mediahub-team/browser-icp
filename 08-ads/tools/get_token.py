#!/usr/bin/env python3
"""get_token.py — получить access-токen Yandex Direct по OAuth (code flow), zero-dep.

Шаг 1 (без аргументов): печатает URL авторизации. Открой его в браузере под нужным
аккаунтом (YD_YANDEX_LOGIN), подтверди доступ — Яндекс покажет КОД подтверждения.
Шаг 2: python3 get_token.py --code <КОД> — меняем код на access_token и пишем его
в .env как YANDEX_DIRECT_TOKEN.

Берёт YD_CLIENT_ID / YD_CLIENT_SECRET из .env.
"""
from __future__ import annotations
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

from yandex_direct import load_env

AUTHORIZE = "https://oauth.yandex.ru/authorize"
TOKEN = "https://oauth.yandex.ru/token"


def env_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")


def upsert_env(key, value):
    p = env_path()
    lines = []
    found = False
    if os.path.isfile(p):
        with open(p, encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith(key + "="):
                    lines.append(f"{key}={value}\n"); found = True
                else:
                    lines.append(line)
    if not found:
        lines.append(f"{key}={value}\n")
    with open(p, "w", encoding="utf-8") as f:
        f.writelines(lines)


def main():
    ap = argparse.ArgumentParser(description="OAuth access-токен Yandex Direct.")
    ap.add_argument("--code", help="код подтверждения из браузера (шаг 2)")
    args = ap.parse_args()

    load_env()
    cid = os.environ.get("YD_CLIENT_ID")
    secret = os.environ.get("YD_CLIENT_SECRET")
    if not cid or not secret:
        print("✗ В .env нет YD_CLIENT_ID / YD_CLIENT_SECRET")
        sys.exit(1)

    if not args.code:
        url = f"{AUTHORIZE}?response_type=code&client_id={cid}&force_confirm=yes"
        login = os.environ.get("YD_YANDEX_LOGIN", "")
        print("ШАГ 1 — открой в браузере" + (f" (войди под {login})" if login else "") + ":\n")
        print("  " + url + "\n")
        print("Подтверди доступ → Яндекс покажет КОД. Затем:")
        print("  python3 get_token.py --code <КОД>")
        return

    data = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "code": args.code.strip(),
        "client_id": cid,
        "client_secret": secret,
    }).encode()
    req = urllib.request.Request(TOKEN, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            tok = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"✗ обмен кода не удался: HTTP {e.code}: {e.read().decode('utf-8','replace')[:300]}")
        sys.exit(2)
    access = tok.get("access_token")
    if not access:
        print(f"✗ нет access_token в ответе: {tok}")
        sys.exit(2)
    upsert_env("YANDEX_DIRECT_TOKEN", access)
    print(f"✓ токен получен и записан в .env (….{access[-4:]}, действует ~{tok.get('expires_in','?')} c).")
    print("Теперь: python3 check_connection.py --production")


if __name__ == "__main__":
    main()
