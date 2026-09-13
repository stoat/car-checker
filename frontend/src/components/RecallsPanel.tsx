import type { Recall } from "@/types/report";
import { AlertTriangle } from "lucide-react";

export function RecallsPanel({ recalls }: { recalls: Recall[] }) {
  if (!recalls.length) return null;

  return (
    <div className="bg-red-50 border border-red-200 rounded-2xl p-6">
      <h3 className="font-bold text-red-800 text-lg mb-4 flex items-center gap-2">
        <AlertTriangle size={18} />
        Outstanding Safety Recalls ({recalls.length})
      </h3>
      <div className="space-y-4">
        {recalls.map((recall, i) => (
          <div key={i} className="bg-white rounded-xl p-4 border border-red-100 space-y-1">
            {recall.concern && (
              <div>
                <span className="text-xs font-semibold text-red-600 uppercase tracking-wide">Concern</span>
                <p className="text-sm text-gray-700 mt-0.5">{recall.concern}</p>
              </div>
            )}
            {recall.remedy && (
              <div className="mt-2">
                <span className="text-xs font-semibold text-gray-500 uppercase tracking-wide">Remedy</span>
                <p className="text-sm text-gray-600 mt-0.5">{recall.remedy}</p>
              </div>
            )}
            {recall.launch_date && (
              <p className="text-xs text-gray-400 mt-1">Issued: {recall.launch_date}</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
