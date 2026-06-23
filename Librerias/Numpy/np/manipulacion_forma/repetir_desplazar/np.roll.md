---
title: np.roll — desplaza los elementos circularmente a lo largo de un eje
aliases:
  - roll
  - np.roll
  - desplazamiento circular
tags:
  - numpy
  - api/funcion
  - manipulacion

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_shape
  - concepto_axis_parametro

draft: false
---

# np.roll — desplaza los elementos circularmente a lo largo de un eje

`np.roll` **rota** los elementos `shift` posiciones a lo largo de un eje: lo que sale por un extremo
**reaparece por el otro** (desplazamiento circular, ningún dato se pierde). A diferencia de
[[np.repeat]] y [[np.tile]], no añade ni quita nada: el **shape se conserva exactamente**, solo
cambia la posición de cada elemento.

## La idea en una fórmula

Rodar es **permutar índices módulo el tamaño del eje**. El shape no cambia:

$$ (n_0,\dots,n_{k-1}) \;\xrightarrow{\ \text{roll},\ \text{shift}=s\ }\; (n_0,\dots,n_{k-1}) \qquad (\text{shape conservado}) $$

Por índices, a lo largo de un eje de tamaño $n$, el elemento de la posición de salida $j$ proviene de
la entrada $(j - s) \bmod n$ (con $s>0$ desplazando hacia adelante/derecha):

$$ y_j \;=\; x_{\,(j - s)\bmod n} $$

El `mod` es lo que hace el envoltorio circular. Para `[0, 1, 2, 3, 4]` con `shift=2`:

$$ [\,0,1,2,3,4\,] \;\xrightarrow{\ s=2\ }\; [\,3,4,0,1,2\,] $$

## Firma

```python
np.roll(
    a,             # array_like: el array de entrada
    shift,         # int | tuple[int]: cuántas posiciones desplazar (por eje si es tupla)
    axis=None,     # None | int | tuple[int]: eje(s) del desplazamiento (None aplana primero)
) -> ndarray
```

## Los parámetros en detalle

### `a` — el array de entrada
`array_like` de cualquier dimensión. Se convierte a `ndarray` si no lo es.

### `shift` — cuántas posiciones se rota
El parámetro central. `int` positivo desplaza hacia **adelante** (derecha en el eje, abajo en
`axis=0`); negativo, hacia atrás. Puede ser una **tupla** emparejada con `axis` para rotar varios
ejes a la vez con cuentas distintas.

```python
np.roll(np.arange(5), 2)    # [3, 4, 0, 1, 2]   → +2
np.roll(np.arange(5), -1)   # [1, 2, 3, 4, 0]   → -1
```

### `axis` — a lo largo de qué eje se desplaza
`None` (defecto) **aplana**, desplaza sobre el array 1D y **restaura** el shape original. Un `int`
rota solo ese [[concepto_axis_parametro|eje]]. Una **tupla** rota varios; si `shift` también es tupla,
se emparejan posición a posición.

```python
M = np.arange(6).reshape(2, 3)
np.roll(M, 1, axis=0)            # desplaza filas (envuelve por arriba/abajo)
np.roll(M, 1, axis=1)            # desplaza columnas (envuelve por los lados)
np.roll(M, (1, 1), axis=(0, 1))  # rota ambos ejes a la vez
```

## El caso N-D

La regla: **el shape no cambia nunca**; lo que decide `axis` es *qué* eje rota. Con `axis=None` el
desplazamiento se hace sobre el orden plano (C-contiguo) y luego se reconstruye el shape.

| `a.shape` | `shift` | `axis` | salida | lectura |
|-----------|---------|--------|--------|---------|
| `(n,)` | `s` | `None`/`0` | `(n,)` | rota el vector |
| `(m, n)` | `s` | `0` | `(m, n)` | rota **filas** (vertical) |
| `(m, n)` | `s` | `1` | `(m, n)` | rota **columnas** (horizontal) |
| `(m, n)` | `s` | `None` | `(m, n)` | aplana, rota, restaura |
| `(m, n)` | `(s0, s1)` | `(0, 1)` | `(m, n)` | rota ambos ejes |

```python
T = np.arange(2*3).reshape(2, 3)
np.roll(T, 1, axis=1)
# [[2, 0, 1],
#  [5, 3, 4]]   → cada fila rotada una posición a la derecha, shape (2,3) intacto
```

## Vectorización

`np.roll` reemplaza el bucle con aritmética módulo o el slicing manual con concatenación. La versión
vectorizada calcula el reordenamiento y copia el bloque en C de una vez:

```python
# Slicing manual (1D, equivalente a shift=s):
np.concatenate([a[-s:], a[:-s]])

# Vectorizado, además N-D y con eje:
np.roll(a, s, axis=1)
```

El beneficio de [[concepto_vectorizacion]] aquí no es solo velocidad: `roll` generaliza el envoltorio
a cualquier eje y a varios ejes a la vez sin tener que pensar el slicing índice a índice.

## Valor de retorno

Devuelve un **`ndarray` nuevo** con el **mismo shape y dtype** que `a` (en la implementación actual es
una copia, no una vista). Ningún elemento se pierde ni se rellena.

| Entrada | `axis` | salida (shape) | dtype |
|---------|--------|----------------|-------|
| `(n,)` | cualquiera | `(n,)` | igual que `a` |
| `(m, n)` | `int`/`None`/`tuple` | `(m, n)` | igual que `a` |
| `(d0, d1, d2)` | cualquiera | `(d0, d1, d2)` | igual que `a` |

## Casos de uso

### Diferencia con el vecino (retardo circular)
```python
x = np.array([10, 20, 30, 40])
delta = x - np.roll(x, 1)   # [10-40, 20-10, 30-20, 40-30] = [-30, 10, 10, 10]
# Ojo: el primer valor (-30) es el wrap-around circular, no una diferencia real.
```

### Rotar una señal periódica (desfase)
```python
señal = np.sin(np.linspace(0, 2*np.pi, 100))
desfasada = np.roll(señal, 25)   # desfase de un cuarto de ciclo
```

### Convolución / correlación circular en 2D (N-D)
```python
img = np.arange(3*3).reshape(3, 3)
np.roll(img, (1, -1), axis=(0, 1))   # baja una fila, sube una columna, todo circular
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Se esperaba relleno con ceros | `roll` es circular, no rellena | usar slicing o [[np.pad]] para shift con relleno |
| Matriz aplanada inesperadamente | `axis=None` por defecto | pasar `axis` explícito |
| Sentido del desplazamiento contrario | signo de `shift` | positivo = adelante/derecha/abajo |
| El primer valor de una "diferencia" es absurdo | es el wrap-around | descartar/manejar el borde circular |

## Notas relacionadas

- [[concepto_shape]] — el shape se conserva intacto
- [[concepto_axis_parametro]] — qué eje rota
- [[np.pad]] — desplazar con relleno (no circular)
- [[np.repeat]] · [[np.tile]]
