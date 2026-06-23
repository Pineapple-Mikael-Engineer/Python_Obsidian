---
title: np.linalg.multi_dot — producto encadenado con orden de asociación óptimo
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
requiere:
  - concepto_shape
draft: false
---

# np.linalg.multi_dot — producto encadenado con orden de asociación óptimo

`np.linalg.multi_dot` calcula el producto matricial **encadenado** de una secuencia de matrices
`A @ B @ C @ ...` eligiendo automáticamente el **orden de asociación** (el paréntesado) que minimiza
el número total de operaciones escalares. El producto matricial es **asociativo** —el resultado
numérico es idéntico al de `A @ B @ C`—, pero el **coste** depende del orden en que se agrupan los
productos. `multi_dot` resuelve el clásico problema de *matrix chain ordering* con **programación
dinámica** y luego ejecuta los [[np.matmul|productos matriciales]] en el orden barato. Solo cambia el
coste, nunca la semántica.

## La idea en una fórmula

El producto encadenado de $p$ matrices contrae sucesivamente las dimensiones interiores. Cada eslabón
debe encadenar con el siguiente (la columna de uno = la fila del próximo):

$$
(d_0, d_1)\,(d_1, d_2)\,(d_2, d_3)\cdots(d_{p-1}, d_p)\ \longrightarrow\ (d_0, d_p)
$$

**El mapa de shapes de la cadena** — solo sobreviven la primera fila y la última columna; todas las
dimensiones interiores $d_1, \dots, d_{p-1}$ se **contraen y desaparecen**:

$$
(m, k_1)\,(k_1, k_2)\cdots(k_{p-1}, n)\ \xrightarrow{\ \text{multi\_dot}\ }\ (m, n)
$$

El coste de un solo producto $(a, b)\,(b, c)$ es $a\cdot b\cdot c$ operaciones escalares. Para una
cadena, el coste total **depende del paréntesado**:

$$
\underbrace{(A\,B)\,C}_{\text{un orden}} \quad\neq_{\text{coste}}\quad \underbrace{A\,(B\,C)}_{\text{otro orden}} \qquad (\text{mismo resultado, distinto número de ops})
$$

`multi_dot` elige, entre todos los paréntesados posibles, el de **mínimo coste**.

## Firma

```python
np.linalg.multi_dot(arrays, *, out=None) -> ndarray
```

## Los parámetros en detalle

### `arrays` — la secuencia de matrices a encadenar
Una **lista o tupla** de matrices (mínimo 2), en el orden en que se multiplican. Las dimensiones
interiores deben encadenar: `arrays[i].shape[-1] == arrays[i+1].shape[0]`. La optimización del orden
solo se aplica con **3 o más** matrices; con exactamente 2, `multi_dot` simplemente llama al producto
(no hay nada que reordenar). Las matrices **intermedias** deben ser 2D.

> Pásalo como **una sola lista**: `multi_dot([A, B, C])`, no `multi_dot(A, B, C)` (matrices sueltas
> lanza error).

### `out` — buffer de salida (keyword-only)
`ndarray` preasignado con el shape exacto del resultado final $(m, n)$. Evita asignar memoria para el
resultado; útil al repetir la cadena en un bucle.

### Manejo de los extremos 1D
El primer y el último operando pueden ser **vectores** 1D, tratados como fila/columna para que la
cadena cierre como escalar o vector:

| Primera matriz | Última matriz | Efecto |
|----------------|---------------|--------|
| 1D `(k,)` | — | se trata como fila `(1, k)` |
| — | 1D `(k,)` | se trata como columna `(k, 1)` |
| 1D `(k,)` | 1D `(k,)` | la cadena colapsa a un **escalar** |

## El caso N-D

`multi_dot` está pensado para **cadenas de matrices 2D**: no hace broadcasting por lotes como
[[np.matmul]]. Los únicos operandos que pueden no ser 2D son los **extremos**, y solo como vectores
1D. El razonamiento de coste se apoya en cómo encajan los [[concepto_shape|shapes]] de cada eslabón:
las dimensiones interiores que se contraen son justo las que aparecen una sola vez entre dos factores
consecutivos.

```python
# Cadena con extremos 1D: v @ M1 @ M2 @ w  → escalar
v = np.random.rand(3)
M1 = np.random.rand(3, 5)
M2 = np.random.rand(5, 4)
w = np.random.rand(4)
np.linalg.multi_dot([v, M1, M2, w])   # escalar (forma cerrada bilineal)
```

## Vectorización

El "bucle" que `multi_dot` evita no es Python sobre elementos, sino la **mala asociación** de un
`@` encadenado, que siempre agrupa de izquierda a derecha. `multi_dot` calcula el paréntesado óptimo
y solo entonces ejecuta los productos (cada uno en BLAS):

```python
# Encadenar @ : SIEMPRE izquierda a derecha (((A@B)@C)@D), pueda costar de más
lento = A @ B @ C @ D

# multi_dot: elige el paréntesado de mínimo coste y luego multiplica
rapido = np.linalg.multi_dot([A, B, C, D])   # mismo valor, menos operaciones
```

Mismo resultado; la ganancia crece cuanto **más varían las dimensiones intermedias** y más larga es la
cadena. Para 2 matrices no hay nada que optimizar: usa `@` directamente.

## Valor de retorno

| `arrays` | salida | tipo |
|----------|--------|------|
| `[A(m,k), …, Z(j,n)]` (todas 2D) | `(m, n)` | `ndarray` |
| `[v(k,), M, …, Z]` (primera 1D) | `(n,)` | `ndarray` (vector) |
| `[A, …, w(k,)]` (última 1D) | `(m,)` | `ndarray` (vector) |
| `[v(k,), …, w(k,)]` (ambos extremos 1D) | `()` | **escalar** |

- El resultado es **numéricamente idéntico** a encadenar `@` en cualquier orden; solo cambia el coste.
- El `dtype` sigue las reglas de promoción de los productos intermedios.

## Casos de uso

### El ahorro frente a `A @ B @ C` ingenuo
```python
A = np.random.rand(10, 100)
B = np.random.rand(100, 5)
C = np.random.rand(5, 50)

# (A @ B) @ C  → 10·100·5 + 10·5·50  = 5_000 + 2_500  =  7_500 ops
# A @ (B @ C)  → 100·5·50 + 10·100·50 = 25_000 + 50_000 = 75_000 ops
np.linalg.multi_dot([A, B, C])   # elige el primer orden (7_500): 10x menos trabajo
```
La dimensión intermedia $100$ aparece dos veces: agruparla pronto (`A @ B` la elimina antes) es lo que
abarata la cadena. `multi_dot` descubre eso solo.

### Cadenas largas en ML / álgebra lineal
```python
# Proyecciones encadenadas con dimensiones dispares
M = np.linalg.multi_dot([W1, X, W2, V])   # orden óptimo automático
```

### Sustituir un `@` encadenado por rendimiento
```python
lento = A @ B @ C @ D
rapido = np.linalg.multi_dot([A, B, C, D])   # mismo valor, menos ops
```

### Forma bilineal con extremos 1D
```python
v, w = np.random.rand(4), np.random.rand(6)
M = np.random.rand(4, 6)
np.linalg.multi_dot([v, M, w])   # escalar  →  vᵀ M w
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `multi_dot(A, B, C)` falla | matrices pasadas sueltas | envolver en lista: `multi_dot([A, B, C])` |
| `shapes not aligned` | dimensiones interiores no encadenan | verificar `arrays[i].shape[-1] == arrays[i+1].shape[0]` |
| Esperar otro resultado numérico | solo optimiza coste, no semántica | el valor es idéntico a `A@B@C` |
| Usarlo con 2 matrices esperando mejora | con 2 no hay reordenamiento | usar `@` |
| Pasar matrices intermedias 1D | solo los extremos pueden ser 1D | dar forma 2D a las del medio |

## Notas relacionadas

- [[np.matmul]] — el producto matricial individual que `multi_dot` encadena
- [[concepto_shape]] — el coste de la cadena se razona sobre los shapes de cada eslabón
- [[np.linalg.matrix_power]] · [[np.linalg.matrix_transpose]]
