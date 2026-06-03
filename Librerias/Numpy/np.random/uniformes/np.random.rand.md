---
title: np.random.rand — Uniforme [0,1) con dimensiones como argumentos sueltos
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
retorna: ndarray o float
inplace: false
draft: false
---

# np.random.rand — Uniforme [0,1) con dimensiones como argumentos sueltos

## Firma de la función

```python
np.random.rand(d0, d1, ..., dn) -> ndarray
# d0, d1, ... = enteros, cada uno una dimensión SUELTA (no una tupla)
```

Genera valores con distribución **uniforme continua en el intervalo `[0, 1)`** (0 incluido, 1 excluido). La diferencia crítica frente a [[np.random.random]] está en la **firma**: `rand` recibe las dimensiones como **argumentos posicionales separados**, no como un shape en tupla.

## Valor de retorno

| Entrada | Retorno | Ejemplo |
|---------|---------|---------|
| `rand()` (sin args) | `float` escalar | `0.5731...` |
| `rand(3)` | ndarray `(3,)` | `[0.12, 0.97, 0.44]` |
| `rand(2, 3)` | ndarray `(2, 3)` | matriz 2×3 |
| `rand(2, 3, 4)` | ndarray `(2, 3, 4)` | tensor 3D |

```python
import numpy as np
np.random.rand(2, 3)
# array([[0.417, 0.720, 0.000],
#        [0.302, 0.146, 0.092]])
```

## Parámetros en detalle

### `d0, d1, ..., dn` — dimensiones SUELTAS

Cada eje del [[concepto_shape|shape]] se pasa como un entero **independiente**, igual que se escribiría `shape=(d0, d1, ...)` pero **sin la tupla**.

```python
np.random.rand(5)        # (5,)      vector — NO rand((5,))
np.random.rand(3, 4)     # (3, 4)    matriz — NO rand((3, 4))
np.random.rand(2, 3, 4)  # (2, 3, 4) tensor
np.random.rand()         # escalar float
```

⚠️ **Contraste de firma (confusión nº1):** `rand` toma dimensiones sueltas; `random` toma una tupla.

| Llamada | Función | Resultado |
|---------|---------|-----------|
| `np.random.rand(2, 3)` | rand (args sueltos) | ✅ matriz `(2, 3)` |
| `np.random.rand((2, 3))` | rand con tupla | ❌ `TypeError` |
| `np.random.random((2, 3))` | random (tupla) | ✅ matriz `(2, 3)` |
| `np.random.random(2, 3)` | random con args sueltos | ❌ `TypeError` |

## Casos de uso

### Matriz de pesos iniciales

```python
W = np.random.rand(4, 4)   # pesos uniformes en [0, 1)
```

### Simulación / muestreo rápido en [0,1)

```python
muestras = np.random.rand(1000)   # 1000 valores uniformes
muestras.mean()                   # ≈ 0.5
```

### Escalar a otro rango manualmente

```python
# uniforme en [10, 20) reescalando [0,1)
x = 10 + np.random.rand(5) * 10
```

## Buenas prácticas

1. Usa `rand` cuando tengas las dimensiones **sueltas** y cómodas de escribir; si ya tienes un `shape` en variable tupla, usa [[np.random.random]] o `np.random.random(size=mi_shape)`.
2. Para un rango distinto de `[0,1)` no reescales a mano: usa directamente `np.random.uniform(low, high, size)`.
3. Fija la semilla con `np.random.seed(...)` (o un `Generator`) para reproducibilidad.
4. Para enteros aleatorios no uses `rand`; usa `np.random.randint`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `TypeError: 'tuple' object cannot be interpreted as an integer` | pasar una tupla: `rand((2, 3))` | usar args sueltos: `rand(2, 3)` |
| Esperabas rango `[low, high)` | `rand` solo da `[0, 1)` | usar `np.random.uniform` o reescalar |
| Resultados no reproducibles | sin semilla fija | `np.random.seed(0)` antes |
| Querías enteros | `rand` siempre da floats | usar `np.random.randint` |

## Notas relacionadas

- [[np.random.random]]
- [[np.random.uniform]]
- [[np.random.random_sample]]
- [[concepto_shape]]
