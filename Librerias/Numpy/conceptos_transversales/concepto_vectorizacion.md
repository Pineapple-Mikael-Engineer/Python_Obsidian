---
title: Vectorizacion — Operaciones sin bucles explicitos
aliases:
  - vectorization
  - codigo vectorizado
tags:
  - numpy
  - concepto
  - rendimiento
lib: numpy
tipo: concepto
requiere:
  - concepto_ndarray
  - concepto_broadcasting
  - concepto_ufuncs
draft: false
---

# Vectorizacion — Operaciones sin bucles explicitos

## Definicion fundamental

**Vectorizacion** es la tecnica de aplicar operaciones a arrays completos en lugar de hacerlo elemento por elemento mediante bucles explicitos en Python.

En lugar de:
```python
# Lento (Python loop)
for i in range(len(arr)):
    arr[i] = arr[i] * 2
```

Se escribe:
```python
# Rapido (vectorizado)
arr = arr * 2
```

## Por que vectorizar es crucial

### Comparacion de rendimiento

| Enfoque | Velocidad relativa | Codigo | Riesgo de errores |
|---------|-------------------|--------|------------------|
| Bucle Python puro | 1× (base lenta) | Muchas lineas | Alto |
| List comprehension | ~2-3× | Medio | Medio |
| NumPy vectorizado | ~50-100× | 1 linea | Bajo |

### Ejemplo concreto

```python
import numpy as np
import time

# Crear datos
arr = np.random.rand(1000000)

# Metodo 1: Bucle Python
inicio = time.time()
resultado_bucle = []
for x in arr:
    resultado_bucle.append(x ** 2 + np.sin(x))
tiempo_bucle = time.time() - inicio

# Metodo 2: Vectorizado
inicio = time.time()
resultado_vectorizado = arr ** 2 + np.sin(arr)
tiempo_vectorizado = time.time() - inicio

print(f"Bucle Python: {tiempo_bucle:.3f} seg")
print(f"Vectorizado: {tiempo_vectorizado:.3f} seg")
print(f"Aceleracion: {tiempo_bucle/tiempo_vectorizado:.0f}x")
```

**Salida tipica:**
```
Bucle Python: 1.767 seg
Vectorizado: 0.011 seg
Aceleracion: 160x
```

## El problema del bucle Python

Python es lento para operaciones numericas por varias razones:

| Causa | Explicacion | Impacto |
|-------|-------------|---------|
| Tipado dinamico | Python verifica el tipo en cada iteracion | Alto |
| Interpretado | No hay compilacion a codigo maquina | Alto |
| Overhead de objeto | Cada elemento es un objeto Python completo | Muy alto |
| Indireccion de memoria | Los elementos no son contiguos en memoria | Medio |

NumPy vectorizado opera directamente en el buffer de memoria C, evitando todo este overhead.

## Como funciona la vectorizacion internamente

### Modelo conceptual

```
Bucle Python:
┌─────────────────────────────────────────┐
│ Python interpreter                       │
│   for i in range(n):                     │
│     check type(arr[i])                   │
│     create Python object                 │
│     execute operation                    │
│     extract result                       │
│     store back                           │
└─────────────────────────────────────────┘
         ↓ (n iteraciones, lento)

Vectorizado:
┌─────────────────────────────────────────┐
│ C loop (compilado)                       │
│   for i in range(n):                     │
│     arr_c[i] = arr_c[i] * 2              │
└─────────────────────────────────────────┘
         ↓ (una llamada a C, rapido)
```

### El rol de las ufuncs

Las [[concepto_ufuncs|Universal Functions (ufuncs)]] son el mecanismo interno que NumPy usa para vectorizar operaciones.

```python
# Estas operaciones usan ufuncs internamente
arr + 1        # ufunc: np.add
arr * 2        # ufunc: np.multiply
np.sin(arr)    # ufunc: np.sin
arr > 0.5      # ufunc: np.greater
```

## Tipos de vectorizacion

### 1. Operaciones aritmeticas elemento a elemento

```python
arr = np.array([1, 2, 3, 4])

# Vectorizado
arr + 10      # [11, 12, 13, 14]
arr * 2       # [2, 4, 6, 8]
arr ** 2      # [1, 4, 9, 16]
1 / arr       # [1, 0.5, 0.333, 0.25]
```

### 2. Funciones matematicas universales

```python
arr = np.array([0, np.pi/2, np.pi])

np.sin(arr)   # [0, 1, 0]
np.cos(arr)   # [1, 0, -1]
np.exp(arr)   # [1, 4.81, 23.14]
np.log(arr + 1)  # [0, 0.45, 0.69]
```

### 3. Comparaciones y mascaras booleanas

```python
arr = np.array([1, 5, 2, 8, 3])

# Vectorizado
mascara = arr > 3        # [False, True, False, True, False]
resultado = arr[mascara] # [5, 8]

# Equivalente con bucle (mucho mas lento)
mascara_bucle = []
for x in arr:
    mascara_bucle.append(x > 3)
```

### 4. Reducciones (operaciones agregadas)

```python
arr = np.array([[1, 2, 3],
                [4, 5, 6]])

np.sum(arr)           # 21 (todos los elementos)
np.sum(arr, axis=0)   # [5, 7, 9] (por columna)
np.mean(arr, axis=1)  # [2, 5] (por fila)
np.max(arr)           # 6
```

### 5. Broadcasting combinado con vectorizacion

```python
# Broadcasting + vectorizacion = poder puro
matriz = np.random.rand(100, 100)
vector = np.random.rand(100)

# Esto es vectorizado Y usa broadcasting
resultado = matriz + vector  # Suma vector a cada fila
```

## Lo que NO es vectorizable (y como manejarlo)

### Caso 1: Dependencias secuenciales

```python
# NO vectorizable (cada paso depende del anterior)
arr = np.array([1, 2, 3, 4])
for i in range(1, len(arr)):
    arr[i] = arr[i-1] + arr[i]

# Alternativa: funciones acumulativas
arr = np.array([1, 2, 3, 4])
arr = np.cumsum(arr)  # [1, 3, 6, 10]
```

### Caso 2: Condiciones complejas con ramificacion

```python
# Dificil de vectorizar
for x in arr:
    if x < 0:
        resultado.append(0)
    elif x < 0.5:
        resultado.append(x * 2)
    else:
        resultado.append(x)

# Vectorizado con np.where
resultado = np.where(arr < 0, 0,
              np.where(arr < 0.5, arr * 2, arr))
```

### Caso 3: Funciones que operan sobre escalares

```python
def mi_funcion_escalar(x):
    # Logica compleja que solo acepta escalares
    return x ** 2 if x > 0 else 0

# NO funciona directamente con arrays
# arr_resultado = mi_funcion_escalar(arr)  # Error

# Solucion: np.vectorize (mas lento, pero funciona)
mi_funcion_vectorizada = np.vectorize(mi_funcion_escalar)
resultado = mi_funcion_vectorizada(arr)

# Mejor: reescribir para que sea vectorizada
def mi_funcion_vectorizada(arr):
    return np.where(arr > 0, arr ** 2, 0)
```

## Reglas para escribir codigo vectorizado

| Regla | Mal (lento) | Bien (rapido) |
|-------|-------------|---------------|
| Evitar bucles explicitos | `for i in range(len(arr)):` | `arr * 2` |
| Usar operadores aritmeticos | `np.add(arr, 1)` | `arr + 1` |
| Preferir ufuncs existentes | `np.fromiter(map(f, arr))` | `np.sin(arr)` |
| Usar slicing en lugar de indexado individual | `arr[i]` en bucle | `arr[inicio:fin]` |
| Combinar operaciones | `tmp1 = arr*2; tmp2 = tmp1+1` | `arr*2 + 1` |

## Medir vectorizacion con `%timeit`

En Jupyter/IPython:

```python
arr = np.random.rand(10000)

# Bucle Python
%%timeit
resultado = []
for x in arr:
    resultado.append(x ** 2)
# Salida: 100 loops, best of 5: 4.5 ms per loop

# List comprehension
%%timeit
resultado = [x ** 2 for x in arr]
# Salida: 1000 loops, best of 5: 1.2 ms per loop

# Vectorizado
%%timeit
resultado = arr ** 2
# Salida: 100000 loops, best of 5: 8.5 µs per loop
```

## Errores comunes al vectorizar

### Error 1: Mezclar tipos de datos

```python
arr = np.array([1, 2, 3], dtype=np.int32)
resultado = arr + 0.5  # dtype se convierte a float64 (ok, pero inesperado)
print(resultado.dtype)  # float64
```

### Error 2: Asumir que toda operacion vectorizada es automatica

```python
# Esto NO es vectorizado (sigue siendo Python puro)
arr = np.array([1, 2, 3])
resultado = [x * 2 for x in arr]  # List comprehension, no vectorizado

# Esto SI es vectorizado
resultado = arr * 2
```

### Error 3: Olvidar que las reducciones cambian dimension

```python
arr = np.array([[1, 2, 3],
                [4, 5, 6]])

suma_total = np.sum(arr)        # Escalar (0D)
suma_por_fila = np.sum(arr, axis=1)  # Vector (2,)
suma_por_columna = np.sum(arr, axis=0)  # Vector (3,)

# Para mantener dimensiones usar keepdims
suma_con_dim = np.sum(arr, axis=1, keepdims=True)  # (2, 1)
```

## Beneficios secundarios de la vectorizacion

| Beneficio | Explicacion |
|-----------|-------------|
| Codigo mas legible | Menos lineas, intencion clara |
| Menos bugs | Sin errores de indices de bucle |
| Mas facil de mantener | Expresiones matematicas directas |
| Documentacion implicita | La operacion es auto-evidente |
| Consistencia con matematicas | Se lee como formulas |

## Relacion con otros conceptos

- [[concepto_ndarray]]
- [[concepto_broadcasting]]
- [[concepto_ufuncs]]
- [[concepto_views_vs_copias]]
- [[np.where]]
- [[np.vectorize]]
