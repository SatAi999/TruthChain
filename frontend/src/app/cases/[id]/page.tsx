"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Network, AlertTriangle, HelpCircle, FileText, Activity } from "lucide-react";
import TopBar from "@/components/workspace/TopBar";
import LeftClaimPanel from "@/components/workspace/LeftClaimPanel";
import RightActivityFeed from "@/components/workspace/RightActivityFeed";
import BottomTimeline from "@/components/workspace/BottomTimeline";
import EvidenceGraphCanvas from "@/components/graph/EvidenceGraphCanvas";
import ContradictionsView from "@/components/contradictions/ContradictionsView";
import EvidenceGapsView from "@/components/gaps/EvidenceGapsView";
import SourceInspectorModal from "@/components/inspector/SourceInspectorModal";
import ReplayModal from "@/components/replay/ReplayModal";

import { fetchCaseById, fetchCaseGraph, submitChallenge, triggerRedTeam, triggerExternalSearch } from "@/lib/api";
import { CaseDetail, GraphData, Source } from "@/lib/types";

export default function CaseWorkspacePage() {
  const params = useParams();
  const caseId = params.id as string;

  const [caseData, setCaseData] = useState<CaseDetail | null>(null);
  const [graphData, setGraphData] = useState<GraphData | null>(null);
  const [activeTab, setActiveTab] = useState<"graph" | "contradictions" | "gaps">("graph");
  const [selectedSource, setSelectedSource] = useState<Source | null>(null);
  const [showReplay, setShowReplay] = useState(false);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      const [cDetails, gDetails] = await Promise.all([
        fetchCaseById(caseId),
        fetchCaseGraph(caseId),
      ]);
      setCaseData(cDetails);
      setGraphData(gDetails);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [caseId]);

  const handleChallenge = async () => {
    const q = prompt("Enter challenge statement or question against current conclusion:", "Could remaining units have been delivered separately?");
    if (q) {
      const updated = await submitChallenge(caseId, q);
      setCaseData(updated);
      alert("Challenge registered. Re-investigating under challenge hypothesis.");
    }
  };

  const handleRedTeam = async () => {
    const updated = await triggerRedTeam(caseId);
    setCaseData(updated);
    alert("Adversarial Red-Team mode activated! Priority search for counter-evidence enabled.");
  };

  const handleExternalSearch = async () => {
    try {
      setLoading(true);
      await triggerExternalSearch(caseId);
      await loadData();
      alert("External Web Search complete! Discovered and ingested external web evidence into case.");
    } catch (e: any) {
      alert("External Search error: " + (e.message || e));
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadReport = () => {
    window.open(`http://localhost:8000/api/cases/${caseId}/report`, "_blank");
  };

  if (loading || !caseData) {
    return (
      <div className="flex-1 flex items-center justify-center font-mono text-xs text-slate-500 bg-slate-950">
        Loading Investigation Command Center Workspace...
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col h-[calc(100vh-64px)] overflow-hidden bg-slate-950">
      {/* Top Header Command Bar */}
      <TopBar
        caseData={caseData}
        activeTab={activeTab}
        onSelectTab={setActiveTab}
        onTriggerChallenge={handleChallenge}
        onTriggerRedTeam={handleRedTeam}
        onTriggerExternalSearch={handleExternalSearch}
        onReplay={() => setShowReplay(true)}
        onDownloadReport={handleDownloadReport}
        onSelectSource={setSelectedSource}
      />

      {/* Main Command Center Body */}
      <div className="flex-1 flex flex-col lg:flex-row overflow-hidden relative">
        {/* Left Panel: Original & Atomic Claims */}
        <LeftClaimPanel
          originalClaim={caseData.claim_statement}
          atomicClaims={caseData.atomic_claims}
        />

        {/* Center Panel Workspace Tabs */}
        <div className="flex-1 flex flex-col bg-slate-950 relative overflow-hidden">
          {/* Tab Selection Navigation */}
          <div className="flex items-center justify-between border-b border-slate-800 px-4 bg-slate-950 h-10">
            <div className="flex items-center space-x-1">
              <button
                onClick={() => setActiveTab("graph")}
                className={`flex items-center gap-1.5 px-3 py-1 rounded text-xs font-mono font-medium transition ${
                  activeTab === "graph" ? "bg-sky-950 text-sky-400 border border-sky-800" : "text-slate-400 hover:text-slate-200"
                }`}
              >
                <Network className="w-3.5 h-3.5" />
                Evidence Graph
              </button>

              <button
                onClick={() => setActiveTab("contradictions")}
                className={`flex items-center gap-1.5 px-3 py-1 rounded text-xs font-mono font-medium transition ${
                  activeTab === "contradictions" ? "bg-rose-950 text-rose-400 border border-rose-800" : "text-slate-400 hover:text-slate-200"
                }`}
              >
                <AlertTriangle className="w-3.5 h-3.5" />
                Contradiction Center ({caseData.contradictions.length})
              </button>

              <button
                onClick={() => setActiveTab("gaps")}
                className={`flex items-center gap-1.5 px-3 py-1 rounded text-xs font-mono font-medium transition ${
                  activeTab === "gaps" ? "bg-amber-950 text-amber-400 border border-amber-800" : "text-slate-400 hover:text-slate-200"
                }`}
              >
                <HelpCircle className="w-3.5 h-3.5" />
                Evidence Gap Analysis ({caseData.evidence_gaps.length})
              </button>
            </div>

            <span className="text-[10px] font-mono text-slate-500 uppercase hidden sm:block">
              MODE: {caseData.mode}
            </span>
          </div>

          {/* Active Tab Workspace View */}
          <div className="flex-1 relative overflow-y-auto">
            {activeTab === "graph" && graphData && (
              <EvidenceGraphCanvas
                nodes={graphData.nodes}
                edges={graphData.edges}
                onNodeClick={(node) => {
                  if (node.data && node.data.node_type === "SOURCE") {
                    const src = caseData.sources.find((s) => s.name === node.data.label);
                    if (src) setSelectedSource(src);
                  }
                }}
              />
            )}

            {activeTab === "contradictions" && (
              <ContradictionsView
                contradictions={caseData.contradictions}
                hypotheses={caseData.hypotheses}
              />
            )}

            {activeTab === "gaps" && (
              <EvidenceGapsView gaps={caseData.evidence_gaps} />
            )}
          </div>
        </div>

        {/* Right Panel: Activity Feed & Audit Metrics */}
        <RightActivityFeed steps={caseData.steps} />
      </div>

      {/* Bottom Panel: Interactive Chronological Timeline */}
      <BottomTimeline events={caseData.events} />

      {/* Modals */}
      {selectedSource && (
        <SourceInspectorModal
          source={selectedSource}
          onClose={() => setSelectedSource(null)}
        />
      )}

      {showReplay && (
        <ReplayModal
          steps={caseData.steps}
          onClose={() => setShowReplay(false)}
        />
      )}
    </div>
  );
}
