# AMPA — Frontend (React + Vite)

Interfaz visual con dos apartados (**Química** y **Filosofía**) que consume la API
local de AMPA. Portable: el núcleo y la API no tienen dependencias; este frontend
solo necesita Node para desarrollar/compilar.

## Uso

1. Arranca la API (en la raíz del repo):

   ```bash
   ampa servir            # http://127.0.0.1:8000
   ```

2. En `frontend/`:

   ```bash
   npm install
   npm run dev            # desarrollo (http://localhost:5173)
   # o
   npm run build          # genera dist/ (estático, abrible donde sea)
   ```

La URL de la API se puede cambiar con la variable `VITE_AMPA_API`.
