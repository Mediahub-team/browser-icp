# Этап 1 — Гипотезы аудиторий

Из описания продукта генерируем 6–10 сегментов-кандидатов со **скорингом fit-confidence**,
fit-рангом и **validation agenda** (ранг важности гипотез про аудиторию). Шаблон:
[`../templates/audience-hypotheses-template.md`](../templates/audience-hypotheses-template.md).

**Вход:** [`../00-product/product-description.md`](../00-product/product-description.md) (§2 ценность,
§4 отстройка, §6 kill-criteria, §9 вопросы) + [`../00-product/market-landscape.md`](../00-product/market-landscape.md).
**Выход:** `audience-hypotheses.md` — fit-таблица сегментов + validation agenda + финальный выбор для этапа 2.

### Промпт генерации
> Действуй как эксперт по customer research для B2C. На основе `00-product/product-description.md`
> (особенно §6 kill-criteria и §9 вопросы) и `market-landscape.md` собери 6–10 сегментов-кандидатов
> строго по шаблону `templates/audience-hypotheses-template.md`. **Kill-criteria этапа 0 —
> доминирующая gating-ось** скоринга: сегмент, проваливающий gate, не первичен. Для каждого — рычаг/
> модель ценности, **сильнейший конкурент именно этого сегмента** (не средний), заземление на
> market-landscape. **Не путай два результата:** (A) fit-ранг сегментов (кого в ICP) и (B) validation
> agenda — ранжированные по важности (Impact×Неопределённость) **гипотезы про аудиторию** как
> проверяемые вопросы с заземлением, kill-criteria первыми → это каркас порядка вопросов интервью.
> Числа моделей вознаграждения — иллюстрации, не зашивать в скоринг. Скоринг — `untested`.
</content>
