"use client";

import { X, FileText, CheckCircle2, AlertTriangle, Search, GitBranch } from "lucide-react";
import { Source } from "@/lib/types";

interface SourceInspectorModalProps {
  source: Source | null;
  onClose: () => void;
}

export default function SourceInspectorModal({ source, onClose }: SourceInspectorModalProps) {
  if (!source) return null;

  const isDerived = source.source_type in ["DERIVED", "COPIED"] || source.name.includes("Derived");

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/85 backdrop-blur-md flex items-center justify-center p-4">
      <div className="w-full max-w-2xl bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[85vh]">
        <div className="px-5 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-950">
          <div className="flex items-center gap-2">
            <FileText className="w-5 h-5 text-sky-400" />
            <span className="font-mono text-xs font-bold text-slate-200">Source Provenance Inspector — {source.name}</span>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-200 p-1 rounded-lg">
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="p-6 overflow-y-auto space-y-4 text-xs font-mono">
          <div className="grid grid-cols-3 gap-3">
            <div className="p-3 bg-slate-950 border border-slate-800 rounded-xl">
              <span className="text-[10px] text-slate-500 block font-bold uppercase">FILE FORMAT</span>
              <span className="text-sky-400 font-bold text-sm">{source.file_type}</span>
            </div>
            <div className="p-3 bg-slate-950 border border-slate-800 rounded-xl">
              <span className="text-[10px] text-slate-500 block font-bold uppercase">SOURCE LINEAGE</span>
              <span className={`font-bold text-sm ${isDerived ? "text-amber-400" : "text-emerald-400"}`}>
                {isDerived ? "DERIVED / COPIED" : "INDEPENDENT PRIMARY"}
              </span>
            </div>
            <div className="p-3 bg-slate-950 border border-slate-800 rounded-xl">
              <span className="text-[10px] text-slate-500 block font-bold uppercase">PROVENANCE CONFIDENCE</span>
              <span className="text-emerald-400 font-bold text-sm">100% AUDITED</span>
            </div>
          </div>

          {/* Visual Lineage Tree */}
          <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-2">
            <span className="text-[10px] text-slate-400 font-bold uppercase flex items-center gap-1">
              <GitBranch className="w-3.5 h-3.5 text-sky-400" /> Source Lineage & Independence Tree
            </span>

            {isDerived ? (
              <div className="p-3 bg-amber-950/30 border border-amber-800/80 rounded-lg text-amber-200 font-sans space-y-1 text-xs">
                <p className="font-bold">⚠️ Derived Content Warning:</p>
                <p>
                  This source (<i>{source.name}</i>) copies/re-publishes content from the primary Supplier Email record. TRUTHCHAIN's lineage engine filters this source to prevent false multi-counting.
                </p>
              </div>
            ) : (
              <div className="p-3 bg-emerald-950/30 border border-emerald-800/80 rounded-lg text-emerald-200 font-sans space-y-1 text-xs">
                <p className="font-bold">✓ Primary Evidence Source:</p>
                <p>Direct operational record verified as an independent evidence point.</p>
              </div>
            )}
          </div>

          <div>
            <span className="text-[10px] text-slate-400 block mb-1 uppercase font-bold">Extracted Provenance Fact Excerpts</span>
            <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl text-slate-300 font-sans space-y-2.5">
              <p className="border-l-2 border-sky-500 pl-3 py-0.5 text-xs">
                "Quantity delivered: 8,500 units of Medical Device #MD-10K under PO-2026-9042 on September 14."
              </p>
              <p className="border-l-2 border-emerald-500 pl-3 py-0.5 text-xs">
                "Second shipment of 1,500 units received on September 17 at Dock B."
              </p>
            </div>
          </div>

          <div className="pt-2 border-t border-slate-800 flex justify-end">
            <button onClick={onClose} className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg font-sans text-xs">
              Close Inspector
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
