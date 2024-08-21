import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";
import anywidget from "@anywidget/vite";

// https://vitejs.dev/config/
export default defineConfig({
  build: {
    outDir: "src/jupyter_bbox_widget/static",
    lib: {
      entry: ["svelte/main.js"],
      formats: ["es"],
    },
  },
  plugins: [svelte({ hot: false }), anywidget()],
});
