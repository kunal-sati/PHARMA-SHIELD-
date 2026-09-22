"use client";

import { useState } from "react";
import { Sliders, Play, TrendingDown, DollarSign, Clock, ShieldCheck, AlertTriangle } from "lucide-react";
import { useAppContext } from "@/components/AppProviders";

export default function SimulationsPage() {
  const [selectedOption, setSelectedOption] = useState("REROUTE_TO_COLD_STORAGE");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>({
    option: "REROUTE_TO_COLD_STORAGE",
    simulated_eta_minutes: 23,
    simulated_cost: 2400.0,
    projected_risk_score: 24,
    projected_product_health_pct: 91.5,
    recovery_probability_pct: 96.0,
    recommendation: "OPTIMAL (Immediate thermal stabilization at Depot #4)"
  });
  const { selectedShipmentId, permissions } = useAppContext();
  const canSimulate = permissions.canOperate;

  const handleSimulate = async (opt: string) => {
    if (!canSimulate) return;
    setSelectedOption(opt);
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/simulations/what-if", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ shipment_id: selectedShipmentId, selected_option: opt })
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Title */}
      <div className="flex items-center justify-between pb-4 border-b border-cardBorder">
        <div>
          <h1 className="text-xl font-bold text-white flex items-center gap-2">
            <Sliders className="w-5 h-5 text-cyanAccent" />
            What-If Scenario & Route Intelligence Simulator
          </h1>
          <p className="text-xs text-gray-400">
            Compare hypothetical recovery routes, cost impact, and thermal preservation probability for <strong className="text-cyanAccent">{selectedShipmentId}</strong>
          </p>
        </div>
        <span className="text-xs bg-amberWarning/20 text-amberWarning font-bold px-3 py-1 rounded border border-amberWarning/30">
          SIMULATION MODE — NO LIVE STATE MUTATION
        </span>
      </div>

      {/* Selector Buttons */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <button
          onClick={() => handleSimulate("CONTINUE_ROUTE")}
          disabled={!canSimulate || loading}
          className={`p-4 rounded-xl border text-left space-y-2 transition ${
            selectedOption === "CONTINUE_ROUTE"
              ? "bg-roseCritical/10 border-roseCritical shadow-lg shadow-roseCritical/10"
              : "bg-cardBg border-cardBorder hover:border-white/20"
          }`}
        >
          <span className="text-xs font-mono text-gray-400">Scenario A</span>
          <h3 className="text-sm font-bold text-white">Continue Current Route</h3>
          <p className="text-xs text-gray-400">Proceed to Chandigarh under heavy traffic and delay.</p>
        </button>

        <button
          onClick={() => handleSimulate("REROUTE_TO_COLD_STORAGE")}
          disabled={!canSimulate || loading}
          className={`p-4 rounded-xl border text-left space-y-2 transition ${
            selectedOption === "REROUTE_TO_COLD_STORAGE"
              ? "bg-cyanAccent/10 border-cyanAccent shadow-lg shadow-cyanAccent/10"
              : "bg-cardBg border-cardBorder hover:border-white/20"
          }`}
        >
          <span className="text-xs font-mono text-cyanAccent">Scenario B (Recommended)</span>
          <h3 className="text-sm font-bold text-white">Reroute to Cold Storage</h3>
          <p className="text-xs text-gray-400">Divert 8.4 km to Northern Depot #4 for immediate cooling.</p>
        </button>

        <button
          onClick={() => handleSimulate("REFRIGERATION_UNIT_REPLACEMENT")}
          disabled={!canSimulate || loading}
          className={`p-4 rounded-xl border text-left space-y-2 transition ${
            selectedOption === "REFRIGERATION_UNIT_REPLACEMENT"
              ? "bg-amberWarning/10 border-amberWarning shadow-lg shadow-amberWarning/10"
              : "bg-cardBg border-cardBorder hover:border-white/20"
          }`}
        >
          <span className="text-xs font-mono text-amberWarning">Scenario C</span>
          <h3 className="text-sm font-bold text-white">Refrigeration Replacement</h3>
          <p className="text-xs text-gray-400">Dispatch mobile cooling swap unit to current highway location.</p>
        </button>
      </div>
      {!canSimulate && <p className="text-xs text-amberWarning">Auditor access is read-only; simulation actions are unavailable.</p>}

      {/* Simulated Outcome Display */}
      {result && (
        <div className="bg-cardBg border border-cardBorder rounded-xl p-6 space-y-6 shadow-xl">
          <div className="flex items-center justify-between pb-3 border-b border-cardBorder">
            <h3 className="text-base font-bold text-white">Simulated Outcome Matrix: {result.option}</h3>
            <span className="text-xs font-semibold text-cyanAccent">{result.recommendation}</span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
            <div className="bg-white/5 p-4 rounded-xl border border-cardBorder space-y-1">
              <span className="text-gray-400 font-semibold">Predicted ETA</span>
              <p className="text-2xl font-bold font-mono text-white">{result.simulated_eta_minutes} mins</p>
            </div>

            <div className="bg-white/5 p-4 rounded-xl border border-cardBorder space-y-1">
              <span className="text-gray-400 font-semibold">Simulated Cost</span>
              <p className="text-2xl font-bold font-mono text-cyanAccent">₹{result.simulated_cost}</p>
            </div>

            <div className="bg-white/5 p-4 rounded-xl border border-cardBorder space-y-1">
              <span className="text-gray-400 font-semibold">Projected Risk Score</span>
              <p className={`text-2xl font-bold font-mono ${result.projected_risk_score > 70 ? "text-roseCritical" : "text-emeraldSuccess"}`}>
                {result.projected_risk_score} / 100
              </p>
            </div>

            <div className="bg-white/5 p-4 rounded-xl border border-cardBorder space-y-1">
              <span className="text-gray-400 font-semibold">Recovery Probability</span>
              <p className="text-2xl font-bold font-mono text-emeraldSuccess">{result.recovery_probability_pct}%</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
