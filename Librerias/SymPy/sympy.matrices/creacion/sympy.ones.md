---
title: sympy.ones — matriz de unos r x c
aliases:
  - ones
  - matriz unos
tags:
  - sympy
  - api/funcion
  - matrices/creacion
lib: sympy
mod: sympy.matrices
tipo: funcion
retorna: Matrix
requiere:
  - Matrix
draft: false
---

# sympy.ones — matriz de unos r x c

`ones(r, c)` devuelve una [[Matrix]] de SymPy de tamano r×c donde **todos** los elementos son el entero simbolico `1`. Con un solo argumento es cuadrada r×r. Es el complemento natural de [[sympy.zeros]]: donde `zeros` inicializa en blanco, `ones` parte de una base uniforme de unos. Util para construir vectores de suma, matrices de promedio o como molde base antes de asignar valores individuales. Equivale a `numpy.ones` en el mundo exacto.

## Firma

```python
sympy.ones(
    r,        # int: numero de filas
    c=None,   # int opcional: numero de columnas; si None -> cuadrada r x r
) -> Matrix
```

## Valor de retorno

| Tipo | Forma | Significado |
|------|-------|-------------|
| `Matrix` | r x c (o r x r) | Todos los elementos son el entero simbolico `1` |

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Cuadrada r x r de unos | `ones(r)` |
| Rectangular r x c de unos | `ones(r, c)` |
| Vector columna de unos | `ones(r, 1)` |
| Vector fila de unos | `ones(1, c)` |

```python
from sympy import ones
ones(3)      # Matrix([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
ones(2, 3)   # Matrix([[1, 1, 1], [1, 1, 1]])
ones(3, 1)   # Matrix([[1], [1], [1]])
ones(1, 3)   # Matrix([[1, 1, 1]])
```

## Parametros en detalle

### `r` (obligatorio)

Numero de **filas**. Entero no negativo. Con `r = 0` devuelve una matriz vacia.

```python
from sympy import ones
ones(1)      # Matrix([[1]])
ones(4)      # Matrix([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]])
```

### `c` (opcional, defecto `None`)

Numero de **columnas**. Si se omite, `c = r` y la salida es cuadrada.

```python
from sympy import ones
ones(2, 4)   # Matrix([[1, 1, 1, 1], [1, 1, 1, 1]])
ones(4, 1)   # Matrix([[1], [1], [1], [1]])
```

## Casos de uso

### Vector de suma — sumar todos los elementos de una columna

```python
from sympy import ones, Matrix, symbols
a, b, c = symbols("a b c")
v = Matrix([a, b, c])       # vector columna
e = ones(1, 3)              # vector fila de unos
e * v                       # Matrix([[a + b + c]])   -> suma de componentes
```

### Escalar una matriz de unos para obtener una constante

```python
from sympy import ones, symbols
k = symbols("k", positive=True)
M = k * ones(3)             # Matrix([[k, k, k], [k, k, k], [k, k, k]])
```

### Molde base antes de personalizar

```python
from sympy import ones, symbols
x = symbols("x")
M = ones(2)
M[0, 1] = x                # solo cambiar un elemento
M                           # Matrix([[1, x], [1, 1]])
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `ones(2.0)` falla | Los argumentos deben ser enteros | Usar `ones(int(r))` |
| `ones((r, c))` falla | SymPy no acepta tupla | Usar `ones(r, c)` (argumentos separados) |
| Esperar `1.0` (flotante) | `ones` devuelve el entero simbolico `1` | Los valores son exactos; para flotantes usar NumPy |
| Olvidar que `Matrix` es mutable | La asignacion modifica el objeto | Copiar con `.copy()` si se quiere preservar el original |

## Notas relacionadas

- [[sympy.zeros]]
- [[sympy.eye]]
- [[sympy.diag]]
- [[sympy.matrices/creacion/index | creacion]]
- [[sympy.matrices/index | sympy.matrices]]
