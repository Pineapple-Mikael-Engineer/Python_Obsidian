---
title: ndarray.dump — Serializar el array a archivo con pickle
aliases:
  - dump
  - ndarray.dump
tags:
  - numpy
  - api/metodo
  - io
lib: numpy
obj: ndarray
tipo: metodo
retorna: None
inplace: false
draft: false
---

# ndarray.dump — Serializar el array a archivo con pickle

## Firma del método

```python
ndarray.dump(file) -> None
```

## Valor de retorno

| Retorna | Significado |
|---------|-------------|
| `None` | Guarda el array serializado con **pickle** en `file`. No modifica el array (solo lo exporta). |

A diferencia de `tofile`, **sí preserva** `shape` y [[concepto_dtype|dtype]] porque serializa el objeto completo. Se recupera con `np.load(file, allow_pickle=True)` o con `pickle.load`.

```python
import numpy as np
arr = np.arange(6).reshape(2, 3)
arr.dump('estado.pkl')                          # crea estado.pkl
back = np.load('estado.pkl', allow_pickle=True) # array([[0,1,2],[3,4,5]])
```

## Parámetros en detalle

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `file` | str / Path / file | Destino donde escribir el pickle. |

```python
import pickle
with open('estado.pkl', 'rb') as f:
    back = pickle.load(f)       # también recupera con pickle estándar
```

## Casos de uso

```python
# Snapshot rápido de un array (incluyendo dtype y shape exactos)
modelo = np.random.rand(100, 100)
modelo.dump('checkpoint.pkl')
```

## Buenas prácticas

1. Para persistencia portable prefiere [[np.save]] (`.npy`); pickle es menos seguro/estable entre versiones.
2. **Nunca** cargues pickles de origen no confiable: `allow_pickle` ejecuta código.
3. Si necesitas los bytes en memoria en vez de un archivo, usa `dumps`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: allow_pickle=False` | `np.load` por defecto bloquea pickle | pasar `allow_pickle=True` |
| Pickle no carga en otra versión | formato dependiente de versión | usar `.npy` con [[np.save]] |
| Riesgo de seguridad | pickle ejecuta código al cargar | no abrir archivos ajenos |

## Notas relacionadas

- [[concepto_dtype]]
- [[np.save]]
- [[ndarray.dumps]]
