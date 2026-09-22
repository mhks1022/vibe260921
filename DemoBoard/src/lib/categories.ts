export const CATEGORIES = ["자유", "질문", "정보", "공지"] as const;
export type Category = (typeof CATEGORIES)[number];
