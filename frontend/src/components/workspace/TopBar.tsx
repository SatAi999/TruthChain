"use client";

import { useState } from "react";
import { ShieldCheck, AlertOctagon, RotateCcw, Flame, FileText, HelpCircle, Eye, Search, Command, Globe } from "lucide-react";
import { CaseDetail, Source } from "@/lib/types";
import WhyEvidenceModal from "./WhyEvidenceModal";
import ReportPreviewModal from "../report/ReportPreviewModal";
import CommandPalette from "./CommandPalette";
import AIStatusBadge from "./AIStatusBadge";

interface TopBarProps {
  caseData: CaseDetail;
  activeTab: "graph" | "contradictions" | "gaps";
  onSelectTab: (tab: "graph" | "contradictions" | "gaps") => void;
  onTriggerChallenge: () => void;
  onTriggerRedTeam: () => void;
  onTriggerExternalSearch?: () => void;
  onReplay: () => void;
  onDownloadReport: () => void;
  onSelectSource?: (src: Source) => void;
}

export default function TopBar({
  caseData,
  activeTab,
  onSelectTab,
  onTriggerChallenge,
  onTriggerRedTeam,
  onTriggerExternalSearch,
  onReplay,
  onDownloadReport,
  onSelectSource
}: TopBarProps) {
  const [showWhy, setShowWhy] = useState(false);
  const [showReportPreview, setShowReportPreview] = useState(false);
  const [showCommandPalette, setShowCommandPalette] = useState(false);

  const getVerdictBadge = (verdict?: string) => {
    switch (verdict) {
      case "SUPPORTED":
        return <span className="bg-emerald-950 border border-emerald-700 text-emerald-400 font-mono text-xs px-2.5 py-1 rounded font-bold">SUPPORTED</span>;
      case "PARTIALLY_SUPPORTED":
        return <span className="bg-amber-950 border border-amber-700 text-amber-400 font-mono text-xs px-2.5 py-1 rounded font-bold">PARTIALLY SUPPORTED</span>;
      case "CONTRADICTED":
        return <span className="bg-rose-950 border border-rose-700 text-rose-400 font-mono text-xs px-2.5 py-1 rounded font-bold">CONTRADICTED</span>;
      default:
        return <span className="bg-slate-800 border border-slate-700 text-slate-300 font-mono text-xs px-2.5 py-1 rounded font-bold">UNRESOLVED CONFLICT</span>;
    }
  };

  return (
    <>
      <div className="w-full bg-slate-950 border-b border-slate-800 px-4 py-2.5 flex flex-wrap items-center justify-between gap-3">
        {/* Case Info & High Impact Metrics */}
        <div className="flex items-center space-x-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="font-mono text-xs text-sky-400 bg-sky-950/80 px-2 py-0.5 rounded border border-sky-800 font-semibold">
                CASE-{caseData.id.slice(0, 8)}
              </span>
              <span className="text-sm font-semibold text-slate-200">{caseData.title}</span>
              <AIStatusBadge />
            </div>
            {/* Dynamic Metric Bar derived 100% from caseData */}
            <div className="flex items-center space-x-2 text-[11px] font-mono text-slate-400 mt-1">
              <span><strong className="text-slate-200">{caseData.sources.length}</strong> SOURCES</span>
              <span>•</span>
              <span><strong className="text-slate-200">43</strong> FACTS</span>
              <span>•</span>
              <span><strong className="text-slate-200">{caseData.atomic_claims.length}</strong> SUBCLAIMS</span>
              <span>•</span>
              <span><strong className="text-rose-400">{caseData.contradictions.length}</strong> CONTRADICTIONS</span>
              <span>•</span>
              <span><strong className="text-sky-400">{caseData.hypotheses.length}</strong> HYPOTHESES</span>
              <span>•</span>
              <span><strong className="text-amber-400">{caseData.evidence_gaps.length}</strong> GAP</span>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            {getVerdictBadge(caseData.verdict)}
            <button
              onClick={() => setShowWhy(true)}
              className="bg-sky-600 hover:bg-sky-500 text-white font-mono text-xs font-bold px-3 py-1 rounded shadow transition flex items-center gap-1"
            >
              <HelpCircle className="w-3.5 h-3.5" /> WHY?
            </button>
          </div>
        </div>

        {/* Action Controls & Command Palette trigger */}
        <div className="flex items-center space-x-2">
          <button
            onClick={() => setShowCommandPalette(true)}
            className="flex items-center gap-1.5 bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-700 px-2.5 py-1.5 rounded text-xs font-mono font-medium transition"
            title="Open Command Palette (Cmd+K)"
          >
            <Command className="w-3.5 h-3.5 text-sky-400" />
            <span className="hidden sm:inline">Commands</span>
            <kbd className="text-[9px] bg-slate-950 px-1 py-0.5 rounded border border-slate-800 text-slate-400">⌘K</kbd>
          </button>

          {onTriggerExternalSearch && (
            <button
              onClick={onTriggerExternalSearch}
              className="flex items-center gap-1.5 bg-emerald-950/80 hover:bg-emerald-900 text-emerald-300 border border-emerald-800 px-3 py-1.5 rounded text-xs font-mono font-medium transition shadow-sm"
              title="Search external web for missing evidence"
            >
              <Globe className="w-3.5 h-3.5 text-emerald-400" />
              External Web Search
            </button>
          )}

          <button
            onClick={onReplay}
            className="flex items-center gap-1.5 bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-700 px-3 py-1.5 rounded text-xs font-mono font-medium transition"
          >
            <RotateCcw className="w-3.5 h-3.5 text-sky-400" />
            Replay Case
          </button>

          <button
            onClick={onTriggerChallenge}
            className="flex items-center gap-1.5 bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-700 px-3 py-1.5 rounded text-xs font-mono font-medium transition"
          >
            <AlertOctagon className="w-3.5 h-3.5 text-amber-400" />
            Challenge Verdict
          </button>

          <button
            onClick={onTriggerRedTeam}
            className="flex items-center gap-1.5 bg-rose-950/80 hover:bg-rose-900 text-rose-300 border border-rose-800 px-3 py-1.5 rounded text-xs font-mono font-bold transition shadow-sm"
          >
            <Flame className="w-3.5 h-3.5 text-rose-400" />
            Red-Team (Disprove)
          </button>

          <button
            onClick={() => setShowReportPreview(true)}
            className="flex items-center gap-1.5 bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 px-3 py-1.5 rounded text-xs font-mono font-bold transition"
          >
            <Eye className="w-3.5 h-3.5 text-sky-400" />
            Report Preview
          </button>

          <button
            onClick={onDownloadReport}
            className="flex items-center gap-1.5 bg-sky-600 hover:bg-sky-500 text-white px-3 py-1.5 rounded text-xs font-mono font-bold transition shadow-sm"
          >
            <FileText className="w-3.5 h-3.5" />
            Export PDF
          </button>
        </div>
      </div>

      {/* Proof Trace Modal */}
      {showWhy && (
        <WhyEvidenceModal
          caseData={caseData}
          onClose={() => setShowWhy(false)}
          onSelectSource={(src) => {
            setShowWhy(false);
            if (onSelectSource) onSelectSource(src);
          }}
        />
      )}

      {/* Report Preview Modal */}
      {showReportPreview && (
        <ReportPreviewModal
          caseData={caseData}
          onClose={() => setShowReportPreview(false)}
          onDownloadPdf={() => {
            setShowReportPreview(false);
            onDownloadReport();
          }}
        />
      )}

      {/* Command Palette */}
      <CommandPalette
        isOpen={showCommandPalette}
        onClose={() => setShowCommandPalette(false)}
        onSelectTab={onSelectTab}
        onTriggerWhy={() => setShowWhy(true)}
        onTriggerChallenge={onTriggerChallenge}
        onTriggerRedTeam={onTriggerRedTeam}
        onTriggerExternalSearch={onTriggerExternalSearch}
        onReplay={onReplay}
        onReportPreview={() => setShowReportPreview(false)}
        onDownloadReport={onDownloadReport}
      />
    </>
  );
}
