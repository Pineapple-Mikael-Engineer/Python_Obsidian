---
title: Formatters — Texto de las etiquetas de ticks
aliases:
  - formatters
  - tick formatters
  - ScalarFormatter
  - FormatStrFormatter
  - PercentFormatter

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

# Formatters — Texto de las etiquetas de ticks

## Idea clave

Los `Formatters` controlan **qué texto** se dibuja en cada tick. Son la pareja de los Locators: los Locators deciden **dónde** caen las marcas, los Formatters deciden **cómo se escriben**.

```python
import matplotlib.ticker as ticker

ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
ax.yaxis.set_major_formatter(ticker.PercentFormatter())
```

## Valor de retorno

| Construcción | Retorno | Se aplica con |
|--------------|---------|---------------|
| `ticker.ScalarFormatter()` | objeto `Formatter` | `ax.xaxis.set_major_formatter(...)` |
| `ticker.FormatStrFormatter('%.2f')` | objeto `Formatter` | idem |
| `ticker.PercentFormatter()` | objeto `Formatter` | idem |

El Formatter en sí no muta el Axes; la mutación ocurre al pasarlo a `set_major_formatter`.

## Formatters principales

### ScalarFormatter

El formato numérico por defecto. Controla notación científica y offset.

```python
import matplotlib.ticker as ticker

fmt = ticker.ScalarFormatter(useMathText=True)
fmt.set_scientific(True)
fmt.set_powerlimits((-3, 4))     # → notación científica fuera de [1e-3, 1e4]
ax.yaxis.set_major_formatter(fmt)
```

### FormatStrFormatter

Formato estilo `printf` con `%`.

```python
import matplotlib.ticker as ticker

ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))   # → 3.14
ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d°'))    # → 90°
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('$%1.0f')) # → $50
```

### StrMethodFormatter

Igual que el anterior pero con `str.format` (estilo `{}`), recomendado en código moderno.

```python
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:.1f} kg'))   # → 12.5 kg
```

### PercentFormatter

Convierte valores a porcentajes.

```python
import matplotlib.ticker as ticker

# Datos en 0–1 mostrados como 0%–100%
ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1.0))   # → 0.25 → 25%

# Datos ya en 0–100
ax.yaxis.set_major_formatter(ticker.PercentFormatter())           # → 25 → 25%
```

### NullFormatter

Oculta el texto de los ticks (deja la marca, quita el número).

```python
ax.xaxis.set_minor_formatter(ticker.NullFormatter())   # → ticks menores sin etiqueta
```

## Major vs minor

Cada Axis acepta un formatter para ticks mayores y otro para menores.

```python
ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.0f'))
ax.xaxis.set_minor_formatter(ticker.NullFormatter())
```

## Casos de uso

```python
# Dos decimales fijos
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))

# Eje monetario
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))   # → $1,250

# Porcentaje a partir de proporciones
ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1.0))
```

## Combinación con locators

Los Formatters deciden el texto; la posición la deciden los [[Locators]]. Se suelen aplicar juntos.

```python
import matplotlib.ticker as ticker

ax.xaxis.set_major_locator(ticker.MultipleLocator(0.25))
ax.xaxis.set_major_formatter(ticker.PercentFormatter(xmax=1.0))
```

## Buenas prácticas

1. Usa `StrMethodFormatter` (`{}`) en código nuevo; `FormatStrFormatter` (`%`) es el clásico.
2. Para porcentajes desde proporciones, fija `xmax=1.0`.
3. Para máxima libertad usa `FuncFormatter` con una función propia.
4. Aplica `NullFormatter` a los minor ticks para no saturar de números.
5. Empareja siempre formatter + locator coherentes.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Decimales no cambian | formatter no aplicado al Axis correcto | Usa `ax.xaxis`/`ax.yaxis`, no `ax` |
| Porcentajes x100 erróneos | `xmax` por defecto (100) con datos 0–1 | Pasa `PercentFormatter(xmax=1.0)` |
| `%` literal sin formato | string sin especificador | Usa `'%.2f'`, no `'%'` |
| Formatter sin efecto visible | locator oculta los ticks | Revisa también el locator |

## Notas relacionadas

- [[Locators]]
- [[FuncFormatter]]
- [[DateFormatter]]
