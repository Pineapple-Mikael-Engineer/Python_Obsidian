---
title: plt.colorbar — Añadir una barra de color a un mappable
aliases:
  - colorbar
  - plt.colorbar
tags:
  - matplotlib
  - api/funcion
  - styling
lib: matplotlib
obj: pyplot
tipo: funcion
retorna: Colorbar
muta_estado: true
draft: false
---

# plt.colorbar — Añadir una barra de color a un mappable

## Idea clave

`plt.colorbar()` crea una **barra de color** que traduce los colores de un *mappable* (un Artist con escala de color: `imshow`, `scatter`, `contourf`, `pcolormesh`) a sus valores numéricos. Es la leyenda imprescindible de cualquier gráfico que codifica datos como color.

Roba espacio a los ejes indicados (`ax`) para colocar la barra y devuelve un objeto `Colorbar` configurable.

## Firma de la función

```python
matplotlib.pyplot.colorbar(
    mappable=None,   # ScalarMappable (imshow, scatter, contourf...)
    cax=None,        # Axes donde dibujar la barra (control manual)
    ax=None,         # Axes (o lista) a los que robar espacio
    *,
    label=None,      # etiqueta de la barra
    orientation=None,# 'vertical' | 'horizontal'
    fraction=0.15,   # fracción de espacio que ocupa
    shrink=1.0,      # factor de escala del largo
    pad=0.05,        # separación respecto al Axes
    **kwargs
)
```

## Valor de retorno

| Entrada | Retorno | Ejemplo |
|---------|---------|---------|
| un mappable válido | `Colorbar` | `cb = plt.colorbar(im)` |
| sin `mappable` | `Colorbar` del último mappable activo | `plt.colorbar()` |

```python
im = plt.imshow(matriz)
cb = plt.colorbar(im)
type(cb)        # → <class 'matplotlib.colorbar.Colorbar'>
cb.set_label("Temperatura (°C)")
```

## Parámetros en detalle

### `mappable` — la fuente del mapa de color

```python
sc = plt.scatter(x, y, c=valores, cmap="viridis")
plt.colorbar(sc, label="intensidad")
```

Debe ser un `ScalarMappable`. Si se omite, usa el mappable actual, lo que puede fallar con varios ejes; conviene pasarlo explícito.

### `ax` — a quién robar espacio

```python
fig, axs = plt.subplots(1, 2)
im = axs[0].imshow(m)
fig.colorbar(im, ax=axs)   # comparte una barra entre ambos ejes
```

### `orientation`, `shrink`, `pad` — colocación

```python
plt.colorbar(im, orientation="horizontal", shrink=0.8, pad=0.1)
```

| Parámetro | Efecto |
|-----------|--------|
| `orientation` | `'vertical'` (default) o `'horizontal'` |
| `shrink` | acorta la barra (`0.8` = 80% del largo) |
| `fraction` | fracción del Axes original cedida a la barra |
| `pad` | separación entre el Axes y la barra |

## Casos de uso

### Caso 1: mapa de calor con leyenda de color

```python
fig, ax = plt.subplots()
im = ax.imshow(matriz, cmap="plasma")
fig.colorbar(im, ax=ax, label="densidad")
```

### Caso 2: scatter coloreado por una tercera variable

```python
fig, ax = plt.subplots()
sc = ax.scatter(x, y, c=z, cmap="coolwarm")
cb = fig.colorbar(sc, ax=ax)
cb.set_label("z")
```

> En código orientado a objetos se prefiere `fig.colorbar(mappable, ax=ax)`, que es explícito sobre a qué figura y ejes pertenece la barra, frente a la función de estado de pyplot. Ver [[concepto_pyplot_vs_oo]].

## Buenas prácticas

1. Pasa siempre el `mappable` explícito: evita ambigüedad con varios ejes.
2. Indica `ax=...` (o una lista de ejes) para controlar de dónde sale el espacio.
3. Etiqueta la barra con `label=` o `cb.set_label(...)`: una colorbar sin unidades no informa.
4. Usa `shrink`/`fraction` para que la barra no domine la figura.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `RuntimeError: No mappable was found` | no hay mappable o se llamó sin `c=`/imagen | crear `imshow`/`scatter` con datos de color primero |
| La barra se superpone a otro subplot | falta `ax=` o `pad` | pasar `ax` correcto y ajustar `pad` |
| Barra desproporcionada | tamaño por defecto | usar `shrink`/`fraction` |
| Colores no coinciden con los datos | mappable equivocado | pasar el mappable concreto del plot deseado |

## Limitaciones

Requiere un `ScalarMappable`: no genera escala de color a partir de un `plot` de líneas normal. Para barras totalmente personalizadas (posición/tamaño exactos) usa el parámetro `cax` con un Axes creado a mano.

## Notas relacionadas

- [[concepto_pyplot_vs_oo]]
- [[Colorbar]]
- [[plt.subplots]]
- [[ax.imshow]]
- [[concepto_figure_axes]]
