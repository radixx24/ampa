# Contrato: evento de percepción

> Define el formato del **Evento** que produce la capa de percepción. Es un
> contrato **estable**: otros módulos (orquestador, memoria, escriba) dependen de
> estos campos. Fuente: Concepto Maestro §5.2 · Implementación:
> `ampa/perception/events.py`.

## Esquema

```yaml
evento:
  tipo: pregunta | archivo_modificado | correccion | error | decision | comando
  dominio_probable: quimica | filosofia | general | documentacion | operacion
  entidades_relevantes: []      # términos/conceptos distintivos detectados
  archivos_relacionados: []     # rutas mencionadas o indicadas
  intencion_detectada: ""       # breve descripción de la intención
  riesgo_operativo: bajo | medio | alto
  guardar_en_memoria: true | false
  justificacion: ""             # por qué se clasificó y evaluó así
```

## Campos

| Campo | Tipo | Descripción |
|---|---|---|
| `tipo` | enum | Naturaleza del evento. |
| `dominio_probable` | enum | Dominio asignado por el clasificador. |
| `entidades_relevantes` | lista | Términos distintivos hallados. |
| `archivos_relacionados` | lista | Rutas mencionadas en el texto o aportadas. |
| `intencion_detectada` | texto | Resumen de la intención (tipo + dominio). |
| `riesgo_operativo` | enum | Señal de riesgo para acciones de escritura. |
| `guardar_en_memoria` | bool | Si el evento debe persistir (anti-ruido). |
| `justificacion` | texto | Explicación auditable de la clasificación. |

## Reglas de riesgo

- **alto:** comando que modifica archivos, o intención de modificación con
  archivos presentes.
- **medio:** comando sin modificación, o corrección / cambio de archivo, o hay
  archivos relacionados.
- **bajo:** el resto (típicamente preguntas).

## Reglas de memoria (§6.2)

- Se **guarda** si el dominio no es `general`, o si el tipo es `decision`,
  `correccion` o `archivo_modificado`.
- **No** se guarda una pregunta `general` muy breve (se considera ruido).

## Estabilidad

Cambiar este contrato obliga a actualizar `events.py`, la capa de percepción y este
documento; y a registrar un ADR si el cambio afecta a otros módulos.
