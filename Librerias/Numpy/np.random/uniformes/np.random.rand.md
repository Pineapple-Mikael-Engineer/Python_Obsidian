---
title: np.random.rand — uniforme [0,1) con las dimensiones como argumentos sueltos
aliases:
  - rand
  - random.rand
  - np.random.rand
tags:
  - numpy
  - api/funcion
  - aleatorio
lib: numpy
mod: np.random
tipo: funcion
retorna: ndarray | float
inplace: false
draft: false
---

# np.random.rand — uniforme [0,1) con las dimensiones como argumentos sueltos

`np.random.rand` genera valores con distribución **uniforme continua en el intervalo `[0, 1)`** (el 0 puede salir, el 1 nunca). Es la función de **conveniencia**: su única particularidad frente a [[np.random.random]] es la **firma**, porque recibe las dimensiones del array como **argumentos posicionales sueltos** (`rand(2, 3, 4)`), no como una tupla. Es un atajo de estilo MATLAB para cuando ya escribes las dimensiones a mano.

> [!tip] Versión moderna
> Esta función usa el **estado global** de `np.random` (el que fija `np.random.seed`), hoy considerado *legacy*. La API recomendada crea un generador propio y aislado con [[np.random.default_rng]]:
> ```python
> rng = np.random.default_rng()
> rng.random(size=(2, 3))   # equivalente moderno de np.random.rand(2, 3)
> ```
> `Generator` no tiene un método `rand` con dimensiones sueltas: el equivalente es `rng.random(size=...)`, que siempre toma una **tupla** en `size`.

## La idea

Muestrea cada elemento del array de forma independiente de una uniforme $U \sim \mathcal{U}[0, 1)$, de modo que todos los valores del intervalo son igualmente probables y la media tiende a $0{.}5$. El rango es **fijo**: si necesitas otro intervalo, escala a mano o usa [[np.random.uniform]].

$$ X_{i_0,\dots,i_{k-1}} \sim \mathcal{U}[0, 1) \quad \text{i.i.d., con shape } (d_0, d_1, \dots, d_{n}) $$

## Firma

```python
np.random.rand(d0, d1, ..., dn) -> ndarray | float
# d0, d1, ..., dn : int — cada uno una dimensión SUELTA del shape (no una tupla)
#                          sin argumentos → devuelve un float escalar
```

## Los parámetros en detalle

### `d0, d1, ..., dn` — las dimensiones, sueltas

Cada eje del [[concepto_shape|shape]] se pasa como un entero **independiente**, igual que se escribiría `shape=(d0, d1, ...)` pero **sin la tupla**. El número de argumentos fija el `ndim` del resultado.

```python
np.random.rand()         # float escalar
np.random.rand(5)        # (5,)       vector — NO rand((5,))
np.random.rand(3, 4)     # (3, 4)     matriz — NO rand((3, 4))
np.random.rand(2, 3, 4)  # (2, 3, 4)  tensor
```

Esta es la diferencia que más confunde: `rand` toma dimensiones **sueltas**; `random`/`uniform` toman una **tupla** en `size`. Pasarle una tupla a `rand` es un `TypeError`.

| Llamada | Función | Resultado |
|---|---|---|
| `np.random.rand(2, 3)` | rand (args sueltos) | matriz `(2, 3)` |
| `np.random.rand((2, 3))` | rand con tupla | `TypeError` |
| `np.random.random((2, 3))` | random (tupla) | matriz `(2, 3)` |
| `np.random.random(2, 3)` | random con args sueltos | `TypeError` |

## size y la forma de salida

La forma del array generado es exactamente la secuencia de argumentos `(d0, d1, ..., dn)`; cada `di` es el tamaño de un eje. Sin argumentos, el retorno es un `float` escalar (no un array `0-d`).

| Llamada | shape de salida | retorno |
|---|---|---|
| `rand()` | — | `float` escalar |
| `rand(3)` | `(3,)` | `ndarray` 1D |
| `rand(2, 3)` | `(2, 3)` | `ndarray` 2D |
| `rand(8, 3, 64, 64)` | `(8, 3, 64, 64)` | `ndarray` 4D |

Como cada dimensión es un argumento aparte, generar un tensor de muchos ejes es solo añadir números. Un **lote de imágenes** RGB de $64\times64$ (formato `(lote, canales, alto, ancho)`) son cuatro argumentos sueltos:

```python
lote = np.random.rand(8, 3, 64, 64)   # 8 imágenes, 3 canales, 64×64
lote.shape    # (8, 3, 64, 64)
lote.ndim     # 4
lote.size     # 8*3*64*64 = 98_304

# y un tensor 5D (p. ej. vídeo: lote, frames, canales, alto, ancho):
clip = np.random.rand(4, 16, 3, 64, 64)
clip.shape    # (4, 16, 3, 64, 64)
```

## Casos de uso

### Muestreo rápido en [0,1)

```python
muestras = np.random.rand(1000)   # 1000 valores uniformes
muestras.mean()                   # ≈ 0.5
```

### Matriz de pesos / ruido inicial

```python
W = np.random.rand(4, 4)   # pesos uniformes en [0, 1)
```

### Escalar a otro rango a mano

```python
# uniforme en [10, 20) reescalando [0, 1)
x = 10 + np.random.rand(5) * 10
# (preferible: np.random.uniform(10, 20, 5))
```

## Errores comunes

| Error | Causa | Solución |
|---|---|---|
| `TypeError: 'tuple' object cannot be interpreted as an integer` | pasar una tupla: `rand((2, 3))` | usar args sueltos: `rand(2, 3)` |
| Esperabas el rango `[low, high)` | `rand` solo da `[0, 1)` | usar [[np.random.uniform]] o reescalar |
| Resultados no reproducibles | sin semilla fija | `np.random.seed(0)` antes, o un `Generator` |
| Querías enteros | `rand` siempre da floats | usar [[np.random.randint]] |

## Notas relacionadas

- [[np.random.random]] — misma distribución, pero con `size` como tupla (la forma canónica)
- [[np.random.uniform]] — uniforme en un rango arbitrario `[low, high)`
- [[np.random.default_rng]] — la API moderna recomendada (`Generator`)
- [[np.random.seed]] · [[concepto_shape]]
