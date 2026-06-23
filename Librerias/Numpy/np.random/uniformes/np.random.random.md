---
title: np.random.random — uniforme [0,1) con el shape como tupla (size)
aliases:
  - random
  - random.random
  - np.random.random
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

# np.random.random — uniforme [0,1) con el shape como tupla (size)

`np.random.random` genera valores con distribución **uniforme continua en `[0, 1)`** (el 0 puede salir, el 1 nunca), exactamente la misma distribución que [[np.random.rand]]. Lo que cambia es la **firma**: recibe **un único parámetro `size`** con el shape completo (una tupla), no dimensiones posicionales sueltas. Es la **forma canónica** de la familia y la que conviene usar por defecto.

> [!tip] Versión moderna
> Esta función opera sobre el **estado global** de `np.random` (el que fija `np.random.seed`), hoy considerado *legacy*. La API recomendada usa un generador propio creado con [[np.random.default_rng]], cuyo método `random` tiene **la misma firma `size=...`**:
> ```python
> rng = np.random.default_rng()
> rng.random(size=(2, 3))   # equivalente moderno de np.random.random((2, 3))
> ```

> [!note] Los alias `ranf` / `sample` / `random_sample` ya no existen
> `np.random.random_sample`, `np.random.ranf` y `np.random.sample` eran **alias exactos** de esta función (idéntica firma `size=None`). Se han eliminado en NumPy moderno: usa siempre `np.random.random` (o, mejor, el `Generator` moderno).

## La idea

Muestrea cada elemento de forma independiente de una uniforme $U \sim \mathcal{U}[0, 1)$; todos los valores del intervalo son igualmente probables y la media tiende a $0{.}5$. El rango es **fijo** en `[0, 1)`; para un intervalo arbitrario, [[np.random.uniform]].

$$ X_{i_0,\dots,i_{k-1}} \sim \mathcal{U}[0, 1) \quad \text{i.i.d., con shape } \texttt{size} $$

## Firma

```python
np.random.random(size=None) -> ndarray | float
# size : int | tuple[int] | None
#        — el shape completo del resultado, como entero (1D) o TUPLA (nD)
#        — None devuelve un float escalar
```

## Los parámetros en detalle

### `size` — el shape, como tupla

Único argumento. Es el [[concepto_shape|shape]] del resultado expresado como entero (para 1D) o **tupla** (para nD). Por defecto `None`, que devuelve un `float` escalar.

```python
np.random.random()           # float escalar
np.random.random(5)          # (5,)       vector
np.random.random((3, 4))     # (3, 4)     matriz — TUPLA obligatoria
np.random.random((2, 3, 4))  # (2, 3, 4)  tensor
np.random.random(size=(3,))  # forma explícita por keyword
```

Frente a [[np.random.rand]] la firma es la opuesta: aquí el shape va en **una tupla**, no en argumentos sueltos. Pasar dimensiones sueltas a `random` es un `TypeError`.

| Llamada | Función | Resultado |
|---|---|---|
| `np.random.random((2, 3))` | random (tupla) | matriz `(2, 3)` |
| `np.random.random(2, 3)` | random con args sueltos | `TypeError` |
| `np.random.rand(2, 3)` | rand (args sueltos) | matriz `(2, 3)` |
| `np.random.rand((2, 3))` | rand con tupla | `TypeError` |

## size y la forma de salida

La forma del array generado **es** `size`: la tupla que pasas se convierte literalmente en el shape de salida. Que `size` sea una tupla es justo lo cómodo cuando el shape ya vive en una variable.

| `size` | shape de salida | retorno |
|---|---|---|
| `None` | — | `float` escalar |
| `5` | `(5,)` | `ndarray` 1D |
| `(2, 3)` | `(2, 3)` | `ndarray` 2D |
| `(8, 3, 64, 64)` | `(8, 3, 64, 64)` | `ndarray` 4D |

Como `size` es una tupla, generar un tensor de muchos ejes es directo. Un **lote de imágenes** RGB de $64\times64$ (formato `(lote, canales, alto, ancho)`) es una tupla de cuatro enteros:

```python
lote = np.random.random((8, 3, 64, 64))   # 8 imágenes, 3 canales, 64×64
lote.shape    # (8, 3, 64, 64)
lote.ndim     # 4
lote.size     # 8*3*64*64 = 98_304

# y un tensor 5D (vídeo: lote, frames, canales, alto, ancho):
clip = np.random.random((4, 16, 3, 64, 64))
clip.shape    # (4, 16, 3, 64, 64)
```

## Casos de uso

### Generar a partir de un shape guardado en variable

```python
shape = (3, 4)
M = np.random.random(shape)   # cómodo: el shape ya es una tupla
```

### Muestreo en [0,1)

```python
u = np.random.random(10000)
u.mean()    # ≈ 0.5
```

### Escalar a [a, b) a mano

```python
a, b = -1, 1
x = a + (b - a) * np.random.random((2, 2))   # uniforme en [-1, 1)
# (preferible: np.random.uniform(-1, 1, (2, 2)))
```

## Errores comunes

| Error | Causa | Solución |
|---|---|---|
| `TypeError` con `random(2, 3)` | pasar dimensiones sueltas | usar tupla: `random((2, 3))` |
| Confundirla con `rand` | firmas opuestas | `rand` = sueltos, `random` = tupla |
| `ranf` / `sample` / `random_sample` no existen | eran alias ya eliminados | usar `np.random.random` |
| Esperabas `[low, high)` | solo da `[0, 1)` | usar [[np.random.uniform]] |
| Resultados no reproducibles | sin semilla | `np.random.seed(0)` antes, o un `Generator` |

## Notas relacionadas

- [[np.random.rand]] — misma distribución, pero con las dimensiones como argumentos sueltos
- [[np.random.uniform]] — uniforme en un rango arbitrario `[low, high)`
- [[np.random.default_rng]] — la API moderna recomendada (`Generator`)
- [[np.random.seed]] · [[concepto_shape]]
