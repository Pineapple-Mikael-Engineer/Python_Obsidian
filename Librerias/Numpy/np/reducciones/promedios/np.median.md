---
title: np.median — Mediana (valor central)
aliases:
  - median
  - np.median
  - mediana
tags:
  - numpy
  - api/funcion
  - estadistica

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray o escalar
inplace: false

# --- Dependencias ---
requiere:
  - concepto_axis_parametro

draft: false
---

# np.median — Mediana (valor central)

## Firma de la función

```python
np.median(
    a,
    axis=None,
    out=None,
    overwrite_input=False,
    keepdims=False
) -> ndarray | escalar
```

## Valor de retorno

Devuelve la mediana: el valor que deja la mitad de los datos por debajo. Con número par de elementos, promedia los dos centrales. Más **robusta a outliers** que la [[np.mean|media]].

| Entrada | Salida |
|---------|--------|
| `[1, 2, 3, 4, 5]` | `3.0` |
| `[1, 2, 3, 4]` | `2.5` (promedio de 2 y 3) |
| `[1, 2, 100]` | `2.0` (el outlier no la desplaza) |

```python
import numpy as np
np.median([1, 2, 3, 4, 5])   # 3.0
np.median([1, 2, 100])       # 2.0  → vs mean = 34.3
```

## Parámetros en detalle

### `axis` — eje

Como en las demás reducciones; `None` aplana (ver [[concepto_axis_parametro]]).

### `overwrite_input` — optimización de memoria

Si `True`, permite a NumPy ordenar `a` in-place (lo destruye) para ahorrar memoria. Úsalo solo si no necesitas conservar `a`.

## Casos de uso

### Resumen robusto frente a outliers

```python
salarios = np.array([30, 32, 31, 33, 500])   # un outlier
np.mean(salarios)     # 125.2  engañoso
np.median(salarios)   # 32.0   representativo
```

### Mediana por columna

```python
datos = np.random.rand(100, 5)
np.median(datos, axis=0)
```

## Buenas prácticas

1. Prefiérela a la media cuando haya **outliers** o distribuciones sesgadas.
2. Para datos con NaN, usa [[np.nanmedian]].
3. Para otros cuantiles (percentil 25, 75…), usa `np.percentile` o `np.quantile`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultado NaN | hay NaN | [[np.nanmedian]] |
| `a` modificado | `overwrite_input=True` | dejarlo en `False` si necesitas `a` |

## Limitaciones

- Requiere ordenar (coste mayor que la media).
- Propaga NaN.

## Notas relacionadas

- [[concepto_axis_parametro]]
- [[np.mean]]
- [[np.std]]
