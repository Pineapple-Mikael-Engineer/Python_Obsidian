---
title: ax.set_xlim — Límites visibles del eje X
aliases:
  - set_xlim
  - ax.set_xlim
tags:
  - matplotlib
  - api/metodo
  - formato

# --- Clasificación ---
lib: matplotlib
obj: Axes
tipo: metodo

# --- Comportamiento ---
retorna: tuple (left, right)
muta_estado: true

draft: false
---

# ax.set_xlim — Límites visibles del eje X

Fija el rango de datos visible en el eje horizontal del Axes. Es el método con el que se hace *zoom* manual sobre una región, se fuerza un origen en cero o se recorta una serie. Sin él, Matplotlib autoescala los límites a partir de los datos dibujados.

## Firma de la función

```python
Axes.set_xlim(
    left=None,
    right=None,
    *,
    emit=True,
    auto=False,
    xmin=None,
    xmax=None
)
```

## Valor de retorno

Devuelve la tupla `(left, right)` con los límites efectivamente aplicados, ya resueltos (sin `None`). Es un método que **muta el estado** del Axes; el retorno es secundario y rara vez se usa.

| Entrada | Retorno | Ejemplo |
|---------|---------|---------|
| `set_xlim(0, 10)` | `(0.0, 10.0)` | rango fijo ascendente |
| `set_xlim(10, 0)` | `(10.0, 0.0)` | eje invertido (decreciente) |
| `set_xlim(left=5)` | `(5.0, <auto>)` | solo borde izquierdo, derecho autoescala |
| `set_xlim()` | `(<auto>, <auto>)` | sin cambios, devuelve límites actuales |

```python
lims = ax.set_xlim(0, 100)
print(lims)   # → (0.0, 100.0)
```

## Formas básicas de llamada

| Llamada | Efecto |
|---------|--------|
| `ax.set_xlim(0, 10)` | posicional: `left=0`, `right=10` |
| `ax.set_xlim((0, 10))` | acepta una tupla/lista como primer argumento |
| `ax.set_xlim(right=10)` | fija solo el borde derecho |
| `ax.set_xlim(left=None, right=None)` | ambos `None` → autoescala completa |

## Parámetros en detalle

### left

Valor de datos en el borde izquierdo del eje. Si es `None`, ese borde se deja autoescalar.

```python
ax.set_xlim(left=0)   # ancla el origen en x=0, derecha automática
```

### right

Valor de datos en el borde derecho. Si `right < left`, el eje queda **invertido** (los valores decrecen hacia la derecha).

```python
ax.set_xlim(0, 10)    # normal
ax.set_xlim(10, 0)    # invertido
```

### xmin / xmax

Alias de `left` / `right`. No se pueden mezclar con sus equivalentes posicionales (lanza error).

| Forma moderna | Alias legado |
|---------------|--------------|
| `left` | `xmin` |
| `right` | `xmax` |

### auto

`True` reactiva el autoescalado del eje X tras fijar el límite que no se haya pasado.

## Casos de uso

### Zoom a una región de interés

```python
ax.plot(x, y)
ax.set_xlim(2.0, 4.0)   # solo se ve el tramo [2, 4]
```

### Forzar origen en cero

```python
ax.bar(categorias, valores)
ax.set_xlim(left=0)     # barras desde 0, sin margen izquierdo
```

### Invertir el eje (p. ej. profundidad o longitud de onda)

```python
ax.set_xlim(700, 400)   # 700 a la izquierda, 400 a la derecha
```

## Buenas prácticas

1. Llamar a `set_xlim` **después** de dibujar los datos; antes, el autoescalado posterior puede sobrescribir el límite.
2. Para invertir un eje, preferir `set_xlim(max, min)` por claridad; `ax.invert_xaxis()` es la alternativa explícita.
3. Pasar solo el borde que interesa (`left=` o `right=`) y dejar que el otro autoescale.
4. Si necesitas el rango actual sin modificarlo, usa `ax.get_xlim()` en vez de llamar a `set_xlim()` sin argumentos.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| El límite se ignora | Se dibujaron datos *después* de `set_xlim` | Fijar los límites al final, tras los `plot` |
| `TypeError` por `xmin` y `left` juntos | Se mezcló alias y nombre nuevo | Usar solo uno de los dos |
| Eje sale invertido sin querer | `left > right` | Verificar el orden de los argumentos |
| Margen vacío a un lado | Otro `plot` reactivó el autoescalado | Volver a fijar o usar `ax.margins(0)` |

## Notas relacionadas

El equivalente en la interfaz `pyplot` es `plt.xlim()`, que opera sobre el Axes activo (ver [[concepto_pyplot_vs_oo]]). Conceptualmente, este método controla la sección *limits* dentro de la [[concepto_anatomia_figura]].

- [[ax.set_ylim]]
- [[ax.set_xscale]]
- [[concepto_anatomia_figura]]
- [[concepto_pyplot_vs_oo]]
