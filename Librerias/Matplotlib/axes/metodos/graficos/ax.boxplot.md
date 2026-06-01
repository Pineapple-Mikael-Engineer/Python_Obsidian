---
title: ax.boxplot — Diagrama de caja y bigotes
aliases:
  - boxplot
  - ax.boxplot
  - caja y bigotes
  - diagrama de caja

tags:
  - matplotlib
  - api/metodo
  - plot/distribuciones

# --- Clasificación ---
lib: matplotlib
obj: Axes
tipo: metodo

# --- Comportamiento ---
retorna: dict
muta_estado: true

# --- Dependencias ---
requiere:
  - concepto_figure_axes

draft: false
---

# ax.boxplot — Diagrama de caja y bigotes

## Firma de la función

```python
Axes.boxplot(
    x,
    notch=None,
    sym=None,
    vert=None,
    whis=1.5,
    positions=None,
    widths=None,
    patch_artist=None,
    labels=None,
    showmeans=False,
    showcaps=True,
    showbox=True,
    showfliers=True,
    meanline=False,
    **kwargs
)
```

## Valor de retorno

Retorna un **diccionario** cuyas claves son grupos de Artists (no un solo objeto). Cada clave es una lista de [[concepto_artist]] que se pueden reestilizar después de dibujar.

| Clave | Contiene | Tipo de Artist |
|-------|----------|----------------|
| `'boxes'` | la caja (Q1–Q3) de cada grupo | `Line2D` o `Patch` (si `patch_artist=True`) |
| `'medians'` | la línea de la mediana | `Line2D` |
| `'whiskers'` | los bigotes (2 por caja) | `Line2D` |
| `'caps'` | las tapas de los bigotes (2 por caja) | `Line2D` |
| `'fliers'` | los outliers (puntos fuera de los bigotes) | `Line2D` |
| `'means'` | la media (solo si `showmeans=True`) | `Line2D` |

```python
bp = ax.boxplot(datos)
type(bp)            # <class 'dict'>
bp.keys()           # dict_keys(['whiskers','caps','boxes','medians','fliers','means'])
len(bp['boxes'])    # número de cajas dibujadas (1 por grupo)

# Reestilizar la mediana de la primera caja:
bp['medians'][0].set_color('red')
```

## Formas básicas de llamada

| Forma | `x` | Resultado |
|-------|-----|-----------|
| `boxplot(y)` | array 1D | una sola caja |
| `boxplot([y1, y2, y3])` | lista de arrays | una caja por grupo, lado a lado |
| `boxplot(M)` | array 2D `(n, k)` | una caja por **columna** (k cajas) |

## Parámetros en detalle

### `x` — los datos

El parámetro de datos (posicional). Acepta un array 1D (una caja) o una secuencia de arrays / matriz 2D (varias cajas). Los grupos pueden tener longitudes distintas si se pasa una lista de arrays.

| Tipo aceptado | Ejemplo | Cajas |
|---------------|---------|-------|
| array 1D | `np.random.randn(100)` | 1 |
| lista de arrays | `[a, b, c]` | 3 (longitudes libres) |
| array 2D `(n, k)` | `np.random.randn(100, 4)` | 4 (una por columna) |

### `notch` — caja con muesca

```python
ax.boxplot(datos, notch=True)   # muesca = intervalo de confianza de la mediana
```

Si las muescas de dos cajas no se solapan, es indicio (visual) de que sus medianas difieren significativamente.

### `labels` — etiquetas de los grupos

```python
ax.boxplot([a, b, c], labels=['control', 'A', 'B'])
# pone una etiqueta en el eje X bajo cada caja
```

### `whis` — alcance de los bigotes

Controla hasta dónde llegan los bigotes en múltiplos del rango intercuartílico (IQR = Q3 − Q1). Por defecto `1.5`. Lo que queda fuera se dibuja como `fliers` (outliers).

```python
ax.boxplot(datos, whis=1.5)        # bigotes a 1.5 * IQR (clásico de Tukey)
ax.boxplot(datos, whis=(5, 95))    # bigotes en los percentiles 5 y 95
```

### `vert` — orientación

```python
ax.boxplot(datos, vert=True)    # cajas verticales (por defecto)
ax.boxplot(datos, vert=False)   # cajas horizontales
```

### `patch_artist` — cajas rellenables

```python
bp = ax.boxplot(datos, patch_artist=True)
for caja in bp['boxes']:
    caja.set_facecolor('lightblue')   # ahora 'boxes' son Patch, no Line2D
```

### `showmeans` / `meanline` — mostrar la media

```python
ax.boxplot(datos, showmeans=True)               # media como marcador
ax.boxplot(datos, showmeans=True, meanline=True) # media como línea
```

## Casos de uso

### Comparar varias distribuciones

```python
import numpy as np
import matplotlib.pyplot as plt

datos = [np.random.normal(0, std, 200) for std in (1, 2, 3)]

fig, ax = plt.subplots()
ax.boxplot(datos, labels=['σ=1', 'σ=2', 'σ=3'])
ax.set_title("Dispersión por grupo")
ax.set_ylabel("valor")
```

### Cajas con color y muesca

```python
bp = ax.boxplot(datos, notch=True, patch_artist=True)
for caja in bp['boxes']:
    caja.set(facecolor='lightgreen', alpha=0.6)
for med in bp['medians']:
    med.set_color('black')
```

## Buenas prácticas

1. Pasa `labels` para identificar cada grupo en el eje.
2. Usa `patch_artist=True` cuando quieras rellenar las cajas con color.
3. Guarda el dict retornado si vas a reestilizar medianas, bigotes u outliers.
4. Documenta el criterio de `whis` si no es el clásico `1.5 * IQR`.
5. Para muchos grupos, considera `vert=False` para que las etiquetas no se solapen.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `bp.set_color(...)` falla | el retorno es un `dict`, no un Artist | indexar: `bp['boxes'][0].set_color(...)` |
| Las cajas no se rellenan | `boxes` son `Line2D` por defecto | pasar `patch_artist=True` |
| `labels` con longitud distinta a los grupos | una etiqueta por caja | igualar `len(labels)` al nº de grupos |
| Una sola caja con array 2D inesperado | 2D se interpreta por columnas | pasar lista de arrays 1D si se quiere control |
| Outliers "desaparecen" | `showfliers=False` o `whis` muy amplio | revisar `showfliers` y `whis` |

## Notas relacionadas

- [[concepto_artist]]
- [[Axes]]
- [[concepto_figure_axes]]
- [[ax.plot]]
- [[plt.subplots]]
