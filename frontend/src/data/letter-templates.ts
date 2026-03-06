// Normalized stroke data for 27 Hebrew letters (22 regular + 5 sofit)
// Each stroke is an array of {x, y} points normalized to 0-1 range
// Letters are drawn right-to-left as in Hebrew writing

export interface StrokePoint {
  x: number;
  y: number;
}

export interface LetterTemplate {
  letter: string;
  name: string;
  name_ru: string;
  strokes: StrokePoint[][];
}

export const LETTER_TEMPLATES: LetterTemplate[] = [
  {
    letter: "א", name: "Alef", name_ru: "Алеф",
    strokes: [
      [{ x: 0.7, y: 0.2 }, { x: 0.5, y: 0.5 }, { x: 0.3, y: 0.8 }],
      [{ x: 0.8, y: 0.7 }, { x: 0.6, y: 0.5 }],
      [{ x: 0.4, y: 0.5 }, { x: 0.2, y: 0.3 }],
    ],
  },
  {
    letter: "ב", name: "Bet", name_ru: "Бет",
    strokes: [
      [{ x: 0.8, y: 0.2 }, { x: 0.8, y: 0.8 }, { x: 0.2, y: 0.8 }],
      [{ x: 0.8, y: 0.2 }, { x: 0.3, y: 0.2 }],
    ],
  },
  {
    letter: "ג", name: "Gimel", name_ru: "Гимель",
    strokes: [
      [{ x: 0.6, y: 0.2 }, { x: 0.6, y: 0.6 }, { x: 0.5, y: 0.8 }],
      [{ x: 0.6, y: 0.6 }, { x: 0.4, y: 0.8 }],
    ],
  },
  {
    letter: "ד", name: "Dalet", name_ru: "Далет",
    strokes: [
      [{ x: 0.8, y: 0.2 }, { x: 0.3, y: 0.2 }],
      [{ x: 0.8, y: 0.2 }, { x: 0.8, y: 0.8 }],
    ],
  },
  {
    letter: "ה", name: "He", name_ru: "hей",
    strokes: [
      [{ x: 0.8, y: 0.2 }, { x: 0.3, y: 0.2 }],
      [{ x: 0.8, y: 0.2 }, { x: 0.8, y: 0.8 }],
      [{ x: 0.3, y: 0.4 }, { x: 0.3, y: 0.8 }],
    ],
  },
  {
    letter: "ו", name: "Vav", name_ru: "Вав",
    strokes: [
      [{ x: 0.5, y: 0.2 }, { x: 0.5, y: 0.8 }],
    ],
  },
  {
    letter: "ז", name: "Zayin", name_ru: "Зайин",
    strokes: [
      [{ x: 0.7, y: 0.2 }, { x: 0.3, y: 0.2 }],
      [{ x: 0.5, y: 0.2 }, { x: 0.5, y: 0.8 }],
    ],
  },
  {
    letter: "ח", name: "Chet", name_ru: "Хет",
    strokes: [
      [{ x: 0.8, y: 0.2 }, { x: 0.2, y: 0.2 }],
      [{ x: 0.8, y: 0.2 }, { x: 0.8, y: 0.8 }],
      [{ x: 0.2, y: 0.2 }, { x: 0.2, y: 0.8 }],
    ],
  },
  {
    letter: "ט", name: "Tet", name_ru: "Тет",
    strokes: [
      [{ x: 0.2, y: 0.8 }, { x: 0.2, y: 0.3 }, { x: 0.5, y: 0.2 }, { x: 0.8, y: 0.3 }, { x: 0.8, y: 0.8 }],
    ],
  },
  {
    letter: "י", name: "Yod", name_ru: "Йуд",
    strokes: [
      [{ x: 0.6, y: 0.2 }, { x: 0.5, y: 0.4 }],
    ],
  },
  {
    letter: "כ", name: "Kaf", name_ru: "Каф",
    strokes: [
      [{ x: 0.8, y: 0.2 }, { x: 0.3, y: 0.2 }, { x: 0.2, y: 0.5 }, { x: 0.3, y: 0.8 }, { x: 0.8, y: 0.8 }],
    ],
  },
  {
    letter: "ך", name: "Kaf Sofit", name_ru: "Каф софит",
    strokes: [
      [{ x: 0.8, y: 0.2 }, { x: 0.3, y: 0.2 }, { x: 0.2, y: 0.5 }, { x: 0.2, y: 1.0 }],
    ],
  },
  {
    letter: "ל", name: "Lamed", name_ru: "Ламед",
    strokes: [
      [{ x: 0.5, y: 0.0 }, { x: 0.6, y: 0.3 }, { x: 0.4, y: 0.5 }, { x: 0.3, y: 0.8 }],
    ],
  },
  {
    letter: "מ", name: "Mem", name_ru: "Мем",
    strokes: [
      [{ x: 0.8, y: 0.2 }, { x: 0.5, y: 0.2 }, { x: 0.2, y: 0.5 }, { x: 0.2, y: 0.8 }],
      [{ x: 0.8, y: 0.2 }, { x: 0.8, y: 0.8 }, { x: 0.2, y: 0.8 }],
    ],
  },
  {
    letter: "ם", name: "Mem Sofit", name_ru: "Мем софит",
    strokes: [
      [{ x: 0.8, y: 0.2 }, { x: 0.2, y: 0.2 }, { x: 0.2, y: 0.8 }, { x: 0.8, y: 0.8 }, { x: 0.8, y: 0.2 }],
    ],
  },
  {
    letter: "נ", name: "Nun", name_ru: "Нун",
    strokes: [
      [{ x: 0.7, y: 0.2 }, { x: 0.3, y: 0.2 }],
      [{ x: 0.3, y: 0.2 }, { x: 0.3, y: 0.8 }],
    ],
  },
  {
    letter: "ן", name: "Nun Sofit", name_ru: "Нун софит",
    strokes: [
      [{ x: 0.5, y: 0.2 }, { x: 0.5, y: 1.0 }],
    ],
  },
  {
    letter: "ס", name: "Samekh", name_ru: "Самех",
    strokes: [
      [{ x: 0.8, y: 0.2 }, { x: 0.2, y: 0.2 }, { x: 0.2, y: 0.8 }, { x: 0.8, y: 0.8 }, { x: 0.8, y: 0.2 }],
    ],
  },
  {
    letter: "ע", name: "Ayin", name_ru: "Айин",
    strokes: [
      [{ x: 0.7, y: 0.2 }, { x: 0.5, y: 0.5 }, { x: 0.3, y: 0.8 }],
      [{ x: 0.3, y: 0.2 }, { x: 0.5, y: 0.5 }, { x: 0.7, y: 0.8 }],
    ],
  },
  {
    letter: "פ", name: "Pe", name_ru: "Пэй",
    strokes: [
      [{ x: 0.8, y: 0.2 }, { x: 0.3, y: 0.2 }, { x: 0.2, y: 0.5 }, { x: 0.3, y: 0.7 }, { x: 0.6, y: 0.7 }],
      [{ x: 0.8, y: 0.2 }, { x: 0.8, y: 0.8 }],
    ],
  },
  {
    letter: "ף", name: "Pe Sofit", name_ru: "Пэй софит",
    strokes: [
      [{ x: 0.8, y: 0.2 }, { x: 0.3, y: 0.2 }, { x: 0.2, y: 0.5 }, { x: 0.3, y: 0.7 }, { x: 0.6, y: 0.7 }],
      [{ x: 0.8, y: 0.2 }, { x: 0.8, y: 1.0 }],
    ],
  },
  {
    letter: "צ", name: "Tsadi", name_ru: "Цади",
    strokes: [
      [{ x: 0.3, y: 0.3 }, { x: 0.3, y: 0.8 }],
      [{ x: 0.7, y: 0.2 }, { x: 0.5, y: 0.5 }, { x: 0.3, y: 0.8 }],
    ],
  },
  {
    letter: "ץ", name: "Tsadi Sofit", name_ru: "Цади софит",
    strokes: [
      [{ x: 0.3, y: 0.3 }, { x: 0.3, y: 0.6 }],
      [{ x: 0.7, y: 0.2 }, { x: 0.5, y: 0.5 }, { x: 0.3, y: 0.6 }, { x: 0.3, y: 1.0 }],
    ],
  },
  {
    letter: "ק", name: "Qof", name_ru: "Куф",
    strokes: [
      [{ x: 0.8, y: 0.2 }, { x: 0.3, y: 0.2 }],
      [{ x: 0.8, y: 0.2 }, { x: 0.8, y: 0.8 }],
      [{ x: 0.3, y: 0.2 }, { x: 0.3, y: 1.0 }],
    ],
  },
  {
    letter: "ר", name: "Resh", name_ru: "Реш",
    strokes: [
      [{ x: 0.8, y: 0.2 }, { x: 0.3, y: 0.2 }],
      [{ x: 0.8, y: 0.2 }, { x: 0.8, y: 0.8 }],
    ],
  },
  {
    letter: "ש", name: "Shin", name_ru: "Шин",
    strokes: [
      [{ x: 0.2, y: 0.8 }, { x: 0.2, y: 0.3 }, { x: 0.3, y: 0.2 }],
      [{ x: 0.5, y: 0.2 }, { x: 0.5, y: 0.8 }],
      [{ x: 0.7, y: 0.2 }, { x: 0.8, y: 0.3 }, { x: 0.8, y: 0.8 }],
    ],
  },
  {
    letter: "ת", name: "Tav", name_ru: "Тав",
    strokes: [
      [{ x: 0.8, y: 0.2 }, { x: 0.3, y: 0.2 }],
      [{ x: 0.8, y: 0.2 }, { x: 0.8, y: 0.8 }],
      [{ x: 0.3, y: 0.2 }, { x: 0.2, y: 0.5 }, { x: 0.3, y: 0.8 }],
    ],
  },
];
