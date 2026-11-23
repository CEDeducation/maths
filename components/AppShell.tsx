"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { BarChart3, BookOpenText, Compass, GraduationCap, LayoutDashboard, LogIn, LogOut, Menu, Search, X, ArrowRight, ChartNoAxesCombined } from "lucide-react";
import { useState, type ReactNode } from "react";
import { useProgress } from "@/lib/progress";
import { lessons } from "@/lib/curriculum";

const nav = [
  { href: "/", label: "Dashboard", icon: LayoutDashboard },
  { href: "/track/geometry", label: "Geometry", icon: Compass },
  { href: "/track/algebra-2", label: "Algebra 2", icon: BookOpenText },
  { href: "/track/math-bridge", label: "Math Bridge", icon: GraduationCap },
  { href: "/progress", label: "My progress", icon: BarChart3 },
  { href: "/lab", label: "Graphing lab", icon: ChartNoAxesCombined },
  { href: "/search", label: "Find a lesson", icon: Search }
];

export default function AppShell({ children }: { children: ReactNode }) {
  const path = usePathname();
  const [open, setOpen] = useState(false);
  const { user, logout, progress, configured, syncing } = useProgress();
  const done = lessons.filter(l => progress[l.id]?.completed).length;
  const initial = user?.email?.[0]?.toUpperCase() || "S";
  return <div className="shell">
    {open && <button className="sidebar-overlay" onClick={() => setOpen(false)} aria-label="Close navigation" />}
    <aside className={`sidebar ${open ? "sidebar-open" : ""}`}>
      <div className="sidebar-top"><Link href="/" className="brand" onClick={() => setOpen(false)}><span className="brand-icon">∑</span><span><strong>arc<span>math</span></strong><small>LEARNING STUDIO</small></span></Link><button className="mobile-close icon-button" onClick={() => setOpen(false)} aria-label="Close menu"><X size={20}/></button></div>
      <div className="sidebar-label">WORKSPACE</div>
      <nav className="main-nav" aria-label="Main navigation">{nav.map(({ href, label, icon: Icon }) => <Link onClick={() => setOpen(false)} href={href} key={href} className={`nav-link ${path === href || (href !== "/" && href !== "/search" && path.startsWith(href + "/")) ? "active" : ""}`}><Icon size={19}/><span>{label}</span></Link>)}</nav>
      <div className="sidebar-spacer"/>
      <div className="sidebar-spotlight"><div className="spotlight-orb">✦</div><strong>Small steps. Big breakthroughs.</strong><p>Keep showing up. Every question builds a stronger you.</p><Link href="/track/geometry">Keep learning <ArrowRight size={14}/></Link></div>
      <div className="sidebar-footer"><span className="avatar">{initial}</span><div><strong>{user?.email?.split("@")[0] || "Guest learner"}</strong><small>{user ? (syncing ? "Syncing progress…" : "Supabase account") : (configured ? "Sign in to sync" : "Local demo mode")}</small></div>{user ? <button title="Sign out" className="footer-action" onClick={() => logout()}><LogOut size={17}/></button> : <Link title="Sign in" href="/auth" className="footer-action"><LogIn size={17}/></Link>}</div>
    </aside>
    <div className="app-area"><header className="topbar"><button className="mobile-menu icon-button" onClick={() => setOpen(true)} aria-label="Open navigation"><Menu size={23}/></button><div className="topbar-location">GRADE 10 <span>/</span> YOUR MATH SPACE</div><div className="topbar-right"><span className="topbar-progress"><span className="green-dot"/> {done}/{lessons.length} lessons completed</span><Link href="/search" className="icon-button topbar-search" aria-label="Search lessons"><Search size={19}/></Link><Link href={user ? "/progress" : "/auth"} className="topbar-avatar">{initial}</Link></div></header><main className="main-content">{children}</main><footer className="app-footer">arc<span>math</span> · Made for curious Grade 10 minds <span className="footer-note">Original practice content · Not affiliated with any school</span></footer></div>
  </div>;
}
