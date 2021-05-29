import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      "^/reports/.*": {
        target: "http://127.0.0.1:8000/dl_report",
      },
    },
  },
});
