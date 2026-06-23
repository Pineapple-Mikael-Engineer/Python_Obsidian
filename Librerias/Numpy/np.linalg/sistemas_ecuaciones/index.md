---
title: np.linalg — sistemas de ecuaciones
tags:
  - numpy
  - indice
lib: numpy
mod: np.linalg
draft: false
---

# np.linalg — sistemas de ecuaciones

Resolver $A\mathbf{x}=\mathbf{b}$ es el problema fundamental del álgebra lineal aplicada: dada una matriz
de coeficientes $A$ y un lado derecho $\mathbf{b}$, encontrar la $\mathbf{x}$ que satisface el sistema.
Las tres funciones de este directorio cubren los tres escenarios según **cómo sea $A$**: cuadrada y
exacta, rectangular (mínimos cuadrados) o un tensor N-D.

## Las tres funciones

| Función | Sistema que resuelve | Requisito de $A$ | Devuelve |
|---|---|---|---|
| [[np.linalg.solve]] | exacto $A\mathbf{x}=\mathbf{b}$ | **cuadrada** $(n,n)$ e invertible | `x` |
| [[np.linalg.lstsq]] | mínimos cuadrados $\min\lVert A\mathbf{x}-\mathbf{b}\rVert_2$ | **cualquier** forma $(M,N)$; sobredeterminado o rango deficiente | `(x, residuals, rank, s)` |
| [[np.linalg.tensorsolve]] | ecuación **tensorial** $A\mathbf{x}=\mathbf{b}$ | tensor N-D **cuadrado al aplanar** | `x` |

- **[[np.linalg.solve]]** resuelve un sistema determinado vía factorización LU. Acepta varios lados a la
  vez (`b` puede ser `(n, k)`) y lotes de sistemas por broadcasting.
- **[[np.linalg.lstsq]]** minimiza el residuo cuando no hay solución exacta (más ecuaciones que
  incógnitas, o $A$ singular). Usa SVD y devuelve además rango y valores singulares. Es el motor de la
  **regresión lineal** y el **ajuste polinómico**.
- **[[np.linalg.tensorsolve]]** generaliza `solve` a tensores: reordena y aplana $A$ a una matriz
  cuadrada, resuelve y reconstruye $\mathbf{x}$. Reservada para sistemas genuinamente N-dimensionales.

## Tabla de decisión

| ¿Cómo es $A$? | Función |
|---|---|
| Cuadrada $(n,n)$ e invertible → solución **exacta** | [[np.linalg.solve]] |
| Rectangular: más ecuaciones que incógnitas (**sobredeterminado**) | [[np.linalg.lstsq]] |
| Rectangular: más incógnitas que ecuaciones (**subdeterminado**) | [[np.linalg.lstsq]] |
| Singular o casi singular (**rango deficiente**) | [[np.linalg.lstsq]] |
| **Tensor N-D**: $A_{ijkl}\,x_{kl}=b_{ij}$ | [[np.linalg.tensorsolve]] |

```text
¿A es cuadrada y no singular?
  Sí → solve         (LU, exacto, más rápido)
  No → lstsq         (SVD, mínimos cuadrados; tolera sobre/subdeterminado y rango deficiente)
¿A es un tensor de orden superior?
  Sí → tensorsolve   (aplana a matriz cuadrada y resuelve)
```

## La regla de oro: `solve`, no `inv`

> [!regla] Nunca `inv(A) @ b` para resolver un sistema
> Para hallar $\mathbf{x}$ en $A\mathbf{x}=\mathbf{b}$ se usa **siempre** [[np.linalg.solve]], no
> `np.linalg.inv(A) @ b`. `solve` factoriza $A$ una sola vez (LU) en lugar de calcular la inversa
> completa: es **más rápido** y **numéricamente más estable**. Calcular [[np.linalg.inv|la inversa]] solo
> se justifica si necesitas $A^{-1}$ como objeto en sí mismo, cosa rara.

Notas complementarias:

- Para varios términos independientes con la misma $A$, pásalos juntos como columnas de `b`: una sola
  factorización los resuelve todos.
- `lstsq` devuelve además el **rango efectivo** y los **valores singulares**, útiles para diagnosticar
  el condicionamiento del problema.
