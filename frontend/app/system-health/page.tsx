"use client";

import { useEffect, useState } from "react";
import { Activity, Server, Database, Radio, Cpu, ShieldCheck } from "lucide-react";

export default function SystemHealthPage() {
  const [health, setHealth] = useState<any>(null);

  useEffect(() => {
    fetch("http://localhost:8000/api/system-health")
      .then(res => res.json())
      .then(setHealth)
      .catch(console.error);
  }, []);

  if (!health) return <div className="p-8 text-center text-gray-400">Checking system health...</div>;

  return (
    <div className="space-y-6">
      {/* Title */}
      <div className="flex items-center justify-between pb-4 border-b border-cardBorder">
        <div>
          <h1 className="text-xl font-bold text-white flex items-center gap-2">
            <Activity className="w-5 h-5 text-emeraldSuccess animate-pulse" />
            System Health & Observability Dashboard
          </h1>
          <p className="text-xs text-gray-400">
            Realtime Subsystem Telemetry: Database, WebSockets, Agents & SAP Integration Health
          </p>
        </div>
        <span className="text-xs bg-emeraldSuccess/20 text-emeraldSuccess font-bold px-3 py-1 rounded border border-emeraldSuccess/30">
          ALL SYSTEMS HEALTHY
        </span>
      </div>

      {/* Subsystem Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-cardBg border border-cardBorder p-5 rounded-xl space-y-4">
          <h3 className="text-sm font-bold text-white flex items-center gap-2">
            <Database className="w-4 h-4 text-cyanAccent" /> Database Subsystem
          </h3>
          <div className="text-xs space-y-2">
            <div className="flex items-center justify-between p-2.5 rounded bg-white/5 border border-cardBorder">
              <span className="text-gray-400">Engine</span>
              <span className="font-mono text-white">{health.subsystems.database.engine}</span>
            </div>
            <div className="flex items-center justify-between p-2.5 rounded bg-emeraldSuccess/10 text-emeraldSuccess border border-emeraldSuccess/30">
              <span>Status</span>
              <span className="font-bold">{health.subsystems.database.status}</span>
            </div>
          </div>
        </div>

        <div className="bg-cardBg border border-cardBorder p-5 rounded-xl space-y-4">
          <h3 className="text-sm font-bold text-white flex items-center gap-2">
            <Radio className="w-4 h-4 text-blueAccent" /> WebSocket Telemetry Stream
          </h3>
          <div className="text-xs space-y-2">
            <div className="flex items-center justify-between p-2.5 rounded bg-white/5 border border-cardBorder">
              <span className="text-gray-400">Active WebSocket Clients</span>
              <span className="font-mono text-white">{health.subsystems.websocket_stream.active_clients}</span>
            </div>
            <div className="flex items-center justify-between p-2.5 rounded bg-emeraldSuccess/10 text-emeraldSuccess border border-emeraldSuccess/30">
              <span>Status</span>
              <span className="font-bold">{health.subsystems.websocket_stream.status}</span>
            </div>
          </div>
        </div>

        <div className="bg-cardBg border border-cardBorder p-5 rounded-xl space-y-4">
          <h3 className="text-sm font-bold text-white flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-amberWarning" /> SAP Governance Adapter
          </h3>
          <div className="text-xs space-y-2">
            <div className="flex items-center justify-between p-2.5 rounded bg-white/5 border border-cardBorder">
              <span className="text-gray-400">Integration Mode</span>
              <span className="font-mono text-amberWarning font-bold">{health.subsystems.sap_governance_adapter.mode}</span>
            </div>
            <div className="flex items-center justify-between p-2.5 rounded bg-emeraldSuccess/10 text-emeraldSuccess border border-emeraldSuccess/30">
              <span>Status</span>
              <span className="font-bold">{health.subsystems.sap_governance_adapter.status}</span>
            </div>
          </div>
        </div>

        <div className="bg-cardBg border border-cardBorder p-5 rounded-xl space-y-4">
          <h3 className="text-sm font-bold text-white flex items-center gap-2">
            <Cpu className="w-4 h-4 text-cyanAccent" /> Agentic Pipeline Latency
          </h3>
          <div className="text-xs space-y-2">
            <div className="flex items-center justify-between p-2.5 rounded bg-white/5 border border-cardBorder">
              <span className="text-gray-400">Disruption Agent</span>
              <span className="font-mono text-white">{health.subsystems.disruption_agent.latency_ms} ms</span>
            </div>
            <div className="flex items-center justify-between p-2.5 rounded bg-white/5 border border-cardBorder">
              <span className="text-gray-400">Planning Agent</span>
              <span className="font-mono text-white">{health.subsystems.planning_agent.latency_ms} ms</span>
            </div>
            <div className="flex items-center justify-between p-2.5 rounded bg-white/5 border border-cardBorder">
              <span className="text-gray-400">Execution Agent</span>
              <span className="font-mono text-white">{health.subsystems.execution_agent.latency_ms} ms</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
