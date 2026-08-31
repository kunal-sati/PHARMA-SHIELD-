"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { AlertTriangle, Clock, ShieldCheck, ArrowRight, UserCheck, CheckCircle2 } from "lucide-react";
import { api } from "@/lib/api";

export default function IncidentsPage() {
  const [incidents, setIncidents] = useState<any[]>([]);

  const loadData = async () => {
    try {
      const res = await fetch("http://localhost:8000/api/incidents");
      const data = await res.json();
      setIncidents(data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-6">
      {/* Title */}
      <div className="flex items-center justify-between pb-4 border-b border-cardBorder">
        <div>
          <h1 className="text-xl font-bold text-white flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-roseCritical" />
            Cold Chain Incident Management Center
          </h1>
          <p className="text-xs text-gray-400">
            Active Disruption Incidents, Operational SLA Timers & Resolution Workflows
          </p>
        </div>
        <span className="text-xs bg-roseCritical/20 text-roseCritical border border-roseCritical/30 font-bold px-3 py-1 rounded-full">
          {incidents.length} Active Incident(s)
        </span>
      </div>

      {/* Incidents Grid */}
      <div className="space-y-4">
        {incidents.map((inc) => (
          <div key={inc.id} className="bg-cardBg border-2 border-roseCritical/40 rounded-xl p-6 space-y-4 shadow-xl">
            <div className="flex flex-wrap items-center justify-between gap-4 pb-3 border-b border-cardBorder">
              <div className="flex items-center gap-3">
                <span className="px-2.5 py-1 rounded text-[10px] font-bold bg-roseCritical text-white">
                  {inc.severity}
                </span>
                <h2 className="text-base font-bold text-white font-mono">{inc.id}</h2>
                <span className="text-xs text-cyanAccent font-semibold font-mono">Shipment: {inc.shipment_id}</span>
              </div>
              <div className="flex items-center gap-2 text-xs text-amberWarning font-mono">
                <Clock className="w-3.5 h-3.5" />
                <span>SLA Timer: {inc.sla_minutes} min remaining</span>
              </div>
            </div>

            <p className="text-xs text-gray-200">{inc.reason}</p>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
              <div className="bg-white/5 p-3 rounded-lg border border-cardBorder space-y-1">
                <span className="text-gray-400 font-semibold">Incident Owner</span>
                <p className="text-white font-semibold truncate">{inc.owner}</p>
              </div>

              <div className="bg-white/5 p-3 rounded-lg border border-cardBorder space-y-1">
                <span className="text-gray-400 font-semibold">Lifecycle Status</span>
                <p className="text-amberWarning font-bold">{inc.status}</p>
              </div>

              <div className="bg-white/5 p-3 rounded-lg border border-cardBorder space-y-1">
                <span className="text-gray-400 font-semibold">SAP Rule Impact</span>
                <p className="text-cyanAccent font-semibold">Rules 3 & 4 Enforced</p>
              </div>

              <div className="bg-white/5 p-3 rounded-lg border border-cardBorder space-y-1">
                <span className="text-gray-400 font-semibold">Target Action</span>
                <p className="text-emeraldSuccess font-semibold">Reroute Cold Storage</p>
              </div>
            </div>

            <div className="flex items-center justify-between pt-2 border-t border-cardBorder">
              <span className="text-[11px] text-gray-400 font-mono">Created: {new Date(inc.created_at).toLocaleTimeString()}</span>
              <div className="flex items-center gap-3">
                <Link
                  href="/decisions"
                  className="px-3.5 py-1.5 rounded text-xs font-semibold bg-white/5 hover:bg-white/10 text-cyanAccent border border-cyanAccent/30 transition"
                >
                  View AI Pipeline
                </Link>
                <Link
                  href="/approvals"
                  className="px-4 py-1.5 rounded text-xs font-bold bg-gradient-to-r from-roseCritical to-amberWarning text-white shadow hover:opacity-95 transition"
                >
                  Resolve Incident &rarr;
                </Link>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
