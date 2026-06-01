---
title: FuncFormatter — Formatea ticks con una función propia
aliases:
  - FuncFormatter
  - func formatter

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

# FuncFormatter — Formatea ticks con una función propia

## Firma de la función

```python
import matplotlib.ticker as ticker

ticker.FuncFormatter(func)
# func : callable(valor, pos) -> str
#   valor : float  → valor numérico del tick
#   pos   : int    → índice posicional del tick (puede ser None)
# → devuelve un Formatter que delega el texto en func
```

## Valor de retorno

| Construcción | Retorno | Se aplica con |
|--------------|---------|---------------|
| `ticker.FuncFormatter(f)` | objeto `Formatter` | `ax.xaxis.set_major_formatter(...)` |
| `f(valor, pos)` | string que verá el tick | lo decides tú |

```python
import matplotlib.ticker as ticker

def miles(x, pos):
    return f"{x/1000:.0f}k"      # → 5000 se muestra como 5k

ax.yaxis.set_major_formatter(ticker.FuncFormatter(miles))
```

## Parámetros en detalle

### func — la función de formato

Recibe `(valor, pos)` y devuelve la cadena exacta del tick. Es la máxima flexibilidad: cualquier lógica de Python.

```python
def grados(x, pos):
    return f"{int(x)}°C"          # → 20 se muestra como 20°C

ax.yaxis.set_major_formatter(ticker.FuncFormatter(grados))
```

El argumento `pos` permite alternar formato según la posición del tick:

```python
def alterna(x, pos):
    return f"{x:.0f}" if pos % 2 == 0 else ""   # → etiqueta uno sí, uno no
```

### Con lambda

Para casos breves se usa una lambda directamente.

```python
ax.yaxis.set_major_formatter(
    ticker.FuncFormatter(lambda x, pos: f"${x:,.0f}"))   # → $1,250
```

## Casos de uso

```python
import matplotlib.ticker as ticker

# Bytes legibles
def humano(x, pos):
    for u in ['B', 'KB', 'MB', 'GB']:
        if x < 1024:
            return f"{x:.0f}{u}"
        x /= 1024
    return f"{x:.0f}TB"

ax.yaxis.set_major_formatter(ticker.FuncFormatter(humano))

# Radianes como fracciones de pi
import numpy as np
def rad(x, pos):
    n = x / np.pi
    return "0" if n == 0 else f"{n:.0g}π"
ax.xaxis.set_major_formatter(ticker.FuncFormatter(rad))
```

## Buenas prácticas

1. Usa `FuncFormatter` cuando ningún formatter predefinido alcanza la lógica deseada.
2. La función debe devolver siempre un `str` (no un número).
3. Aprovecha `pos` para clarear etiquetas (mostrar una de cada dos).
4. Para formatos comunes (porcentaje, fecha) prefiere `PercentFormatter` o `DateFormatter`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `TypeError` en la función | firma sin `pos` | Define `func(x, pos)`, dos argumentos |
| Tick vacío inesperado | la función devuelve `None` | Devuelve siempre una cadena (`""` si quieres ocultar) |
| Número crudo en vez de texto | `return x` en vez de `str` | Formatea: `return f"{x:.1f}"` |
| Sin efecto | aplicado al Axis equivocado | Usa `ax.xaxis`/`ax.yaxis` correcto |

Cuando solo necesitas patrones fijos basta con los [[Formatters]] predefinidos; la posición sigue gobernada por los [[Locators]].

## Notas relacionadas

- [[Formatters]]
- [[Locators]]
- [[DateFormatter]]
