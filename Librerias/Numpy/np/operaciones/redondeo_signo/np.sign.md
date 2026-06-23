---
title: np.sign — signo de cada elemento (ufunc)
aliases:
  - sign
  - np.sign
  - signo
tags:
  - numpy
  - api/funcion
  - transformaciones

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_ufuncs
  - concepto_vectorizacion

draft: false
---

# np.sign — signo de cada elemento (ufunc)

`np.sign` es una **ufunc unaria**: reduce cada elemento a su **signo** $\operatorname{sign}(x_i)\in\{-1,0,+1\}$,
sin mirar a sus vecinos y **sin cambiar el shape**. Es la operación que **extrae la dirección** y
descarta la magnitud: te dice *hacia dónde* apunta cada valor, no *cuánto* vale. La convención clave es
$\operatorname{sign}(0)=0$ (no $+1$). Para complejos no devuelve $\pm1$ sino la **fase normalizada**
$x/|x|$. Suele combinarse con [[np.abs]] para separar y recomponer signo y magnitud.

## La idea en una fórmula

Cada elemento se transforma de forma independiente; el shape se **conserva**. Para entrada **real**:

$$
\operatorname{sign}(x_i) =
\begin{cases}
+1 & x_i > 0 \\
\phantom{+}0 & x_i = 0 \\
-1 & x_i < 0
\end{cases}
\qquad (n_0,\dots,n_k)\ \xrightarrow{\ \text{sign}\ }\ (n_0,\dots,n_k)
$$

Para entrada **compleja**, el signo es el número de **módulo 1** con la misma fase (y `0` para `0`):

$$
\operatorname{sign}(x) = \frac{x}{|x|} \qquad (x \ne 0)
$$

| `x` (real) | $\operatorname{sign}(x)$ |
|-----|-----------|
| `> 0` | `1` |
| `== 0` | `0` |
| `< 0` | `-1` |
| `nan` | `nan` |

## Firma

```python
np.sign(
    x,                 # array_like: el tensor de entrada (real o complejo)
    /,
    out=None,          # ndarray | None: destino preasignado
    *,
    where=True,        # array_like[bool]: máscara de cómputo
    casting='same_kind',  # política de conversión de tipos
    order='K',         # 'K' | 'C' | 'F' | 'A': layout de memoria del resultado
    dtype=None,        # dtype: fuerza el tipo de cómputo/salida
) -> ndarray
```

## Los parámetros en detalle

### `x` — el tensor de entrada
`array_like` (ndarray, lista, escalar), **real o complejo**. Se procesa elemento a elemento; el shape de
la salida es el de `x`. Con `nan` el resultado es `nan`.

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape de salida. Evita asignar memoria; permite in-place
(`np.sign(arr, out=arr)`). El dtype debe ser compatible bajo `casting`.

### `where` — máscara de cómputo
`array_like` booleano broadcasteable con `x`. Solo calcula el signo donde es `True`; donde es `False`,
conserva el valor previo de `out` (basura si no se pasó `out`). Va casi siempre con `out`.

### `dtype` — tipo de cómputo y salida
Fuerza el tipo de cálculo/salida. Útil si quieres el signo como `int8` para ahorrar memoria
(`np.sign(arr).astype(np.int8)` o `dtype=`), o como `float`.

### `casting` — política de conversión
`'no'`, `'equiv'`, `'safe'`, `'same_kind'` (defecto), `'unsafe'`. Controla qué conversiones se permiten al
escribir en `out` o aplicar `dtype`.

### `order` — layout de memoria
`'K'` (defecto), `'C'`, `'F'`, `'A'`. Solo afecta al almacenamiento del resultado, no a sus valores.

## El caso N-D

`np.sign` se aplica **elemento a elemento** sobre cualquier dimensión: no hay `axis`, no colapsa nada,
**conserva el shape**. Un tensor `(d0, d1, d2)` entra y sale como `(d0, d1, d2)`:

```python
T = np.array([[[-5.0, 0.0], [ 3.0, -0.2]],
              [[ 2.0, -7.0], [ 0.0,  9.0]]])   # shape (2, 2, 2)
np.sign(T).shape       # (2, 2, 2)  → shape idéntico
np.sign(T)
# [[[-1.,  0.], [ 1., -1.]],
#  [[ 1., -1.], [ 0.,  1.]]]
```

Cada posición se evalúa por separado; la estructura del tensor no afecta al resultado.

## Vectorización

`np.sign` reemplaza un bucle Python con `if`/`elif` por elemento. La versión vectorizada corre el bucle
en C, sobre memoria contigua:

```python
# Bucle Python (lento):
out = np.empty_like(arr)
for i in range(arr.size):
    v = arr.flat[i]
    out.flat[i] = 1 if v > 0 else (-1 if v < 0 else 0)

# ufunc (un único bucle en C):
out = np.sign(arr)
```

Es el principio de [[concepto_vectorizacion]]: describes la transformación, no la iteración. Soporta
`out`/`where` como toda ufunc.

## Valor de retorno

`ndarray` (o escalar de NumPy si la entrada es escalar) con el **mismo shape** que `x`. El `dtype` sigue
al de la entrada (el signo se expresa en ese tipo):

| Entrada (`x`) | dtype salida | valores |
|---------------|--------------|---------|
| flotante (`float64`) | `float64` | `-1.`, `0.`, `1.`, `nan` |
| entero (`int64`...) | mismo entero | `-1`, `0`, `1` |
| **complejo** | **complejo** | $x/|x|$ (módulo 1) o `0` |

```python
np.sign([-5, 0, 3, -0.2])    # array([-1.,  0.,  1., -1.])
np.sign(np.array([-3, 0, 7])).dtype   # int64
np.sign(3 + 4j)              # (0.6+0.8j)   → x/|x|, módulo 1
```

## Casos de uso

### Dirección de un cambio (subida/bajada)
```python
direccion = np.sign(np.diff(serie))   # +1 sube, -1 baja, 0 igual
```

### Separar y recomponer magnitud y signo
```python
x = np.array([-3.0, 2.0, -1.0])
np.sign(x) * np.abs(x)        # vuelve a x: dirección × magnitud
```

### Aplicar un signo a otra magnitud (copysign manual)
```python
magnitud = np.array([2.0, 5.0, 1.0])
referencia = np.array([-1.0, 3.0, -4.0])
magnitud * np.sign(referencia)   # [-2., 5., -1.]  toma el signo de la referencia
```

### N-D: signo por elemento de un tensor
```python
campo = np.array([[[-5, 0], [ 3, -2]],
                  [[ 2, -7], [ 0,  9]]])   # (2, 2, 2)
np.sign(campo)
# [[[-1, 0], [ 1, -1]],
#  [[ 1,-1], [ 0,  1]]]                    # mismo shape, solo dirección
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Esperar `±1` y obtener `0` | el valor era exactamente `0` ($\operatorname{sign}(0)=0$) | tratar el `0` aparte si molesta (p. ej. `np.where(x==0, 1, np.sign(x))`) |
| `nan` en el resultado | la entrada contenía `NaN` (se propaga) | filtrar/limpiar antes |
| Sorpresa con complejos | devuelve $x/|x|$ (módulo 1), no `±1` | esperado; usa la parte real si querías un signo escalar |
| Posiciones con basura tras `where` | `where=` sin `out` inicializado | pasar siempre `out=` junto con `where=` |

## Notas relacionadas

- [[concepto_ufuncs]] — `np.sign` es una ufunc unaria; hereda `out`/`where`/`dtype`/`casting`
- [[concepto_vectorizacion]] — por qué sustituye al bucle por elemento
- [[np.abs]] — su complemento: la magnitud (juntas reconstruyen el valor)
- [[np.ceil]] · [[np.copysign]]
