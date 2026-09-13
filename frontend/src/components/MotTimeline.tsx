import type { MotTest, MotDefect } from "@/types/report";
import { CheckCircle, XCircle, ChevronDown, ChevronUp } from "lucide-react";
import { useState } from "react";
import { clsx } from "clsx";

function DefectTag({ defect }: { defect: MotDefect }) {
  const styles: Record<string, string> = {
    FAIL:  "bg-red-100 text-red-800 border-red-200",
    MAJOR: "bg-red-100 text-red-800 border-red-200",
    MINOR: "bg-orange-100 text-orange-800 border-orange-200",
    ADVISORY: "bg-yellow-100 text-yellow-800 border-yellow-200",
    "USER ENTERED": "bg-gray-100 text-gray-700 border-gray-200",
  };
  const label = defect.type.toUpperCase();
  return (
    <div className={clsx("rounded border px-2 py-1 text-xs flex gap-2 items-start", styles[label] ?? styles.ADVISORY)}>
      <span className="font-semibold shrink-0">{label}</span>
      <span>{defect.text}</span>
    </div>
  );
}

function MotCard({ test }: { test: MotTest }) {
  const [open, setOpen] = useState(false);
  const passed = test.test_result === "PASSED";
  const failCount = test.defects.filter(d => ["FAIL", "MAJOR"].includes(d.type.toUpperCase())).length;
  const advisoryCount = test.defects.filter(d => ["ADVISORY", "MINOR"].includes(d.type.toUpperCase())).length;

  return (
    <div className={clsx(
      "rounded-xl border-l-4 bg-white border border-gray-200 overflow-hidden",
      passed ? "border-l-green-500" : "border-l-red-500"
    )}>
      <button
        onClick={() => setOpen(o => !o)}
        className="w-full flex items-center gap-3 px-4 py-3 text-left hover:bg-gray-50"
      >
        {passed
          ? <CheckCircle size={18} className="text-green-500 shrink-0" />
          : <XCircle size={18} className="text-red-500 shrink-0" />
        }
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <span className="font-semibold text-sm">
              {test.completed_date.slice(0, 10)}
            </span>
            <span className={clsx(
              "text-xs font-medium px-2 py-0.5 rounded-full",
              passed ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"
            )}>
              {passed ? "PASS" : "FAIL"}
            </span>
          </div>
          <div className="text-xs text-gray-500 mt-0.5 flex gap-3">
            {test.odometer_value != null && (
              <span>{test.odometer_value.toLocaleString()} {test.odometer_unit ?? "mi"}</span>
            )}
            {failCount > 0 && <span className="text-red-600">{failCount} failure{failCount > 1 ? "s" : ""}</span>}
            {advisoryCount > 0 && <span className="text-yellow-600">{advisoryCount} advisor{advisoryCount > 1 ? "ies" : "y"}</span>}
          </div>
        </div>
        {test.defects.length > 0 && (
          open ? <ChevronUp size={16} className="text-gray-400 shrink-0" />
               : <ChevronDown size={16} className="text-gray-400 shrink-0" />
        )}
      </button>

      {open && test.defects.length > 0 && (
        <div className="px-4 pb-4 space-y-1.5 border-t border-gray-100 pt-3">
          {test.defects.map((d, i) => <DefectTag key={i} defect={d} />)}
        </div>
      )}
    </div>
  );
}

export function MotTimeline({ tests }: { tests: MotTest[] }) {
  if (!tests.length) {
    return (
      <div className="bg-white rounded-2xl border border-gray-200 p-6">
        <h3 className="font-bold text-lg mb-2">MOT History</h3>
        <p className="text-gray-500 text-sm">No MOT records found.</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-2xl border border-gray-200 p-6">
      <h3 className="font-bold text-lg mb-4">MOT History ({tests.length} tests)</h3>
      <div className="space-y-2">
        {tests.map((test, i) => <MotCard key={i} test={test} />)}
      </div>
    </div>
  );
}
