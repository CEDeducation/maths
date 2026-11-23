import Link from "next/link";
export default function NotFound(){return <div className="blank-state"><h1>Oops, this page is missing.</h1><p>There&apos;s still plenty to explore.</p><Link href="/" className="button button-primary">Back to dashboard</Link></div>}
