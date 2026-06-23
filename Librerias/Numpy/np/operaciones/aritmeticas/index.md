---
title: np/operaciones/aritmeticas — operaciones aritméticas elemento a elemento (ufuncs)
tags:
  - numpy
  - indice
draft: false
---

# np/operaciones/aritmeticas — operaciones aritméticas elemento a elemento (ufuncs)

Esta carpeta agrupa las **operaciones aritméticas elemento a elemento** de NumPy y los **operadores**
que las respaldan. Cada operador (`+ - * / // % **`) es azúcar sintáctico sobre una
[[concepto_ufuncs|ufunc]]: `a + b` invoca `np.add(a, b)`, `a // b` invoca `np.floor_divide(a, b)`,
etc. Se usan los operadores en código normal; se baja a la ufunc cuando se necesitan sus parámetros
extra (`out=` para reusar buffers, `where=` para aplicación condicional, `casting=`/`dtype=` para
control de tipos).

## Operadores y sus ufuncs

| Operador | ufunc | Hace |
|---|---|---|
| `a + b` | [[np.add]] | suma elemento a elemento |
| `a - b` | [[np.subtract]] | resta elemento a elemento (`-` binario) |
| `-a` | [[np.negative]] | negación elemento a elemento (`-` unario) |
| `a * b` | [[np.multiply]] | producto **elemento a elemento** (Hadamard), no matricial |
| `a / b` | [[np.divide]] | división real, siempre devuelve float |
| `a // b` | [[np.floor_divide]] | división entera hacia abajo (suelo, hacia $-\infty$) |
| `a % b` | [[np.mod]] · [[np.remainder]] | resto con signo del divisor (`remainder` es el nombre canónico) |
| `a ** b` | [[np.power]] | potencia elemento a elemento |

## Cómo encajan entre sí

Todas estas operaciones alinean sus entradas por [[concepto_broadcasting|broadcasting]] (alineación
por la derecha) y son [[concepto_ufuncs|ufuncs]]: el bucle vive en C, no en Python. El par
cociente/resto (`//` y `%`) está ligado por la identidad de división euclídea:

$$ \texttt{a == (a//b)*b + a\%b} $$

donde [[np.floor_divide]] da el cociente y [[np.remainder]] (alias [[np.mod]]) da el resto. Para
obtener ambos en una sola pasada existe [[np.divmod]].

> [!warning] `*` (Hadamard) no es `@` (producto matricial)
> El operador `*` ([[np.multiply]]) multiplica **elemento a elemento**: requiere shapes broadcasteables
> y conserva la forma. El **producto matricial** es otra operación distinta, el operador `@`
> (`np.matmul`), que contrae el último eje de un array con el penúltimo del otro. Confundirlos es un
> error clásico: `A * B` no es `A @ B`.

## Notas relacionadas

- [[concepto_ufuncs]] — el motor element-wise de todas estas funciones
- [[concepto_broadcasting]] — cómo se alinean los operandos
- [[Librerias/Numpy/np/operaciones/index\|np/operaciones — ufuncs element-wise]]
