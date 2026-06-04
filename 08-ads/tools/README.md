---
type: reference
stage: 8
status: done
tags: [stage/8, tool, yandex-direct]
---

# Yandex Direct API — возможности и инструмент

Python-инструмент (stdlib, zero-dep) для управления кампаниями Yandex Direct под наш
**пред-продуктовый лендинг-тест** (объявление → лендинг → лист ожидания). Здесь — что
API умеет, **что грузим**, **какие таргетинги**, и как безопасно запускать.

> **Безопасность.** По умолчанию **sandbox + suspended**. Реальные кампании и тем более
> открутка — только осознанно (`--production`, снять suspend вручную). `--dry-run` печатает
> payload без отправки. `--validate-only` — только проверка char-лимитов.

## Контекст и РСЯ — раздельно
Две сети ведём **разными кампаниями** (по требованию):
- **Контекст / Поиск** — `network: "search"` → `Network: SERVING_OFF`. Бьём по горячим
  ключам (search-intent), объявления текстовые. Спек: `campaign-spec.search.example.json`.
- **РСЯ / сеть** — `network: "rsya"` → `Search: SERVING_OFF`. Бьём по интересам/поведению,
  объявления текст+картинка (графика), крючки эмоциональнее. Спек: `campaign-spec.rsya.example.json`.

## API basics
- Версия **v5** (JSON). База: `https://api.direct.yandex.com/json/v5/`;
  **sandbox:** `https://api-sandbox.direct.yandex.com/json/v5/`.
- **Auth:** OAuth Bearer-токен из env `YANDEX_DIRECT_TOKEN` (см. `.env.example`).
- Расход — в баллах (заголовок `Units`), клиент его логирует.
- Sandbox: тот же токен, бесплатно, для безопасных экспериментов.

## Типы кампаний
Используем **TextCampaign** (текстово-графические объявления, поиск + РСЯ). Разделение
сетей — через `BiddingStrategy` (одна из сетей `SERVING_OFF`). Прочие типы (DynamicText,
Smart, Cpm) — не для этого теста.

## Что грузим (форматы объявлений и char-лимиты)
TextAd — выверено по `ref-v5/ads/add`:

| Поле | Лимит |
|---|---|
| **Title** (Заголовок 1) | **56** символов, слово ≤22 |
| **Title2** (Заголовок 2) | **30** обычных + ≤15 «узких», слово ≤22 |
| **Text** (Текст) | **81** обычных + ≤15 «узких», слово ≤23 |
| **DisplayUrlPath** | **20** (буквы/цифры/`-`/`/`/`№`/`%`/`#`) |
| Href | полный URL лендинга (с UTM) |

«Узкие» символы: `! , . ; : "`. Типы объявлений: `TextAd`, `TextImageAd`,
`TextAdBuilderAd`, `CpmBannerAdBuilderAd` и др.

Дополнительно грузим (через соответствующие сервисы):
- **Картинки для РСЯ** — `AdImages.add` (base64) → `AdImageHash` в объявлении. Форматы
  JPG/PNG/GIF; размеры/вес уточнять в доке `ref-v5/adimages` перед заливкой.
- **Быстрые ссылки (сайтлинки)** и **уточнения** — через расширения объявлений
  (`Sitelinks`/`AdExtensions`); типовые лимиты: сайтлинк-заголовок ~30, уточнение ~25
  символов — **сверять в доке** перед использованием.
- **Ключевые фразы** + минус-слова — `Keywords.add`.

## Какие таргетинги
- **Ключи/минус-слова** (`Keywords`) — Поиск; на РСЯ ключи = контекстный таргетинг.
- **Гео** — `RegionIds` группы; справочник `Dictionaries.get(["GeoRegions"])` (Россия = 225).
- **Демография, моб., аудитории, гео-корректировки** — `BidModifiers.add`.
- **Интересы / ретаргетинг / Yandex Audience** — `AudienceTargets.add`, `RetargetingLists`.
- **Расписание, стратегия ставок** — в настройках кампании (`BiddingStrategy`,
  `WeeklySpendLimit`).

## Замер (этап 9)
- Цель в **Яндекс.Метрике** «waitlist_signup» (отправка формы лендинга) + UTM в Href
  (`utm_source=yandex&utm_medium=cpc|cpm&utm_campaign=...&utm_content=...`).
- Статистика — сервис `Reports` (`client.get_report(...)`): показы, CTR, CPC, конверсии
  → считаем **signup-rate, cost-per-signup** и сверяем с гипотезами `test-plan.md`.

## Файлы
- `yandex_direct/client.py` — ядро (вызовы, auth, units, sandbox, dry-run).
- `yandex_direct/services.py` — обёртки сервисов (Campaigns/AdGroups/Ads/Keywords/
  AdImages/AudienceTargets/RetargetingLists/BidModifiers/Dictionaries/Reports).
- `build_campaign.py` — оркестратор спека → кампания (создаёт suspended).
- `campaign-spec.search.example.json` / `campaign-spec.rsya.example.json` — примеры спеков.
- `.env.example` — где взять токен.

## Запуск
```bash
# 1) локально проверить char-лимиты спека (без токена)
python3 build_campaign.py --spec campaign-spec.search.example.json --validate-only
# 2) собрать payload без отправки
python3 build_campaign.py --spec campaign-spec.rsya.example.json --dry-run
# 3) создать в песочнице (нужен YANDEX_DIRECT_TOKEN), кампания будет suspended
YANDEX_DIRECT_TOKEN=... python3 build_campaign.py --spec campaign-spec.search.example.json
# 4) боевой аккаунт — осознанно (кампания всё равно suspended, открутку снимаете вручную)
YANDEX_DIRECT_TOKEN=... python3 build_campaign.py --spec ... --production
```

## Документация
- Справочник API v5: https://yandex.ru/dev/direct/doc/ref-v5/
- Объявления (лимиты): https://yandex.ru/dev/direct/doc/ref-v5/ads/add.html
- Песочница: https://yandex.ru/dev/direct/doc/concepts/sandbox.html
- OAuth: https://yandex.ru/dev/direct/doc/start/token.html
