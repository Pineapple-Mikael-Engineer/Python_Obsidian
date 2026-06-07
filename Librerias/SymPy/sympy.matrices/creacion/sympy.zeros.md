---
title: sympy.zeros — matriz de ceros r x c
aliases:
  - zeros
  - matriz ceros
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

# sympy.zeros — matriz de ceros r x c

`zeros(r, c)` devuelve una [[Matrix]] de SymPy de tamano r×c rellena completamente de ceros simbolicos exactos (el entero `0`, no un flotante). Con un solo argumento `zeros(r)` la matriz es cuadrada r×r. Es el punto de partida tipico cuando se necesita construir una matriz elemento a elemento o acumular contribuciones dentro de un bucle simbolico, equivalente a `numpy.zeros` pero en el mundo exacto.

## Firma

```python
sympy.zeros(
    r,        # int: numero de filas
    c=None,   # int opcional: numero de columnas; si None -> cuadrada r x r
) -> Matrix
```

## Valor de retorno

| Tipo | Forma | Significado |
|------|-------|-------------|
| `Matrix` | r x c (o r x r) | Todos los elementos son el entero simbolico `0` |

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Cuadrada r x r de ceros | `zeros(r)` |
| Rectangular r x c de ceros | `zeros(r, c)` |

```python
from sympy import zeros
zeros(3)      # Matrix([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
zeros(2, 3)   # Matrix([[0, 0, 0], [0, 0, 0]])
zeros(1, 4)   # Matrix([[0, 0, 0, 0]])
```

## Parametros en detalle

### `r` (obligatorio)

Numero de **filas**. Entero no negativo. Con `r = 0` devuelve una matriz vacia.

```python
from sympy import zeros
zeros(2)     # Matrix([[0, 0], [0, 0]])
zeros(0, 3)  # Matrix(0, 3, [])  -> 0 filas, 3 columnas (vacia)
```

### `c` (opcional, defecto `None`)

Numero de **columnas**. Si se omite, la matriz es cuadrada.

```python
from sympy import zeros
zeros(3, 1)   # Matrix([[0], [0], [0]])   -> columna
zeros(1, 3)   # Matrix([[0, 0, 0]])       -> fila
```

## Casos de uso

### Inicializar una matriz y rellenar elemento a elemento

```python
from sympy import zeros, symbols
x, y = symbols("x y")
M = zeros(2)
M[0, 0] = x**2
M[1, 1] = y
M          # Matrix([[x**2, 0], [0, y]])
```

### Acumular la suma de matrices simbolicas

```python
from sympy import zeros, eye, symbols
a, b = symbols("a b", real=True)
acc = zeros(2)
for k, val in enumerate([a, b]):
    acc += val * eye(2)   # a*I + b*I
acc   # Matrix([[a + b, 0], [0, a + b]])
```

### Plantilla de matriz de coeficientes

```python
from sympy import zeros, symbols
a11, a12, a21, a22 = symbols("a11 a12 a21 a22")
A = zeros(2)
A[0, 0], A[0, 1] = a11, a12
A[1, 0], A[1, 1] = a21, a22
A   # Matrix([[a11, a12], [a21, a22]])
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `zeros(2.0)` falla | Los argumentos deben ser enteros | Usar `zeros(int(r))` |
| Esperar `0.0` (flotante) | `zeros` devuelve el entero simbolico `0` | Para flotantes usar `numpy.zeros`; en SymPy los ceros son exactos |
| Olvidar que `Matrix` es mutable | Las asignaciones modifican el objeto en sitio | Si se quiere conservar el original: `B = A.copy()` antes |
| Confundir con `numpy.zeros((r, c))` | SymPy usa argumentos posicionales, no tupla | Correcto: `zeros(r, c)`, no `zeros((r, c))` |

## Notas relacionadas

- [[sympy.ones]]
- [[sympy.eye]]
- [[sympy.diag]]
- [[sympy.matrices/creacion/index | creacion]]
- [[sympy.matrices/index | sympy.matrices]]
