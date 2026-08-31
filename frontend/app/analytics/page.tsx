"use client";

import { useEffect, useState } from "react";
import { BarChart3, TrendingUp, ShieldCheck, DollarSign, Clock, Activity } from "lucide-react";

export default function AnalyticsPage() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    fetch("http://localhost:8000/api/analytics/summary")
      .then((res) => res.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return <div className="p-8 text-center text-gray-400">Loading fleet analytics...</div>;

  return (
    <div className="space-y-6">
      {/* Title */}
      <div className="flex items-center justify-between pb-4 border-b border-cardBorder">
        <div>
          <h1 className="text-xl font-bold text-white flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-cyanAccent" />
            Fleet Analytics & Cold Chain Intelligence
          </h1>
          <p className="text-xs text-gray-400">
            Network Resilience Metrics, Recovery Performance, and Product Loss Prevention Analysis
          </p>
        </div>
        <span className="text-xs bg-white/5 border border-white/10 px-3 py-1 rounded text-gray-300 font-mono">
          Last 24 Hours Metrics
        </span>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="bg-cardBg border border-cardBorder p-4 rounded-xl space-y-1">
          <span className="text-xs text-gray-400 font-semibold">Resilience Score</span>
          <p className="text-2xl font-bold text-cyanAccent font-mono">{data.resilience_kpis.supply_chain_resilience_score}%</p>
          <span className="text-[10px] text-emeraldSuccess font-medium">Target: &gt;95%</span>
        </div>

        <div className="bg-cardBg border border-cardBorder p-4 rounded-xl space-y-1">
          <span className="text-xs text-gray-400 font-semibold">Cold Chain Compliance</span>
          <p className="text-2xl font-bold text-emeraldSuccess font-mono">{data.resilience_kpis.cold_chain_compliance_rate}%</p>
          <span className="text-[10px] text-gray-400">Thermal integrity rate</span>
        </div>

        <div className="bg-cardBg border border-cardBorder p-4 rounded-xl space-y-1">
          <span className="text-xs text-gray-400 font-semibold">Recovery Success</span>
          <p className="text-2xl font-bold text-emeraldSuccess font-mono">{data.resilience_kpis.recovery_success_rate}%</p>
          <span className="text-[10px] text-gray-400">Avg time: {data.resilience_kpis.avg_recovery_time_minutes} min</span>
        </div>

        <div className="bg-cardBg border border-cardBorder p-4 rounded-xl space-y-1">
          <span className="text-xs text-gray-400 font-semibold">Avoided Product Loss</span>
          <p className="text-2xl font-bold text-cyanAccent font-mono">{data.resilience_kpis.avoided_product_loss_val}</p>
          <span className="text-[10px] text-gray-400">Simulated valuation</span>
        </div>
      </div>

      {/* Corridor Performance Table */}
      <div className="bg-cardBg border border-cardBorder rounded-xl p-5 space-y-4">
        <h3 className="text-base font-bold text-white">Cold Chain Logistics Corridor Performance</h3>
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="border-b border-cardBorder text-gray-400 uppercase font-semibold">
              <th className="py-2.5 px-3">Corridor</th>
              <th className="py-2.5 px-3">Shipment Volume</th>
              <th className="py-2.5 px-3">Excursion Rate</th>
              <th className="py-2.5 px-3">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-cardBorder text-gray-300 font-mono">
            {data.corridor_performance.map((c: any, i: number) => (
              <tr key={i} className="hover:bg-white/5">
                <td className="py-3 px-3 font-sans font-semibold text-white">{c.corridor}</td>
                <td className="py-3 px-3">{c.volume} shipments</td>
                <td className="py-3 px-3">{c.excursion_rate}</td>
                <td className="py-3 px-3">
                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                    c.status === "OPTIMAL" ? "bg-emeraldSuccess/20 text-emeraldSuccess" : "bg-amberWarning/20 text-amberWarning"
                  }`}>
                    {c.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
