---
title: ax.contourf — Contornos rellenos
aliases:
  - contourf
  - ax.contourf
  - contornos rellenos
  - mapa de niveles

tags:
  - matplotlib
  - api/metodo
  - plot/contornos

# --- Clasificación ---
lib: matplotlib
obj: Axes
tipo: metodo

# --- Comportamiento ---
retorna: QuadContourSet
muta_estado: true

# --- Dependencias ---
requiere:
  - numpy.meshgrid
  - concepto_figure_axes

draft: false
---

# ax.contourf — Contornos rellenos

## Firma de la función

```python
Axes.contourf(
    *args,          # [X, Y,] Z, [levels]
    levels=None,
    cmap=None,
    colors=None,
    norm=None,
    vmin=None,
    vmax=None,
    extend='neither',
    alpha=None,
    **kwargs
)
```

## Valor de retorno

Retorna un único objeto `QuadContourSet` (una colección de [[concepto_artist]] que agrupa todas las regiones rellenas por nivel). Ese objeto es el que se pasa a [[plt.colorbar]] para construir la barra de color.

| Entrada | Retorno | Uso típico |
|---------|---------|-----------|
| `contourf(Z)` | `QuadContourSet` | `fig.colorbar(cs)` |
| `contourf(X, Y, Z)` | `QuadContourSet` | rellena regiones entre niveles |
| `contourf(X, Y, Z, levels)` | `QuadContourSet` | niveles fijados manualmente |

```python
cs = ax.contourf(X, Y, Z, levels=10, cmap='viridis')
cs.levels          # array con los valores de corte de los niveles
fig.colorbar(cs)   # barra de color asociada
```

## contourf vs contour

| Aspecto | `ax.contourf` (esta nota) | `ax.contour` |
|---------|---------------------------|--------------|
| Qué dibuja | **regiones rellenas** entre niveles | solo **líneas** de nivel |
| Apariencia | mapa de color por bandas | curvas tipo "mapa topográfico" |
| Retorno | `QuadContourSet` | `QuadContourSet` |
| Etiquetas | menos habitual | suele usar `ax.clabel` |

A menudo se combinan: `contourf` para el relleno y [[ax.contour]] encima para resaltar las líneas. La `f` final significa *filled* (relleno).

## Parámetros en detalle

### `X`, `Y`, `Z` — la rejilla

`Z` es la matriz de valores; `X` e `Y` son las coordenadas de la rejilla, normalmente generadas con `numpy.meshgrid`. Si se omiten `X` e `Y`, se usan los índices de `Z`.

```python
import numpy as np
x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)     # X, Y tienen forma (100, 100)
Z = np.exp(-(X**2 + Y**2))   # misma forma que X e Y
```

| Argumento | Forma | Rol |
|-----------|-------|-----|
| `Z` | `(M, N)` | valores a colorear |
| `X`, `Y` | `(M, N)` o vectores compatibles | coordenadas de la rejilla |

### `levels` — número o valores de los niveles

```python
ax.contourf(X, Y, Z, levels=20)              # 20 bandas automáticas
ax.contourf(X, Y, Z, levels=[0, 0.2, 0.5, 1])  # cortes manuales
```

Un entero pide *aproximadamente* esa cantidad de niveles; una secuencia fija los cortes exactos (deben ir en orden creciente).

### `cmap` — mapa de color

```python
ax.contourf(X, Y, Z, cmap='viridis')   # perceptualmente uniforme (recomendado)
ax.contourf(X, Y, Z, cmap='coolwarm')  # divergente (centrado en un valor)
ax.contourf(X, Y, Z, cmap='gray')      # escala de grises
```

### `extend` — colorear fuera de rango

```python
ax.contourf(X, Y, Z, levels=[0.2, 0.5, 0.8], extend='both')
# 'neither' (def) | 'min' | 'max' | 'both' → flechas/colores en los extremos
```

### `alpha` — transparencia

```python
ax.contourf(X, Y, Z, alpha=0.6)   # útil al superponer sobre otra capa
```

## Casos de uso

### Mapa de color básico con barra

```python
import numpy as np
import matplotlib.pyplot as plt

x = y = np.linspace(-3, 3, 200)
X, Y = np.meshgrid(x, y)
Z = np.sin(X) * np.cos(Y)

fig, ax = plt.subplots()
cs = ax.contourf(X, Y, Z, levels=15, cmap='viridis')
fig.colorbar(cs, ax=ax, label="Z")
ax.set_title("Campo escalar")
```

### Relleno + líneas resaltadas

```python
cs = ax.contourf(X, Y, Z, levels=15, cmap='Blues')
lineas = ax.contour(X, Y, Z, levels=cs.levels, colors='k', linewidths=0.5)
ax.clabel(lineas, inline=True, fontsize=8)
```

## Buenas prácticas

1. Genera `X`, `Y` con `meshgrid` y verifica que `Z` comparte su forma.
2. Acompaña casi siempre el `contourf` con una barra de color para dar escala.
3. Prefiere mapas perceptualmente uniformes (`viridis`, `cividis`) frente a `jet`.
4. Usa `extend` cuando recortes los niveles para no perder los valores extremos.
5. Si quieres líneas de nivel, dibújalas con `contour` reutilizando `cs.levels`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `Input z must be 2D` | `Z` es 1D | construir `Z` sobre una rejilla 2D |
| Formas incompatibles `X/Y/Z` | tamaños distintos | igualar formas; usar `meshgrid` |
| `levels` no crecientes | secuencia desordenada | pasar niveles en orden ascendente |
| Imagen sin escala interpretable | falta barra de color | añadir `fig.colorbar(cs)` |
| `colors` y `cmap` a la vez | son mutuamente excluyentes | usar solo uno |

## Notas relacionadas

- [[ax.contour]]
- [[plt.colorbar]]
- [[concepto_artist]]
- [[Axes]]
- [[ax.imshow]]
- [[plt.subplots]]
