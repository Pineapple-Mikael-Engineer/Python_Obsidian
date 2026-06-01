---
title: ndarray.flatten — Aplanar a 1D (siempre copia)
aliases:
  - flatten
  - ndarray.flatten
tags:
  - numpy
  - api/metodo
  - shape
lib: numpy
obj: ndarray
tipo: metodo
retorna: ndarray
inplace: false
draft: false
---

# ndarray.flatten — Aplanar a 1D (siempre copia)

## Firma del método

```python
ndarray.flatten(order='C') -> ndarray
```

## Valor de retorno

Devuelve un `ndarray` **1D** con todos los elementos. A diferencia de `ravel`, **siempre devuelve una copia independiente**: escribir en el resultado nunca afecta al original.

| Entrada | Llamada | Salida |
|---------|---------|--------|
| `(2, 3)` | `arr.flatten()` | `(6,)` copia |
| cualquier shape | `arr.flatten('F')` | `(n,)` copia, orden columnas |

```python
M = np.arange(6).reshape(2, 3)
f = M.flatten()
f[0] = 99
M               # intacto → flatten copió
```

## Equivalencia con np.ravel

No existe `np.flatten`: `flatten` solo vive como **método** del array. Su análogo de función es `np.ravel`, pero con una diferencia clave de comportamiento (copia vs vista). Para el aplanado que puede devolver vista, ver [[np.ravel]].

```python
arr.flatten()          # copia SIEMPRE (solo método)
arr.ravel()            # vista si puede; copia si no
np.ravel(arr)          # idem ravel
```

## Diferencia clave: flatten vs ravel

| Aspecto | `flatten` | `ravel` |
|---------|-----------|---------|
| Retorno | **siempre copia** | vista si es posible, si no copia |
| Coste | mayor (asigna memoria) | mínimo si devuelve vista |
| Escribir afecta al original | nunca | sí cuando es vista |
| Disponible como función `np.*` | no | sí (`np.ravel`) |

## Parámetros en detalle

`order` (`'C'`, `'F'`, `'A'`, `'K'`) controla el recorrido al aplanar; mismo significado que en [[ndarray.ravel]].

## Casos de uso

```python
M = np.arange(6).reshape(2, 3)
indep = M.flatten()        # 1D seguro de modificar
indep += 100               # no toca M

# Devolver datos a un consumidor que podría mutarlos:
def exportar(a):
    return a.flatten()     # garantiza que el original queda protegido
```

## Buenas prácticas

1. Usa `flatten` cuando necesites un 1D **independiente** y seguro de modificar.
2. Si solo lees el resultado y el rendimiento importa, [[ndarray.ravel]] evita la copia.
3. No combines `flatten` con la expectativa de vista: por diseño nunca lo es.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Copia innecesaria penaliza rendimiento | `flatten` siempre copia | usar `ravel` si no necesitas independencia |
| Buscar `np.flatten(arr)` | no existe esa función | usar `arr.flatten()` o `np.ravel(arr)` |

## Notas relacionadas

- [[ndarray.ravel]]
- [[np.ravel]]
- [[concepto_views_vs_copias]]
- [[concepto_shape]]
