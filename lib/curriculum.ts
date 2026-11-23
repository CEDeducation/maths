import raw from "@/data/curriculum.json";
import rawQuestions from "@/data/question-bank.json";
import rawTestQuestions from "@/data/checkpoint-bank.json";

export type Track = {
  id: string; title: string; subtitle: string; description: string;
  color: string; icon: string; level: string;
};
export type Chapter = {
  id: string; trackId: string; title: string; description: string; order: number;
};
export type Lesson = {
  id: string; chapterId: string; title: string; summary: string;
  ideas: string[]; formulas: string[];
  workedExample: { prompt: string; steps: string[] };
  commonMistake: string; realWorld: string; order: number; estimatedMinutes: number;
};
export type Question = {
  id: string; lessonId: string; prompt: string; options: string[];
  answerIndex: number; hints: string[]; explanation: string[];
  type: "multiple-choice"; difficulty: string; skill: string;
};
export const tracks: Track[] = raw.tracks;
export const chapters: Chapter[] = raw.chapters;
export const lessons: Lesson[] = raw.lessons;
export const questions: Question[] = rawQuestions as Question[];
export const testQuestions: Question[] = rawTestQuestions as Question[];
export const trackById = (id: string) => tracks.find(t => t.id === id);
export const chapterById = (id: string) => chapters.find(c => c.id === id);
export const lessonById = (id: string) => lessons.find(l => l.id === id);
export const chaptersForTrack = (id: string) => chapters.filter(c => c.trackId === id);
export const lessonsForChapter = (id: string) => lessons.filter(l => l.chapterId === id);
export const lessonsForTrack = (id: string) => lessons.filter(l => chapterById(l.chapterId)?.trackId === id);
export const questionsForLesson = (id: string) => questions.filter(q => q.lessonId === id);

/** 10 independent checkpoint questions, from a separate unseen test bank. */
export function questionsForTest(chapterId: string): Question[] {
  const childLessons = lessonsForChapter(chapterId);
  if (!childLessons.length) return [];
  const picked: Question[] = [];
  const slots = [4, 3, 3];
  childLessons.forEach((lesson, lessonIndex) => {
    const pool = testQuestions.filter(q => q.lessonId === lesson.id);
    for (let i = 0; i < (slots[lessonIndex] ?? 3); i++) {
      picked.push(pool[i]);
    }
  });
  return picked.filter(Boolean);
}
export const TOTAL_PRACTICE = lessons.length * 20;
export const TOTAL_TESTS = chapters.length;
