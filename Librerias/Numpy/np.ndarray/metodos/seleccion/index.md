---
title: np.ndarray — metodos de seleccion
tags:
  - numpy
  - indice
draft: false
---

# np.ndarray — metodos de seleccion

4 metodos para extraer o modificar elementos del array usando indices enteros o condiciones booleanas. Complementan el indexado por corchetes (`arr[...]`) con una interfaz de metodo que en algunos casos es mas explicita o permite especificar el eje de operacion.

## Tabla de metodos

| Metodo | Firma resumida | Descripcion |
|--------|---------------|-------------|
| [[ndarray.take]] | `arr.take(indices, axis=None)` | Extrae elementos por indices con soporte explicito de `axis`; siempre devuelve copia |
| [[ndarray.put]] | `arr.put(indices, values)` | Modifica elementos in-place usando indices en el array aplanado; devuelve `None` |
| [[ndarray.compress]] | `arr.compress(condition, axis=None)` | Filtra filas o columnas donde la mascara booleana es `True`; siempre devuelve copia |
| [[ndarray.nonzero]] | `arr.nonzero()` | Devuelve las posiciones de todos los elementos distintos de cero, uno por dimension |

## `take` — extraccion por indices

Equivalente a fancy indexing pero con el parametro `axis` explicito, lo que evita ambiguedades en arrays multidimensionales. Siempre devuelve una **copia**:

```python
arr = np.array([[1, 2, 3],
                [4, 5, 6]])
arr.take([0, 2], axis=1)  # → [[1, 3], [4, 6]]  (columnas 0 y 2)
arr[:, [0, 2]]            # equivalente con fancy indexing
```

## `put` — escritura in-place por indices planos

Opera sobre el array visto como si fuera 1D (orden C). Modifica `self` directamente y devuelve `None`. Si `values` tiene menos elementos que `indices`, se repite en ciclo:

```python
arr = np.zeros(6).reshape(2, 3)
arr.put([1, 4], [9, 7])  # modifica los elementos planos 1 y 4
# arr → [[0, 9, 0], [0, 7, 0]]
```

## `compress` — filtrado por mascara

Similar a indexado booleano pero permite especificar el eje sobre el que se aplica la condicion. La longitud de `condition` debe coincidir con el tamaño de ese eje:

```python
arr = np.array([[1, 2],
                [3, 4],
                [5, 6]])
arr.compress([True, False, True], axis=0)  # → [[1, 2], [5, 6]]  (filas 0 y 2)
arr.compress([False, True], axis=1)        # → [[2], [4], [6]]   (columna 1)
```

## `nonzero` — posiciones de elementos no nulos

Devuelve una tupla de arrays de indices, uno por dimension. El resultado se puede usar directamente para indexar o para localizar elementos antes de operar:

```python
arr = np.array([[0, 3],
                [0, 7]])
rows, cols = arr.nonzero()
# rows → [0, 1],  cols → [1, 1]
arr[arr.nonzero()]  # → [3, 7]  (los elementos no nulos)
```

Para arrays 1D, el resultado es una tupla de un solo array:

```python
np.array([0, 3, 0, 7]).nonzero()  # → (array([1, 3]),)
```
