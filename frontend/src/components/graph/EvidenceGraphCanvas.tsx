"use client";

import React, { useMemo } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  Handle,
  Position,
  NodeProps,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { FileText, AlertTriangle, Search, HelpCircle, Layers, CheckCircle2 } from "lucide-react";

// --- Custom Node Types ---
const ClaimNode = ({ data }: NodeProps) => (
  <div className="px-4 py-3 rounded-xl border-2 border-sky-500 bg-slate-900 shadow-xl shadow-sky-500/10 min-w-[240px]">
    <Handle type="source" position={Position.Bottom} className="w-3 h-3 bg-sky-500" />
    <div className="flex items-center gap-2 mb-1">
      <Layers className="w-4 h-4 text-sky-400" />
      <span className="font-mono text-[10px] font-bold tracking-wider text-sky-400">CLAIM</span>
    </div>
    <p className="text-xs font-medium text-slate-100">{data.title as string}</p>
  </div>
);

const AtomicClaimNode = ({ data }: NodeProps) => (
  <div className="px-3 py-2.5 rounded-lg border border-slate-700 bg-slate-900/90 min-w-[200px]">
    <Handle type="target" position={Position.Top} className="w-2.5 h-2.5 bg-slate-500" />
    <Handle type="source" position={Position.Bottom} className="w-2.5 h-2.5 bg-slate-500" />
    <div className="flex items-center justify-between gap-1 mb-1">
      <span className="font-mono text-[9px] text-slate-400 font-bold">{data.label as string}</span>
      <span className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-sky-950 text-sky-400 border border-sky-800">
        SUBCLAIM
      </span>
    </div>
    <p className="text-xs text-slate-200 line-clamp-2">{data.statement as string}</p>
  </div>
);

const SourceNode = ({ data }: NodeProps) => (
  <div className="px-3 py-2 rounded-lg border border-slate-800 bg-slate-950 min-w-[170px]">
    <Handle type="target" position={Position.Top} className="w-2.5 h-2.5 bg-sky-600" />
    <Handle type="source" position={Position.Bottom} className="w-2.5 h-2.5 bg-sky-600" />
    <div className="flex items-center gap-1.5">
      <FileText className="w-3.5 h-3.5 text-sky-400" />
      <div>
        <span className="font-mono text-xs font-bold text-slate-200 block truncate">{data.label as string}</span>
        <span className="text-[9px] font-mono text-slate-500 block">{data.file_type as string} ({data.source_type as string})</span>
      </div>
    </div>
  </div>
);

const FactNode = ({ data }: NodeProps) => (
  <div className="px-3 py-2 rounded-lg border border-emerald-900/80 bg-emerald-950/40 min-w-[180px]">
    <Handle type="target" position={Position.Top} className="w-2.5 h-2.5 bg-emerald-500" />
    <Handle type="source" position={Position.Bottom} className="w-2.5 h-2.5 bg-emerald-500" />
    <span className="font-mono text-[9px] text-emerald-400 block mb-0.5 font-bold">{data.label as string}</span>
    <p className="text-xs text-emerald-200 line-clamp-2">{data.value as string}</p>
  </div>
);

const ContradictionNode = ({ data }: NodeProps) => (
  <div className="px-3 py-2.5 rounded-xl border-2 border-rose-600 bg-rose-950/60 shadow-lg shadow-rose-950/40 min-w-[220px]">
    <Handle type="target" position={Position.Top} className="w-3 h-3 bg-rose-500" />
    <Handle type="source" position={Position.Bottom} className="w-3 h-3 bg-rose-500" />
    <div className="flex items-center gap-1.5 mb-1">
      <AlertTriangle className="w-4 h-4 text-rose-400" />
      <span className="font-mono text-[10px] font-bold text-rose-300 tracking-wider">CONTRADICTION</span>
    </div>
    <p className="text-xs font-semibold text-rose-100">{data.statement_a as string}</p>
    <p className="text-[11px] text-rose-300 mt-1">vs {data.statement_b as string}</p>
  </div>
);

const GapNode = ({ data }: NodeProps) => (
  <div className="px-3 py-2 rounded-lg border border-amber-800 bg-amber-950/50 min-w-[200px]">
    <Handle type="target" position={Position.Top} className="w-2.5 h-2.5 bg-amber-500" />
    <div className="flex items-center gap-1.5 mb-1">
      <HelpCircle className="w-3.5 h-3.5 text-amber-400" />
      <span className="font-mono text-[9px] font-bold text-amber-300">EVIDENCE GAP</span>
    </div>
    <p className="text-xs text-amber-200 line-clamp-2">{data.description as string}</p>
  </div>
);

interface EvidenceGraphCanvasProps {
  nodes: any[];
  edges: any[];
  onNodeClick?: (node: any) => void;
}

export default function EvidenceGraphCanvas({ nodes, edges, onNodeClick }: EvidenceGraphCanvasProps) {
  const nodeTypes = useMemo(
    () => ({
      claimNode: ClaimNode,
      atomicClaimNode: AtomicClaimNode,
      sourceNode: SourceNode,
      factNode: FactNode,
      contradictionNode: ContradictionNode,
      gapNode: GapNode,
    }),
    []
  );

  return (
    <div className="w-full h-full bg-slate-950 relative">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        onNodeClick={(_, node) => onNodeClick && onNodeClick(node)}
        fitView
        colorMode="dark"
      >
        <Background color="#1e293b" gap={16} size={1} />
        <Controls className="bg-slate-900 border border-slate-800 fill-slate-300" />
        <MiniMap
          nodeColor={(node) => {
            if (node.type === "contradictionNode") return "#ef4444";
            if (node.type === "claimNode") return "#0284c7";
            if (node.type === "gapNode") return "#f59e0b";
            return "#334155";
          }}
          maskColor="rgba(15, 23, 42, 0.8)"
          className="bg-slate-900 border border-slate-800 rounded-lg"
        />
      </ReactFlow>
    </div>
  );
}
