---
title: np.savez_compressed — guarda VARIOS arrays comprimidos en un .npz (zip deflate)
aliases:
  - savez_compressed
  - np.savez_compressed
tags:
  - numpy
  - api/funcion
  - io

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: None
inplace: false

# --- Dependencias ---
requiere:
  - concepto_dtype

draft: false
---

# np.savez_compressed — guarda VARIOS arrays comprimidos en un .npz

`np.savez_compressed` es idéntica a [[np.savez]] —agrupa varios arrays con nombre en un `.npz`— pero
**comprime** cada miembro con el algoritmo **deflate** del formato zip. Produce archivos más
pequeños a cambio de más CPU al guardar y al cargar. Se usa exactamente igual (kwargs nombrados) y se
recupera con [[np.load]] sin cambios; cada array conserva su `shape` N-D y su
[[concepto_dtype|dtype]] exactos.

## La idea

Mismo contenedor `.npz` que `savez`, pero las entradas se guardan **comprimidas**. El compromiso:

| Aspecto | [[np.savez]] (sin comprimir) | `np.savez_compressed` (deflate) |
|---------|------------------------------|----------------------------------|
| Tamaño en disco | mayor | **menor** |
| CPU al guardar | rápido | más lento (comprime) |
| CPU al cargar | rápido | más lento (descomprime) |
| Ideal para | acceso frecuente, datos aleatorios | archivado, datos con **redundancia** |

La compresión solo compensa cuando los datos tienen **redundancia** (muchos ceros, valores
repetidos, máscaras booleanas, arrays dispersos): ahí el `.npz` puede encoger varios órdenes de
magnitud. En datos **aleatorios** (ruido, `float` sin estructura) apenas ahorra y solo añade CPU; en
ese caso `savez` a secas es mejor.

> [!tip] Cuándo compensa
> Pásate a `savez_compressed` cuando el tamaño/transferencia importe **y** los datos sean
> redundantes, o cuando guardes para archivar y leas pocas veces. Si vas a recargar muy a menudo,
> [[np.savez]] sin comprimir es más rápido.

## Firma

```python
np.savez_compressed(
    file,        # str | Path | file-object: destino (añade .npz si falta)
    *args,       # arrays posicionales → nombres automáticos arr_0, arr_1, ...
    **kwds,      # arrays por palabra clave → nombre = la clave (recomendado)
) -> None
```

## Los parámetros en detalle

Idénticos a [[np.savez]]: `file` es el destino (añade `.npz` si falta), `*args` da nombres
automáticos `arr_0`, `arr_1`, … y `**kwds` guarda cada array bajo su clave (la forma recomendada y
legible). La **única** diferencia frente a `savez` es interna: cada miembro se escribe con
compresión deflate en lugar de almacenarse tal cual.

## Round-trip

El ciclo es `np.savez_compressed` ↔ [[np.load]], igual que `savez` (la descompresión es
transparente). Forma y tipo se restauran exactos.

```python
import numpy as np

X = np.zeros((1000, 1000))        # mucha redundancia (ceros) → comprime muy bien
y = np.arange(1000)
np.savez_compressed('datos.npz', X=X, y=y)

with np.load('datos.npz') as d:   # NpzFile lazy; cerrar con with
    d.files                       # ['X', 'y']
    d['X'].shape                  # (1000, 1000)  → recuperado exacto
```

### Conservación del shape en 4D/5D

La compresión no toca la cabecera `.npy` de cada miembro: la forma N-D vuelve intacta.

```python
cubo  = np.zeros((2, 2, 2, 2, 2))         # 5D, todo ceros → comprime muchísimo
plano = np.ones((4, 3, 8, 8), np.int8)    # 4D, repetitivo
np.savez_compressed('mixto.npz', cubo=cubo, plano=plano)

with np.load('mixto.npz') as d:
    d['cubo'].shape == cubo.shape         # True → (2, 2, 2, 2, 2)
    d['plano'].shape == plano.shape       # True → (4, 3, 8, 8)
    np.array_equal(d['cubo'], cubo)       # True
```

## Casos de uso

### Archivar datasets dispersos o repetitivos

```python
np.savez_compressed('mascaras.npz', m1=mascara1, m2=mascara2)
# máscaras booleanas → enorme redundancia → archivo diminuto
```

### Reducir el tamaño de un dataset que se transfiere por red

```python
np.savez_compressed('entrega.npz', X=X, y=y)   # menos bytes que viajan
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Carga más lenta de lo esperado | descompresión en cada `np.load` | usar [[np.savez]] si prima la velocidad |
| Sin ahorro de tamaño | datos aleatorios (sin redundancia) | la compresión no ayuda; usar `savez` |
| Esperabas un array y recibes `NpzFile` | `.npz` con varios | indexar por nombre `d['x']` |
| El contenedor no se libera | `np.load` sin cerrar | usar `with np.load(...) as d:` |

## Notas relacionadas

- [[concepto_dtype]] — conservado por cada miembro comprimido
- [[np.savez]] — la versión sin comprimir (más rápida)
- [[np.save]] — para **un** solo array
- [[np.load]] — el inverso (descomprime de forma transparente)
