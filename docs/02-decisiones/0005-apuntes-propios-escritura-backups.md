# ADR 0005 — Apuntes propios como fuente principal; escritura de archivos con backups

- **Estado:** Aceptado
- **Fecha:** 2026-06-18

## Contexto

El autor quiere que AMPA aprenda, **en ~90%**, de sus propios apuntes de
investigación, y que además pueda **corregir y mantener documentación** escribiendo
archivos tanto en **Windows** como en **Linux**.

## Decisión

1. **Fuente principal = apuntes del autor (regla 90/10).** La ingestión documental
   (RAG) de los apuntes es el mecanismo central de aprendizaje. La base curada de
   química y filosofía es solo el cimiento (~10%).
2. **Módulo "escriba" multiplataforma.** AMPA podrá escribir/corregir archivos usando
   rutas portables (`pathlib`), funcionando igual en Windows y Linux.
3. **Backups obligatorios.** Ninguna escritura ocurre sin crear antes una copia de
   seguridad con marca de tiempo. Cada cambio se registra.
4. **Espacio acotado.** El escriba solo opera dentro de un directorio de trabajo
   autorizado; nunca fuera de él.

## Alternativas

- **Reentrenar el modelo con cada apunte:** causa olvido catastrófico e
  inestabilidad (según el informe de investigación). Descartado para el día a día.
- **Escritura sin backups:** rápido pero peligroso; un error sobreescribe trabajo.
  Inaceptable.
- **Permitir escritura en todo el sistema de archivos:** riesgo innecesario.

## Consecuencias

- 👍 AMPA aprende de inmediato del material del autor, sin GPU.
- 👍 La corrección de documentación es segura y reversible.
- 👍 Portabilidad real Windows/Linux desde el diseño.
- 👎 Hay que diseñar con cuidado los permisos y los límites del escriba.
- ➡️ Introduce los módulos `knowledge/` (ingesta) y `scribe/` (escritura + backups).
