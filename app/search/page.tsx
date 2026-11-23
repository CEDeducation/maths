"use client";
import Link from "next/link";
import { useState } from "react";
import { ArrowRight, BookOpenText, Search } from "lucide-react";
import { PageHeader } from "@/components/UI";
import { chapterById, lessons, trackById } from "@/lib/curriculum";
import { useProgress } from "@/lib/progress";
export default function SearchPage(){
 const [text,setText]=useState("");const [track,setTrack]=useState("all");const {progress}=useProgress();
 const filtered=lessons.filter(l=>{const c=chapterById(l.chapterId)!;return (track==="all"||c.trackId===track)&&`${l.title} ${l.summary} ${c.title}`.toLowerCase().includes(text.trim().toLowerCase())});
 return <div className="page-enter"><PageHeader eyebrow="THE LESSON LIBRARY" title="Find what you need" description="Search all 39 subtopic lessons across our three math tracks."/><div className="search-panel"><div className="search-input-wrap"><Search size={21}/><input value={text} onChange={e=>setText(e.target.value)} autoFocus placeholder="Try ‘quadratics’, ‘trigonometry’, ‘probability’…" aria-label="Search lessons"/></div><div className="filter-tabs">{[{id:"all",label:"All lessons"},{id:"geometry",label:"Geometry"},{id:"algebra-2",label:"Algebra 2"},{id:"math-bridge",label:"Math Bridge"}].map(t=><button key={t.id} onClick={()=>setTrack(t.id)} className={track===t.id?"selected":""}>{t.label}</button>)}</div></div><div className="search-count">{filtered.length} lessons found</div><div className="search-results">{filtered.length?filtered.map(l=>{const c=chapterById(l.chapterId)!;const t=trackById(c.trackId)!;return <Link key={l.id} href={`/learn/${l.id}`} className="search-result"><div className={`search-result-icon icon-${t.color}`}><BookOpenText size={20}/></div><div><small>{t.title} · {c.title}</small><h3>{l.title}</h3><p>{l.summary}</p></div>{progress[l.id]?.completed?<span className="completed-tag">Completed</span>:<ArrowRight size={19}/>}</Link>}):<div className="blank-state"><Search size={32}/><strong>Nothing matches yet</strong><p>Try a shorter keyword or choose another track.</p></div>}</div></div>;
}
