"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Search } from "lucide-react";

export default function HomePage() {
  const router = useRouter();
  const [plate, setPlate] = useState("");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const reg = plate.trim().toUpperCase().replace(/\s+/g, "");
    if (reg) router.push(`/vehicle/${reg}`);
  }

  return (
    <div className="flex flex-col items-center gap-10 pt-16">
      <div className="text-center space-y-3">
        <h1 className="text-4xl font-black tracking-tight">Check Any UK Vehicle</h1>
        <p className="text-gray-500 text-lg max-w-md">
          MOT history, maintenance risk analysis, valuations, and outstanding recalls.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="w-full max-w-lg space-y-4">
        {/* UK number plate styled input */}
        <div className="flex rounded-xl overflow-hidden border-4 border-plate-black shadow-lg">
          <div className="bg-blue-700 w-10 flex items-center justify-center shrink-0">
            <span className="text-white text-xs font-bold rotate-0 writing-mode-vertical leading-none text-center">
              GB
            </span>
          </div>
          <input
            type="text"
            value={plate}
            onChange={(e) => setPlate(e.target.value.toUpperCase())}
            placeholder="AB12 CDE"
            maxLength={8}
            spellCheck={false}
            autoComplete="off"
            className="flex-1 bg-plate-yellow text-plate-black text-3xl font-black tracking-widest
                       text-center py-4 px-4 outline-none placeholder:text-yellow-700/40
                       uppercase"
          />
        </div>

        <button
          type="submit"
          disabled={!plate.trim()}
          className="w-full flex items-center justify-center gap-2 bg-gray-900 text-white
                     rounded-xl py-4 text-lg font-semibold hover:bg-gray-700 disabled:opacity-40
                     transition-colors"
        >
          <Search size={20} />
          Check Vehicle
        </button>
      </form>

      <p className="text-xs text-gray-400 text-center max-w-sm">
        Data sourced from DVLA, DVSA, and WeBuyAnyCar. For personal research use only.
      </p>
    </div>
  );
}
