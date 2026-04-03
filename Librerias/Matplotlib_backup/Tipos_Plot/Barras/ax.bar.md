---
title: ax.bar — Gráfico de barras verticales
alias:
  - bar
  - barras
  - gráfico barras
tags:
  - matplotlib
  - axes
  - graficos
  - barras
draft: false
---

# ax.bar — Gráfico de barras verticales

## Firma

```python
Axes.bar(
    x,
    height,
    width=0.8,
    bottom=None,
    align='center',
    **kwargs
)
```

## Parámetros principales

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `x` | array-like | - | Posiciones de las barras en eje X |
| `height` | escalar o array-like | - | Altura de las barras |
| `width` | escalar o array-like | `0.8` | Ancho de las barras |
| `bottom` | escalar o array-like | `0` | Base de las barras (para apiladas) |
| `align` | `'center'` o `'edge'` | `'center'` | Alineación de la barra respecto a x |
| `**kwargs` | - | - | Propiedades de [[Rectangle]] |

## Parámetros adicionales (kwargs comunes)

| Parámetro | Ejemplo | Descripción |
|-----------|---------|-------------|
| `color` / `facecolor` | `color='blue'` | Color de relleno |
| `edgecolor` | `edgecolor='black'` | Color del borde |
| `linewidth` | `linewidth=1` | Grosor del borde |
| `alpha` | `alpha=0.7` | Transparencia |
| `label` | `label='Ventas'` | Etiqueta para [[ax.legend]] |
| `hatch` | `hatch='/'` | Patrón: `'/'`, `'\\'`, `'x'`, `'-'`, `'|'`, `'+'` |
| `zorder` | `zorder=3` | Orden de dibujo |

## Valor de retorno

```python
bars = ax.bar(x, height)
```

Retorna una lista de objetos `Rectangle` (un rectángulo por cada barra).

### Modificación posterior

```python
bars = ax.bar(x, height)

# Modificar barra individual
bars[0].set_color('red')
bars[0].set_height(15)
bars[0].set_width(0.5)

# Modificar todas
for bar in bars:
    bar.set_alpha(0.7)
    bar.set_edgecolor('black')
```

Ver [[Rectangle]] para métodos completos.

## Alineación (align)

| `align` | Posición de la barra respecto a `x` |
|---------|-------------------------------------|
| `'center'` | `x` es el centro de la barra (default) |
| `'edge'` | `x` es el borde izquierdo de la barra |

```python
# Alineación al borde (útil para series temporales)
ax.bar(x, height, align='edge', width=1.0)
```

## Barras apiladas (bottom)

```python
x = ['A', 'B', 'C']
valores1 = [10, 20, 15]
valores2 = [5, 10, 8]

ax.bar(x, valores1, label='Grupo 1')
ax.bar(x, valores2, bottom=valores1, label='Grupo 2')
ax.legend()
```

### Múltiples capas apiladas

```python
bottom_layer = valores1
ax.bar(x, valores1, label='Capa 1')

bottom_layer = [v1 + v2 for v1, v2 in zip(valores1, valores2)]
ax.bar(x, valores2, bottom=valores1, label='Capa 2')

ax.bar(x, valores3, bottom=bottom_layer, label='Capa 3')
```

## Barras agrupadas

```python
x = np.arange(len(categorias))  # posiciones numéricas
width = 0.35

ax.bar(x - width/2, valores1, width, label='Grupo 1')
ax.bar(x + width/2, valores2, width, label='Grupo 2')

ax.set_xticks(x)
ax.set_xticklabels(categorias)
ax.legend()
```

## Colores

### Color único

```python
ax.bar(x, height, color='steelblue')
```

### Colores por barra

```python
colores = ['red', 'blue', 'green', 'purple', 'orange']
ax.bar(x, height, color=colores)
```

### Usando colormap

```python
import numpy as np
import matplotlib.cm as cm

colores = cm.viridis(np.linspace(0, 1, len(x)))
ax.bar(x, height, color=colores)
```

Ver [[Colormaps]] para más opciones.

## Barras con barras de error

`ax.bar` acepta parámetros para barras de error que se pasan internamente a [[errorbar]].

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `yerr` | Error absoluto en Y (escalar o array) | `yerr=2` |
| `xerr` | Error absoluto en X (escalar o array) | `xerr=0.5` |
| `capsize` | Tamaño de los extremos de la barra de error (puntos) | `capsize=4` |
| `capthick` | Grosor de los extremos | `capthick=2` |
| `error_kw` | Diccionario con kwargs para [[errorbar]] | `error_kw={'linewidth': 2, 'color': 'red'}` |
| `ecolor` | Color de las barras de error (alternativa a error_kw) | `ecolor='black'` |

```python
# Error simple
errores = [2, 3, 1, 2]
ax.bar(x, height, yerr=errores, capsize=5)

# Error con personalización
ax.bar(x, height, yerr=errores, capsize=5, 
       error_kw={'linewidth': 2, 'color': 'darkred'})

# Error asimétrico
errores_arriba = [2, 3, 1, 2]
errores_abajo = [1, 2, 0.5, 1]
ax.bar(x, height, yerr=[errores_abajo, errores_arriba], capsize=5)
```

## Hatch (sombreado)

```python
ax.bar(x, height, hatch='/', edgecolor='black', facecolor='lightgray')
```

Patrones disponibles: `'/'`, `'\\'`, `'x'`, `'-'`, `'|'`, `'+'`, `'o'`, `'.'`, `'*'`.

## Casos comunes

### Barras con etiquetas de valor

```python
bars = ax.bar(x, height)
for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
            f'{bar.get_height()}', ha='center', va='bottom')
```

Ver [[ax.text]] para más opciones.

### Barras destacando un valor

```python
bars = ax.bar(x, height)
bars[2].set_color('red')  # destacar barra 2
bars[2].set_edgecolor('black')
bars[2].set_linewidth(2)
```

### Barras con línea base no cero

```python
ax.bar(x, height, bottom=10)  # todas comienzan desde 10
```

### Barras horizontales

Para gráficos de barras horizontales, ver [[ax.barh]].

```python
ax.barh(y, width)  # alternativa para barras horizontales
```

## Buenas prácticas

1. Mantener ancho de barra consistente en la misma gráfica
2. Usar `align='edge'` para datos temporales con intervalos
3. Limitar número de barras (< 20) para legibilidad
4. Usar colores contrastantes para grupos diferentes
5. Para barras apiladas, ordenar de mayor a menor (o viceversa)
6. Siempre etiquetar ejes ([[ax.set_xlabel_ylabel]])

## Errores comunes

| Error | Solución |
|-------|----------|
| `len(x) != len(height)` | Deben tener misma longitud |
| Barras superpuestas | Verificar `width` y posiciones `x` |
| Etiquetas X cortadas | Usar `fig.tight_layout()` o [[ax.set_xticks_yticks]] con rotación |
| Barras apiladas mal ordenadas | Verificar que `bottom` acumula correctamente |
| Colormap no funciona en `color` | Usar `color` con lista de colores, `cmap` no aplica a `bar` |

## Notas relacionadas

- [[ax.barh]]
- [[Rectangle]]
- [[ax.legend]]
- [[ax.set_xlabel_ylabel]]
- [[ax.set_xticks_yticks]]
- [[errorbar]]
- [[ax.text]]
- [[Colormaps]]
