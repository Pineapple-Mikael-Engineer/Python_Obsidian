---
title: np.deg2rad — convierte grados a radianes elemento a elemento (ufunc)
aliases:
  - deg2rad
  - np.deg2rad
  - radians
  - np.radians
  - grados a radianes
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

draft: false
---

# np.deg2rad — convierte grados a radianes elemento a elemento (ufunc)

`np.deg2rad` es una **ufunc unaria**: multiplica cada elemento por $\pi/180$ para pasar de **grados a
radianes**, sin mirar a sus vecinos y **sin cambiar el shape**. Es el paso obligatorio antes de
alimentar [[np.sin]], [[np.cos]] o [[np.tan]], que **esperan radianes**: si les pasas grados sin
convertir, el resultado es silenciosamente incorrecto. Tiene el alias exacto `np.radians` (misma
función). Su inversa es [[np.rad2deg]].

## La idea en una fórmula

Cada elemento se escala de forma independiente por la constante $\pi/180$; el shape se **conserva**:

$$
z_i = x_i \cdot \frac{\pi}{180} \qquad (n_0,\dots,n_k)\ \xrightarrow{\ \text{deg2rad}\ }\ (n_0,\dots,n_k)
$$

Es una multiplicación por un escalar fijo; "media circunferencia" ($180°$) se mapea a $\pi$.

| `x` (grados) | `deg2rad(x)` (radianes) |
|-----|------------------|
| `0` | `0.0` |
| `90` | `1.5708…` ($\pi/2$) |
| `180` | `3.1416…` ($\pi$) |
| `270` | `4.7124…` ($3\pi/2$) |
| `360` | `6.2832…` ($2\pi$) |

## Firma

```python
np.deg2rad(
    x,                 # array_like: ángulos en grados
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

### `x` — el tensor de entrada (en grados)
`array_like` **real** (ndarray, lista, escalar) interpretado como ángulos en grados. Los enteros se
promueven a float (la conversión casi nunca es entera). El shape de la salida es el de `x`.

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape de salida. Evita asignar memoria y permite operar in-place
(`np.deg2rad(arr, out=arr)`). El dtype debe ser flotante y compatible bajo `casting`.

### `where` — máscara de cómputo
`array_like` booleano broadcasteable con `x`. Solo convierte donde es `True`; donde es `False`, la
posición conserva el valor previo de `out` (basura si no se pasó `out`). Úsalo junto con `out`.

### `dtype` — tipo de cómputo y salida
Fuerza el tipo flotante de cálculo/salida (p. ej. `float32` para ahorrar memoria). No cambia el
significado del valor, solo su precisión.

### `casting` — política de conversión
`'no'`, `'equiv'`, `'safe'`, `'same_kind'` (defecto), `'unsafe'`. Controla qué conversiones se permiten
al escribir en `out` o aplicar `dtype`.

### `order` — layout de memoria
`'K'` (defecto), `'C'`, `'F'`, `'A'`. Solo afecta al almacenamiento del resultado, no a sus valores.

## El caso N-D

`np.deg2rad` se aplica **elemento a elemento** sobre cualquier dimensión: no hay `axis`, no colapsa
nada, **conserva el shape**. Un tensor `(d0, d1, d2)` entra y sale como `(d0, d1, d2)`:

```python
T = np.array([[0., 90.], [180., 270.]])   # shape (2, 2), en grados
np.deg2rad(T).shape       # (2, 2)  → shape idéntico
np.deg2rad(T)
# [[0.        , 1.57079633],
#  [3.14159265, 4.71238898]]
```

## Vectorización

`np.deg2rad` reemplaza un bucle que multiplicaría cada elemento por `pi/180`. La versión vectorizada
corre el bucle en C, sobre memoria contigua:

```python
# Bucle Python (lento):
out = np.empty_like(arr)
for i in range(arr.size):
    out.flat[i] = arr.flat[i] * np.pi / 180

# ufunc (un único bucle en C):
out = np.deg2rad(arr)
```

Es el principio de [[concepto_vectorizacion]]: describes la transformación, no la iteración. Multiplicar
por `np.pi / 180` a mano da lo mismo; `np.deg2rad` lo dice de forma explícita y autocontenida.

## Valor de retorno

`ndarray` (o escalar de NumPy si la entrada es escalar) con el **mismo shape** que `x` y dtype
**flotante**:

| Entrada (`x`) | dtype salida | nota |
|---------------|--------------|------|
| `float64` | `float64` | precisión por defecto |
| `float32` | `float32` | conserva la precisión |
| entero (`int64`...) | `float64` | se promueve a float |

```python
np.deg2rad(180.0)              # 3.141592653589793  (escalar)
np.deg2rad([0, 90, 180]).dtype # float64
type(np.deg2rad([90]))         # numpy.ndarray
```

## Casos de uso

### Convertir antes de aplicar una función trigonométrica
```python
angulos = np.array([0, 30, 45, 60, 90])      # grados
np.sin(np.deg2rad(angulos))                  # [0., 0.5, 0.707…, 0.866…, 1.]
```

### Equivalencia con el alias y con la fórmula manual
```python
np.radians([180, 360])         # [3.1416…, 6.2832…]  (alias exacto)
np.deg2rad(90) == 90 * np.pi / 180   # True
```

### N-D: tabla de ángulos por elemento
```python
T = np.array([[0., 90.], [180., 270.]])      # (2, 2), grados
np.deg2rad(T)
# [[0.        , 1.57079633],
#  [3.14159265, 4.71238898]]                  # mismo shape, ahora en radianes
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `np.sin(90)` da `0.894…` en vez de `1` | se pasaron grados donde NumPy espera radianes | `np.sin(np.deg2rad(90))` |
| Confundir el sentido de la conversión | `deg2rad` va de grados **a** radianes | para el camino inverso usar [[np.rad2deg]] |
| Posiciones con basura tras `where` | `where=` sin `out` inicializado | pasar siempre `out=` junto con `where=` |

## Notas relacionadas

- [[concepto_ufuncs]] — `np.deg2rad` es una ufunc unaria; hereda `out`/`where`/`dtype`/`casting`
- [[np.rad2deg]] — su inversa: radianes → grados
- [[np.sin]] · [[np.cos]] · [[np.tan]] — esperan radianes, por eso esta conversión es previa
- [[Librerias/Numpy/np/operaciones/trigonometricas/index\|trigonométricas — todo en radianes]]
