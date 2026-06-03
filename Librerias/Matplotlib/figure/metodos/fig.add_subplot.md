---
title: fig.add_subplot — Añadir un Axes a la rejilla
aliases:
  - add_subplot
  - fig.add_subplot
tags:
  - matplotlib
  - api/metodo
  - layout
lib: matplotlib
obj: Figure
tipo: metodo
retorna: Axes
muta_estado: true
draft: false
---

# fig.add_subplot — Añadir un Axes a la rejilla

## Idea clave

`fig.add_subplot()` crea y añade **un** `Axes` a una rejilla del `Figure`, devolviéndolo para dibujar en él. Es la forma de **bajo nivel** de construir subplots, frente a [[plt.subplots]], que crea la rejilla completa de una sola vez. Encaja en la jerarquía lienzo/subgrafo descrita en [[concepto_figure_axes]].

---

## Firma

```python
Figure.add_subplot(
    nrows, ncols, index,   # posición en rejilla (o entero de 3 dígitos)
    *,
    projection=None,       # 'polar' | '3d' | None
    sharex=None,           # compartir eje X con otro Axes
    sharey=None,           # compartir eje Y con otro Axes
    **kwargs               # propiedades del Axes
)
```

---

## Valor de retorno

| Entrada | Retorno | Ejemplo |
|---------|---------|---------|
| Posición en rejilla | Un objeto `Axes` | `ax = fig.add_subplot(2, 2, 1)` |
| Con `projection='3d'` | `Axes3D` | `ax = fig.add_subplot(1, 1, 1, projection='3d')` |

```python
ax = fig.add_subplot(1, 1, 1)
type(ax)    # → <class 'matplotlib.axes._axes.Axes'>
```

---

## Formas básicas de llamada

| Llamada | Significado |
|---------|-------------|
| `add_subplot(2, 2, 1)` | Rejilla 2×2, posición 1 (arriba-izquierda) |
| `add_subplot(221)` | Igual que arriba, forma compacta de 3 dígitos |
| `add_subplot(1, 1, 1)` | Un único Axes que ocupa toda la figura |
| `add_subplot(gridspec[0, :])` | Posición tomada de un `GridSpec` |

> [!note] El índice empieza en **1** y recorre la rejilla por filas (izquierda→derecha, arriba→abajo).

---

## Parámetros en detalle

### `nrows, ncols, index` — la posición

```python
fig = plt.figure(figsize=(8, 5))
ax1 = fig.add_subplot(2, 1, 1)   # fila superior
ax2 = fig.add_subplot(2, 1, 2)   # fila inferior
```

### `projection` — tipo de Axes

```python
ax = fig.add_subplot(1, 1, 1, projection='3d')    # Axes 3D
ax = fig.add_subplot(1, 1, 1, projection='polar') # coordenadas polares
```

### `sharex` / `sharey` — compartir ejes manualmente

```python
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2, sharex=ax1)   # mismo eje X que ax1
```

---

## Casos de uso

### Construcción manual de una rejilla

```python
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(8, 6))
ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 2)
ax3 = fig.add_subplot(2, 2, 3)
ax4 = fig.add_subplot(2, 2, 4)

ax1.plot([1, 2, 3])
ax4.scatter([1, 2], [3, 4])
```

### Layout no uniforme (mezclando tamaños)

```python
fig = plt.figure()
ax_top = fig.add_subplot(2, 1, 1)        # ocupa la fila superior entera
ax_bl  = fig.add_subplot(2, 2, 3)        # cuarto inferior izquierdo
ax_br  = fig.add_subplot(2, 2, 4)        # cuarto inferior derecho
```

Esto es lo que `add_subplot` hace mejor que `plt.subplots`: combinar Axes de distintos tamaños sin recurrir a [[GridSpec]] explícito.

---

## Buenas prácticas

1. Para rejillas regulares, preferir `plt.subplots()`: una línea y array indexable.
2. Reservar `add_subplot()` para layouts heterogéneos o construcción dinámica de la figura.
3. Pasar `projection='3d'`/`'polar'` aquí cuando solo un panel necesita proyección especial.
4. Para compartir ejes en layouts manuales, encadenar `sharex=`/`sharey=` con el primer Axes creado.

---

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Índice fuera de rango | El índice empieza en 1, no en 0 | Usar `1..nrows*ncols` |
| Subplots superpuestos | Reusar el mismo `index` con rejillas distintas | Mantener una misma `nrows, ncols` coherente |
| `add_subplot(22)` inesperado | Forma de 3 dígitos mal escrita | Usar `add_subplot(2, 2, x)` o un entero de 3 cifras |
| Falta de espacio entre paneles | Layout no ajustado | `fig.tight_layout()` |

---

## Limitaciones

`add_subplot()` añade Axes de uno en uno y no gestiona la compartición de ejes ni el squeeze del array automáticamente. Para layouts regulares con muchos paneles, `plt.subplots()` es más conciso y escalable; para control fino de proporciones, combinar con `GridSpec`.

---

## Notas relacionadas

- [[concepto_figure_axes]]
- [[Figure]]
- [[plt.subplots]]
- [[GridSpec]]
- [[fig.tight_layout]]
- [[Axes]]
