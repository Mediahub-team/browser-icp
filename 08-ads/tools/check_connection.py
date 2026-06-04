#!/usr/bin/env python3
"""check_connection.py — проверить интеграцию с Yandex Direct (read-only, без спенда).

Берёт токен из .env (YANDEX_DIRECT_TOKEN) и делает безопасный read-вызов:
Dictionaries.getGeoRegions (справочник регионов) — мутаций и трат нет.
По умолчанию sandbox; --production — read в боевом аккаунте.

Использование:
  python3 check_connection.py            # sandbox
  python3 check_connection.py --production
"""
from __future__ import annotations
import argparse
import sys

from yandex_direct import DirectClient, DirectError, Services, load_env


def main():
    p = argparse.ArgumentParser(description="Read-only проверка коннекта Yandex Direct.")
    p.add_argument("--production", action="store_true", help="боевой аккаунт (иначе sandbox)")
    args = p.parse_args()

    src = load_env()
    print(f".env: {'загружен ' + src if src else 'не найден — нужен 08-ads/tools/.env с YANDEX_DIRECT_TOKEN'}")

    env = "PRODUCTION" if args.production else "SANDBOX"
    try:
        client = DirectClient(sandbox=not args.production, dry_run=False)
    except DirectError as e:
        print(f"✗ {e}")
        sys.exit(1)

    print(f"Среда: {env}. Запрос Dictionaries.getGeoRegions (read-only)…")
    try:
        res = Services(client).geo_regions()
        regions = res.get("GeoRegions", []) if isinstance(res, dict) else []
        u = client.last_units
        print(f"✓ КОННЕКТ ЕСТЬ. Регионов в справочнике: {len(regions)}.")
        if regions:
            sample = next((r for r in regions if r.get("GeoRegionId") == 225), regions[0])
            print(f"  пример: {sample.get('GeoRegionId')} — {sample.get('GeoRegionName')}")
        print(f"  баллы (units): потрачено {u.spent} / лимит {u.daily_limit}")
    except DirectError as e:
        print(f"✗ API error: {e} (code={e.code}, detail={e.detail}, request_id={e.request_id})")
        if e.code == 53:
            print("  → код 53: невалидный/просроченный токен. Перевыпустите OAuth-токен.")
        sys.exit(2)


if __name__ == "__main__":
    main()
