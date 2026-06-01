---
title: fig.suptitle — Título global del Figure
aliases:
  - suptitle
  - fig.suptitle
tags:
  - matplotlib
  - api/metodo
  - styling
lib: matplotlib
obj: Figure
tipo: metodo
retorna: Text
muta_estado: true
draft: false
---

# fig.suptitle — Título global del Figure

## Idea clave

`fig.suptitle()` coloca un **título global** centrado en la parte superior del `Figure`, por encima de todos los subplots. Es distinto de `ax.set_title()`, que titula un único `Axes`. Pertenece al lienzo completo, como se explica en [[concepto_figure_axes]].

---

## Firma

```python
Figure.suptitle(
    t,                # str: texto del título
    x=0.5,            # posición horizontal (coords de figura, 0–1)
    y=0.98,           # posición vertical (coords de figura, 0–1)
    horizontalalignment='center',  # alias: ha
    verticalalignment='top',       # alias: va
    fontsize=None,    # tamaño de fuente (o 'large', 'x-large'…)
    fontweight=None,  # 'normal' | 'bold' | …
    **kwargs          # cualquier propiedad de Text
)
```

---

## Valor de retorno

| Entrada | Retorno | Ejemplo |
|---------|---------|---------|
| Texto del título | Objeto `Text` | `t = fig.suptitle("Informe")` |

```python
t = fig.suptitle("Resultados")
type(t)        # → <class 'matplotlib.text.Text'>
t.set_color("navy")   # se puede modificar después
```

El objeto `Text` devuelto es un `Artist`: se puede reestilizar tras crearlo.

---

## Parámetros en detalle

### `t` — el texto

```python
fig.suptitle("Análisis de la señal")
fig.suptitle(r"$\sigma = \sqrt{\sum (x-\mu)^2 / N}$")   # admite LaTeX
```

### `x`, `y` — posición en coordenadas de figura

```python
fig.suptitle("Arriba a la izquierda", x=0.1, y=0.95, ha="left")
```

| Coordenada | Significado |
|-----------|-------------|
| `x=0.5`, `y=0.98` | Centrado arriba (default) |
| `0` | Borde izquierdo / inferior del Figure |
| `1` | Borde derecho / superior del Figure |

### `fontsize`, `fontweight` — estilo

```python
fig.suptitle("Título destacado", fontsize=16, fontweight="bold")
```

---

## Casos de uso

### Título global sobre varios subplots

```python
import matplotlib.pyplot as plt

fig, axs = plt.subplots(1, 2, figsize=(10, 4))
axs[0].plot([1, 2, 3])
axs[1].plot([3, 2, 1])

axs[0].set_title("Subida")     # título del subgrafo izquierdo
axs[1].set_title("Bajada")     # título del subgrafo derecho
fig.suptitle("Comparación de tendencias")   # título de TODO el lienzo
```

### Título global + ajuste de espacio

```python
fig, axs = plt.subplots(2, 2)
fig.suptitle("Panel de métricas", fontsize=14)
fig.tight_layout()   # reserva espacio para que el suptitle no se solape
```

---

## Buenas prácticas

1. Usar `suptitle` solo para el mensaje que abarca **toda** la figura; los títulos por panel van en `ax.set_title()`.
2. Tras un `suptitle`, llamar a `fig.tight_layout()` o usar `layout='constrained'` para evitar que se solape con los subplots.
3. Guardar el `Text` devuelto si necesitas reestilizarlo o moverlo después.
4. Para subtítulos o anotaciones libres, preferir `fig.text()` en vez de forzar la posición del suptitle.

---

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Título solapa los subplots | No se reservó espacio | `fig.tight_layout()` o `layout='constrained'` |
| Se confunde con el título del panel | Se quería `ax.set_title()` | Usar el método del Axes para títulos por panel |
| Aparecen dos títulos | `suptitle` llamado dos veces crea dos `Text` | Reusar el objeto o ajustar el existente |

---

## Notas relacionadas

- [[concepto_figure_axes]]
- [[Figure]]
- [[fig.tight_layout]]
- [[ax.set_title]]
