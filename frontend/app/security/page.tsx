"use client";

import { useEffect, useState } from "react";
import { Lock, ShieldCheck, CheckCircle2, AlertTriangle, Key, Cpu } from "lucide-react";

export default function SecurityPage() {
  const [sec, setSec] = useState<any>(null);

  useEffect(() => {
    fetch("http://localhost:8000/api/security/status")
      .then(res => res.json())
      .then(setSec)
      .catch(console.error);
  }, []);

  if (!sec) return <div className="p-8 text-center text-gray-400">Loading security center...</div>;

  return (
    <div className="space-y-6">
      {/* Title */}
      <div className="flex items-center justify-between pb-4 border-b border-cardBorder">
        <div>
          <h1 className="text-xl font-bold text-white flex items-center gap-2">
            <Lock className="w-5 h-5 text-cyanAccent" />
            Security & Governance Guardrails Center
          </h1>
          <p className="text-xs text-gray-400">
            Authentication, Role-Based Access Controls (RBAC), Audit Chain Cryptography & AI Safety Guards
          </p>
        </div>
        <span className="text-xs bg-emeraldSuccess/20 text-emeraldSuccess font-bold px-3 py-1 rounded border border-emeraldSuccess/30">
          SECURITY GUARDRAILS ACTIVE
        </span>
      </div>

      {/* Security Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Authentication & Authorization */}
        <div className="bg-cardBg border border-cardBorder p-5 rounded-xl space-y-4">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Key className="w-4 h-4 text-cyanAccent" />
            Authentication & Server RBAC
          </h3>
          <div className="space-y-2 text-xs text-gray-300">
            <div className="flex items-center justify-between p-2.5 rounded bg-white/5 border border-cardBorder">
              <span>Token Architecture</span>
              <strong className="text-white font-mono">{sec.authentication.token_type}</strong>
            </div>
            <div className="flex items-center justify-between p-2.5 rounded bg-white/5 border border-cardBorder">
              <span>Manager Approval Security Guard</span>
              <strong className="text-emeraldSuccess font-semibold">{sec.rbac_authorization.manager_approval_guard}</strong>
            </div>
            <div className="flex items-center justify-between p-2.5 rounded bg-white/5 border border-cardBorder">
              <span>Supported Roles</span>
              <strong className="text-cyanAccent font-mono">{sec.rbac_authorization.roles.join(", ")}</strong>
            </div>
          </div>
        </div>

        {/* Cryptographic Audit Chain */}
        <div className="bg-cardBg border border-cardBorder p-5 rounded-xl space-y-4">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-emeraldSuccess" />
            Cryptographic Audit Chain Integrity
          </h3>
          <div className="space-y-2 text-xs text-gray-300">
            <div className="flex items-center justify-between p-2.5 rounded bg-white/5 border border-cardBorder">
              <span>Hash Chaining Engine</span>
              <strong className="text-white font-mono">{sec.audit_integrity.hash_algorithm}</strong>
            </div>
            <div className="flex items-center justify-between p-2.5 rounded bg-emeraldSuccess/10 border border-emeraldSuccess/30 text-emeraldSuccess">
              <span>Audit Chain Integrity Status</span>
              <strong className="font-mono text-sm">{sec.audit_integrity.status}</strong>
            </div>
            <div className="flex items-center justify-between p-2.5 rounded bg-white/5 border border-cardBorder">
              <span>Historical Records Verified</span>
              <strong className="text-cyanAccent font-mono">{sec.audit_integrity.records_verified} blocks</strong>
            </div>
          </div>
        </div>

        {/* AI Safety Rules */}
        <div className="bg-cardBg border border-cardBorder p-5 rounded-xl space-y-4 md:col-span-2">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Cpu className="w-4 h-4 text-amberWarning" />
            Deterministic AI Safety & Governance Constraints
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div className="p-3.5 rounded-lg bg-white/5 border border-cardBorder space-y-1">
              <span className="text-gray-400">Autonomous AI Approval</span>
              <p className="text-roseCritical font-bold">PROHIBITED (Strict Human Sign-off)</p>
            </div>
            <div className="p-3.5 rounded-lg bg-white/5 border border-cardBorder space-y-1">
              <span className="text-gray-400">Governance Bypass</span>
              <p className="text-roseCritical font-bold">PROHIBITED (ABAP Rules Mandatory)</p>
            </div>
            <div className="p-3.5 rounded-lg bg-white/5 border border-cardBorder space-y-1">
              <span className="text-gray-400">Safety Thresholds</span>
              <p className="text-emeraldSuccess font-bold">HARDCODED DETERMINISTIC PYTHON</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
