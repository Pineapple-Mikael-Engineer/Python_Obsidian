---
title: Broadcasting — Alineacion automatica de shapes
aliases:
  - broadcasting
  - reglas de broadcasting
tags:
  - numpy
  - concepto
  - transformaciones
lib: numpy
tipo: concepto
requiere:
  - concepto_ndarray
  - concepto_shape
draft: false
---

# Broadcasting — Alineacion automatica de shapes

## Definicion fundamental

**Broadcasting** es el mecanismo por el cual [[concepto_ndarray|NumPy]] permite operar arrays de diferentes [[concepto_shape|shapes]] sin necesidad de copiar datos.

En lugar de exigir que todos los arrays tengan exactamente la misma forma, NumPy "estira" virtualmente los arrays mas pequeños para que coincidan con los mas grandes.

## Por que existe broadcasting

Sin broadcasting, para sumar un escalar a una matriz habria que:

```python
# Sin broadcasting (tedioso)
matriz = np.array([[1, 2, 3],
                   [4, 5, 6]])
escalar = 10
matriz_escalar = np.full((2, 3), escalar)  # Crear matriz de 10s
resultado = matriz + matriz_escalar        # Luego sumar

# Con broadcasting (directo)
resultado = matriz + 10  # NumPy hace el trabajo automaticamente
```

Broadcasting elimina la necesidad de crear arrays intermedios explícitos, ahorrando memoria y código.

## La regla central (unica regla)

Dos dimensiones son compatibles bajo broadcasting si:

| Condicion | Ejemplo | Compatible |
|-----------|---------|------------|
| Son iguales | `5` y `5` | SI |
| Una de ellas es 1 | `5` y `1` | SI |
| Ninguna condicion se cumple | `5` y `3` | NO |

**Esta es la unica regla que hay que memorizar.**

## Algoritmo paso a paso

### Paso 1: Alinear por la derecha

NumPy compara las dimensiones de derecha a izquierda (desde las ultimas dimensiones hacia las primeras).

### Paso 2: Aplicar la regla a cada par

Para cada par de dimensiones (una de cada array), verificar si son compatibles.

### Paso 3: Determinar el shape resultado

Cada dimension del resultado es el maximo de las dos dimensiones comparadas.

### Paso 4: Si algun par es incompatible → error

## Tabla de compatibilidad (casos fundamentales)

| Shape A | Shape B | Comparacion (der → izq) | Compatible | Shape resultado |
|---------|---------|------------------------|------------|-----------------|
| `(3, 4)` | `(4,)` | `4` vs `4` = OK; `3` vs `1` (implícito) = OK | SI | `(3, 4)` |
| `(3, 4)` | `(3, 1)` | `4` vs `1` = OK; `3` vs `3` = OK | SI | `(3, 4)` |
| `(3, 4)` | `(1, 4)` | `4` vs `4` = OK; `3` vs `1` = OK | SI | `(3, 4)` |
| `(3, 4)` | `(1, 1)` | `4` vs `1` = OK; `3` vs `1` = OK | SI | `(3, 4)` |
| `(3, 4)` | `(5, 4)` | `4` vs `4` = OK; `3` vs `5` = NO | NO | Error |
| `(5, 3, 4)` | `(3, 4)` | `4` vs `4` = OK; `3` vs `3` = OK; `5` vs `1` (implícito) = OK | SI | `(5, 3, 4)` |
| `(5, 3, 4)` | `(5, 4)` | `4` vs `4` = OK; `3` vs `5` = NO | NO | Error |
| `(1, 4, 1)` | `(3, 1, 5)` | `1` vs `5` = OK; `4` vs `1` = OK; `1` vs `3` = OK | SI | `(3, 4, 5)` |

## Ejemplos progresivos

### Nivel 1: Escalar + array (el mas simple)

```python
import numpy as np

arr = np.array([[1, 2, 3],
                [4, 5, 6]])
escalar = 10

resultado = arr + escalar
# escalar se trata como shape (1,1)
# Se "estira" virtualmente a (2,3)
# Resultado: [[11, 12, 13],
#             [14, 15, 16]]
```

**Visualizacion:**
```
Shape A: (2, 3)
Shape B: (1, 1)  ← escalar
Result:  (2, 3)
```

### Nivel 2: Vector fila + vector columna

```python
fila = np.array([1, 2, 3])      # shape (3,)
columna = np.array([[4],
                    [5],
                    [6]])       # shape (3, 1)

resultado = fila + columna
```

**Paso a paso:**

| Array | Shape original | Shape despues de broadcasting |
|-------|---------------|-------------------------------|
| Fila | `(3,)` | `(3, 3)` |
| Columna | `(3, 1)` | `(3, 3)` |
| Resultado | - | `(3, 3)` |

**Resultado numerico:**
```python
# fila estirada: [[1,2,3],
#                 [1,2,3],
#                 [1,2,3]]

# columna estirada: [[4,4,4],
#                    [5,5,5],
#                    [6,6,6]]

# suma: [[5,6,7],
#        [6,7,8],
#        [7,8,9]]
```

### Nivel 3: Array 3D + vector (dimensiones intermedias)

```python
arr_3d = np.ones((2, 3, 4))     # shape (2, 3, 4)
vector = np.array([1, 2, 3, 4]) # shape (4,)

resultado = arr_3d + vector
```

**Transformacion del vector:**
```
(4,) → (1, 1, 4) → (2, 3, 4)
```

**Resultado:** Cada fila de la ultima dimension suma `[1,2,3,4]` a todos los 2×3×4 elementos.

## Casos que fallan (errores tipicos)

### Error 1: Dimensiones intermedias incompatibles

```python
arr = np.ones((3, 4))
vector = np.array([1, 2, 3])  # shape (3,)

arr + vector
# (3,4) vs (3,)
# Comparacion: 4 vs 3 → NO compatible
# ValueError: operands could not be broadcast together
```

**Solucion:** Usar `reshape` o `np.newaxis`:
```python
vector_columna = vector[:, np.newaxis]  # shape (3, 1)
arr + vector_columna  # OK → (3,4)
```

### Error 2: Demasiadas dimensiones sin coincidencia

```python
arr = np.ones((2, 3, 4))
vector = np.array([1, 2])  # shape (2,)

arr + vector
# (2,3,4) vs (2,)
# Comparacion: 4 vs 2 → NO compatible
# Error
```

## Memoria y rendimiento (por que broadcasting es eficiente)

**Broadcasting NO crea copias de datos.**

El "estiramiento" es virtual y se implementa mediante [[concepto_views_vs_copias|vistas]] con `strides` especiales donde algunos pasos son cero.

### Verificacion con `strides`

```python
arr = np.array([1, 2, 3])
arr_estirando = arr[:, np.newaxis]  # shape (3, 1)

print(arr_estirando.strides)
# Salida: (8, 0)  ← el stride 0 indica repeticion sin copiar datos
```

El stride 0 significa que para avanzar en esa dimension, no se mueve el puntero de memoria; se repite el mismo valor.

### Comparacion de rendimiento

| Metodo | Tiempo (aprox) | Memoria extra | Uso de CPU |
|--------|---------------|---------------|------------|
| Con broadcasting | 1× (base) | 0 bytes | Bajo |
| Creando arrays explicitos | 3-5× | n× elementos | Alto |

## Reglas para predecir el shape resultado (resumen)

1. El shape resultado tiene tantas dimensiones como el array con mas dimensiones
2. Para cada posicion (de derecha a izquierda):
   - Si ambas dimensiones existen: el resultado es `max(dim_A, dim_B)`
   - Si solo una existe: el resultado toma esa dimension
3. Si en alguna posicion las dimensiones son diferentes y ninguna es 1 → error

**Ejercicio mental:** ¿Que shape resulta de estas operaciones?

| Operacion | Shape A | Shape B | Shape resultado |
|-----------|---------|---------|-----------------|
| `A + B` | `(6, 1)` | `(5,)` | ? |
| `A + B` | `(4, 1, 6)` | `(2, 1, 5)` | ? |
| `A + B` | `(1, 5, 1, 4)` | `(3, 1, 4, 1)` | ? |

**Respuestas:**
1. `(6, 5)` — porque: `(6,1) + (1,5) → (6,5)`
2. `(4, 2, 6, 5)` — porque: `(4,1,6,1) + (1,2,1,5) → (4,2,6,5)`
3. `(3, 5, 4, 4)` — porque: `(1,5,1,4) + (3,1,4,1) → (3,5,4,4)`

## Casos especiales: `np.newaxis` y `reshape`

Para forzar broadcasting cuando las dimensiones no coinciden naturalmente:

### `np.newaxis` (alias de `None`)

Inserta una dimension de tamaño 1 en la posicion indicada:

```python
vector = np.array([1, 2, 3])  # shape (3,)

# Convertir a vector columna
columna = vector[:, np.newaxis]  # shape (3, 1)

# Convertir a vector fila
fila = vector[np.newaxis, :]  # shape (1, 3)
```

### Uso combinado con operaciones

```python
arr = np.ones((4, 4))
vector = np.array([1, 2, 3, 4])

# Sumar vector a cada fila (necesita shape (1,4) o (4,))
arr + vector  # OK

# Sumar vector a cada columna (necesita shape (4,1))
arr + vector[:, np.newaxis]  # OK
```

## Relacion con otros conceptos

- [[concepto_ndarray]]
- [[concepto_shape]]
- [[concepto_vectorizacion]]
- [[concepto_ufuncs]]
- [[np.reshape]]
- [[np.newaxis]]
