"use client";

import { Activity, CheckCircle2, AlertCircle, FileText, Cpu, Search } from "lucide-react";
import { InvestigationStep } from "@/lib/types";

interface RightActivityFeedProps {
  steps: InvestigationStep[];
  progressPct?: number;
}

export default function RightActivityFeed({ steps, progressPct = 100 }: RightActivityFeedProps) {
  return (
    <div className="w-full lg:w-80 border-l border-slate-800 bg-slate-950 p-4 flex flex-col h-full overflow-y-auto">
      <div className="mb-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-[10px] font-mono uppercase tracking-widest text-slate-400 flex items-center gap-1">
            <Activity className="w-3.5 h-3.5 text-sky-400" />
            Investigation Status
          </span>
          <span className="text-xs font-mono font-bold text-sky-400">{progressPct}%</span>
        </div>
        <div className="w-full bg-slate-900 rounded-full h-2 overflow-hidden border border-slate-800">
          <div className="bg-sky-500 h-full rounded-full transition-all duration-500" style={{ width: `${progressPct}%` }}></div>
        </div>

        <div className="grid grid-cols-2 gap-2 mt-3 text-[11px] font-mono">
          <div className="p-2 bg-slate-900/80 border border-slate-800 rounded">
            <span className="text-slate-400 block text-[10px]">Sources Analyzed</span>
            <span className="text-slate-200 font-bold text-sm">17</span>
          </div>
          <div className="p-2 bg-slate-900/80 border border-slate-800 rounded">
            <span className="text-slate-400 block text-[10px]">Facts Extracted</span>
            <span className="text-slate-200 font-bold text-sm">43</span>
          </div>
          <div className="p-2 bg-slate-900/80 border border-slate-800 rounded">
            <span className="text-slate-400 block text-[10px]">Entities Resolved</span>
            <span className="text-slate-200 font-bold text-sm">9</span>
          </div>
          <div className="p-2 bg-rose-950/40 border border-rose-900/60 rounded">
            <span className="text-rose-400 block text-[10px]">Contradictions</span>
            <span className="text-rose-300 font-bold text-sm">3</span>
          </div>
        </div>
      </div>

      <div className="flex-1">
        <span className="text-[10px] font-mono uppercase tracking-widest text-slate-400 block mb-3">Live Activity Stream</span>
        <div className="space-y-3 font-mono text-xs">
          {steps.map((step, idx) => {
            const isAlert = step.step_type.includes("CONTRADICTION") || step.step_type.includes("RED_TEAM");
            return (
              <div key={idx} className="flex items-start space-x-2 text-slate-300">
                {isAlert ? (
                  <AlertCircle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
                ) : (
                  <CheckCircle2 className="w-4 h-4 text-sky-400 shrink-0 mt-0.5" />
                )}
                <div>
                  <span className={`font-semibold block ${isAlert ? "text-rose-300" : "text-slate-200"}`}>
                    {step.title}
                  </span>
                  <span className="text-[11px] text-slate-400 leading-tight block mt-0.5">{step.detail}</span>
                  <span className="text-[9px] text-slate-500 block mt-0.5">
                    {strTime(step.timestamp)}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

function strTime(val: any): string {
  if (!val) return "00:00:00";
  return String(val).slice(11, 19) || "00:00:00";
}
