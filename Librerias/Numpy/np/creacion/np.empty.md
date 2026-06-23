---
title: np.empty — crea un array de la shape dada SIN inicializar (contenido basura)
aliases:
  - empty
  - np.empty
  - vacio
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

# np.empty — crea un array de la shape dada SIN inicializar (contenido basura)

`np.empty` reserva la memoria para un [[concepto_ndarray|ndarray]] con la **forma** que le pidas, **pero no escribe ningún valor**: el contenido es **basura** (lo que hubiera en esa RAM). Es la más **rápida** de las funciones de creación, justo porque se salta el paso de inicializar. Solo tiene sentido cuando vas a **sobrescribir cada elemento** después; en cualquier otro caso, [[np.zeros]] es la opción segura.

> [!warning] La trampa: NO asumas que es cero
> `np.empty` **no** inicializa a 0. Puede *parecer* que devuelve ceros (la RAM recién pedida al SO a veces viene a cero), pero eso **no está garantizado** y reciclar memoria ya usada devuelve valores arbitrarios. Nunca **leas** un `np.empty` antes de haberlo **escrito** entero.

## La idea

`np.empty` materializa el tensor descrito por `shape` reservando su buffer, sin tocar su contenido. El mapa de forma es idéntico al de [[np.zeros]]; lo único que cambia es que los bytes quedan **indefinidos**.

$$ \text{shape} = (n_0, n_1, \dots, n_{k-1}) \;\xrightarrow{\ \text{empty}\ }\; \text{buffer de } \textstyle\prod_i n_i \text{ elementos SIN inicializar} $$

La forma de salida **es** el argumento `shape`. La diferencia con `zeros`/`ones` no está en la forma sino en que aquí **no se paga** el coste de recorrer el buffer escribiendo un valor.

## Firma

```python
np.empty(
    shape,             # int | tuple[int]: la forma del array de salida
    dtype=float,       # dtype: tipo de los elementos (por defecto float64)
    order='C',         # {'C', 'F'}: disposición en memoria
    *,
    like=None,         # array_like: referencia para crear con otra librería compatible
) -> ndarray
```

## Los parámetros en detalle

### `shape` — la forma del array de salida
El único obligatorio. **Entero** → vector 1D; **tupla** → un eje por componente. Es el [[concepto_shape|shape]] exacto del buffer reservado.

```python
np.empty(5)         # (5,)       5 elementos sin inicializar
np.empty((3, 4))    # (3, 4)     12 elementos sin inicializar
np.empty((2, 3, 4)) # (2, 3, 4)  tensor de rango 3
```

### `dtype` — tipo de los elementos
Por defecto `float64`. Fija cuántos bytes ocupa cada elemento y cómo se interpretan (ver [[concepto_dtype]]). No cambia el hecho de que el contenido es basura: solo decide qué *tipo* de basura.

```python
np.empty(3).dtype             # float64
np.empty(3, dtype=np.int32)   # 3 enteros arbitrarios
```

### `order` — disposición en memoria
`'C'` (filas contiguas, por defecto) o `'F'` (columnas contiguas). Igual que en [[np.zeros]]: solo afecta al rendimiento en 2D+.

### `like` — prototipo de otra librería
Solo-palabra-clave (`*`). Crea un array del **mismo tipo de objeto** que `like` si este implementa el protocolo de array de NumPy.

## Cuándo usarla (y cuándo no)

| Situación | Función |
|-----------|---------|
| Vas a **sobrescribir cada elemento** justo después | `np.empty` (no inicializas dos veces) |
| Necesitas ceros de partida | [[np.zeros]] |
| Necesitas unos | [[np.ones]] |
| Necesitas un valor constante | [[np.full]] |
| Tienes la menor duda | [[np.zeros]]: la diferencia de velocidad rara vez importa y evitas bugs |

El ahorro frente a `np.zeros` solo se nota con arrays **grandes** que se rellenan al 100 %. Si solo escribes una parte, el resto queda con basura.

## El caso N-D

La forma de salida es la tupla `shape` tal cual; lo único especial es que el contenido no está definido.

```python
# 4D real: buffer de salida para un lote de imágenes que vas a llenar entero
out = np.empty((2, 3, 4, 5))   # 4D: (lote, canal, alto, ancho) — SIN inicializar
out.shape   # (2, 3, 4, 5)
out.ndim    # 4
# ⚠️ out NO es cero: hay que escribir los 120 elementos antes de leerlos
for i in range(out.shape[0]):
    out[i] = procesar(i)       # se rellena ejemplo a ejemplo

# 5D real: buffer para un lote de vídeo que produce una operación vectorizada
v = np.empty((8, 16, 3, 64, 64))  # 5D: (lote, frames, canal, alto, ancho)
v.shape   # (8, 16, 3, 64, 64)
v.ndim    # 5
np.multiply(fuente, 2.0, out=v)   # se sobrescribe TODO v de una vez
```

El `(2, 3, 4, 5)` se reserva como cualquier tensor 4D (**lote, canal, alto, ancho**), pero `np.empty` solo garantiza la *forma* y el *dtype*, no los valores. Por eso el patrón correcto es siempre "reservar con `empty` y rellenarlo entero" (con un bucle o, mejor, pasándolo como `out=` a una operación vectorizada).

## Casos de uso

### Preasignar y llenar en un bucle (sin pagar la inicialización)
```python
n = 1000
out = np.empty(n)             # sin coste de poner ceros
for i in range(n):
    out[i] = calcular(i)      # se rellena por completo
```

### Buffer de salida de una operación vectorizada
```python
res = np.empty_like(a)        # mismo shape/dtype que a, sin inicializar
np.multiply(a, 2, out=res)    # la ufunc escribe directamente en res
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Valores "aleatorios" inesperados | se leyó antes de escribirlo | escribir el array entero antes de leerlo |
| Asumir que son ceros | `empty` **no** inicializa | usar [[np.zeros]] si necesitas ceros reales |
| Solo se rellenó parte del array | el resto sigue con basura | rellenar al 100 % o usar [[np.zeros]] |
| `np.empty(2, 3)` da `TypeError` | el `3` se interpreta como `dtype` | pasar una tupla: `np.empty((2, 3))` |

## Notas relacionadas

- [[concepto_shape]] — la forma de salida es el argumento `shape`
- [[concepto_dtype]] — decide el tipo de la basura reservada
- [[np.zeros]] · [[np.ones]] · [[np.full]] — creaciones que **sí** inicializan
- [[np.empty_like]] — misma shape/dtype que otro array, sin inicializar
