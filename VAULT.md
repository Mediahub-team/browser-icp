---
type: reference
stage: meta
status: done
tags: [meta, obsidian, vault]
---

# VAULT — конвенция Obsidian

Репозиторий открывается как **Obsidian-ваулт**: папку `browser-icp/` указываем как vault.
Цель — видеть **граф связей** и **бэклинки** «откуда что берётся» по пайплайну, плюс
авто-таблицы через **Dataview**.

> Применяется **going-forward**: новые файлы (этапы 6–9, будущие прогоны) — по этой
> конвенции. Существующие файлы не переписываем; их markdown-ссылки тоже видны в графе.
> Методология — [[PLAN]], версионирование/ветки — [[BRANCHING]], прогресс — [[PIPELINE]].

## 1. Как открыть и проверить
1. Obsidian → *Open folder as vault* → выбрать `browser-icp/`.
2. Включить **Dataview**: Settings → Community plugins → Browse → Dataview → Install → Enable.
   (В репозитории плагин уже помечен включённым в `.obsidian/community-plugins.json`, но
   сам код плагина Obsidian докачивает локально при установке.)
3. Проверка формата:
   - **CLI (объективно):** `python3 tools/check-vault.py` — валидирует frontmatter и
     резолв всех `[[вики-ссылок]]`. Зелёный выход = ссылки и шапки целы.
   - **Визуально (в Obsidian):** открыть *Graph view* (связи), панель *Backlinks* на любом
     ICP (видно персоны из него), и заметку с Dataview-запросом (таблицы рендерятся).

## 2. Стиль ссылок
- **Вики-ссылки `[[имя-файла]]`** (без `.md`), алиас — `[[icp-01-ai-power-users|AI-power]]`,
  на заголовок — `[[summary#Ключевые находки]]`.
- В `app.json` включено `useMarkdownLinks: false` → новые ссылки создаются как вики.

## 3. Frontmatter (YAML-шапка нового файла)
Общие ключи:

```yaml
---
type: product-functionality|product-positioning|market-landscape|product-description|product|hypothesis|icp|persona|guide|run|analysis|offer|targeting|creative|landing|test-plan|result|reference|template
stage: 0            # номер этапа 0–9 (или meta)
status: draft|untested|validated|done
tags: [stage/N, motive/A]
---
```

Спец-поля по типу:

```yaml
# icp
motive: A            # A | S | C
fit_confidence: high # high|med|low
source: "[[audience-hypotheses]]"

# persona
icp: "[[icp-01-ai-power-users]]"
motive: A
fit_ring: core       # core|strong|peripheral|non-icp
age: 29
city: Москва

# run
guide: "[[guide-v2-deep-value-adoption]]"
branch: s4/guide-custdev-first
date: 2026-06-04
n: 40
distribution: "core 16 / strong 12 / peripheral 8 / non-icp 4"

# analysis | offer | result
sources: ["[[run-custdev-v2-2026-06-04/summary]]"]
segment: "[[icp-05-deal-hunters]]"
```

## 4. Теги
`#stage/0…9` · `#motive/A` `#motive/S` `#motive/C` ·
`#fit/core` `#fit/strong` `#fit/peripheral` `#fit/non-icp` ·
`#status/untested` `#status/validated`.

## 5. Трассировка «откуда что берётся» — главное правило
Каждый артефакт ссылается **вверх по пайплайну** на свой источник: в frontmatter
(`source:`/`sources:`) **и** строкой в тексте `**Источники:** [[...]]`. Тогда бэклинки
покажут downstream автоматически.

Цепочка источников:

```
product-functionality ┐
                       ├→ market-landscape → product-description → hypotheses → icp → persona → guide → run → analysis → offer → targeting → result
product-positioning ───┘
```

> Этап 0 раскладывается на под-артефакты (0.1 функциональность, 0.2 позиционирование, 0.5
> ландшафт, 0.9 описание). Функциональность — корень без источника; позиционирование ссылается
> на функциональность; ландшафт — на позиционирование; описание — на все три. Принцип
> «функциональность ⟂ позиционирование» — в [[PLAN]] §2.0.

## 6. Dataview — готовые запросы (вставлять в любую заметку)

Все ICP по мотивам:
````
```dataview
table motive, fit_confidence, status from "02-icp" where type = "icp" sort motive
```
````

Персоны по ICP и кольцу:
````
```dataview
table icp, fit_ring, age, city from "03-personas" where type = "persona" sort fit_ring
```
````

Таблица прогонов:
````
```dataview
table guide, branch, date, n from "05-simulations" where type = "run"
```
````

Все непроверенные утверждения (по всему ваулту):
````
```dataview
list from #status/untested
```
````

## 7. Что коммитим из `.obsidian/`
Трекаем `app.json`, `core-plugins.json`, `community-plugins.json` (единый формат для всех).
Игнорим волатильное (`workspace.json`, кэш, данные плагинов) — см. `.gitignore`.

## Связи
[[README]] · [[PLAN]] · [[PIPELINE]] · [[BRANCHING]]
