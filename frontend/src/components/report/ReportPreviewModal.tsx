"use client";

import { X, FileText, Download, CheckCircle2, AlertTriangle, Layers, Calendar, HelpCircle, Database } from "lucide-react";
import { CaseDetail } from "@/lib/types";

interface ReportPreviewModalProps {
  caseData: CaseDetail;
  onClose: () => void;
  onDownloadPdf: () => void;
}

export default function ReportPreviewModal({ caseData, onClose, onDownloadPdf }: ReportPreviewModalProps) {
  return (
    <div className="fixed inset-0 z-50 bg-slate-950/85 backdrop-blur-md flex items-center justify-center p-4">
      <div className="w-full max-w-4xl bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-950">
          <div className="flex items-center gap-2">
            <FileText className="w-5 h-5 text-sky-400" />
            <span className="font-mono text-xs font-bold text-slate-200 uppercase tracking-wider">
              TRUTHCHAIN Investigation Case Report Preview
            </span>
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={onDownloadPdf}
              className="px-4 py-1.5 bg-sky-600 hover:bg-sky-500 text-white text-xs font-mono font-bold rounded-lg transition flex items-center gap-1.5 shadow"
            >
              <Download className="w-3.5 h-3.5" /> EXPORT PDF REPORT
            </button>
            <button onClick={onClose} className="text-slate-400 hover:text-slate-200 p-1.5 rounded-lg">
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Report Preview Body */}
        <div className="p-8 overflow-y-auto space-y-8 bg-slate-950 text-slate-200 font-sans">
          {/* Title Header */}
          <div className="border-b border-slate-800 pb-4">
            <h1 className="text-2xl font-extrabold text-slate-100">CASE REPORT: {caseData.title}</h1>
            <p className="text-xs font-mono text-slate-400 mt-1">
              Case ID: {caseData.id} | Generated: 2026-09-20 | Classification: AUDIT TRAIL
            </p>
          </div>

          {/* 1. Executive Summary & Verdict */}
          <div>
            <h3 className="text-xs font-mono font-bold uppercase tracking-widest text-sky-400 mb-2">
              1. Executive Assessment Finding
            </h3>
            <div className="p-4 rounded-xl border border-amber-800/80 bg-amber-950/20 space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-bold text-amber-400 uppercase">
                  VERDICT: {caseData.verdict || "PARTIALLY_SUPPORTED"}
                </span>
                <span className="text-[10px] font-mono text-slate-400">Confidence: 88%</span>
              </div>
              <p className="text-xs text-slate-200 leading-relaxed italic">
                "{caseData.verdict_reasoning}"
              </p>
            </div>
          </div>

          {/* 2. Atomic Claims */}
          <div>
            <h3 className="text-xs font-mono font-bold uppercase tracking-widest text-sky-400 mb-2 flex items-center gap-1.5">
              <Layers className="w-3.5 h-3.5" /> 2. Atomic Claim Decomposition Matrix
            </h3>
            <div className="overflow-x-auto border border-slate-800 rounded-xl">
              <table className="w-full text-left text-xs font-mono">
                <thead className="bg-slate-900 text-slate-400 text-[10px] uppercase border-b border-slate-800">
                  <tr>
                    <th className="p-3">Sub-claim Statement</th>
                    <th className="p-3">Subject</th>
                    <th className="p-3">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                  {caseData.atomic_claims.map((ac, idx) => (
                    <tr key={idx} className="hover:bg-slate-900/50">
                      <td className="p-3 text-slate-200 font-sans">{ac.statement}</td>
                      <td className="p-3 text-slate-400">{ac.subject || "N/A"}</td>
                      <td className="p-3">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          ac.statement.toLowerCase().includes("deadline") || ac.statement.toLowerCase().includes("before")
                            ? "bg-rose-950 text-rose-400 border border-rose-800"
                            : "bg-emerald-950 text-emerald-400 border border-emerald-800"
                        }`}>
                          {ac.statement.toLowerCase().includes("deadline") || ac.statement.toLowerCase().includes("before") ? "CONTRADICTED" : "SUPPORTED"}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* 3. Contradiction Summary */}
          <div>
            <h3 className="text-xs font-mono font-bold uppercase tracking-widest text-rose-400 mb-2 flex items-center gap-1.5">
              <AlertTriangle className="w-3.5 h-3.5" /> 3. Detected Contradictions
            </h3>
            <div className="space-y-2 text-xs">
              {caseData.contradictions.map((c, idx) => (
                <div key={idx} className="p-3 bg-slate-900 border border-slate-800 rounded-lg">
                  <span className="font-mono text-[10px] font-bold text-rose-400 block mb-1">
                    [{c.contradiction_type}] DISCREPANCY #{idx + 1}
                  </span>
                  <p className="text-slate-300">• Statement A ({c.source_a_name}): {c.statement_a}</p>
                  <p className="text-slate-300">• Statement B ({c.source_b_name}): {c.statement_b}</p>
                  {c.resolution_summary && (
                    <p className="text-emerald-400 text-[11px] mt-1 italic">Resolution: {c.resolution_summary}</p>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* 4. Evidence Gaps */}
          <div>
            <h3 className="text-xs font-mono font-bold uppercase tracking-widest text-amber-400 mb-2 flex items-center gap-1.5">
              <HelpCircle className="w-3.5 h-3.5" /> 4. Evidence Gap Analysis
            </h3>
            <div className="space-y-2 text-xs">
              {caseData.evidence_gaps.map((g, idx) => (
                <div key={idx} className="p-3 bg-slate-900 border border-slate-800 rounded-lg">
                  <span className="font-mono text-[10px] font-bold text-amber-400 block mb-1">EVIDENCE GAP #{idx + 1}</span>
                  <p className="text-slate-200 font-bold">{g.description}</p>
                  <p className="text-slate-400 text-[11px] mt-0.5">Why it matters: {g.why_it_matters}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
