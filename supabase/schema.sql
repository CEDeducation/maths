-- arcMath student progress schema (Supabase SQL Editor)
-- Run this ONCE after creating a new Supabase project.
-- No service role key is needed in the frontend. Auth uses Supabase email/password.

create table if not exists public.lesson_progress (
  user_id uuid not null references auth.users(id) on delete cascade,
  lesson_id text not null,
  completed boolean not null default false,
  best_score integer not null default 0 check (best_score between 0 and 20),
  attempts integer not null default 0 check (attempts >= 0),
  updated_at timestamptz not null default now(),
  primary key (user_id, lesson_id)
);

create table if not exists public.chapter_attempts (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  chapter_id text not null,
  score integer not null check (score between 0 and 10),
  total integer not null default 10 check (total = 10),
  answers jsonb not null default '[]'::jsonb,
  created_at timestamptz not null default now()
);

create index if not exists chapter_attempts_user_created_idx
  on public.chapter_attempts(user_id, created_at desc);

-- PRIVACY: row-level security restricts student records to their own login.
alter table public.lesson_progress enable row level security;
alter table public.chapter_attempts enable row level security;

create policy "Students read their own lesson progress"
  on public.lesson_progress for select to authenticated
  using ((select auth.uid()) = user_id);
create policy "Students insert their own lesson progress"
  on public.lesson_progress for insert to authenticated
  with check ((select auth.uid()) = user_id);
create policy "Students update their own lesson progress"
  on public.lesson_progress for update to authenticated
  using ((select auth.uid()) = user_id)
  with check ((select auth.uid()) = user_id);
create policy "Students read their own test attempts"
  on public.chapter_attempts for select to authenticated
  using ((select auth.uid()) = user_id);
create policy "Students insert their own test attempts"
  on public.chapter_attempts for insert to authenticated
  with check ((select auth.uid()) = user_id);

-- Grant table access; RLS above enforces ownership even with an anon browser key.
grant select, insert, update on public.lesson_progress to authenticated;
grant select, insert on public.chapter_attempts to authenticated;
