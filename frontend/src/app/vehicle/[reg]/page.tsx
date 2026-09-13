"use client";

import { use } from "react";
import { useQuery } from "@tanstack/react-query";
import { fetchVehicleReport } from "@/lib/api";
import { VehicleSummary } from "@/components/VehicleSummary";
import { MotTimeline } from "@/components/MotTimeline";
import { MaintenanceRisk } from "@/components/MaintenanceRisk";
import { ValuationPanel } from "@/components/ValuationPanel";
import { RecallsPanel } from "@/components/RecallsPanel";
import { ArrowLeft, Loader2, AlertTriangle } from "lucide-react";
import Link from "next/link";

export default function VehiclePage({ params }: { params: Promise<{ reg: string }> }) {
  const { reg } = use(params);
  const registration = reg.toUpperCase();

  const { data, isLoading, error } = useQuery({
    queryKey: ["vehicle", registration],
    queryFn: () => fetchVehicleReport(registration),
    retry: 1,
  });

  return (
    <div className="space-y-6">
      <Link href="/" className="inline-flex items-center gap-1.5 text-sm text-gray-500 hover:text-gray-900">
        <ArrowLeft size={14} />
        New search
      </Link>

      {isLoading && (
        <div className="flex flex-col items-center gap-4 py-20 text-gray-500">
          <Loader2 size={36} className="animate-spin" />
          <p className="text-sm">Fetching vehicle data&hellip;</p>
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-2xl p-6 flex gap-3 items-start">
          <AlertTriangle size={20} className="text-red-500 shrink-0 mt-0.5" />
          <div>
            <p className="font-semibold text-red-800">Could not load vehicle data</p>
            <p className="text-sm text-red-600 mt-1">{(error as Error).message}</p>
          </div>
        </div>
      )}

      {data && (
        <>
          {/* Mock data banner */}
          {data.errors._mock && (
            <div className="bg-blue-50 border border-blue-200 rounded-xl px-4 py-3 flex items-center gap-2">
              <span className="text-blue-700 font-semibold text-sm">DEV MODE</span>
              <span className="text-blue-600 text-sm">Showing sample data — add API keys to .env to use real data.</span>
            </div>
          )}

          {/* Partial-data warnings (excluding the mock flag) */}
          {Object.entries(data.errors).filter(([k]) => k !== "_mock").length > 0 && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-xl px-4 py-3">
              <p className="text-sm text-yellow-800 font-medium">
                Some data sources were unavailable:
              </p>
              <ul className="text-xs text-yellow-700 mt-1 list-disc list-inside">
                {Object.entries(data.errors).filter(([k]) => k !== "_mock").map(([src, msg]) => (
                  <li key={src}><strong>{src}</strong>: {msg}</li>
                ))}
              </ul>
            </div>
          )}

          {data.vehicle && <VehicleSummary vehicle={data.vehicle} />}

          {data.recalls.length > 0 && <RecallsPanel recalls={data.recalls} />}

          {data.risk_analysis && (
            <MaintenanceRisk risk={data.risk_analysis} mileage={data.mileage_consistency} />
          )}

          {data.valuation && <ValuationPanel valuation={data.valuation} />}

          <MotTimeline tests={data.mot_history} />
        </>
      )}
    </div>
  );
}
