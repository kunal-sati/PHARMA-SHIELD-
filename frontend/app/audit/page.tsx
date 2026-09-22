"use client";

import { useEffect, useState } from "react";
import { 
  FileText, 
  Filter, 
  Search, 
  Clock, 
  ShieldCheck, 
  User, 
  Cpu, 
  CheckCircle2, 
  Flame 
} from "lucide-react";
import { api } from "@/lib/api";
import { useAppContext } from "@/components/AppProviders";

export default function AuditPage() {
  const [logs, setLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [shipmentFilter, setShipmentFilter] = useState("PS-1026");
  const [actorFilter, setActorFilter] = useState("ALL");
  const { selectedShipmentId } = useAppContext();

  useEffect(() => {
    setShipmentFilter(selectedShipmentId);
  }, [selectedShipmentId]);

  const loadData = async () => {
    try {
      const data = await api.getAuditLogs(shipmentFilter || undefined);
      setLogs(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 3000);
    return () => clearInterval(interval);
  }, [shipmentFilter]);

  const filteredLogs = logs.filter(l => {
    if (actorFilter !== "ALL" && l.actor_type !== actorFilter) return false;
    return true;
  });

  return (
    <div className="space-y-6">
      {/* Title */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-cardBorder">
        <div>
          <h1 className="text-xl font-bold text-white flex items-center gap-2">
            <FileText className="w-5 h-5 text-cyanAccent" />
            Audit & Compliance Ledger
          </h1>
          <p className="text-xs text-gray-400">
            Append-Only Traceability Ledger — Correlation ID: <strong className="text-cyanAccent font-mono">CORR-PS1026-001</strong>
          </p>
        </div>

        {/* Filter Controls */}
        <div className="flex items-center gap-3 text-xs">
          <div className="flex items-center gap-1.5 bg-cardBg border border-cardBorder px-3 py-1.5 rounded-lg">
            <Filter className="w-3.5 h-3.5 text-gray-400" />
            <span className="text-gray-400">Shipment:</span>
            <select
              value={shipmentFilter}
              onChange={(e) => setShipmentFilter(e.target.value)}
              className="bg-transparent text-white font-semibold focus:outline-none"
            >
              <option value="PS-1026">PS-1026 (Vaccine Demo)</option>
              <option value="PS-1025">PS-1025</option>
              <option value="PS-1024">PS-1024</option>
              <option value="PS-1023">PS-1023 (Cryo Plasma)</option>
            </select>
          </div>

          <div className="flex items-center gap-1.5 bg-cardBg border border-cardBorder px-3 py-1.5 rounded-lg">
            <span className="text-gray-400">Actor Type:</span>
            <select
              value={actorFilter}
              onChange={(e) => setActorFilter(e.target.value)}
              className="bg-transparent text-white font-semibold focus:outline-none"
            >
              <option value="ALL">All Actors</option>
              <option value="HUMAN_MANAGER">HUMAN MANAGER</option>
              <option value="AGENT">AI AGENT</option>
              <option value="SYSTEM">SAP / SYSTEM</option>
            </select>
          </div>
        </div>
      </div>

      {/* Timeline View */}
      <div className="bg-cardBg border border-cardBorder rounded-xl p-6 space-y-6">
        <div className="flex items-center justify-between pb-3 border-b border-cardBorder">
          <h3 className="text-sm font-bold text-white">Chronological Audit Event Log</h3>
          <span className="text-xs text-gray-400 font-mono">Records: {filteredLogs.length}</span>
        </div>

        {filteredLogs.length === 0 ? (
          <p className="text-xs text-gray-400 text-center py-8">No audit events recorded for this selection.</p>
        ) : (
          <div className="relative border-l-2 border-cardBorder ml-4 space-y-6 pl-6">
            {filteredLogs.map((log, idx) => {
              const isHuman = log.actor_type === "HUMAN_MANAGER";
              const isAgent = log.actor_type === "AGENT";

              return (
                <div key={log.id} className="relative group">
                  {/* Timeline Dot */}
                  <div
                    className={`absolute -left-[31px] top-1.5 w-4 h-4 rounded-full border-2 border-darkBg ${
                      isHuman
                        ? "bg-emeraldSuccess shadow-md shadow-emeraldSuccess/30"
                        : isAgent
                        ? "bg-cyanAccent shadow-md shadow-cyanAccent/30"
                        : "bg-amberWarning"
                    }`}
                  ></div>

                  {/* Card Content */}
                  <div className="bg-white/5 border border-cardBorder rounded-xl p-4 space-y-2 hover:border-cyanAccent/40 transition">
                    <div className="flex flex-wrap items-center justify-between gap-2 text-xs">
                      <div className="flex items-center gap-2">
                        <span className="font-bold text-white font-mono">{log.event_type}</span>
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          isHuman ? "bg-emeraldSuccess/20 text-emeraldSuccess" : "bg-cyanAccent/20 text-cyanAccent"
                        }`}>
                          {log.actor_type}
                        </span>
                      </div>

                      <span className="font-mono text-gray-400 text-[11px]">
                        {new Date(log.timestamp).toLocaleTimeString()} | {new Date(log.timestamp).toLocaleDateString()}
                      </span>
                    </div>

                    <div className="text-xs text-gray-300 flex flex-wrap items-center justify-between gap-2">
                      <p>
                        Actor: <strong className="text-white">{log.actor}</strong> {log.agent && `(${log.agent})`}
                      </p>
                      <span className="font-mono text-gray-400">Action: {log.action} &rarr; Decision: <strong className="text-cyanAccent">{log.decision}</strong></span>
                    </div>

                    {log.metadata_json && Object.keys(log.metadata_json).length > 0 && (
                      <div className="pt-2 border-t border-cardBorder">
                        <pre className="text-[10px] font-mono text-gray-400 bg-darkBg/60 p-2 rounded overflow-x-auto">
                          {JSON.stringify(log.metadata_json, null, 2)}
                        </pre>
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
