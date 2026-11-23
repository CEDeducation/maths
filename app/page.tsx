"use client";
import Link from "next/link";
import { ArrowRight, BookOpen, CheckCircle2, ClipboardCheck, Flame, Lightbulb, MoveUpRight, PlayCircle, Target, Trophy } from "lucide-react";
import HeroArt from "@/components/HeroArt";
import { Eyebrow, ProgressBar, TrackCard } from "@/components/UI";
import { chapters, lessons, lessonsForChapter, lessonsForTrack, tracks } from "@/lib/curriculum";
import { useProgress } from "@/lib/progress";

export default function Dashboard() {
  const { progress, tests, user } = useProgress();
  const completed = lessons.filter(l => progress[l.id]?.completed).length;
  const attempts = Object.values(progress).reduce((n,p)=>n+p.attempts,0);
  const scores = Object.values(progress).map(p=>p.bestScore);
  const accuracy = scores.length ? Math.round(scores.reduce((a,b)=>a+b,0)/scores.length/20*100) : 0;
  const next = lessons.find(l => !progress[l.id]?.completed) || lessons[0];
  const nextChapter = chapters.find(c => lessonsForChapter(c.id).some(l=>l.id===next.id));
  return <div className="dashboard page-enter">
    <div className="dashboard-welcome"><div><Eyebrow>YOUR PERSONAL LEARNING SPACE</Eyebrow><h1>Hey, {user ? "math explorer" : "future problem solver"} <span className="wave">✳</span></h1><p>One concept at a time. You&apos;re doing great by showing up.</p></div><div className="date-chip">GRADE 10 · ALL LEVELS</div></div>
    <section className="hero-banner"><div className="hero-copy"><span className="hero-pill"><Flame size={15}/> YOUR NEXT BIG AHA MOMENT</span><h2>Math makes sense<br/>when it <em>clicks.</em></h2><p>Clear explanations, guided examples, and enough practice to make every idea stick.</p><Link href={`/learn/${next.id}`} className="button button-white">Continue learning <ArrowRight size={18}/></Link></div><HeroArt /></section>
    <section className="stat-grid" aria-label="Learning statistics"><div className="stat-card"><span className="stat-icon stat-purple"><BookOpen size={21}/></span><div><small>Lessons mastered</small><strong>{completed}<span> / {lessons.length}</span></strong></div><span className="stat-trend">Keep going ↗</span></div><div className="stat-card"><span className="stat-icon stat-coral"><Target size={21}/></span><div><small>Practice sessions</small><strong>{attempts}</strong></div><span className="stat-trend">20 Qs per lesson</span></div><div className="stat-card"><span className="stat-icon stat-mint"><Trophy size={21}/></span><div><small>Best-score average</small><strong>{accuracy}<span>%</span></strong></div><span className="stat-trend">{tests.length} chapter tests</span></div></section>
    <section className="section"><div className="section-heading"><div><span className="section-kicker">CHOOSE YOUR PATH</span><h2>Explore your math tracks</h2><p>Pick the course that matches your class. No one-size-fits-all syllabus.</p></div><Link href="/search" className="subtle-link">Browse all lessons <ArrowRight size={16}/></Link></div><div className="track-grid">{tracks.map(track=><TrackCard key={track.id} track={track}/>)}</div></section>
    <div className="dashboard-lower"><section className="next-card"><div className="section-kicker">PICK UP WHERE YOU LEFT OFF</div><h2>Your next lesson</h2><div className="next-lesson"><span className="next-lesson-graphic"><PlayCircle size={35}/></span><div><span className="small-overline">{nextChapter?.title || "Geometry"}</span><h3>{next.title}</h3><p>{next.summary}</p></div><Link href={`/learn/${next.id}`} className="round-arrow" aria-label={`Open ${next.title}`}><MoveUpRight size={22}/></Link></div><ProgressBar percent={Math.round(completed/lessons.length*100)}/><div className="next-card-footer"><span>{completed} of {lessons.length} lessons completed</span><Link href="/progress">View progress <ArrowRight size={14}/></Link></div></section><aside className="tip-card"><span className="tip-icon"><Lightbulb size={26}/></span><span className="section-kicker">A LITTLE LEARNING TIP</span><h2>Understanding beats memorizing.</h2><p>Read the worked example. Try one question on your own. Then explain your reasoning out loud—it works!</p><div className="tip-illustration"><CheckCircle2 size={22}/><span>Learn</span><ArrowRight size={16}/><ClipboardCheck size={22}/><span>Practice</span></div></aside></div>
  </div>;
}
