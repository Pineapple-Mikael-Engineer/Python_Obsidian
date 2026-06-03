---
title: Figure y Axes — La jerarquia contenedora de Matplotlib
aliases:
  - figure
  - axes
  - figura y ejes
  - figure vs axes
tags:
  - matplotlib
  - concepto
  - estructura
lib: matplotlib
tipo: concepto
requiere:
  - none
draft: false
---

# Figure y Axes — La jerarquia contenedora de Matplotlib

## Definicion fundamental

Todo grafico en Matplotlib vive dentro de dos contenedores anidados:

- **Figure** = el lienzo completo (la "hoja de papel"). Contiene uno o varios Axes.
- **Axes** = una region de ploteo individual (un sistema de coordenadas donde se dibuja). Es donde ocurre el 95% del trabajo: `ax.plot`, `ax.set_title`, etc.

**Regla mental:** un `Figure` contiene N `Axes`; un `Axes` pertenece a un solo `Figure`.

## Por que existe esta separacion

Separar el lienzo (Figure) de las regiones de dibujo (Axes) permite componer **varios subgrafos** en una sola imagen, controlar el tamaño/DPI/guardado a nivel de Figure y el contenido a nivel de Axes.

```python
import matplotlib.pyplot as plt

# Un Figure con una rejilla 2x2 de Axes
fig, axs = plt.subplots(2, 2)   # fig: el lienzo · axs: array (2,2) de Axes
axs[0, 0].plot([1, 2, 3])       # dibujo en un Axes concreto
fig.suptitle("Titulo del lienzo")  # propiedad del Figure (afecta a todo)
```

## La regla central: quien hace que

| Tarea | Objeto | Ejemplo |
|-------|--------|---------|
| Crear el lienzo | Figure | `plt.figure()`, `plt.subplots()` |
| Guardar/exportar la imagen | Figure | `fig.savefig('out.png')` |
| Titulo global | Figure | `fig.suptitle(...)` |
| Dibujar datos | Axes | `ax.plot`, `ax.scatter`, `ax.bar` |
| Titulo del subgrafo | Axes | `ax.set_title(...)` |
| Ejes, ticks, limites | Axes | `ax.set_xlim`, `ax.set_xticks` |
| Leyenda | Axes | `ax.legend()` |

> Si dudas dónde va un método: lo que afecta a **todo el lienzo** es del Figure; lo que afecta a **un subgrafo** es del Axes.

## La forma idiomatica de empezar

```python
fig, ax = plt.subplots()        # 1 Figure + 1 Axes, desempaquetados
ax.plot(x, y)
ax.set_title("Mi grafico")
fig.savefig("grafico.png")
```

`plt.subplots()` es la puerta de entrada recomendada: devuelve el Figure y los Axes ya creados, listos para la interfaz orientada a objetos (ver [[concepto_pyplot_vs_oo]]).

## Casos que confunden

### Axes no es lo mismo que Axis

- **Axes** (plural-looking, singular) = la region de ploteo completa.
- **Axis** = un eje individual (X o Y) dentro de un Axes.

Ver [[concepto_anatomia_figura]] para el vocabulario completo.

### Varios Axes: indexar el array

```python
fig, axs = plt.subplots(1, 3)
for ax in axs:           # axs es un array de Axes
    ax.plot(...)
```

Con un solo subplot, `plt.subplots()` devuelve un Axes suelto (no un array). Ver [[arrays]] para el manejo de rejillas de Axes.

## Relacion con otros conceptos

- [[concepto_artist]]
- [[concepto_pyplot_vs_oo]]
- [[concepto_anatomia_figura]]
- [[plt.subplots]]
- [[Figure]]
- [[Axes]]
