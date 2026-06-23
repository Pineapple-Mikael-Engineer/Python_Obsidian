---
title: np.diag — construye una diagonal (1D) o extrae la diagonal (2D)
aliases:
  - diag
  - np.diag
tags:
  - numpy
  - api/funcion
  - creacion
lib: numpy
mod: np
tipo: funcion
retorna: ndarray
inplace: false
requiere:
  - concepto_shape
draft: false
---

# np.diag — construye una diagonal (1D) o extrae la diagonal (2D)

`np.diag` es **ambivalente**: su comportamiento cambia según la dimensión de la entrada. Si recibe un
**vector 1D**, lo coloca en la diagonal de una matriz cuadrada nueva (la **construye**). Si recibe una
**matriz 2D**, devuelve los elementos de su diagonal como un vector 1D (la **extrae**). Una sola
función para los dos sentidos del verbo "diagonal". Para la extracción por lotes N-D existe la
hermana [[np.diagonal]], con la que conviene no confundirla.

## La idea

Las dos caras de la función, gobernadas por el `ndim` de la entrada:

**Construir (entrada 1D).** Un vector $v = [d_0, d_1, d_2]$ se convierte en la matriz diagonal cuyos
valores fuera de la diagonal son cero:

$$
\text{diag}([d_0, d_1, d_2]) = \begin{bmatrix} d_0 & 0 & 0 \\ 0 & d_1 & 0 \\ 0 & 0 & d_2 \end{bmatrix}
$$

**Extraer (entrada 2D).** Una matriz $A$ devuelve el vector de su diagonal principal:

$$
\text{diag}\!\begin{bmatrix} a_{00} & a_{01} & a_{02} \\ a_{10} & a_{11} & a_{12} \\ a_{20} & a_{21} & a_{22} \end{bmatrix}
= \begin{bmatrix} a_{00} & a_{11} & a_{22} \end{bmatrix}
$$

El **mapa de shapes** resume la ambivalencia, con el desplazamiento `k`:

$$
(n,) \xrightarrow{\ \text{diag}\ } (n+|k|,\ n+|k|)
\qquad\qquad
(m, n) \xrightarrow{\ \text{diag}\ } \big(\min(m,n)-|k|,\big)
$$

Construir con $k \neq 0$ agranda la matriz (el vector ocupa una diagonal desplazada y el resto se
rellena con ceros). Ver [[concepto_shape]].

## Firma

```python
np.diag(
    v,      # array_like: vector 1D (construir) o matriz 2D (extraer)
    k=0,    # int: diagonal a usar (0 principal, >0 arriba, <0 abajo)
) -> ndarray
```

## Los parámetros en detalle

### `v` — la entrada que decide el modo
`array_like`. Su **número de ejes** elige el comportamiento:
- **1D** → construye una matriz diagonal $(n+|k|, n+|k|)$ con `v` en la diagonal `k`.
- **2D** → extrae la diagonal `k` como vector 1D.
- **3D o más** → `ValueError`: `np.diag` solo entiende 1D y 2D. Para lotes N-D usa [[np.diagonal]].

```python
np.diag([1, 2, 3])
# array([[1, 0, 0],
#        [0, 2, 0],
#        [0, 0, 3]])

np.diag([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
# array([1, 5, 9])   → la diagonal extraída
```

### `k` — qué diagonal
`int` (defecto `0`). `0` es la principal; `k > 0` una superdiagonal; `k < 0` una subdiagonal. En el
**modo construir**, desplazar la diagonal **agranda** la matriz para que quepa. En el **modo extraer**,
selecciona qué diagonal se devuelve (y su longitud cambia).

```python
np.diag([1, 2, 3], k=1)
# array([[0, 1, 0, 0],
#        [0, 0, 2, 0],
#        [0, 0, 0, 3],
#        [0, 0, 0, 0]])   → 4×4: el vector subió a la superdiagonal

A = np.arange(9).reshape(3, 3)
np.diag(A, k=1)    # array([1, 5])   → la diagonal de encima
np.diag(A, k=-1)   # array([3, 7])   → la de debajo
```

## Casos de uso

### Matriz diagonal a partir de un vector (escalado por ejes)
```python
escalas = np.array([2., 0.5, 10.])
D = np.diag(escalas)   # transformación que escala cada eje por su factor
```

### Extraer y sumar la diagonal (traza)
```python
A = np.array([[10, 2, 3], [4, 20, 6], [7, 8, 30]])
np.diag(A)          # [10, 20, 30]
np.diag(A).sum()    # 60  → equivale a np.trace(A)
```

### Doble aplicación: limpiar todo menos la diagonal
Como construir y extraer son inversas, `diag(diag(A))` deja solo la diagonal de `A`:
```python
soloDiag = np.diag(np.diag(A))   # matriz con la diagonal de A y ceros fuera
```

## `np.diag` vs `np.diagonal` vs `np.diagflat`

| Función | Entrada | Hace | Salida |
|---------|---------|------|--------|
| `np.diag(v)` | 1D | **construye** matriz diagonal | 2D |
| `np.diag(A)` | 2D | **extrae** la diagonal (copia) | 1D |
| [[np.diagonal]] | 2D / N-D | **extrae** (vista solo lectura, soporta lotes) | 1D / lote |
| [[np.diagflat]] | cualquiera | **construye** desde la entrada **aplanada** | 2D |

La diferencia clave: `np.diag` decide entre extraer/construir según el `ndim` y solo admite 1D/2D;
[[np.diagonal]] siempre **extrae** y es el que maneja lotes N-D; [[np.diagflat]] siempre **construye**
aplanando primero.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Esperar construir y obtener un vector | la entrada era 2D → `diag` **extrajo** | aplanar antes, o usar [[np.diagflat]] |
| Esperar extraer y obtener una matriz | la entrada era 1D → `diag` **construyó** | revisa el `ndim` de la entrada |
| `ValueError: Input must be 1- or 2-d` | la entrada tiene 3+ ejes | usar [[np.diagonal]] con `axis1`/`axis2` |
| Matriz más grande de lo esperado al construir | `k != 0` agranda la matriz $(n+|k|)$ | es correcto; el vector cabe en la diagonal desplazada |

## Notas relacionadas

- [[concepto_shape]] — el `ndim` de la entrada decide construir (1D→2D) o extraer (2D→1D)
- [[np.diagonal]] — extracción que devuelve **vista** y soporta lotes N-D
- [[np.diagflat]] — construir aplanando siempre la entrada
- [[np.eye]] · [[np.identity]] — la diagonal constante de unos
- [[np.trace]] — la suma de la diagonal
