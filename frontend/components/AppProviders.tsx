"use client";

import { createContext, useContext, useEffect, useMemo, useState } from "react";

export type Role = "OPERATOR" | "MANAGER" | "AUDITOR" | "ADMIN";

const ROLE_PERMISSIONS: Record<Role, { canApprove: boolean; canOperate: boolean; canManageSimulation: boolean }> = {
  OPERATOR: { canApprove: false, canOperate: true, canManageSimulation: false },
  MANAGER: { canApprove: true, canOperate: true, canManageSimulation: false },
  AUDITOR: { canApprove: false, canOperate: false, canManageSimulation: false },
  ADMIN: { canApprove: true, canOperate: true, canManageSimulation: true },
};

type AppContextValue = {
  role: Role;
  setRole: (role: Role) => void;
  permissions: (typeof ROLE_PERMISSIONS)[Role];
  selectedShipmentId: string;
  selectShipment: (shipmentId: string) => void;
};

const AppContext = createContext<AppContextValue | null>(null);

export function AppProviders({ children }: { children: React.ReactNode }) {
  const [role, setCurrentRole] = useState<Role>("ADMIN");
  const [selectedShipmentId, setSelectedShipmentId] = useState("PS-1026");

  useEffect(() => {
    const savedRole = localStorage.getItem("pharmashield_role") as Role | null;
    const savedShipment = localStorage.getItem("pharmashield_selected_shipment");
    if (savedRole && savedRole in ROLE_PERMISSIONS) setCurrentRole(savedRole);
    if (savedShipment) setSelectedShipmentId(savedShipment);
  }, []);

  const setRole = (nextRole: Role) => {
    setCurrentRole(nextRole);
    localStorage.setItem("pharmashield_role", nextRole);
  };

  const selectShipment = (shipmentId: string) => {
    setSelectedShipmentId(shipmentId);
    localStorage.setItem("pharmashield_selected_shipment", shipmentId);
  };

  const value = useMemo(() => ({
    role,
    setRole,
    permissions: ROLE_PERMISSIONS[role],
    selectedShipmentId,
    selectShipment,
  }), [role, selectedShipmentId]);

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

export function useAppContext() {
  const context = useContext(AppContext);
  if (!context) throw new Error("useAppContext must be used within AppProviders");
  return context;
}
