# arcMath — Grade 10 Math Learning Studio

A **real React/Next.js learning platform** for Grade 10 students in American/international schools in Taiwan, deployable on Vercel with optional Supabase authentication and synced progress. Original content, inspired by the **learning experience** of guided mastery platforms—not copied lessons or branding.

## What's included

- **3 placement-aware tracks**: Geometry, Algebra 2, and Math Bridge (Statistics/Precalculus extension).
- **13 chapters and 39 fully written subtopic lessons** with conceptual explanations, formulas, practical applications, worked examples, and common mistakes.
- **20 multiple-choice practice questions per subtopic: 780 questions total.** Two sequential hints and worked feedback, a private scratchpad, practice scoring and retry.
- **End-of-chapter checkpoint test** for each of 13 chapters, 10 questions each drawn from a separate 195-question checkpoint bank, with scoring, review and retakes.
- Student dashboard, progress dashboard, library search, **interactive graphing lab with quadratic/linear/sine sliders**, responsive design, email/password sign-up and sign-in.
- Guest mode works without Supabase; progress saves to **browser localStorage**. With Supabase configured, authenticated progress saves in **Postgres**, protected by row-level security (RLS).

> **Scope:** This is a working, deployable learning MVP, not a complete full-service school LMS. The question pools are deterministic and based on 2 targeted question patterns per subtopic. All tests are *formative*, with answer keys in client-side JSON. For high-stakes exams, move assessment grading and the test bank server-side, and commission professional curriculum review. There are no video lessons, teacher/admin accounts, or custom question editor yet.

## 1. Run locally

Requires **Node.js 20.9+** and npm.

```bash
npm install
cp .env.example .env.local
npm run dev
```

Open **http://localhost:3000**. Without real Supabase values, use the platform immediately as a **guest**; progress persists on your own device.

## 2. Create your Supabase database

1. Visit https://supabase.com/dashboard and create a new project.
2. Open **SQL Editor**, create a query, paste the contents of **`supabase/schema.sql`**, and run it **once**. Tables are created with RLS enabled. (Policies are designed for a clean new project; rerunning the policy statements will report duplicate-policy errors.)
3. Under **Authentication → Providers**, enable Email if needed. You may require email confirmation.
4. Under **Authentication → URL Configuration**:
   - **Site URL**: your deployed `https://YOUR-PROJECT.vercel.app` (or `http://localhost:3000` while testing).
   - **Redirect URLs**: `http://localhost:3000/**` and `https://YOUR-PROJECT.vercel.app/**` (replace with real deployed URL). The app emails a confirmation link to `/auth`.
5. In **Project Settings → API Keys**, copy the **Project URL** and **publishable key** (or legacy `anon` public key). Put them in `.env.local`:

```env
NEXT_PUBLIC_SUPABASE_URL=https://YOUR_PROJECT.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=YOUR_PUBLIC_ANON_OR_PUBLISHABLE_KEY
```

**Never place a `service_role` or secret key in `NEXT_PUBLIC_...` variables.** The safe browser publishable key is constrained by the included RLS policies.

6. Restart `npm run dev`. Go to `/auth`, sign up, verify your email if required, and start practicing. Your account's progress is stored in Supabase.

## 3. Deploy to Vercel

1. Create a **private GitHub repository**; upload all files from this folder. Do not commit `.env.local`.
2. On https://vercel.com/new, import the repository and select **Next.js**. Root Directory is the repository root.
3. Add these **Environment Variables** under the Vercel project:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
4. Select Production, Preview and Development as appropriate, then **Deploy**.
5. Add the deployed domain in Supabase Authentication URL Configuration. If you changed environment variables, redeploy.
6. Test `/api/health` and an actual signup → login → practice → progress flow.

Vercel auto-detects Next.js and usually needs no custom build settings. For a quick deployment without Supabase, you may skip environment variables, but only browser-local demo progress will work.

## 4. How content is organized

- `data/curriculum.json` — all track / chapter / lesson content, including theory, formulas and worked examples.
- `data/question-bank.json` — 780 practice problems with correct answers, two hints, explanations and difficulty labels.
- `data/checkpoint-bank.json` — 195 independent test items; each chapter draws 10.
- `scripts/generate_curriculum.py` — source data for curriculum.
- `scripts/generate_questions.py` — source for reproducible practice question generation.
- `lib/curriculum.ts` — typed selectors and chapter-test question selection.
- `lib/progress.tsx` — guest storage and Supabase progress saves.
- `supabase/schema.sql` — SQL schema and RLS policies.
- `app/` — Next.js App Router pages and styles.

To edit the syllabus, adjust `scripts/generate_curriculum.py`, then run `python scripts/generate_curriculum.py`. To change question patterns, edit `scripts/generate_questions.py` and run `python scripts/generate_questions.py`. In the existing version, each chapter has three subtopic lessons, each with 20 exercises. Run `python scripts/validate_content.py` for the integrity checks.

## 5. Student safety / future upgrades

- The app stores **email, lesson progress, and checkpoint answers** for signed-in users. The practice scratchpad stays in React state and is *not* uploaded.
- No advertising or student-to-student messaging is included.
- For institutional use with minors: review privacy notices, parental consent requirements where applicable, retention and deletion workflows, cybersecurity, accessibility, content accuracy, and school policies before production launch.
- For future work: teacher dashboard, verified server-side grading, admin content CMS, LaTeX editor, diagrams, Desmos-powered graphing, instructional videos, more diverse word problems, adaptive question generation, and school SSO.

## Content use

All course copy and generated questions in this package are newly written for this project. This project is **not affiliated with Khan Academy, Taipei American School or Kaohsiung American School**. The three tracks are broad U.S./MYP-friendly categories and are **not a verified course catalog for a specific school**.
