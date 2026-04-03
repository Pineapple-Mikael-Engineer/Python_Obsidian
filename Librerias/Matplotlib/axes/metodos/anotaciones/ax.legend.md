---
title: ax.legend — Leyenda de axes
aliases:
  - legend
  - leyenda
  - ax.legend
tags:
  - matplotlib
  - api/metodo
  - axes/metodos
lib: matplotlib
obj: Axes
tipo: metodo
muta_estado: true
requiere: []
draft: false
---






# ax.legend — Leyenda de axes

## Firma

```python
Axes.legend(
    handles=None,
    labels=None,
    loc='best',
    bbox_to_anchor=None,
    ncol=1,
    **kwargs
)
```

## Parámetros principales

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `handles` | lista de [[artist.Artist]] | `None` | Elementos a incluir en leyenda ([[lines.Line2D]], Patch, etc.) |
| `labels` | lista de `str` | `None` | Etiquetas correspondientes a handles |
| `loc` | `str` o `int` | `'best'` | Posición de la leyenda |
| `bbox_to_anchor` | tupla `(x, y)` o `(x, y, width, height)` | `None` | Anclaje para posicionamiento avanzado |
| `ncol` | `int` | `1` | Número de columnas |
| `**kwargs` | - | - | Ver Personalizacion_Leyendas |

## Posiciones predefinidas (loc)

| Código | String | Posición |
|--------|--------|----------|
| 0 | `'best'` | Automática (evita solapamiento) |
| 1 | `'upper right'` | Superior derecha |
| 2 | `'upper left'` | Superior izquierda |
| 3 | `'lower left'` | Inferior izquierda |
| 4 | `'lower right'` | Inferior derecha |
| 5 | `'right'` | Derecha |
| 6 | `'center left'` | Centro izquierda |
| 7 | `'center right'` | Centro derecha |
| 8 | `'lower center'` | Centro inferior |
| 9 | `'upper center'` | Centro superior |
| 10 | `'center'` | Centro |

```python
ax.legend(loc='upper left')
```

## Posicionamiento con bbox_to_anchor

`bbox_to_anchor` define un **rectángulo de anclaje** en coordenadas normalizadas (0 a 1) del axes. El parámetro `loc` determina qué parte de la leyenda se coloca en ese rectángulo.

### Caso 1: tupla `(x, y)` - punto de anclaje

```python
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
```

Interpretación:
- `bbox_to_anchor=(1.05, 1)` → punto en X=1.05, Y=1 (esquina superior derecha del axes + 5% a la derecha)
- `loc='upper left'` → la esquina superior izquierda de la leyenda se coloca en ese punto

Resultado: leyenda fuera del axes, a la derecha, alineada arriba.

### Caso 2: tupla `(x, y, width, height)` - rectángulo completo

```python
ax.legend(bbox_to_anchor=(0.5, 0.5, 0.5, 0.5), loc='center')
```

Interpretación:
- Se define un rectángulo centrado en (0.5, 0.5) con ancho 0.5 y alto 0.5
- `loc='center'` coloca el centro de la leyenda en el centro de ese rectángulo

### Sistema de coordenadas

| Valor | Significado |
|-------|-------------|
| `(0, 0)` | esquina inferior izquierda del axes |
| `(1, 1)` | esquina superior derecha del axes |
| `>1` | fuera del axes (a la derecha o arriba) |
| `<0` | fuera del axes (a la izquierda o abajo) |

### Ejemplos comunes

```python
# Leyenda fuera a la derecha (alineada arriba)
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

# Leyenda fuera a la derecha (alineada centro)
ax.legend(bbox_to_anchor=(1.05, 0.5), loc='center left')

# Leyenda debajo del axes
ax.legend(bbox_to_anchor=(0.5, -0.15), loc='upper center')

# Leyenda dentro, desplazada hacia la izquierda
ax.legend(bbox_to_anchor=(0.3, 0.9), loc='upper left')
```

## Manejo automático vs manual

### Automático (usa `label`)

```python
ax.plot(x, y1, label='Seno')
ax.plot(x, y2, label='Coseno')
ax.legend()  # automático
```

### Manual (especifica handles y labels)

```python
line1, = ax.plot(x, y1)
line2, = ax.plot(x, y2)
ax.legend(handles=[line1, line2], labels=['Seno', 'Coseno'])
```

### Incluir solo algunos elementos

```python
lines = ax.plot(x, y1, x, y2, x, y3)
ax.legend(handles=[lines[0], lines[2]], labels=['Primero', 'Tercero'])
```

### Mezclar tipos de artistas

```python
line, = ax.plot(x, y, label='Línea')
scatter = ax.scatter(x, y, c='red', label='Puntos')
ax.legend(handles=[line, scatter])
```

## Casos comunes

### Leyenda sin línea (solo marcador)

```python
ax.scatter(x, y, label='Puntos')
ax.legend(markerfirst=True)  # marcador antes que texto
```

### Ocultar elemento de la leyenda

```python
ax.plot(x, y1, label='Visible')
ax.plot(x, y2, label='_nolegend_')  # no aparece en leyenda
```

### Leyenda con título

```python
ax.legend(title='Curvas', title_fontsize=12)
```

Para más opciones de personalización, ver Personalizacion_Leyendas.

### Leyenda fuera del axes con ajuste automático

```python
fig, ax = plt.subplots()
ax.plot(x, y, label='Datos')
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
fig.tight_layout()  # ajusta márgenes para que quepa la leyenda
fig.subplots_adjust(right=0.8)  # alternativa manual
```

## Buenas prácticas

1. Siempre incluir `label` al graficar si se usará leyenda automática
2. Usar `loc='best'` como default (evita solapamiento)
3. Para leyendas fuera del axes, usar `bbox_to_anchor` y `fig.tight_layout()`
4. Mantener `ncol` bajo (2-3 columnas máximo) para legibilidad
5. Posicionar leyendas donde no oculten datos críticos
6. Usar `_nolegend_` para elementos auxiliares (líneas de referencia, rellenos)

## Errores comunes

| Error | Solución |
|-------|----------|
| Olvidar `label` y llamar `ax.legend()` sin argumentos | Agregar `label` o usar modo manual con `handles`/`labels` |
| Leyenda cortada fuera del axes | Usar `fig.tight_layout()` o `fig.subplots_adjust()` |
| `_nolegend_` no funciona con modo manual | Usar modo manual excluyendo el handle |
| `bbox_to_anchor` desplaza la leyenda al lugar incorrecto | Recordar que `loc` se aplica a la leyenda, no al ancla |
| Coordenadas fuera de rango (ej: >1) sin ajustar layout | La leyenda existe pero puede estar invisible; ajustar márgenes |

## Notas relacionadas

- [[ax.plot]]
