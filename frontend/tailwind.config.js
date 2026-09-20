/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#0b0f17",
        foreground: "#f8fafc",
        card: "#111827",
        border: "#1e293b",
        primary: {
          DEFAULT: "#0284c7",
          foreground: "#ffffff"
        },
        supported: {
          DEFAULT: "#10b981",
          bg: "#064e3b"
        },
        contradicted: {
          DEFAULT: "#ef4444",
          bg: "#7f1d1d"
        },
        partial: {
          DEFAULT: "#f59e0b",
          bg: "#78350f"
        },
        unresolved: {
          DEFAULT: "#6366f1",
          bg: "#312e81"
        }
      }
    },
  },
  plugins: [],
};
