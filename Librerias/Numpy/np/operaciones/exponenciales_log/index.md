---
title: np/operaciones/exponenciales_log — funciones exponenciales, logaritmicas y de potencia (ufuncs)
tags:
  - numpy
  - indice
draft: false
---

# np/operaciones/exponenciales_log — funciones exponenciales, logaritmicas y de potencia (ufuncs)

Las 7 [[concepto_ufuncs|ufuncs]] exponenciales, logaritmicas y de potencia de NumPy. Esenciales para calculo numerico, transformaciones de escala y estabilidad numerica. Varias tienen variantes "numericamente seguras" disenadas para valores cercanos a cero o extremadamente grandes, donde la formulacion ingenua pierde digitos significativos por cancelacion catastrofica.

## Funciones de este grupo

| Grupo | ufunc | Descripcion |
|---|---|---|
| **Exponenciales** | [[np.exp]] | exponencial e^x; para x > 709 en float64 da overflow a inf |
| | [[np.expm1]] | calcula e^x - 1 con mayor precision que `np.exp(x) - 1` cuando x es cercano a cero; critico en probabilidades y series de Taylor |
| **Logaritmos** | [[np.log]] | logaritmo natural (base e); `log(0)` da -inf con warning, `log` de negativos da nan |
| | [[np.log2]] | logaritmo en base 2; usado en teoria de la informacion y analisis de algoritmos |
| | [[np.log10]] | logaritmo en base 10; usado en escalas de magnitud (dB, pH, magnitud estelar) |
| **Potencias** | [[np.sqrt]] | raiz cuadrada; equivale a `x**0.5` pero mas rapido y semanticamente claro; devuelve float para arrays de enteros |
| | [[np.square]] | eleva al cuadrado elemento a elemento; equivale a `x**2` pero mas rapido para arrays grandes |

## Notas relacionadas

- [[concepto_ufuncs]]
- [[concepto_broadcasting]]
- [[Librerias/Numpy/np/operaciones/index\|np/operaciones — ufuncs element-wise]]
