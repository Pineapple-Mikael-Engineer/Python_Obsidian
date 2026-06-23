---
title: np.logspace — num puntos espaciados logarítmicamente
aliases:
  - logspace
  - np.logspace
tags:
  - numpy
  - api/funcion
  - creacion

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
  - concepto_dtype

draft: false
---

# np.logspace — num puntos espaciados logarítmicamente

`np.logspace` genera `num` puntos espaciados **logarítmicamente** entre `base**start` y `base**stop`.
Es [[np.linspace]] aplicado a los **exponentes**: los exponentes crecen de forma lineal y los valores
crecen geométricamente. Es la función idiomática para **escalas log** que abarcan varios órdenes de
magnitud: ejes de frecuencia, barridos de learning rate, concentraciones.

## La idea

`np.logspace(start, stop, num)` equivale a $base^{\,\text{linspace}(start,\,stop,\,num)}$. Es decir:
toma `num` exponentes equiespaciados en $[start, stop]$ y los eleva como potencias de `base`:

$$ a_k = base^{\,start + k\cdot\Delta},\quad \Delta = \frac{stop - start}{num - 1},\quad k = 0,\dots,num-1 $$

El resultado es un vector 1D de [[concepto_shape|shape]] $(num,)$:

$$ start,\ stop,\ num,\ base \;\xrightarrow{\ \text{logspace}\ }\; (num,) $$

La clave a recordar: **`start` y `stop` son exponentes**, no los valores finales. `logspace(0, 3)`
va de $base^0 = 1$ a $base^3 = 1000$ (con `base=10`). Si ya tienes los valores extremos directamente
(no sus exponentes), la hermana [[np.linspace|np.geomspace]] hace lo mismo recibiendo los valores.

## Firma

```python
np.logspace(
    start,              # escalar | array_like: exponente inicial (base**start)
    stop,               # escalar | array_like: exponente final (base**stop)
    num=50,             # int ≥ 0: cantidad de puntos
    endpoint=True,      # bool: incluir base**stop como último punto
    base=10.0,          # escalar | array_like: base de la potencia
    dtype=None,         # dtype: tipo de salida
    axis=0,             # int: eje donde colocar los num puntos si start/stop son arrays
) -> ndarray
```

## Los parámetros en detalle

### `start`, `stop` — exponentes
El rango va de `base**start` a `base**stop`. **Son exponentes**, no valores: para empezar en 1 usa
`start=0`; para `1e-5` usa `start=-5`. Es el error más común de la función.

```python
np.logspace(0, 3, 4)    # [1., 10., 100., 1000.]  → exponentes 0,1,2,3
np.logspace(-5, -1, 5)  # [1e-5, 1e-4, 1e-3, 1e-2, 1e-1]
```

### `num` — cantidad de puntos
Entero `≥ 0`. Define el shape `(num,)`. Igual que en [[np.linspace]], son **puntos**, con `num-1`
intervalos (en el espacio de exponentes) cuando `endpoint=True`.

### `endpoint` — incluir el extremo
Como en [[np.linspace]]: `True` (defecto) incluye `base**stop` como último punto; `False` lo excluye
y reparte en `num` intervalos.

### `base` — base de la potencia
Por defecto `10.0`. Usa `2` para escalas binarias, `np.e` para naturales. Puede ser un array para
generar varias escalas a la vez (combinado con `axis`).

```python
np.logspace(0, 9, 10, base=2)   # potencias de 2: [1, 2, 4, ..., 512]
np.logspace(0, 3, 4, base=np.e) # exponenciales naturales
```

### `dtype` — tipo de salida
Por defecto flotante. Pasarlo fuerza el tipo del resultado (ver [[concepto_dtype]]).

### `axis` — eje donde colocar los puntos (con start/stop array)
Cuando `start`/`stop` son arrays, controla en qué eje se inserta la dimensión de los `num` puntos,
igual que en [[np.linspace]].

## El caso N-D

Con extremos escalares el resultado es siempre 1D `(num,)`. Para tensores valen las mismas dos vías
que en [[np.linspace]]: encadenar con [[np.reshape]], o pasar `start`/`stop` como arrays para que la
dimensión de los `num` puntos se inserte según `axis`.

```python
# Una escala log por fila: dos rangos de exponentes distintos, 5 puntos cada uno
ini = np.array([0, -3])      # exponentes iniciales
fin = np.array([3,  0])      # exponentes finales
escala = np.logspace(ini, fin, 5, axis=-1)   # shape (2, 5)
escala.shape                  # (2, 5): fila 0 va de 1 a 1000, fila 1 de 1e-3 a 1
```

Aquí el eje insertado (`axis=-1`) recorre los 5 puntos logarítmicos, y el eje 0 distingue las dos
escalas: un ejemplo de cómo `logspace` produce un tensor N-D sin bucles.

## Casos de uso

### Eje X logarítmico para gráficas
```python
frecuencias = np.logspace(1, 5, 100)   # 10 Hz a 100 kHz
```

### Barrido de hiperparámetros (learning rate)
```python
lrs = np.logspace(-5, -1, 5)   # [1e-5, 1e-4, 1e-3, 1e-2, 1e-1]
```

### Escala binaria
```python
tamanos = np.logspace(0, 10, 11, base=2)   # 1, 2, 4, ..., 1024
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Valores enormes/diminutos inesperados | se pasaron valores en vez de exponentes | usar `np.geomspace`, o pasar `log10` de los extremos |
| Base equivocada | `base=10` por defecto | indicar `base` explícitamente |
| Esperaba incluir el extremo y falta | `endpoint=False` | dejar `endpoint=True` (defecto) |

## Notas relacionadas

- [[concepto_shape]] — el resultado es `(num,)`
- [[concepto_dtype]] — tipo de salida
- [[np.linspace]] — la base lineal sobre la que se construye (`base**linspace`)
- [[np.arange]] — secuencia por paso constante
