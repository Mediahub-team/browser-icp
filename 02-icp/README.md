# Этап 2 — ICP

Полные ICP-профили по сегментам, отобранным на этапе 1. **1 файл = 1 ICP**, имя
`icp-NN-<slug>.md`. Шаблон: [`../templates/icp-template.md`](../templates/icp-template.md).

**Вход:** `00-product/product-description.md` + топ-сегменты из `01-hypotheses/`.
**Выход:** ранжированные ICP с fit-confidence, болями топ-5 и customer language.

### Промпт генерации
> Действуй как эксперт по customer research для B2C. На основе описания продукта
> (`00-product`) и отобранной гипотезы аудитории (`01-hypotheses`) собери ICP строго по
> шаблону `templates/icp-template.md`. Конкретика под наш продукт (кешбэк-браузер, RU,
> маркетплейсы), без общих мест. Для каждого сильного тезиса — уровень уверенности и
> на чём основан. Боли — топ-5 по остроте с gap-анализом. Раздел customer language —
> дословные фразы и слова-табу. В конце явно раздели validated/untested.
