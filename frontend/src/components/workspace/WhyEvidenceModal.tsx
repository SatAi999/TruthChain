"use client";

import { X, Layers, FileText, CheckCircle2, AlertTriangle, ArrowRight, ShieldCheck, Search } from "lucide-react";
import { CaseDetail, Source } from "@/lib/types";

interface WhyEvidenceModalProps {
  caseData: CaseDetail;
  onClose: () => void;
  onSelectSource: (src: Source) => void;
}

export default function WhyEvidenceModal({ caseData, onClose, onSelectSource }: WhyEvidenceModalProps) {
  const findSource = (namePattern: string): Source | undefined => {
    return caseData.sources.find((s) => s.name.toLowerCase().includes(namePattern.toLowerCase()));
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/85 backdrop-blur-md flex items-center justify-center p-4">
      <div className="w-full max-w-4xl bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-950">
          <div className="flex items-center gap-2">
            <div className="p-1.5 rounded bg-sky-950 text-sky-400 border border-sky-800">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-bold text-slate-100 text-sm">TRUTHCHAIN Proof Trace — Why Did We Reach This Conclusion?</h3>
              <p className="text-[11px] text-slate-400 font-mono">Traceability: Verdict → Atomic Claim → Extracted Fact → Source Provenance</p>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-200 p-1.5 rounded-lg">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content Body */}
        <div className="p-6 overflow-y-auto space-y-6">
          {/* 1. Final Verdict Top Banner */}
          <div className="p-4 rounded-xl border border-amber-800/80 bg-amber-950/30 flex items-start gap-3">
            <AlertTriangle className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
            <div>
              <span className="font-mono text-xs font-bold text-amber-400 bg-amber-950 px-2 py-0.5 rounded border border-amber-800">
                FINAL ASSESSMENT: PARTIALLY SUPPORTED
              </span>
              <p className="text-xs text-slate-200 mt-1 leading-relaxed">
                {caseData.verdict_reasoning}
              </p>
            </div>
          </div>

          {/* 2. Visual Proof Chain Breakdown */}
          <div className="space-y-4">
            <span className="text-xs font-mono font-bold uppercase tracking-widest text-slate-400 block">
              Auditable Evidence Chain
            </span>

            {/* Step 1: Subclaim Quantity */}
            <div className="p-4 rounded-xl border border-slate-800 bg-slate-950 space-y-3">
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-bold text-sky-400 flex items-center gap-1.5">
                  <Layers className="w-4 h-4" /> SUBCLAIM #1: 10,000 Units Delivered
                </span>
                <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800">
                  ✓ FULLY RECONCILED (10,000 / 10,000)
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2 text-xs">
                {/* Fact A */}
                <div
                  onClick={() => {
                    const s = findSource("Hospital_Receiving_Receipt_1") || caseData.sources[0];
                    if (s) onSelectSource(s);
                  }}
                  className="p-3 bg-slate-900 border border-slate-800 hover:border-sky-500 rounded-lg cursor-pointer transition group"
                >
                  <span className="text-[10px] font-mono text-slate-400 block mb-1">FACT #1 (Partial Shipment 1)</span>
                  <p className="text-slate-200 font-semibold group-hover:text-sky-300">8,500 units received on Sept 14</p>
                  <span className="text-[10px] font-mono text-sky-400 mt-2 block underline flex items-center gap-1">
                    <FileText className="w-3 h-3" /> Inspect Hospital_Receiving_Receipt_1.txt
                  </span>
                </div>

                {/* Fact B */}
                <div
                  onClick={() => {
                    const s = findSource("Hospital_Receiving_Receipt_2") || caseData.sources[0];
                    if (s) onSelectSource(s);
                  }}
                  className="p-3 bg-slate-900 border border-slate-800 hover:border-sky-500 rounded-lg cursor-pointer transition group"
                >
                  <span className="text-[10px] font-mono text-slate-400 block mb-1">FACT #2 (Partial Shipment 2)</span>
                  <p className="text-slate-200 font-semibold group-hover:text-sky-300">1,500 units received on Sept 17</p>
                  <span className="text-[10px] font-mono text-sky-400 mt-2 block underline flex items-center gap-1">
                    <FileText className="w-3 h-3" /> Inspect Hospital_Receiving_Receipt_2.txt
                  </span>
                </div>
              </div>
            </div>

            {/* Step 2: Subclaim Deadline */}
            <div className="p-4 rounded-xl border border-rose-900/60 bg-slate-950 space-y-3">
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-bold text-rose-400 flex items-center gap-1.5">
                  <AlertTriangle className="w-4 h-4 text-rose-400" /> SUBCLAIM #2: Delivered Before September 15 Deadline
                </span>
                <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-rose-950 text-rose-400 border border-rose-800">
                  ✕ DEADLINE CONTRADICTED (Sept 17 &gt; Sept 15)
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2 text-xs">
                {/* Fact C */}
                <div
                  onClick={() => {
                    const s = findSource("PO-2026-9042") || caseData.sources[0];
                    if (s) onSelectSource(s);
                  }}
                  className="p-3 bg-slate-900 border border-slate-800 hover:border-rose-500 rounded-lg cursor-pointer transition group"
                >
                  <span className="text-[10px] font-mono text-slate-400 block mb-1">REQUIRED DEADLINE</span>
                  <p className="text-slate-200 font-semibold group-hover:text-rose-300">Must deliver before Sept 15, 2026</p>
                  <span className="text-[10px] font-mono text-sky-400 mt-2 block underline flex items-center gap-1">
                    <FileText className="w-3 h-3" /> Inspect PO-2026-9042.txt
                  </span>
                </div>

                {/* Fact D */}
                <div
                  onClick={() => {
                    const s = findSource("Hospital_Receiving_Receipt_2") || caseData.sources[0];
                    if (s) onSelectSource(s);
                  }}
                  className="p-3 bg-slate-900 border border-slate-800 hover:border-rose-500 rounded-lg cursor-pointer transition group"
                >
                  <span className="text-[10px] font-mono text-slate-400 block mb-1">ACTUAL COMPLETION DATE</span>
                  <p className="text-rose-300 font-semibold group-hover:text-rose-200">Final shipment received Sept 17 (2 days late)</p>
                  <span className="text-[10px] font-mono text-sky-400 mt-2 block underline flex items-center gap-1">
                    <FileText className="w-3 h-3" /> Inspect Hospital_Receiving_Receipt_2.txt
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-slate-800 bg-slate-950 flex items-center justify-between">
          <span className="text-[10px] font-mono text-slate-500">Every factual node is verified against raw document provenance.</span>
          <button onClick={onClose} className="px-4 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-mono rounded-lg">
            Close Proof Trace
          </button>
        </div>
      </div>
    </div>
  );
}
