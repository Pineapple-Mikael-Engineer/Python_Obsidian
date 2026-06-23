---
title: Vectorizacion — Operaciones sin bucles explicitos
aliases:
  - vectorization
  - codigo vectorizado
tags:
  - numpy
  - concepto
  - rendimiento
lib: numpy
tipo: concepto
requiere:
  - concepto_ndarray
  - concepto_broadcasting
  - concepto_ufuncs
draft: false
---

# Vectorización — Operaciones sin bucles explícitos

## Definición fundamental

**Vectorización** es operar sobre [[concepto_ndarray|arrays]] enteros en lugar de iterar elemento a elemento en Python. Una expresión como `a + b` no recorre los elementos en el intérprete: describe la operación sobre **todo el array** y deja que NumPy la ejecute de golpe.

La idea es **dejar de pensar en índices y empezar a pensar en shapes y ejes**. En código vectorizado no hay un `for i in range(...)` visible; hay una expresión que se lee como una fórmula matemática.

## La regla / el modelo central

> El bucle no desaparece: **se traslada a C**. La expresión NumPy ejecuta el mismo recorrido elemento a elemento, pero en un bucle compilado, sin overhead del intérprete y sin *boxing* de cada valor.

Un bucle Python paga, **en cada iteración**, un coste que el bucle en C no paga:

| Coste por iteración | Bucle Python | Bucle en C (NumPy) |
|---------------------|--------------|--------------------|
| Comprobación de tipo | sí, cada vez | una sola vez, al inicio |
| *Boxing*/objeto Python por elemento | sí | no, datos crudos contiguos |
| Despacho del intérprete (bytecode) | sí | no, código máquina |
| Acceso a memoria | indirecto, disperso | contiguo, *cache-friendly* |

Eso es todo el modelo: **misma cantidad de operaciones, distinto motor**. El motor interno son las [[concepto_ufuncs|ufuncs]], que aplican la operación sobre el buffer de memoria sin volver al intérprete.

## El contraste: bucle Python vs expresión NumPy

El corazón de la nota. La misma operación, lado a lado, en tres niveles crecientes.

### Nivel 1: sumar dos arrays

```python
import numpy as np
a = np.arange(1_000_000)
b = np.arange(1_000_000)
```

```python
# Bucle Python                      # Expresión NumPy
c = np.empty_like(a)                c = a + b
for i in range(len(a)):
    c[i] = a[i] + b[i]
```

El bucle entra y sale del intérprete un millón de veces; `a + b` hace **una** llamada que recorre el buffer en C.

### Nivel 2: normalizar cada fila por su suma

```python
M = np.random.rand(1000, 50)
```

```python
# Bucle Python                          # Expresión NumPy
out = np.empty_like(M)                  sumas = M.sum(axis=1, keepdims=True)  # (1000, 1)
for i in range(M.shape[0]):             out = M / sumas                       # broadcasting
    fila = M[i]
    out[i] = fila / fila.sum()
```

La versión vectorizada piensa en **ejes**: reduce a lo largo de `axis=1` con `keepdims` para conservar la forma `(1000, 1)` y deja que [[concepto_broadcasting|broadcasting]] alinee la división. No hay índice de fila por ningún lado.

### Nivel 3: una operación N-D sobre un lote

Distancia al cuadrado de cada vector de un lote `(b, n)` a un centroide `(n,)`, sin bucle sobre el lote:

```python
lote = np.random.rand(128, 64)     # (b, n) = 128 vectores de dimensión 64
centro = np.random.rand(64)        # (n,)
```

```python
# Bucle Python                              # Expresión NumPy
d = np.empty(lote.shape[0])                 dif = lote - centro            # (128,64) broadcasting
for i in range(lote.shape[0]):              d = (dif ** 2).sum(axis=1)     # reduce el eje n → (128,)
    dif = lote[i] - centro
    d[i] = (dif ** 2).sum()
```

`lote - centro` alinea el `(64,)` del centro contra el último eje del lote por broadcasting; la reducción `sum(axis=1)` colapsa el eje de la dimensión y deja un resultado `(128,)`, **un escalar por vector del lote**. El `for i in range(b)` se ha disuelto en la elección del `axis`.

## Cómo pensar vectorizado

1. **En shapes, no en índices.** En vez de "para cada fila `i`...", pregunta "¿qué eje quiero reducir y qué eje quiero conservar?".
2. **Alinear ejes** es trabajo de [[concepto_broadcasting|broadcasting]]: insertar un eje de tamaño 1 (`keepdims=True`, `np.newaxis`) suele bastar para que dos arrays operen sin bucle.
3. **El motor son las ufuncs.** `a + b`, `np.sin(a)`, `a > 0` son ufuncs; conocerlas evita reinventar bucles.

```python
# Estas operaciones son ufuncs aplicadas sobre todo el array
a + 1        # np.add
a * 2        # np.multiply
np.sin(a)    # np.sin
a > 0.5      # np.greater
```

## Lo que NO se vectoriza directamente (y cómo manejarlo)

### Caso 1: dependencias secuenciales

Cada paso depende del anterior; no hay paralelismo elemento a elemento. La salida es una **función acumulativa**, no un bucle.

```python
# NO vectorizable como suma directa
arr = np.array([1, 2, 3, 4])
# arr[i] = arr[i-1] + arr[i]  ← depende del valor ya actualizado

# Alternativa vectorizada: cumsum recorre la dependencia en C
np.cumsum(arr)   # [1, 3, 6, 10]
```

### Caso 2: condiciones con ramificación

Un `if/elif/else` por elemento se traduce a `np.where` (o máscaras booleanas), no a un bucle:

```python
# Vectorizado con np.where
resultado = np.where(arr < 0, 0,
              np.where(arr < 0.5, arr * 2, arr))
```

### Caso 3: funciones escalares y el espejismo de `np.vectorize`

`np.vectorize` **no acelera**: es azúcar sintáctico que sigue ejecutando el bucle en Python por dentro. Sirve para comodidad de la firma, no para rendimiento.

```python
def f(x):
    return x ** 2 if x > 0 else 0

# np.vectorize NO es más rápido que un bucle: el for sigue en Python
f_vec = np.vectorize(f)
resultado = f_vec(arr)

# Mejor: reescribir de forma genuinamente vectorizada
resultado = np.where(arr > 0, arr ** 2, 0)
```

## Casos que fallan (errores típicos)

### Error 1: dejar un bucle Python innecesario

```python
# Lento: list comprehension sobre el array (sigue siendo Python puro)
resultado = np.array([x * 2 for x in arr])

# Vectorizado de verdad
resultado = arr * 2
```

### Error 2: romper la vectorización con `.tolist()`

Convertir a lista saca los datos del buffer de C y vuelve al mundo de objetos Python; cualquier operación posterior pierde toda la ventaja.

```python
datos = arr.tolist()                 # ahora son ints/floats de Python, no un buffer
resultado = [x * 2 for x in datos]   # bucle Python, boxing por elemento → lento
```

### Error 3: olvidar que las reducciones cambian la dimensión

```python
arr = np.array([[1, 2, 3],
                [4, 5, 6]])

np.sum(arr)                       # escalar 0-D
np.sum(arr, axis=1)               # vector (2,)
np.sum(arr, axis=1, keepdims=True)  # (2, 1)  → conserva el eje para broadcasting
```

Ver [[concepto_axis_parametro|axis]] para el detalle de qué eje desaparece.

## Relación con otros conceptos

- [[concepto_ndarray]]
- [[concepto_broadcasting]]
- [[concepto_ufuncs]]
- [[concepto_axis_parametro]]
- [[concepto_views_vs_copias]]
- [[np.where]]
- [[np.vectorize]]
