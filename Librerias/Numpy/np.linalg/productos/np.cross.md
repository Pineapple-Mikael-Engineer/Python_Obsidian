---
title: np.cross — producto vectorial (a × b), el vector perpendicular a dos vectores 3D
aliases:
  - producto vectorial
  - producto cruz
  - cross
  - np.cross
  - "a × b"
tags:
  - numpy
  - api/funcion
  - algebra/matricial
lib: numpy
mod: np
tipo: funcion
retorna: ndarray | escalar
inplace: false
requiere:
  - concepto_shape
draft: false
---

# np.cross — producto vectorial `a × b`

El producto vectorial (o producto cruz) toma dos vectores de **3 componentes** y devuelve un tercer
vector **perpendicular** a ambos, cuya longitud es el área del paralelogramo que forman. Es la
operación de la normal a un plano, el momento de una fuerza ($\vec{r}\times\vec{F}$) y el momento
angular en física. El eje sobre el que viven los vectores (por defecto el **último**) debe tener
tamaño **3** (o 2 para el caso reducido). A diferencia del producto matricial, que contrae un eje y
suma (ver [[np.matmul]]), `cross` **conserva** la dimensión de los vectores: $3 \to 3$.

## La idea en una fórmula

El producto vectorial se obtiene del **determinante simbólico** sobre la base $(\hat{\imath},
\hat{\jmath}, \hat{k})$:

$$
a \times b \;=\;
\begin{vmatrix}
\hat{\imath} & \hat{\jmath} & \hat{k} \\
a_1 & a_2 & a_3 \\
b_1 & b_2 & b_3
\end{vmatrix}
\;=\;
\bigl(\,a_2 b_3 - a_3 b_2,\ \ a_3 b_1 - a_1 b_3,\ \ a_1 b_2 - a_2 b_1\,\bigr)
$$

Su norma es $\lVert a \times b \rVert = \lVert a\rVert\,\lVert b\rVert\,\sin\theta$ (el área del
paralelogramo), y el vector resultante es **perpendicular** a $a$ y a $b$ (regla de la mano derecha).

**El mapa de shapes** (la relación entrada → salida): el eje de vectores —de tamaño 3— se conserva;
los demás ejes son lote y se alinean por broadcasting.

$$
(\underbrace{\dots}_{\text{lote}},\, 3)\ \times\ (\underbrace{\dots}_{\text{lote}},\, 3)\ \longrightarrow\ (\underbrace{\dots}_{\text{lote}},\, 3)
$$

Si los vectores son **2D** (tamaño 2 en el eje), el resultado es el **escalar** $a_1 b_2 - a_2 b_1$
(la componente $z$, único valor no nulo de un cruce en el plano): ese eje **desaparece**.

$$
(\underbrace{\dots}_{\text{lote}},\, 2)\ \times\ (\underbrace{\dots}_{\text{lote}},\, 2)\ \longrightarrow\ (\underbrace{\dots}_{\text{lote}})
$$

Visualmente, para dos vectores de la base canónica el cruce devuelve el tercero (regla de la mano
derecha):

```text
  z
  │   a × b = ẑ
  │ ↗
  │╱
  └────── y      a = x̂ = (1, 0, 0)
 ╱               b = ŷ = (0, 1, 0)
x                a × b = (0, 0, 1) = ẑ   ⟂ a y ⟂ b
```

## Firma

```python
np.cross(
    a,            # array_like: primer vector (o lote), eje de vectores de tamaño 3 o 2
    b,            # array_like: segundo vector (o lote)
    axisa=-1,     # int: eje de vectores en a
    axisb=-1,     # int: eje de vectores en b
    axisc=-1,     # int: eje de vectores en el resultado
    axis=None,    # int: atajo que fija axisa = axisb = axisc a la vez
) -> ndarray | escalar
```

## Los parámetros en detalle

### `a`, `b` — los dos vectores (u operandos por lotes)
`array_like`. El **eje de vectores** (por defecto el último) debe tener tamaño **3** o **2**. Los
demás ejes son de lote y se alinean por [[concepto_broadcasting|broadcasting]]. Pueden mezclarse
tamaños 2 y 3: si **alguno** es 3, el resultado es 3D (el componente faltante se toma como 0).

```python
np.cross([1, 0, 0], [0, 1, 0])   # array([0, 0, 1])
np.cross([1, 2], [3, 4])         # array(-2)  → escalar (componente z): 1*4 - 2*3
```

### `axisa` — eje de vectores en `a`
`int` (defecto `-1`, el último). Indica qué eje de `a` contiene las 3 componentes. Útil cuando los
vectores están en columnas en vez de filas.

### `axisb` — eje de vectores en `b`
`int` (defecto `-1`). Igual que `axisa` pero para `b`. Pueden ser distintos: `a` con los vectores en
el eje 0 y `b` en el último.

### `axisc` — eje de vectores en el resultado
`int` (defecto `-1`). Dónde colocar las 3 componentes del resultado. Solo aplica cuando la salida es
3D (si los dos operandos son 2D y la salida es escalar, se **ignora**).

### `axis` — atajo para fijar los tres a la vez
`int` o `None` (defecto). Si se da, **sobrescribe** `axisa`, `axisb` y `axisc` con el mismo valor.
Es la forma idiomática cuando todos los vectores viven en el mismo eje:

```python
A = np.random.rand(3, 100)   # 100 vectores 3D en columnas (eje 0)
B = np.random.rand(3, 100)
np.cross(A, B, axis=0).shape # (3, 100)  → cruza columna a columna
```

## El caso N-D

`cross` opera sobre el **eje de vectores** y trata el resto como lote, alineándolo por broadcasting
(igual que [[np.matmul]] con sus dos últimos ejes). La regla mecánica: el eje de tamaño 3 se conserva
en su sitio (`axisc`); los demás se broadcastean.

| `a.shape` | `b.shape` | `axis(*)` | resultado | qué pasa |
|-----------|-----------|-----------|-----------|----------|
| `(3,)` | `(3,)` | `-1` | `(3,)` | un solo producto vectorial |
| `(2,)` | `(2,)` | `-1` | `()` escalar | componente z (cruce en el plano) |
| `(n, 3)` | `(n, 3)` | `-1` | `(n, 3)` | **lote** de `n` cruces |
| `(n, 3)` | `(3,)` | `-1` | `(n, 3)` | `b` se **broadcastea** a todo el lote |
| `(3, n)` | `(3, n)` | `axis=0` | `(3, n)` | vectores en columnas |
| `(b, m, 3)` | `(b, m, 3)` | `-1` | `(b, m, 3)` | lote 2D de cruces |

```python
A = np.random.rand(10, 3)    # 10 vectores 3D
B = np.random.rand(10, 3)
np.cross(A, B).shape         # (10, 3)  → 10 normales, sin bucle
np.cross(A, [0, 0, 1]).shape # (10, 3)  → cada vector cruzado con ẑ (broadcast)
```

## Vectorización

El producto vectorial por lotes es [[concepto_vectorizacion]] puro: calcular `n` cruces de golpe sin
recorrer el lote desde Python. Las dos versiones dan lo mismo:

```python
# Bucle Python: un cross por par del lote
def cross_lento(A, B):
    out = np.empty_like(A)
    for i in range(A.shape[0]):
        out[i] = np.cross(A[i], B[i])
    return out

# Vectorizado: NumPy calcula las 3 componentes sobre el eje en C
np.cross(A, B)
```

NumPy expresa internamente las tres componentes como combinaciones de productos elemento a elemento
sobre el eje de vectores; el recorrido del lote ocurre en C, no en el intérprete. Razonar "el eje de
tamaño 3 es el vector, lo demás es lote" permite cruzar un campo vectorial entero sin un solo `for`.

## Valor de retorno

| `a` (eje vec.) | `b` (eje vec.) | salida (shape) | tipo |
|----------------|----------------|----------------|------|
| `3` | `3` | eje de vectores de tamaño 3 (lote broadcasteado) | `ndarray` |
| `2` | `2` | el eje **desaparece** (escalar/lote sin ese eje) | `ndarray` o **escalar** |
| `2` y `3` mezclados | — | tamaño 3 (la componente faltante se toma como 0) | `ndarray` |

- Con dos vectores 1D de tamaño 2, el retorno es un **escalar de NumPy** (0-d), no un `ndarray`.
- El `dtype` sigue las reglas de **promoción** (`int × float → float`).
- `a × b = -(b × a)`: el producto **no es conmutativo**, es **anticonmutativo** (cambiar el orden
  invierte el signo). Y `a × a = 0` (un vector cruzado consigo mismo es el vector nulo).

```python
a = np.array([1, 0, 0])
b = np.array([0, 1, 0])
np.cross(a, b)    # [ 0,  0,  1]
np.cross(b, a)    # [ 0,  0, -1]   → signo opuesto (anticonmutativo)
np.cross(a, a)    # [ 0,  0,  0]   → vector nulo
```

## Casos de uso

### Normal a un plano definido por tres puntos
Dos aristas del plano, su cruce da la dirección perpendicular (la normal).

```python
P, Q, R = np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([0, 1, 0])
n = np.cross(Q - P, R - P)   # [0, 0, 1]  → normal al plano XY
n / np.linalg.norm(n)        # normal unitaria
```

### Momento de una fuerza (torque)
El momento $\vec{\tau} = \vec{r} \times \vec{F}$: brazo de palanca cruzado con la fuerza.

```python
r = np.array([2.0, 0.0, 0.0])    # posición del punto de aplicación (m)
F = np.array([0.0, 3.0, 0.0])    # fuerza (N)
np.cross(r, F)                   # [0, 0, 6]  → 6 N·m alrededor del eje z
```

### Cruce en el plano (área con signo)
Con vectores 2D el resultado es el escalar $a_1 b_2 - a_2 b_1$: el área con signo (positiva si el
giro de `a` a `b` es antihorario), base del test de orientación en geometría computacional.

```python
a = np.array([1, 0])
b = np.array([0, 1])
np.cross(a, b)    # 1   → giro antihorario (CCW)
np.cross(b, a)    # -1  → horario (CW)
```

### Lote de vectores (campo de normales, N-D)
Cruzar dos lotes de vectores 3D de una vez, por ejemplo las normales de muchos triángulos de una
malla.

```python
# 4 triángulos: aristas e1 y e2 por triángulo
e1 = np.array([[1, 0, 0], [0, 2, 0], [1, 1, 0], [3, 0, 0]])  # (4, 3)
e2 = np.array([[0, 1, 0], [0, 0, 3], [0, 1, 1], [0, 0, 2]])  # (4, 3)
np.cross(e1, e2)
# [[ 0,  0,  1],
#  [ 6,  0,  0],
#  [ 1, -1,  1],
#  [ 0, -6,  0]]   → una normal por triángulo, sin bucle
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `incompatible dimensions for cross product` | el eje de vectores no tiene tamaño 2 ni 3 | redimensionar a 3 (o 2) en el eje correcto |
| Esperar `a × b == b × a` | es **anticonmutativo**: invierte el signo | respetar el orden (`r × F`, no `F × r`) |
| Resultado escalar inesperado | los vectores eran 2D (tamaño 2) | usar 3 componentes si quieres un vector 3D |
| Cruce sobre el eje equivocado | los vectores estaban en columnas | fijar `axis=0` (o `axisa`/`axisb`) |
| Confundirlo con el producto punto | `cross` da un vector ⟂; `dot` da un escalar (proyección) | usar [[np.matmul]]/`np.dot` para el producto punto |

## Notas relacionadas

- [[concepto_shape]] — el eje de tamaño 3 se conserva; los demás son lote
- [[concepto_vectorizacion]] — cruzar un lote de vectores sin bucle
- [[np.matmul]] — el producto punto (contrae el eje, da escalar), no confundir con el cruce
- [[np.linalg.norm]] · [[np.dot]] · [[np.outer]]
