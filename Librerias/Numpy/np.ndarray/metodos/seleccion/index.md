---
title: np.ndarray — metodos de seleccion
tags:
  - numpy
  - indice
draft: false
---

# np.ndarray — metodos de seleccion

Los 4 metodos de seleccion extraen o modifican elementos del array usando indices enteros o condiciones booleanas. Complementan el indexado por corchetes (`arr[...]`) con una interfaz de metodo.

## Tabla de metodos

| Metodo | Firma resumida | Descripcion |
|--------|---------------|-------------|
| [[ndarray.take]] | `arr.take(indices, axis=None)` | Extrae elementos por indices; equivalente a fancy indexing |
| [[ndarray.put]] | `arr.put(indices, values)` | Modifica elementos in-place por indices en el array aplanado |
| [[ndarray.compress]] | `arr.compress(condition, axis=None)` | Filtra elementos donde la mascara booleana es `True` |
| [[ndarray.nonzero]] | `arr.nonzero()` | Devuelve las posiciones de elementos distintos de cero |

## Notas de uso

### `take` — extraccion por indices

Equivalente a fancy indexing pero con soporte explicito de `axis`. Siempre devuelve una **copia**:

```python
arr = np.array([10, 20, 30, 40])
arr.take([0, 2])        # → [10, 30]
arr[[0, 2]]             # identico (fancy indexing)
```

### `put` — escritura in-place por indices

Opera sobre el array aplanado. Modifica `self` sin devolver nada (`None`):

```python
arr = np.zeros(5)
arr.put([1, 3], [9, 7])  # arr → [0, 9, 0, 7, 0]
```

### `compress` — filtrado por mascara

Similar a indexado booleano pero permite especificar el eje sobre el que se aplica la condicion:

```python
arr = np.array([[1, 2], [3, 4], [5, 6]])
arr.compress([True, False, True], axis=0)  # → [[1, 2], [5, 6]]
```

### `nonzero` — posiciones de elementos no nulos

Devuelve una tupla de arrays de indices, uno por dimension. Util para localizar elementos antes de operar:

```python
arr = np.array([0, 3, 0, 7])
arr.nonzero()  # → (array([1, 3]),)
```
