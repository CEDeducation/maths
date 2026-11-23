"use client";
import Link from "next/link";
import { useParams } from "next/navigation";
import { ArrowRight, BookOpen, ChevronRight, ClipboardCheck, Clock3, Target } from "lucide-react";
import { Breadcrumbs, ChapterCard, PageHeader, ProgressBar, TrackSymbol } from "@/components/UI";
import { chapterById, chaptersForTrack, lessonsForTrack, trackById } from "@/lib/curriculum";
import { useProgress } from "@/lib/progress";
export default function TrackPage() {
  const { trackId } = useParams<{ trackId: string }>();
  const track = trackById(trackId); const { progress, tests } = useProgress();
  if (!track) return <div className="blank-state"><h1>Track not found.</h1><Link href="/">Back to dashboard</Link></div>;
  const chapterList = chaptersForTrack(track.id);const ls = lessonsForTrack(track.id);
  const done = ls.filter(l=>progress[l.id]?.completed).length;
  const pct = Math.round(done/ls.length*100);
  const trackTests = tests.filter(t=>chapterById(t.chapterId)?.trackId===track.id).length;
  return <div className="page-enter"><Breadcrumbs parts={[{title:"Dashboard",href:"/"},{title:track.title}]}/><div className={`track-intro intro-${track.color}`}><div><span className="track-intro-overline">{track.level.toUpperCase()}</span><h1>{track.title}</h1><h2>{track.subtitle}</h2><p>{track.description}</p><div className="track-intro-stats"><span><BookOpen size={16}/>{ls.length} lessons</span><span><ClipboardCheck size={16}/>{chapterList.length} chapter tests</span><span><Clock3 size={16}/>Learn at your pace</span></div></div><div className="track-intro-art"><TrackSymbol track={track} size={68}/></div></div><div className="track-progress-banner"><div><strong>Your journey</strong><span>{done}/{ls.length} lessons completed</span></div><ProgressBar percent={pct} color={track.color} height={10}/><span className="progress-percent">{pct}%</span></div>
  <div className="section-heading track-section-heading"><div><span className="section-kicker">COURSE ROADMAP</span><h2>Chapters & lessons</h2><p>Study the explanation, finish 20 practice questions, and then take your chapter checkpoint.</p></div><span className="lesson-total"><Target size={17}/>{trackTests} tests taken</span></div><div className="chapters-list">{chapterList.map(c=><ChapterCard key={c.id} chapterId={c.id}/>)}</div><div className="bottom-invite">Ready to dive in? <Link href={`/learn/${ls.find(l=>!progress[l.id]?.completed)?.id || ls[0].id}`}>Open your next lesson <ArrowRight size={16}/></Link></div></div>;
}
