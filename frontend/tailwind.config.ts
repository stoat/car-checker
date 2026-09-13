import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        plate: {
          yellow: "#F5C518",
          black: "#1a1a1a",
        },
      },
    },
  },
  plugins: [],
};

export default config;
