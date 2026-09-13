import type { Metadata } from "next";
import "./globals.css";
import { Providers } from "./providers";

export const metadata: Metadata = {
  title: "Car Checker",
  description: "UK vehicle provenance checker — MOT history, valuations, and recalls",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Providers>
          <header className="bg-white border-b border-gray-200 px-4 py-3">
            <div className="max-w-4xl mx-auto flex items-center gap-3">
              <span className="text-2xl font-black tracking-tight text-gray-900">Car Checker</span>
              <span className="text-sm text-gray-500">UK Vehicle Provenance</span>
            </div>
          </header>
          <main className="max-w-4xl mx-auto px-4 py-8">{children}</main>
        </Providers>
      </body>
    </html>
  );
}
