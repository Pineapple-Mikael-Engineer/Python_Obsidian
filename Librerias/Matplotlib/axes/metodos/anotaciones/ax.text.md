---
title: ax.text — Coloca texto en coordenadas de datos
aliases:
  - text
  - ax.text

tags:
  - matplotlib
  - api/metodo
  - anotaciones

# --- Clasificación ---
lib: matplotlib
obj: Axes
tipo: metodo

# --- Comportamiento ---
retorna: Text
muta_estado: true

draft: false
---

# ax.text — Coloca texto en coordenadas de datos

## Firma de la función

```python
ax.text(x, y, s, fontsize=None, color=None, ha='left', va='baseline', **kwargs)
# x, y : float        → posición en coordenadas de DATOS (mismo sistema que los puntos)
# s    : str          → la cadena a dibujar
# ha   : str          → horizontal alignment: 'left' | 'center' | 'right'
# va   : str          → vertical alignment:   'top' | 'center' | 'bottom' | 'baseline'
# → devuelve un objeto Text
```

## Valor de retorno

| Entrada | Retorno | Ejemplo |
|---------|---------|---------|
| `ax.text(1, 2, "hola")` | objeto `Text` | `t = ax.text(1, 2, "hola")` |
| `Text` mutable después | sí, vía setters | `t.set_color("red")` |

```python
t = ax.text(0.5, 0.5, "etiqueta")
t.set_fontsize(14)          # → modifica el Text ya dibujado
print(type(t))              # → <class 'matplotlib.text.Text'>
```

## Parámetros en detalle

### x, y — coordenadas de datos

Por defecto se interpretan en el sistema de **datos** del Axes, igual que cualquier punto ploteado.

```python
ax.plot([0, 10], [0, 100])
ax.text(5, 50, "centro")     # → en x=5, y=50 del eje
```

Para usar coordenadas relativas al Axes (0–1), pasa `transform=ax.transAxes`:

```python
ax.text(0.95, 0.95, "esquina", transform=ax.transAxes, ha='right', va='top')
# → siempre arriba-derecha sin importar los límites de datos
```

### s — la cadena

Admite LaTeX matemático entre `$...$`:

```python
ax.text(1, 1, r"$\alpha = \frac{1}{2}$")   # → renderiza la fórmula
```

### ha / va — alineación

| Parámetro | Valores | Punto de anclaje |
|-----------|---------|------------------|
| `ha` | `'left'`, `'center'`, `'right'` | borde horizontal del texto |
| `va` | `'top'`, `'center'`, `'bottom'`, `'baseline'` | borde vertical del texto |

```python
ax.text(5, 50, "centrado", ha='center', va='center')   # → (5,50) al centro del texto
```

## Casos de uso

```python
# Etiquetar el valor de un punto
ax.plot([3], [9], 'o')
ax.text(3, 9, "  (3, 9)", va='center')      # → texto a la derecha del marcador

# Caja de fondo para legibilidad
ax.text(0.5, 0.5, "nota", bbox=dict(facecolor='yellow', alpha=0.5))
```

## Buenas prácticas

1. Para señalar con flecha usa `ax.annotate`; `ax.text` es solo texto plano.
2. Usa `transform=ax.transAxes` para posiciones fijas (esquinas, títulos internos).
3. Centra con `ha='center', va='center'` cuando el punto es el centro lógico.
4. Añade `bbox=` cuando el texto cae sobre datos densos.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Texto fuera de vista | `x, y` fuera de los límites de datos | Ajusta `set_xlim`/`set_ylim` o usa `transAxes` |
| Texto desalineado del punto | `ha`/`va` por defecto (`left`/`baseline`) | Define `ha='center', va='center'` |
| `$...$` muestra literal | falta el prefijo `r` en la cadena | Usa `r"$...$"` (raw string) |
| Se solapa con datos | sin fondo | Añade `bbox=dict(facecolor='white')` |

El texto se coloca sobre la región de ploteo descrita en [[concepto_anatomia_figura]], que distingue cada parte visible del gráfico.

## Notas relacionadas

- [[ax.annotate]]
- [[concepto_anatomia_figura]]
- [[ax.set_title]]
