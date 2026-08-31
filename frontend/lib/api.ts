const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api";

export async function fetchApi(endpoint: string, options: RequestInit = {}) {
  const token = typeof window !== "undefined" ? localStorage.getItem("pharmashield_token") : null;
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: "Network request failed" }));
    throw new Error(errorData.detail || "API Request Failed");
  }

  return res.json();
}

export const api = {
  getShipments: () => fetchApi("/shipments"),
  getShipment: (id: string) => fetchApi(`/shipments/${id}`),
  getSensorReadings: (id: string) => fetchApi(`/shipments/${id}/readings`),
  
  // Agent & Governance
  triggerDetect: (id: string) => fetchApi(`/agents/detect?shipment_id=${id}`, { method: "POST" }),
  triggerPlan: (id: string) => fetchApi(`/agents/plan?shipment_id=${id}`, { method: "POST" }),
  validateSAP: (id: string) => fetchApi(`/governance/validate?shipment_id=${id}`, { method: "POST" }),
  
  // Approvals & Execution
  getPendingApprovals: () => fetchApi("/approvals/pending"),
  approveAction: (id: string, comments: string = "") => 
    fetchApi(`/approvals/${id}/approve`, { method: "POST", body: JSON.stringify({ comments }) }),
  rejectAction: (id: string, comments: string = "") => 
    fetchApi(`/approvals/${id}/reject`, { method: "POST", body: JSON.stringify({ comments }) }),
  executeRecovery: (shipmentId: string) => fetchApi(`/execution/${shipmentId}`, { method: "POST" }),

  // Audit
  getAuditLogs: (shipmentId?: string) => 
    fetchApi(shipmentId ? `/audit?shipment_id=${shipmentId}` : "/audit"),

  // Simulation & Demo
  startSimulation: (id: string = "PS-1026") => fetchApi(`/simulation/start?shipment_id=${id}`, { method: "POST" }),
  triggerExcursion: (id: string = "PS-1026") => fetchApi(`/simulation/temperature-excursion?shipment_id=${id}`, { method: "POST" }),
  resetSimulation: (id: string = "PS-1026") => fetchApi(`/simulation/reset?shipment_id=${id}`, { method: "POST" }),
  runVaccineDemo: () => fetchApi("/demo/run-vaccine-excursion", { method: "POST" }),
  resetDemo: () => fetchApi("/demo/reset", { method: "POST" }),
};
