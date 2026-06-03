---
title: ax.add_patch — Añadir una forma (Patch) al Axes
aliases:
  - add_patch
  - ax.add_patch
tags:
  - matplotlib
  - api/metodo
  - plot/formas
lib: matplotlib
obj: Axes
tipo: metodo
retorna: Patch
muta_estado: true
draft: false
---

# ax.add_patch — Añadir una forma (Patch) al Axes

## Firma de la función

```python
Axes.add_patch(p) -> Patch
```

## Valor de retorno

Añade el [[Patch]] `p` (un [[concepto_artist|Artist]]) a la lista de hijos del Axes para que se dibuje, y devuelve el propio patch. **Es el paso imprescindible**: crear un `Rectangle`/`Circle`/… no lo muestra; hay que añadirlo con `add_patch`.

| Entrada | Efecto |
|---------|--------|
| una instancia de Patch | se dibuja en el Axes; se devuelve la misma instancia |

```python
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

fig, ax = plt.subplots()
ax.add_patch(Rectangle((0.2, 0.2), 0.4, 0.3, facecolor='skyblue'))
ax.add_patch(Circle((0.7, 0.7), 0.1, color='salmon'))
```

## Por que es necesario

Las formas de [[Patch]] son objetos "sueltos": no pertenecen a ningún Axes hasta que las añades. Sin `add_patch` no aparecen.

```python
rect = Rectangle((0, 0), 1, 1)
# ax... todavía no muestra nada
ax.add_patch(rect)   # ahora sí se dibuja
```

## Parámetros en detalle

### `p` — el patch a añadir

Cualquier instancia de [[Patch]]: [[Rectangle]], [[Circle]], [[Ellipse]], [[Polygon]], etc.

## Casos de uso

### Resaltar una región del gráfico

```python
ax.plot(x, y)
ax.add_patch(Rectangle((2, 0), 1, 5, alpha=0.2, color='yellow'))   # banda destacada
```

### Dibujar geometría sobre datos

```python
ax.add_patch(Circle((cx, cy), radius=r, fill=False, edgecolor='red', lw=2))
ax.set_aspect('equal')   # para que el círculo no salga ovalado (ver ax.set_aspect)
```

## Buenas prácticas

1. Recuerda fijar límites (`ax.set_xlim`/`set_ylim`) o usar `ax.autoscale`; `add_patch` no reescala los ejes automáticamente.
2. Para que los círculos se vean redondos, combina con [[ax.set_aspect]] `'equal'`.
3. Para añadir **muchos** patches eficientemente, usa una `PatchCollection` en vez de añadirlos uno a uno.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| El patch no aparece | no se llamó a `add_patch` | añadirlo explícitamente |
| El patch queda fuera de vista | los ejes no se reescalaron | fijar límites o `ax.autoscale_view()` |
| Círculo ovalado | aspecto no igual | `ax.set_aspect('equal')` |

## Limitaciones

- No reescala los ejes por sí solo (a diferencia de los métodos de ploteo como `ax.plot`).

## Notas relacionadas

- [[Patch]]
- [[Rectangle]]
- [[Circle]]
- [[ax.set_aspect]]
- [[concepto_artist]]
