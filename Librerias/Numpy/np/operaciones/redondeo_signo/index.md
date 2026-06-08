---
title: np/operaciones/redondeo_signo — valor absoluto, signo y redondeo (ufuncs)
tags:
  - numpy
  - indice
draft: false
---

# np/operaciones/redondeo_signo — valor absoluto, signo y redondeo (ufuncs)

Las 4 [[concepto_ufuncs|ufuncs]] de valor absoluto, signo y redondeo de NumPy. Son las mas "basicas" del grupo de operaciones pero aparecen constantemente en calculo numerico, normalizacion y deteccion de signos.

## Funciones de este grupo

| ufunc | Descripcion |
|---|---|
| [[np.abs]] | valor absoluto elemento a elemento; alias de `np.absolute`; soporta numeros complejos (devuelve la magnitud `sqrt(re^2 + im^2)`); es la version que se usa siempre |
| [[np.fabs]] | valor absoluto para flotantes; mas rapido que `abs` en algunos casos pero **no soporta complejos ni enteros**; usar `np.abs` en la mayoria de casos |
| [[np.sign]] | devuelve -1, 0 o 1 segun el signo de cada elemento; para complejos devuelve el vector unitario en la misma direccion |
| [[np.ceil]] | redondeo hacia arriba (hacia +inf); para redondeo hacia abajo: `np.floor`; hacia cero: `np.trunc`; al entero mas cercano: `np.round` o `np.rint` |

## Notas relacionadas

- [[concepto_ufuncs]]
- [[concepto_broadcasting]]
- [[Librerias/Numpy/np/operaciones/index\|np/operaciones — ufuncs element-wise]]
