---
title: np.ravel — Aplanar a una dimensión
aliases:
  - ravel
  - np.ravel
  - aplanar
tags:
  - numpy
  - api/funcion
  - shape

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_shape
  - concepto_views_vs_copias

draft: false
---

# np.ravel — Aplanar a una dimensión

## Firma de la función

```python
np.ravel(
    a,
    order='C'
) -> ndarray
```

## Valor de retorno

Devuelve un [[concepto_ndarray|ndarray]] **1D** con todos los elementos de `a` en secuencia. Devuelve una [[concepto_views_vs_copias|vista]] siempre que sea posible (más eficiente que `flatten`, que siempre copia).

| Entrada | Shape entrada | Salida |
|---------|---------------|--------|
| `[[1, 2], [3, 4]]` | `(2, 2)` | `[1, 2, 3, 4]` |
| `arange(24).reshape(2,3,4)` | `(2, 3, 4)` | `(24,)` |

```python
import numpy as np
M = np.array([[1, 2, 3],
              [4, 5, 6]])
np.ravel(M)   # array([1, 2, 3, 4, 5, 6])
```

## ravel vs flatten vs reshape(-1)

| Operación | Devuelve | Copia | Nota |
|-----------|----------|-------|------|
| `np.ravel(a)` / `a.ravel()` | 1D | solo si hace falta | **vista** preferente |
| `a.flatten()` | 1D | siempre | copia independiente |
| `a.reshape(-1)` | 1D | solo si hace falta | equivalente a `ravel` |

> Usa `ravel` si te vale una vista (más rápido); usa `flatten` si necesitas una copia garantizada.

## Parámetros en detalle

### `a` — array de entrada

Array de cualquier dimensión.

### `order` — orden de recorrido

| Valor | Recorre | Resultado de `[[1,2],[3,4]]` |
|-------|---------|------------------------------|
| `'C'` (por defecto) | por filas | `[1, 2, 3, 4]` |
| `'F'` | por columnas | `[1, 3, 2, 4]` |
| `'K'` | según el layout en memoria | el más eficiente |

```python
M = np.array([[1, 2], [3, 4]])
M.ravel(order='C')   # [1, 2, 3, 4]
M.ravel(order='F')   # [1, 3, 2, 4]
```

## Casos de uso

### Recorrer todos los elementos en serie

```python
img = np.random.rand(100, 100)
for pixel in img.ravel():
    pass   # acceso lineal a los 10 000 valores
```

### Preparar para una operación 1D y reconstruir

```python
A = np.arange(12).reshape(3, 4)
plano = A.ravel()                 # vista 1D
plano[0] = 99                     # modifica también A[0,0] (es vista)
```

### Concatenar contenidos de varias matrices

```python
todo = np.concatenate([a.ravel(), b.ravel()])
```

## Buenas prácticas

1. Prefiere `ravel` sobre `flatten` salvo que necesites una copia independiente.
2. Recuerda que como **vista**, escribir en el resultado afecta al original.
3. Para añadir dimensiones (lo contrario), usa [[np.reshape]] o [[np.expand_dims]].
4. `order='K'` da el recorrido más rápido cuando el orden lógico no importa.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| El original se modificó | `ravel` devolvió vista | usar `a.flatten()` o `a.ravel().copy()` |
| Orden inesperado tras venir de Fortran/MATLAB | `order='C'` por defecto | usar `order='F'` |
| Esperar 2D y recibir 1D | `ravel` siempre aplana del todo | usar `reshape` para forma intermedia |

## Limitaciones

- Siempre produce 1D; no permite aplanados parciales (para eso, `reshape`).
- Como puede ser vista, no garantiza independencia de memoria.

## Notas relacionadas

- [[concepto_shape]]
- [[concepto_views_vs_copias]]
- [[np.reshape]]
- [[np.expand_dims]]
- [[np.squeeze]]
