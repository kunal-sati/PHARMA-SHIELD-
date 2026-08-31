"use client";

import { useEffect, useState } from "react";
import { Navigation, MapPin, Warehouse } from "lucide-react";

interface ShipmentMapProps {
  latitude?: number;
  longitude?: number;
  status?: string;
  destination?: string;
}

export function ShipmentMap({
  latitude = 28.7041,
  longitude = 77.1025,
  status = "CRITICAL",
  destination = "Chandigarh"
}: ShipmentMapProps) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return <div className="h-64 bg-cardBg rounded-xl animate-pulse"></div>;

  return (
    <div className="relative h-72 w-full rounded-xl overflow-hidden border border-cardBorder bg-[#0D1322] flex flex-col justify-between p-4 shadow-inner">
      {/* Grid Pattern Background simulating map canvas */}
      <div className="absolute inset-0 opacity-20 bg-[radial-gradient(#3B82F6_1px,transparent_1px)] [background-size:16px_16px]"></div>

      {/* Map Header Overlay */}
      <div className="relative z-10 flex items-center justify-between bg-cardBg/90 backdrop-blur px-3 py-2 rounded-lg border border-white/10 text-xs">
        <div className="flex items-center gap-2">
          <Navigation className="w-4 h-4 text-cyanAccent animate-pulse" />
          <span className="font-semibold text-white">Live GPS Corridor: Delhi → {destination}</span>
        </div>
        <span className="text-[10px] text-gray-400 font-mono">
          LAT: {latitude.toFixed(4)} | LON: {longitude.toFixed(4)}
        </span>
      </div>

      {/* Visual Simulated Route Waypoints */}
      <div className="relative z-10 my-auto flex items-center justify-between px-8">
        {/* Origin */}
        <div className="flex flex-col items-center gap-1">
          <div className="w-8 h-8 rounded-full bg-blueAccent/20 border border-blueAccent flex items-center justify-center text-blueAccent">
            <MapPin className="w-4 h-4" />
          </div>
          <span className="text-xs font-medium text-gray-300">Delhi (Origin)</span>
        </div>

        {/* Route Line & Active Vehicle */}
        <div className="flex-1 mx-4 relative flex items-center">
          <div className="w-full h-1 bg-gradient-to-r from-blueAccent via-amberWarning to-roseCritical rounded"></div>

          {/* Vehicle Marker */}
          <div className="absolute left-[45%] -top-3 transform -translate-x-1/2 flex flex-col items-center">
            <div className={`px-2 py-0.5 rounded text-[10px] font-bold text-white shadow-lg ${
              status === "CRITICAL" ? "bg-roseCritical animate-pulse" : "bg-cyanAccent text-darkBg"
            }`}>
              PS-1026
            </div>
            <div className="w-4 h-4 rounded-full bg-roseCritical border-2 border-white shadow-lg shadow-roseCritical/50"></div>
          </div>

          {/* Reroute Cold Storage Target Marker */}
          {status === "CRITICAL" || status === "AWAITING_APPROVAL" || status === "RECOVERED" ? (
            <div className="absolute right-[25%] -bottom-8 flex flex-col items-center">
              <div className="w-7 h-7 rounded-lg bg-emeraldSuccess/20 border border-emeraldSuccess flex items-center justify-center text-emeraldSuccess shadow-lg">
                <Warehouse className="w-4 h-4" />
              </div>
              <span className="text-[10px] font-semibold text-emeraldSuccess whitespace-nowrap">
                Cold Storage (8.4 km)
              </span>
            </div>
          ) : null}
        </div>

        {/* Destination */}
        <div className="flex flex-col items-center gap-1">
          <div className="w-8 h-8 rounded-full bg-gray-800 border border-gray-600 flex items-center justify-center text-gray-400">
            <MapPin className="w-4 h-4" />
          </div>
          <span className="text-xs font-medium text-gray-300">{destination}</span>
        </div>
      </div>

      {/* Map Legend Footer */}
      <div className="relative z-10 flex items-center justify-between text-[11px] text-gray-400 bg-cardBg/90 backdrop-blur px-3 py-1.5 rounded-lg border border-white/10">
        <div className="flex items-center gap-4">
          <span className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-roseCritical"></span>
            Excursion Point (9.6°C)
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-emeraldSuccess"></span>
            Reroute Target (23 min ETA)
          </span>
        </div>
        <span className="text-cyanAccent font-medium">NH-44 Expressway</span>
      </div>
    </div>
  );
}
