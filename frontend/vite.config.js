import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Build portable: rutas relativas para poder abrir el dist en cualquier lado.
export default defineConfig({
  base: "./",
  plugins: [react()],
});
