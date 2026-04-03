---
title: ax.set_title — Título del axes
alias:
  - set_title
  - titulo
  - title
tags:
  - matplotlib
  - axes
  - labels
  - formato
draft: false
---

# ax.set_title — Título del axes

## Firma

```python
Axes.set_title(
    label,
    fontdict=None,
    loc='center',
    pad=None,
    **kwargs
)
```

## Parámetros principales

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `label` | `str` | - | Texto del título |
| `fontdict` | `dict` | `None` | Diccionario de propiedades de fuente |
| `loc` | `str` | `'center'` | Posición del título |
| `pad` | `float` | `None` | Espacio entre título y axes (puntos) |
| `**kwargs` | - | - | Propiedades de [[Text]] (color, size, weight, etc.) |

## Posiciones disponibles (loc)

| Valor | Posición |
|-------|----------|
| `'left'` | Izquierda |
| `'center'` | Centro (default) |
| `'right'` | Derecha |

```python
ax.set_title('Título centrado', loc='center')
ax.set_title('Izquierda', loc='left')
ax.set_title('Derecha', loc='right')
```

## Parámetros de fuente (kwargs)

Los argumentos adicionales se pasan al objeto [[Text]] interno.

| Parámetro | Ejemplo | Descripción |
|-----------|---------|-------------|
| `fontsize` | `fontsize=14` | Tamaño de fuente |
| `fontweight` | `fontweight='bold'` | Grosor ('normal', 'bold') |
| `fontstyle` | `fontstyle='italic'` | Estilo ('normal', 'italic') |
| `color` | `color='navy'` | Color del texto |
| `backgroundcolor` | `backgroundcolor='lightgray'` | Color de fondo |
| `alpha` | `alpha=0.8` | Transparencia |

```python
ax.set_title('Resultados', fontsize=16, fontweight='bold', color='darkblue')
```

## Uso de fontdict

`fontdict` agrupa propiedades de fuente en un diccionario:

```python
font = {'family': 'serif', 'color': 'darkred', 'weight': 'bold', 'size': 14}
ax.set_title('Título con fontdict', fontdict=font)
```

## pad — espaciado

Controla la distancia entre el título y el axes (en puntos).

```python
ax.set_title('Título separado', pad=20)  # más separación del axes
```

## Casos comunes

### Título simple

```python
ax.set_title('Evolución de la temperatura')
```

### Título con formato matemático (LaTeX)

```python
ax.set_title(r'$E = mc^2$')
ax.set_title(r'Función $\sin(x)$')
```

### Título con múltiples líneas

```python
ax.set_title('Primera línea\nSegunda línea\nTercera línea')
```

### Título con variables

```python
valor_max = 42
ax.set_title(f'Valor máximo: {valor_max}')
```

## Diferencia entre set_title y suptitle

| Método | Ámbito | Ubicación |
|--------|--------|-----------|
| `ax.set_title` | Axes individual | Sobre el axes |
| `fig.suptitle` | Figura completa | Sobre todos los axes |

```python
fig, axs = plt.subplots(2, 2)
fig.suptitle('Título general de la figura')  # una sola vez
axs[0, 0].set_title('Subplot 1')             # por cada axes
axs[0, 1].set_title('Subplot 2')
```

## Buenas prácticas

1. Usar títulos descriptivos y concisos
2. Mantener `fontsize` del título mayor que el de etiquetas de ejes
3. Usar `pad` para evitar solapamiento con elementos superiores (como títulos de otros subplots)
4. Para múltiples subplots, usar `fig.suptitle` para título global y `ax.set_title` para títulos individuales
5. Usar [[LaTeX]] para notación matemática (con `r''` raw string)

## Errores comunes

| Error | Solución |
|-------|----------|
| Título cortado por `tight_layout()` | Aumentar `pad` o ajustar márgenes con `fig.subplots_adjust(top=0.9)` |
| LaTeX no se renderiza | Usar raw string `r'$...$'` y tener LaTeX instalado |
| Confundir `set_title` con `set_xlabel` | `set_title` arriba, `set_xlabel` abajo |
| Título se solapa con otro subplot | Usar `fig.tight_layout(pad=...)` o aumentar `pad` |

## Notas relacionadas

- [[ax.set_xlabel_ylabel]]
- [[fig.suptitle]]
- [[Text]]
- [[LaTeX]]
- [[plt.subplots]]
