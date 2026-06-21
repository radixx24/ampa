# ADR-0012: Orquestación del ciclo — proponer por defecto, ejecutar con autorización

> Formato según Concepto Maestro §13.

## Estado

Aceptada

## Contexto

El comando `ciclo` realiza el lazo percepción → memoria → acción (§6). La etapa de
acción **escribe archivos**, lo que es irreversible si se hace a la ligera. Hace
falta una semántica segura y predecible para un comando que toca disco y memoria.

## Opciones consideradas

- **A. Proponer por defecto (simular); ejecutar solo con `--ejecutar`.**
- **B. Ejecutar siempre** (más directo, pero arriesgado y sorprendente).
- **C. Pedir confirmación interactiva** en cada ejecución (no portable a scripts ni
  a entornos no interactivos).

## Decisión

**Opción A.** Por defecto, `ciclo` **propone**: percibe, recupera y **simula** la
escritura sin persistir nada. Con `--ejecutar` recuerda la observación (diario y
memoria según la política) y escribe con **respaldo previo**, siempre bajo la
**puerta de riesgo** (`riesgo alto` exige `--forzar`).

## Alternativas

**B** se descartó por inseguro; **C** por no ser portable ni automatizable. La
simulación por defecto cubre la necesidad sin diálogo interactivo.

## Consecuencias

- 👍 Comando seguro de invocar; efectos solo con autorización explícita; reversible.
- 👎 Requiere un segundo paso (`--ejecutar`) para aplicar; dos invocaciones.
- ➡️ La nota podrá enriquecerse con generación (LLM) sin cambiar esta semántica.
