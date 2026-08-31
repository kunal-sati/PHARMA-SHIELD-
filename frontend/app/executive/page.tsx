"use client";

import { useEffect, useState } from "react";
import { Crown, ShieldCheck, AlertCircle, TrendingUp, DollarSign, Lock } from "lucide-react";

export default function ExecutivePage() {
  const [kpis, setKpis] = useState<any>(null);

  useEffect(() => {
    fetch("http://localhost:8000/api/executive/kpis")
      .then(res => res.json())
      .then(setKpis)
      .catch(console.error);
  }, []);

  if (!kpis) return <div className="p-8 text-center text-gray-400">Loading executive tower data...</div>;

  return (
    <div className="space-y-6">
      {/* Title */}
      <div className="flex items-center justify-between pb-4 border-b border-cardBorder">
        <div>
          <h1 className="text-xl font-bold text-white flex items-center gap-2">
            <Crown className="w-5 h-5 text-amberWarning" />
            Executive Supply Chain Control Tower
          </h1>
          <p className="text-xs text-gray-400">
            High-Level Executive Dashboard: Enterprise Resilience, Compliance & Risk Governance
          </p>
        </div>
        <span className="text-xs bg-amberWarning/20 text-amberWarning font-bold px-3 py-1 rounded border border-amberWarning/30">
          EXECUTIVE SUITE
        </span>
      </div>

      {/* Main KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-cardBg border border-cardBorder p-6 rounded-xl space-y-3 shadow-xl">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-gray-400">Resilience Index</span>
            <ShieldCheck className="w-5 h-5 text-cyanAccent" />
          </div>
          <p className="text-4xl font-bold text-cyanAccent font-mono">{kpis.resilience_score}%</p>
          <p className="text-xs text-gray-300">Network-wide cold chain recovery capability</p>
        </div>

        <div className="bg-cardBg border border-cardBorder p-6 rounded-xl space-y-3 shadow-xl">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-gray-400">Active Network Risk</span>
            <AlertCircle className="w-5 h-5 text-roseCritical" />
          </div>
          <p className="text-lg font-bold text-roseCritical">{kpis.active_risk_tier}</p>
          <p className="text-xs text-gray-300">Primary corridor: Delhi $\rightarrow$ Chandigarh (PS-1026)</p>
        </div>

        <div className="bg-cardBg border border-cardBorder p-6 rounded-xl space-y-3 shadow-xl">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-gray-400">SAP Governance</span>
            <Lock className="w-5 h-5 text-amberWarning" />
          </div>
          <p className="text-lg font-bold text-amberWarning">{kpis.sap_governance_status}</p>
          <p className="text-xs text-gray-300">ABAP Rules 1–5 enforced for human sign-off</p>
        </div>
      </div>
    </div>
  );
}
