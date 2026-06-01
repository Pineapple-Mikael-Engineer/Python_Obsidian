---
title: np.gradient — Derivada numérica por diferencias centradas
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
retorna: ndarray o list
inplace: false

# --- Dependencias ---
requiere:
  - concepto_axis_parametro

draft: false
---

# np.gradient — Derivada numérica por diferencias centradas

## Firma de la función

```python
np.gradient(
    f,
    *varargs,
    axis=None,
    edge_order=1
) -> ndarray | list[ndarray]
```

## Valor de retorno

Aproxima la **derivada** de `f` usando diferencias centradas en el interior y de un lado en los bordes. A diferencia de [[np.diff]], **conserva la longitud** del array.

| Entrada | Salida |
|---------|--------|
| 1D de tamaño `n` | 1D de tamaño `n` |
| 2D | lista de 2 arrays (derivada por cada eje) |

```python
import numpy as np
f = np.array([1, 2, 4, 7, 11], dtype=float)
np.gradient(f)   # array([1. , 1.5, 2.5, 3.5, 4. ])
```

## Parámetros en detalle

### `f` — valores de la función

Array con los valores muestreados.

### `*varargs` — espaciado

Escalar (paso uniforme) o array de coordenadas (paso variable). Sin él, asume paso 1.

```python
x = np.array([0, 1, 4, 9])           # paso no uniforme
y = x ** 2
np.gradient(y, x)                    # usa las coordenadas reales
```

### `axis` — eje(s) sobre los que derivar

En arrays nD, por defecto deriva en **todos** los ejes y devuelve una lista.

### `edge_order` — precisión en los bordes

`1` (lineal) o `2` (cuadrática) para la aproximación en los extremos.

## Casos de uso

### Velocidad y aceleración con tiempo real

```python
t = np.linspace(0, 10, 100)
x = posicion(t)
v = np.gradient(x, t)     # velocidad
a = np.gradient(v, t)     # aceleración
```

### Gradiente espacial de un campo 2D

```python
campo = np.random.rand(50, 50)
dy, dx = np.gradient(campo)
```

## Buenas prácticas

1. Pasa el espaciado real (`varargs`) para que la derivada tenga unidades correctas.
2. Frente a [[np.diff]], `gradient` es mejor para **derivadas** (centrado, sin acortar).
3. En nD devuelve una lista (una derivada por eje): desempaqueta con cuidado.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Magnitud incorrecta | no se pasó el espaciado | pasar `dx` o las coordenadas |
| Esperar un array y recibir lista | en nD devuelve lista | indexar/desempaquetar por eje |
| Resultado entero truncado | `f` es de tipo int | convertir a `float` |

## Limitaciones

- Aproximación numérica: error en bordes y con ruido.
- En nD devuelve una lista, no un único array.

## Notas relacionadas

- [[concepto_axis_parametro]]
- [[np.diff]]
- [[np.trapz]]
