/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        darkBg: "#0B0F19",
        cardBg: "#111827",
        cardBorder: "#1F2937",
        cyanAccent: "#06B6D4",
        blueAccent: "#3B82F6",
        emeraldSuccess: "#10B981",
        amberWarning: "#F59E0B",
        roseCritical: "#EF4444",
      },
    },
  },
  plugins: [],
}
