---
title: ax.set_aspect — Relación de aspecto de los ejes
aliases:
  - set_aspect
  - ax.set_aspect
  - relacion de aspecto
tags:
  - matplotlib
  - api/metodo
  - formato
lib: matplotlib
obj: Axes
tipo: metodo
retorna: None
muta_estado: true
draft: false
---

# ax.set_aspect — Relación de aspecto de los ejes

## Firma de la función

```python
Axes.set_aspect(
    aspect,
    adjustable=None,
    anchor=None
) -> None
```

## Valor de retorno

`None`: fija cómo se relaciona la escala del eje Y con la del X. Controla si una unidad en X mide lo mismo que una unidad en Y en pantalla.

| `aspect` | Significado |
|----------|-------------|
| `'auto'` (por defecto) | el Axes se estira para llenar su área; X e Y independientes |
| `'equal'` | misma escala en X e Y (1 unidad X = 1 unidad Y en pantalla) |
| número (p. ej. `2`) | la altura de 1 unidad Y es `2`× el ancho de 1 unidad X |

```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.set_aspect('equal')   # imprescindible para círculos, mapas, geometría
```

## Por que importa

Sin `'equal'`, un círculo dibujado con [[Circle]] se ve **ovalado** porque X e Y tienen escalas distintas. Lo mismo afecta a mapas, vectores y cualquier geometría donde las proporciones cuentan.

```python
from matplotlib.patches import Circle
ax.add_patch(Circle((0, 0), 1))
ax.set_xlim(-2, 2); ax.set_ylim(-2, 2)
ax.set_aspect('equal')   # ahora el círculo es redondo
```

## Parámetros en detalle

### `aspect`

`'auto'`, `'equal'` o un número (ratio Y/X).

### `adjustable`

Qué se ajusta para cumplir el aspecto: `'box'` (cambia la forma del recuadro) o `'datalim'` (cambia los límites de datos).

## Casos de uso

### Mapas y datos geométricos

```python
ax.set_aspect('equal')   # que 1 km en X mida igual que 1 km en Y
```

### Imágenes

[[ax.imshow]] usa `aspect='equal'` por defecto (píxeles cuadrados); cámbialo con `aspect='auto'` si quieres que la imagen llene el Axes.

## Buenas prácticas

1. Usa `'equal'` siempre que las proporciones sean significativas (círculos, mapas, campos vectoriales).
2. Combínalo con [[ax.add_patch]] al dibujar formas geométricas.
3. Con `'equal'`, fija límites coherentes para que no quede espacio sobrante.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Círculos ovalados | aspecto `'auto'` por defecto | `ax.set_aspect('equal')` |
| Hueco grande alrededor | `'equal'` con límites desiguales | ajustar `set_xlim`/`set_ylim` |
| La imagen se deforma | `imshow` con `aspect='auto'` | dejar el `'equal'` por defecto |

## Limitaciones

- `'equal'` puede dejar espacio en blanco según los límites; es el precio de mantener proporciones.

## Notas relacionadas

- [[ax.add_patch]]
- [[ax.imshow]]
- [[Circle]]
- [[concepto_anatomia_figura]]
