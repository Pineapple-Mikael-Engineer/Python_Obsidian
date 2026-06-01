---
title: np.random.exponential — Muestras de la distribución exponencial
aliases: [exponential, random.exponential, np.random.exponential]
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

# np.random.exponential — Muestras de la distribución exponencial

Modela el **tiempo entre eventos** de un proceso de Poisson (llegadas de clientes, fallos de un componente, desintegraciones). La exponencial no tiene memoria: la probabilidad de esperar otro intervalo no depende de cuánto hayas esperado ya. Su parámetro de escala es `scale = 1/λ`, donde `λ` es la tasa media de eventos por unidad de tiempo.

## Firma de la función

```python
np.random.exponential(
    scale=1.0,
    size=None
) -> ndarray | float
```

## Valor de retorno

Devuelve valores reales no negativos extraídos de una densidad `f(x) = (1/scale)·exp(−x/scale)` para `x ≥ 0`. La media de las muestras tiende a `scale` y la varianza a `scale²`.

| Entrada | Retorno | Ejemplo |
|---------|---------|---------|
| `size=None` | `float` escalar | `0.73` |
| `size=5` | `ndarray (5,)` | `[0.2, 1.4, 0.05, 3.1, 0.9]` |
| `size=(2, 3)` | `ndarray (2, 3)` | matriz de tiempos |
| `scale=10` | valores ~10× mayores | media ≈ 10 |

```python
import numpy as np
np.random.seed(0)
np.random.exponential(scale=2.0, size=4)
# array([1.59, 2.39, 0.47, 1.78])  → media tiende a 2.0
```

## Parámetros en detalle

### `scale` — escala (inversa de la tasa)

Es `1/λ`. A mayor `scale`, eventos más espaciados (tasa baja); a menor `scale`, eventos frecuentes. Debe ser `> 0`. Acepta escalar o array (se aplica broadcasting con `size`).

```python
np.random.exponential(scale=0.5)   # tasa λ=2 eventos/unidad → esperas cortas
np.random.exponential(scale=5.0)   # tasa λ=0.2 → esperas largas
```

### `size` — forma de la salida

Entero o tupla que define el [[concepto_shape|shape]] del resultado. Con `None` devuelve un único `float`.

```python
np.random.exponential(1.0)            # escalar
np.random.exponential(1.0, size=1000) # vector (1000,)
np.random.exponential(1.0, (3, 4))    # matriz (3, 4)
```

## Casos de uso

### Simular tiempos entre llegadas en una cola

```python
# λ = 3 clientes/min → scale = 1/3 min entre llegadas
entre_llegadas = np.random.exponential(scale=1/3, size=10)
instantes = np.cumsum(entre_llegadas)   # tiempos absolutos de llegada
```

### Tiempos de vida en un estudio de fiabilidad

```python
# Componente con vida media de 5000 horas
vidas = np.random.exponential(scale=5000, size=1000)
vidas.mean()   # ≈ 5000
```

## Buenas prácticas

1. Recuerda que el parámetro es `scale = 1/λ`, **no** la tasa `λ`; es el error más común.
2. Fija la semilla con [[np.random.seed]] para resultados reproducibles en simulaciones.
3. Para el conteo de eventos en un intervalo (no el tiempo entre ellos) usa la distribución de Poisson.
4. La exponencial es el caso particular de [[np.random.gamma]] con `shape=1`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Media muy distinta a la esperada | Pasar `λ` en lugar de `1/λ` | Usar `scale=1/lambda` |
| `ValueError: scale < 0` | `scale` negativo | Garantizar `scale > 0` |
| Valores siempre iguales | Semilla fijada en bucle | Sembrar una sola vez |
| Esperar simetría | La exponencial es muy asimétrica | Es correcto: cola larga a la derecha |

## Notas relacionadas

- [[concepto_shape]]
- [[np.random.gamma]]
- [[np.random.seed]]
- [[np.random.lognormal]]
