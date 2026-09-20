"use client";

import { useEffect, useState } from "react";
import { Search, Network, AlertTriangle, HelpCircle, FileText, RotateCcw, Flame, Eye, X, Globe } from "lucide-react";

interface CommandPaletteProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectTab: (tab: "graph" | "contradictions" | "gaps") => void;
  onTriggerWhy: () => void;
  onTriggerChallenge: () => void;
  onTriggerRedTeam: () => void;
  onTriggerExternalSearch?: () => void;
  onReplay: () => void;
  onReportPreview: () => void;
  onDownloadReport: () => void;
}

export default function CommandPalette({
  isOpen,
  onClose,
  onSelectTab,
  onTriggerWhy,
  onTriggerChallenge,
  onTriggerRedTeam,
  onTriggerExternalSearch,
  onReplay,
  onReportPreview,
  onDownloadReport,
}: CommandPaletteProps) {
  const [query, setQuery] = useState("");

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        if (isOpen) onClose();
        else onClose(); // parent handles toggle
      }
      if (e.key === "Escape" && isOpen) {
        onClose();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const commands = [
    { id: "why", label: "Trace Proof Chain (Why Did We Reach This Verdict?)", icon: HelpCircle, action: () => { onTriggerWhy(); onClose(); } },
    { id: "search", label: "Execute External Web Search (Discover Web Evidence)", icon: Globe, action: () => { if (onTriggerExternalSearch) onTriggerExternalSearch(); onClose(); } },
    { id: "graph", label: "View Interactive Evidence Graph", icon: Network, action: () => { onSelectTab("graph"); onClose(); } },
    { id: "contradictions", label: "View Contradiction & Discrepancy Center", icon: AlertTriangle, action: () => { onSelectTab("contradictions"); onClose(); } },
    { id: "gaps", label: "View Evidence Gap Analysis", icon: HelpCircle, action: () => { onSelectTab("gaps"); onClose(); } },
    { id: "challenge", label: "Submit Challenge Question (Re-open Investigation)", icon: AlertTriangle, action: () => { onTriggerChallenge(); onClose(); } },
    { id: "redteam", label: "Activate Adversarial Red-Team Mode (Try To Disprove)", icon: Flame, action: () => { onTriggerRedTeam(); onClose(); } },
    { id: "replay", label: "Replay Investigation Audit Steps", icon: RotateCcw, action: () => { onReplay(); onClose(); } },
    { id: "preview", label: "Preview Case Investigation Report", icon: Eye, action: () => { onReportPreview(); onClose(); } },
    { id: "export", label: "Export Case Report (PDF Document)", icon: FileText, action: () => { onDownloadReport(); onClose(); } },
  ];

  const filteredCommands = commands.filter((c) => c.label.toLowerCase().includes(query.toLowerCase()));

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-start justify-center pt-20 p-4">
      <div className="w-full max-w-xl bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl overflow-hidden flex flex-col">
        {/* Command Search Input */}
        <div className="p-3 border-b border-slate-800 flex items-center space-x-3 bg-slate-950">
          <Search className="w-4 h-4 text-sky-400 shrink-0" />
          <input
            type="text"
            autoFocus
            placeholder="Type a command or search investigation... (Press Esc to close)"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full bg-transparent text-slate-100 placeholder-slate-500 text-xs font-mono focus:outline-none"
          />
          <button onClick={onClose} className="text-slate-400 hover:text-slate-200">
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Command List */}
        <div className="p-2 max-h-80 overflow-y-auto space-y-1 font-mono text-xs">
          {filteredCommands.length === 0 ? (
            <div className="p-4 text-center text-slate-500">No matching investigation commands.</div>
          ) : (
            filteredCommands.map((cmd) => {
              const Icon = cmd.icon;
              return (
                <button
                  key={cmd.id}
                  onClick={cmd.action}
                  className="w-full px-3 py-2.5 rounded-lg hover:bg-slate-800 text-slate-200 hover:text-sky-300 flex items-center gap-2.5 transition text-left group"
                >
                  <Icon className="w-4 h-4 text-slate-400 group-hover:text-sky-400 shrink-0" />
                  <span className="truncate">{cmd.label}</span>
                </button>
              );
            })
          )}
        </div>

        {/* Footer info */}
        <div className="px-4 py-2 bg-slate-950 border-t border-slate-800 text-[10px] font-mono text-slate-500 flex justify-between">
          <span>TRUTHCHAIN Command Palette</span>
          <span>Shortcut: Cmd/Ctrl + K</span>
        </div>
      </div>
    </div>
  );
}
