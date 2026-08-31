"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  ShieldAlert, 
  LayoutDashboard, 
  Truck, 
  GitMerge, 
  CheckCircle2, 
  FileText,
  AlertTriangle,
  Sliders,
  BarChart3,
  Crown,
  Lock,
  Activity
} from "lucide-react";

export function Sidebar() {
  const pathname = usePathname();

  const primaryNav = [
    { name: "Control Tower", href: "/dashboard", icon: LayoutDashboard },
    { name: "Shipment PS-1026", href: "/shipments/PS-1026", icon: Truck },
    { name: "Incident Center", href: "/incidents", icon: AlertTriangle },
    { name: "AI Decision Center", href: "/decisions", icon: GitMerge },
    { name: "Approval Center", href: "/approvals", icon: CheckCircle2 },
    { name: "Audit Ledger", href: "/audit", icon: FileText },
  ];

  const enterpriseNav = [
    { name: "What-If Simulator", href: "/simulations", icon: Sliders },
    { name: "Fleet Analytics", href: "/analytics", icon: BarChart3 },
    { name: "Executive Tower", href: "/executive", icon: Crown },
    { name: "Security & Guards", href: "/security", icon: Lock },
    { name: "System Health", href: "/system-health", icon: Activity },
  ];

  return (
    <aside className="w-64 bg-cardBg border-r border-cardBorder flex flex-col h-screen sticky top-0 z-30">
      {/* Brand Header */}
      <div className="p-5 border-b border-cardBorder flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyanAccent to-blueAccent flex items-center justify-center shadow-lg shadow-cyanAccent/20">
          <ShieldAlert className="w-6 h-6 text-darkBg stroke-[2.5]" />
        </div>
        <div>
          <h1 className="font-bold text-lg tracking-wide text-white flex items-center gap-1.5">
            Pharma<span className="text-cyanAccent">Shield</span>
          </h1>
          <p className="text-xs text-gray-400 font-medium">Enterprise Cold Chain</p>
        </div>
      </div>

      {/* Main Nav Links */}
      <nav className="flex-1 p-4 space-y-4 overflow-y-auto">
        <div className="space-y-1">
          <div className="px-3 py-1 text-[10px] font-semibold text-gray-400 uppercase tracking-wider">
            Operations & Control
          </div>
          {primaryNav.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href || (item.href !== "/dashboard" && pathname.startsWith(item.href));
            return (
              <Link
                key={item.name}
                href={item.href}
                className={`flex items-center gap-3 px-3.5 py-2 rounded-lg text-xs font-medium transition-all ${
                  isActive
                    ? "bg-cyanAccent/10 text-cyanAccent border border-cyanAccent/30 font-bold shadow-sm"
                    : "text-gray-400 hover:text-gray-200 hover:bg-white/5"
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? "text-cyanAccent" : "text-gray-400"}`} />
                {item.name}
              </Link>
            );
          })}
        </div>

        <div className="space-y-1 pt-2 border-t border-cardBorder">
          <div className="px-3 py-1 text-[10px] font-semibold text-gray-400 uppercase tracking-wider">
            Enterprise & Intelligence
          </div>
          {enterpriseNav.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.name}
                href={item.href}
                className={`flex items-center gap-3 px-3.5 py-2 rounded-lg text-xs font-medium transition-all ${
                  isActive
                    ? "bg-cyanAccent/10 text-cyanAccent border border-cyanAccent/30 font-bold shadow-sm"
                    : "text-gray-400 hover:text-gray-200 hover:bg-white/5"
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? "text-cyanAccent" : "text-gray-400"}`} />
                {item.name}
              </Link>
            );
          })}
        </div>
      </nav>

      {/* SAP Governance Badge */}
      <div className="p-3 m-3 rounded-xl bg-cardBorder/60 border border-white/5 space-y-1.5">
        <div className="flex items-center justify-between text-xs">
          <span className="text-gray-400 font-medium">SAP Governance</span>
          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amberWarning/20 text-amberWarning border border-amberWarning/30">
            DEMO MOCK
          </span>
        </div>
        <p className="text-[10px] text-gray-400 leading-tight">
          ABAP Rules 1–5 Active. Human approval enforced for critical actions.
        </p>
      </div>

      {/* System Status Footer */}
      <div className="p-3.5 border-t border-cardBorder text-xs text-gray-400 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-emeraldSuccess animate-pulse"></span>
          <span className="text-[11px]">System Healthy</span>
        </div>
        <span className="text-[10px] bg-white/5 px-2 py-0.5 rounded text-gray-400">v2.0 Enterprise</span>
      </div>
    </aside>
  );
}
