---
type: reference
stage: 8
status: draft
tags: [stage/8, tool, landing-generator]
---

# Генератор лендингов — мобайл, лаконично, не «AI-slop»

Собирает статический лендинг под оффер из `content/<seg>.json` + шаблон + дизайн-система.
Один самодостаточный HTML (CSS вшит), mobile-first, форма waitlist + intent-блок.

> **Почему не выглядит «как AI».** Гарантия — **рукотворная дизайн-система**
> (`design-system.css`), а не генерация «на лету»: характерная типографика (не Inter/Roboto),
> тёплая бумажная палитра вместо фиолетовых градиентов, тонкая зернистость, сдержанная анимация.
> Принципы — из скилла `frontend-design`.

> **Визуал — на бренде** (сверено по Figma-экспортам лендингов): индиго-синий первичный +
> зелёный AI-акцент, светлый прохладный фон, белые скруглённые карточки с мягкой тенью,
> Golos Text. Точные hex/радиусы — в `design-system.css` (правятся при необходимости).

## Посыл
Тексты в `content/<seg>.json` — **research-углы по калибровке** (S «проверь товар»,
A «суть без копипаста»), а не кешбэк-лед. Тон/слова-табу — из ICP. Честность: «разбор пока на Ozon».

## Файлы
- `design-system.css` — токены + компоненты (правится под бренд).
- `landing.template.html` — каркас с плейсхолдерами + JS формы/intent.
- `generate_landing.py` — сборщик: `content/<seg>.json` → `build/landing-<seg>.html`.
- `content/<seg>.json` — контент по сегменту (hero, буллеты, demo, intent, proof).

## Запуск
```bash
python3 generate_landing.py --content content/icp04.json
# → build/landing-icp04.html (открой в браузере / на телефоне)
```

## Связка с AI-генерацией
Для генерации через сервисы дизайна (Claude Artifacts и т.п.) — промт-шаблон
[`../../../templates/landing-design-prompt.md`](../../../templates/landing-design-prompt.md);
ТЗ дизайнеру — [`../../../templates/landing-designer-brief.md`](../../../templates/landing-designer-brief.md).
Этот генератор даёт быстрый «эталон на бренде», от которого пляшут оба.
