"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { 
  ArrowLeft, 
  Flame, 
  Clock, 
  ShieldCheck, 
  GitMerge, 
  CheckCircle2,
  AlertCircle,
  MapPin,
  TrendingUp
} from "lucide-react";
import { 
  ResponsiveContainer, 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  Tooltip, 
  ReferenceLine, 
  CartesianGrid 
} from "recharts";
import { api } from "@/lib/api";
import { ShipmentMap } from "@/components/ShipmentMap";

export default function ShipmentDetailPage({ params }: { params: { shipment_id: string } }) {
  const [shipment, setShipment] = useState<any>(null);
  const [readings, setReadings] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      const s = await api.getShipment(params.shipment_id);
      const r = await api.getSensorReadings(params.shipment_id);
      setShipment(s);
      setReadings(r);
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
  }, [params.shipment_id]);

  if (loading || !shipment) {
    return <div className="p-8 text-center text-gray-400">Loading cold-chain telemetry data...</div>;
  }

  const chartData = readings.map((item, idx) => ({
    time: new Date(item.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" }),
    temperature: item.temperature,
    maxSafe: shipment.max_temperature,
    minSafe: shipment.min_temperature
  }));

  const isExcursion = shipment.current_temperature > shipment.max_temperature || shipment.current_temperature < shipment.min_temperature;

  return (
    <div className="space-y-6">
      {/* Top Header & Navigation */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-cardBorder">
        <div className="flex items-center gap-4">
          <Link
            href="/dashboard"
            className="p-2 rounded-lg bg-cardBg border border-cardBorder text-gray-400 hover:text-white transition"
          >
            <ArrowLeft className="w-4 h-4" />
          </Link>
          <div>
            <div className="flex items-center gap-3">
              <h1 className="text-xl font-bold text-white font-mono">{shipment.shipment_id}</h1>
              <span className={`px-3 py-0.5 rounded-full text-xs font-bold border ${
                isExcursion ? "bg-roseCritical/20 text-roseCritical border-roseCritical/30" : "bg-emeraldSuccess/20 text-emeraldSuccess border-emeraldSuccess/30"
              }`}>
                {shipment.current_status}
              </span>
              <span className="text-xs bg-white/5 text-gray-300 px-2.5 py-0.5 rounded border border-white/10">
                Criticality: <strong className="text-roseCritical">{shipment.criticality}</strong>
              </span>
            </div>
            <p className="text-xs text-gray-400 mt-1">
              Product: <span className="text-gray-200 font-semibold">{shipment.product_name}</span> ({shipment.product_type})
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <Link
            href="/decisions"
            className="px-4 py-2 text-xs font-bold rounded-lg bg-cyanAccent/10 text-cyanAccent border border-cyanAccent/30 hover:bg-cyanAccent/20 transition flex items-center gap-1.5"
          >
            <GitMerge className="w-4 h-4" /> View AI Decision Pipeline
          </Link>
          <Link
            href="/approvals"
            className="px-4 py-2 text-xs font-bold rounded-lg bg-gradient-to-r from-roseCritical to-amberWarning text-white shadow-lg shadow-roseCritical/20 hover:opacity-95 transition flex items-center gap-1.5"
          >
            <CheckCircle2 className="w-4 h-4" /> Go to Approval Center
          </Link>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="bg-cardBg border border-cardBorder p-4 rounded-xl space-y-1">
          <span className="text-xs text-gray-400 font-semibold">Current Sensor Temperature</span>
          <p className={`text-2xl font-bold font-mono ${isExcursion ? "text-roseCritical" : "text-emeraldSuccess"}`}>
            {shipment.current_temperature}°C
          </p>
          <span className="text-[11px] text-gray-400">Safe Limit: {shipment.min_temperature}°C – {shipment.max_temperature}°C</span>
        </div>

        <div className="bg-cardBg border border-cardBorder p-4 rounded-xl space-y-1">
          <span className="text-xs text-gray-400 font-semibold">Calculated Risk Score</span>
          <p className="text-2xl font-bold font-mono text-roseCritical">91 <span className="text-xs text-gray-400 font-normal">/ 100</span></p>
          <span className="text-[11px] text-roseCritical font-semibold">CRITICAL Risk Tier</span>
        </div>

        <div className="bg-cardBg border border-cardBorder p-4 rounded-xl space-y-1">
          <span className="text-xs text-gray-400 font-semibold">Logistics Route & Delay</span>
          <p className="text-lg font-bold text-white">{shipment.origin} → {shipment.destination}</p>
          <span className="text-[11px] text-amberWarning font-medium">Delay: +{shipment.delay_minutes} min (High Traffic)</span>
        </div>

        <div className="bg-cardBg border border-cardBorder p-4 rounded-xl space-y-1">
          <span className="text-xs text-gray-400 font-semibold">Nearest Cold Storage</span>
          <p className="text-lg font-bold text-cyanAccent">8.4 km away</p>
          <span className="text-[11px] text-gray-400">Depot #4 (ETA: 23 mins)</span>
        </div>
      </div>

      {/* Temperature Telemetry Graph & Map Split */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recharts Temperature Chart */}
        <div className="bg-cardBg border border-cardBorder rounded-xl p-5 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-cyanAccent" />
                Realtime Thermal Telemetry Stream
              </h3>
              <p className="text-xs text-gray-400">Threshold upper boundary set at 8.0°C</p>
            </div>
            <span className="text-xs font-mono bg-white/5 text-gray-300 px-2 py-1 rounded">2°C–8°C Corridor</span>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" />
                <XAxis dataKey="time" stroke="#9CA3AF" tick={{ fontSize: 11 }} />
                <YAxis domain={[0, 12]} stroke="#9CA3AF" tick={{ fontSize: 11 }} />
                <Tooltip
                  contentStyle={{ backgroundColor: "#111827", borderColor: "#1F2937", borderRadius: "8px", color: "#FFF" }}
                />
                <ReferenceLine y={8.0} label={{ value: "Max 8.0°C", fill: "#EF4444", fontSize: 11 }} stroke="#EF4444" strokeDasharray="4 4" />
                <ReferenceLine y={2.0} label={{ value: "Min 2.0°C", fill: "#10B981", fontSize: 11 }} stroke="#10B981" strokeDasharray="4 4" />
                <Line
                  type="monotone"
                  dataKey="temperature"
                  stroke="#EF4444"
                  strokeWidth={3}
                  dot={{ fill: "#EF4444", r: 4 }}
                  activeDot={{ r: 7 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Route Map */}
        <div className="bg-cardBg border border-cardBorder rounded-xl p-5 space-y-4">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <MapPin className="w-4 h-4 text-cyanAccent" />
            Route Corridor & Reroute Target
          </h3>
          <ShipmentMap
            latitude={shipment.current_latitude}
            longitude={shipment.current_longitude}
            status={shipment.current_status}
            destination={shipment.destination}
          />
        </div>
      </div>

      {/* AI Recommendation & Recovery Options Box */}
      <div className="bg-cardBg border border-cardBorder rounded-xl p-5 space-y-4">
        <div className="flex items-center justify-between pb-3 border-b border-cardBorder">
          <div>
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <GitMerge className="w-4 h-4 text-cyanAccent" />
              Scenario Planning Agent Recovery Options
            </h3>
            <p className="text-xs text-gray-400">Ranked by thermal safety preservation and cost efficiency</p>
          </div>
          <span className="text-xs bg-cyanAccent/20 text-cyanAccent px-3 py-1 rounded-full font-bold">
            AI Confidence: 94%
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Option 1 */}
          <div className="p-4 rounded-xl bg-white/5 border border-cardBorder space-y-2">
            <span className="text-xs text-gray-400 font-mono">Option 1</span>
            <h4 className="text-sm font-bold text-white">Continue Current Route</h4>
            <div className="text-xs text-gray-400 space-y-1 font-mono">
              <p>ETA: 65 mins</p>
              <p>Cost: ₹0</p>
              <p className="text-roseCritical font-bold">Risk Level: HIGH</p>
            </div>
            <p className="text-[11px] text-gray-400">High probability of total product thermal spoilage.</p>
          </div>

          {/* Option 2 Recommended */}
          <div className="p-4 rounded-xl bg-cyanAccent/10 border-2 border-cyanAccent space-y-2 relative shadow-lg shadow-cyanAccent/10">
            <span className="absolute top-3 right-3 text-[10px] bg-cyanAccent text-darkBg px-2 py-0.5 rounded font-bold">
              RECOMMENDED
            </span>
            <span className="text-xs text-cyanAccent font-mono">Option 2</span>
            <h4 className="text-sm font-bold text-white">Reroute to Cold Storage</h4>
            <div className="text-xs text-gray-300 space-y-1 font-mono">
              <p>Distance: 8.4 km | ETA: 23 mins</p>
              <p>Cost: ₹2,400</p>
              <p className="text-emeraldSuccess font-bold">Risk Level: LOW</p>
            </div>
            <p className="text-[11px] text-gray-300 leading-tight">
              Minimizes thermal exposure by immediately transferring shipment to cold storage facility #4.
            </p>
          </div>

          {/* Option 3 */}
          <div className="p-4 rounded-xl bg-white/5 border border-cardBorder space-y-2">
            <span className="text-xs text-gray-400 font-mono">Option 3</span>
            <h4 className="text-sm font-bold text-white">Refrigeration Replacement</h4>
            <div className="text-xs text-gray-400 space-y-1 font-mono">
              <p>ETA: 35 mins</p>
              <p>Cost: ₹6,500</p>
              <p className="text-amberWarning font-bold">Risk Level: MEDIUM</p>
            </div>
            <p className="text-[11px] text-gray-400">Higher cost and delay in waiting for service unit.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
