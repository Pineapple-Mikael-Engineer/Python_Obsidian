---
title: np.gradient — derivada numérica por diferencias centradas (conserva el shape)
aliases:
  - gradient
  - np.gradient
  - derivada numerica
tags:
  - numpy
  - api/funcion
  - reducciones

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray | list[ndarray]
inplace: false

# --- Dependencias ---
requiere:
  - concepto_axis_parametro
  - concepto_vectorizacion

draft: false
---

# np.gradient — derivada numérica por diferencias centradas (conserva el shape)

`np.gradient` aproxima la **derivada** de una función muestreada usando **diferencias centradas** en
el interior y diferencias de un lado en los bordes. A diferencia de [[np.diff]] (que acorta el eje),
`gradient` **conserva el shape** de la entrada: devuelve una derivada por cada punto, alineada con
él. En N-D devuelve **una derivada parcial por cada eje** —una **lista de arrays**—, lo que lo
convierte en el camino directo al gradiente de un campo.

## La idea en una fórmula

En un punto interior, con espaciado $h$, la diferencia centrada es de segundo orden de precisión:

$$ \frac{\partial f}{\partial x}\Big|_i \approx \frac{f_{i+1}-f_{i-1}}{2h} $$

En los bordes no hay vecino a un lado, así que usa una diferencia de un lado (de orden 1 o 2 según
`edge_order`). Con coordenadas no uniformes, el denominador deja de ser $2h$ y se ajusta al
espaciado real de cada tramo.

**El mapa de shapes.** `gradient` **conserva el shape**; lo que cambia es *cuántos* arrays devuelve.
Para un eje (1D, o `axis=p` fijo) la salida es un único array del mismo shape:

$$ (n_0,\dots,n_k)\ \xrightarrow{\ \text{gradient, axis}=p\ }\ (n_0,\dots,n_k) $$

Sin fijar `axis` en un array de `ndim` ejes, deriva en **todos** y devuelve una **lista de `ndim`
arrays**, cada uno con el shape completo:

$$ (n_0,\dots,n_k)\ \xrightarrow{\ \text{gradient}\ }\ \big[\,G_0,\,G_1,\,\dots,\,G_k\,\big],\quad G_j.\text{shape}=(n_0,\dots,n_k) $$

Visual sobre un vector de 5 puntos (paso 1):

```
f = [ 1   2   4   7   11 ]                       shape (5,)
        ↑borde  ↑centrada (4-1)/2  ...  ↑borde
G = [ 1.   1.5   2.5   3.5   4. ]                shape (5,)   ← mismo tamaño
```

## Firma

```python
np.gradient(
    f,             # array_like: los valores muestreados de la función
    *varargs,      # escalar(es) o array(s): espaciado o coordenadas por eje
    axis=None,     # None | int | tuple[int]: eje(s) sobre los que derivar
    edge_order=1,  # 1 | 2: orden de la aproximación en los bordes
) -> ndarray | list[ndarray]
```

## Los parámetros en detalle

### `f` — los valores de la función
`array_like` con las muestras de la función sobre una rejilla. Se trata como `float`: si pasas
enteros, NumPy promueve a `float64` para la división, así que el resultado **no** se trunca. Es el
único argumento posicional obligatorio.

### `*varargs` — espaciado o coordenadas (uno por eje)
Define la distancia entre muestras, y es lo que da **unidades físicas** a la derivada. Tres formas:
- **nada** → asume paso `1` en todos los ejes.
- **un escalar** → paso uniforme común; con varios escalares, un paso por eje.
- **un array 1D de coordenadas** por eje → muestreo **no uniforme** (cada tramo con su propio $h$).

```python
x = np.array([0., 1., 4., 9.])   # paso NO uniforme
y = x**2
np.gradient(y, x)                # ≈ [1., 4., 9., 16.]  → ~2x, usa las coordenadas reales
np.gradient(y, 2.0)              # paso uniforme = 2.0 (escalar)
```
El número de `varargs` debe coincidir con el de ejes derivados (1 si das `axis=int`; `ndim` si no).

### `axis` — eje(s) sobre los que derivar
`None` (defecto) deriva en **todos** los ejes → lista de `ndim` arrays. Un `int` deriva solo en ese
eje → **un único array**. Una **tupla** deriva en ese subconjunto → lista de ese tamaño. Acepta ejes
negativos. Ver [[concepto_axis_parametro]] (aquí `axis` **no reduce**: dirige la derivada).

```python
campo = np.random.rand(4, 5)
np.gradient(campo, axis=0).shape   # (4, 5)   un solo array (derivada en el eje 0)
len(np.gradient(campo))            # 2        lista: derivada por cada eje
```

### `edge_order` — precisión en los bordes
`1` (defecto) usa una diferencia de un lado de primer orden en los extremos; `2` usa una fórmula de
segundo orden (más precisa cerca del borde, exige al menos 3 puntos en el eje). En el **interior**
no cambia nada (siempre centrada).

```python
f = np.array([0., 1., 8., 27.])      # ~ x**3
np.gradient(f, edge_order=1)         # bordes de 1er orden
np.gradient(f, edge_order=2)         # bordes de 2º orden (mejor en los extremos)
```

## El eje y el caso N-D

`axis` aquí **dirige** la derivada, no la reduce: el shape se mantiene en todos los casos. Lo único
que varía es si recibes **un array** (eje fijo) o una **lista** (varios ejes).

| `f.shape` | `axis` | salida | qué es |
|-----------|--------|--------|--------|
| `(n,)` | `None` o `0` | **1 array** `(n,)` | derivada de la serie |
| `(r, c)` | `0` | **1 array** `(r, c)` | $\partial f/\partial(\text{eje 0})$ |
| `(r, c)` | `1` | **1 array** `(r, c)` | $\partial f/\partial(\text{eje 1})$ |
| `(r, c)` | `None` | **lista de 2** arrays `(r, c)` | `[d/d_eje0, d/d_eje1]` |
| `(d0, d1, d2)` | `None` | **lista de 3** arrays `(d0, d1, d2)` | gradiente en 3D |

```python
# Campo escalar 2D z = x^2 + y^2 sobre una rejilla:
y, x = np.mgrid[0:3, 0:4].astype(float)
z = x**2 + y**2
gy, gx = np.gradient(z)        # ¡orden eje 0 (filas=y), luego eje 1 (cols=x)!
gx   # ≈ 2x por columna        gy   # ≈ 2y por fila
```
Atención al **orden de la lista**: sigue el orden de los ejes (`eje 0`, `eje 1`, ...), que en una
rejilla suele ser `(y, x)`, no `(x, y)`.

## Vectorización

`np.gradient` reemplaza el bucle de aplicar la fórmula centrada punto a punto. Internamente combina
**vistas desplazadas** del array (`f[2:] - f[:-2]`) más el tratamiento especial de los dos bordes,
todo en C:

```python
# Bucle Python (lento, explícito), interior con paso h=1:
def grad1d(f):
    g = np.empty_like(f, dtype=float)
    g[0]  = f[1] - f[0]            # borde izq (un lado)
    g[-1] = f[-1] - f[-2]         # borde der (un lado)
    for i in range(1, len(f) - 1):
        g[i] = (f[i+1] - f[i-1]) / 2   # centrada
    return g

# Vectorizado (interior de una sola vez):
g_interior = (f[2:] - f[:-2]) / 2      # lo que hace gradient en el interior
```
Es el principio de [[concepto_vectorizacion]]: describes la derivada sobre el eje entero; NumPy
recorre las rebanadas en C. Generaliza a N-D aplicando lo mismo eje por eje.

## Valor de retorno

El tipo de retorno **depende de `axis`** (y por eso conviene desambiguarlo):

| Entrada | `axis` | retorno | shape de cada array |
|---------|--------|---------|---------------------|
| `(n,)` | cualquiera | **1 `ndarray`** | `(n,)` |
| `(r, c)` | `int` | **1 `ndarray`** | `(r, c)` |
| `(r, c)` | `None` | **`list` de 2 `ndarray`** | `(r, c)` cada uno |
| `(d0,…,dk)` | `None` | **`list` de `ndim` `ndarray`** | `(d0,…,dk)` cada uno |
| `(d0,…,dk)` | `tuple` de `m` ejes | **`list` de `m` `ndarray`** | shape completo |

El `dtype` es siempre de coma flotante (`float64` por defecto, o el float de `f`). Regla práctica:
**1 array si derivas un solo eje; lista si derivas varios** (incluido el `axis=None` en N-D).

```python
g = np.gradient(np.arange(5.))      # ndarray (1D → un solo eje)
gs = np.gradient(np.ones((3, 3)))   # list (2D, axis=None → 2 arrays)
type(g), type(gs)                   # (numpy.ndarray, list)
```

## Casos de uso

### Velocidad y aceleración con tiempo real
```python
t = np.linspace(0, 10, 100)
x = np.sin(t)
v = np.gradient(x, t)     # dx/dt  → coseno aproximado
a = np.gradient(v, t)     # d²x/dt² → derivando otra vez
```

### Derivada con muestreo no uniforme
```python
x = np.array([0., 0.5, 2., 5.])
y = x**2
np.gradient(y, x)         # usa el espaciado real de cada tramo (≈ 2x)
```

### Gradiente espacial de un campo 2D
```python
campo = np.random.rand(50, 50)
dy, dx = np.gradient(campo)     # parciales en eje 0 (filas) y eje 1 (columnas)
magnitud = np.hypot(dx, dy)     # |∇campo| en cada punto
```

### Derivar solo a lo largo de un eje (sin la lista)
```python
imgs = np.random.rand(8, 32, 32)      # lote de 8 imágenes
d_x = np.gradient(imgs, axis=2)       # 1 array (8,32,32): derivada horizontal
```

### N-D con valores concretos: campo z = x² + y²
```python
y, x = np.mgrid[0:3, 0:3].astype(float)
z = x**2 + y**2
gy, gx = np.gradient(z)
gx
# [[0., 1., 2.],     → ∂z/∂x ≈ 2x por columna (bordes de un lado)
#  [0., 1., 2.],
#  [0., 1., 2.]] * 2  (aprox; centrada da 2x en el interior)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Magnitud de la derivada incorrecta | no se pasó el espaciado real | pasar `dx` (escalar) o las coordenadas |
| Esperar un array y recibir una lista | en N-D con `axis=None` devuelve lista | fijar `axis=int` o desempaquetar por eje |
| Orden de las parciales invertido | la lista sigue el orden de ejes (`y, x`) | recordar `gy, gx = np.gradient(z)` |
| `edge_order=2` falla | menos de 3 puntos en el eje | usar `edge_order=1` o más muestras |
| Nº de `varargs` no coincide | un espaciado por cada eje derivado | dar tantos como ejes (o `axis=int`) |

## Notas relacionadas

- [[concepto_axis_parametro]] — aquí `axis` dirige la derivada, no reduce
- [[concepto_vectorizacion]] — la fórmula centrada sobre el eje completo
- [[np.diff]] — diferencia cruda que **acorta** el eje (sin centrar)
- [[np.trapz]] — la operación inversa (integración numérica)
