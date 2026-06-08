---
title: np.linalg — productos matriciales
tags:
  - numpy
  - indice
draft: false
---

# np.linalg — productos matriciales

Multiplicacion matricial y operaciones de potencia. La multiplicacion matricial en NumPy moderno se hace con el operador `@` (desde Python 3.5); estas funciones existen para casos especiales o cuando se necesitan parametros extra.

## Funciones

| Funcion | Que calcula | Caso tipico |
|---|---|---|
| [[np.linalg.dot]] | Producto punto (vectores) o producto matricial (2D+) | Producto de dos arrays |
| [[np.linalg.multi_dot]] | Cadena de productos con orden optimo automatico | Tres o mas matrices |
| [[np.linalg.matrix_power]] | Potencia entera de una matriz cuadrada (A^n) | A^n con n entero (positivo, cero o negativo) |
| [[np.linalg.matrix_transpose]] | Transpuesta de las ultimas dos dimensiones de un array N-D | Equivalente a `.T`, disponible desde NumPy 2.0 |

## Descripcion de cada funcion

**`np.linalg.dot(a, b)`** — producto punto para vectores, producto matricial para 2D, y contraccion del ultimo eje con el penultimo para N-D. Historicamente era la forma principal; hoy se prefiere `@` o `np.matmul` por claridad. Para 1D calcula el producto escalar.

**`np.linalg.multi_dot(arrays)`** — cadena de productos matriciales con optimizacion automatica del orden de evaluacion. `np.multi_dot([A, B, C, D])` es potencialmente mucho mas rapido que `A @ B @ C @ D` si las matrices tienen shapes muy diferentes, porque elige el parentesado de menor coste.

**`np.linalg.matrix_power(m, n)`** — eleva una matriz cuadrada a la potencia entera `n`. Para n negativo calcula `inv(m)^|n|`. Para n=0 devuelve la identidad.

**`np.linalg.matrix_transpose(x)`** — transpuesta de las ultimas dos dimensiones de un array N-D (util para batches de matrices). Disponible desde NumPy 2.0; para uso simple preferir `.T` o `np.transpose`.

## Nota sobre `@` vs `np.dot`

Desde Python 3.5+, el operador `@` es el modo preferido para productos matriciales:

```python
C = A @ B        # preferido
C = np.dot(A, B) # equivalente, pero mas verboso
```

`np.dot` sigue siendo util en contextos donde se pasa la funcion como callable o para arrays de dimension 1 (producto escalar).

## Cuando usar cada funcion

| Necesito... | Funcion |
|---|---|
| Producto de dos matrices o vectores | `@` o [[np.linalg.dot]] |
| Producto de cadena A @ B @ C @ ... (eficiencia) | [[np.linalg.multi_dot]] |
| Elevar una matriz a la potencia n | [[np.linalg.matrix_power]] |
| Transponer por ejes (en lotes de matrices) | [[np.linalg.matrix_transpose]] o `.T` |

## `multi_dot`: optimizacion automatica

`multi_dot` elige el orden de agrupacion que minimiza el numero de operaciones escalares (algoritmo de parentizacion optima). Para cadenas largas esto puede ser significativamente mas rapido que encadenar `@` de izquierda a derecha.

```python
np.linalg.multi_dot([A, B, C, D])   # orden optimo automatico
A @ B @ C @ D                        # siempre izquierda a derecha
```
