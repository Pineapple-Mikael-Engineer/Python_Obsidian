---
title: np.linalg.tensorinv — inversa de un tensor respecto al producto tensorial
aliases:
  - tensorinv
  - linalg.tensorinv
  - np.linalg.tensorinv
tags:
  - numpy
  - api/funcion
  - algebra/matricial
lib: numpy
mod: np.linalg
tipo: funcion
retorna: ndarray
inplace: false
requiere:
  - concepto_shape
draft: false
---

# np.linalg.tensorinv — inversa de un tensor respecto al producto tensorial

`np.linalg.tensorinv` generaliza [[np.linalg.inv]] de matrices a **tensores N-D**: calcula la
inversa de un tensor respecto al producto tensorial que ejecuta `np.tensordot`. La idea es que un
tensor de muchos ejes puede **mirarse como una matriz** agrupando sus ejes en dos bloques; `tensorinv`
invierte esa matriz equivalente y luego **devuelve el resultado con los ejes reordenados** de vuelta
a forma de tensor. Es la pieza que invierte el operador en [[np.linalg.tensorsolve]] cuando hay que
resolver $A \cdot x = b$ con $A$ y $x$ tensoriales.

## La idea en una fórmula

El parámetro `ind` parte los ejes de `a` en dos grupos: los **primeros `ind`** y **el resto**. Para
que la inversa exista, el producto de cada grupo debe coincidir (la matriz equivalente es cuadrada):

$$
\text{prod}(a.\text{shape}[:\text{ind}]) \;=\; \text{prod}(a.\text{shape}[\text{ind}:]) \;=\; p
$$

Internamente `a` se aplana a la matriz $M$ de shape $(p, p)$, se invierte con `inv`, y la inversa se
**reorganiza** poniendo el segundo grupo de ejes delante.

**El mapa de shapes** — los dos bloques de ejes **intercambian su orden** en la salida:

$$
(\underbrace{s_0,\dots,s_{\text{ind}-1}}_{\text{bloque A},\ \prod = p},\ \underbrace{s_{\text{ind}},\dots,s_{k-1}}_{\text{bloque B},\ \prod = p})
\ \xrightarrow{\ \text{tensorinv}\ }\
(\underbrace{s_{\text{ind}},\dots,s_{k-1}}_{\text{bloque B}},\ \underbrace{s_0,\dots,s_{\text{ind}-1}}_{\text{bloque A}})
$$

Es decir: `out.shape == a.shape[ind:] + a.shape[:ind]`. Es la versión tensorial de "la inversa
transpone la forma".

## Firma

```python
np.linalg.tensorinv(
    a,        # array_like: el tensor a invertir; prod(shape[:ind]) == prod(shape[ind:])
    ind=2,    # int >= 1: nº de ejes iniciales (define el corte en dos bloques)
) -> ndarray
```

## Los parámetros en detalle

### `a` — el tensor a invertir
`array_like` N-D. La única condición fuerte: con el corte que fija `ind`, el producto del primer
bloque de ejes debe igualar el del segundo, para que la matriz aplanada sea **cuadrada**. Si no, o si
esa matriz es singular, lanza `LinAlgError`.

### `ind` — dónde cortar los ejes (entero ≥ 1)
Número de ejes iniciales que forman el **primer bloque**; el resto forma el segundo. Es el análogo de
elegir "filas vs columnas" al ver el tensor como matriz. Cambiar `ind` cambia tanto la condición de
cuadratura como el shape de salida.

```python
a = np.eye(4*6).reshape(4, 6, 4, 6)
np.linalg.tensorinv(a, ind=2).shape   # (4, 6, 4, 6)  → bloques (4,6) y (4,6)
```
Con `ind=2` (defecto), `a.shape[:2]` y `a.shape[2:]` deben tener el mismo producto.

## El caso N-D

`tensorinv` **ya es** la operación N-D: no actúa "por lotes" sobre los dos últimos ejes (eso es
`inv`), sino que colapsa **todos** los ejes en una única matriz cuadrada. La relación con `inv` es
directa: `tensorinv` aplana → `inv` → reordena.

| `a.shape` | `ind` | bloques (prod) | salida |
|-----------|-------|----------------|--------|
| `(4, 6, 8, 3)` | `2` | `(4,6)=24` y `(8,3)=24` | `(8, 3, 4, 6)` |
| `(4, 6, 4, 6)` | `2` | `24` y `24` | `(4, 6, 4, 6)` |
| `(24, 8, 3)` | `1` | `(24)=24` y `(8,3)=24` | `(8, 3, 24)` |
| `(2, 3, 2, 3)` con prod desigual | — | `6 ≠ ...` | `LinAlgError` |

## Vectorización

`tensorinv` evita que tú hagas el aplanado/reordenado a mano: empaqueta `reshape → inv → reshape` en
una sola llamada compilada, sin bucles Python (el principio de [[concepto_vectorizacion]]). El
equivalente manual deja ver lo que hace por dentro:

```python
# Manual: aplanar a matriz cuadrada, invertir, reordenar ejes
def tensorinv_manual(a, ind=2):
    oldshape = a.shape
    prod = int(np.prod(oldshape[ind:]))
    inv = np.linalg.inv(a.reshape(prod, prod))
    return inv.reshape(*oldshape[ind:], *oldshape[:ind])

# Equivalente:
np.linalg.tensorinv(a, ind)
```

## Valor de retorno

| Entrada (shape) | `ind` | salida | tipo |
|---|---|---|---|
| `(s₀,…,s_{k-1})` con bloques de igual producto | `ind` | `shape[ind:] + shape[:ind]` | `ndarray` flotante |
| bloques de producto distinto | cualquiera | — | `LinAlgError` (matriz no cuadrada) |
| matriz aplanada singular | cualquiera | — | `LinAlgError: Singular matrix` |

El resultado es flotante (o complejo) y su shape es el de la entrada con los **dos bloques de ejes
intercambiados**.

## Casos de uso

### Tensor `(4, 6, 8, 3)` con `ind=2` (el ejemplo canónico)
```python
np.random.seed(0)
a = np.random.randn(4, 6, 8, 3)      # prod(4,6)=24 == prod(8,3)=24
ainv = np.linalg.tensorinv(a, ind=2)
ainv.shape                           # (8, 3, 4, 6)  → bloques intercambiados

# Verificación: tensordot de a con su inversa da la "identidad tensorial"
ident = np.tensordot(a, ainv, axes=2)   # shape (4, 6, 4, 6)
np.allclose(ident.reshape(24, 24), np.eye(24))   # True
```

### Distinto corte con `ind=1`
```python
a = np.eye(24).reshape(24, 8, 3)     # bloque A = (24), bloque B = (8,3)
ainv = np.linalg.tensorinv(a, ind=1)
ainv.shape                           # (8, 3, 24)
```

### Resolver un sistema tensorial reutilizando la inversa
```python
a = np.random.randn(4, 6, 8, 3)
b = np.random.randn(4, 6)            # mismo shape que el bloque A
ainv = np.linalg.tensorinv(a, ind=2)
x = np.tensordot(ainv, b, axes=([2, 3], [0, 1]))   # x.shape (8, 3)
# equivalente directo (sin inversa explícita): np.linalg.tensorsolve(a, b)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `LinAlgError: ... must be square` | `prod(shape[:ind]) != prod(shape[ind:])` | elegir un `ind` que equilibre los productos |
| `LinAlgError: Singular matrix` | la matriz aplanada es singular | revisar el tensor; no hay inversa exacta |
| Shape de salida inesperado | olvidar que los bloques se **intercambian** | `out.shape == a.shape[ind:] + a.shape[:ind]` |
| Confundirlo con `inv` por lotes | `tensorinv` colapsa todos los ejes, no opera por lote | para pilas `(...,n,n)` usar [[np.linalg.inv]] |

## Notas relacionadas

- [[np.linalg.tensorsolve]] — resolver el sistema tensorial sin construir la inversa explícita
- [[np.linalg.inv]] — el caso matricial que `tensorinv` generaliza
- [[concepto_shape]] — el corte en dos bloques y el intercambio de ejes
- [[np.tensordot]] · [[np.linalg.pinv]]
