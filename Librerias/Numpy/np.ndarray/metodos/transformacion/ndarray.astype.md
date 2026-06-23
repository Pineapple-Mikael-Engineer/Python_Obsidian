---
title: ndarray.astype — convierte el array a otro dtype (devuelve una copia)
aliases:
  - astype
  - ndarray.astype
tags:
  - numpy
  - api/metodo
  - dtype
lib: numpy
mod: np.ndarray
obj: ndarray
tipo: metodo
retorna: ndarray
inplace: false
requiere:
  - concepto_dtype
  - concepto_views_vs_copias
draft: false
---

# ndarray.astype — convierte el array a otro dtype (devuelve una copia)

`astype` es el método **central de conversión de tipo** del `ndarray`: produce un array nuevo con el mismo shape pero **otro [[concepto_dtype|dtype]]**, convirtiendo cada valor al tipo destino (float → int trunca, int → bool compara con cero, etc.). A diferencia de [[ndarray.view]], que reinterpreta los mismos bytes, `astype` **convierte de verdad los valores** y por eso **devuelve siempre una copia** con buffer propio (salvo el atajo `copy=False` cuando ya coincide todo).

## La idea

`astype` recorre el array y **convierte cada elemento** al `dtype` pedido, escribiendo el resultado en un buffer nuevo. No cambia el shape: solo la interpretación numérica de cada elemento.

$$ \texttt{ndarray}[\,\text{shape}=S,\ \text{dtype}=\tau_0\,] \ \xrightarrow{\ \texttt{astype}(\tau_1)\ }\ \texttt{ndarray}[\,\text{shape}=S,\ \text{dtype}=\tau_1\,]\ \text{(copia)} $$

La conversión sigue las reglas del sistema de tipos: de flotante a entero **trunca hacia cero** (no redondea), y si el valor no cabe en el dtype destino se produce **overflow** silencioso. El array original **nunca** se toca.

## Firma

```python
ndarray.astype(
    dtype,                 # tipo destino: clase, string o np.dtype
    order='K',             # 'C' | 'F' | 'A' | 'K': layout en memoria del resultado
    casting='unsafe',      # 'no' | 'equiv' | 'safe' | 'same_kind' | 'unsafe'
    subok=True,            # bool: conservar la subclase del array
    copy=True,             # bool: forzar copia aun si el dtype ya coincide
) -> ndarray
```

## Los parámetros en detalle

### `dtype` — tipo destino

Cualquier especificador de [[concepto_dtype|dtype]]: una clase (`np.int32`), una string (`'float32'`, `'<i4'`, `'U10'`) o un `np.dtype`. Es el único parámetro obligatorio.

```python
arr.astype('float32')   # equivalente a np.float32
arr.astype('U10')       # texto Unicode de hasta 10 caracteres
arr.astype('>i4')       # int32 big-endian (cambia también el byte order)
```

### `order` — disposición en memoria del resultado

Controla el layout del buffer de la copia (ver [[concepto_contiguidad_memoria|contigüidad]]):

| `order` | Resultado |
|---------|-----------|
| `'C'` | C-contiguo (por filas) |
| `'F'` | F-contiguo (por columnas) |
| `'A'` | `'F'` si el origen es F-contiguo, si no `'C'` |
| `'K'` (defecto) | conserva el layout del origen lo más posible |

### `casting` — política de conversión

Decide **qué conversiones se permiten**, de más estricta a más laxa. El defecto de `astype` es `'unsafe'` (lo permite todo), pero subir el rigor sirve para que NumPy **falle pronto** ante una conversión con pérdida en lugar de truncar en silencio:

| `casting` | Permite | Ejemplo permitido | Ejemplo rechazado |
|-----------|---------|-------------------|-------------------|
| `'no'` | nada | — | cualquier cambio |
| `'equiv'` | solo cambio de byte order | `<i4 → >i4` | `int32 → int64` |
| `'safe'` | solo sin pérdida | `int32 → int64` | `float64 → int32` |
| `'same_kind'` | dentro del kind o ensanchando | `float64 → float32` | `float → int` |
| `'unsafe'` (defecto) | todo | `float64 → int8` | — |

```python
a = np.array([1.5, 2.5])
a.astype(np.int32)                   # OK con 'unsafe' por defecto → [1, 2]
a.astype(np.int32, casting='safe')   # TypeError → float→int no es safe
```

### `copy` — evitar la copia cuando ya coincide

Con el valor por defecto `True`, **siempre** devuelve una copia nueva, aunque el dtype destino sea idéntico al origen. Con `copy=False`, si el array ya tiene el dtype y el order pedidos, devuelve el **mismo objeto** sin copiar; en cualquier otro caso copia igual (la conversión obliga).

```python
arr = np.array([1, 2], dtype=np.int32)
arr.astype(np.int32, copy=False) is arr   # True  → nada que convertir, sin copia
arr.astype(np.int64, copy=False) is arr   # False → debe convertir, copia
```

### `subok` — conservar la subclase

Con `True` (defecto), si `self` es una subclase de `ndarray` (p. ej. `np.matrix`, `np.ma.MaskedArray`), el resultado mantiene esa subclase. Con `False`, el resultado es un `ndarray` base.

## ¿Vista o copia?

**Siempre copia** (con la única excepción de `copy=False` + dtype/order ya coincidentes, donde devuelve el mismo objeto). Es la frontera con [[ndarray.view]]: convertir valores exige escribir bytes nuevos, así que el resultado tiene **buffer propio** (`base is None`, `flags.owndata == True`) y el original queda intacto.

```python
arr = np.array([1.7, 2.9, 3.1])
out = arr.astype(np.int32)
out                # array([1, 2, 3], dtype=int32)  → trunca, NO redondea
out.base is None   # True  → copia independiente
arr                # array([1.7, 2.9, 3.1])  → original intacto
```

> [!warning] `astype` convierte, `view` reinterpreta
> `arr.astype(np.int32)` calcula el entero equivalente de cada float (con copia). `arr.view(np.int32)` lee los **mismos bytes** del float como si fueran un entero (sin copia, valores "raros"). No son intercambiables.

## Valor de retorno

Un `ndarray` nuevo con el **mismo shape** que `self` y el `dtype` pedido. El layout depende de `order`. Es el único método de este grupo que **cambia el dtype del resultado**.

| Entrada | Llamada | Salida (valores, dtype) |
|---------|---------|-------------------------|
| `[1.7, 2.9]` float64 | `arr.astype(np.int32)` | `[1, 2]` int32 (trunca hacia 0) |
| `[0, 1, 2]` int64 | `arr.astype(bool)` | `[False, True, True]` (0 → False) |
| `[1, 0]` int64 | `arr.astype(np.float64)` | `[1., 0.]` float64 |
| `['10', '20']` str | `arr.astype(np.int64)` | `[10, 20]` int64 (parsea texto) |
| `[300]` int64 | `arr.astype(np.int8)` | `[44]` int8 (overflow: 300 mod 256) |

## Casos de uso

### Reducir memoria bajando el dtype

```python
img = np.zeros((1000, 1000))    # float64 → 8 MB
img8 = img.astype(np.uint8)     # uint8   → 1 MB (8× menos)
```

### Redondear antes de convertir a entero

Como `astype` **trunca**, para redondear hay que aplicar `np.round` primero:

```python
arr = np.array([3.99, 1.01, 2.5])
arr.astype(np.int32)             # [3, 1, 2]  → trunca hacia cero
np.round(arr).astype(np.int32)  # [4, 1, 2]  → redondea primero
```

### Parsear texto a número

```python
ids = np.array(['10', '20', '30'])
ids.astype(np.int64)             # [10, 20, 30]  → texto a int
```

### Ejemplo realista: normalizar una imagen uint8 a float

Patrón típico en procesamiento de imágenes: subir a flotante para operar y volver a `uint8` para guardar.

```python
img = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)

f = img.astype(np.float32) / 255.0     # a [0, 1] en float32 (copia)
f = np.clip(f * 1.2, 0, 1)             # operaciones en float
out = (f * 255).round().astype(np.uint8)   # de vuelta a uint8 para guardar
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Esperar redondeo float → int | `astype` trunca hacia cero | `np.round(arr).astype(int)` |
| `TypeError` de casting | conversión no permitida por `casting` | bajar a `casting='unsafe'` (defecto) o convertir antes |
| Overflow silencioso al bajar de tamaño | dtype destino sin rango suficiente | elegir un dtype más ancho; validar el rango |
| Modificar `out` y esperar que cambie `arr` | `astype` devuelve una copia | trabajar sobre el array devuelto |
| Copia cara en bucle caliente | `astype` copia siempre | convertir una sola vez fuera del bucle |

## Notas relacionadas

- [[concepto_dtype]] — el sistema de tipos, la promoción y el casting
- [[concepto_views_vs_copias]] — por qué `astype` cae del lado "copia"
- [[ndarray.view]] — reinterpretar bytes en vez de convertir valores
- [[ndarray.copy]] — copia sin cambiar el dtype
- [[ndarray.dtype]] — consultar el dtype actual del array
