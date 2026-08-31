"use client";

import { useState, useEffect } from "react";
import { UserCheck, ShieldCheck, Bell, Bot, Sparkles } from "lucide-react";
import { CopilotDrawer } from "@/components/CopilotDrawer";

export function Header() {
  const [role, setRole] = useState("MANAGER");
  const [isCopilotOpen, setIsCopilotOpen] = useState(false);
  const [unreadCount, setUnreadCount] = useState(2);

  useEffect(() => {
    const savedRole = localStorage.getItem("pharmashield_role") || "MANAGER";
    setRole(savedRole);
  }, []);

  const handleRoleChange = (newRole: string) => {
    setRole(newRole);
    localStorage.setItem("pharmashield_role", newRole);
    window.dispatchEvent(new Event("pharmashield_role_change"));
  };

  return (
    <>
      <header className="h-16 border-b border-cardBorder bg-cardBg/90 backdrop-blur px-6 flex items-center justify-between sticky top-0 z-20">
        {/* Title / Breadcrumb */}
        <div className="flex items-center gap-3">
          <h2 className="text-sm font-semibold text-gray-200">Supply Chain Command & Control Tower</h2>
          <span className="text-xs bg-blueAccent/10 text-blueAccent px-2.5 py-1 rounded-full font-medium border border-blueAccent/20">
            Delhi → Chandigarh Corridor
          </span>
        </div>

        {/* Right Controls: Copilot, Notifications & User Profile */}
        <div className="flex items-center gap-3">
          {/* Resilience Copilot Trigger Button */}
          <button
            onClick={() => setIsCopilotOpen(true)}
            className="px-3 py-1.5 rounded-lg bg-cyanAccent/10 text-cyanAccent border border-cyanAccent/30 hover:bg-cyanAccent/20 transition text-xs font-bold flex items-center gap-1.5"
          >
            <Bot className="w-4 h-4" />
            <span>Copilot</span>
            <Sparkles className="w-3 h-3 text-cyanAccent" />
          </button>

          {/* Notifications Icon */}
          <div className="relative p-2 rounded-lg bg-white/5 text-gray-400 hover:text-white cursor-pointer transition">
            <Bell className="w-4 h-4" />
            {unreadCount > 0 && (
              <span className="absolute top-1 right-1 w-4 h-4 rounded-full bg-roseCritical text-[10px] font-bold text-white flex items-center justify-center">
                {unreadCount}
              </span>
            )}
          </div>

          {/* Role Selector Guard Visualizer */}
          <div className="flex items-center gap-2 bg-darkBg/80 p-1.5 rounded-lg border border-cardBorder">
            <UserCheck className="w-4 h-4 text-cyanAccent ml-1" />
            <span className="text-xs text-gray-400 font-medium hidden sm:inline">Active Role:</span>
            <select
              value={role}
              onChange={(e) => handleRoleChange(e.target.value)}
              className="bg-cardBg text-xs font-semibold text-white px-2.5 py-1 rounded border border-cardBorder focus:outline-none focus:border-cyanAccent"
            >
              <option value="OPERATOR">OPERATOR (View & Trigger)</option>
              <option value="MANAGER">MANAGER (Can Approve)</option>
              <option value="AUDITOR">AUDITOR (Read Only Audit)</option>
              <option value="ADMIN">ADMIN (Full Control)</option>
            </select>
          </div>

          {/* User Badge */}
          <div className="flex items-center gap-2 pl-2 border-l border-cardBorder">
            <div className="w-8 h-8 rounded-full bg-cyanAccent/20 text-cyanAccent flex items-center justify-center font-bold text-xs border border-cyanAccent/40">
              SC
            </div>
            <div className="hidden md:block text-left text-xs">
              <p className="font-semibold text-white leading-none">Sarah Connor</p>
              <p className="text-[10px] text-gray-400">Cold Chain Lead</p>
            </div>
          </div>
        </div>
      </header>

      {/* Slide-out Copilot Drawer */}
      <CopilotDrawer isOpen={isCopilotOpen} onClose={() => setIsCopilotOpen(false)} />
    </>
  );
}
