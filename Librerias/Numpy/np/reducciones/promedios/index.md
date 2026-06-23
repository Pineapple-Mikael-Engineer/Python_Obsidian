---
title: np/reducciones/promedios — tendencia central y dispersión
tags:
  - numpy
  - indice
draft: false
---

# np/reducciones/promedios — tendencia central y dispersión

Esta subcarpeta agrupa las **medidas estadísticas descriptivas** clásicas: las que resumen un
conjunto de datos en dos preguntas. **Tendencia central** — "¿dónde están concentrados los datos?"
([[np.mean|mean]], [[np.median|median]], [[np.average|average]]) — y **dispersión** — "¿cuánto se
alejan de ese centro?" ([[np.std|std]], [[np.var|var]]). Son cinco funciones distintas, pero todas
comparten el mismo patrón de NumPy.

**El patrón común:** todas son **reducciones** que **colapsan un eje**. Aceptan `axis=` y, como
cualquier reducción, el eje recorrido **desaparece** del shape (ver [[concepto_axis_parametro]]):
sin `axis` resumen *todo* el array a un escalar; con `axis=0` resumen cada columna, con `axis=1`
cada fila. `keepdims=True` conserva el eje en tamaño 1 para poder broadcastear el resultado de vuelta
(imprescindible para estandarizar). Es la misma mecánica de [[np.sum]], solo cambia *qué* se calcula
sobre el eje.

```python
import numpy as np
a = np.array([1.0, 2.0, 3.0, 100.0])  # 100 es un outlier

np.mean(a)    # 26.5  → arrastrado por el outlier
np.median(a)  # 2.5   → robusta, no se ve afectada

np.std(a, ddof=1)  # desviación muestral (ddof=1 es la convención estadística)
np.var(a, ddof=1)  # == np.std(a, ddof=1)**2
```

## Tabla de decisión

**Tendencia central** — elegir según la distribución y los pesos:

| Situación | Función | Por qué |
|---|---|---|
| Distribución simétrica, sin valores extremos | [[np.mean]] | la más eficiente; suma ÷ n |
| Distribución sesgada o con outliers | [[np.median]] | robusta (no la arrastra un valor extremo), pero más lenta: ordena el array |
| Cada elemento pesa distinto | [[np.average]] | acepta `weights=` para ponderar (notas, medias móviles) |

**Dispersión** — `var` y `std` calculan lo mismo; cambia la unidad:

| Situación | Función | Por qué |
|---|---|---|
| Medir dispersión en las **unidades originales** | [[np.std]] | está en las mismas unidades que los datos (raíz de la varianza) |
| Dispersión en unidades **al cuadrado** / paso intermedio | [[np.var]] | a veces la raíz se cancela o es innecesaria; `var == std**2` |

**El divisor `ddof`** (común a `std` y `var`) — poblacional vs muestral:

| `ddof` | Divisor | Cuándo |
|---|---|---|
| `0` (defecto en NumPy) | $N$ | los datos **son** toda la población |
| `1` | $N-1$ | los datos son una **muestra** (convención estadística; el defecto en R, pandas...) |

## Notas de esta subcarpeta

| Función | Qué hace |
|---|---|
| [[np.mean]] | Media aritmética (suma dividida entre n). Sensible a outliers. Con `axis=0` da la media de cada columna; con `axis=1` la de cada fila. |
| [[np.median]] | Valor central de los datos ordenados. Robusta a outliers a diferencia de la media. Más lenta en arrays grandes por el ordenamiento interno. |
| [[np.average]] | Media ponderada: igual que `mean` sin pesos, pero acepta `weights=` para dar distinta importancia a cada elemento. |
| [[np.std]] | Desviación típica. `ddof=0` (defecto) es poblacional; `ddof=1` es muestral, la que usan la mayoría de paquetes estadísticos. En las unidades originales de los datos. |
| [[np.var]] | Varianza: igual que `std` pero sin la raíz cuadrada (unidades al cuadrado). `np.var(a, ddof=k) == np.std(a, ddof=k)**2`. Útil como paso intermedio. |

> [!tip] Datos con NaN
> Si el array puede contener NaN, usa las variantes de
> [[Librerias/Numpy/np/reducciones/nan_safe/index|nan_safe/]]: [[np.nanmean]], [[np.nanmedian]],
> [[np.nanstd]], [[np.nanvar]].

## Notas relacionadas

- [[concepto_axis_parametro]] — todas reducen un eje
- [[concepto_vectorizacion]] — por qué `axis` sustituye al bucle
- [[np.sum]] — la reducción base; mismo patrón de `axis`/`keepdims`
- [[Librerias/Numpy/np/reducciones/index|reducciones/]] — la carpeta madre
