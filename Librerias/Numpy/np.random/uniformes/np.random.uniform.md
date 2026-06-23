---
title: np.random.uniform — uniforme en un rango arbitrario [low, high)
aliases:
  - uniform
  - random.uniform
  - np.random.uniform
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

# np.random.uniform — uniforme en un rango arbitrario [low, high)

`np.random.uniform` genera valores con distribución **uniforme continua en `[low, high)`**. A diferencia de [[np.random.random]] y [[np.random.rand]] (que solo cubren `[0, 1)`), `uniform` permite un **rango arbitrario** sin reescalar a mano, y además acepta arrays en `low`/`high` para [[concepto_broadcasting|broadcasting]]. El `size` es una **tupla**, como en `random`.

> [!tip] Versión moderna
> Esta función usa el **estado global** de `np.random` (el que fija `np.random.seed`), hoy considerado *legacy*. La API recomendada usa un generador propio creado con [[np.random.default_rng]], cuyo método `uniform` tiene **la misma firma**:
> ```python
> rng = np.random.default_rng()
> rng.uniform(-1, 1, size=(2, 3))   # equivalente moderno de np.random.uniform(-1, 1, (2, 3))
> ```

## La idea

Muestrea cada elemento independientemente de una uniforme sobre el intervalo semiabierto $[low, high)$; todos los valores del rango son igualmente probables y la media tiende a $\tfrac{low + high}{2}$. Es `random` con el rango parametrizado:

$$ X \sim \mathcal{U}[low, high), \qquad X = low + (high - low)\,U, \quad U \sim \mathcal{U}[0, 1) $$

## Firma

```python
np.random.uniform(low=0.0, high=1.0, size=None) -> ndarray | float
# low  : float | array_like — límite inferior (incluido)
# high : float | array_like — límite superior (excluido)
# size : int | tuple[int] | None — el shape del resultado (tupla en nD)
```

## Los parámetros en detalle

### `low` — límite inferior (incluido)

Valor mínimo posible. Por defecto `0.0`. Puede ser un array para hacer [[concepto_broadcasting|broadcasting]] con `high` y/o `size`.

```python
np.random.uniform(low=5, high=10)   # un float en [5, 10)
```

### `high` — límite superior (excluido)

Valor máximo, **no alcanzable** (intervalo semiabierto). Por defecto `1.0`. Cuidado: si das solo `low`, `high` sigue siendo `1.0`. Si `high < low`, NumPy **no lanza error**; simplemente invierte el rango efectivo.

```python
np.random.uniform(low=5)        # [5, 1.0) → rango invertido, no lo que parece
np.random.uniform(0, 100, 4)    # 4 valores en [0, 100)
```

### `size` — el shape, como tupla

Entero (1D) o **tupla** para el [[concepto_shape|shape]] nD. Toma una tupla (como `random`), no dimensiones sueltas (como `rand`). Si `low`/`high` son arrays, `size` debe ser compatible con su broadcasting.

```python
np.random.uniform(0, 1, 5)        # (5,)
np.random.uniform(0, 1, (3, 4))   # (3, 4)
```

## size y la forma de salida

La forma del array generado es `size` (cuando `low`/`high` son escalares). Si `low` o `high` son arrays, la forma sale del **broadcasting** entre ellos y `size`.

| Llamada | shape de salida | retorno |
|---|---|---|
| `uniform()` | — | `float` en `[0, 1)` |
| `uniform(10, 20)` | — | `float` en `[10, 20)` |
| `uniform(-1, 1, 3)` | `(3,)` | `ndarray` en `[-1, 1)` |
| `uniform(0, 5, (2, 3))` | `(2, 3)` | `ndarray` en `[0, 5)` |
| `uniform(0, 1, (8, 3, 64, 64))` | `(8, 3, 64, 64)` | `ndarray` 4D |

Como `size` es una tupla, generar un tensor de muchos ejes es directo. Un **lote de imágenes** RGB de $64\times64$ (formato `(lote, canales, alto, ancho)`) con valores en `[0, 255)`:

```python
lote = np.random.uniform(0, 255, (8, 3, 64, 64))   # 8 imágenes, 3 canales, 64×64
lote.shape    # (8, 3, 64, 64)
lote.ndim     # 4
lote.size     # 8*3*64*64 = 98_304

# y un tensor 5D (vídeo: lote, frames, canales, alto, ancho):
clip = np.random.uniform(-1, 1, (4, 16, 3, 64, 64))
clip.shape    # (4, 16, 3, 64, 64)
```

## Casos de uso

### Inicializar pesos en un rango simétrico

```python
W = np.random.uniform(-0.5, 0.5, (4, 4))   # pesos centrados en 0
```

### Coordenadas aleatorias dentro de un dominio

```python
x = np.random.uniform(0, 100, 1000)   # x en [0, 100)
y = np.random.uniform(0, 50, 1000)    # y en [0, 50)
```

### Broadcasting de límites por columna

```python
lows  = np.array([0, 10, 100])
highs = np.array([1, 20, 200])
np.random.uniform(lows, highs)   # un valor por cada par (low, high)
```

## Errores comunes

| Error | Causa | Solución |
|---|---|---|
| Rango inesperado con `uniform(5)` | `high` sigue siendo `1.0` por defecto | pasar `high` explícito |
| `TypeError` con `size` suelto | `uniform(0, 1, 2, 3)` se lee mal | usar tupla: `uniform(0, 1, (2, 3))` |
| Querías enteros | `uniform` siempre da floats | usar [[np.random.randint]] |
| `high` nunca aparece | intervalo semiabierto `[low, high)` | es el comportamiento esperado |
| Resultados no reproducibles | sin semilla | `np.random.seed(0)` antes, o un `Generator` |

## Notas relacionadas

- [[np.random.random]] — uniforme en `[0, 1)` con `size` como tupla (la forma canónica)
- [[np.random.rand]] — uniforme en `[0, 1)` con las dimensiones como argumentos sueltos
- [[np.random.default_rng]] — la API moderna recomendada (`Generator`)
- [[np.random.seed]] · [[concepto_shape]]
