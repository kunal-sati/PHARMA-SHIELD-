"use client";

import { useState } from "react";
import { Play, Flame, RefreshCw, CheckCircle, Zap } from "lucide-react";
import { api } from "@/lib/api";
import { useAppContext } from "@/components/AppProviders";

interface SimulationControlsProps {
  onRefresh?: () => void;
}

export function SimulationControls({ onRefresh }: SimulationControlsProps) {
  const [loading, setLoading] = useState(false);
  const [lastAction, setLastAction] = useState<string | null>(null);
  const { role, permissions } = useAppContext();
  const canUseSimulation = permissions.canOperate;

  const handleRunExcursion = async () => {
    if (!canUseSimulation) return;
    setLoading(true);
    try {
      await api.runVaccineDemo();
      setLastAction("Primary Vaccine Excursion Triggered (PS-1026)");
      if (onRefresh) onRefresh();
    } catch (err: any) {
      alert(`Simulation Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = async () => {
    if (!permissions.canManageSimulation) return;
    setLoading(true);
    try {
      await api.resetDemo();
      setLastAction("Demo Scenario Reset to Normal");
      if (onRefresh) onRefresh();
    } catch (err: any) {
      alert(`Reset Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleNormal = async () => {
    if (!canUseSimulation) return;
    setLoading(true);
    try {
      await api.startSimulation("PS-1026");
      setLastAction("Started Normal Telemetry Simulation");
      if (onRefresh) onRefresh();
    } catch (err: any) {
      alert(`Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-cardBg/90 border border-cardBorder rounded-xl p-4 flex flex-wrap items-center justify-between gap-4 shadow-xl">
      <div className="flex items-center gap-3">
        <div className="p-2 rounded-lg bg-cyanAccent/10 text-cyanAccent border border-cyanAccent/20">
          <Zap className="w-5 h-5" />
        </div>
        <div>
          <h3 className="text-sm font-bold text-white flex items-center gap-2">
            Hackathon Demo Simulator
            <span className="text-[10px] bg-cyanAccent/20 text-cyanAccent px-2 py-0.5 rounded-full font-semibold">
              PS-1026 Vaccine Corridor
            </span>
          </h3>
          <p className="text-xs text-gray-400">
            {lastAction ? (
              <span className="text-cyanAccent font-medium">Last Action: {lastAction}</span>
            ) : (
              "Click 'Simulate Excursion' to launch the end-to-end agentic demo pipeline."
            )}
          </p>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex flex-wrap items-center gap-2">
        <button
          onClick={handleNormal}
          disabled={loading || !canUseSimulation}
          className="px-3.5 py-2 text-xs font-semibold rounded-lg bg-white/5 hover:bg-white/10 text-gray-300 border border-white/10 transition flex items-center gap-1.5"
        >
          <CheckCircle className="w-3.5 h-3.5 text-emeraldSuccess" />
          Normal Mode
        </button>

        <button
          onClick={handleRunExcursion}
          disabled={loading || !canUseSimulation}
          className="px-4 py-2 text-xs font-bold rounded-lg bg-gradient-to-r from-roseCritical to-amberWarning text-white shadow-lg shadow-roseCritical/20 hover:opacity-95 transition flex items-center gap-2 disabled:opacity-50"
        >
          <Flame className="w-4 h-4 animate-bounce" />
          Simulate Temperature Excursion (9.6°C)
        </button>

        <button
          onClick={handleReset}
          disabled={loading || !permissions.canManageSimulation}
          className="px-3.5 py-2 text-xs font-semibold rounded-lg bg-white/5 hover:bg-white/10 text-gray-300 border border-white/10 transition flex items-center gap-1.5"
        >
          <RefreshCw className={`w-3.5 h-3.5 text-cyanAccent ${loading ? "animate-spin" : ""}`} />
          Reset Scenario
        </button>
      </div>
      {!canUseSimulation && <p className="w-full text-right text-[10px] text-amberWarning">{role} is read-only. Operational controls are unavailable.</p>}
      {canUseSimulation && !permissions.canManageSimulation && <p className="w-full text-right text-[10px] text-gray-400">Reset Scenario requires ADMIN permission.</p>}
    </div>
  );
}
