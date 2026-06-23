---
title: np/reducciones/agregacion — suma y producto, totales y acumulados
tags:
  - numpy
  - indice
draft: false
---

# np/reducciones/agregacion — suma y producto, totales y acumulados

Esta carpeta agrupa las **agregaciones aditivas y multiplicativas** sobre un eje: la suma y el
producto, cada uno en sus dos sabores —**total** (una sola respuesta) y **acumulado** (la trayectoria
de respuestas parciales)—. Son cuatro funciones que comparten la misma maquinaria de
[[concepto_axis_parametro|eje]] pero se dividen por un eje conceptual claro: **reducir vs. escanear**.

## El patrón común: reduce vs. scan

La distinción que organiza la carpeta es **qué le pasa al shape**:

- **Reduce** ([[np.sum]], [[np.prod]]): recorre el eje y lo **colapsa** a un valor. El eje
  **desaparece** del shape; con `axis=None` el resultado es un escalar. Devuelve solo la respuesta
  final.
  $$ (n_0,\dots,n_k)\ \xrightarrow{\ \text{reduce, axis}=p\ }\ (n_0,\dots,n_{p-1},\,n_{p+1},\dots,n_k) $$

- **Scan** ([[np.cumsum]], [[np.cumprod]]): barre el eje guardando el resultado parcial en cada
  posición. El **shape se conserva**; `axis` aquí **dirige** el barrido en vez de colapsar. Devuelve
  toda la trayectoria, y su **último elemento coincide con la reducción** correspondiente.
  $$ (n_0,\dots,n_k)\ \xrightarrow{\ \text{scan, axis}=p\ }\ (n_0,\dots,n_k) $$

```python
import numpy as np
a = np.array([1, 2, 3, 4])

np.sum(a)      # 10            — reduce: escalar, el eje desaparece
np.cumsum(a)   # [1, 3, 6, 10] — scan: mismo shape, último = np.sum(a)

np.prod(a)     # 24
np.cumprod(a)  # [1, 2, 6, 24] — último = np.prod(a)
```

Con arrays 2-D, `axis` fija la orientación del colapso (reduce) o del barrido (scan):

```python
M = np.array([[1, 2],
              [3, 4]])

np.sum(M, axis=0)     # [4, 6]          — suma por columna (colapsa filas)
np.cumsum(M, axis=1)  # [[1, 3], [3, 7]] — acumula a lo largo de cada fila (shape conservado)
```

## Tabla de decisión

| Operación | Total (reduce, colapsa el eje) | Acumulado (scan, conserva el shape) |
|-----------|--------------------------------|-------------------------------------|
| **Suma** | [[np.sum]] | [[np.cumsum]] |
| **Producto** | [[np.prod]] | [[np.cumprod]] |

Elige la **columna** según necesites una respuesta única (total) o la trayectoria de respuestas
parciales (acumulado); elige la **fila** según sumes o multipliques. Los productos
([[np.prod]]/[[np.cumprod]]) crecen exponencialmente: vigila el **overflow** y fija `dtype` (ver
[[concepto_dtype]]).

## Notas de esta subcarpeta

| Función | Qué hace |
|---|---|
| [[np.sum]] | Suma (reduce) los elementos a lo largo de un eje. El workhorse de las reducciones: `dtype=`, `keepdims=`, `initial=`, `where=`. Controlar el `dtype` del acumulador evita overflow silencioso con enteros pequeños. |
| [[np.prod]] | Producto (reduce) a lo largo de un eje. Gemela multiplicativa de `sum`; el overflow es **más peligroso** (crecimiento exponencial) → fija `dtype`. Producto vacío = 1. |
| [[np.cumsum]] | Suma acumulada (scan): el elemento $k$ es la suma de los $0..k$. Conserva el shape. Útil para saldos, sumas de prefijos y CDFs. |
| [[np.cumprod]] | Producto acumulado (scan): el elemento $k$ es el producto de los $0..k$. Conserva el shape. Capitalización compuesta y factoriales parciales; misma advertencia de overflow que `prod`. |

## Notas relacionadas

- [[concepto_axis_parametro]] — el eje que se colapsa (reduce) o se barre (scan)
- [[concepto_vectorizacion]] — por qué `axis` y el scan sustituyen al bucle Python
- [[concepto_dtype]] — el acumulador y el overflow
- [[np.nansum]] · [[np.nanprod]] · [[np.nancumsum]] · [[np.nancumprod]] — variantes que ignoran `NaN`
