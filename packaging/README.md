# Empaquetar AMPA como ejecutable (`ampakadabra`)

Genera un **ejecutable único** que lleva dentro la web + la API. Quien lo reciba
solo lo ejecuta y se abre el navegador con la app: **no necesita Python ni Node**.

## Pasos

```bash
# 1) Compila el frontend
cd frontend && npm install && npm run build && cd ..

# 2) Instala PyInstaller (solo para construir)
pip install pyinstaller

# 3) Construye
python packaging/build_exe.py
```

El ejecutable queda en `dist_exe/ampakadabra` (o `ampakadabra.exe` en Windows).

El `frontend/dist` se incrusta en el binario; al ejecutarse, el servidor lo
detecta mediante `sys._MEIPASS` (ADR 0015) y sirve la web + la API en
`http://127.0.0.1:8000`.
