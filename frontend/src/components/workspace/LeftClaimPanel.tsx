"use client";

import { CheckCircle2, AlertTriangle, HelpCircle, Layers, FileCode } from "lucide-react";
import { AtomicClaim } from "@/lib/types";

interface LeftClaimPanelProps {
  originalClaim: string;
  atomicClaims: AtomicClaim[];
  onSelectAtomicClaim?: (ac: AtomicClaim) => void;
}

export default function LeftClaimPanel({ originalClaim, atomicClaims, onSelectAtomicClaim }: LeftClaimPanelProps) {
  return (
    <div className="w-full lg:w-80 border-r border-slate-800 bg-slate-950 p-4 flex flex-col h-full overflow-y-auto">
      <div className="mb-4">
        <span className="text-[10px] font-mono uppercase tracking-widest text-slate-400 flex items-center gap-1">
          <Layers className="w-3.5 h-3.5 text-sky-400" />
          Primary Claim Statement
        </span>
        <div className="mt-2 p-3 bg-slate-900/90 border border-slate-800 rounded-lg">
          <p className="text-xs text-slate-200 leading-relaxed font-sans italic">"{originalClaim}"</p>
        </div>
      </div>

      <div className="flex-1">
        <div className="flex items-center justify-between mb-3">
          <span className="text-[10px] font-mono uppercase tracking-widest text-slate-400">Atomic Claims ({atomicClaims.length})</span>
          <span className="text-[10px] font-mono text-sky-400">Click to Inspect</span>
        </div>

        <div className="space-y-2.5">
          {atomicClaims.map((ac, idx) => {
            const isDeadline = ac.statement.toLowerCase().includes("deadline") || ac.statement.toLowerCase().includes("before");
            const isContradicted = isDeadline || ac.contradiction_count > 0;

            return (
              <div
                key={ac.id || idx}
                onClick={() => onSelectAtomicClaim && onSelectAtomicClaim(ac)}
                className="p-3 rounded-lg border bg-slate-900/60 border-slate-800 hover:border-sky-700 cursor-pointer transition flex flex-col gap-2 group"
              >
                <div className="flex items-start justify-between gap-2">
                  <div className="flex items-center gap-1.5">
                    {isContradicted ? (
                      <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
                    ) : (
                      <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                    )}
                    <span className="text-xs font-medium text-slate-200 group-hover:text-sky-300 transition">
                      {ac.statement}
                    </span>
                  </div>
                </div>

                <div className="flex items-center justify-between text-[11px] font-mono text-slate-400 pt-1 border-t border-slate-800/60">
                  <span className="flex items-center gap-1">
                    <FileCode className="w-3 h-3 text-slate-500" />
                    Reqs: {ac.verification_requirements_json.length}
                  </span>
                  {isContradicted ? (
                    <span className="text-rose-400 bg-rose-950/80 px-1.5 py-0.5 rounded text-[10px] border border-rose-800">CONTRADICTED</span>
                  ) : (
                    <span className="text-emerald-400 bg-emerald-950/80 px-1.5 py-0.5 rounded text-[10px] border border-emerald-800">SUPPORTED</span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
