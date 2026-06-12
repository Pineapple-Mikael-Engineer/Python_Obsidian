---
title: sympy.matrices/creacion — constructores especializados
tags:
  - sympy
  - indice
draft: false
---

# creacion

Esta carpeta agrupa los **constructores especializados** de matrices simbolicas de SymPy: funciones que producen matrices especiales sin necesidad de escribir listas de listas manualmente. Las cuatro funciones — `eye`, `zeros`, `ones` y `diag` — cubren los patrones de inicializacion mas frecuentes en algebra lineal simbolica: la identidad, matrices uniformes (todo ceros o todo unos) y la estructura diagonal o de bloques. Son el punto de partida para cualquier manipulacion matricial en SymPy; la alternativa sin ellas seria escribir `Matrix([[1,0,0],[0,1,0],[0,0,1]])` cada vez, lo cual es fragil y no escala.

El ejemplo siguiente muestra como las cuatro funciones se combinan para construir una **matriz de bloques** tipica de un sistema de control:

```python
from sympy import eye, zeros, ones, diag, symbols

# Bloque de integradores 2x2
A = eye(2)             # Matrix([[1, 0], [0, 1]])

# Bloque de amortiguamiento 2x2
B = zeros(2)           # Matrix([[0, 0], [0, 0]])
B[0, 1] = -1           # Matrix([[0, -1], [0, 0]])

# Escalar de ganancia 1x1
k = symbols("k", positive=True)

# Ensamblar como sistema por bloques
M = diag(A, k)         # Matrix([[1, 0, 0], [0, 1, 0], [0, 0, k]])

# Vector de excitacion uniforme
e = ones(3, 1)         # Matrix([[1], [1], [1]])
M * e                  # Matrix([[1], [1], [k]])
```

## Como se relacionan

La decision clave: **que patron de valores** necesitas en la nueva matriz.

| Funcion | Patron | Dimension | Cuando usarla |
|---------|--------|-----------|---------------|
| [[sympy.eye]] | 1 en diagonal, 0 fuera | n×n o n×m | Identidad, termino neutro del producto, base de modificacion |
| [[sympy.zeros]] | Todo 0 | r×c | Inicializar y rellenar elemento a elemento, acumular sumas |
| [[sympy.ones]] | Todo 1 | r×c | Vectores de suma, escalar uniformemente, molde de constante |
| [[sympy.diag]] | Bloques en diagonal | n×n (suma de bloques) | Matrices diagonales simbolicas, sistemas por bloques, forma de Jordan |

Arbol de decision:

- ¿Necesitas el **elemento neutro del producto** matricial? -> [[sympy.eye]].
- ¿Quieres una **base vacia** para rellenar posicion a posicion? -> [[sympy.zeros]].
- ¿Todos los valores son **iguales a 1** (o la escalaras luego)? -> [[sympy.ones]].
- ¿Los valores de interes estan **solo en la diagonal** o quieres montar **bloques**? -> [[sympy.diag]].

> [!info] diag engloba a eye
> `diag(1, 1, 1)` y `eye(3)` producen la misma matriz. La diferencia es semantica: usa `eye` cuando el significado es "identidad" y `diag` cuando construyes una diagonal de valores distintos o de bloques. `diag(eye(2), 3)` es el patron tipico de matrices de bloques que mezclan ambos.

## Notas

- [[sympy.eye]] — identidad n×n o n×m; 1s en la diagonal, 0s fuera. Punto de partida para `A - lambda*I` y matrices de transformacion.
- [[sympy.zeros]] — r×c de ceros exactos. Molde para construir matrices elemento a elemento o acumular sumas simbolicas.
- [[sympy.ones]] — r×c de unos exactos. Util para vectores de suma y escalados uniformes.
- [[sympy.diag]] — diagonal o bloques diagonales a partir de escalares y/o matrices; dimension final = suma de los tamanos de los bloques.

## Notas relacionadas

- [[sympy.matrices/index | sympy.matrices]]
