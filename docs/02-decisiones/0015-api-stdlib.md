# ADR-0015: API JSON con biblioteca estándar (stdlib) antes que un framework

> Formato según Concepto Maestro §13.

## Estado

Aceptada

## Contexto

AMPA necesita exponer sus dominios por HTTP/JSON para un frontend (React). La
portabilidad es un valor central (ADR 0007): el núcleo no tiene dependencias.
Frameworks como Django REST Framework o FastAPI añaden dependencias y peso.

## Opciones consideradas

- **A. API con `http.server`** de la biblioteca estándar (cero dependencias).
- **B. FastAPI**: ligero y moderno, con docs OpenAPI, pero con dependencias.
- **C. Django REST Framework**: potente pero pesado (ORM, migraciones, admin).

## Decisión

**Opción A.** Una capa fina (`ampa/api/`) sobre los dominios, con `http.server`,
JSON y CORS, despachada por una función pura `manejar(metodo, ruta, datos)`
(testeable sin sockets). Cero dependencias: corre donde haya Python. Si más
adelante se quiere OpenAPI/ecosistema, se puede envolver con FastAPI **sin tocar
los dominios**.

## Alternativas

**C** se descartó por pesado e innecesario (no hay base de datos relacional ni
autenticación). **B** se pospone: es buena opción, pero rompe el «cero
dependencias» que distingue a AMPA.

## Consecuencias

- 👍 Máxima portabilidad: el backend completo corre sin instalar nada.
- 👎 Sin utilidades de framework (validación, docs): se hacen a mano si hacen falta.
- ➡️ El despacho es puro y testeable; migrar a FastAPI sería solo envolverlo.
