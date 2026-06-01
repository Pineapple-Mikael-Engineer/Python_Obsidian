---
title: DateFormatter — Formatea ticks de fechas con strftime
aliases:
  - DateFormatter
  - date formatter

tags:
  - matplotlib
  - api/clase
  - formato

# --- Clasificación ---
lib: matplotlib
obj: ticker
tipo: clase

# --- Comportamiento ---
muta_estado: false

draft: false
---

# DateFormatter — Formatea ticks de fechas con strftime

## Firma de la función

```python
import matplotlib.dates as mdates

mdates.DateFormatter(fmt, tz=None, usetex=None)
# fmt : str   → patrón strftime (códigos %Y, %m, %d, %H, %M...)
# → devuelve un Formatter aplicable a un eje temporal
```

Nota: `DateFormatter` vive en `matplotlib.dates`, no en `matplotlib.ticker`, pero es un Formatter como los del módulo ticker y se aplica igual.

## Valor de retorno

| Construcción | Retorno | Se aplica con |
|--------------|---------|---------------|
| `mdates.DateFormatter('%Y-%m')` | objeto `Formatter` | `ax.xaxis.set_major_formatter(...)` |
| Tick con valor de fecha | string formateado | `2026-06` |

```python
import matplotlib.dates as mdates
fmt = mdates.DateFormatter('%Y-%m')
ax.xaxis.set_major_formatter(fmt)
# → ticks como 2026-01, 2026-02, ...
```

## Parámetros en detalle

### fmt — patrón strftime

Cadena con códigos de fecha estándar de Python.

| Código | Significado | Ejemplo de salida |
|--------|-------------|-------------------|
| `%Y` | año (4 dígitos) | `2026` |
| `%m` | mes (01–12) | `06` |
| `%d` | día (01–31) | `01` |
| `%H` | hora (00–23) | `14` |
| `%M` | minuto | `30` |
| `%b` | mes abreviado | `Jun` |
| `%a` | día de semana abreviado | `Mon` |

```python
mdates.DateFormatter('%d/%m/%Y')   # → 01/06/2026
mdates.DateFormatter('%b %Y')      # → Jun 2026
mdates.DateFormatter('%H:%M')      # → 14:30
```

### tz — zona horaria

Opcional, para datos con timezone. Por defecto usa la del sistema.

```python
import matplotlib.dates as mdates
fmt = mdates.DateFormatter('%H:%M', tz='UTC')
```

## Casos de uso

```python
import matplotlib.dates as mdates

# Eje mensual
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))   # → Jun 2026

# Eje diario con rotación de etiquetas
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
fig.autofmt_xdate()      # → rota las etiquetas para que no se solapen
```

## Buenas prácticas

1. Empareja `DateFormatter` con un date-locator (`MonthLocator`, `DayLocator`...).
2. Usa `fig.autofmt_xdate()` para rotar etiquetas largas de fecha.
3. Mantén el patrón corto (`%b %Y`) si hay muchos ticks.
4. Convierte tus datos a `datetime` o usa `plot_date` antes de formatear.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Etiquetas como números grandes | el eje no es temporal | Plotea fechas como `datetime`/`np.datetime64` |
| Fechas solapadas | demasiados ticks juntos | `fig.autofmt_xdate()` o un locator más espaciado |
| Formato literal sin sustituir | código strftime mal escrito | Revisa `%Y`, `%m`, `%d` (sensibles a may/min) |
| Solo funciona en major | minor sin formatter | Llama también `set_minor_formatter` |

La posición de los ticks temporales la fija el date-locator, pareja de estos [[Formatters]] descrita junto a los [[Locators]].

## Notas relacionadas

- [[Formatters]]
- [[Locators]]
- [[FuncFormatter]]
