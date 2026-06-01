---
title: np.linalg.pinv — Pseudo-inversa de Moore-Penrose
aliases:
  - pinv
  - linalg.pinv
  - np.linalg.pinv
tags:
  - numpy
  - api/funcion
  - algebra/matricial
lib: numpy
mod: np.linalg
tipo: funcion
retorna: ndarray
inplace: false
draft: false
---

# np.linalg.pinv — Pseudo-inversa de Moore-Penrose

## Firma de la función

```python
np.linalg.pinv(a, rcond=1e-15, hermitian=False) -> ndarray
```

## Valor de retorno

Devuelve la **pseudo-inversa de Moore-Penrose** `a⁺`, calculada mediante descomposición en valores singulares (SVD). A diferencia de [[np.linalg.inv]], funciona con matrices **no cuadradas** o **singulares**. Para una entrada de shape `(M, N)` devuelve `(N, M)`.

| Entrada | Retorno | Caso |
|---------|---------|------|
| `(M, N)` con `M > N` | `(N, M)` | sobredeterminado → solución de mínimos cuadrados |
| `(M, N)` con `M < N` | `(N, M)` | infradeterminado → solución de norma mínima |
| `(M, M)` no singular | `(M, M)` | coincide con la inversa ordinaria |
| `(M, M)` singular | `(M, M)` | inversa generalizada (sin error) |

```python
import numpy as np
A = np.array([[1., 0.],
              [0., 1.],
              [1., 1.]])     # (3, 2) → rectangular
Aplus = np.linalg.pinv(A)
Aplus.shape                  # (2, 3)
Aplus @ A                    # ≈ identidad 2×2
```

## Parámetros en detalle

### `a` — matriz de entrada

Array de shape `(..., M, N)`. No necesita ser cuadrada ni invertible. El [[concepto_shape|shape]] del resultado intercambia los dos últimos ejes: `(..., N, M)`.

### `rcond` — umbral de valores singulares

Valores singulares menores que `rcond * (mayor valor singular)` se tratan como cero. Controla la tolerancia frente al ruido numérico; subirlo regulariza problemas mal condicionados.

```python
A = np.array([[1., 1.],
              [1., 1.0000001]])   # casi singular
np.linalg.pinv(A, rcond=1e-3)     # descarta el valor singular minúsculo
```

### `hermitian` — matriz hermítica

Si `True`, asume que `a` es hermítica (simétrica si es real), usando un algoritmo más eficiente.

## Casos de uso

### Mínimos cuadrados manual

```python
A = np.array([[1., 1.],
              [1., 2.],
              [1., 3.]])
b = np.array([1., 2., 2.])
x = np.linalg.pinv(A) @ b    # solución de mínimos cuadrados
```

### Inversa de matriz singular sin error

```python
S = np.array([[1., 2.],
              [2., 4.]])     # singular
np.linalg.pinv(S)           # devuelve resultado en vez de LinAlgError
```

## Buenas prácticas

1. Para resolver mínimos cuadrados, prefiere [[np.linalg.lstsq]]: además del vector solución entrega residuos y rango, y es más estable que `pinv(A) @ b`.
2. Usa `pinv` cuando necesites la matriz pseudo-inversa explícita y reutilizable.
3. Si la matriz es cuadrada y claramente no singular, `inv` es más directo.
4. Ajusta `rcond` para regularizar datos con ruido o casi colineales.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `LinAlgError: SVD did not converge` | datos con `inf`/`NaN` o patológicos | limpiar entrada; comprobar `np.isfinite` |
| Resultado dominado por ruido | `rcond` demasiado bajo | subir `rcond` para descartar valores singulares pequeños |
| Lentitud frente a `solve` | usar `pinv` en sistema cuadrado bien definido | usar `solve` o `inv` |

## Limitaciones

- Más costosa que `inv`/`solve` por requerir una SVD completa.
- Para resolver sistemas, `lstsq`/`solve` suelen ser preferibles.

## Notas relacionadas

- [[np.linalg.lstsq]]
- [[np.linalg.inv]]
- [[np.linalg.solve]]
- [[concepto_shape]]
