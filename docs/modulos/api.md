# Módulo: api (API JSON portable)

> Documentado según la plantilla del Concepto Maestro §12.
> Código: `ampa/api/` · Pruebas: `tests/test_api.py` · Decisión: ADR 0015

## 1. Propósito

Exponer los dominios de AMPA (química, filosofía) por **HTTP/JSON** para un
frontend (p. ej. React), **sin dependencias** (`http.server`).

## 2. Responsabilidad exacta

**Hace:**
- Sirve endpoints JSON (química y filosofía) con **CORS** para el frontend.
- Sirve además el **frontend compilado** (`frontend/dist`) con fallback SPA.
- Despacha con una función **pura** `manejar(metodo, ruta, datos)` (testeable).
- Reutiliza los dominios; no añade lógica nueva.

**No hace:**
- No persiste estado propio (usa los módulos de dominio).
- No trae framework ni dependencias (ADR 0015/0007).

## 3. Entradas

- Peticiones HTTP GET/POST con cuerpo JSON.

## 4. Salidas / endpoints

- `GET  /api/salud`
- `GET  /api/quimica/tabla` · `POST /api/quimica/identificar`
- `POST /api/quimica/analizar` (molécula → fórmula, masa, grupos, reacciones)
- `GET/POST /api/quimica/compuestos` (listar / guardar)
- `POST /api/filosofia/identificar` · `POST /api/filosofia/pensar`
- `GET  /api/filosofia/diccionario`
- `GET  /*` → frontend compilado (SPA), si existe `frontend/dist`.

Arranque: `ampa servir` (solo API/estáticos) o `ampa ampakadabra` ✨ (compila el
frontend si falta, sirve web + API y abre el navegador).

## 5. Flujo interno

1. El handler lee método, ruta y (en POST) el JSON del cuerpo.
2. `manejar` busca la ruta y llama a la función del dominio.
3. Responde JSON (200) o error (400/404), con cabeceras CORS.

## 6. Decisiones de diseño

- **Stdlib antes que framework** (ADR 0015): portabilidad y cero dependencias.
- **Despacho puro** (`manejar`) separado del socket: se prueba sin red.
- **CORS abierto** para el desarrollo del frontend.

## 7. Errores esperados

- Ruta inexistente → 404; JSON o molécula inválida → 400.

## 8. Seguridad y límites

- Pensada para uso **local** (127.0.0.1). El CORS abierto es solo para desarrollo;
  hay que endurecerlo antes de exponerla en red.

## 9. Pruebas mínimas

- `tests/test_api.py` (7 casos): salud, tabla, identificar, analizar, filosofía,
  404 y 400 — sobre `manejar` (sin sockets).
- Ejecutar: `python -m unittest discover -s tests -t .`

## 10. Cambios pendientes

- Más endpoints según los pida el frontend.
- Empaquetar `ampakadabra` como ejecutable único para distribución.
