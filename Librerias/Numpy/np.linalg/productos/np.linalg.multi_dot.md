---
title: np.linalg.multi_dot — Producto encadenado con orden óptimo
aliases:
  - multi_dot
  - linalg.multi_dot
  - np.linalg.multi_dot
tags:
  - numpy
  - api/funcion
  - algebra/matricial
lib: numpy
mod: np.linalg
tipo: funcion
retorna: ndarray
inplace: false
draft: false
---

# np.linalg.multi_dot — Producto encadenado con orden óptimo

## Firma de la función

```python
np.linalg.multi_dot(arrays, *, out=None) -> ndarray
```

## Valor de retorno

Calcula el producto matricial encadenado de una secuencia de matrices `A @ B @ C @ ...`, pero eligiendo automáticamente el **orden de asociación óptimo** que minimiza el número total de operaciones escalares. El resultado numérico es idéntico a `A @ B @ C`; solo cambia el coste.

| `arrays` | Resultado | Equivalente |
|----------|-----------|-------------|
| `[A, B, C, D]` | matriz producto | `A @ B @ C @ D` |
| `[A, B]` | matriz producto | `A @ B` (sin optimizar, solo 2) |

```python
import numpy as np
A = np.random.rand(10, 100)
B = np.random.rand(100, 5)
C = np.random.rand(5, 50)

np.linalg.multi_dot([A, B, C])     # mismo resultado que A @ B @ C
```

## Por qué importa el orden

El producto matricial es **asociativo** (el resultado no cambia) pero el coste sí depende del paréntesis. `multi_dot` resuelve el problema clásico de *matrix chain ordering* con **programación dinámica**.

```python
# Dimensiones: A(10,100) B(100,5) C(5,50)
# (A @ B) @ C  → 10*100*5 + 10*5*50  = 5000 + 2500 = 7500 ops
# A @ (B @ C)  → 100*5*50 + 10*100*50 = 25000 + 50000 = 75000 ops
# multi_dot elige automáticamente la primera (7500)
```

La ganancia crece cuanto más varían las dimensiones intermedias y más matrices hay en la cadena.

## Parámetros en detalle

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `arrays` | secuencia de ndarrays | Lista/tupla de matrices a multiplicar en orden. Mínimo 2 |
| `out` | ndarray, opcional | Destino preasignado para el resultado final |

### Manejo de los extremos (1D)

| Primera matriz | Última matriz | Efecto |
|----------------|---------------|--------|
| 1D `(K,)` | — | se trata como fila `(1, K)` |
| — | 1D `(K,)` | se trata como columna `(K, 1)` |

Las matrices intermedias deben ser 2D. La optimización de orden solo se aplica con **3 o más** matrices; con 2 simplemente llama al producto. El razonamiento del coste se basa en cómo encajan los [[concepto_shape|shapes]] de cada eslabón.

## Casos de uso

### Cadenas largas con dimensiones dispares

```python
# Muy frecuente en álgebra lineal / ML: proyecciones encadenadas
M = np.linalg.multi_dot([W1, X, W2, b])
```

### Sustituir un `@` encadenado por rendimiento

```python
lento = A @ B @ C @ D
rapido = np.linalg.multi_dot([A, B, C, D])   # mismo valor, menos ops
```

## Buenas prácticas

1. Úsalo cuando encadenes **3+** matrices con dimensiones intermedias variables.
2. Pasa las matrices como **lista**, no como argumentos sueltos.
3. Con solo 2 matrices, usa directamente `@`: no hay nada que optimizar.
4. Reutiliza `out=` en bucles para evitar asignaciones repetidas.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `multi_dot(A, B, C)` | pasar matrices sueltas | envolver en lista: `multi_dot([A, B, C])` |
| `shapes not aligned` | dimensiones interiores no encadenan | verificar `A.shape[-1]==B.shape[0]`... |
| Esperar otro resultado | el valor es idéntico a `A@B@C` | solo optimiza coste, no semántica |
| Usarlo con 2 matrices esperando mejora | con 2 no hay reordenamiento | usar `@` |

## Notas relacionadas

- [[np.linalg.dot]]
- [[concepto_shape]]
- [[np.linalg.matrix_power]]
