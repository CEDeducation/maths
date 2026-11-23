import type { Metadata } from "next";
import "./globals.css";
import { ProgressProvider } from "@/lib/progress";
import AppShell from "@/components/AppShell";
export const metadata: Metadata = {
  title: { default: "arcMath — Learn Grade 10 Mathematics", template: "%s | arcMath" },
  description: "Original, step-by-step Grade 10 Geometry, Algebra 2 and Math Bridge lessons, with 20 practice questions per subtopic and chapter tests.",
  icons: { icon: "/favicon.svg" }
};
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body><ProgressProvider><AppShell>{children}</AppShell></ProgressProvider></body></html>;
}
