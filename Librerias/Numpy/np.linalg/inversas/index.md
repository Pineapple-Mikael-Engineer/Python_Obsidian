---
title: np.linalg — inversas
tags:
  - numpy
  - indice
draft: false
---

# np.linalg — inversas

La inversa de una matriz A es la matriz A^{-1} tal que A A^{-1} = I. Existe solo si A es cuadrada y no singular (det != 0). En la practica, calcular la inversa explicita es a menudo innecesario y numericamente inferior a resolver el sistema directamente con `np.linalg.solve`.

## Funciones

| Funcion | Que calcula | Requisito |
|---|---|---|
| [[np.linalg.inv]] | Inversa exacta A^-1 | Matriz cuadrada y no singular |
| [[np.linalg.pinv]] | Pseudoinversa de Moore-Penrose A^+ | Funciona con rectangulares y singulares |

## Descripcion de cada funcion

**`np.linalg.inv(a)`** — inversa de una matriz cuadrada no singular. Si la matriz es singular o casi singular, lanza `LinAlgError` o devuelve resultados con gran error numerico. Regla: si el objetivo es resolver Ax=b, usar `solve(A, b)` en vez de `inv(A) @ b` — es mas rapido y numericamente mas estable.

**`np.linalg.pinv(a, rcond)`** — pseudoinversa de Moore-Penrose. Funciona con matrices rectangulares (no cuadradas) y singulares. Usa SVD internamente: los valores singulares menores que `rcond` se tratan como cero. Es la generalizacion de la inversa para el caso general.

## Regla de decision

```
¿La matriz es cuadrada y garantizadamente no singular?
  Si  → np.linalg.inv
  No  → np.linalg.pinv
```

| Caso | Funcion |
|---|---|
| Matriz cuadrada, det != 0 | [[np.linalg.inv]] |
| Matriz rectangular (mas filas que columnas) | [[np.linalg.pinv]] |
| Matriz singular o casi singular | [[np.linalg.pinv]] |
| Resolver `Ax = b` (no solo invertir) | [[np.linalg.solve]] — preferido sobre `inv` |

## Advertencia

En la mayoria de los casos en que se calcula `inv(A) @ b`, es preferible usar directamente `solve(A, b)`: misma solucion pero mas rapido y numericamente mas estable (evita el calculo explicito de la inversa).
