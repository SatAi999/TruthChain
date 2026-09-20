"use client";

import { Cpu, Calculator, Search, ShieldCheck, Database, CheckCircle2 } from "lucide-react";

export default function AITransparencyPage() {
  return (
    <div className="max-w-5xl mx-auto py-12 px-4 space-y-10 text-slate-100">
      <div>
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-sky-950 border border-sky-800 text-sky-400 font-mono text-xs mb-3">
          <Cpu className="w-3.5 h-3.5" />
          SYSTEM ARCHITECTURE & AI TRANSPARENCY
        </div>
        <h1 className="text-3xl font-extrabold text-slate-100">How TRUTHCHAIN Uses Artificial Intelligence</h1>
        <p className="text-sm text-slate-400 mt-1">
          TRUTHCHAIN cleanly separates AI semantic reasoning from deterministic code verification to prevent hallucinations.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Category A: AI-Powered Features */}
        <div className="p-6 rounded-2xl border border-sky-900/80 bg-sky-950/30 space-y-4">
          <div className="flex items-center gap-2 text-sky-400 font-mono text-xs font-bold uppercase">
            <Cpu className="w-4 h-4" /> 1. Real AI-Powered Features
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">
            AI language models are used for semantic interpretation, hypothesis generation, and structured claim decomposition:
          </p>
          <ul className="text-xs text-slate-300 space-y-2 font-mono">
            <li className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-sky-400 shrink-0 mt-0.5" />
              <span><strong>Atomic Claim Decomposition:</strong> Deconstructs statements into subject-predicate-object constraints.</span>
            </li>
            <li className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-sky-400 shrink-0 mt-0.5" />
              <span><strong>Hypothesis Formulation:</strong> Formulates plausible explanations when evidence conflicts arise.</span>
            </li>
            <li className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-sky-400 shrink-0 mt-0.5" />
              <span><strong>Adversarial Red-Team Reasoning:</strong> Actively searches for contract defaults and timeline breaches.</span>
            </li>
            <li className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-sky-400 shrink-0 mt-0.5" />
              <span><strong>Natural Language Challenge Interpretation:</strong> Evaluates user counter-questions against evidence.</span>
            </li>
          </ul>
        </div>

        {/* Category B: Deterministic Python Engine */}
        <div className="p-6 rounded-2xl border border-emerald-900/80 bg-emerald-950/30 space-y-4">
          <div className="flex items-center gap-2 text-emerald-400 font-mono text-xs font-bold uppercase">
            <Calculator className="w-4 h-4" /> 2. Real Deterministic Python Engine
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">
            LLMs are NEVER trusted for arithmetic or date comparisons. The following are computed in Python:
          </p>
          <ul className="text-xs text-slate-300 space-y-2 font-mono">
            <li className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
              <span><strong>Arithmetic & Quantity Reconciliation:</strong> Sums partial shipments ($8,500 + 1,500 = 10,000$).</span>
            </li>
            <li className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
              <span><strong>Temporal & Deadline Verification:</strong> Compares ISO dates (Sept 17 &gt; Sept 15: Deadline breach).</span>
            </li>
            <li className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
              <span><strong>Chronological Timeline Sorting:</strong> Orders historical events deterministically.</span>
            </li>
            <li className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
              <span><strong>Source Provenance Integrity:</strong> Guarantees fact citations match raw document page numbers.</span>
            </li>
          </ul>
        </div>
      </div>

      {/* Important Limitations Disclaimer */}
      <div className="p-6 rounded-2xl border border-slate-800 bg-slate-900/80 space-y-3">
        <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-amber-400" />
          Important Operational Limitation Statement
        </h3>
        <p className="text-xs text-slate-300 leading-relaxed">
          TRUTHCHAIN does not claim to know "objective reality" or "universal truth." Its sole function is to evaluate what available evidence documents can support, detect contradictions, identify missing evidence gaps, and present an auditable proof trail.
        </p>
      </div>
    </div>
  );
}
