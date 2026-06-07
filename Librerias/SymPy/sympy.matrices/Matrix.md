---
title: Matrix — matriz simbolica densa de algebra lineal exacta
aliases:
  - Matrix
  - matriz simbolica
tags:
  - sympy
  - api/clase
  - matrices
lib: sympy
mod: sympy.matrices
tipo: clase
retorna: Matrix
requiere:
  - Symbol
  - concepto_expr_arbol
draft: false
---

# Matrix — matriz simbolica densa de algebra lineal exacta

Clase central de [[sympy.matrices/index | sympy.matrices]]: representa una matriz densa cuyos elementos son **expresiones SymPy** (simbolos, racionales, funciones…). Toda operacion —determinante, inversa, valores propios— se realiza de forma **exacta** sobre el arbol simbolico, sin aproximacion flotante. Se construye pasando una lista de listas; a partir de ahi se comporta como un objeto de algebra lineal completo: soporta aritmetica matricial, indexacion `M[i, j]`, slicing, sustitucion con `.subs()` y transformacion elemento a elemento con `.applyfunc()`.

## Constructor

```python
sympy.Matrix(
    data,   # list[list]: lista de filas, cada fila es una lista de elementos
)           # -> Matrix
```

Los elementos de `data` pueden ser enteros, `Rational`, `Symbol`, cualquier `Expr` o incluso cero. SymPy infiere el numero de filas y columnas desde la estructura de listas.

## Atributos y metodos clave

| Miembro | Tipo | Significado |
|---------|------|-------------|
| `.shape` | `tuple` | `(filas, columnas)` |
| `.rows` | `int` | Numero de filas |
| `.cols` | `int` | Numero de columnas |
| `.T` | `Matrix` | Transpuesta |
| `M[i, j]` | `Expr` | Elemento en fila `i`, columna `j` (0-indexed) |
| `M[i, :]` | `Matrix` | Fila `i` completa (slice de fila) |
| `M[:, j]` | `Matrix` | Columna `j` completa (slice de columna) |
| `.det()` | metodo | Determinante exacto \| ver `[[Matrix.det]]` |
| `.inv()` | metodo | Inversa exacta (por adjunta o LU) \| ver `[[Matrix.inv]]` |
| `.rref()` | metodo | Forma escalonada reducida + pivotes \| ver `[[Matrix.rref]]` |
| `.eigenvals()` | metodo | `{valor_propio: multiplicidad}` \| ver `[[Matrix.eigenvals]]` |
| `.eigenvects()` | metodo | `[(val, mult, [vecs])]` \| ver `[[Matrix.eigenvects]]` |
| `.nullspace()` | metodo | Lista de vectores de la base del nucleo \| ver `[[Matrix.nullspace]]` |
| `.subs(old, new)` | metodo | Sustituye un simbolo en todos los elementos |
| `.applyfunc(f)` | metodo | Aplica `f` elemento a elemento; devuelve nueva `Matrix` |
| `.tolist()` | metodo | Convierte a lista de listas de Python |

## Ejemplo

```python
from sympy import symbols, Matrix, Rational

x, y = symbols("x y")

# Construccion
M = Matrix([[1, x], [y, 2]])
M                               # Matrix([[1, x], [y, 2]])
M.shape                         # (2, 2)

# Acceso e indexacion
M[0, 1]                         # x
M[1, :]                         # Matrix([[y, 2]])

# Transpuesta
M.T                             # Matrix([[1, y], [x, 2]])

# Determinante y aritmetica exacta
M.det()                         # 2 - x*y

# Sustitucion simbolica
M.subs(x, 3).subs(y, 0)         # Matrix([[1, 3], [0, 2]])

# Matriz numerica exacta (Rational)
A = Matrix([[1, 2], [3, 4]])
A.det()                         # -2
A.inv()                         # Matrix([[-2, 1], [3/2, -1/2]])

# Multiplicacion matricial
B = Matrix([[0, 1], [1, 0]])
A * B                           # Matrix([[2, 1], [4, 3]])

# applyfunc: elevar al cuadrado cada elemento
A.applyfunc(lambda e: e**2)     # Matrix([[1, 4], [9, 16]])

# tolist: salir del objeto Matrix
A.tolist()                      # [[1, 2], [3, 4]]
```

## Cuando usar Matrix

| Situacion | Recomendacion |
|-----------|---------------|
| Algebra lineal exacta con simbolos o racionales | `Matrix` de SymPy |
| Calculo numerico con flotantes grandes | `numpy.ndarray`; mucho mas rapido |
| Valores propios / vectores exactos (sistema pequeno) | `Matrix` (`.eigenvals()`, `.eigenvects()`) |
| Valores propios numericos (dimension grande) | `numpy.linalg.eig` o `scipy.linalg.eig` |
| Forma escalonada o espacio nulo exacto | `Matrix` (`.rref()`, `.nullspace()`) |
| Operaciones estadisticas / broadcasting | `numpy.ndarray` |
| Resolver `A x = b` exactamente | `A.solve(b)` o `A.inv() * b` (con `Matrix`) |
| Resolver `A x = b` numericamente | `numpy.linalg.solve` |

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `ShapeError` en multiplicacion | Dimensiones incompatibles (`A * B` requiere `A.cols == B.rows`) | Verifica `.shape` de cada matriz antes de multiplicar |
| `NonInvertibleMatrixError` en `.inv()` | El determinante es cero; la matriz es singular | Comprueba `M.det() != 0`; usa `.nullspace()` si te interesa el nucleo |
| Elementos flotantes danan la exactitud | Mezclar `0.5` con simbolos introduce `Float` en lugar de `Rational` | Usa `Rational(1, 2)` o `S.Half` en lugar de literales flotantes |
| `.eigenvals()` lento o sin resultado cerrado | Polinomio caracteristico de grado >= 5 sin raices simbolicas sencillas | Limita el caso simbolico a matrices pequenas (2x2, 3x3); usa NumPy para dimensiones mayores |
| `IndexError` al indexar | SymPy usa `M[i, j]` (coma dentro del corchete), no `M[i][j]` | Reemplaza `M[i][j]` por `M[i, j]` |

## Notas relacionadas

- [[Matrix.det]]
- [[Matrix.inv]]
- [[Matrix.rref]]
- [[Matrix.eigenvals]]
- [[Matrix.eigenvects]]
- [[Matrix.nullspace]]
- [[concepto_expr_arbol]]
- [[sympy.matrices/index | sympy.matrices]]
