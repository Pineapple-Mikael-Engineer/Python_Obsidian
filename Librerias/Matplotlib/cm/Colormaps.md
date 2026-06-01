---
title: Colormaps — Mapas de color que asignan valores a colores
aliases:
  - colormap
  - colormaps
  - cmap
  - mapa de color
tags:
  - matplotlib
  - api/objeto
  - styling

# --- Clasificación ---
lib: matplotlib
mod: matplotlib.cm
tipo: objeto
obj: Colormap

# --- Comportamiento ---
retorna: Colormap
muta_estado: false

draft: false
---

# Colormaps — Mapas de color que asignan valores a colores

## Definición

Un **colormap** es una función que mapea valores numéricos normalizados (0–1) a colores RGBA. Es el puente entre un dato escalar y su representación visual: combinado con un `Normalize`, traduce el rango real de tus datos al rango 0–1 que el colormap entiende. Es la propiedad central que hace que un objeto como [[PathCollection]] o una imagen muestre color en función del valor.

```python
import matplotlib.pyplot as plt

cmap = plt.get_cmap('viridis')   # obtener un colormap por nombre
cmap(0.0)    # → (0.267, 0.004, 0.329, 1.0)  color del extremo bajo
cmap(1.0)    # → (0.993, 0.906, 0.143, 1.0)  color del extremo alto
cmap(0.5)    # → color intermedio
```

## Categorías de colormaps

| Categoría | Cuándo usarla | Ejemplos |
|-----------|---------------|----------|
| **Secuencial** | datos ordenados de bajo a alto (densidad, temperatura) | `viridis`, `plasma`, `magma`, `inferno`, `Blues`, `Greens` |
| **Divergente** | datos con punto central significativo (cero, media) | `coolwarm`, `RdBu`, `seismic`, `bwr` |
| **Cualitativo** | categorías sin orden (grupos, clases) | `tab10`, `tab20`, `Set1`, `Pastel1` |
| **Cíclico** | datos que envuelven (ángulos, fase, hora) | `twilight`, `twilight_shifted`, `hsv` |

## Obtención y uso

| Acción | Código | Resultado |
|--------|--------|-----------|
| Obtener por nombre | `plt.get_cmap('plasma')` | objeto `Colormap` |
| Aplicar en scatter | `ax.scatter(x, y, c=z, cmap='viridis')` | colorea por valor |
| Aplicar en imagen | `ax.imshow(M, cmap='magma')` | imagen coloreada |
| Aplicar en contornos | `ax.contourf(X, Y, Z, cmap='coolwarm')` | regiones coloreadas |
| Invertir | `plt.get_cmap('viridis_r')` | mismo mapa invertido |
| Versión discreta | `plt.get_cmap('viridis', 5)` | 5 niveles discretos |

```python
z = np.random.rand(100)
scat = ax.scatter(x, y, c=z, cmap='viridis')
plt.colorbar(scat)   # la barra muestra la correspondencia valor → color
```

## Casos de uso

### Datos ordenados (secuencial)

```python
ax.imshow(elevacion, cmap='viridis')   # mapas de altura, densidad, intensidad
```

### Datos con punto cero (divergente)

```python
# Anomalías de temperatura: negativo azul, cero blanco, positivo rojo
ax.imshow(anomalias, cmap='coolwarm', vmin=-5, vmax=5)
```

### Categorías sin orden (cualitativo)

```python
ax.scatter(x, y, c=etiquetas, cmap='tab10')   # hasta 10 grupos distinguibles
```

## Buenas prácticas

1. Prefiere `viridis` (y la familia `plasma`/`magma`/`inferno`) sobre `jet`: son **perceptualmente uniformes**, sin bandas artificiales, y legibles en escala de grises y para daltónicos.
2. Empareja la categoría del colormap con la naturaleza del dato: secuencial para magnitudes, divergente para desviaciones respecto a un centro, cualitativo para clases.
3. Para datos divergentes, fija `vmin`/`vmax` simétricos para que el color central caiga exactamente en el punto de referencia.
4. Añade siempre [[plt.colorbar]]: sin leyenda de color, el mapa no comunica valores.
5. Usa el sufijo `_r` para invertir antes de inventar un colormap nuevo.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Colores planos / poca distinción | `jet` u otro mapa no uniforme | Cambiar a `viridis` o `cividis` |
| Centro descentrado en divergente | `vmin`/`vmax` asimétricos | Fijar límites simétricos respecto al centro |
| `cmap` no tiene efecto | `c` es un color fijo, no un array de valores | Pasar `c=` numérico |
| `ValueError: <nombre> is not a valid value` | nombre de colormap mal escrito | Revisar `plt.colormaps()` |
| Pocos grupos distinguibles | colormap secuencial para categorías | Usar cualitativo (`tab10`) |

## Notas relacionadas

- [[ListedColormap]]
- [[plt.colorbar]]
- [[ax.scatter]]
- [[concepto_artist]]
