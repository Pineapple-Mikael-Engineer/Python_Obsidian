---
title: np.average — Media (opcionalmente ponderada)
aliases:
  - average
  - np.average
  - media ponderada
tags:
  - numpy
  - api/funcion
  - estadistica

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray o escalar
inplace: false

# --- Dependencias ---
requiere:
  - concepto_axis_parametro

draft: false
---

# np.average — Media (opcionalmente ponderada)

`np.average` es una **reducción** que colapsa un eje y devuelve su media, pero con un superpoder
que [[np.mean]] no tiene: **pesos**. Sin `weights` es exactamente la media aritmética; con
`weights` calcula la **media ponderada**, donde cada elemento contribuye en proporción a su peso.
Esa es la única diferencia conceptual con `mean`: *quién pesa más en el promedio*. Como toda
reducción, la pregunta es **"¿qué eje desaparece?"**.

## La idea en una fórmula

Promediar con pesos es sumar cada elemento multiplicado por su peso y dividir por la suma de pesos.
A lo largo del eje que se reduce (índice $i$):

**Mapa de shapes** — el eje $p$ que se reduce **desaparece** del shape (idéntico a `np.sum`):

$$ (n_0,\dots,n_k)\ \xrightarrow{\ \text{average, axis}=p\ }\ (n_0,\dots,n_{p-1},\,n_{p+1},\dots,n_k) $$

**Fórmula por índices** — media ponderada sobre el eje reducido:

$$
\bar{x}=\frac{\sum_i w_i\, x_i}{\sum_i w_i}
$$

Cuando todos los pesos son iguales, $w_i$ sale de las dos sumas y queda
$\bar{x}=\frac{1}{m}\sum_i x_i$: la media aritmética. Por eso **sin `weights`, `average` es `mean`**.
El eje del subíndice $i$ es el que se reduce y desaparece (ver [[concepto_axis_parametro]]).

## Firma

```python
np.average(
    a,                 # array_like: el tensor de entrada
    axis=None,         # None | int | tuple[int]: eje(s) a reducir
    weights=None,      # array_like | None: pesos de cada elemento
    returned=False,    # bool: si True devuelve también la suma de pesos
    keepdims=False,    # bool: conservar los ejes reducidos con tamaño 1
) -> ndarray | escalar | tuple
```

## Los parámetros en detalle

### `a` — el tensor de entrada
`array_like` (ndarray, lista, escalar). Se convierte a `ndarray` si no lo es. El resultado es
flotante (la división lo fuerza).

### `axis` — qué eje se reduce
`None` (defecto) promedia **todos** los elementos y devuelve un escalar. Un `int` reduce ese eje;
acepta tupla y ejes negativos (`axis=-1` = último eje), igual que [[np.mean]]:

```python
T = np.ones((2, 3, 4))
np.average(T, axis=None).shape   # ()      → escalar
np.average(T, axis=0).shape      # (3, 4)  → desaparece el eje 0
np.average(T, axis=-1).shape     # (2, 3)  → desaparece el último eje
```

### `weights` — los pesos (el corazón de la función)
`array_like` con el peso de cada elemento. **Su shape debe alinear con el `axis` que se promedia**,
y ahí está la trampa:
- Si `axis=None` o `weights` tiene **la misma forma que `a`**, hay un peso por elemento.
- Si das `axis=k` y un `weights` **1-D**, su longitud debe ser **exactamente `a.shape[k]`** (un
  peso por posición a lo largo de ese eje); NumPy lo difunde al resto de ejes.

Los pesos **no necesitan sumar 1**: se normalizan internamente al dividir por $\sum_i w_i$.

```python
notas = np.array([4.0, 6.0, 8.0])
pesos = np.array([1, 1, 2])           # el último vale doble
np.average(notas, weights=pesos)      # 6.5  = (4+6+16)/4

M = np.array([[1., 2., 3.],
              [4., 5., 6.]])
np.average(M, axis=0, weights=[1, 3]) # pondera las 2 filas → [3.25, 4.25, 5.25]
```

### `returned` — devolver también la suma de pesos
Si `True`, el retorno deja de ser solo el promedio y pasa a ser la **tupla `(promedio, suma_de_pesos)`**.
La suma de pesos es el denominador $\sum_i w_i$ y tiene el mismo shape que el promedio. Útil para
combinar medias ponderadas de varios lotes (promedio de promedios pesando por su masa):

```python
media, total_pesos = np.average(notas, weights=pesos, returned=True)
# media = 6.5,  total_pesos = 4.0
```

### `keepdims` — conservar el eje reducido como tamaño 1
Si `True`, el eje reducido queda con tamaño 1 para seguir siendo **broadcasteable** contra `a`
(ver [[concepto_broadcasting]]), igual que en las demás reducciones.

```python
M.average  # (no existe método; usar la función)
np.average(M, axis=1, keepdims=True).shape  # (2, 1)
```

## El eje y el caso N-D

La regla es la misma de toda reducción: **el eje de `axis` se elimina del shape**; los demás quedan
en orden. Lo propio de `average` es que `weights` debe **alinearse con ese eje**.

| `a.shape` | `axis` | `weights` válido | salida | lectura |
|-----------|--------|------------------|--------|---------|
| `(n,)` | `0`/`None` | `(n,)` | `()` escalar | media ponderada de todo |
| `(m, n)` | `0` | `(m,)` | `(n,)` | pondera las **filas**, una media por columna |
| `(m, n)` | `1` | `(n,)` | `(m,)` | pondera las **columnas**, una media por fila |
| `(m, n)` | `None` | `(m, n)` | `()` | un peso por celda, media total |
| `(b, m, n)` | `0` | `(b,)` | `(m, n)` | pondera el lote: matriz media ponderada |
| `(b, m, n)` | `-1` | `(n,)` | `(b, m)` | pondera la última dimensión |

```python
# Tensor (d0, d1, d2) = (3, 2, 4): 3 láminas; pondera las láminas (eje 0)
T = np.arange(3*2*4).reshape(3, 2, 4).astype(float)
w = np.array([1., 2., 1.])                 # la lámina central pesa doble
np.average(T, axis=0, weights=w).shape     # (2, 4)  → desaparece el eje 0
```

## Vectorización

`np.average` con pesos reemplaza el clásico bucle "suma de productos / suma de pesos". Las dos
versiones dan lo mismo, pero la vectorizada lo hace en C:

```python
# Bucle Python (lento, explícito):
def media_ponderada(x, w):
    num = 0.0
    den = 0.0
    for xi, wi in zip(x, w):
        num += wi * xi
        den += wi
    return num / den

# Vectorizado (producto elemento a elemento + dos reducciones en C):
np.average(x, weights=w)
```
Internamente es `np.sum(a * w, axis) / np.sum(w, axis)`: dos reducciones y un broadcasting de los
pesos. Mismo principio de [[concepto_vectorizacion]]: describes la operación sobre el eje, no el
bucle.

## Valor de retorno

El retorno **cambia de naturaleza según `returned`** (la desambiguación clave de esta función):

| `returned` | `axis` | `keepdims` | retorno | tipo |
|------------|--------|------------|---------|------|
| `False` | `None` | `False` | el promedio | **escalar de NumPy** (float) |
| `False` | `int`/`tuple` | `False` | el promedio | `ndarray` (float) |
| `False` | cualquiera | `True` | el promedio | `ndarray`, ejes reducidos en 1 |
| `True` | cualquiera | — | **`(promedio, suma_de_pesos)`** | `tuple` de dos elementos del mismo shape |

- El promedio es **siempre flotante** (enteros y `bool` → `float64`).
- Con `returned=True` desempaqueta siempre dos valores; ambos comparten shape y dtype.

```python
np.average([1, 2, 3, 4])                          # np.float64(2.5)   escalar
type(np.average(np.ones((2, 2)), axis=0))         # numpy.ndarray
np.average([1, 2, 3], weights=[1, 1, 4], returned=True)  # (np.float64(2.5), np.float64(6.0))
```

## Casos de uso

### Promedio ponderado por importancia
```python
notas = np.array([4.0, 6.0, 8.0])
creditos = np.array([2, 3, 5])              # cada nota pesa según sus créditos
np.average(notas, weights=creditos)         # 6.6  → nota media ponderada
```

### Precio medio ponderado por volumen
```python
precios = np.array([10.0, 20.0, 30.0])
cantidades = np.array([100, 50, 10])        # ponderar por unidades vendidas
np.average(precios, weights=cantidades)     # 13.75
```

### Combinar medias de lotes con `returned`
```python
m1, w1 = np.average([1., 2., 3.], returned=True)   # (2.0, 3.0)
m2, w2 = np.average([4., 5.], returned=True)        # (4.5, 2.0)
global_ = (m1*w1 + m2*w2) / (w1 + w2)               # media global correcta = 3.0
```

### N-D trabajado: media ponderada por feature de un lote `(b, n)`
```python
lote = np.array([[1., 2., 3.],     # muestra 0
                 [3., 4., 5.],     # muestra 1
                 [5., 6., 7.]])    # muestra 2   → shape (3, 3): 3 muestras, 3 features
pesos = np.array([1., 1., 4.])     # la muestra 2 cuenta cuádruple
np.average(lote, axis=0, weights=pesos)   # [4., 5., 6.]  → media de cada feature
# El eje 0 (las muestras) desaparece; weights tiene longitud 3 = lote.shape[0].
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `Length of weights not compatible` | shape de `weights` no alinea con el eje promediado | igualar `len(weights)` a `a.shape[axis]` |
| `Weights sum to zero, can't be normalized` | los pesos suman 0 | usar pesos con suma no nula |
| Esperaba un float y llega una tupla | `returned=True` desempaqueta dos valores | recoger `(media, pesos)` o poner `returned=False` |
| Resultado `NaN` | hay `NaN` en `a` (no hay variante `nan` ni `where`) | enmascarar antes con `weights=0` en los NaN |
| Resultado distinto de `mean` esperado | se pasaron `weights` sin querer | omitir `weights` para la media simple |

## Notas relacionadas

- [[concepto_axis_parametro]] — qué significa reducir un eje
- [[concepto_vectorizacion]] — `average` como dos reducciones y un broadcasting
- [[np.mean]] · [[np.median]] · [[np.sum]] · [[np.std]]
