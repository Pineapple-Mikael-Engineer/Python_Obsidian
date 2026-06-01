---
title: QuadContourSet — El conjunto de contornos que devuelven contour y contourf
aliases:
  - QuadContourSet
  - conjunto de contornos
  - contour set
tags:
  - matplotlib
  - api/clase
  - plot/contornos

# --- Clasificación ---
lib: matplotlib
mod: matplotlib.contour
tipo: clase
obj: QuadContourSet

# --- Comportamiento ---
retorna: QuadContourSet
muta_estado: false

draft: false
---

# QuadContourSet — El conjunto de contornos que devuelven contour y contourf

## Definición

`QuadContourSet` es el objeto que **devuelven** [[ax.contour]] y `ax.contourf`: agrupa todas las líneas (o regiones rellenas) de nivel calculadas sobre una malla como un único conjunto de Artists. Guarda los niveles, sus colores y las trayectorias, y se pasa tal cual a [[plt.colorbar]] para la leyenda de color y a `ax.clabel` para etiquetar cada nivel.

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
cs = ax.contour(X, Y, Z)              # líneas de nivel
type(cs)   # → <class 'matplotlib.contour.QuadContourSet'>

csf = ax.contourf(X, Y, Z, cmap='viridis')   # regiones rellenas
```

## Atributos y métodos clave

| Miembro | Qué representa / hace | Ejemplo |
|---------|-----------------------|---------|
| `cs.levels` | array con los valores de cada nivel de contorno | `cs.levels` → `[0, 2, 4, 6, 8]` |
| `cs.collections` | las colecciones de líneas/regiones por nivel | `cs.collections` |
| `ax.clabel(cs)` | etiqueta los niveles sobre el gráfico | `ax.clabel(cs, inline=True)` |
| `plt.colorbar(cs)` | barra de color asociada a los niveles | `fig.colorbar(cs)` |
| `cs.set_cmap(name)` | cambia el colormap de las regiones | `csf.set_cmap('plasma')` |

## Etiquetar y dar color

El conjunto se conecta con dos herramientas: la leyenda de color y el etiquetado de niveles. Para datos continuos, su colormap procede del mismo sistema de [[Colormaps]] que el resto de la librería.

```python
cs = ax.contour(X, Y, Z, levels=10)
ax.clabel(cs, inline=True, fontsize=8)   # números sobre cada curva
plt.colorbar(cs)                          # leyenda de niveles
```

## Casos de uso

### Contornos de línea con niveles concretos

```python
cs = ax.contour(X, Y, Z, levels=[0, 1, 2, 5, 10])
ax.clabel(cs, inline=True, fmt='%1.0f')
```

### Relleno (contourf) con barra de color

```python
csf = ax.contourf(X, Y, Z, levels=20, cmap='coolwarm')
plt.colorbar(csf, label='magnitud')
```

### Combinar relleno y líneas

```python
csf = ax.contourf(X, Y, Z, cmap='viridis', alpha=0.8)
cs = ax.contour(X, Y, Z, colors='black', linewidths=0.5)
ax.clabel(cs, inline=True, fontsize=7)
```

## Buenas prácticas

1. Guarda el retorno (`cs = ax.contour(...)`) para poder etiquetar con `clabel` y añadir la barra de color; sin él pierdes el acceso al conjunto.
2. Genera la malla con `np.meshgrid` antes de evaluar `Z`: `contour` espera `X`, `Y`, `Z` 2D coherentes.
3. Controla los niveles con `levels=` (un entero para nº automático, o una lista para valores exactos).
4. Para datos divergentes usa un colormap divergente y `levels` simétricos respecto al centro.
5. Combina `contourf` (relleno) + `contour` (líneas negras finas) para legibilidad.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `clabel` no muestra etiquetas | no se guardó el `QuadContourSet` | `cs = ax.contour(...)` y `ax.clabel(cs)` |
| Colorbar no aparece | no se pasó el conjunto a `colorbar` | `plt.colorbar(cs)` con el retorno |
| `Input z must be 2D` | `Z` no es bidimensional | Construir `Z` sobre malla `meshgrid` |
| Niveles desordenados o vacíos | `levels` no monótonos o fuera del rango de `Z` | Usar lista creciente dentro del rango de datos |
| Contornos en blanco | todos los valores de `Z` iguales | Verificar que `Z` varía |

## Notas relacionadas

- [[ax.contour]]
- [[plt.colorbar]]
- [[Colormaps]]
- [[concepto_artist]]
- [[PathCollection]]
