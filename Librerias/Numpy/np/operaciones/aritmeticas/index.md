---
title: np/operaciones/aritmeticas — operaciones aritmeticas basicas (ufuncs)
tags:
  - numpy
  - indice
draft: false
---

# np/operaciones/aritmeticas — operaciones aritmeticas basicas (ufuncs)

Las 6 operaciones aritmeticas fundamentales como [[concepto_ufuncs|ufuncs]]. Son los equivalentes funcionales de los operadores `+ - * / ** %`, con una ventaja clave: exponen `out=` para reusar buffers (critico en bucles de animacion o calculo iterativo), `where=` para aplicacion condicional, y `casting=` para control de tipos. En codigo normal se usan los operadores; las ufuncs aparecen cuando se necesitan esos parametros extra.

## Funciones de este grupo

| Operador | ufunc | Descripcion |
|---|---|---|
| `a + b` | [[np.add]] | suma elemento a elemento; con `out=resultado` escribe directamente en el array de salida sin crear uno nuevo |
| `a - b` | [[np.subtract]] | resta elemento a elemento |
| `a * b` | [[np.multiply]] | multiplicacion elemento a elemento — **no** producto matricial; para eso usar `@` o `np.matmul` |
| `a / b` | [[np.divide]] | division real, siempre devuelve float; para division entera usar `np.floor_divide` o `//` |
| `a ** b` | [[np.power]] | potencia elemento a elemento; `x2` puede ser un array (cada elemento elevado a su propio exponente) |
| `a % b` | [[np.mod]] | modulo (resto de la division); el signo del resultado sigue el signo del divisor — comportamiento de Python, diferente a C |

## Notas relacionadas

- [[concepto_ufuncs]]
- [[concepto_broadcasting]]
- [[Librerias/Numpy/np/operaciones/index\|np/operaciones — ufuncs element-wise]]
