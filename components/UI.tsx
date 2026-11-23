"use client";
import Link from "next/link";
import { ArrowRight, Atom, CheckCircle2, ChevronRight, Circle, Sigma, Shapes, Sparkles } from "lucide-react";
import { type ReactNode } from "react";
import { chapterById, chaptersForTrack, lessonsForChapter, lessonsForTrack, lessonById, type Track } from "@/lib/curriculum";
import { useProgress } from "@/lib/progress";

export function ProgressBar({ percent, color = "violet", height = 8 }: { percent: number; color?: string; height?: number }) {
  return <div className="progress-track" style={{ height }} role="progressbar" aria-valuenow={percent} aria-valuemin={0} aria-valuemax={100}><div className={`progress-fill fill-${color}`} style={{ width: `${Math.max(0, Math.min(100, percent))}%` }} /></div>;
}
export function TrackSymbol({ track, size = 23 }: { track: Track; size?: number }) {
  const icons: Record<string, ReactNode> = { geometry: <Shapes size={size} />, "algebra-2": <Sigma size={size} />, "math-bridge": <Atom size={size} /> };
  return <span className={`track-symbol symbol-${track.color}`}>{icons[track.id]}</span>;
}
export function Eyebrow({ children }: { children: ReactNode }) { return <div className="eyebrow"><Sparkles size={13}/>{children}</div>; }
export function PageHeader({ eyebrow, title, description, action }: { eyebrow?: string; title: string; description?: string; action?: ReactNode }) {
  return <div className="page-heading"><div>{eyebrow && <Eyebrow>{eyebrow}</Eyebrow>}<h1>{title}</h1>{description && <p className="muted intro-text">{description}</p>}</div>{action}</div>;
}
export function TrackCard({ track }: { track: Track }) {
  const { progress } = useProgress();
  const items = lessonsForTrack(track.id);
  const completed = items.filter(item => progress[item.id]?.completed).length;
  const percentage = Math.round(completed/items.length*100);
  const chapters = chaptersForTrack(track.id);
  return <Link href={`/track/${track.id}`} className={`track-card card-${track.color}`}>
    <div className="track-card-top"><TrackSymbol track={track}/><span className="track-level">{track.id==="math-bridge" ? "EXTENSION" : "CORE TRACK"}</span></div>
    <div><h3>{track.title}</h3><p>{track.subtitle}</p></div>
    <div className="track-bottom"><div className="track-metrics"><span>{chapters.length} chapters</span><span className="dot-separator">·</span><span>{items.length} lessons</span></div><div className="track-completion"><strong>{percentage}%</strong><ProgressBar percent={percentage} color={track.color} /></div><div className="track-cta">Explore track <ArrowRight size={16}/></div></div>
  </Link>;
}
export function Breadcrumbs({ parts }: { parts: { title: string; href?: string }[] }) {
  return <nav aria-label="Breadcrumb" className="breadcrumbs">{parts.map((part, i) => <span key={`${part.title}-${i}`}>{i>0 && <ChevronRight size={14} />}{part.href ? <Link href={part.href}>{part.title}</Link> : <span aria-current="page">{part.title}</span>}</span>)}</nav>;
}
export function LessonRow({ lessonId, index }: { lessonId: string; index: number }) {
  const { progress } = useProgress();
  const lesson = lessonById(lessonId);
  if (!lesson) return null;
  const complete = progress[lesson.id]?.completed;
  return <Link href={`/learn/${lesson.id}`} className="lesson-row">
    <span className={`lesson-status ${complete ? "done" : ""}`}>{complete ? <CheckCircle2 size={19}/> : <Circle size={19}/>}</span>
    <div className="lesson-row-copy"><span className="small-overline">LESSON {index}</span><strong>{lesson.title}</strong><small>{lesson.estimatedMinutes} min lesson · 20 practice questions</small></div>
    <ChevronRight className="chevron" size={18}/>
  </Link>;
}
export function ChapterCard({ chapterId }: { chapterId: string }) {
  const chapter = chapterById(chapterId); const { tests, progress } = useProgress();
  if (!chapter) return null;
  const sub = lessonsForChapter(chapter.id);
  const complete = sub.filter(l => progress[l.id]?.completed).length;
  const attempts = tests.filter(t => t.chapterId === chapter.id);
  const best = attempts.length ? Math.max(...attempts.map(t => Math.round(t.score/t.total*100))) : null;
  return <article className="chapter-card"><div className="chapter-head"><div className="chapter-number">{String(chapter.order).padStart(2,"0")}</div><div className="chapter-head-main"><span className="small-overline">CHAPTER {chapter.order}</span><h3>{chapter.title}</h3><p>{chapter.description}</p></div><span className="chapter-count">{complete}/{sub.length} lessons</span></div>
    <div className="chapter-lessons">{sub.map((lesson, i) => <LessonRow key={lesson.id} lessonId={lesson.id} index={i+1}/>)}</div>
    <div className="chapter-test-link"><div className="test-icon">★</div><div><strong>Chapter checkpoint</strong><small>10 questions · Independent assessment {best!==null?`· Best score: ${best}%`:""}</small></div><Link href={`/test/${chapter.id}`} className="button button-outline button-sm">{best===null?"Take test":"Retake test"} <ArrowRight size={16}/></Link></div>
  </article>;
}
