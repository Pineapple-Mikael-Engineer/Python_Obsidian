---
title: np.linalg — productos matriciales
tags:
  - numpy
  - indice
draft: false
---

# np.linalg — productos matriciales

Operaciones de producto y potencia matricial. En la mayoria de los casos, el operador `@` (Python 3.5+) es suficiente para productos simples.

## Funciones

| Funcion | Que calcula | Caso tipico |
|---|---|---|
| [[np.linalg.dot]] | Producto punto (vectores) o producto matricial (2D+) | Producto de dos arrays |
| [[np.linalg.multi_dot]] | Cadena de productos con orden optimo automatico | Tres o mas matrices |
| [[np.linalg.matrix_power]] | Potencia entera de una matriz cuadrada (A^n) | A^n con n entero (positivo, cero o negativo) |
| [[np.linalg.matrix_transpose]] | Transpuesta de la ultima dimension | Equivalente a `.T`, disponible desde NumPy 2.0 |

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
