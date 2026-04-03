---
title: Manejo Arrays Axes — Manejo de arrays de Axes
aliases:
  - arrays de axes
  - multiple axes
  - iterar subplots
  - Manejo Arrays Axes
tags:
  - matplotlib
  - api/clase
  - api/clase
lib: matplotlib
tipo: clase
muta_estado: false
requiere: []
draft: false
---






# Manejo de arrays de Axes

## Por qué existe esto

Cuando usas `plt.subplots()` con más de un subplot, el segundo valor retornado (`axs`) no es un objeto `Axes` único, sino un **array de NumPy** que contiene múltiples instancias de `Axes`.

```python
fig, axs = plt.subplots(2, 3)
type(axs)  # numpy.ndarray
axs.shape  # (2, 3)
```

Matplotlib usa arrays de NumPy para organizar los axes porque:
- Permite indexación por fila/columna
- Es consistente con la estructura visual de la grilla
- Facilita operaciones vectorizadas (aunque eso es más de NumPy)

---

## Formas del array según la configuración

La forma (shape) de `axs` depende de `nrows`, `ncols` y el parámetro `squeeze`:

| Configuración | `squeeze=True` (default) | `squeeze=False` |
|---------------|--------------------------|-----------------|
| `(1, 1)` | `Axes` (objeto, no array) | array de forma `(1, 1)` |
| `(1, N)` | array de forma `(N,)` | array de forma `(1, N)` |
| `(N, 1)` | array de forma `(N,)` | array de forma `(N, 1)` |
| `(N, M)` | array de forma `(N, M)` | array de forma `(N, M)` |

> [!warning] La inconsistencia es la principal fuente de errores. Un código que funciona con `(2, 2)` puede fallar con `(1, 3)`.

---

## Indexación de axes

### Grilla 2D (N > 1 y M > 1)

```python
fig, axs = plt.subplots(2, 3)

axs[0, 0]  # fila 0, columna 0
axs[1, 2]  # fila 1, columna 2
axs[-1, -1]  # última fila, última columna
```

### Una fila (N = 1, M > 1)

```python
fig, axs = plt.subplots(1, 3)  # axs.shape = (3,)

axs[0]  # primer axes
axs[2]  # tercer axes
```

### Una columna (N > 1, M = 1)

```python
fig, axs = plt.subplots(3, 1)  # axs.shape = (3,)

axs[0]  # primer axes
axs[2]  # tercer axes
```

### Caso especial (1, 1)

```python
fig, ax = plt.subplots()  # ax es un objeto Axes, no array

# No se puede indexar
# ax[0]  # TypeError
```

---

## Iteración sobre axes

### Para grillas 2D con `.flat`

`.flat` es un atributo de los arrays de NumPy que permite iterar sobre todos los elementos en orden (fila por fila).

```python
fig, axs = plt.subplots(2, 3)

for ax in axs.flat:
    ax.grid(True)
    ax.set_xlabel("Tiempo")
```

> [!tip] `.flat` funciona con arrays de cualquier dimensión. Es la forma más segura de iterar sobre todos los axes sin importar la forma.

### Para arrays 1D (iteración directa)

```python
fig, axs = plt.subplots(1, 3)  # o (3, 1)

for ax in axs:
    ax.set_ylim(0, 10)
```

### Con `enumerate` para índices

```python
for i, ax in enumerate(axs.flat):
    ax.set_title(f"Gráfico {i+1}")
```

### Con `zip` para datos múltiples

```python
datos = [data1, data2, data3, data4, data5, data6]
for ax, d in zip(axs.flat, datos):
    ax.plot(d)
```

---

## Patrón robusto (recomendado)

Para escribir código que funcione con **cualquier** configuración de subplots:

```python
import numpy as np

fig, axs = plt.subplots(nrows, ncols)

# Convertir a array 1D garantizado
if not isinstance(axs, np.ndarray):
    axs = np.array([axs])  # caso (1,1)
axs = axs.ravel()  # ahora siempre es 1D

# Iterar con confianza
for i, ax in enumerate(axs):
    ax.plot(x, y)
    ax.set_title(f"Subplot {i}")
```

Este patrón maneja:
- `(1, 1)` → array de 1 elemento
- `(1, N)` o `(N, 1)` → array 1D
- `(N, M)` → array 1D aplanado

---

## Errores comunes

### Error: asumir que `axs` es siempre 2D

```python
fig, axs = plt.subplots(1, 3)  # axs es 1D
axs[0, 1].plot(x, y)  # IndexError: too many indices for array
```

### Error: asumir que `axs` es siempre 1D

```python
fig, axs = plt.subplots(2, 2)  # axs es 2D
for ax in axs:  # itera sobre filas, no sobre axes
    ax.plot(x, y)  # AttributeError: 'numpy.ndarray' has no attribute 'plot'
```

### Error: olvidar el caso (1, 1)

```python
fig, ax = plt.subplots()  # ax NO es array
for a in ax.flat:  # AttributeError: 'Axes' object has no attribute 'flat'
    pass
```

---

## Patrones útiles específicos de matplotlib

### Aplicar configuración a todos los axes

```python
for ax in axs.flat:
    ax.grid(True, alpha=0.3)
    ax.set_facecolor('#f0f0f0')
    ax.tick_params(labelsize=8)
```

### Ocultar axes no utilizados

```python
fig, axs = plt.subplots(2, 2)
# Solo usamos 3 subplots, el último sobra
axs[1, 1].set_visible(False)
```

### Acceder a ejes compartidos

Cuando usas `sharex=True`, los axes comparten el mismo objeto de eje X:

```python
fig, axs = plt.subplots(2, 1, sharex=True)
axs[0].set_xlim(0, 10)  # automáticamente afecta a axs[1]
```

---

## Relación con NumPy

Los métodos mencionados (`.flat`, `.ravel()`, `.flatten()`, `.shape`) pertenecen a NumPy. Para entenderlos a fondo, consulta las notas de NumPy sobre:
- Indexación de arrays
- Atributos de arrays (shape, ndim, size)
- Métodos de aplanamiento (ravel, flatten)

En el contexto de matplotlib, solo necesitas saber:
- `axs.flat` → itera sobre todos los axes
- `axs.ravel()` → convierte a 1D (cuando ya es array)
- `axs.shape` → dimensiones de la grilla

---

## Notas relacionadas

- [[plt.subplots]]
- [[GridSpec]]
- [[ax.shared_axes]]
