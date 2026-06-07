---
title: np/operaciones/exponenciales_log — funciones exponenciales, logaritmicas y de potencia (ufuncs)
tags:
  - numpy
  - indice
draft: false
---

# np/operaciones/exponenciales_log — funciones exponenciales, logaritmicas y de potencia (ufuncs)

Las 7 [[concepto_ufuncs|ufuncs]] exponenciales, logaritmicas y de potencia de NumPy. Operan **elemento a elemento** y soportan [[concepto_broadcasting|broadcasting]] completo.

## Tabla de funciones

| Grupo | ufunc | Formula | Nota |
|---|---|---|---|
| **Exponenciales** | [[np.exp]] | e^x | exponencial natural |
| | [[np.expm1]] | e^x - 1 | numericamente estable para x cercano a 0 |
| **Logaritmos** | [[np.log]] | ln(x) | logaritmo natural (base e) |
| | [[np.log2]] | log2(x) | logaritmo en base 2 |
| | [[np.log10]] | log10(x) | logaritmo en base 10 |
| **Potencias** | [[np.sqrt]] | sqrt(x) | raiz cuadrada (x >= 0) |
| | [[np.square]] | x^2 | cuadrado elemento a elemento |

## Uso basico

```python
import numpy as np

x = np.array([0.0, 1.0, 2.0, 3.0])

np.exp(x)     # [1.    2.718  7.389  20.086]
np.log(x[1:]) # [0.    0.693  1.099]   — x=0 da -inf
np.sqrt(x)    # [0.    1.     1.414   1.732]
np.square(x)  # [0.    1.     4.      9.   ]
```

### Logaritmos en distintas bases

```python
x = np.array([1, 2, 8, 10, 100])

np.log(x)    # logaritmo natural
np.log2(x)   # [0.  1.  3.  3.322  6.644]
np.log10(x)  # [0.  0.301  0.903  1.  2.]
```

## Estabilidad numerica: `expm1` y `log1p`

> [!tip] Usar `expm1` para x cercano a 0
> `np.exp(x) - 1` pierde digitos significativos cuando x es muy pequeno (cancelacion catastrofica). `np.expm1(x)` calcula `e^x - 1` directamente con precision completa.

```python
x = 1e-10

# Calculo ingenuo: pierde precision
np.exp(x) - 1       # 1.000000082740371e-10  (impreciso)

# Calculo estable
np.expm1(x)         # 1.00000000005e-10      (correcto)
```

Caso tipico: probabilidades, tasas de interes continuas, funciones de activacion.

## Broadcasting

```python
M = np.arange(1, 13, dtype=float).reshape(3, 4)

np.log(M)      # log de cada elemento → shape (3, 4)
np.sqrt(M)     # raiz de cada elemento → shape (3, 4)
np.exp(M / M.max())   # normalizacion antes de exp
```

## Notas de este grupo

- [[np.exp]]
- [[np.expm1]]
- [[np.log]]
- [[np.log2]]
- [[np.log10]]
- [[np.sqrt]]
- [[np.square]]

## Notas relacionadas

- [[concepto_ufuncs]]
- [[concepto_broadcasting]]
- [[Librerias/Numpy/np/operaciones/index|np/operaciones — ufuncs element-wise]]
