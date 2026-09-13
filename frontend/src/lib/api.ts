import type { VehicleReport } from "@/types/report";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function fetchVehicleReport(registration: string): Promise<VehicleReport> {
  const response = await fetch(`${API_BASE}/api/vehicles/${registration}`);
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail || `HTTP ${response.status}`);
  }
  return response.json();
}
