---
title: handles_labels — Control explícito de handles y labels de la leyenda
aliases:
  - handles_labels
  - handles y labels
  - proxy artist
tags:
  - matplotlib
  - api/objeto
  - styling

# --- Clasificación ---
lib: matplotlib
mod: matplotlib.legend
tipo: objeto
obj: Legend

# --- Comportamiento ---
retorna: Legend
muta_estado: false

draft: false
---

# handles_labels — Control explícito de handles y labels de la leyenda

## Definición

Una leyenda asocia **handles** (los artistas de muestra: una línea, un marcador, un parche) con **labels** (su texto). [[ax.legend]] suele inferirlos del `label=` de cada elemento, pero se pueden controlar a mano para reordenar, filtrar o inventar entradas que no corresponden a ninguna curva real (proxies).

## Dos modos de control

| Modo | Llamada | Cuándo |
|------|---------|--------|
| Automático | `ax.legend()` | usa el `label=` de cada artista |
| Explícito | `ax.legend(handles, labels)` | reordenar, filtrar o inyectar proxies |

```python
ax.plot(x, y1, label='Seno')
ax.plot(x, y2, label='Coseno')
ax.legend()                        # automático: lee los labels
```

## Recuperar los handles actuales

`ax.get_legend_handles_labels()` devuelve las dos listas paralelas tal como las detectó Matplotlib. Es la base para reordenar o filtrar.

```python
handles, labels = ax.get_legend_handles_labels()
# reordenar: invertir el orden de las entradas
ax.legend(handles[::-1], labels[::-1])
```

```python
# filtrar: mostrar solo algunas entradas
h, l = ax.get_legend_handles_labels()
keep = [0, 2]
ax.legend([h[i] for i in keep], [l[i] for i in keep])
```

## Proxy artists (entradas sin artista real)

Cuando quieres una entrada de leyenda para algo que no dibuja un `Artist` etiquetable (un relleno, una categoría conceptual), creas un artista artificial que **solo** sirve de muestra. No se añade al Axes; se pasa directo a `handles`.

```python
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

proxies = [
    Line2D([0], [0], color='red', lw=2, label='Tendencia'),
    Patch(facecolor='skyblue', edgecolor='none', label='Banda 95%'),
]
ax.legend(handles=proxies)
```

| Proxy | Clase | Uso típico |
|-------|-------|------------|
| Línea de muestra | `Line2D([0],[0], ...)` | representar un estilo de línea/marcador |
| Parche de color | [[Patch]] | representar un relleno o una categoría |

## Casos de uso

### Combinar artistas reales y proxies

```python
line, = ax.plot(x, y, label='Datos')
banda = Patch(facecolor='gray', alpha=0.3, label='Incertidumbre')
ax.legend(handles=[line, banda])
```

### Repartir handles entre varias leyendas

Cuando construyes [[Multiples_Leyendas]] sueles dividir estas listas en subconjuntos disjuntos, uno por leyenda.

```python
h, l = ax.get_legend_handles_labels()
leg1 = ax.legend(h[:2], l[:2], loc='upper right')
ax.add_artist(leg1)
ax.legend(h[2:], l[2:], loc='lower right')
```

## Buenas prácticas

1. Para reordenar/filtrar parte siempre de `get_legend_handles_labels()` en lugar de reescribir los labels a mano.
2. Los proxies son `Artist` que NO se añaden al Axes; pásalos solo por `handles`. Repasa el protocolo común en [[concepto_artist]].
3. Da el `label=` directamente al construir el proxy y luego puedes omitir la lista de `labels`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Entrada vacía en la leyenda | label empieza por `_` (`_nolegend_`) | Quitar el guion bajo inicial |
| Proxy aparece dibujado en el Axes | se añadió con `add_*` | No añadirlo; pasarlo solo a `handles` |
| `handles` y `labels` desalineados | listas de distinta longitud | Igualar longitudes o pasar solo `handles` con `label=` |
| Orden de leyenda no coincide con el plot | Matplotlib ordena por creación | Reordenar con slicing de las listas |

## Notas relacionadas

- [[ax.legend]]
- [[Multiples_Leyendas]]
- [[Legend]]
- [[concepto_artist]]
