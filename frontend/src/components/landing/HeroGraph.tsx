"use client";

import { motion } from "framer-motion";
import { FileText, AlertTriangle, Search, CheckCircle2, ArrowRight } from "lucide-react";

export default function HeroGraph() {
  const steps = [
    { id: "claim", title: "CLAIM", icon: FileText, color: "text-slate-300", bg: "bg-slate-900 border-slate-700", desc: "10,000 units by Sept 15" },
    { id: "evidence", title: "EVIDENCE", icon: Search, color: "text-sky-400", bg: "bg-sky-950/80 border-sky-700", desc: "17 documents ingested" },
    { id: "conflict", title: "CONFLICT", icon: AlertTriangle, color: "text-rose-400", bg: "bg-rose-950/80 border-rose-800", desc: "Quantity & Deadline gap" },
    { id: "investigation", title: "INVESTIGATION", icon: Search, color: "text-amber-400", bg: "bg-amber-950/80 border-amber-800", desc: "Hypothesis H1 resolved" },
    { id: "resolution", title: "VERDICT", icon: CheckCircle2, color: "text-emerald-400", bg: "bg-emerald-950/80 border-emerald-800", desc: "PARTIALLY SUPPORTED" },
  ];

  return (
    <div className="w-full py-8 px-4 bg-slate-950/60 border border-slate-800/80 rounded-2xl relative overflow-hidden backdrop-blur-md">
      <div className="text-center mb-6">
        <span className="text-xs uppercase tracking-widest text-slate-400 font-mono">Autonomous Evidence Intelligence Pipeline</span>
      </div>

      <div className="flex flex-col lg:flex-row items-center justify-between gap-4 relative z-10">
        {steps.map((step, idx) => {
          const Icon = step.icon;
          return (
            <div key={step.id} className="flex flex-col lg:flex-row items-center w-full lg:w-auto">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.15 }}
                className={`w-full lg:w-48 p-4 rounded-xl border ${step.bg} flex flex-col items-center text-center shadow-lg hover:border-sky-500/50 transition`}
              >
                <div className={`p-2.5 rounded-lg mb-2 bg-slate-900/90 border border-slate-800 ${step.color}`}>
                  <Icon className="w-5 h-5" />
                </div>
                <span className="font-mono text-xs font-bold text-slate-200 tracking-wider mb-1">{step.title}</span>
                <span className="text-[11px] text-slate-400 leading-tight">{step.desc}</span>
              </motion.div>

              {idx < steps.length - 1 && (
                <div className="my-2 lg:my-0 lg:mx-2 text-slate-600 flex justify-center items-center">
                  <ArrowRight className="w-5 h-5 hidden lg:block text-slate-600" />
                  <div className="w-0.5 h-6 bg-slate-800 lg:hidden"></div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
