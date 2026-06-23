---
title: np.ndarray — métodos de serialización
tags:
  - numpy
  - indice
draft: false
---

# np.ndarray — métodos de serialización

Estos cinco **métodos propios del `ndarray`** convierten o guardan el array fuera del ecosistema NumPy: a
una estructura de Python, a bytes en memoria, o a un archivo. Ninguno modifica el array original (solo lo
exportan). La pregunta que decide cuál usar es siempre la misma: **¿necesito poder reconstruir el array
exacto después, y dónde va el resultado?**

- [[ndarray.tolist]] — a una **lista anidada de Python** (escalares nativos). Pierde el dtype; ideal para JSON.
- [[ndarray.tobytes]] — a los **bytes crudos** del buffer, en memoria. Sin metadatos.
- [[ndarray.tofile]] — a un **archivo binario crudo** (o texto). Rápido, no portable.
- [[ndarray.dump]] — a un **archivo** con pickle. Conserva dtype y shape.
- [[ndarray.dumps]] — a **bytes** con pickle. Conserva dtype y shape, en memoria.

## Tabla comparativa

| Método | Formato | Inverso | ¿Portable? |
|--------|---------|---------|------------|
| `tolist` | lista de Python anidada | `np.array(lista, dtype=...)` | Sí (pierde el dtype) |
| `tobytes` | `bytes` crudos del buffer | `np.frombuffer(b, dtype=...).reshape(...)` | No (dtype/shape/endianness aparte) |
| `tofile` | archivo binario crudo (o texto) | `np.fromfile(f, dtype=...).reshape(...)` | No (dtype/shape/endianness aparte) |
| `dump` | archivo pickle | `np.load(f, allow_pickle=True)` / `pickle.load` | Parcial (depende de versiones, inseguro) |
| `dumps` | `bytes` pickle | `pickle.loads(b)` | Parcial (depende de versiones, inseguro) |

El eje que organiza la tabla: **crudo** (`tobytes`/`tofile`) frente a **autodescriptivo** (`dump`/`dumps`),
y **memoria** (`tolist`/`tobytes`/`dumps`) frente a **disco** (`tofile`/`dump`).

## La recomendación general

Para **guardar arrays de verdad** (persistirlos y releerlos exactos más tarde), ninguno de estos cinco es
la primera opción: usa **`np.save`** (formato `.npy`), que guarda dtype, shape y endianness en una
cabecera y se relee con un simple `np.load("x.npy")`, sin recordar metadatos, de forma portable entre
versiones y **sin el riesgo de seguridad de pickle**.

```python
np.save("arr.npy", arr)        # portable, autodescriptivo, seguro
back = np.load("arr.npy")      # round-trip exacto, shape y dtype incluidos
```

Cuándo usar cada uno de los métodos propios:
- **`tolist`** → frontera con código no-NumPy (JSON, APIs, plantillas).
- **`tobytes`** → enviar por red, hashear, o columna BLOB, controlando tú el dtype/shape.
- **`tofile`** → interoperar con C/Fortran que esperan un buffer crudo concreto.
- **`dump` / `dumps`** → caché o snapshot **de confianza** dentro de tu propio proceso (nunca datos ajenos).

## Notas relacionadas

- [[concepto_dtype]] — el metadato que estos métodos conservan o descartan
- [[concepto_contiguidad_memoria]] — el `order` en que se serializan los bytes
- [[np.save]] · [[np.fromfile]] · [[np.frombuffer]]
