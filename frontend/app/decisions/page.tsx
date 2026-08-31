"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { 
  GitMerge, 
  CheckCircle2, 
  Clock, 
  ShieldCheck, 
  Flame, 
  ArrowRight,
  ChevronDown,
  Cpu
} from "lucide-react";
import { api } from "@/lib/api";

export default function DecisionsPage() {
  const [auditLogs, setAuditLogs] = useState<any[]>([]);

  useEffect(() => {
    api.getAuditLogs("PS-1026").then(setAuditLogs).catch(console.error);
  }, []);

  const pipelineStages = [
    { id: 1, name: "1. Monitor Telemetry", agent: "IoT Sensor Simulator", desc: "Receives continuous temperature & GPS stream", status: "COMPLETED", time: "10:31:02 AM" },
    { id: 2, name: "2. Detect Excursion", agent: "Agent 1: Disruption Sensing Agent", desc: "Breach detected: 9.6°C exceeds 8.0°C limit", status: "COMPLETED", time: "10:31:05 AM" },
    { id: 3, name: "3. Analyze Risk", agent: "Deterministic Risk Engine", desc: "Multi-factor score calculated: 91/100 (CRITICAL)", status: "COMPLETED", time: "10:31:07 AM" },
    { id: 4, name: "4. Plan Scenarios", agent: "Agent 2: Scenario Planning Agent", desc: "Generated 3 recovery options (Continue, Reroute, Replace)", status: "COMPLETED", time: "10:31:09 AM" },
    { id: 5, name: "5. Recommend Option", agent: "Scenario Ranker", desc: "Recommended SCN-002: Reroute to Cold Storage (Confidence: 0.94)", status: "COMPLETED", time: "10:31:10 AM" },
    { id: 6, name: "6. SAP Rules Governance", agent: "ABAP Business Rules Engine", desc: "ABAP Rules 3 & 4: Human Manager Approval Mandatory", status: "COMPLETED", time: "10:31:11 AM" },
    { id: 7, name: "7. Human Approval", agent: "Approval Center (Manager Role)", desc: "Manager sign-off required for ₹2,400 / 23m reroute action", status: "ACTIVE", time: "10:31:14 AM" },
    { id: 8, name: "8. Execute Reroute", agent: "Agent 3: Execution Agent", desc: "Updates shipment state & GPS coordinates to Cold Storage", status: "PENDING", time: "--" },
    { id: 9, name: "9. Immutable Audit", agent: "Agent 4: Compliance Audit Agent", desc: "Appends complete trace under correlation ID CORR-PS1026-001", status: "PENDING", time: "--" }
  ];

  return (
    <div className="space-y-6">
      {/* Title */}
      <div className="flex items-center justify-between pb-4 border-b border-cardBorder">
        <div>
          <h1 className="text-xl font-bold text-white flex items-center gap-2">
            <Cpu className="w-5 h-5 text-cyanAccent" />
            AI Decision & Governance Center
          </h1>
          <p className="text-xs text-gray-400">
            End-to-End Orchestration Pipeline for Shipment <strong className="text-cyanAccent">PS-1026</strong>
          </p>
        </div>
        <Link
          href="/approvals"
          className="px-4 py-2 text-xs font-bold rounded-lg bg-gradient-to-r from-roseCritical to-amberWarning text-white shadow-lg shadow-roseCritical/20 hover:opacity-95 transition flex items-center gap-2"
        >
          Go to Pending Approvals <ArrowRight className="w-4 h-4" />
        </Link>
      </div>

      {/* Governance Banner */}
      <div className="p-4 rounded-xl bg-cardBg border border-cyanAccent/30 flex items-center justify-between text-xs">
        <div className="flex items-center gap-3">
          <ShieldCheck className="w-5 h-5 text-cyanAccent" />
          <div>
            <p className="font-bold text-white">Governance Paradigm Active</p>
            <p className="text-gray-400">AI recommends. SAP governs. Humans approve. System executes and audits.</p>
          </div>
        </div>
        <span className="px-3 py-1 rounded bg-amberWarning/20 text-amberWarning font-bold border border-amberWarning/30">
          SAP Rules 1–5 Enforced
        </span>
      </div>

      {/* Pipeline Steps Grid */}
      <div className="space-y-4">
        {pipelineStages.map((stage) => {
          const isCompleted = stage.status === "COMPLETED";
          const isActive = stage.status === "ACTIVE";

          return (
            <div
              key={stage.id}
              className={`p-4 rounded-xl border transition flex items-center justify-between gap-4 ${
                isActive
                  ? "bg-amberWarning/10 border-amberWarning text-white shadow-lg shadow-amberWarning/10"
                  : isCompleted
                  ? "bg-cardBg border-cardBorder hover:border-cyanAccent/40"
                  : "bg-white/5 border-cardBorder text-gray-400 opacity-60"
              }`}
            >
              <div className="flex items-center gap-4">
                <div
                  className={`w-9 h-9 rounded-full flex items-center justify-center font-bold text-xs ${
                    isActive
                      ? "bg-amberWarning text-darkBg animate-pulse"
                      : isCompleted
                      ? "bg-cyanAccent/20 text-cyanAccent border border-cyanAccent/40"
                      : "bg-gray-800 text-gray-400"
                  }`}
                >
                  {stage.id}
                </div>

                <div>
                  <div className="flex items-center gap-3">
                    <h3 className="text-sm font-bold text-white">{stage.name}</h3>
                    <span className="text-[10px] bg-white/5 text-gray-400 px-2 py-0.5 rounded font-mono">
                      {stage.agent}
                    </span>
                  </div>
                  <p className="text-xs text-gray-300 mt-0.5">{stage.desc}</p>
                </div>
              </div>

              <div className="flex items-center gap-4 text-xs">
                <span className="font-mono text-gray-400">{stage.time}</span>
                <span
                  className={`px-2.5 py-1 rounded text-[10px] font-bold ${
                    isActive
                      ? "bg-amberWarning text-darkBg"
                      : isCompleted
                      ? "bg-emeraldSuccess/20 text-emeraldSuccess border border-emeraldSuccess/30"
                      : "bg-gray-800 text-gray-400"
                  }`}
                >
                  {stage.status}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
