"use client";

import Link from "next/link";
import { ShieldAlert, Database, Search, Cpu } from "lucide-react";

export default function Navbar() {
  return (
    <header className="border-b border-slate-800 bg-slate-950/80 backdrop-blur sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center space-x-3">
          <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-sky-500 to-blue-700 flex items-center justify-center shadow-lg shadow-sky-500/20">
            <ShieldAlert className="w-5 h-5 text-white" />
          </div>
          <div>
            <span className="font-bold text-lg tracking-wider text-slate-100 flex items-center gap-2">
              TRUTHCHAIN <span className="text-[10px] uppercase tracking-widest px-1.5 py-0.5 rounded bg-sky-950 border border-sky-800 text-sky-400 font-mono">v1.0 ENGINE</span>
            </span>
            <p className="text-xs text-slate-400 font-sans hidden sm:block">Evidence Intelligence Workstation</p>
          </div>
        </Link>

        <nav className="flex items-center space-x-6 text-sm">
          <Link href="/cases" className="text-slate-300 hover:text-sky-400 transition font-medium flex items-center gap-1.5">
            <Database className="w-4 h-4 text-sky-400" />
            Investigations
          </Link>
          <Link href="/investigate" className="bg-sky-600 hover:bg-sky-500 text-white px-4 py-1.5 rounded-md font-medium text-xs tracking-wide transition shadow-sm flex items-center gap-1.5">
            <Cpu className="w-4 h-4" />
            New Investigation
          </Link>
        </nav>
      </div>
    </header>
  );
}
