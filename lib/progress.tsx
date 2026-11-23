"use client";
import { createContext, useContext, useEffect, useState, useCallback, type ReactNode } from "react";
import type { User } from "@supabase/supabase-js";
import { supabase, supabaseConfigured } from "@/lib/supabase";

type LessonProgress = { lessonId: string; completed: boolean; bestScore: number; attempts: number; updatedAt: string };
type TestAttempt = { id: string; chapterId: string; score: number; total: number; answers: number[]; createdAt: string };
type SaveResult = { ok: boolean; message?: string };
type Context = {
  user: User | null; loading: boolean; syncing: boolean; configured: boolean;
  progress: Record<string, LessonProgress>; tests: TestAttempt[];
  savePractice: (lessonId: string, score: number, total: number) => Promise<SaveResult>;
  saveTest: (chapterId: string, score: number, total: number, answers: number[]) => Promise<SaveResult>;
  logout: () => Promise<void>;
};
const ProgressContext = createContext<Context | null>(null);
const KEY_P = "arcmath:practice:v1";
const KEY_T = "arcmath:tests:v1";
const readJson = <T,>(key: string, fallback: T): T => {
  try { const str = localStorage.getItem(key); return str ? JSON.parse(str) as T : fallback; } catch { return fallback; }
};

export function ProgressProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);
  const [progress, setProgress] = useState<Record<string, LessonProgress>>({});
  const [tests, setTests] = useState<TestAttempt[]>([]);

  useEffect(() => {
    setProgress(readJson(KEY_P, {}));
    setTests(readJson(KEY_T, []));
    if (!supabase) { setLoading(false); return; }
    const client = supabase;
    let active = true;
    client.auth.getUser().then(({ data }) => {
      if (active) { setUser(data.user); setLoading(false); }
    }).catch(() => { if (active) setLoading(false); });
    const { data: { subscription } } = client.auth.onAuthStateChange((_event, session) => {
      if (active) { setUser(session?.user ?? null); setLoading(false); }
    });
    return () => { active = false; subscription.unsubscribe(); };
  }, []);

  useEffect(() => {
    if (!supabase || !user) {
      setProgress(readJson(KEY_P, {}));
      setTests(readJson(KEY_T, []));
      return;
    }
    const client = supabase;
    let active = true;
    setSyncing(true);
    Promise.all([
      client.from("lesson_progress").select("lesson_id,completed,best_score,attempts,updated_at").eq("user_id", user.id),
      client.from("chapter_attempts").select("id,chapter_id,score,total,answers,created_at").eq("user_id", user.id).order("created_at", { ascending: false }).limit(200)
    ]).then(([p, t]) => {
      if (!active) return;
      if (!p.error) setProgress(Object.fromEntries((p.data ?? []).map((r) => [r.lesson_id, { lessonId: r.lesson_id, completed: r.completed, bestScore: r.best_score, attempts: r.attempts, updatedAt: r.updated_at }])));
      if (!t.error) setTests((t.data ?? []).map(r => ({ id: r.id, chapterId: r.chapter_id, score: r.score, total: r.total, answers: r.answers ?? [], createdAt: r.created_at })));
      setSyncing(false);
    }).catch(() => { if (active) setSyncing(false); });
    return () => { active = false; };
  }, [user?.id]);

  const savePractice = useCallback(async (lessonId: string, score: number, total: number): Promise<SaveResult> => {
    const existing = progress[lessonId];
    const now = new Date().toISOString();
    const next: LessonProgress = { lessonId, completed: total === 20 || Boolean(existing?.completed), bestScore: Math.max(score, existing?.bestScore ?? 0), attempts: (existing?.attempts ?? 0) + 1, updatedAt: now };
    if (user && supabase) {
      const { error } = await supabase.from("lesson_progress").upsert({ user_id: user.id, lesson_id: next.lessonId, completed: next.completed, best_score: next.bestScore, attempts: next.attempts, updated_at: now }, { onConflict: "user_id,lesson_id" });
      if (error) return { ok: false, message: "Could not save to Supabase. Check that you ran the SQL setup." };
      setProgress(old => ({ ...old, [lessonId]: next }));
      return { ok: true };
    }
    setProgress(old => {
      const merged = { ...old, [lessonId]: next };
      localStorage.setItem(KEY_P, JSON.stringify(merged));
      return merged;
    });
    return { ok: true, message: "Saved on this device (demo mode). Sign in to save to Supabase." };
  }, [progress, user]);

  const saveTest = useCallback(async (chapterId: string, score: number, total: number, answers: number[]): Promise<SaveResult> => {
    const attempt: TestAttempt = { id: crypto.randomUUID(), chapterId, score, total, answers, createdAt: new Date().toISOString() };
    if (user && supabase) {
      const { data, error } = await supabase.from("chapter_attempts").insert({ user_id: user.id, chapter_id: chapterId, score, total, answers }).select("id,created_at").single();
      if (error) return { ok: false, message: "Could not save to Supabase. Check your SQL tables and RLS policies." };
      setTests(old => [{ ...attempt, id: data.id, createdAt: data.created_at }, ...old]);
      return { ok: true };
    }
    setTests(old => {
      const merged = [attempt, ...old].slice(0, 200);
      localStorage.setItem(KEY_T, JSON.stringify(merged));
      return merged;
    });
    return { ok: true, message: "Saved on this device (demo mode)." };
  }, [user]);

  const logout = useCallback(async () => { await supabase?.auth.signOut(); setUser(null); }, []);

  return <ProgressContext.Provider value={{ user, loading, syncing, configured: supabaseConfigured, progress, tests, savePractice, saveTest, logout }}>{children}</ProgressContext.Provider>;
}
export function useProgress() { const ctx = useContext(ProgressContext); if (!ctx) throw new Error("useProgress must be inside ProgressProvider"); return ctx; }
export function useTrackStats(trackLessonIds: string[]) {
  const { progress } = useProgress();
  const completed = trackLessonIds.filter(id => progress[id]?.completed).length;
  const attempts = trackLessonIds.reduce((sum, id) => sum + (progress[id]?.attempts ?? 0), 0);
  const bestScores = trackLessonIds.map(id => progress[id]?.bestScore).filter((n): n is number => n !== undefined);
  return { completed, total: trackLessonIds.length, percentage: trackLessonIds.length ? Math.round(completed / trackLessonIds.length * 100) : 0, attempts, average: bestScores.length ? Math.round(bestScores.reduce((a,b)=>a+b,0)/bestScores.length/20*100) : 0 };
}
