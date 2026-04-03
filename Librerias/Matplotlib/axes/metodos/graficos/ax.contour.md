---
title: ax.contour — Curvas de nivel
aliases:
  - contour
  - curvas nivel
  - isolineas
tags:
  - matplotlib
  - metodo
  - graficos
  - contornos
  - tiene_retorno
draft: false
lib: matplotlib
obj: Axes
tipo: metodo
---

# ax.contour — Curvas de nivel

## Firma completa

```python
Axes.contour(
    X, Y, Z,
    levels=None,
    *,
    colors=None,
    cmap=None,
    norm=None,
    vmin=None,
    vmax=None,
    linewidths=None,
    linestyles=None,
    alpha=None,
    origin=None,
    extent=None,
    transform=None,
    **kwargs
)
```

### Formas alternativas de llamada

```python
# Forma 1: X, Y como vectores 1D
ax.contour(x, y, Z, levels=10)

# Forma 2: X, Y como malla 2D (de np.meshgrid)
ax.contour(X, Y, Z, levels=10)

# Forma 3: sin X, Y (usar índices)
ax.contour(Z, levels=10)
```

## Parámetros principales

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `X`, `Y` | array (1D o 2D) | - | Coordenadas de la cuadrícula |
| `Z` | array 2D (M, N) | - | Valores de altura |
| `levels` | int o array-like | `None` | Número de niveles o valores específicos |
| `colors` | color o lista | `None` | Color(es) de las líneas |
| `cmap` | `str` o `Colormap` | `None` | Mapa de colores |
| `norm` | `Normalize` | `None` | Normalización para colores |
| `vmin`, `vmax` | `float` | `None` | Límites de normalización |
| `linewidths` | `float` o lista | `None` | Grosor(es) de línea |
| `linestyles` | `str` o lista | `None` | Estilo(s) de línea |
| `alpha` | `float` | `None` | Transparencia |
| `origin` | `str` | `None` | Origen: `'upper'` o `'lower'` |
| `extent` | tupla (4,) | `None` | Límites `(left, right, bottom, top)` |
| `transform` | `Transform` | `None` | Transformación de coordenadas |

## Valor de retorno

```python
contour_set = ax.contour(X, Y, Z)
```

Retorna un objeto **[[QuadContourSet]]** que contiene todas las curvas de nivel.

### Modificación posterior básica

```python
cs = ax.contour(X, Y, Z, levels=10, cmap='viridis')

# Cambiar colormap de todas las líneas
cs.set_cmap('plasma')

# Cambiar transparencia
cs.set_alpha(0.7)

# Cambiar grosor de todas las líneas
for line in cs.collections:
    line.set_linewidth(1.5)

# Cambiar color de un nivel específico
cs.collections[3].set_color('red')

# Cambiar estilo de línea
for line in cs.collections:
    line.set_linestyle('dashed')

# Ocultar todos
cs.set_visible(False)

# Eliminar del axes
cs.remove()
```

### Métodos principales de QuadContourSet

| Método | Descripción | Ejemplo |
|--------|-------------|---------|
| `set_cmap()` | Cambia mapa de colores | `cs.set_cmap('coolwarm')` |
| `set_alpha()` | Cambia transparencia | `cs.set_alpha(0.5)` |
| `set_linewidth()` | Cambia grosor | `cs.set_linewidth(2)` |
| `set_linestyle()` | Cambia estilo | `cs.set_linestyle('--')` |
| `clabel()` | Añade etiquetas | `cs.clabel(inline=True)` |
| `remove()` | Elimina del gráfico | `cs.remove()` |

## Parámetros en detalle

### X, Y — coordenadas

| Forma | Requisito | Ejemplo |
|-------|-----------|---------|
| 1D para X e Y | `len(X) == Z.shape[1]`, `len(Y) == Z.shape[0]` | `x = np.linspace(0, 10, 100)` |
| 2D ambos | `X.shape == Y.shape == Z.shape` | `X, Y = np.meshgrid(x, y)` |
| `None` | - | `ax.contour(Z)` usa índices |

### levels — niveles de contorno

| Tipo | Comportamiento | Ejemplo |
|------|----------------|---------|
| Entero positivo | Crea ese número de niveles automáticos | `levels=15` |
| Lista/array | Usa esos valores exactos | `levels=[-2, -1, 0, 1, 2]` |
| `None` | Usa default (10) | `levels=None` |

### colors — colores de líneas

| Valor | Efecto | Ejemplo |
|-------|--------|---------|
| Color único | Todas las líneas del mismo color | `colors='black'` |
| Lista de colores | Un color por nivel | `colors=['red', 'green', 'blue']` |
| `None` | Usa [[Colormaps]] | `colors=None, cmap='viridis'` |

### cmap — mapa de colores

```python
ax.contour(X, Y, Z, cmap='viridis')     # secuencial
ax.contour(X, Y, Z, cmap='coolwarm')    # divergente
```

Ver [[Colormaps]].

### norm — normalización

Controla cómo los valores de `Z` se mapean a colores.

```python
import matplotlib.colors as colors

# Normalización lineal (default)
ax.contour(X, Y, Z, norm=colors.Normalize(vmin=-2, vmax=2))

# Normalización logarítmica
ax.contour(X, Y, Z, norm=colors.LogNorm())
```

### vmin, vmax — límites de normalización

Atajo para `Normalize(vmin, vmax)`.

```python
ax.contour(X, Y, Z, vmin=-2, vmax=2, cmap='RdBu')
```

### linewidths — grosor de línea

```python
ax.contour(X, Y, Z, linewidths=2)  # todas igual
ax.contour(X, Y, Z, linewidths=[0.5, 1, 1.5, 2])  # por nivel
```

### linestyles — estilo de línea

```python
ax.contour(X, Y, Z, linestyles='solid')
ax.contour(X, Y, Z, linestyles='dashed')
ax.contour(X, Y, Z, linestyles='dashdot')
ax.contour(X, Y, Z, linestyles='dotted')
```

Ver [[Estilos_Linea]].

### alpha — transparencia

```python
ax.contour(X, Y, Z, alpha=0.7)
```

### origin — origen de la matriz

Controla cómo se interpreta el índice (0,0) de `Z`:

| Valor | Interpretación |
|-------|----------------|
| `'upper'` | (0,0) es esquina superior izquierda |
| `'lower'` | (0,0) es esquina inferior izquierda (default) |

```python
ax.contour(Z, origin='lower')
```

### extent — límites de la cuadrícula

Define los límites `(left, right, bottom, top)` cuando no se usan `X, Y`.

```python
ax.contour(Z, extent=[0, 10, -5, 5])
```

### transform — transformación de coordenadas

Aplica una transformación a las coordenadas (útil para proyecciones).

```python
import matplotlib.transforms as transforms

# Transformación lineal
tr = transforms.Affine2D().rotate_deg(45)
ax.contour(X, Y, Z, transform=tr + ax.transData)
```

## Casos comunes

### Contorno básico con malla

```python
import numpy as np
x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
Z = np.exp(-(X**2 + Y**2))

ax.contour(X, Y, Z, levels=15, cmap='viridis')
ax.set_aspect('equal')
```

### Contorno con etiquetas de valor

```python
cs = ax.contour(X, Y, Z, levels=10, cmap='plasma')
ax.clabel(cs, inline=True, fontsize=8, fmt='%.2f')
```

### Contorno con niveles específicos

```python
niveles = [-2, -1, -0.5, 0, 0.5, 1, 2]
cs = ax.contour(X, Y, Z, levels=niveles, colors='black')
ax.clabel(cs, fmt='%1.1f')
```

### Contorno con relleno combinado

```python
# Relleno primero (contourf)
cf = ax.contourf(X, Y, Z, levels=20, cmap='coolwarm')
# Líneas encima (contour)
cs = ax.contour(X, Y, Z, levels=20, colors='black', linewidths=0.5)
# Barra de color
plt.colorbar(cf, label='Valor')
```

### Contorno con normalización logarítmica

```python
import matplotlib.colors as colors

Z_log = np.exp(Z)
ax.contour(X, Y, Z_log, levels=20, norm=colors.LogNorm(), cmap='viridis')
```

## Buenas prácticas

1. Usar `contourf` para relleno, `contour` para líneas
2. Combinar `contourf` + `contour` para mejor visualización
3. Usar `ax.set_aspect('equal')` para no distorsionar curvas
4. Usar `clabel` para curvas con valores importantes (especialmente nivel cero)
5. Elegir [[Colormaps]] apropiado: secuencial para datos monótonos, divergente para datos con punto medio
6. Para datos con cero, usar colormap divergente con blanco/neutro en cero (ej: `'RdBu'`, `'coolwarm'`)

## Errores comunes

| Error | Solución |
|-------|----------|
| Dimensiones de `X, Y, Z` inconsistentes | `Z` debe ser (M, N); `X` e `Y` pueden ser (M, N) o `len(X)==N`, `len(Y)==M` |
| `levels` muy alto (ruido visual) | Reducir número de niveles o usar `contourf` con alisado |
| Curvas cortadas en bordes | Extender rango de `X, Y` o usar `extent` |
| Colores poco distinguibles | Usar `cmap` en lugar de `colors` único |
| Contorno vacío sin curvas | Verificar que los niveles estén dentro del rango de `Z` (`np.min(Z)`, `np.max(Z)`) |

## Notas relacionadas

- [[ax.contourf]]
- [[QuadContourSet]]
- [[Colormaps]]
- [[plt.colorbar]]
- [[ax.clabel]]
- [[np.meshgrid]]
- [[Line2D]]
- [[Estilos_Linea]]
- [[Normalize]]
- [[LogNorm]]
