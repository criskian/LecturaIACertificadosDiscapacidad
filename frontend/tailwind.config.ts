import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        canvas: "#f7f9f8",
        shell: "#fdfefd",
        ink: "#2d3440",
        line: "#d5e8e4",
        almia: {
          50: "#d8f4f1",
          100: "#b1e9e3",
          200: "#89ded4",
          300: "#62d3c6",
          400: "#3bc8b8",
          500: "#30af9f",
          700: "#1f746d",
          800: "#165753"
        },
        sage: {
          50: "#eef9f7",
          100: "#d8f4f1",
          500: "#3bc8b8",
          700: "#1f746d"
        },
        amber: {
          50: "#fbf1de",
          100: "#f5e5c5",
          500: "#c78925",
          700: "#8b5a13"
        },
        terracotta: {
          50: "#f8ecec",
          100: "#efd6d7",
          200: "#e2b4b7",
          500: "#c26b6f",
          700: "#88484b"
        },
        blue: {
          50: "#edf8f8",
          100: "#d8f4f1",
          500: "#3ba8b8",
          700: "#2d6574"
        }
      },
      boxShadow: {
        soft: "0 18px 40px rgba(36, 66, 70, 0.06)"
      },
      borderRadius: {
        "2xl": "1.5rem",
        "3xl": "1.9rem"
      },
      fontFamily: {
        sans: ["Manrope", "Segoe UI", "Helvetica Neue", "sans-serif"]
      }
    }
  },
  plugins: []
} satisfies Config;
