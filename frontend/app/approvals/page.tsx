"use client";

import { useEffect, useState } from "react";
import { 
  CheckCircle2, 
  XCircle, 
  ShieldCheck, 
  AlertTriangle, 
  Clock, 
  DollarSign, 
  TrendingDown,
  Lock,
  UserCheck
} from "lucide-react";
import { api } from "@/lib/api";
import { useAppContext } from "@/components/AppProviders";

export default function ApprovalsPage() {
  const [approvals, setApprovals] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionMessage, setActionMessage] = useState<string | null>(null);
  const { role: activeRole, permissions } = useAppContext();

  const loadData = async () => {
    try {
      const pending = await api.getPendingApprovals();
      setApprovals(pending);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleApprove = async (approvalId: string, shipmentId: string) => {
    if (!permissions.canApprove) {
      alert(`FORBIDDEN: Approval requires role 'MANAGER' or 'ADMIN'. Your current role is '${activeRole}'.`);
      return;
    }

    try {
      await api.approveAction(approvalId, "Approved cold storage rerouting by Cold Chain Manager.");
      await api.executeRecovery(shipmentId);
      setActionMessage(`Successfully APPROVED & EXECUTED recovery for shipment ${shipmentId}!`);
      loadData();
    } catch (err: any) {
      alert(`Approval Error: ${err.message}`);
    }
  };

  const handleReject = async (approvalId: string) => {
    if (!permissions.canApprove) {
      alert(`FORBIDDEN: Rejection requires role 'MANAGER' or 'ADMIN'. Your current role is '${activeRole}'.`);
      return;
    }

    try {
      await api.rejectAction(approvalId, "Rejected by Manager.");
      setActionMessage(`Rejected approval ${approvalId}.`);
      loadData();
    } catch (err: any) {
      alert(`Rejection Error: ${err.message}`);
    }
  };

  const canApprove = permissions.canApprove;

  return (
    <div className="space-y-6">
      {/* Title */}
      <div className="flex items-center justify-between pb-4 border-b border-cardBorder">
        <div>
          <h1 className="text-xl font-bold text-white flex items-center gap-2">
            <CheckCircle2 className="w-5 h-5 text-cyanAccent" />
            Governance Approval Center
          </h1>
          <p className="text-xs text-gray-400">
            Human-in-the-Loop Sign-Off for High-Impact Cold Chain Recovery Actions
          </p>
        </div>

        {/* Role Guard Badge */}
        <div className="flex items-center gap-2 bg-cardBg border border-cardBorder px-3 py-1.5 rounded-lg text-xs">
          <UserCheck className="w-4 h-4 text-cyanAccent" />
          <span className="text-gray-400">Logged in as:</span>
          <span className={`font-bold ${canApprove ? "text-emeraldSuccess" : "text-amberWarning"}`}>
            {activeRole}
          </span>
          {!canApprove && (
            <span className="text-[10px] bg-roseCritical/20 text-roseCritical px-2 py-0.5 rounded font-bold flex items-center gap-1">
              <Lock className="w-3 h-3" /> Read Only
            </span>
          )}
        </div>
      </div>

      {actionMessage && (
        <div className="p-4 rounded-xl bg-emeraldSuccess/10 border border-emeraldSuccess/30 text-emeraldSuccess text-xs font-semibold flex items-center justify-between">
          <span>{actionMessage}</span>
          <button onClick={() => setActionMessage(null)} className="text-xs underline">Dismiss</button>
        </div>
      )}

      {/* Pending Approvals List */}
      {approvals.length === 0 ? (
        <div className="bg-cardBg border border-cardBorder rounded-xl p-12 text-center space-y-3">
          <ShieldCheck className="w-12 h-12 text-cyanAccent mx-auto opacity-80" />
          <h3 className="text-base font-bold text-white">No Pending Approval Requests</h3>
          <p className="text-xs text-gray-400 max-w-md mx-auto">
            All high-impact cold chain actions have been evaluated and resolved. Click "Simulate Temperature Excursion" on the dashboard to trigger a new demo request.
          </p>
        </div>
      ) : (
        <div className="space-y-6">
          {approvals.map((app) => (
            <div key={app.id} className="bg-cardBg border-2 border-amberWarning/40 rounded-xl p-6 space-y-6 shadow-xl relative">
              {/* Top Banner */}
              <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-cardBorder">
                <div className="flex items-center gap-3">
                  <span className="text-xs bg-amberWarning/20 text-amberWarning px-3 py-1 rounded-full font-bold border border-amberWarning/30">
                    PENDING APPROVAL
                  </span>
                  <h2 className="text-lg font-bold text-white font-mono">{app.shipment_id}</h2>
                  <span className="text-xs text-gray-400 font-medium">Product: Vaccine (High Criticality)</span>
                </div>
                <span className="text-xs font-mono text-gray-400">Request ID: {app.id}</span>
              </div>

              {/* Metrics Grid */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                <div className="bg-white/5 p-3.5 rounded-lg border border-cardBorder space-y-1">
                  <span className="text-[11px] text-gray-400 font-semibold">Excursion Temp</span>
                  <p className="text-xl font-bold font-mono text-roseCritical">9.6°C</p>
                  <span className="text-[10px] text-gray-400">Safe: 2°C–8°C</span>
                </div>

                <div className="bg-white/5 p-3.5 rounded-lg border border-cardBorder space-y-1">
                  <span className="text-[11px] text-gray-400 font-semibold">Risk Score</span>
                  <p className="text-xl font-bold font-mono text-roseCritical">91 / 100</p>
                  <span className="text-[10px] text-roseCritical font-semibold">CRITICAL</span>
                </div>

                <div className="bg-white/5 p-3.5 rounded-lg border border-cardBorder space-y-1">
                  <span className="text-[11px] text-gray-400 font-semibold">Estimated Cost</span>
                  <p className="text-xl font-bold font-mono text-cyanAccent">₹2,400</p>
                  <span className="text-[10px] text-gray-400">Cold Storage Transfer</span>
                </div>

                <div className="bg-white/5 p-3.5 rounded-lg border border-cardBorder space-y-1">
                  <span className="text-[11px] text-gray-400 font-semibold">Reroute ETA</span>
                  <p className="text-xl font-bold font-mono text-emeraldSuccess">23 mins</p>
                  <span className="text-[10px] text-gray-400">Nearest Storage 8.4 km</span>
                </div>
              </div>

              {/* AI Recommendation Reasoning */}
              <div className="bg-cyanAccent/10 border border-cyanAccent/30 p-4 rounded-xl space-y-2">
                <div className="flex items-center justify-between text-xs font-bold text-cyanAccent">
                  <span>AI Recommended Action: REROUTE_TO_COLD_STORAGE</span>
                  <span>Confidence: 94%</span>
                </div>
                <p className="text-xs text-gray-200 leading-relaxed">
                  "The temperature excursion for Vaccine has reached 9.6°C (exceeding safe limit 8.0°C). Given heavy traffic and a 47-minute delay, continuing the current route presents an unacceptable spoilage risk. Rerouting to nearest cold storage facility minimizes exposure while maintaining reasonable recovery cost."
                </p>
              </div>

              {/* SAP Governance Rule Evaluation Box */}
              <div className="bg-white/5 p-4 rounded-xl border border-cardBorder text-xs space-y-1.5">
                <p className="font-bold text-white">SAP ABAP Governance Rule Evaluation:</p>
                <ul className="list-disc list-inside text-gray-400 space-y-1">
                  <li><strong className="text-gray-200">Rule 3 Applied:</strong> Product Criticality HIGH & Action Cost (₹2,400) &gt; Threshold (₹1,000) &rarr; Human Approval Mandatory.</li>
                  <li><strong className="text-gray-200">Rule 4 Applied:</strong> Action 'REROUTE_TO_COLD_STORAGE' is high-impact &rarr; Autonomous Execution Prohibited.</li>
                </ul>
              </div>

              {/* Action Buttons */}
              <div className="flex items-center justify-end gap-3 pt-2">
                <button
                  onClick={() => handleReject(app.id)}
                  disabled={!canApprove}
                  title={!canApprove ? "Manager or Admin approval permission required" : undefined}
                  className={`px-5 py-2.5 rounded-lg text-xs font-bold transition flex items-center gap-2 ${canApprove ? "bg-white/5 hover:bg-white/10 text-gray-300 border border-white/10" : "bg-gray-800 text-gray-500 cursor-not-allowed border border-gray-700"}`}
                >
                  <XCircle className="w-4 h-4 text-roseCritical" />
                  REJECT
                </button>

                <button
                  onClick={() => handleApprove(app.id, app.shipment_id)}
                  disabled={!canApprove}
                  title={!canApprove ? "Manager or Admin approval permission required" : undefined}
                  className={`px-6 py-2.5 rounded-lg text-xs font-bold transition flex items-center gap-2 shadow-lg ${
                    canApprove
                      ? "bg-emeraldSuccess hover:bg-emeraldSuccess/90 text-darkBg shadow-emeraldSuccess/20"
                      : "bg-gray-800 text-gray-500 cursor-not-allowed border border-gray-700"
                  }`}
                >
                  <CheckCircle2 className="w-4 h-4" />
                  APPROVE RECOVERY ACTION
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
