---
title: Multiples_Leyendas — Varias leyendas en un mismo Axes
aliases:
  - Multiples_Leyendas
  - multiple legends
  - dos leyendas
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

# Multiples_Leyendas — Varias leyendas en un mismo Axes

## Definición

Por defecto cada llamada a [[ax.legend]] **reemplaza** la leyenda anterior: solo puede haber una asociada al Axes. Para mostrar **dos o más leyendas a la vez** hay que crear la primera, guardarla y volver a registrarla manualmente con `ax.add_artist` antes de crear la segunda.

## El patrón clave

```python
# 1) primera leyenda (un subconjunto de líneas)
leg1 = ax.legend(handles=[l1, l2], loc='upper right', title='Grupo A')

# 2) re-registrarla como Artist para que NO la borre la siguiente
ax.add_artist(leg1)

# 3) segunda leyenda (otro subconjunto)
leg2 = ax.legend(handles=[l3, l4], loc='lower right', title='Grupo B')
```

Sin el paso 2, la segunda llamada elimina `leg1`. `add_artist` la fija como un `Artist` independiente que ya no es "la leyenda actual" del Axes (ver [[Legend]]).

## Por qué funciona

| Concepto | Explicación |
|----------|-------------|
| `ax.legend()` | crea la leyenda y la guarda en `ax.legend_` (atributo único) |
| Segunda llamada | sobrescribe `ax.legend_`, perdiendo la anterior |
| `ax.add_artist(leg1)` | añade `leg1` a la lista de artistas hijos, fuera de `ax.legend_` |
| Resultado | ambas se dibujan; solo la última es la "oficial" |

## Casos de uso

### Dos grupos temáticos

```python
l1, = ax.plot(x, y1, 'r-', label='Real A')
l2, = ax.plot(x, y2, 'r--', label='Modelo A')
l3, = ax.plot(x, y3, 'b-', label='Real B')
l4, = ax.plot(x, y4, 'b--', label='Modelo B')

leg1 = ax.legend(handles=[l1, l2], loc='upper left', title='A')
ax.add_artist(leg1)
ax.legend(handles=[l3, l4], loc='lower left', title='B')
```

### Separar estilo de color (leyenda de líneas + leyenda de marcadores)

```python
# leyenda 1: qué significa cada color
leg_color = ax.legend(handles=color_proxies, loc='upper right', title='Color')
ax.add_artist(leg_color)

# leyenda 2: qué significa cada estilo de marcador
ax.legend(handles=marker_proxies, loc='lower right', title='Marcador')
```

Cuando las entradas no corresponden a curvas reales conviene construir handles artificiales (proxies), descritos en la guía de control de handles.

## Buenas prácticas

1. Crea siempre las leyendas en orden y llama `ax.add_artist` a TODAS menos a la última.
2. Asigna `loc` distinto a cada una para que no se solapen.
3. Si controlas qué entra en cada leyenda mediante `handles`/`labels`, apóyate en [[handles_labels]] para construir los subconjuntos o proxies.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Solo aparece la última leyenda | falta `add_artist` en las previas | `ax.add_artist(leg1)` antes de la 2ª |
| Las leyendas se superponen | mismo `loc` en ambas | Dar `loc`/`bbox_to_anchor` distintos |
| La 1ª desaparece tras `tight_layout` | se editó como leyenda oficial | Re-registrarla con `add_artist` |
| Handles duplicados en ambas | se pasaron las mismas líneas | Repartir los `handles` en subconjuntos disjuntos |

## Notas relacionadas

- [[ax.legend]]
- [[Legend]]
- [[handles_labels]]
- [[Personalizacion_Leyendas]]
