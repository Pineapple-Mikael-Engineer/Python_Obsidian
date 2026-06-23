---
title: np.trapz — integral por la regla del trapecio (reduce el eje)
aliases:
  - trapz
  - np.trapz
  - trapezoid
  - integral
  - regla del trapecio
tags:
  - numpy
  - api/funcion
  - reducciones

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray | escalar
inplace: false

# --- Dependencias ---
requiere:
  - concepto_axis_parametro
  - concepto_vectorizacion

draft: false
---

# np.trapz — integral por la regla del trapecio (reduce el eje)

`np.trapz` aproxima la **integral** (área bajo la curva) de una función muestreada mediante la
**regla del trapecio**: une los puntos con segmentos rectos y suma las áreas de los trapecios. Es
una **reducción**, como [[np.sum]]: el eje integrado **desaparece** del shape, colapsándose a un
valor por cada combinación de los ejes restantes. Frente a [[np.diff]] (que acorta) y a
[[np.gradient]] (que conserva), `trapz` es la que de verdad **elimina** el eje.

> [!important] Renombrada en NumPy 2.0
> Desde NumPy 2.0 la función se llama **`np.trapezoid`** y `np.trapz` queda **deprecada** (mismo
> comportamiento, alias mantenido por compatibilidad). En código nuevo usa `np.trapezoid`.

## La idea en una fórmula

Cada par de puntos consecutivos aporta el área de un trapecio (semisuma de alturas por la base):

$$ \int y\,dx \approx \sum_i \frac{y_i+y_{i+1}}{2}\,\Delta x_i $$

donde $\Delta x_i$ es la separación entre muestras (constante si das `dx`, variable si das `x`).

**El mapa de shapes.** Como toda reducción, el eje `axis=p` **se elimina** del shape; los demás
quedan en orden:

$$ (n_0,\dots,n_p,\dots,n_k)\ \xrightarrow{\ \text{trapz, axis}=p\ }\ (n_0,\dots,n_{p-1},\,n_{p+1},\dots,n_k) $$

Visual sobre un vector de 4 puntos (`dx=1`):

```
y = [ 0   1   2   3 ]                 shape (4,)
      └─┬─┘ └─┬─┘ └─┬─┘
       0.5  1.5  2.5     trapecios → suma = 4.5   shape ()  ← el eje desaparece
```

## Firma

```python
np.trapz(           # (NumPy ≥ 2.0: np.trapezoid, misma firma)
    y,              # array_like: las alturas (valores de la función)
    x=None,         # array_like | None: coordenadas del muestreo (espaciado variable)
    dx=1.0,         # escalar: espaciado uniforme (se ignora si se pasa x)
    axis=-1,        # int: eje a lo largo del que se integra
) -> ndarray | escalar
```

## Los parámetros en detalle

### `y` — las alturas muestreadas
`array_like` con los valores de la función a integrar a lo largo de `axis`. Se promueve a `float`
para el cálculo. Es el único argumento obligatorio; sin `x` ni `dx` asume paso `1`.

### `x` — coordenadas (espaciado variable)
`array_like` de las posiciones donde se muestreó `y`. Si se da, define el ancho **real** de cada
trapecio y **tiene prioridad** sobre `dx`. Debe poder alinearse con `y` a lo largo del eje (misma
longitud en ese eje; 1D se broadcastea a las filas). Si `x` es **decreciente**, el área sale con
signo negativo (los $\Delta x_i$ son negativos).

```python
x = np.linspace(0, np.pi, 100)
y = np.sin(x)
np.trapz(y, x)        # ≈ 2.0  → integral de sin en [0, π], con espaciado real
```

### `dx` — espaciado uniforme
Escalar con el paso constante entre muestras, usado **solo cuando `x` es `None`**. Por defecto `1.0`.
Escala el resultado: el área es proporcional a `dx`.

```python
y = np.array([0., 1., 2., 3.])
np.trapz(y)          # 4.5   (dx=1)
np.trapz(y, dx=0.5)  # 2.25  → mitad del paso, mitad del área
```

### `axis` — eje de integración
Por defecto `-1` (el **último** eje). Es el eje que se integra y, por tanto, el que **desaparece**
del shape. Los demás se conservan: se integra una curva por cada combinación de ellos. Ver
[[concepto_axis_parametro]]. Acepta ejes negativos.

```python
M = np.array([[0., 1., 2.],
              [0., 2., 4.]])
np.trapz(M, axis=1)   # [2., 4.]  → una integral por fila (el eje 1 desaparece)
np.trapz(M, axis=0)   # [0., 1.5, 3.]  → integra por columna (el eje 0 desaparece)
```

## El eje y el caso N-D

La regla es la de cualquier reducción: **el eje de `axis` se elimina**; los demás quedan en orden.
Léelo como "para cada combinación de los ejes que sobreviven, integro la curva a lo largo del eje
elegido".

| `y.shape` | `axis` | salida | lectura |
|-----------|--------|--------|---------|
| `(m,)` | `-1`/`0` | `()` escalar | integral de la curva |
| `(r, c)` | `1` | `(r,)` | una integral por **fila** |
| `(r, c)` | `0` | `(c,)` | una integral por **columna** |
| `(b, t)` | `1` | `(b,)` | integral de cada serie del lote |
| `(b, m, n)` | `-1` | `(b, m)` | integra el último eje |

```python
# Lote de 3 señales de 5 muestras:  (3, 5)
S = np.array([[0., 1., 2., 3., 4.],
              [0., 0., 0., 0., 0.],
              [4., 3., 2., 1., 0.]])
np.trapz(S, axis=1)    # [8., 0., 8.]  → el eje de tiempo (5) desaparece; un área por señal
np.trapz(S, axis=1).shape   # (3,)
```

## Vectorización

`np.trapz` reemplaza el bucle de acumular áreas de trapecios. Internamente es una resta de vistas
desplazadas (las bases $\Delta x$) multiplicada por la semisuma de alturas, reducida con un
[[np.sum]] sobre el eje, todo en C:

```python
# Bucle Python (lento, explícito):
def trapecio(y, dx=1.0):
    total = 0.0
    for i in range(len(y) - 1):
        total += (y[i] + y[i+1]) / 2 * dx
    return total

# Vectorizado (lo que hace trapz sobre el último eje, dx=1):
np.sum((y[1:] + y[:-1]) / 2)
```
Es el principio de [[concepto_vectorizacion]]: describes la integral sobre el eje entero, y NumPy
recorre las rebanadas en C. Generaliza a N-D integrando cada "fila" del eje elegido a la vez.

## Valor de retorno

El tipo del retorno **depende de `axis` y del `ndim`** de `y`:

| Entrada (shape) | `axis` | salida (shape) | tipo |
|-----------------|--------|----------------|------|
| `(m,)` | cualquiera | `()` | **escalar de NumPy** (`np.float64`) |
| `(r, c)` | `1` | `(r,)` | `ndarray` |
| `(r, c)` | `0` | `(c,)` | `ndarray` |
| `(d0,…,dk)` | `p` | shape sin el eje `p` | `ndarray` |

El `dtype` de salida es de coma flotante (`float64` salvo que `y`/`x` sean `float32`). Como `np.sum`,
integrar una entrada 1D devuelve un **escalar**, no un `ndarray`.

```python
np.trapz([0., 1., 2., 3.])              # np.float64(4.5)  → escalar
type(np.trapz(np.ones((2, 4)), axis=1)) # numpy.ndarray    → (2,)
```

## Casos de uso

### Energía / trabajo a partir de una curva de potencia
```python
tiempo = np.linspace(0, 10, 500)
potencia = np.full_like(tiempo, 3.0)
energia = np.trapz(potencia, tiempo)    # ≈ 30  → área = potencia × tiempo
```

### Área bajo una curva ROC (AUC)
```python
fpr = np.array([0., 0.1, 0.4, 1.0])
tpr = np.array([0., 0.6, 0.8, 1.0])
auc = np.trapz(tpr, fpr)                # área bajo la curva ROC
```

### Espaciado uniforme con dx
```python
y = np.sin(np.linspace(0, np.pi, 1000))
np.trapz(y, dx=np.pi/999)               # ≈ 2.0
```

### N-D: integrar cada fila de una matriz
```python
M = np.array([[0., 1., 2., 3.],     # ∫ ≈ 4.5
              [3., 2., 1., 0.]])    # ∫ ≈ 4.5
np.trapz(M, axis=1)                 # [4.5, 4.5]  → el eje 1 (4 puntos) desaparece
```

### Espaciado por eje con coordenadas compartidas
```python
x = np.array([0., 1., 3., 6.])          # mismo muestreo para ambas filas
Y = np.array([[0., 1., 1., 0.],
              [1., 1., 1., 1.]])
np.trapz(Y, x, axis=1)                  # un área por fila usando las x reales
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultado mal escalado | no se pasó `x`/`dx` correcto | indicar el espaciado real |
| Signo del área negativo | `x` decreciente | ordenar `x` ascendente o tomar `abs` |
| `x` y `y` no alinean | distinta longitud en el eje | igualar longitudes o ajustar `axis` |
| Baja precisión | pocos puntos (trapecios anchos) | aumentar el muestreo |
| `DeprecationWarning` | `np.trapz` deprecada en NumPy ≥ 2.0 | usar `np.trapezoid` |

## Notas relacionadas

- [[concepto_axis_parametro]] — el eje integrado desaparece (reducción)
- [[concepto_vectorizacion]] — la suma de trapecios sobre el eje completo
- [[np.gradient]] — la operación inversa (derivación numérica)
- [[np.diff]] · [[np.cumsum]] (suma acumulada, integral discreta sin promediar)
