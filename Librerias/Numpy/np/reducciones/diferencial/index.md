---
title: np/reducciones/diferencial — calculo numerico discreto
tags:
  - numpy
  - indice
draft: false
---

# np/reducciones/diferencial — calculo numerico discreto

Las 3 funciones de esta subcarpeta son la interfaz entre el analisis matematico continuo y los datos discretos del mundo real: aproximan derivadas e integrales cuando no se tiene la funcion analitica, solo una tabla de valores muestreados.

La diferencia de comportamiento mas importante: `diff` y `trapz` cambian la longitud del resultado (`diff` la reduce en 1, `trapz` devuelve un escalar), mientras que `gradient` conserva el mismo shape que la entrada, lo que lo hace compatible con el resto de operaciones de NumPy sin necesidad de alinear indices.

```python
import numpy as np
x = np.array([0.0, 1.0, 2.0, 3.0])
y = x**2          # y = x^2; derivada analitica = 2x

np.diff(y)        # [1., 3., 5.]     — longitud n-1, aproximacion cruda
np.gradient(y, x) # [1., 2., 4., 6.] — mismo shape, diferencias centradas
np.trapz(y, x)    # 9.0              — escalar (integral numerica)
```

## Notas de esta subcarpeta

| Funcion | Que hace |
|---|---|
| [[np.diff]] | Diferencias finitas de primer orden: `a[i+1] - a[i]` para cada i. El resultado tiene un elemento menos que el input en el eje de operacion. Con `n=2` calcula diferencias de segundo orden (segunda derivada aproximada). Aproxima la derivada cuando los puntos estan equiespaciados. |
| [[np.gradient]] | Gradiente numerico con diferencias centradas: `(f[i+1] - f[i-1]) / (2*dx)` en puntos interiores, diferencias de un lado en los bordes. Es mas preciso que `diff` y conserva el shape del input, lo que lo hace mas comodo para vectorizar calculos. |
| [[np.trapz]] | Integral numerica por la regla del trapecio. Acepta `x` con puntos no uniformes (muestreo arbitrario). Para mayor precision o formulas de orden superior usar `scipy.integrate.quad` o `scipy.integrate.simpson`. |

> [!note] diff vs gradient
> [[np.diff]] es mas simple y rapido pero acorta el array; [[np.gradient]] conserva el shape y usa diferencias centradas, lo que da mayor precision en los puntos interiores. Elegir segun si se necesita mantener la longitud del array.
