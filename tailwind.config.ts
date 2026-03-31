import type { Config } from "tailwindcss";

export default {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Palette personalizzata per il gioco Snake
        snake: {
          primary: "#00ff88",
          secondary: "#00cc6a",
          accent: "#7b61ff",
          danger: "#ff4757",
          warning: "#ffa502",
          success: "#2ed573",
          dark: {
            100: "#2f3542",
            200: "#1e272e",
            300: "#0d1117",
            400: "#010409",
          },
        },
      },
      animation: {
        "pulse-slow": "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "glow": "glow 2s ease-in-out infinite alternate",
        "slide-up": "slideUp 0.5s ease-out",
        "slide-down": "slideDown 0.5s ease-out",
        "fade-in": "fadeIn 0.3s ease-in",
        "bounce-slow": "bounce 2s infinite",
      },
      keyframes: {
        glow: {
          "0%": { boxShadow: "0 0 5px #00ff88, 0 0 10px #00ff88, 0 0 15px #00ff88" },
          "100%": { boxShadow: "0 0 10px #00ff88, 0 0 20px #00ff88, 0 0 30px #00ff88" },
        },
        slideUp: {
          "0%": { transform: "translateY(20px)", opacity: "0" },
          "100%": { transform: "translateY(0)", opacity: "1" },
        },
        slideDown: {
          "0%": { transform: "translateY(-20px)", opacity: "0" },
          "100%": { transform: "translateY(0)", opacity: "1" },
        },
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
      },
      fontFamily: {
        game: ["'Press Start 2P'", "cursive"],
        modern: ["'Inter'", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
} satisfies Config;
