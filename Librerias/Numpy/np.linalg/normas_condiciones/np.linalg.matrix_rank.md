---
title: np.linalg.matrix_rank — rango (independencia lineal) de una matriz vía SVD
aliases:
  - matrix_rank
  - linalg.matrix_rank
  - np.linalg.matrix_rank
tags:
  - numpy
  - api/funcion
  - algebra/matricial
lib: numpy
mod: np.linalg
tipo: funcion
retorna: int | ndarray
inplace: false
requiere:
  - concepto_shape
draft: false
---

# np.linalg.matrix_rank — rango (independencia lineal) de una matriz vía SVD

`np.linalg.matrix_rank` cuenta cuántas filas (o columnas) de `A` son **linealmente
independientes**: su rango. Numéricamente, eso es el **número de valores singulares mayores que un
umbral** de la [[np.linalg.svd|SVD]] — los valores singulares casi nulos corresponden a direcciones
que la matriz "aplasta", es decir, a dependencias lineales. Sirve para detectar **deficiencia de
rango**: columnas redundantes en datos, sistemas sin solución única, matrices casi singulares.

## La idea en una fórmula

El rango es el número de valores singulares $\sigma_i$ de la SVD que superan una tolerancia $\tau$:

$$
\operatorname{rank}(A) = \#\{\, i : \sigma_i > \tau \,\}
\qquad
\tau = \texttt{S.max()} \cdot \max(m, n) \cdot \varepsilon \ \text{(por defecto)}
$$

donde $\varepsilon$ es la precisión de máquina (`eps`). **El mapa de shapes**: `matrix_rank`
colapsa los dos últimos ejes (la matriz) a un **entero** y conserva los ejes de lote:

$$
(\underbrace{n_0,\dots,n_{k-1}}_{\text{lote}},\, m,\, n)\ \xrightarrow{\ \text{matrix\_rank}\ }\ (\underbrace{n_0,\dots,n_{k-1}}_{\text{lote}})\ \ \text{(enteros)}
$$

El rango está acotado por $0 \le \operatorname{rank}(A) \le \min(m, n)$. Igualdad con $\min(m,n)$ →
**rango completo** (sin dependencias); menor → **rango deficiente**.

```text
σ = [4.7, 2.1, 1e-16]   →  dos σ "grandes", uno ~0  →  rank = 2
                           el valor singular nulo señala una dirección dependiente
```

## Firma

```python
np.linalg.matrix_rank(
    A,                 # array_like (..., M, N): matriz o pila de matrices
    tol=None,          # float | array_like: umbral absoluto (heredado; usar rtol)
    hermitian=False,   # bool: A es hermítica/simétrica → autovalores en vez de SVD
    *,
    rtol=None,         # float | array_like: umbral relativo a S.max() (NumPy ≥ 1.24)
) -> int | ndarray
```

## Los parámetros en detalle

### `A` — el tensor de entrada
`array_like` de shape `(M, N)` o pila `(..., M, N)`. **No** necesita ser cuadrada: el rango está
definido para cualquier matriz. Con más de 2 ejes opera por lotes sobre los dos últimos.

### `tol` — umbral absoluto de valor singular
Valores singulares por debajo de `tol` se consideran **cero** (direcciones dependientes). Si es
`None`, NumPy usa la tolerancia por defecto $\texttt{S.max()} \cdot \max(M,N) \cdot \varepsilon$,
escalada a los datos. Súbelo cuando los datos tengan **ruido** y quieras que el ruido no cuente
como una dirección independiente.

```python
A = np.array([[1.0, 2.0],
              [2.0, 4.000001]])      # casi dependiente (ruido en una cifra)
np.linalg.matrix_rank(A)            # 2  → el ruido cuenta como independiente
np.linalg.matrix_rank(A, tol=1e-3) # 1  → tolerancia agresiva lo colapsa
```

### `rtol` — umbral relativo (preferido)
Igual que `tol` pero **relativo** al mayor valor singular: el umbral efectivo es
$\texttt{rtol} \cdot \texttt{S.max()}$. Es keyword-only y la forma recomendada en NumPy moderno
(escala sola con la magnitud de los datos). No combinar con `tol`: se usa uno u otro.

```python
np.linalg.matrix_rank(A, rtol=1e-5)  # umbral = 1e-5 · σ_max
```

### `hermitian` — matriz hermítica/simétrica
Si `True`, asume que `A` es hermítica (simétrica real) y usa una descomposición de **autovalores**,
más eficiente que la SVD general. Solo actívalo si `A` lo es de verdad; si no, el resultado es
incorrecto.

```python
S = np.array([[2.0, 1.0], [1.0, 2.0]])
np.linalg.matrix_rank(S, hermitian=True)   # 2  → ruta eficiente
```

## El caso N-D / axis

`matrix_rank` no tiene `axis`: trata **siempre** los dos últimos ejes como la matriz y todo lo
anterior como **lote**. Cada matriz del lote produce un **entero**; el resultado tiene el shape del
lote.

| `A.shape` | salida | lectura |
|-----------|--------|---------|
| `(m, n)` | `int` de Python | rango de la matriz |
| `(b, m, n)` | `(b,)` enteros | un rango por matriz del lote |
| `(b, c, m, n)` | `(b, c)` enteros | una rejilla de rangos |

```python
lote = np.stack([np.eye(3),                       # rango 3
                 np.array([[1.,2.,3.],
                           [2.,4.,6.],             # fila 2 = 2·fila 1
                           [0.,0.,1.]])])          # rango 2
lote.shape                  # (2, 3, 3)
np.linalg.matrix_rank(lote) # [3, 2]  → un entero por matriz, sin bucle
```

## Vectorización

El caso por lotes evita un bucle Python: NumPy calcula la SVD de cada matriz en LAPACK y cuenta los
valores singulares significativos en C. Es [[concepto_vectorizacion]] sobre álgebra lineal:

```python
# Bucle Python: una SVD por matriz
def rangos(stack):
    out = np.empty(stack.shape[0], dtype=int)
    for i in range(stack.shape[0]):
        out[i] = np.linalg.matrix_rank(stack[i])
    return out

# Vectorizado: NumPy recorre el lote en LAPACK
np.linalg.matrix_rank(stack)
```

Mismo resultado; la versión vectorizada no salta al intérprete por cada matriz.

## Valor de retorno

| Entrada | salida | tipo |
|---------|--------|------|
| `(m, n)` | un rango | **`int` de Python** |
| `(b, m, n)` | `(b,)` | `ndarray` de enteros |
| `(b, c, m, n)` | `(b, c)` | `ndarray` de enteros |

- Para una matriz 2D el retorno es un **`int` de Python** (no un `ndarray` 0-d).
- Para una pila N-D es un `ndarray` de enteros con el shape del lote.
- El rango siempre cumple $0 \le \operatorname{rank} \le \min(M, N)$.

```python
A = np.array([[1, 2], [2, 4]])        # fila 2 = 2 · fila 1
np.linalg.matrix_rank(A)              # 1   → rango deficiente
np.linalg.matrix_rank(np.eye(3))      # 3   → rango completo
type(np.linalg.matrix_rank(A))        # <class 'int'>
```

## Casos de uso

### Detectar columnas redundantes en datos
```python
X = np.array([[1, 2, 3],
              [2, 4, 6],              # = 2 · fila 1
              [1, 0, 1]], dtype=float)
np.linalg.matrix_rank(X)             # 2  → una fila/columna es combinación de otras
```

### Comprobar si un sistema tiene solución única
```python
A = np.array([[1.0, 1.0], [1.0, 1.0]])
np.linalg.matrix_rank(A)             # 1 < 2  → sin solución única
```

### Datos ruidosos: ajustar la tolerancia
```python
ruido = np.eye(3) + 1e-9 * np.random.rand(3, 3)
np.linalg.matrix_rank(ruido)               # 3   → el ruido aparenta independencia
np.linalg.matrix_rank(ruido, rtol=1e-6)    # 3   → aquí sigue, pero el umbral controla
```

### N-D: rango de un lote de matrices
```python
lote = np.random.rand(10, 5, 5)
np.linalg.matrix_rank(lote)          # (10,)  → un rango por matriz del lote
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Rango mayor del esperado | el ruido numérico cuenta como dirección independiente | subir `tol`/`rtol` |
| Rango menor del esperado | umbral demasiado alto colapsa direcciones reales | bajar/quitar `tol`/`rtol` |
| Resultado raro en simétrica | no se usó la ruta eficiente / se usó mal | `hermitian=True` solo si lo es de verdad |
| `LinAlgError` durante la SVD | la matriz contiene `NaN`/`inf` | limpiar valores no finitos antes |
| Mezclar `tol` y `rtol` | son redundantes | usar **uno**; preferir `rtol` |

## Notas relacionadas

- [[np.linalg.svd]] — los valores singulares que se cuentan para obtener el rango
- [[np.linalg.cond]] — distingue "singular exacta" de "casi singular" (κ frente a rango)
- [[np.linalg.norm]] · [[np.linalg.det]] · [[np.linalg.solve]]
- [[normas_condiciones/index|normas y condiciones]] — la nota madre del grupo
