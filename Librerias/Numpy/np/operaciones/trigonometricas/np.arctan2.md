---
title: np.arctan2 — ángulo del punto (x, y) con el cuadrante correcto (ufunc binaria)
aliases:
  - arctan2
  - np.arctan2
  - arcotangente de dos argumentos
tags:
  - numpy
  - api/funcion
  - trigonometricas

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray | escalar
inplace: false

# --- Dependencias ---
requiere:
  - concepto_ufuncs
  - concepto_broadcasting

draft: false
---

# np.arctan2 — ángulo del punto (x, y) con el cuadrante correcto (ufunc binaria)

`np.arctan2` es una **ufunc binaria**: dados dos tensores `y` y `x`, devuelve **en radianes** el
ángulo del punto $(x_i, y_i)$ medido desde el eje $+X$, usando el signo de **ambos** argumentos para
dar el **cuadrante correcto**. Es la inversa "completa" de la tangente: donde [[np.arctan]] solo ve
el cociente $y/x$ —y pierde de qué cuadrante viene— `arctan2` los recibe **separados** y recupera el
rango completo $(-\pi,\pi]$. Como toda ufunc binaria, no reduce ningún eje: alinea `y` y `x` por
[[concepto_broadcasting|broadcasting]] y produce la **shape común**. Su uso canónico es la conversión
**cartesiano → polar** (el ángulo de un vector). Nota el orden de los argumentos: **`y` primero, `x`
después**.

## La idea en una fórmula

La operación es **elemento a elemento** sobre dos entradas; cada posición de la salida es el ángulo
del punto correspondiente:

$$
\theta_i = \operatorname{arctan2}(y_i,\,x_i) \in (-\pi,\,\pi]
$$

Frente a $\arctan(y/x)\in(-\pi/2,\pi/2)$, `arctan2` usa los signos de $x$ e $y$ para colocar el
ángulo en el cuadrante real:

$$
\operatorname{arctan2}(y,x)=
\begin{cases}
\arctan(y/x) & x>0\\
\arctan(y/x)+\pi & x<0,\ y\ge 0\\
\arctan(y/x)-\pi & x<0,\ y<0\\
+\pi/2 & x=0,\ y>0\\
-\pi/2 & x=0,\ y<0
\end{cases}
$$

El **mapa de shapes es el de broadcasting**: `y` y `x` se alinean **por la derecha**, se rellena con
`1` a la izquierda y cada eje toma el `max` (válido si en cada eje coinciden o uno es `1`):

$$
(\dots, a_{k-1}, a_k),\ (\dots, b_{k-1}, b_k)\ \xrightarrow{\ \text{broadcast}\ }\ (\dots,\,\max(a_{k-1},b_{k-1}),\,\max(a_k,b_k))
$$

| `x` | `y` | $\operatorname{arctan2}(y,x)$ | cuadrante |
|-----|-----|-------------------------------|-----------|
| `1` | `1` | `π/4 ≈ 0.785` | I |
| `-1` | `1` | `3π/4 ≈ 2.356` | II |
| `-1` | `-1` | `-3π/4 ≈ -2.356` | III |
| `1` | `-1` | `-π/4 ≈ -0.785` | IV |
| `0` | `1` | `π/2` | eje +Y |
| `0` | `-1` | `-π/2` | eje -Y |
| `-1` | `0` | `π` | eje -X |

Toda la lógica de alineación vive en [[concepto_broadcasting]].

## Firma

```python
np.arctan2(
    x1,                     # array_like: las ORDENADAS y (numerador)
    x2,                     # array_like: las ABSCISAS x (denominador)
    /,
    out=None,               # ndarray | None: destino preasignado
    *,
    where=True,             # array_like[bool]: máscara de cómputo
    dtype=None,             # dtype: tipo de cómputo/salida
    casting='same_kind',    # política de conversión
    order='K',              # layout en memoria de la salida
) -> ndarray | escalar
```

> El primer argumento `x1` son las **`y`** (ordenadas) y el segundo `x2` son las **`x`** (abscisas):
> se invoca `np.arctan2(y, x)`, no `(x, y)`.

## Los parámetros en detalle

### `x1` (las `y`), `x2` (las `x`) — las componentes del punto
`array_like` **real** (ndarray, lista, escalar). `x1` son las ordenadas, `x2` las abscisas. Deben ser
**broadcasteables** entre sí; sus shapes se alinean por la derecha. No hay restricción de dominio
(cualquier real); el único caso especial es $(0,0)$, que da `0.0`. Si ambos son escalares, el retorno
es un escalar de NumPy.

### `out` — escribir en un buffer existente
`ndarray` preasignado con la shape de salida (la del broadcast). Evita asignar memoria nueva; útil en
bucles. El dtype debe ser flotante y compatible bajo `casting`.

### `where` — máscara de cómputo
`array_like` booleano broadcasteable con las entradas. Solo se calcula donde `where` es `True`; en el
resto, la salida **conserva lo que hubiera en `out`**. Por eso con `where` casi siempre se pasa `out`
explícito (si no, esas posiciones quedan sin inicializar):

```python
y = np.array([1.0, -2.0, 3.0])
x = np.array([1.0,  2.0, -3.0])
np.arctan2(y, x, where=y > 0, out=np.zeros(3))   # solo donde y > 0
```

### `dtype` — tipo de cómputo y de salida
Fuerza el tipo flotante en el que se opera y se devuelve (p. ej. `float32`). El resultado es siempre
flotante.

### `casting` — política de conversión
`'no'`, `'equiv'`, `'safe'`, `'same_kind'` (defecto), `'unsafe'`. Controla qué conversiones se
permiten al escribir en `out` o aplicar `dtype`.

### `order` — layout en memoria de la salida
`'K'` (defecto), `'C'`, `'F'`, `'A'`. Solo afecta a **cómo** se almacena el resultado, no a sus
valores.

## Broadcasting y el caso N-D

`np.arctan2` no tiene `axis`: su comportamiento en N-D lo dicta enteramente el broadcasting entre `y`
y `x`. La regla es mecánica —alinear por la derecha, rellenar con `1`, tomar el `max` por eje—:

| `y.shape` (`x1`) | `x.shape` (`x2`) | salida | lectura |
|------------------|------------------|--------|---------|
| `(n,)` | `(n,)` | `(n,)` | ángulo de cada par `(x_i, y_i)` |
| `(n,)` | `()` escalar | `(n,)` | mismo `x` para todas las `y` |
| `(m, n)` | `(n,)` | `(m, n)` | el vector `x` por columna en cada fila |
| `(m, 1)` | `(1, n)` | `(m, n)` | malla: ángulo de cada par fila/columna |
| `(b, m, n)` | `(b, m, n)` | `(b, m, n)` | ángulo por elemento de un lote de campos |

Ejemplo: ángulo de un lote de campos vectoriales 2D —cada celda tiene su `(x, y)`—:

```python
Vy = np.array([[[0., 1.], [-1., 0.]],
               [[1., 1.], [-1., -1.]]])   # (2, 2, 2)  componente y
Vx = np.array([[[1., 0.], [ 0., -1.]],
               [[1., -1.], [-1.,  1.]]])  # (2, 2, 2)  componente x
np.arctan2(Vy, Vx).shape    # (2, 2, 2)  → mismo shape
np.arctan2(Vy, Vx)
# [[[ 0.    ,  1.5708], [-1.5708,  3.1416]],
#  [[ 0.7854,  2.3562], [-2.3562, -0.7854]]]   # ángulo (rad) de cada celda
```

## Vectorización

`np.arctan2` reemplaza el bucle Python que llamaría a `math.atan2(y_i, x_i)` posición a posición. Las
dos versiones dan lo mismo, pero la ufunc corre en C sobre memoria contigua, aplicando broadcasting
sin materializar formas intermedias:

```python
import math
# Bucle Python (lento, explícito):
out = np.empty_like(y, dtype=float)
for i in range(y.size):
    out.flat[i] = math.atan2(y.flat[i], x.flat[i])

# Vectorizado (un único bucle en C, con broadcasting):
out = np.arctan2(y, x)
```

Es el principio de [[concepto_vectorizacion]]: describes *qué* operación aplicar a cada posición, no
*cómo* iterar. Soporta `out`/`where`/`dtype`/`casting` como toda ufunc binaria.

## Valor de retorno

La salida tiene la **shape común del broadcasting** de `y` y `x`; dtype **flotante** y valores en
$(-\pi,\pi]$ (radianes):

| `y` (`x1`) | `x` (`x2`) | salida (shape) | tipo |
|------------|------------|----------------|------|
| escalar | escalar | `()` | **escalar de NumPy** (`np.float64`...) |
| `(n,)` | escalar | `(n,)` | `ndarray` |
| `(m, n)` | `(n,)` | `(m, n)` | `ndarray` |
| `(m, 1)` | `(1, n)` | `(m, n)` | `ndarray` |

Reglas de `dtype` (promoción, sin `dtype=` explícito): enteros se promueven a `float64`; `float32` +
`float32` → `float32`; mezcla con `float64` → `float64`. La salida es un escalar de NumPy solo si
**ambas** entradas son escalares.

```python
np.arctan2(1, 1)                  # 0.7853981633974483  (π/4)
np.arctan2(1, -1)                 # 2.356194490192345   (3π/4) → cuadrante II
type(np.arctan2(1, 1))            # numpy.float64  (escalar)
np.arctan2([1, 1], [1, -1]).dtype # float64
```

## Casos de uso

### Ángulo (orientación) de un vector
```python
np.rad2deg(np.arctan2(3, 4))      # 36.87°  → dirección del vector (4, 3)
np.arctan2(-1, -1)                # -3π/4   → cuadrante III, no π/4
```

### Conversión cartesiano → polar
```python
x = np.array([1.0, 0.0, -1.0,  0.0])
y = np.array([0.0, 1.0,  0.0, -1.0])
r     = np.hypot(x, y)            # radio
theta = np.arctan2(y, x)          # ángulo en (-π, π]
# theta → [0., π/2, π, -π/2]      cada punto en su cuadrante/eje correcto
```

### Por qué no `arctan(y/x)`
```python
np.arctan((-1) / (-1))            # π/4    → ¡cuadrante equivocado! (el signo se canceló)
np.arctan2(-1, -1)                # -3π/4  → correcto
np.arctan2(1, 0)                  # π/2    → maneja x = 0 sin división por cero
```

### N-D: ángulo de un lote de campos vectoriales
```python
Vy = np.array([[[0., 1.], [-1., 0.]],
               [[1., 1.], [-1., -1.]]])   # (2, 2, 2)
Vx = np.array([[[1., 0.], [ 0., -1.]],
               [[1., -1.], [-1.,  1.]]])  # (2, 2, 2)
np.arctan2(Vy, Vx)
# [[[ 0.    ,  1.5708], [-1.5708,  3.1416]],
#  [[ 0.7854,  2.3562], [-2.3562, -0.7854]]]   # ángulo por celda, mismo shape
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Argumentos invertidos | se pasó `(x, y)` en vez de `(y, x)` | el orden es `np.arctan2(y, x)` (ordenada primero) |
| Cuadrante equivocado | se usó `np.arctan(y / x)`, que pierde los signos | usar `arctan2` con `y` y `x` separados |
| `inf`/`ZeroDivisionError` con `x = 0` | formar `y / x` antes de invertir | `arctan2` maneja `x = 0` directamente |
| `operands could not be broadcast together` | shapes de `y` y `x` incompatibles | alinear por la derecha; ver [[concepto_broadcasting]] |
| Resultado "en grados raro" | el retorno está en **radianes** | convertir con `np.rad2deg` |

## Notas relacionadas

- [[concepto_ufuncs]] — `np.arctan2` es una ufunc binaria; hereda `out`/`where`/`dtype`/`casting`
- [[concepto_broadcasting]] — la alineación de `y` y `x` que gobierna su salida
- [[np.arctan]] — la versión unaria: solo 2 cuadrantes, rango `(-π/2, π/2)`
- [[np.hypot]] — el radio que acompaña al ángulo en cartesiano → polar
- [[np.arcsin]] · [[np.arccos]] · [[np.rad2deg]]
