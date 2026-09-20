"use client";

import { AlertTriangle, CheckCircle2, Search, ArrowRight, ShieldCheck, Calculator } from "lucide-react";
import { Contradiction, Hypothesis } from "@/lib/types";
import DeterministicVerificationCard from "../workspace/DeterministicVerificationCard";

interface ContradictionsViewProps {
  contradictions: Contradiction[];
  hypotheses: Hypothesis[];
}

export default function ContradictionsView({ contradictions, hypotheses }: ContradictionsViewProps) {
  return (
    <div className="p-6 max-w-5xl mx-auto space-y-6">
      <div>
        <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-rose-400" />
          Contradiction & Discrepancy Center
        </h3>
        <p className="text-xs text-slate-400 mt-1">
          Autonomous conflict detection between uploaded documents, carrier receipts, and contractual statements.
        </p>
      </div>

      {/* Deterministic Verification Python Logic Breakdown Cards */}
      <div>
        <span className="text-xs font-mono font-bold uppercase tracking-widest text-sky-400 block mb-2">
          Deterministic Code Verification Engine Output
        </span>
        <DeterministicVerificationCard
          orderedQty={10000}
          shipment1Qty={8500}
          shipment2Qty={1500}
          deadlineDate="Sep 15, 2026"
          actualDeliveryDate="Sep 17, 2026"
        />
      </div>

      <div className="space-y-4">
        <span className="text-xs font-mono font-bold uppercase tracking-widest text-slate-400 block mb-2">
          Document Discrepancy Findings
        </span>

        {contradictions.map((c, idx) => {
          const isResolved = c.status === "RESOLVED";
          return (
            <div key={c.id || idx} className="p-4 rounded-xl border border-slate-800 bg-slate-900/80 space-y-3">
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-bold text-rose-400 bg-rose-950/80 px-2 py-0.5 rounded border border-rose-800 flex items-center gap-1">
                  <AlertTriangle className="w-3 h-3" />
                  [{c.contradiction_type}] DISCREPANCY #{idx + 1}
                </span>
                <span className={`text-xs font-mono font-bold px-2 py-0.5 rounded ${
                  isResolved ? "bg-emerald-950 text-emerald-400 border border-emerald-800" : "bg-rose-950 text-rose-400 border border-rose-800"
                }`}>
                  {c.status}
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                <div className="p-3 bg-slate-950 rounded border border-slate-800">
                  <span className="text-[10px] font-mono text-slate-400 block mb-1">Source A ({c.source_a_name || "Document A"})</span>
                  <p className="text-slate-200 font-medium">{c.statement_a}</p>
                </div>
                <div className="p-3 bg-slate-950 rounded border border-slate-800">
                  <span className="text-[10px] font-mono text-slate-400 block mb-1">Source B ({c.source_b_name || "Document B"})</span>
                  <p className="text-slate-200 font-medium">{c.statement_b}</p>
                </div>
              </div>

              {c.resolution_summary && (
                <div className="p-3 bg-emerald-950/40 border border-emerald-800/80 rounded-lg text-xs flex items-start gap-2 text-emerald-200">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                  <div>
                    <span className="font-bold font-mono text-[10px] block text-emerald-400 uppercase">Resolution Finding</span>
                    <p>{c.resolution_summary}</p>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      <div className="pt-4 border-t border-slate-800">
        <h4 className="text-sm font-bold text-slate-200 mb-3 flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-sky-400" />
          Autonomous Hypothesis Testing Loop
        </h4>
        <div className="space-y-2">
          {hypotheses.map((h, idx) => (
            <div key={h.id || idx} className="p-3 rounded-lg bg-slate-900 border border-slate-800 flex items-start justify-between text-xs">
              <div>
                <span className="font-mono text-[10px] font-bold text-sky-400 block mb-0.5">{h.status}</span>
                <p className="text-slate-200 font-medium">{h.statement}</p>
                {h.findings && <p className="text-slate-400 text-[11px] mt-1">Findings: {h.findings}</p>}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
