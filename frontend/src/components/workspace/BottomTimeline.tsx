"use client";

import { Calendar, Clock, AlertTriangle, FileText, CheckCircle2 } from "lucide-react";
import { EventItem } from "@/lib/types";

interface BottomTimelineProps {
  events: EventItem[];
  onSelectEvent?: (ev: EventItem) => void;
}

export default function BottomTimeline({ events, onSelectEvent }: BottomTimelineProps) {
  return (
    <div className="w-full bg-slate-950 border-t border-slate-800 px-4 py-3 h-48 overflow-x-auto flex flex-col justify-between">
      <div className="flex items-center justify-between mb-2">
        <span className="text-[10px] font-mono uppercase tracking-widest text-slate-400 flex items-center gap-1.5">
          <Calendar className="w-3.5 h-3.5 text-sky-400" />
          Chronological Event & Provenance Timeline
        </span>
        <span className="text-[10px] font-mono text-slate-500">Deterministic Time Reconstruction</span>
      </div>

      <div className="flex items-center space-x-4 overflow-x-auto pb-2">
        {events.map((ev, idx) => {
          const isDeadline = ev.is_deadline;
          const isLateDelivery = ev.description.toLowerCase().includes("second delivery") || ev.display_date.includes("17 Sep");

          return (
            <div
              key={ev.id || idx}
              onClick={() => onSelectEvent && onSelectEvent(ev)}
              className={`shrink-0 w-64 p-3 rounded-lg border cursor-pointer transition flex flex-col justify-between ${
                isDeadline
                  ? "bg-rose-950/40 border-rose-800 hover:border-rose-600"
                  : isLateDelivery
                  ? "bg-amber-950/40 border-amber-800 hover:border-amber-600"
                  : "bg-slate-900/80 border-slate-800 hover:border-sky-600"
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-1">
                  <span className="font-mono text-xs font-bold text-sky-400">{ev.display_date}</span>
                  {isDeadline ? (
                    <span className="text-[9px] font-mono font-bold bg-rose-950 border border-rose-800 text-rose-400 px-1.5 py-0.5 rounded">
                      DEADLINE
                    </span>
                  ) : (
                    <span className="text-[9px] font-mono text-slate-400">{ev.event_type}</span>
                  )}
                </div>

                <p className="text-xs text-slate-200 line-clamp-2 leading-snug">{ev.description}</p>
              </div>

              <div className="mt-2 text-[10px] font-mono text-slate-400 flex items-center justify-between pt-1 border-t border-slate-800/60">
                <span className="truncate">{ev.location || "Receiving Dock"}</span>
                <span className="text-sky-400 underline flex items-center gap-0.5">
                  <FileText className="w-2.5 h-2.5" /> Source
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
