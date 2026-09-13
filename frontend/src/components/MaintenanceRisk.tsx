import type { RiskAnalysis, MileageConsistency } from "@/types/report";
import { AlertTriangle, CheckCircle, XCircle, TrendingDown } from "lucide-react";
import { clsx } from "clsx";

const CATEGORY_LABELS: Record<string, string> = {
  tyres: "Tyres",
  brakes: "Brakes",
  rust_corrosion: "Rust & Corrosion",
  suspension: "Suspension",
  lights: "Lights",
  emissions: "Emissions",
  structural: "Structural",
  other: "Other",
};

const RISK_STYLES = {
  low: { bg: "bg-green-50", border: "border-green-200", text: "text-green-700", label: "Low Risk" },
  medium: { bg: "bg-yellow-50", border: "border-yellow-200", text: "text-yellow-700", label: "Medium Risk" },
  high: { bg: "bg-red-50", border: "border-red-200", text: "text-red-700", label: "High Risk" },
};

export function MaintenanceRisk({
  risk,
  mileage,
}: {
  risk: RiskAnalysis;
  mileage?: MileageConsistency;
}) {
  const style = RISK_STYLES[risk.overall_risk];
  const flags = risk.flags as Record<string, { text: string; type: string; date: string }[]>;

  const categories = Object.entries(CATEGORY_LABELS).filter(
    ([key]) => (flags[key]?.length ?? 0) > 0
  );

  return (
    <div className="space-y-4">
      {/* Overall risk banner */}
      <div className={clsx("rounded-2xl border p-5 flex items-center gap-4", style.bg, style.border)}>
        {risk.overall_risk === "low"
          ? <CheckCircle size={28} className="text-green-500 shrink-0" />
          : risk.overall_risk === "medium"
          ? <AlertTriangle size={28} className="text-yellow-500 shrink-0" />
          : <XCircle size={28} className="text-red-500 shrink-0" />
        }
        <div>
          <div className={clsx("font-bold text-lg", style.text)}>{style.label}</div>
          <div className="text-sm text-gray-600">
            {risk.fail_count} failure{risk.fail_count !== 1 ? "s" : ""} &middot;{" "}
            {risk.advisory_count} advisor{risk.advisory_count !== 1 ? "ies" : "y"} across all MOT tests
          </div>
        </div>
      </div>

      {/* Category breakdown */}
      {categories.length > 0 && (
        <div className="bg-white rounded-2xl border border-gray-200 p-6">
          <h3 className="font-bold text-lg mb-4">Maintenance Concerns</h3>
          <div className="space-y-4">
            {categories.map(([key, label]) => {
              const items = flags[key] ?? [];
              return (
                <div key={key}>
                  <div className="flex items-center gap-2 mb-1.5">
                    <span className="font-semibold text-sm">{label}</span>
                    <span className="text-xs bg-gray-100 text-gray-600 rounded-full px-2 py-0.5">
                      {items.length}
                    </span>
                  </div>
                  <div className="space-y-1 pl-2 border-l-2 border-gray-100">
                    {items.map((flag, i) => (
                      <div key={i} className="text-xs text-gray-600 flex gap-2">
                        <span className="text-gray-400 shrink-0">{flag.date}</span>
                        <span className={clsx(
                          "font-medium shrink-0",
                          ["FAIL", "MAJOR"].includes(flag.type) ? "text-red-600" : "text-yellow-600"
                        )}>
                          {flag.type}
                        </span>
                        <span>{flag.text}</span>
                      </div>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Recurring issues */}
      {risk.recurring_issues.length > 0 && (
        <div className="bg-orange-50 border border-orange-200 rounded-2xl p-5">
          <h3 className="font-bold text-orange-800 mb-3 flex items-center gap-2">
            <AlertTriangle size={16} />
            Recurring Issues
          </h3>
          <ul className="space-y-1.5">
            {risk.recurring_issues.map((issue, i) => (
              <li key={i} className="text-sm text-orange-700">{issue}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Mileage consistency */}
      {mileage && (
        <div className={clsx(
          "rounded-2xl border p-5",
          mileage.consistent ? "bg-white border-gray-200" : "bg-red-50 border-red-200"
        )}>
          <h3 className="font-bold mb-3 flex items-center gap-2">
            <TrendingDown size={16} />
            Mileage Consistency
          </h3>
          {mileage.consistent ? (
            <p className="text-sm text-green-700 flex items-center gap-1">
              <CheckCircle size={14} /> Odometer readings are consistent across all MOT tests.
            </p>
          ) : (
            <div className="space-y-1.5">
              {mileage.anomalies.map((a, i) => (
                <p key={i} className="text-sm text-red-700">{a}</p>
              ))}
            </div>
          )}
          {mileage.values.length > 0 && (
            <div className="mt-3 grid grid-cols-2 sm:grid-cols-3 gap-2">
              {mileage.values.map((pt, i) => (
                <div key={i} className="bg-gray-50 rounded-lg px-3 py-2 text-center">
                  <div className="text-xs text-gray-500">{pt.date}</div>
                  <div className="font-semibold text-sm">{pt.value.toLocaleString()} {pt.unit}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
