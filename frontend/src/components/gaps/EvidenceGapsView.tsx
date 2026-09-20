"use client";

import { HelpCircle, FileSearch, ArrowRight, ShieldAlert } from "lucide-react";
import { EvidenceGap } from "@/lib/types";

interface EvidenceGapsViewProps {
  gaps: EvidenceGap[];
}

export default function EvidenceGapsView({ gaps }: EvidenceGapsViewProps) {
  return (
    <div className="p-6 max-w-5xl mx-auto space-y-6">
      <div>
        <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
          <HelpCircle className="w-5 h-5 text-amber-400" />
          Evidence Gap & Missing Information Analysis
        </h3>
        <p className="text-xs text-slate-400 mt-1">
          Identifies specific missing records required to convert unresolved claims into auditable verdicts.
        </p>
      </div>

      <div className="space-y-4">
        {gaps.map((gap, idx) => (
          <div key={gap.id || idx} className="p-4 rounded-xl border border-amber-900/60 bg-amber-950/20 space-y-3">
            <div className="flex items-center justify-between">
              <span className="font-mono text-xs font-bold text-amber-400 bg-amber-950/80 px-2 py-0.5 rounded border border-amber-800">
                EVIDENCE GAP #{idx + 1}
              </span>
              <span className="text-[10px] font-mono text-amber-300 uppercase">STATUS: {gap.status}</span>
            </div>

            <div>
              <span className="text-[10px] font-mono uppercase text-slate-400 block mb-1">Missing Evidence Description</span>
              <p className="text-xs text-slate-200 font-semibold">{gap.description}</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs pt-2 border-t border-amber-900/40">
              <div className="p-2.5 bg-slate-950/80 rounded border border-slate-800">
                <span className="text-[10px] font-mono text-amber-400 block mb-1 font-bold">WHY IT MATTERS</span>
                <p className="text-slate-300 leading-snug">{gap.why_it_matters}</p>
              </div>

              <div className="p-2.5 bg-slate-950/80 rounded border border-slate-800">
                <span className="text-[10px] font-mono text-sky-400 block mb-1 font-bold flex items-center gap-1">
                  <FileSearch className="w-3 h-3" /> NEXT BEST EVIDENCE REQUESTED
                </span>
                <p className="text-slate-300 italic leading-snug">"{gap.next_best_evidence}"</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
