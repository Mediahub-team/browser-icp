import { createContext } from "react";

// Варианты лендинга по сегментам (на базе реального бренд-лендинга).
// Выбор — по ?v=<id> в URL (UTM из объявления). Меняются hero, набор секций и копия формы.
//
// Реальный маппинг флагов секций (выверено по DOM):
//   marketplaces (Content1) — пилюли «Работает везде, где привыкли покупать» (кешбэк %)
//   steps        (Content3) — второстепенный блок (баланс/задания)
//   compare      (Content4) — «Как покупать выгоднее в 3 шага» + тизер ассистента (кешбэк-флоу)
//   reviews      (Content6) — «Один товар. Лучшая цена» + «Сравнивай» + «Нейросеть против
//                             заказных отзывов» (smart-блок: проверка товара/цены/отзывы)

export interface LandingVariant {
  id: string;
  label: string;
  hero: { lines: string[]; subtitle: string };
  sections: { marketplaces: boolean; steps: boolean; compare: boolean; reviews: boolean };
  modal: { title: string; subtitle: string; intentQuestion: string; intentOptions: string[] };
}

export const DEFAULT_VARIANT: LandingVariant = {
  id: "base",
  label: "Кешбэк (база)",
  hero: {
    lines: ["Возвращайте до 30% ", "с каждой покупки ", "на маркетплейсах"],
    subtitle: "Закупайтесь выгодно на WB, Ozon, Маркете и других площадках",
  },
  sections: { marketplaces: true, steps: true, compare: true, reviews: true },
  modal: {
    title: "Ранний доступ",
    subtitle: "Оставьте email или телефон, чтобы получить приглашение и бонус +200 ₽ на первую покупку",
    intentQuestion: "Что для вас главное?",
    intentOptions: ["Размер кешбэка", "Чтобы кешбэк реально выводился", "Проверить товар перед покупкой", "Всё в одном месте"],
  },
};

export const variants: Record<string, LandingVariant> = {
  base: DEFAULT_VARIANT,

  // ICP-05/06 — кешбэк, угол доверия к выплате (обучающая ячейка): полный лендинг
  cashback: {
    id: "cashback", label: "Кешбэк — доверие к выплате",
    hero: { lines: ["Кешбэк, который ", "реально выводится"],
      subtitle: "Без «обещали — а он не упал». Честно, без холда — выведешь сам." },
    sections: { marketplaces: true, steps: true, compare: true, reviews: true },
    modal: { title: "Ранний доступ",
      subtitle: "Оставьте email или телефон — позовём первыми, когда откроем вывод кешбэка.",
      intentQuestion: "Что для вас главное?",
      intentOptions: ["Чтобы кешбэк реально выводился", "Размер кешбэка", "Проверить товар перед покупкой", "Всё в одном месте"] },
  },

  // ICP-04 — S, «проверь товар»: hero + smart-блок (нейросеть против отзывов / лучшая цена)
  s: {
    id: "s", label: "S — проверь товар",
    hero: { lines: ["Проверь товар ", "до покупки"],
      subtitle: "ИИ оценит продавца, отзывы и риск подделки — честно: брать или рискованно." },
    sections: { marketplaces: false, steps: false, compare: false, reviews: true },
    modal: { title: "Ранний доступ",
      subtitle: "Оставьте email или телефон — позовём первыми проверять товары до покупки.",
      intentQuestion: "Что для вас сейчас важнее?",
      intentOptions: ["Не нарваться на подделку", "Надёжность продавца", "Честные ли отзывы", "Вернуть часть денег"] },
  },

  // ICP-02 — A, «суть страницы»: hero + smart-блок
  a: {
    id: "a", label: "A — суть без копипаста",
    hero: { lines: ["Суть любой статьи — ", "в один тап"],
      subtitle: "ИИ читает прямо на открытой странице. Без копипаста и прыжков по вкладкам." },
    sections: { marketplaces: false, steps: false, compare: false, reviews: true },
    modal: { title: "Ранний доступ",
      subtitle: "Оставьте email или телефон — позовём первыми, когда откроем ранний доступ.",
      intentQuestion: "Что бы вы делали чаще?",
      intentOptions: ["Сжимать длинные статьи", "Разбираться в теме", "Разгребать сохранённое", "Перевод и сжатие"] },
  },

  // ICP-03 — студенты, A + co-C: hero + smart-блок + пилюли кешбэка
  students: {
    id: "students", label: "Студенты — со ссылками + кешбэк",
    hero: { lines: ["Разберись в теме — ", "со ссылками"],
      subtitle: "ИИ объяснит с проверяемыми источниками. И вернёт часть денег с покупок." },
    sections: { marketplaces: true, steps: false, compare: false, reviews: true },
    modal: { title: "Ранний доступ",
      subtitle: "Оставьте email или телефон — позовём первыми из листа ожидания.",
      intentQuestion: "Что важнее для учёбы?",
      intentOptions: ["Быстро понять тему", "Источники, которым верить", "Сэкономить на покупках", "Собрать инфо"] },
  },

  // ICP-01 — AI-power, только механика (без кешбэка): hero + smart-блок
  power: {
    id: "power", label: "AI-power — без копипаста",
    hero: { lines: ["ИИ на открытой ", "странице"],
      subtitle: "Хватит копировать в чат. ИИ видит то, что открыто — страница, PDF, вкладки." },
    sections: { marketplaces: false, steps: false, compare: false, reviews: true },
    modal: { title: "Ранний доступ",
      subtitle: "Эксперимент для тех, кто живёт в ИИ-инструментах. Зовём первых.",
      intentQuestion: "Что бы вы делали чаще?",
      intentOptions: ["Вопросы по странице", "Синтез вкладок", "PDF и документы", "Ресёрч по вебу"] },
  },
};

export const VariantContext = createContext<LandingVariant>(DEFAULT_VARIANT);

export function pickVariant(search: string): LandingVariant {
  const id = new URLSearchParams(search).get("v");
  return (id && variants[id]) || DEFAULT_VARIANT;
}
