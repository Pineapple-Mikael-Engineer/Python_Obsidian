---
title: np.squeeze — quita los ejes de tamaño 1
aliases:
  - squeeze
  - np.squeeze
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

draft: false
---

# np.squeeze — quita los ejes de tamaño 1

`np.squeeze` limpia el [[concepto_shape|shape]] eliminando los ejes que valen 1: dimensiones que existen en la tupla pero no aportan estructura (un eje de tamaño 1 no multiplica el `size`). Es la operación que convierte un `(1, 3, 1)` en un `(3,)` sin tocar los datos. La uso típica es deshacer las dimensiones "infladas" que dejan las reducciones con `keepdims=True`, los slices o las predicciones por lotes de un solo elemento.

## La idea en una fórmula

Squeeze borra de la tupla los ejes cuyo tamaño es 1, dejando el resto en orden:

$$ (n_0, \dots, n_{p-1},\, 1,\, n_{p+1}, \dots, n_{k-1}) \;\xrightarrow{\ \text{squeeze}\ }\; (n_0, \dots, n_{p-1},\, n_{p+1}, \dots, n_{k-1}) $$

Es decir, de la forma de entrada se eliminan **todas** las posiciones con un `1` (o solo las indicadas por `axis`). El `size` no cambia, porque quitar un eje de tamaño 1 no quita ningún elemento:

$$ (1, 3, 1) \;\xrightarrow{\ \text{squeeze}\ }\; (3,) \qquad\qquad \prod = 3 \text{ en ambos} $$

## Firma

```python
np.squeeze(
    a,                 # array_like: el array a comprimir
    axis=None,         # None | int | tuple[int]: qué ejes de tamaño 1 quitar
) -> ndarray
```

## Los parámetros en detalle

### `a` — el array de entrada
`array_like` de cualquier forma. Se convierte a `ndarray` si no lo es. No se modifica; el resultado es una vista.

### `axis` — qué ejes de tamaño 1 quitar
- `None` (defecto): elimina **todos** los ejes de tamaño 1 que haya.
- `int` o tupla de `int`: elimina **solo** esos ejes, que **deben** valer 1 (si no, `ValueError`). Admite ejes negativos.

```python
a = np.zeros((1, 3, 1))
np.squeeze(a).shape               # (3,)    → todos los ejes de tamaño 1
np.squeeze(a, axis=0).shape       # (3, 1)  → solo el eje 0
np.squeeze(a, axis=(0, 2)).shape  # (3,)    → los ejes 0 y 2
```

Pasar `axis` explícito es lo prudente: con `None`, si un eje vale 1 por casualidad (un lote de tamaño 1, por ejemplo), se eliminaría sin querer.

## El caso N-D

La regla es mecánica: de la tupla desaparecen las posiciones con un `1`; las demás quedan en su orden. El número de ejes eliminados puede ser cualquiera.

| `a.shape` | `axis` | salida | lectura |
|-----------|--------|--------|---------|
| `(1, 3, 1)` | `None` | `(3,)` | quita los dos ejes unitarios |
| `(1, 3, 1)` | `0` | `(3, 1)` | quita solo el primero |
| `(1, 3, 1)` | `2` | `(1, 3)` | quita solo el último |
| `(2, 3)` | `None` | `(2, 3)` | sin ejes de 1 → intacto |
| `(1, 1, 1)` | `None` | `()` | todo eran unos → escalar 0-D |

```python
# Tensor (lote de 1 imagen RGB 2×2):  (1, 2, 2, 3)
img = np.arange(1*2*2*3).reshape(1, 2, 2, 3)
np.squeeze(img, axis=0).shape    # (2, 2, 3)  → quita el eje de lote
np.squeeze(img).shape            # (2, 2, 3)  → aquí coincide (solo el eje 0 vale 1)
```
Con un tensor de varios ejes unitarios, `axis` decide cuáles caen y cuáles sobreviven.

## Vista vs copia

`np.squeeze` devuelve **siempre una vista**: solo reescribe la tupla de shape y los `strides`, nunca mueve datos (ver [[concepto_views_vs_copias]]). Modificar el resultado modifica `a`.

```python
a = np.zeros((1, 3, 1))
s = np.squeeze(a)
np.shares_memory(a, s)   # True → es una vista
```

## Valor de retorno

`ndarray` con el mismo `dtype` y los mismos datos que `a`, y un shape sin los ejes de tamaño 1 (todos, o los de `axis`). Siempre vista.

| Entrada | `axis` | salida | tipo |
|---------|--------|--------|------|
| `(1, 5, 1)` | `None` | `(5,)` | `ndarray` |
| `(1, 5, 1)` | `0` | `(5, 1)` | `ndarray` |
| `(1, 1, 1)` | `None` | `()` | `ndarray` 0-D (¡no escalar Python!) |

Ojo con el caso `(1,1,1)`: queda un array 0-D, no un número de Python; usa `.item()` si necesitas el escalar.

## Casos de uso

### Quitar la dimensión de lote tras una predicción
```python
pred = modelo(x)            # shape (1, 10)
logits = np.squeeze(pred)   # shape (10,)  → vector de logits
```

### Colapsar el resultado de una reducción con `keepdims`
```python
M = np.ones((4, 5))
s = M.sum(axis=1, keepdims=True)   # (4, 1)
s = np.squeeze(s, axis=1)          # (4,)
```

### Limpiar ejes sobrantes de un slice (caso N-D)
```python
cubo = np.arange(10*1*10).reshape(10, 1, 10)
plano = np.squeeze(cubo)    # (10, 10)  → desaparece el eje central de tamaño 1
plano.shape                 # (10, 10)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `cannot select an axis to squeeze out which has size not equal to one` | el `axis` indicado no vale 1 | comprobar el shape antes |
| Se eliminó un eje que querías conservar | `axis=None` quita todos los unitarios | pasar `axis` explícito |
| Escalar 0-D inesperado | todos los ejes valían 1 (`(1,1,1)`) | reconstruir con `reshape` o usar `.item()` |
| Sigue sobrando un eje | era de tamaño > 1 | `squeeze` solo quita los de tamaño 1; usar `reshape` |

## Notas relacionadas

- [[concepto_shape]] — los ejes de tamaño 1 y por qué no aportan al `size`
- [[concepto_views_vs_copias]] — `squeeze` siempre devuelve vista
- [[np.expand_dims]] — la operación inversa: inserta un eje de tamaño 1
- [[np.reshape]] · [[np.ravel]]
