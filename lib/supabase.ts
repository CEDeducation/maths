"use client";
import { createClient, type SupabaseClient } from "@supabase/supabase-js";

const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
const key = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
export const supabaseConfigured = Boolean(
  url && key && !url.includes("YOUR_PROJECT") && !key.includes("YOUR_PUBLIC")
);
// Browser-scoped client. The public anon key only works safely with database RLS enabled.
export const supabase: SupabaseClient | null = supabaseConfigured
  ? createClient(url!, key!, {
      auth: { autoRefreshToken: true, persistSession: true, detectSessionInUrl: true }
    })
  : null;
