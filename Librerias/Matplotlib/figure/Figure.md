---
title: Figure — El lienzo contenedor de Axes
aliases:
  - Figure
  - figura
tags:
  - matplotlib
  - api/clase
  - estructura
lib: matplotlib
obj: Figure
tipo: clase
retorna: Figure
muta_estado: false
draft: false
---

# Figure — El lienzo contenedor de Axes

## Idea clave

`Figure` es el **lienzo completo** de Matplotlib: la "hoja de papel" que contiene uno o varios `Axes`, más elementos globales (título global, leyendas a nivel de figura, colorbars). Controla el tamaño físico, el DPI y el guardado de la imagen.

Un `Figure` contiene N `Axes`; cada `Axes` pertenece a un solo `Figure`. Esta jerarquía contenedora se describe en [[concepto_figure_axes]].

> [!important] Rara vez se instancia con `Figure()` directo. La forma idiomática es crearlo (junto con sus Axes) mediante [[plt.subplots]], o vacío con `plt.figure()`.

---

## Firma del constructor

```python
matplotlib.figure.Figure(
    figsize=None,        # (ancho, alto) en pulgadas
    dpi=None,            # puntos por pulgada (resolución)
    facecolor=None,      # color de fondo del lienzo
    edgecolor=None,      # color del borde
    linewidth=0.0,       # grosor del borde
    frameon=None,        # dibujar el fondo del Figure
    layout=None,         # 'constrained' | 'tight' | 'compressed' | None
    **kwargs
)
```

Aunque el constructor acepta estos argumentos, en la práctica se pasan a través de las funciones de pyplot:

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 5), dpi=120)   # vía idiomática
fig = plt.figure(figsize=(8, 5))                  # lienzo vacío
fig = plt.figure()                                # defaults de rcParams
```

---

## Cómo se crea (formas habituales)

| Forma | Resultado | Cuándo usarla |
|-------|-----------|---------------|
| `fig, axs = plt.subplots(n, m)` | Figure + rejilla de Axes lista | Caso por defecto, layout regular |
| `fig = plt.figure()` | Figure vacío, sin Axes | Construir el layout a mano |
| `Figure()` | Figure sin gestor de ventana | Backends embebidos (GUI propia, web) |

---

## Atributos clave

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `axes` | `list[Axes]` | Lista de todos los Axes contenidos en el Figure |
| `dpi` | `float` | Resolución en puntos por pulgada (afecta tamaño en píxeles) |
| `number` | `int` | Identificador del Figure dentro de pyplot |
| `patch` | `Rectangle` | El fondo rectangular del lienzo |

```python
fig, axs = plt.subplots(2, 2)
len(fig.axes)   # → 4
fig.dpi         # → 100.0  (default)
```

---

## Métodos clave

| Método | Retorna | Rol |
|--------|---------|-----|
| `fig.savefig` | None | Guardar la figura a archivo (PNG, PDF, SVG…) |
| `fig.suptitle` | Text | Título global sobre todos los subplots |
| `fig.tight_layout` | None | Ajustar espaciados para evitar solapes |
| `fig.add_subplot` | Axes | Añadir un Axes a la rejilla (bajo nivel) |
| `fig.add_axes` | Axes | Añadir un Axes en posición arbitraria |
| `fig.colorbar` | Colorbar | Barra de color compartida a nivel de figura |

Los detalles de cada método viven en su nota: ver [[fig.suptitle]], `fig.tight_layout` y `fig.add_subplot`.

---

## Ejemplo de ciclo de vida

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)

# 1. Crear el Figure (lienzo) y sus Axes
fig, axs = plt.subplots(1, 2, figsize=(10, 4))

# 2. Dibujar en cada Axes (trabajo a nivel de subgrafo)
axs[0].plot(x, np.sin(x))
axs[1].plot(x, np.cos(x))

# 3. Operaciones globales (nivel Figure)
fig.suptitle("Seno y coseno")   # título global
fig.tight_layout()              # ajustar márgenes

# 4. Exportar
fig.savefig("trig.png", dpi=150)
```

La separación lienzo/subgrafo es coherente con el modelo de objetos `Artist`: tanto Figure como Axes son artistas contenedores.

---

## Buenas prácticas

1. Crear el Figure con `plt.subplots()` y trabajar con el `fig` devuelto; evita `Figure()` directo salvo en backends embebidos.
2. Reservar los métodos de `fig` para lo que afecta a **todo el lienzo** (título global, layout, guardado); usar los Axes para el contenido.
3. Fijar `figsize` y `dpi` desde el inicio para resultados reproducibles al exportar.
4. Usar `fig.savefig()` en lugar de `plt.savefig()` cuando manejas varios Figures.

---

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `fig.plot(...)` falla | Figure no dibuja datos; eso es de Axes | Usar `ax.plot(...)` |
| Título global solapado con subplots | Falta ajuste de layout | `fig.tight_layout()` o `layout='constrained'` |
| Imagen exportada borrosa | DPI bajo | `fig.savefig(..., dpi=150)` o más |
| `Figure()` no muestra ventana | Sin gestor de pyplot | Usar `plt.figure()` / `plt.subplots()` |

---

## Notas relacionadas

- [[concepto_figure_axes]]
- [[concepto_artist]]
- [[plt.subplots]]
- [[fig.suptitle]]
- [[fig.tight_layout]]
- [[fig.add_subplot]]
- [[Axes]]
- [[plt.savefig]]
