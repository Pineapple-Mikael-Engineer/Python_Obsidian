---
title: ax.barh — Gráfico de barras horizontales
aliases:
  - barh
  - barras horizontales
  - horizontal bar
  - ax.barh
tags:
  - matplotlib
  - api/metodo
  - axes/metodos
lib: matplotlib
obj: Axes
tipo: metodo
muta_estado: true
requiere: []
draft: false
---






# ax.barh — Gráfico de barras horizontales

## Firma

```python
Axes.barh(
    y,
    width,
    height=0.8,
    left=None,
    align='center',
    **kwargs
)
```

## Parámetros principales

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `y` | array-like | - | Posiciones de las barras en eje Y |
| `width` | escalar o array-like | - | Longitud horizontal de las barras |
| `height` | escalar o array-like | `0.8` | Altura (grosor) de las barras |
| `left` | escalar o array-like | `0` | Punto de inicio horizontal (para apiladas) |
| `align` | `'center'` o `'edge'` | `'center'` | Alineación respecto a `y` |
| `**kwargs` | - | - | Propiedades de [[patches.Rectangle]] |

## Diferencia clave con bar

| Aspecto | `ax.bar` (vertical) | `ax.barh` (horizontal) |
|---------|---------------------|------------------------|
| Eje de posición | X | Y |
| Dimensión principal | `height` | `width` |
| Base/apilamiento | `bottom` | `left` |
| Grosor | `width` | `height` |

## Valor de retorno

```python
bars = ax.barh(y, width)
```

Retorna una lista de objetos `Rectangle` (un rectángulo por cada barra).

### Modificación posterior

```python
bars = ax.barh(y, width)
bars[0].set_color('red')
bars[0].set_width(15)  # cambiar longitud horizontal
bars[0].set_height(0.5)  # cambiar grosor
```

Ver [[patches.Rectangle]] y ax.bar para más detalles de modificación.

## Parámetros de estilo (kwargs)

Mismos que ax.bar:

| Parámetro | Ejemplo | Descripción |
|-----------|---------|-------------|
| `color` / `facecolor` | `color='blue'` | Color de relleno |
| `edgecolor` | `edgecolor='black'` | Color del borde |
| `linewidth` | `linewidth=1` | Grosor del borde |
| `alpha` | `alpha=0.7` | Transparencia |
| `label` | `label='Ventas'` | Etiqueta para ax.legend |
| `hatch` | `hatch='/'` | Patrón de sombreado |
| `zorder` | `zorder=3` | Orden de dibujo |

## Alineación (align)

| `align` | Posición de la barra respecto a `y` |
|---------|-------------------------------------|
| `'center'` | `y` es el centro de la barra (default) |
| `'edge'` | `y` es el borde inferior de la barra |

```python
ax.barh(y, width, align='edge')
```

## Barras apiladas (left)

```python
y = ['A', 'B', 'C']
valores1 = [10, 20, 15]
valores2 = [5, 10, 8]

ax.barh(y, valores1, label='Grupo 1')
ax.barh(y, valores2, left=valores1, label='Grupo 2')
ax.legend()
```

### Múltiples capas apiladas

```python
left_layer = valores1
ax.barh(y, valores1, label='Capa 1')

left_layer = [v1 + v2 for v1, v2 in zip(valores1, valores2)]
ax.barh(y, valores2, left=valores1, label='Capa 2')

ax.barh(y, valores3, left=left_layer, label='Capa 3')
```

## Barras agrupadas

```python
y = np.arange(len(categorias))
height = 0.35

ax.barh(y - height/2, valores1, height, label='Grupo 1')
ax.barh(y + height/2, valores2, height, label='Grupo 2')

ax.set_yticks(y)
ax.set_yticklabels(categorias)
ax.legend()
```

## Casos de uso típicos

### Cuándo usar barh en lugar de bar

| Situación | Razón |
|-----------|-------|
| Etiquetas de categoría largas | Espacio horizontal ilimitado para texto |
| Muchas categorías (10+) | Mejor aprovechamiento del alto de pantalla |
| Visualización de rankings | Natural ordenar de mayor a menor de arriba abajo |
| Comparación de duraciones | Más intuitivo para líneas de tiempo |

### Ejemplo: rankings

```python
categorias = ['Muy Largo', 'Nombre Largo', 'Corto', 'Mediano']
valores = [85, 70, 95, 60]

# Ordenar para mejor visualización
pares = sorted(zip(valores, categorias), reverse=True)
valores, categorias = zip(*pares)

ax.barh(categorias, valores)
ax.set_xlabel('Puntuación')
```

## Barras con barras de error

Mismos parámetros que ax.bar:

```python
errores = [2, 3, 1, 2]
ax.barh(y, width, xerr=errores, capsize=5)

# Error asimétrico
errores_izq = [1, 2, 0.5, 1]
errores_der = [2, 3, 1, 2]
ax.barh(y, width, xerr=[errores_izq, errores_der], capsize=5)
```

| Parámetro | Descripción |
|-----------|-------------|
| `xerr` | Error horizontal (similar a `yerr` en `bar`) |
| `capsize` | Tamaño de extremos |
| `error_kw` | Diccionario con kwargs para errorbar |

## Casos comunes

### Barras horizontales básicas

```python
ax.barh(categorias, valores, color='steelblue')
ax.set_xlabel('Valor')
ax.set_ylabel('Categoría')
```

### Barras horizontales con colores por valor

```python
import numpy as np
import matplotlib.cm as cm

norm = plt.Normalize(min(valores), max(valores))
colores = cm.viridis(norm(valores))
ax.barh(categorias, valores, color=colores)
```

### Barras horizontales con etiquetas de valor

```python
bars = ax.barh(y, width)
for bar in bars:
    ax.text(bar.get_width(), bar.get_y() + bar.get_height()/2,
            f'{bar.get_width()}', ha='left', va='center')
```

### Destacar una barra

```python
bars = ax.barh(y, width)
bars[2].set_color('red')
bars[2].set_edgecolor('black')
bars[2].set_linewidth(2)
```

## Buenas prácticas

1. Ordenar barras por valor (ascendente o descendente) para rankings
2. Usar `fig.tight_layout()` cuando las etiquetas Y son largas
3. Para muchas categorías (>10), aumentar `figsize` vertical
4. Usar `xerr` con `capsize` para mostrar incertidumbre
5. Preferir `barh` sobre `bar` cuando las etiquetas de categoría exceden 10-15 caracteres

## Errores comunes

| Error | Solución |
|-------|----------|
| Confundir `height` (grosor) con `width` (longitud) | `height` controla grosor vertical, `width` controla longitud horizontal |
| Usar `bottom` en lugar de `left` | Para apilamiento horizontal usar `left`, no `bottom` |
| Etiquetas Y cortadas | Ajustar `figsize` o usar `fig.tight_layout()` |
| Confundir `xerr` con `yerr` | Usar `xerr` para error horizontal en `barh` |

## Notas relacionadas

- [[ax.bar]]
- [[ax.legend]]
