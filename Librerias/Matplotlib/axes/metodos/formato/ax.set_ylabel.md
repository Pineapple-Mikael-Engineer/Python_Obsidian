---
title: ax.set_ylabel — Etiqueta del eje Y
aliases:
  - set_ylabel
  - etiqueta eje y
  - ylabel
tags:
  - matplotlib
  - api/metodo
  - axes/formato
lib: matplotlib
obj: Axes
tipo: metodo
retorna: Text
muta_estado: true
draft: false
---

# ax.set_ylabel — Etiqueta del eje Y

## Firma

```python
Axes.set_ylabel(
    ylabel,
    fontdict=None,
    labelpad=None,
    loc='center',
    **kwargs
)
```

## Parámetros

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `ylabel` | `str` | - | Texto de la etiqueta |
| `fontdict` | `dict` | `None` | Diccionario de propiedades de fuente |
| `labelpad` | `float` | `None` | Espacio entre etiqueta y eje (puntos) |
| `loc` | `str` | `'center'` | Posición: `'bottom'`, `'center'`, `'top'` |
| `**kwargs` | - | - | Propiedades de [[Text]] (color, size, weight, etc.) |

## Valor de retorno

Retorna el objeto [[Text]] creado, permitiendo modificaciones posteriores.

```python
text_obj = ax.set_ylabel('Amplitud')
text_obj.set_color('blue')
```

## Posiciones disponibles (loc)

| Valor | Posición |
|-------|----------|
| `'bottom'` | Abajo |
| `'center'` | Centro (default) |
| `'top'` | Arriba |

```python
ax.set_ylabel('Amplitud', loc='top')
```

## Parámetros de fuente (kwargs)

Los argumentos adicionales se pasan al objeto [[Text]] interno.

| Parámetro | Ejemplo | Descripción |
|-----------|---------|-------------|
| `fontsize` | `fontsize=12` | Tamaño de fuente |
| `fontweight` | `fontweight='bold'` | Grosor ('normal', 'bold') |
| `fontstyle` | `fontstyle='italic'` | Estilo ('normal', 'italic') |
| `color` | `color='red'` | Color del texto |
| `backgroundcolor` | `backgroundcolor='yellow'` | Color de fondo |
| `rotation` | `rotation=45` | Rotación en grados |
| `alpha` | `alpha=0.7` | Transparencia |

```python
ax.set_ylabel('Amplitud', fontsize=14, fontweight='bold', color='darkgreen')
```

## Uso de fontdict

`fontdict` agrupa propiedades de fuente en un diccionario:

```python
font = {'family': 'serif', 'color': 'darkred', 'weight': 'normal', 'size': 12}
ax.set_ylabel('Amplitud', fontdict=font)
```

## labelpad — espaciado

Controla la distancia entre la etiqueta y el eje (en puntos).

```python
ax.set_ylabel('Eje Y', labelpad=15)
```

## Casos comunes

### Etiquetas con unidades

```python
ax.set_ylabel('Velocidad (m/s)')
```

### Etiquetas con formato matemático (LaTeX)

```python
ax.set_ylabel(r'$\sin(\theta)$')
```

### Rotación de etiqueta (útil para ejes Y largos)

```python
ax.set_ylabel('Variable muy larga que ocupa espacio', rotation=0, labelpad=20)
# rotation=0 horizontal, rotation=90 vertical (default)
```

### Múltiples líneas

```python
ax.set_ylabel('Primera línea\nSegunda línea')
```

### Ocultar etiqueta

```python
ax.set_ylabel('')  # o simplemente no llamar al método
```

## Relación con otros métodos

| Método | Ámbito |
|--------|--------|
| `ax.set_ylabel` | Etiqueta del eje Y |
| `ax.set_xlabel` | Etiqueta del eje X |
| [[ax.set_title]] | Título del axes |
| [[fig.suptitle]] | Título de la figura |
| [[ax.set_yticklabels]] | Etiquetas de ticks |

## Buenas prácticas

1. Usar nombres descriptivos con unidades cuando corresponda
2. Mantener `fontsize` consistente entre etiquetas y títulos
3. Usar `labelpad` para evitar solapamiento con ticks largos
4. Para etiquetas Y largas, considerar `rotation=0` y ajustar con `labelpad`
5. Usar [[LaTeX]] para notación matemática (con `r''` raw string)

## Errores comunes

| Error | Solución |
|-------|----------|
| Etiqueta cortada en el borde | Usar `fig.tight_layout()` o aumentar `labelpad` |
| LaTeX no se renderiza | Usar raw string `r'$...$'` y tener LaTeX instalado |
| Confundir `set_ylabel` con `set_title` | `set_ylabel` para eje vertical, `set_title` para título superior |
| Olvidar que `**kwargs` pasa a [[Text]] | Revisar documentación de Text para opciones avanzadas |

## Notas relacionadas

- [[ax.set_xlabel]]
- [[ax.set_title]]
- [[fig.suptitle]]
- [[ax.set_yticklabels]]
- [[Text]]
- [[LaTeX]]
