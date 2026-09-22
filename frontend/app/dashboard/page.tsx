"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { 
  Package, 
  CheckCircle, 
  AlertTriangle, 
  Flame, 
  Clock, 
  ArrowRight,
  TrendingUp,
  ShieldCheck
} from "lucide-react";
import { api } from "@/lib/api";
import { SimulationControls } from "@/components/SimulationControls";
import { ShipmentMap } from "@/components/ShipmentMap";
import { useAppContext } from "@/components/AppProviders";

export default function DashboardPage() {
  const [shipments, setShipments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const { selectedShipmentId, selectShipment } = useAppContext();

  const loadData = async () => {
    try {
      const data = await api.getShipments();
      setShipments(data);
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
  }, []);

  const total = shipments.length;
  const normal = shipments.filter(s => s.current_status === "NORMAL" || s.current_status === "IN_TRANSIT").length;
  const warning = shipments.filter(s => s.current_status === "WARNING").length;
  const critical = shipments.filter(s => s.current_status === "CRITICAL" || s.current_status === "AWAITING_APPROVAL").length;
  const recovered = shipments.filter(s => s.current_status === "RECOVERED").length;

  const targetShipment = shipments.find(s => s.shipment_id === selectedShipmentId) || shipments[0];
  const selectedId = targetShipment?.shipment_id || selectedShipmentId;

  return (
    <div className="space-y-6">
      {/* Simulation Controls Banner */}
      <SimulationControls onRefresh={loadData} />

      {/* KPI Cards Row */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
        {/* Total */}
        <div className="bg-cardBg border border-cardBorder p-4 rounded-xl space-y-2">
          <div className="flex items-center justify-between text-gray-400">
            <span className="text-xs font-semibold">Total Tracked</span>
            <Package className="w-4 h-4 text-cyanAccent" />
          </div>
          <p className="text-2xl font-bold text-white">{total}</p>
          <span className="text-[11px] text-gray-400">Cold chain corridors</span>
        </div>

        {/* Normal */}
        <div className="bg-cardBg border border-cardBorder p-4 rounded-xl space-y-2">
          <div className="flex items-center justify-between text-gray-400">
            <span className="text-xs font-semibold">Normal State</span>
            <CheckCircle className="w-4 h-4 text-emeraldSuccess" />
          </div>
          <p className="text-2xl font-bold text-emeraldSuccess">{normal}</p>
          <span className="text-[11px] text-gray-400">Within 2°C–8°C limit</span>
        </div>

        {/* Warning */}
        <div className="bg-cardBg border border-cardBorder p-4 rounded-xl space-y-2">
          <div className="flex items-center justify-between text-gray-400">
            <span className="text-xs font-semibold">Warning</span>
            <AlertTriangle className="w-4 h-4 text-amberWarning" />
          </div>
          <p className="text-2xl font-bold text-amberWarning">{warning}</p>
          <span className="text-[11px] text-gray-400">Thermal threshold elevated</span>
        </div>

        {/* Critical */}
        <div className="bg-cardBg border border-cardBorder p-4 rounded-xl space-y-2">
          <div className="flex items-center justify-between text-gray-400">
            <span className="text-xs font-semibold">Critical Alert</span>
            <Flame className="w-4 h-4 text-roseCritical" />
          </div>
          <p className="text-2xl font-bold text-roseCritical">{critical}</p>
          <span className="text-[11px] text-roseCritical/80 font-medium">Excursion detected</span>
        </div>

        {/* Recovered */}
        <div className="bg-cardBg border border-cardBorder p-4 rounded-xl space-y-2">
          <div className="flex items-center justify-between text-gray-400">
            <span className="text-xs font-semibold">Recovered</span>
            <ShieldCheck className="w-4 h-4 text-blueAccent" />
          </div>
          <p className="text-2xl font-bold text-blueAccent">{recovered}</p>
          <span className="text-[11px] text-gray-400">Action executed & audited</span>
        </div>
      </div>

      {/* Main Grid: Live Map & Active Alert Sidebar */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Map Panel */}
        <div className="lg:col-span-2 bg-cardBg border border-cardBorder rounded-xl p-5 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-base font-bold text-white">Live Cold Chain Route Monitor</h3>
              <p className="text-xs text-gray-400">Active IoT Telemetry Feed — {targetShipment ? `${targetShipment.origin} to ${targetShipment.destination}` : "loading"}</p>
            </div>
            <Link
              href={`/shipments/${selectedId}`}
              className="text-xs text-cyanAccent hover:underline flex items-center gap-1 font-semibold"
            >
              Inspect Telemetry <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <ShipmentMap
            latitude={targetShipment?.current_latitude || 28.7041}
            longitude={targetShipment?.current_longitude || 77.1025}
            status={targetShipment?.current_status || "CRITICAL"}
            destination={targetShipment?.destination || "Chandigarh"}
          />
        </div>

        {/* Live Alerts Panel */}
        <div className="bg-cardBg border border-cardBorder rounded-xl p-5 space-y-4 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between pb-3 border-b border-cardBorder">
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <Flame className="w-4 h-4 text-roseCritical" />
                Live Disruption Feed
              </h3>
              <span className="text-[10px] bg-roseCritical/20 text-roseCritical px-2 py-0.5 rounded font-bold">
                REALTIME
              </span>
            </div>

            {/* Alert List */}
            <div className="mt-4 space-y-3">
              <div className="p-3.5 rounded-lg bg-roseCritical/10 border border-roseCritical/30 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-white">Shipment {selectedId}</span>
                  <span className="text-[10px] bg-roseCritical text-white font-bold px-1.5 py-0.5 rounded">
                    {targetShipment?.current_status || "MONITORING"}
                  </span>
                </div>
                <p className="text-xs text-roseCritical font-semibold">
                  Temperature: {targetShipment?.current_temperature ?? "--"}°C (Safe: {targetShipment?.min_temperature ?? "--"}°C–{targetShipment?.max_temperature ?? "--"}°C)
                </p>
                <div className="text-[11px] text-gray-400 flex items-center justify-between">
                  <span>Product: {targetShipment?.product_type || "--"} ({targetShipment?.criticality || "--"})</span>
                  <span>Delay: {targetShipment?.delay_minutes ?? "--"}m</span>
                </div>
                <div className="pt-2 border-t border-roseCritical/20 flex items-center justify-between">
                  <span className="text-[10px] text-gray-400 font-mono">Risk Score: 91/100</span>
                  <Link
                    href="/approvals"
                    className="text-[11px] font-bold text-cyanAccent hover:underline flex items-center gap-1"
                  >
                    Action Required <ArrowRight className="w-3 h-3" />
                  </Link>
                </div>
              </div>

              <div className="p-3.5 rounded-lg bg-white/5 border border-cardBorder space-y-1">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold text-gray-300">Shipment PS-1025</span>
                  <span className="text-[10px] bg-amberWarning/20 text-amberWarning font-bold px-1.5 py-0.5 rounded">
                    WARNING
                  </span>
                </div>
                <p className="text-xs text-gray-400">Insulin Vials — Temperature elevated (7.8°C)</p>
              </div>
            </div>
          </div>

          <Link
            href="/decisions"
            className="w-full py-2.5 rounded-lg bg-cyanAccent/10 border border-cyanAccent/30 text-cyanAccent text-xs font-bold text-center hover:bg-cyanAccent/20 transition block"
          >
            Open AI Decision Center
          </Link>
        </div>
      </div>

      {/* Shipment Table */}
      <div className="bg-cardBg border border-cardBorder rounded-xl p-5 space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-base font-bold text-white">Active Cold Chain Fleet Overview</h3>
            <p className="text-xs text-gray-400">Deterministic Threshold Monitoring & SAP Governance State</p>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-cardBorder text-xs font-semibold text-gray-400 uppercase tracking-wider">
                <th className="py-3 px-4">Shipment</th>
                <th className="py-3 px-4">Product</th>
                <th className="py-3 px-4">Current Temp</th>
                <th className="py-3 px-4">Safe Range</th>
                <th className="py-3 px-4">Route / Location</th>
                <th className="py-3 px-4">Delay</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-cardBorder text-xs text-gray-300">
              {shipments.map((s) => {
                const isExcursion = s.current_temperature > s.max_temperature || s.current_temperature < s.min_temperature;
                return (
                  <tr key={s.shipment_id} className={`hover:bg-white/5 transition ${s.shipment_id === selectedId ? "bg-cyanAccent/5" : ""}`}>
                    <td className="py-3.5 px-4 font-bold text-white font-mono">{s.shipment_id}</td>
                    <td className="py-3.5 px-4">
                      <div>
                        <p className="font-semibold text-white">{s.product_name}</p>
                        <p className="text-[10px] text-gray-400">{s.product_type}</p>
                      </div>
                    </td>
                    <td className="py-3.5 px-4">
                      <span className={`font-bold font-mono px-2 py-0.5 rounded ${
                        isExcursion ? "bg-roseCritical/20 text-roseCritical border border-roseCritical/30" : "text-emeraldSuccess"
                      }`}>
                        {s.current_temperature}°C
                      </span>
                    </td>
                    <td className="py-3.5 px-4 text-gray-400 font-mono">{s.min_temperature}°C – {s.max_temperature}°C</td>
                    <td className="py-3.5 px-4">{s.origin} → {s.destination}</td>
                    <td className="py-3.5 px-4 font-mono text-gray-400">{s.delay_minutes} min</td>
                    <td className="py-3.5 px-4">
                      <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold border ${
                        s.current_status === "CRITICAL" || s.current_status === "AWAITING_APPROVAL"
                          ? "bg-roseCritical/20 text-roseCritical border-roseCritical/30"
                          : s.current_status === "RECOVERED"
                          ? "bg-blueAccent/20 text-blueAccent border-blueAccent/30"
                          : "bg-emeraldSuccess/20 text-emeraldSuccess border-emeraldSuccess/30"
                      }`}>
                        {s.current_status}
                      </span>
                    </td>
                    <td className="py-3.5 px-4 text-right">
                      <Link
                        href={`/shipments/${s.shipment_id}`}
                        onClick={() => selectShipment(s.shipment_id)}
                        className="px-3 py-1.5 rounded text-xs font-semibold bg-white/5 hover:bg-white/10 text-cyanAccent border border-cyanAccent/30 transition inline-flex items-center gap-1"
                      >
                        Inspect <ArrowRight className="w-3 h-3" />
                      </Link>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
