---
title: ax.set_ylim — Límites visibles del eje Y
aliases:
  - set_ylim
  - ax.set_ylim
tags:
  - matplotlib
  - api/metodo
  - formato

# --- Clasificación ---
lib: matplotlib
obj: Axes
tipo: metodo

# --- Comportamiento ---
retorna: tuple (bottom, top)
muta_estado: true

draft: false
---

# ax.set_ylim — Límites visibles del eje Y

Fija el rango de datos visible en el eje vertical del Axes. Es la versión vertical de `set_xlim`: con ella se hace *zoom* en altura, se ancla el origen en cero o se invierte el eje (por ejemplo para representar profundidad). Sin él, los límites del eje Y se autoescalan a partir de los datos.

## Firma de la función

```python
Axes.set_ylim(
    bottom=None,
    top=None,
    *,
    emit=True,
    auto=False,
    ymin=None,
    ymax=None
)
```

## Valor de retorno

Devuelve la tupla `(bottom, top)` con los límites efectivamente aplicados, ya resueltos. Es un método que muta el estado del Axes; el retorno suele descartarse.

| Entrada | Retorno | Ejemplo |
|---------|---------|---------|
| `set_ylim(0, 100)` | `(0.0, 100.0)` | rango fijo ascendente |
| `set_ylim(100, 0)` | `(100.0, 0.0)` | eje invertido (decreciente hacia arriba) |
| `set_ylim(bottom=0)` | `(0.0, <auto>)` | solo borde inferior, superior autoescala |
| `set_ylim()` | `(<auto>, <auto>)` | sin cambios, devuelve límites actuales |

```python
lims = ax.set_ylim(0, 1)
print(lims)   # → (0.0, 1.0)
```

## Formas básicas de llamada

| Llamada | Efecto |
|---------|--------|
| `ax.set_ylim(0, 100)` | posicional: `bottom=0`, `top=100` |
| `ax.set_ylim((0, 100))` | acepta una tupla/lista como primer argumento |
| `ax.set_ylim(top=100)` | fija solo el borde superior |
| `ax.set_ylim(bottom=None, top=None)` | ambos `None` → autoescala completa |

## Parámetros en detalle

### bottom

Valor de datos en el borde inferior del eje. Si es `None`, ese borde autoescala.

```python
ax.set_ylim(bottom=0)   # ancla el suelo en y=0, techo automático
```

### top

Valor de datos en el borde superior. Si `top < bottom`, el eje queda **invertido** (los valores decrecen hacia arriba), patrón habitual para profundidad o ranking.

```python
ax.set_ylim(0, 100)     # normal
ax.set_ylim(100, 0)     # invertido (0 arriba, 100 abajo)
```

### ymin / ymax

Alias legado de `bottom` / `top`. No se pueden combinar con sus equivalentes posicionales.

| Forma moderna | Alias legado |
|---------------|--------------|
| `bottom` | `ymin` |
| `top` | `ymax` |

### auto

`True` reactiva el autoescalado del eje Y para el borde no especificado.

## Casos de uso

### Fijar una escala de porcentaje 0–100

```python
ax.plot(x, porcentaje)
ax.set_ylim(0, 100)     # rango comparable entre gráficos
```

### Invertir el eje para representar profundidad

```python
ax.plot(temperatura, profundidad)
ax.set_ylim(top=0)      # superficie (0) arriba
ax.set_ylim(bottom=500) # 500 m abajo
```

### Anclar el suelo en cero sin tocar el techo

```python
ax.bar(categorias, valores)
ax.set_ylim(bottom=0)
```

## Buenas prácticas

1. Aplicar `set_ylim` **después** de dibujar para que el autoescalado no lo sobrescriba.
2. Para invertir el eje, `set_ylim(top, bottom)` es más legible que mezclar argumentos; `ax.invert_yaxis()` es la alternativa explícita.
3. Igualar `set_ylim` entre subgráficos para comparaciones justas.
4. Para leer el rango sin modificarlo, usar `ax.get_ylim()`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| El límite no se aplica | Datos dibujados tras `set_ylim` | Fijar los límites al final |
| `TypeError` por `ymin` y `bottom` | Alias y nombre nuevo a la vez | Usar solo uno |
| Eje invertido inesperado | `bottom > top` | Revisar el orden de los argumentos |
| Barras flotando sobre el eje | Falta anclar el suelo | `ax.set_ylim(bottom=0)` |

## Notas relacionadas

El equivalente en `pyplot` es `plt.ylim()`, que actúa sobre el Axes activo (ver [[concepto_pyplot_vs_oo]]). Junto con su par horizontal, define la sección *limits* de la [[concepto_anatomia_figura]].

- [[ax.set_xlim]]
- [[ax.set_yscale]]
- [[concepto_anatomia_figura]]
- [[concepto_pyplot_vs_oo]]
