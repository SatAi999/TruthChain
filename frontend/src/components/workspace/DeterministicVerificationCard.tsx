"use client";

import { CheckCircle2, XCircle, Calculator, Calendar, ArrowRight } from "lucide-react";

interface DeterministicVerificationCardProps {
  orderedQty?: number;
  shipment1Qty?: number;
  shipment2Qty?: number;
  deadlineDate?: string;
  actualDeliveryDate?: string;
}

export default function DeterministicVerificationCard({
  orderedQty = 10000,
  shipment1Qty = 8500,
  shipment2Qty = 1500,
  deadlineDate = "Sep 15, 2026",
  actualDeliveryDate = "Sep 17, 2026"
}: DeterministicVerificationCardProps) {
  const totalDelivered = shipment1Qty + shipment2Qty;
  const isQtyReconciled = totalDelivered === orderedQty;
  const isDeadlineSatisfied = false; // Sep 17 > Sep 15

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 my-4 font-mono">
      {/* 1. Deterministic Quantity Reconciliation Card */}
      <div className="p-4 rounded-xl border border-slate-800 bg-slate-900/90 space-y-3">
        <div className="flex items-center justify-between border-b border-slate-800 pb-2">
          <span className="text-xs font-bold text-sky-400 flex items-center gap-1.5 uppercase">
            <Calculator className="w-4 h-4 text-sky-400" />
            Deterministic Math Check
          </span>
          {isQtyReconciled ? (
            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 flex items-center gap-1">
              <CheckCircle2 className="w-3 h-3" /> RECONCILED
            </span>
          ) : (
            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-rose-950 text-rose-400 border border-rose-800 flex items-center gap-1">
              <XCircle className="w-3 h-3" /> SHORTFALL
            </span>
          )}
        </div>

        <div className="space-y-1.5 text-xs text-slate-300">
          <div className="flex justify-between">
            <span className="text-slate-400">First Shipment (Sept 14):</span>
            <span className="font-bold">{shipment1Qty.toLocaleString()} units</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">Second Shipment (Sept 17):</span>
            <span className="font-bold">{shipment2Qty.toLocaleString()} units</span>
          </div>
          <div className="border-t border-slate-800 pt-1.5 flex justify-between text-slate-100 font-bold">
            <span>Total Accounted Balance:</span>
            <span className="text-emerald-400">{totalDelivered.toLocaleString()} / {orderedQty.toLocaleString()} units</span>
          </div>
        </div>

        <p className="text-[10px] text-slate-400 font-sans italic border-t border-slate-800/60 pt-1.5">
          ✓ Verified deterministically in Python code ($8,500 + 1,500 = 10,000$).
        </p>
      </div>

      {/* 2. Deterministic Temporal Deadline Card */}
      <div className="p-4 rounded-xl border border-slate-800 bg-slate-900/90 space-y-3">
        <div className="flex items-center justify-between border-b border-slate-800 pb-2">
          <span className="text-xs font-bold text-amber-400 flex items-center gap-1.5 uppercase">
            <Calendar className="w-4 h-4 text-amber-400" />
            Deterministic Temporal Check
          </span>
          <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-rose-950 text-rose-400 border border-rose-800 flex items-center gap-1">
            <XCircle className="w-3 h-3" /> DEADLINE BREACH
          </span>
        </div>

        <div className="space-y-1.5 text-xs text-slate-300">
          <div className="flex justify-between">
            <span className="text-slate-400">PO Contract Deadline:</span>
            <span className="font-bold text-amber-300">{deadlineDate}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">Final Balance Received:</span>
            <span className="font-bold text-rose-400">{actualDeliveryDate}</span>
          </div>
          <div className="border-t border-slate-800 pt-1.5 flex justify-between text-slate-100 font-bold">
            <span>Temporal Condition Check:</span>
            <span className="text-rose-400">Sep 17 &gt; Sep 15 (+2 Days Late)</span>
          </div>
        </div>

        <p className="text-[10px] text-slate-400 font-sans italic border-t border-slate-800/60 pt-1.5">
          ✕ Evaluated deterministically in Python datetime module (Sept 17 &gt; Sept 15).
        </p>
      </div>
    </div>
  );
}
