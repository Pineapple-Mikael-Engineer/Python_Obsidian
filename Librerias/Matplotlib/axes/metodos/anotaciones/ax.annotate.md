---
title: ax.annotate — Anotación con flecha hacia un punto
aliases:
  - annotate
  - ax.annotate

tags:
  - matplotlib
  - api/metodo
  - anotaciones

# --- Clasificación ---
lib: matplotlib
obj: Axes
tipo: metodo

# --- Comportamiento ---
retorna: Annotation
muta_estado: true

draft: false
---

# ax.annotate — Anotación con flecha hacia un punto

## Firma de la función

```python
ax.annotate(text, xy, xytext=None, arrowprops=None, ha='left', va='baseline', **kwargs)
# text       : str                → la cadena de la anotación
# xy         : (float, float)     → punto SEÑALADO (la punta de la flecha)
# xytext     : (float, float)     → posición del TEXTO (la cola de la flecha)
# arrowprops : dict               → estilo de la flecha; si es None, no hay flecha
# → devuelve un objeto Annotation
```

## Valor de retorno

| Entrada | Retorno | Ejemplo |
|---------|---------|---------|
| `ax.annotate("pico", (3, 9))` | `Annotation` (sin flecha) | solo texto en `(3,9)` |
| `ax.annotate(..., xytext=..., arrowprops={...})` | `Annotation` (con flecha) | texto + flecha al punto |

```python
a = ax.annotate("máximo", xy=(3, 9), xytext=(5, 7),
                arrowprops=dict(arrowstyle="->"))
print(type(a))     # → <class 'matplotlib.text.Annotation'>
```

## Parámetros en detalle

### xy — el punto señalado

Coordenada que la flecha **apunta** (la punta). Por defecto en sistema de datos.

```python
ax.annotate("aquí", xy=(3, 9), xytext=(5, 7),
            arrowprops=dict(arrowstyle="->"))
# → punta en (3,9), texto en (5,7)
```

### xytext — posición del texto

Dónde se escribe la cadena (la cola). Si se omite, el texto va en `xy` (sin flecha útil).

### arrowprops — estilo de la flecha

Diccionario que define la flecha. Si es `None`, no se dibuja flecha.

| Clave | Significado | Ejemplo |
|-------|-------------|---------|
| `arrowstyle` | forma de la punta | `"->"`, `"-|>"`, `"fancy"` |
| `color` | color de la flecha | `"red"` |
| `connectionstyle` | curvatura del conector | `"arc3,rad=0.3"` |
| `shrink` | margen en los extremos | `0.05` |

```python
ax.annotate("dato clave",
            xy=(3, 9), xytext=(6, 4),
            arrowprops=dict(arrowstyle="-|>", color="red",
                            connectionstyle="arc3,rad=0.3"))
# → flecha roja curva desde el texto hasta (3,9)
```

### Sistemas de coordenadas independientes

`xycoords` y `textcoords` permiten mezclar sistemas (datos para `xy`, axes-fraction para el texto):

```python
ax.annotate("nota fija", xy=(3, 9), xycoords='data',
            xytext=(0.8, 0.9), textcoords='axes fraction',
            arrowprops=dict(arrowstyle="->"))
```

## Casos de uso

```python
# Señalar el máximo de una curva
ymax = y.max(); xmax = x[y.argmax()]
ax.annotate(f"máx = {ymax:.1f}",
            xy=(xmax, ymax), xytext=(xmax+1, ymax-2),
            arrowprops=dict(arrowstyle="->"))

# Anotación sin flecha (equivale a ax.text)
ax.annotate("solo texto", xy=(2, 2))
```

## Buenas prácticas

1. Usa `ax.annotate` (no `ax.text`) cuando necesites **señalar** un punto concreto.
2. Separa `xytext` lo suficiente de `xy` para que la flecha sea legible.
3. `connectionstyle="arc3,rad=..."` evita que la flecha cruce los datos.
4. Mezcla `xycoords='data'` con `textcoords='axes fraction'` para fijar el texto en una esquina.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| No aparece flecha | falta `arrowprops` | Pasa `arrowprops=dict(arrowstyle="->")` |
| Flecha invertida | se confunde `xy` con `xytext` | `xy` = punta señalada; `xytext` = texto |
| Texto sobre el punto | `xytext` igual o cercano a `xy` | Aleja `xytext` del punto |
| `KeyError` en arrowprops | clave inválida (p.ej. `style`) | Usa `arrowstyle`, `color`, `connectionstyle` |

Cada elemento señalado pertenece a la región de ploteo del [[concepto_anatomia_figura]]; conocer su nombre ayuda a decidir qué anotar.

## Notas relacionadas

- [[ax.text]]
- [[concepto_anatomia_figura]]
- [[ax.spines]]
