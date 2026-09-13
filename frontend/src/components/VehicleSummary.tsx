import type { VehicleDetails } from "@/types/report";
import { clsx } from "clsx";

function Badge({ label, value, className }: { label: string; value?: string | number; className?: string }) {
  if (value == null) return null;
  return (
    <div className={clsx("rounded-lg px-3 py-2 text-center", className)}>
      <div className="text-xs text-gray-500 uppercase tracking-wide">{label}</div>
      <div className="font-semibold text-sm mt-0.5">{value}</div>
    </div>
  );
}

function StatusPill({ status }: { status?: string }) {
  if (!status) return null;
  const ok = status.toLowerCase().includes("valid") || status.toLowerCase().includes("taxed");
  return (
    <span className={clsx(
      "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium",
      ok ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"
    )}>
      {status}
    </span>
  );
}

export function VehicleSummary({ vehicle }: { vehicle: VehicleDetails }) {
  return (
    <div className="bg-white rounded-2xl border border-gray-200 p-6 space-y-4">
      <div className="flex items-start justify-between">
        <div>
          <h2 className="text-2xl font-black tracking-tight">
            {[vehicle.make, vehicle.model].filter(Boolean).join(" ") || "Unknown Vehicle"}
          </h2>
          <p className="text-gray-500 text-sm mt-1">
            {vehicle.year_of_manufacture} · {vehicle.colour} · {vehicle.fuel_type}
          </p>
        </div>
        {/* UK plate badge */}
        <div className="flex rounded-lg overflow-hidden border-2 border-gray-900 text-sm font-black shadow">
          <div className="bg-blue-700 text-white px-1.5 flex items-center text-xs">GB</div>
          <div className="bg-plate-yellow text-plate-black px-3 py-1 tracking-widest">
            {vehicle.registration}
          </div>
        </div>
      </div>

      <div className="flex flex-wrap gap-2">
        <StatusPill status={vehicle.mot_status} />
        <StatusPill status={vehicle.tax_status} />
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
        <Badge label="Engine" value={vehicle.engine_capacity ? `${vehicle.engine_capacity}cc` : undefined} className="bg-gray-50" />
        <Badge label="CO₂" value={vehicle.co2_emissions ? `${vehicle.co2_emissions} g/km` : undefined} className="bg-gray-50" />
        <Badge label="Last V5C" value={vehicle.date_of_last_v5c_issued?.slice(0, 10)} className="bg-gray-50" />
        <Badge label="Year" value={vehicle.year_of_manufacture} className="bg-gray-50" />
      </div>
    </div>
  );
}
