"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Database, Plus, ArrowRight, ShieldAlert, FileText } from "lucide-react";
import { fetchCases, loadOneClickDemo } from "@/lib/api";
import { CaseDetail } from "@/lib/types";

export default function CasesPage() {
  const router = useRouter();
  const [cases, setCases] = useState<CaseDetail[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCases()
      .then(setCases)
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  const handleRunDemo = async () => {
    setLoading(true);
    try {
      const demoCase = await loadOneClickDemo();
      router.push(`/cases/${demoCase.id}`);
    } catch (e) {
      console.error(e);
      alert("Error loading demo case.");
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto py-10 px-4 space-y-8 w-full">
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-sky-950 border border-sky-800 text-sky-400 font-mono text-xs mb-2">
            <Database className="w-3.5 h-3.5" />
            INVESTIGATION CASE REGISTER
          </div>
          <h1 className="text-3xl font-extrabold text-slate-100">All Case Investigations</h1>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={handleRunDemo}
            className="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 rounded-xl font-mono text-xs font-bold transition flex items-center gap-1.5"
          >
            Load Procurement Demo
          </button>
          <button
            onClick={() => router.push("/investigate")}
            className="px-4 py-2 bg-sky-600 hover:bg-sky-500 text-white rounded-xl font-bold text-xs transition flex items-center gap-1.5 shadow"
          >
            <Plus className="w-4 h-4" /> New Case
          </button>
        </div>
      </div>

      {loading ? (
        <div className="text-center py-20 font-mono text-xs text-slate-500">Loading cases...</div>
      ) : cases.length === 0 ? (
        <div className="text-center py-16 bg-slate-900/60 border border-slate-800 rounded-2xl space-y-4">
          <p className="text-sm text-slate-400">No active investigations in database.</p>
          <button
            onClick={handleRunDemo}
            className="px-5 py-2.5 bg-sky-600 hover:bg-sky-500 text-white rounded-xl font-bold text-xs shadow inline-flex items-center gap-2"
          >
            Run Procurement Demo Case
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {cases.map((c) => (
            <div
              key={c.id}
              onClick={() => router.push(`/cases/${c.id}`)}
              className="p-5 rounded-2xl border border-slate-800 bg-slate-900/80 hover:border-sky-600 cursor-pointer transition flex flex-col justify-between space-y-4 group"
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="font-mono text-[10px] px-2 py-0.5 rounded bg-sky-950 text-sky-400 border border-sky-800">
                    CASE-{c.id.slice(0, 8)}
                  </span>
                  <span className="text-[10px] font-mono text-slate-400 font-bold">{c.verdict || c.status}</span>
                </div>

                <h3 className="font-bold text-slate-100 text-sm group-hover:text-sky-300 transition line-clamp-1">{c.title}</h3>
                <p className="text-xs text-slate-400 mt-1 line-clamp-2 italic">"{c.claim_statement}"</p>
              </div>

              <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between text-[11px] font-mono text-slate-500">
                <span>Sources: {c.sources.length} | Contradictions: {c.contradictions.length}</span>
                <span className="text-sky-400 group-hover:translate-x-1 transition flex items-center gap-1">
                  Inspect <ArrowRight className="w-3 h-3" />
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
