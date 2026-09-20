"use client";

import { useState, useEffect } from "react";
import { X, Play, Pause, RotateCcw, CheckCircle2, Activity } from "lucide-react";
import { InvestigationStep } from "@/lib/types";

interface ReplayModalProps {
  steps: InvestigationStep[];
  onClose: () => void;
}

export default function ReplayModal({ steps, onClose }: ReplayModalProps) {
  const [currentIdx, setCurrentIdx] = useState(0);
  const [isPlaying, setIsPlaying] = useState(true);

  useEffect(() => {
    let timer: any;
    if (isPlaying && currentIdx < steps.length - 1) {
      timer = setTimeout(() => {
        setCurrentIdx((prev) => prev + 1);
      }, 1500);
    } else if (currentIdx >= steps.length - 1) {
      setIsPlaying(false);
    }
    return () => clearTimeout(timer);
  }, [isPlaying, currentIdx, steps.length]);

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/85 backdrop-blur-md flex items-center justify-center p-4">
      <div className="w-full max-w-xl bg-slate-900 border border-slate-800 rounded-xl shadow-2xl overflow-hidden flex flex-col">
        <div className="px-4 py-3 border-b border-slate-800 flex items-center justify-between bg-slate-950">
          <div className="flex items-center gap-2">
            <Activity className="w-4 h-4 text-sky-400" />
            <span className="font-mono text-xs font-bold text-slate-200">Investigation Replay Engine</span>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-200 p-1 rounded">
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="p-6 space-y-4">
          <div className="flex items-center justify-between text-xs font-mono">
            <span className="text-slate-400">Step {currentIdx + 1} of {steps.length}</span>
            <span className="text-sky-400 font-bold">
              {Math.round(((currentIdx + 1) / steps.length) * 100)}% Complete
            </span>
          </div>

          <div className="w-full bg-slate-950 rounded-full h-2 overflow-hidden border border-slate-800">
            <div
              className="bg-sky-500 h-full transition-all duration-300"
              style={{ width: `${((currentIdx + 1) / steps.length) * 100}%` }}
            ></div>
          </div>

          <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl min-h-[120px] flex flex-col justify-center">
            <span className="text-[10px] font-mono text-sky-400 font-bold block mb-1 uppercase">
              {steps[currentIdx]?.step_type}
            </span>
            <h4 className="text-sm font-bold text-slate-100">{steps[currentIdx]?.title}</h4>
            <p className="text-xs text-slate-400 mt-1">{steps[currentIdx]?.detail}</p>
          </div>

          <div className="flex items-center justify-center space-x-3 pt-2">
            <button
              onClick={() => {
                setCurrentIdx(0);
                setIsPlaying(true);
              }}
              className="p-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs flex items-center gap-1"
            >
              <RotateCcw className="w-4 h-4" />
              Restart
            </button>
            <button
              onClick={() => setIsPlaying(!isPlaying)}
              className="px-4 py-2 bg-sky-600 hover:bg-sky-500 text-white rounded-lg text-xs font-bold flex items-center gap-1.5 shadow"
            >
              {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
              {isPlaying ? "Pause Playback" : "Resume Playback"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
