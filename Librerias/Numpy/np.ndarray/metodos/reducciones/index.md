---
title: np.ndarray — metodos de reduccion
tags:
  - numpy
  - indice
draft: false
---

# np.ndarray — metodos de reduccion

14 metodos que colapsan el array (o uno de sus ejes) a un resultado de menor dimension. Son los mismos conceptos que en `np/reducciones/` pero como metodos del objeto, lo que permite encadenamiento fluido: `arr.sum(axis=1).mean()`.

Todos aceptan el parametro `axis=None` (reduccion global sobre todos los elementos) o un entero (reduccion a lo largo de ese eje unicamente). Con `keepdims=True` la dimension reducida se mantiene con tamaño 1, lo que facilita el broadcasting posterior.

## Suma y producto

| Metodo | Descripcion |
|--------|-------------|
| [[ndarray.sum]] | Suma de todos los elementos (o por eje). El resultado es un escalar si no se especifica `axis`. |
| [[ndarray.cumsum]] | Suma acumulada: devuelve un array del mismo shape con la suma corriente hasta cada elemento. No reduce la dimension. |
| [[ndarray.prod]] | Producto de todos los elementos (o por eje). Analogo a `sum` pero con multiplicacion. |
| [[ndarray.cumprod]] | Producto acumulado: analogo a `cumsum` con multiplicacion. Devuelve array del mismo shape. |

`cumsum` y `cumprod` no son reductores en el sentido estricto — no colapsan la dimension — pero se agrupan aqui por semantica de suma/producto:

```python
arr = np.array([1, 2, 3, 4])
arr.sum()     # → 10           (escalar)
arr.cumsum()  # → [1, 3, 6, 10]  (mismo shape)
```

## Estadistica

| Metodo | Descripcion |
|--------|-------------|
| [[ndarray.mean]] | Media aritmetica. Para arrays enteros devuelve float64 por defecto. |
| [[ndarray.var]] | Varianza. Acepta `ddof=` (grados de libertad a restar): `ddof=0` es varianza poblacional (por defecto), `ddof=1` es muestral. |
| [[ndarray.std]] | Desviacion estandar. Mismo comportamiento que `var` respecto a `ddof`; equivale a `np.sqrt(arr.var(ddof=...))`. |

## Extremos

| Metodo | Descripcion |
|--------|-------------|
| [[ndarray.min]] | Valor minimo del array (o por eje). |
| [[ndarray.max]] | Valor maximo del array (o por eje). |
| [[ndarray.argmin]] | Indice del elemento minimo en el array aplanado, o a lo largo del eje especificado. Devuelve el indice, no el valor. |
| [[ndarray.argmax]] | Indice del elemento maximo. Mismo comportamiento que `argmin`. |
| [[ndarray.ptp]] | Rango pico a pico: `max - min`. Deprecado en NumPy >= 2.0; usar `np.ptp` o `arr.max() - arr.min()`. |

## Utilidades

| Metodo | Descripcion |
|--------|-------------|
| [[ndarray.clip]] | Recorta valores al rango `[a_min, a_max]`: los menores que `a_min` pasan a `a_min` y los mayores que `a_max` pasan a `a_max`. Devuelve un array nuevo (copia). |
| [[ndarray.round]] | Redondea cada elemento al numero de decimales indicado. `arr.round(0)` redondea a entero pero mantiene el dtype float. |

## `argmin` / `argmax` con axis

Sin `axis` devuelven el indice en el array aplanado; con `axis` devuelven un array de indices en esa dimension:

```python
arr = np.array([[3, 1],
                [4, 2]])
arr.argmin()        # → 1  (indice plano del elemento 1)
arr.argmin(axis=0)  # → [0, 0]  (fila del minimo en cada columna)
arr.argmin(axis=1)  # → [1, 1]  (columna del minimo en cada fila)
```
