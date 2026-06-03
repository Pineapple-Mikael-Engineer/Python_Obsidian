---
title: ax.spines — Los 4 bordes del Axes
aliases:
  - spines
  - ax.spines

tags:
  - matplotlib
  - api/atributo
  - formato

# --- Clasificación ---
lib: matplotlib
obj: Axes
tipo: atributo

# --- Comportamiento ---
retorna: Spines
muta_estado: true

draft: false
---

# ax.spines — Los 4 bordes del Axes

## Firma de la función

```python
ax.spines        # atributo, NO método: no se llama con ()
# objeto tipo dict con 4 claves → cada valor es un objeto Spine (un Patch)
ax.spines['top']      # → Spine del borde superior
ax.spines['bottom']   # → Spine del borde inferior
ax.spines['left']     # → Spine del borde izquierdo
ax.spines['right']    # → Spine del borde derecho
```

## Valor de retorno

| Acceso | Retorno | Ejemplo |
|--------|---------|---------|
| `ax.spines` | objeto `Spines` (tipo dict) | contenedor de los 4 bordes |
| `ax.spines['top']` | objeto `Spine` | un borde individual |
| `ax.spines['top'].set_visible(False)` | `None` (muta el Spine) | oculta el borde superior |

```python
print(list(ax.spines))      # → ['left', 'right', 'bottom', 'top']
print(type(ax.spines['left']))   # → <class 'matplotlib.spines.Spine'>
```

## Parámetros en detalle

### Acceso por clave

Los 4 bordes se direccionan como un diccionario: `'top'`, `'bottom'`, `'left'`, `'right'`.

```python
ax.spines['top'].set_visible(False)     # → quita el borde de arriba
ax.spines['right'].set_visible(False)   # → quita el borde de la derecha
```

### set_visible — ocultar bordes

Patrón típico para el estilo "limpio" (solo ejes izquierdo e inferior):

```python
for lado in ('top', 'right'):
    ax.spines[lado].set_visible(False)
# → deja solo bottom y left
```

### set_position — mover un borde

Reubica un Spine respecto a un sistema de referencia.

| Posición | Significado | Ejemplo |
|----------|-------------|---------|
| `('data', v)` | en la coordenada de datos `v` | `set_position(('data', 0))` → en y=0 o x=0 |
| `('axes', f)` | fracción del Axes (0–1) | `set_position(('axes', 0.5))` → centro |
| `'zero'` | atajo de `('data', 0)` | ejes cartesianos clásicos |

```python
# Ejes cruzándose en el origen (estilo cartesiano)
ax.spines['left'].set_position(('data', 0))
ax.spines['bottom'].set_position(('data', 0))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
```

### set_color / set_linewidth — estilo del borde

```python
ax.spines['bottom'].set_color('gray')
ax.spines['bottom'].set_linewidth(2)   # → borde inferior grueso y gris
```

## Casos de uso

```python
# Estilo minimalista
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Caja completa con borde resaltado
for lado in ax.spines:
    ax.spines[lado].set_linewidth(1.5)
```

## Buenas prácticas

1. `ax.spines` es un **atributo**: nunca lo llames con `()`.
2. Itera sobre `('top', 'right')` para ocultar bordes sin repetir código.
3. Usa `set_position(('data', 0))` para gráficas tipo plano cartesiano.
4. Combina con `ax.tick_params` para mover ticks junto con los spines.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `TypeError: not callable` | usar `ax.spines()` con paréntesis | Es atributo: `ax.spines['top']` |
| `KeyError` | clave inválida (`'up'`, `'izq'`) | Solo `'top'`, `'bottom'`, `'left'`, `'right'` |
| Spine sigue visible | olvidar `set_visible(False)` en cada lado | Aplica a cada clave por separado |
| Ticks descolocados al mover spine | ticks no siguen al borde | Ajusta también `ax.xaxis`/`ax.yaxis` o `tick_params` |

Los spines son los 4 bordes del recuadro descritos en el [[concepto_anatomia_figura]], donde cada parte visible recibe un nombre técnico.

## Notas relacionadas

- [[concepto_anatomia_figura]]
- [[ax.tick_params]]
- [[ax.annotate]]
