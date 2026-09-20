"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Cpu, FileText, ArrowRight, ShieldCheck } from "lucide-react";
import { createCase } from "@/lib/api";

export default function InvestigatePage() {
  const router = useRouter();
  const [title, setTitle] = useState("");
  const [claimStatement, setClaimStatement] = useState("");
  const [mode, setMode] = useState("STANDARD");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title || !claimStatement) return;
    setLoading(true);
    try {
      const newCase = await createCase(title, claimStatement, mode);
      router.push(`/cases/${newCase.id}`);
    } catch (err) {
      console.error(err);
      alert("Failed to initialize investigation case");
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto py-12 px-4 space-y-8">
      <div>
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-sky-950 border border-sky-800 text-sky-400 font-mono text-xs mb-3">
          <Cpu className="w-3.5 h-3.5" />
          NEW INVESTIGATION WORKSPACE
        </div>
        <h1 className="text-3xl font-extrabold text-slate-100">Initialize Evidence Investigation</h1>
        <p className="text-xs text-slate-400 mt-1">
          Enter a user claim statement to decompose into atomic verifiable propositions.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6 bg-slate-900/80 border border-slate-800 p-6 rounded-2xl shadow-xl">
        <div>
          <label className="block text-xs font-mono font-bold uppercase tracking-wider text-slate-300 mb-2">
            Case Title / Identifier
          </label>
          <input
            type="text"
            required
            placeholder="e.g., Procurement Audit — Medical Device Order #PO-9042"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-sky-500"
          />
        </div>

        <div>
          <label className="block text-xs font-mono font-bold uppercase tracking-wider text-slate-300 mb-2">
            Primary Claim Statement to Investigate
          </label>
          <textarea
            required
            rows={4}
            placeholder="e.g., Company A delivered 10,000 medical devices to Hospital X before September 15."
            value={claimStatement}
            onChange={(e) => setClaimStatement(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-sky-500"
          />
        </div>

        <div>
          <label className="block text-xs font-mono font-bold uppercase tracking-wider text-slate-300 mb-2">
            Investigation Strategy Mode
          </label>
          <div className="grid grid-cols-2 gap-3">
            <button
              type="button"
              onClick={() => setMode("STANDARD")}
              className={`p-3 rounded-xl border text-left text-xs transition ${
                mode === "STANDARD"
                  ? "bg-sky-950 border-sky-600 text-sky-200"
                  : "bg-slate-950 border-slate-800 text-slate-400"
              }`}
            >
              <span className="font-bold font-mono block mb-1">STANDARD INVESTIGATION</span>
              Balanced evidence collection & contradiction resolution.
            </button>

            <button
              type="button"
              onClick={() => setMode("RED_TEAM")}
              className={`p-3 rounded-xl border text-left text-xs transition ${
                mode === "RED_TEAM"
                  ? "bg-rose-950 border-rose-600 text-rose-200"
                  : "bg-slate-950 border-slate-800 text-slate-400"
              }`}
            >
              <span className="font-bold font-mono block mb-1">RED-TEAM (FALSIFY)</span>
              Adversarial mode actively searching for counter-evidence.
            </button>
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full py-3 bg-sky-600 hover:bg-sky-500 text-white rounded-xl font-bold text-sm shadow-lg transition flex items-center justify-center gap-2 disabled:opacity-50"
        >
          {loading ? "Decomposing Claim..." : "Launch Investigation Workspace"} <ArrowRight className="w-4 h-4" />
        </button>
      </form>
    </div>
  );
}
