"use client";

import Link from "next/link";
import { Cpu, ShieldCheck } from "lucide-react";

export default function AIStatusBadge() {
  return (
    <Link
      href="/ai-transparency"
      className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-sky-950/80 border border-sky-800 text-sky-400 font-mono text-[11px] font-semibold hover:border-sky-600 transition"
      title="Click to view AI & Deterministic Verification Architecture"
    >
      <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
      AI ENGINE ACTIVE
      <span className="text-[9px] text-slate-400 border-l border-sky-800 pl-1.5 hidden sm:inline">
        LLM + Python Verification
      </span>
    </Link>
  );
}
