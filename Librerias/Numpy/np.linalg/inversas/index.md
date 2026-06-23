---
title: np.linalg — inversas
tags:
  - numpy
  - indice
draft: false
---

# np.linalg — inversas

Esta carpeta agrupa las funciones para **invertir** matrices y tensores: dado $A$, encontrar el
objeto $A^{-1}$ (o su generalización) que lo "deshace". La inversa de una matriz $A$ es la matriz
$A^{-1}$ tal que $A A^{-1} = I$; existe solo si $A$ es cuadrada y no singular ($\det A \neq 0$).
Cuando esa condición no se cumple —matriz rectangular, singular o un tensor de varios ejes— hay
generalizaciones: la pseudoinversa [[np.linalg.pinv]] y la inversa tensorial [[np.linalg.tensorinv]].

> [!danger] La regla de oro: casi nunca necesitas la inversa explícita
> Si tu objetivo es **resolver** $Ax = b$, usa [[np.linalg.solve]], **no** `inv(A) @ b`. Es más
> rápido (factoriza una vez, sin construir la inversa entera) y numéricamente más estable. La
> inversa explícita solo se justifica cuando necesitas la matriz $A^{-1}$ como objeto reutilizable
> (covarianzas, transformaciones aplicadas muchas veces).

## Funciones

| Función | Qué calcula | Requisito | Mapa de shapes |
|---|---|---|---|
| [[np.linalg.inv]] | inversa exacta $A^{-1}$ | matriz cuadrada y no singular | $(\dots,n,n) \to (\dots,n,n)$ |
| [[np.linalg.pinv]] | pseudoinversa de Moore-Penrose $A^{+}$ | cualquiera (rectangular o singular) | $(\dots,m,n) \to (\dots,n,m)$ |
| [[np.linalg.tensorinv]] | inversa tensorial (vía producto tensorial) | bloques de ejes con igual producto | $\text{shape}[ind:] + \text{shape}[:ind]$ |

## Regla de decisión

Elige según la forma y el estado de tu operando:

| Caso | Función |
|---|---|
| Matriz **cuadrada** y no singular ($\det \neq 0$) | [[np.linalg.inv]] |
| Matriz **rectangular** (más filas que columnas o al revés) | [[np.linalg.pinv]] |
| Matriz **singular** o casi singular (mal condicionada) | [[np.linalg.pinv]] |
| **Tensor** N-D que se ve como matriz al agrupar ejes | [[np.linalg.tensorinv]] |
| Solo quieres **resolver** $Ax = b$ | [[np.linalg.solve]] — preferido sobre `inv` |

```text
¿Qué tengo?
  matriz cuadrada y no singular        → np.linalg.inv
  matriz rectangular o singular        → np.linalg.pinv
  tensor N-D (operador tensorial)      → np.linalg.tensorinv
  un sistema Ax = b que resolver        → np.linalg.solve  (no inv)
```

## Descripción de cada función

**[[np.linalg.inv]]** — la inversa de toda la vida, $A^{-1}$ con $A A^{-1} = I$. Exige matriz
cuadrada y no singular; si no, lanza `LinAlgError`. Opera por lotes sobre `(...,n,n)`. Regla: para
resolver $Ax = b$, usa `solve(A, b)` en vez de `inv(A) @ b`.

**[[np.linalg.pinv]]** — la pseudoinversa de Moore-Penrose, $A^{+}$, calculada vía SVD. Funciona con
matrices **no cuadradas** y **singulares**; coincide con `inv` cuando $A$ es cuadrada e invertible.
El parámetro `rcond`/`rtol` fija el umbral de valores singulares (regularización). Es la herramienta
para mínimos cuadrados y sistemas mal condicionados.

**[[np.linalg.tensorinv]]** — generaliza `inv` a **tensores N-D** respecto al producto tensorial. El
parámetro `ind` corta los ejes en dos bloques de igual producto; la salida tiene esos bloques
**intercambiados**. Es la inversa que sustenta [[np.linalg.tensorsolve]].

## Notas relacionadas

- [[np.linalg.solve]] — resolver sistemas sin invertir (el camino recomendado)
- [[np.linalg.lstsq]] · [[np.linalg.svd]] · [[np.linalg.tensorsolve]]
- [[concepto_shape]] — cómo cada función transforma la forma
