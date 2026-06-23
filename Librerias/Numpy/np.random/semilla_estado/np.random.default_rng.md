---
title: np.random.default_rng — Constructor del Generator moderno (API recomendada)
aliases:
  - default_rng
  - random.default_rng
  - np.random.default_rng
  - Generator
tags:
  - numpy
  - api/funcion
  - aleatorio
lib: numpy
mod: np.random
tipo: funcion
retorna: Generator
inplace: false
draft: false
---

# np.random.default_rng — el constructor del Generator moderno

`np.random.default_rng` es la **puerta de entrada a la API moderna de aleatoriedad** de NumPy y la forma **recomendada** desde NumPy 1.17. En vez de tocar el estado global con [[np.random.seed]] y llamar a funciones sueltas (`np.random.rand`, `np.random.normal`...), se construye **un objeto generador local** y se le piden los números:

```python
rng = np.random.default_rng(seed)   # un Generator independiente
rng.random((2, 3))                  # se le piden las muestras a ÉL
```

La idea en una frase: **deja de haber un único RNG compartido por todo el proceso**; cada `rng` lleva su propio estado encapsulado. Esto elimina el acoplamiento global (otra librería ya no puede romperte la reproducibilidad), permite tener varios generadores independientes en paralelo y usa un algoritmo mejor por debajo (**PCG64** en lugar del **Mersenne Twister** legacy).

## Firma de la función

```python
np.random.default_rng(
    seed=None,   # None | int | array_like[int] | SeedSequence | BitGenerator | Generator
) -> Generator
```

## Valor de retorno

Devuelve un objeto **`numpy.random.Generator`** respaldado por el bit generator **PCG64**. No es un array: es la fuente desde la que se generan muestras llamando a sus métodos. Dos `rng` construidos con la **misma** semilla producen **exactamente** la misma secuencia.

| `seed` | Qué hace | Reproducible |
|--------|----------|--------------|
| `None` | siembra desde entropía del SO | No |
| `int` (p. ej. `0`, `42`) | siembra determinista | Sí |
| `array_like[int]` | semilla compuesta (varios enteros) | Sí |
| `SeedSequence` | semilla ya derivada (spawning) | Sí |
| `BitGenerator` / `Generator` | reusa ese motor | según su estado |

```python
import numpy as np
rng = np.random.default_rng(0)
type(rng)            # <class 'numpy.random._generator.Generator'>
rng.random(3)
# array([0.63696169, 0.26978671, 0.04097352])
```

## Los métodos del Generator

El `Generator` reúne **toda** la familia de `np.random.*` como métodos. Los más usados:

| Método | Devuelve | Equivale (legacy) a |
|--------|----------|---------------------|
| `rng.random(size)` | uniformes en `[0, 1)` | `np.random.rand` |
| `rng.integers(low, high, size)` | enteros (`high` **excluido** por defecto) | `np.random.randint` |
| `rng.normal(loc, scale, size)` | normal general | `np.random.normal` |
| `rng.standard_normal(size)` | normal estándar N(0,1) | `np.random.randn` |
| `rng.uniform(low, high, size)` | uniforme en `[low, high)` | `np.random.uniform` |
| `rng.choice(a, size, ...)` | muestreo de un array | `np.random.choice` |
| `rng.permutation(x)` | copia permutada | [[np.random.permutation]] |
| `rng.shuffle(x)` | baraja **in-place** (devuelve `None`) | [[np.random.shuffle]] |

```python
rng = np.random.default_rng(42)
rng.integers(0, 10, size=5)      # array([0, 7, 6, 4, 4])  → high=10 excluido
rng.normal(loc=5, scale=2, size=3)
rng.choice(['a', 'b', 'c'], size=4)
```

> [!warning] `rng.integers` no es `np.random.randint`
> En la API moderna el borde superior se **excluye** por defecto (`endpoint=False`, como `range`). Para incluirlo: `rng.integers(0, 10, endpoint=True)`. La legacy `randint` ya excluía `high`, pero el nombre y la opción cambian.

## Legacy → moderno: la tabla de migración

La traducción es casi mecánica: se crea un `rng` una vez y se sustituye el prefijo `np.random.` por `rng.`.

| Legacy (estado global) | Moderno (Generator) |
|------------------------|---------------------|
| `np.random.seed(s)` | `rng = np.random.default_rng(s)` |
| `np.random.rand(...)` | `rng.random(...)` |
| `np.random.randn(...)` | `rng.standard_normal(...)` |
| `np.random.randint(a, b)` | `rng.integers(a, b)` |
| `np.random.normal(m, s)` | `rng.normal(m, s)` |
| `np.random.permutation(x)` | `rng.permutation(x)` |
| `np.random.shuffle(x)` | `rng.shuffle(x)` |
| `np.random.get_state()` | `rng.bit_generator.state` (un `dict`) |

```python
# Antes (legacy, global):
np.random.seed(0)
a = np.random.normal(0, 1, 1000)

# Después (moderno, local):
rng = np.random.default_rng(0)
a = rng.normal(0, 1, 1000)
```

## Por qué es la forma recomendada

### 1. Sin estado global → reproducibilidad por componente

[[np.random.seed]] muta un `RandomState` **único** compartido por todo el proceso. Si otra librería (o tu propio código en otro hilo) llama a `np.random.*` en medio, tu secuencia se desplaza y la reproducibilidad se rompe **en silencio**. Cada `Generator` es **independiente**: dárselo a una función la hace reproducible sin importar qué hagan las demás.

```python
def simular(rng):                  # recibe SU generador
    return rng.normal(size=100)

a = simular(np.random.default_rng(0))
b = simular(np.random.default_rng(0))
np.allclose(a, b)                  # True → aislado del resto del programa
```

### 2. Independencia para paralelo

Se pueden derivar generadores hijos garantizados como independientes (ideal para multiproceso, donde compartir el RNG global sería una condición de carrera):

```python
ss = np.random.SeedSequence(12345)
hijos = [np.random.default_rng(s) for s in ss.spawn(4)]   # 4 streams independientes
```

### 3. Mejor algoritmo (PCG64 vs Mersenne Twister)

El `Generator` usa **PCG64**: estadísticamente mejor, más rápido y con menor estado que el Mersenne Twister del `RandomState` legacy.

## Casos de uso

### Reproducibilidad de un experimento

```python
rng = np.random.default_rng(2024)
datos = rng.normal(size=1000)      # mismos 1000 valores en cada ejecución
```

### Tensor 4D para un lote de imágenes

```python
rng = np.random.default_rng(0)
batch = rng.normal(size=(2, 3, 64, 64))   # (lote, canales, alto, ancho)
batch.shape                                # (2, 3, 64, 64)
```

El [[concepto_shape|shape]] sale directo de `size`, igual que en la API legacy, pero el estado vive en `rng`, no en una variable global.

### Barajar índices de forma reproducible

```python
rng = np.random.default_rng(7)
idx = rng.permutation(len(datos))          # copia; el original intacto
train, test = idx[:800], idx[800:]
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `default_rng().seed(0)` no existe | el `Generator` **no** tiene método `seed` | pasar la semilla al construir: `default_rng(0)` |
| `rng.rand(...)` / `rng.randn(...)` fallan | esos nombres son **solo legacy** | usar `rng.random` / `rng.standard_normal` |
| `rng.integers(0, 10)` no incluye el 10 | borde superior excluido por defecto | `endpoint=True` si lo necesitas |
| Reproducibilidad sigue rota | se mezcla `rng` con `np.random.*` global | usar **solo** `rng` en esa ruta |
| Crear un `rng` nuevo dentro de un bucle | reinicia la secuencia cada vuelta | construirlo **una vez**, fuera del bucle |

## Notas relacionadas

- [[np.random.seed]] — la forma legacy (estado global) que `default_rng` reemplaza
- [[np.random.get_state]] · [[np.random.set_state]] — gestión de estado legacy frente a `rng.bit_generator.state`
- [[np.random.permutation]] · [[np.random.shuffle]] — versiones de método (`rng.permutation` / `rng.shuffle`)
- [[concepto_shape]] — el `size` que pasas a cada método
- [[concepto_aleatoriedad_rng]]
