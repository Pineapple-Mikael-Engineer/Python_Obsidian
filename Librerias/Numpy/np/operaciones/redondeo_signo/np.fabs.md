---
title: np.fabs — valor absoluto en float (solo reales, ufunc)
aliases:
  - fabs
  - np.fabs
tags:
  - numpy
  - api/funcion
  - transformaciones

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_ufuncs
  - concepto_vectorizacion

draft: false
---

# np.fabs — valor absoluto en float (solo reales, ufunc)

`np.fabs` es una **ufunc unaria**: aplica el valor absoluto $|x_i|$ a cada elemento, **sin cambiar el
shape**. Su rasgo distintivo frente a [[np.abs]] es doble: **siempre devuelve `float`** (aunque la
entrada sea entera) y **no acepta números complejos** (lanza `TypeError`). Mapea directamente a la
función `fabs` de C. Úsala cuando quieras **garantizar salida flotante** trabajando solo con reales; usa
`np.abs` si necesitas conservar el dtype entero o soportar complejos (donde devuelve el módulo).

## La idea en una fórmula

Cada elemento se transforma de forma independiente; el shape se **conserva**:

$$
z_i = |x_i| \in \mathbb{R}_{\ge 0} \qquad (n_0,\dots,n_k)\ \xrightarrow{\ \text{fabs}\ }\ (n_0,\dots,n_k)
$$

con la garantía añadida de que $z_i$ es **siempre un flotante** y que $x_i$ debe ser **real** (no
complejo). Matemáticamente es el mismo $|x|$ que `np.abs`; la diferencia está en el tipo y el dominio.

## Firma

```python
np.fabs(
    x,                 # array_like: el tensor de entrada (solo real)
    /,
    out=None,          # ndarray | None: destino preasignado
    *,
    where=True,        # array_like[bool]: máscara de cómputo
    casting='same_kind',  # política de conversión de tipos
    order='K',         # 'K' | 'C' | 'F' | 'A': layout de memoria del resultado
    dtype=None,        # dtype: fuerza el tipo (flotante) de cómputo/salida
) -> ndarray
```

## Los parámetros en detalle

### `x` — el tensor de entrada
`array_like` **real** (ndarray, lista, escalar). Los enteros y booleanos se convierten a float. **No
acepta complejos**: con `complex` lanza `TypeError` (esta es la diferencia clave con `np.abs`). El shape
de salida es el de `x`.

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape de salida. Evita asignar memoria; permite in-place
(`np.fabs(arr, out=arr)`). El dtype debe ser flotante y compatible bajo `casting`.

### `where` — máscara de cómputo
`array_like` booleano broadcasteable con `x`. Solo calcula `|x_i|` donde es `True`; donde es `False`,
conserva el valor previo de `out` (basura si no se pasó `out`). Va casi siempre con `out`.

### `dtype` — tipo de cómputo y salida
Fuerza el tipo flotante de cálculo/salida (`float32`, `float64`). No puede dar un entero: la salida es
flotante por definición.

### `casting` — política de conversión
`'no'`, `'equiv'`, `'safe'`, `'same_kind'` (defecto), `'unsafe'`. Controla qué conversiones se permiten al
escribir en `out` o aplicar `dtype`.

### `order` — layout de memoria
`'K'` (defecto), `'C'`, `'F'`, `'A'`. Solo afecta al almacenamiento del resultado, no a sus valores.

## El caso N-D

`np.fabs` se aplica **elemento a elemento** sobre cualquier dimensión: no hay `axis`, no colapsa nada,
**conserva el shape**. Un tensor `(d0, d1, d2)` entra y sale como `(d0, d1, d2)`, todo en float:

```python
T = np.array([[[-1, 2], [-3, 4]],
              [[ 5,-6], [ 7,-8]]])   # shape (2, 2, 2), enteros
np.fabs(T).shape       # (2, 2, 2)  → shape idéntico
np.fabs(T).dtype       # float64    → siempre flotante
np.fabs(T)
# [[[1., 2.], [3., 4.]],
#  [[5., 6.], [7., 8.]]]
```

## Vectorización

`np.fabs` reemplaza un bucle que llamaría a `math.fabs` por elemento. La versión vectorizada corre el
bucle en C, sobre memoria contigua:

```python
import math
# Bucle Python (lento):
out = np.empty(arr.size, dtype=float)
for i in range(arr.size):
    out[i] = math.fabs(arr.flat[i])

# ufunc (un único bucle en C):
out = np.fabs(arr)
```

Es el principio de [[concepto_vectorizacion]]. Soporta `out`/`where` como toda ufunc.

## Valor de retorno

`ndarray` (o escalar de NumPy si la entrada es escalar) con el **mismo shape** que `x` y dtype
**siempre flotante**:

| Entrada (`x`) | dtype salida | nota |
|---------------|--------------|------|
| entero (`int64`...) | `float64` | **promueve a float** (a diferencia de `np.abs`, que conservaría int) |
| `float32` | `float32` | conserva la precisión |
| `float64` | `float64` | |
| **complejo** | — | **`TypeError`**: no soportado |

```python
np.fabs([-1, -2, 3])           # array([1., 2., 3.])   → float, no int
np.fabs(np.array([-1, 2])).dtype  # float64
np.fabs(3 + 4j)                # TypeError              → usa np.abs para complejos
```

## Casos de uso

### Forzar salida flotante sin castear aparte
```python
enteros = np.array([-3, 5, -7])
np.fabs(enteros)     # array([3., 5., 7.])  ya en float, listo para dividir
```

### fabs vs abs (cuándo cada una)
```python
np.abs(np.array([-2, 3])).dtype    # int64    conserva el entero
np.fabs(np.array([-2, 3])).dtype   # float64  garantiza float
np.abs(3 + 4j)                     # 5.0      módulo del complejo
np.fabs(3 + 4j)                    # TypeError no acepta complejos
```
Usa `np.fabs` cuando: trabajas solo con reales **y** quieres asegurar float (p. ej. antes de divisiones
o de pasar a una API que espera flotantes). Usa `np.abs` cuando: necesitas conservar el dtype entero, o
trabajas con complejos (módulo).

### N-D: magnitud flotante de un tensor
```python
campo = np.array([[[-1, 2], [-3, 4]],
                  [[ 5,-6], [ 7,-8]]])   # (2, 2, 2)
np.fabs(campo)        # mismo shape, todo positivo y en float
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `TypeError` con complejos | `fabs` no acepta complejos | usar [[np.abs]] (devuelve el módulo) |
| Esperar enteros y recibir float | `fabs` siempre promueve a float | usar [[np.abs]] si quieres conservar int |
| Posiciones con basura tras `where` | `where=` sin `out` inicializado | pasar siempre `out=` junto con `where=` |

## Notas relacionadas

- [[concepto_ufuncs]] — `np.fabs` es una ufunc unaria; hereda `out`/`where`/`dtype`/`casting`
- [[concepto_vectorizacion]] — por qué sustituye al bucle por elemento
- [[np.abs]] — variante general: conserva dtype y soporta complejos (módulo)
- [[np.sign]] · [[np.absolute]]
