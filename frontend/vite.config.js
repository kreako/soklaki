import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      "^/api/.*": {
        target: "http://127.0.0.1:8008/",
      },
      "^/reports/.*": {
        target: "http://127.0.0.1:8000/dl_report",
      },
      "^/zip_reports/.*": {
        target: "http://127.0.0.1:8000/dl_zip_reports",
      },
    },
  },
});
