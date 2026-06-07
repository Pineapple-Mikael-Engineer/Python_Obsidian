---
title: np.ndarray — metodos de reduccion
tags:
  - numpy
  - indice
draft: false
---

# np.ndarray — metodos de reduccion

Los 14 metodos de reduccion colapsan el array (o uno de sus ejes) en un resultado de menor dimension. Son los mismos conceptos que en `np.reducciones/` pero como metodos del objeto, lo que permite encadenamiento: `arr.sum(axis=1).mean()`.

Todos aceptan el parametro `axis=None` (reduccion global) o un entero (reduccion a lo largo de ese eje).

## Grupos

### Suma y producto acumulado

| Metodo | Descripcion |
|--------|-------------|
| [[ndarray.sum]] | Suma de todos los elementos (o por eje) |
| [[ndarray.cumsum]] | Suma acumulada (devuelve array de misma forma) |
| [[ndarray.prod]] | Producto de todos los elementos (o por eje) |
| [[ndarray.cumprod]] | Producto acumulado (devuelve array de misma forma) |

### Estadistica

| Metodo | Descripcion |
|--------|-------------|
| [[ndarray.mean]] | Media aritmetica |
| [[ndarray.var]] | Varianza |
| [[ndarray.std]] | Desviacion estandar |

### Extremos

| Metodo | Descripcion |
|--------|-------------|
| [[ndarray.min]] | Valor minimo |
| [[ndarray.max]] | Valor maximo |
| [[ndarray.argmin]] | Indice del valor minimo |
| [[ndarray.argmax]] | Indice del valor maximo |
| [[ndarray.ptp]] | Rango pico a pico (`max - min`); deprecado en NumPy >= 2.0 |

### Utilidades

| Metodo | Descripcion |
|--------|-------------|
| [[ndarray.clip]] | Recorta valores fuera de `[a_min, a_max]` |
| [[ndarray.round]] | Redondea a un numero dado de decimales |

## Nota sobre `cumsum` y `cumprod`

Estos dos metodos no reducen la dimension: devuelven un array de la misma forma que el original, con la operacion aplicada de forma acumulada. No son "reductores" en el sentido estricto pero se agrupan aqui por semantica de suma/producto.

```python
arr = np.array([1, 2, 3, 4])
arr.sum()     # → 10     (escalar)
arr.cumsum()  # → [1, 3, 6, 10]  (mismo shape)
```
