"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { ShieldCheck, Play, ArrowRight, Layers, Cpu, Search, Lock, AlertTriangle, FileCode, HelpCircle } from "lucide-react";
import HeroGraph from "@/components/landing/HeroGraph";
import { loadOneClickDemo } from "@/lib/api";

export default function LandingPage() {
  const router = useRouter();
  const [loadingDemo, setLoadingDemo] = useState(false);

  const handleRunDemo = async () => {
    setLoadingDemo(true);
    try {
      const demoCase = await loadOneClickDemo();
      router.push(`/cases/${demoCase.id}`);
    } catch (e) {
      console.error(e);
      alert("Error loading demo investigation. Make sure backend is running.");
      setLoadingDemo(false);
    }
  };

  const scrollToExplanation = () => {
    const el = document.getElementById("pipeline-explanation");
    if (el) el.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <div className="w-full flex-1 flex flex-col justify-between py-12 px-4 max-w-7xl mx-auto space-y-16">
      {/* Hero Header Section */}
      <div className="text-center max-w-4xl mx-auto space-y-6 pt-6">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-sky-950/80 border border-sky-800 text-sky-400 font-mono text-xs font-semibold">
          <Cpu className="w-3.5 h-3.5" />
          AGENTIC EVIDENCE INVESTIGATION SYSTEM
        </div>

        <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight text-slate-100 leading-tight">
          TRUTHCHAIN
        </h1>

        <p className="text-xl md:text-2xl font-medium text-sky-400 italic">
          "Don't just answer a claim. Investigate it."
        </p>

        <p className="text-sm md:text-base text-slate-300 max-w-2xl mx-auto leading-relaxed">
          Turn a claim into an investigation. Connect evidence, expose contradictions, reconstruct what happened, and see exactly what the evidence can support.
        </p>

        {/* CTAs */}
        <div className="flex flex-wrap items-center justify-center gap-4 pt-4">
          <button
            onClick={handleRunDemo}
            disabled={loadingDemo}
            className="px-8 py-3.5 bg-sky-600 hover:bg-sky-500 text-white rounded-xl font-mono font-bold text-sm shadow-xl shadow-sky-600/30 transition flex items-center gap-2 disabled:opacity-50"
          >
            {loadingDemo ? (
              <>Loading Procurement Case...</>
            ) : (
              <>
                <Play className="w-4 h-4 text-white fill-white" />
                RUN LIVE INVESTIGATION
              </>
            )}
          </button>

          <button
            onClick={scrollToExplanation}
            className="px-6 py-3.5 bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 rounded-xl font-mono font-semibold text-sm transition flex items-center gap-2"
          >
            <HelpCircle className="w-4 h-4 text-slate-400" />
            EXPLORE HOW IT WORKS
          </button>
        </div>
      </div>

      {/* Visual Animated Evidence Graph Hero Component */}
      <HeroGraph />

      {/* Analytical Pipeline Explanation Section */}
      <div id="pipeline-explanation" className="pt-8 border-t border-slate-800/80 space-y-6">
        <div className="text-center max-w-2xl mx-auto">
          <h2 className="text-2xl font-bold text-slate-100">Why TRUTHCHAIN Is Not A Chatbot</h2>
          <p className="text-xs text-slate-400 mt-1">
            Standard AI chatbots retrieve text snippets and hallucinate answers. TRUTHCHAIN runs an auditable evidence pipeline.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 hover:border-slate-700 transition">
            <div className="p-2.5 rounded-lg bg-sky-950/80 border border-sky-800 w-fit text-sky-400 mb-4">
              <Layers className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-base text-slate-100 mb-2">1. Atomic Claim Decomposition</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Deconstructs user statements into subject-predicate-object propositions with explicit date, location, and quantity constraints.
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 hover:border-slate-700 transition">
            <div className="p-2.5 rounded-lg bg-amber-950/80 border border-amber-800 w-fit text-amber-400 mb-4">
              <AlertTriangle className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-base text-slate-100 mb-2">2. Deterministic Python Verification</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Math and date rules are computed in Python code ($8,500 + 1,500 = 10,000$). AI models interpret; code verifies.
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 hover:border-slate-700 transition">
            <div className="p-2.5 rounded-lg bg-emerald-950/80 border border-emerald-800 w-fit text-emerald-400 mb-4">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-base text-slate-100 mb-2">3. Adversarial Red-Team Engine</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Includes a dedicated "TRY TO DISPROVE THIS CLAIM" mode that actively searches for counter-evidence and hidden defaults.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
