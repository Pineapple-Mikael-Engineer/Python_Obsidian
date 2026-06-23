---
title: np.linspace — num puntos equiespaciados en [start, stop]
aliases:
  - linspace
  - np.linspace
tags:
  - numpy
  - api/funcion
  - creacion

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_shape
  - concepto_dtype

draft: false
---

# np.linspace — num puntos equiespaciados en [start, stop]

`np.linspace` genera **exactamente `num` puntos equiespaciados** entre `start` y `stop`. A diferencia
de [[np.arange]], aquí controlas el **número de puntos**, no el paso, y el extremo `stop` **sí se
incluye** por defecto (`endpoint=True`). Es la función idiomática para **muestrear un intervalo
continuo**: el eje X de una gráfica, los puntos de evaluación de una función, los bordes de bins.

## La idea

`np.linspace` reparte `num` puntos de forma uniforme sobre el intervalo **cerrado** $[start, stop]$.
El paso queda determinado por el número de puntos: hay `num` puntos pero `num-1` intervalos entre
ellos, así que

$$ a_k = start + k\cdot\Delta,\quad \Delta = \frac{stop - start}{num - 1},\quad k = 0,\dots,num-1 $$

cuando `endpoint=True`. El resultado es siempre un vector 1D de [[concepto_shape|shape]] $(num,)$:

$$ start,\ stop,\ num \;\xrightarrow{\ \text{linspace}\ }\; (num,) $$

Como la cuenta de puntos es exacta, **no hay error de redondeo** en el número de elementos (la
debilidad de `arange` con pasos flotantes). Si en cambio `endpoint=False`, el último punto sería
`stop` y se omite, repartiendo en `num` intervalos: $\Delta = (stop - start)/num$.

## Firma

```python
np.linspace(
    start,              # escalar | array_like: primer valor (incluido)
    stop,               # escalar | array_like: último valor (incluido si endpoint=True)
    num=50,             # int ≥ 0: cantidad de puntos a generar
    endpoint=True,      # bool: incluir stop como último punto
    retstep=False,      # bool: devolver también el paso Δ
    dtype=None,         # dtype: tipo de salida; por defecto float64
    axis=0,             # int: eje donde colocar los num puntos si start/stop son arrays
) -> ndarray  |  (ndarray, float)
```

## Los parámetros en detalle

### `start`, `stop` — extremos del intervalo
Primer y último valor. Con `endpoint=True` (defecto), `stop` aparece en el resultado. Pueden ser
**arrays**: en ese caso `linspace` interpola entre los extremos elemento a elemento y produce un
array N-D (ver `axis` y la sección N-D).

### `num` — cantidad de puntos
Entero `≥ 0`. Define directamente el shape de salida `(num,)`. Recuerda: son **puntos**, no
intervalos (hay `num-1` intervalos con `endpoint=True`).

```python
np.linspace(0, 1, 11)   # 11 puntos: 0.0, 0.1, ..., 1.0
np.linspace(0, 1, 1)    # [0.]  → un solo punto (el start)
np.linspace(0, 1, 0)    # []    → array vacío
```

### `endpoint` — incluir el extremo
Si `True` (defecto), `stop` es el último punto. Si `False`, `stop` queda **fuera** y el muestreo se
reparte en `num` intervalos; idiomático para señales **periódicas** (no duplicar el extremo del ciclo)
y para bordes de bins.

```python
np.linspace(0, 1, 5)                  # [0., 0.25, 0.5, 0.75, 1.]
np.linspace(0, 1, 5, endpoint=False)  # [0., 0.2, 0.4, 0.6, 0.8]
np.linspace(0, 2*np.pi, 4, endpoint=False)  # fases sin repetir el ciclo
```

### `retstep` — devolver también el paso
Si `True`, el retorno pasa a ser la **tupla** `(array, paso)`, con `paso` $=\Delta$. Útil cuando se
necesita la resolución del muestreo (p. ej. integración numérica, donde $\Delta$ es el `dx`).

```python
valores, paso = np.linspace(0, 1, 5, retstep=True)
paso   # 0.25
```

### `dtype` — tipo de salida
Por defecto `float64`, **aunque los extremos sean enteros** (`np.linspace(0, 10, 3)` da floats). Se
puede forzar con `dtype` (ver [[concepto_dtype]]).

### `axis` — eje donde colocar los puntos (con start/stop array)
Cuando `start`/`stop` son arrays, controla en qué eje del resultado se inserta la dimensión de los
`num` puntos. `axis=0` (defecto) la pone primera; `axis=-1` la pone última.

## El caso N-D

Con `start` y `stop` **escalares**, el resultado es siempre 1D `(num,)`. Para tensores hay dos vías.

**(a) Reshape de un linspace 1D** — fabricar un eje continuo y reorganizarlo:

```python
T = np.linspace(0, 1, 24).reshape(2, 3, 4)   # tensor (2,3,4) con valores en [0,1]
```

**(b) `start`/`stop` como arrays** — `linspace` interpola **por cada par de extremos** e inserta el
eje de `num` puntos según `axis`. Si `start` y `stop` tienen shape $S$, el mapa es:

$$ \text{start},\text{stop de shape } S,\ num \;\xrightarrow{\ \text{linspace, axis}=p\ }\; (S \text{ con } num \text{ insertado en la posición } p) $$

```python
# Interpolar entre dos vectores de 3 componentes en 5 pasos:
ini = np.array([0., 0., 0.])
fin = np.array([1., 10., 100.])
rampa = np.linspace(ini, fin, 5)        # axis=0 → shape (5, 3)
rampa.shape                              # (5, 3): 5 puntos, cada uno un vector (3,)

# Construir un tensor 3D rampa con el eje de muestreo al final:
A = np.zeros((2, 3))
B = np.ones((2, 3))
vol = np.linspace(A, B, 8, axis=-1)      # shape (2, 3, 8)
vol.shape                                # (2, 3, 8)
```

El segundo caso es un ejemplo de **dimensión alta** habitual: se interpola entre dos matrices `(2,3)`
y se obtiene un volumen `(2, 3, 8)` donde el último eje recorre los 8 pasos de la rampa.

## Casos de uso

### Eje X para graficar una función continua
```python
x = np.linspace(0, 2*np.pi, 200)   # suave, 200 puntos
y = np.sin(x)
```

### Interpolar entre dos valores
```python
pasos = np.linspace(10.0, 50.0, 5)   # [10., 20., 30., 40., 50.]
```

### Bordes de bins sin solapamiento
```python
bins = np.linspace(0, 1, 11)         # 10 intervalos iguales en [0, 1]
```

### Construir una rejilla con meshgrid
```python
x = np.linspace(-1, 1, 100)
y = np.linspace(-1, 1, 100)
X, Y = np.meshgrid(x, y)             # rejilla 100x100 para evaluar f(x, y)
```

### Tensor N-D interpolado (dimensión alta)
```python
A, B = np.zeros((4, 4)), np.ones((4, 4))
vol = np.linspace(A, B, 16, axis=-1)   # (4, 4, 16): 16 láminas interpoladas
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Un punto de más al concatenar ciclos | `endpoint=True` duplica el extremo | usar `endpoint=False` |
| `num` tratado como el paso | confundirlo con [[np.arange]] | `num` = cantidad de puntos, no el paso |
| El paso no es el esperado | hay `num-1` intervalos, no `num` | usar `retstep=True` para leer el $\Delta$ real |
| Resultado vacío | `num=0` | usar `num ≥ 1` |
| Esperaba enteros y salen floats | el dtype por defecto es `float64` | pasar `dtype=int` (con cuidado del redondeo) |

## Notas relacionadas

- [[concepto_shape]] — el resultado es `(num,)` (o N-D con start/stop array)
- [[concepto_dtype]] — por qué sale `float64` por defecto
- [[np.arange]] — cuando controlas el paso en vez del número de puntos
- [[np.logspace]] — la versión en escala logarítmica
- [[np.meshgrid]] — combinar varios `linspace` en una rejilla
- [[np.array]]
