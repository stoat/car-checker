import type { Valuation } from "@/types/report";
import { PoundSterling } from "lucide-react";

function ValRow({ label, value }: { label: string; value?: number }) {
  if (value == null) return null;
  return (
    <div className="flex justify-between items-center py-2 border-b border-gray-100 last:border-0">
      <span className="text-sm text-gray-600">{label}</span>
      <span className="font-bold text-lg">£{value.toLocaleString()}</span>
    </div>
  );
}

export function ValuationPanel({ valuation }: { valuation: Valuation }) {
  const hasAny = valuation.webuyanycar || valuation.parkers_retail || valuation.parkers_private;

  return (
    <div className="bg-white rounded-2xl border border-gray-200 p-6">
      <h3 className="font-bold text-lg mb-4 flex items-center gap-2">
        <PoundSterling size={18} />
        Valuations
      </h3>

      {hasAny ? (
        <div>
          <ValRow label="WeBuyAnyCar (instant trade)" value={valuation.webuyanycar} />
          <ValRow label="Parkers retail estimate" value={valuation.parkers_retail} />
          <ValRow label="Parkers private estimate" value={valuation.parkers_private} />
        </div>
      ) : (
        <p className="text-sm text-gray-500">{valuation.source_note ?? "No valuation data available."}</p>
      )}

      {hasAny && valuation.source_note && (
        <p className="text-xs text-gray-400 mt-3">{valuation.source_note}</p>
      )}
    </div>
  );
}
