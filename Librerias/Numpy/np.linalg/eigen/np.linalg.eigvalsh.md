---
title: np.linalg.eigvalsh — Solo autovalores de matriz simétrica o Hermitiana
aliases:
  - eigvalsh
  - linalg.eigvalsh
  - np.linalg.eigvalsh
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

# np.linalg.eigvalsh — Solo autovalores de matriz simétrica o Hermitiana

## Firma de la función

```python
np.linalg.eigvalsh(a, UPLO='L') -> ndarray
```

Donde `a` es una matriz **simétrica** (real) o **Hermitiana** (compleja) de [[concepto_shape|shape]] `(..., M, M)`. Es la versión barata de [[np.linalg.eigh]] cuando no necesitas los autovectores.

## Valor de retorno

Devuelve **un solo `ndarray`** (no una tupla): los autovalores. Por ser la matriz simétrica/Hermitiana, son **reales** y vienen en **orden ascendente**.

| Salida | Shape | Contenido |
|--------|-------|-----------|
| `w` | `(..., M)` | Autovalores **reales**, en orden **ascendente** |

```python
import numpy as np
a = np.array([[2.0, 1.0],
              [1.0, 2.0]])          # simétrica
np.linalg.eigvalsh(a)   # array([1., 3.])  → reales y ascendentes
```

## Parámetros en detalle

### `a` — matriz simétrica/Hermitiana

Array de shape `(..., M, M)`, posiblemente apilado. Solo se lee el triángulo indicado por `UPLO`.

```python
lote = np.random.rand(4, 3, 3)
sim = lote + lote.transpose(0, 2, 1)   # forzar simetría por matriz
np.linalg.eigvalsh(sim).shape          # (4, 3)
```

### `UPLO` — triángulo a usar (`'L'` o `'U'`)

`'L'` (por defecto) lee el triángulo **inferior**; `'U'` el **superior**. El otro se ignora asumiendo simetría.

## Casos de uso

| Caso | Idea |
|------|------|
| Test de definida positiva | Todos `w > 0` ⇒ definida positiva (sin calcular autovectores) |
| Número de condición | `w[-1] / w[0]` (mayor / menor) en matriz SPD |
| Inercia / espectro | Contar autovalores positivos, negativos y nulos |
| Energías propias | Niveles de energía de un Hamiltoniano Hermitiano |

```python
# ¿Es la covarianza definida positiva?
C = np.cov(np.random.rand(50, 4), rowvar=False)
np.all(np.linalg.eigvalsh(C) > 0)   # True → definida positiva
```

## Buenas prácticas

1. Si la matriz es simétrica/Hermitiana y solo necesitas autovalores, usa `eigvalsh` (no [[np.linalg.eigvals]]): reales, ordenados, más estable.
2. El **menor** autovalor es `w[0]` y el **mayor** `w[-1]` (orden ascendente garantizado).
3. Para obtener también los autovectores, cambia a [[np.linalg.eigh]].
4. Evita `eigvals`/`eig` en matrices simétricas: pueden devolver complejos espurios y no ordenan.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `LinAlgError: Last 2 dimensions must be square` | matriz no cuadrada | verificar shape `(..., M, M)` |
| Esperar una tupla `(w, v)` | `eigvalsh` devuelve solo `w` | usar [[np.linalg.eigh]] para autovectores |
| Resultado distinto al esperado | matriz no simétrica; medio triángulo ignorado | asegurar simetría o usar `eigvals` |
| Buscar el máximo en `w[0]` | orden **ascendente** | el máximo es `w[-1]` |

## Notas relacionadas

- [[np.linalg.eigh]]
- [[np.linalg.eigvals]]
- [[np.linalg.eig]]
- [[concepto_shape]]
