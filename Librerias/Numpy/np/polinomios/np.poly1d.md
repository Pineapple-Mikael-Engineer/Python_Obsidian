---
title: np.poly1d — clase que representa un polinomio por sus coeficientes
aliases:
  - poly1d
  - np.poly1d
tags:
  - numpy
  - api/clase
  - polinomios
lib: numpy
mod: np
tipo: clase
retorna: poly1d
inplace: false
requiere:
  - concepto_shape
draft: false
---

# np.poly1d — clase que representa un polinomio por sus coeficientes

`np.poly1d` es la **clase** que envuelve un array de coeficientes y lo convierte en un objeto que se comporta como un polinomio: es **callable** (se evalúa con `p(x)`), soporta los operadores algebraicos (`+`, `-`, `*`, `**`, `//`) entre polinomios, y expone su derivada, su integral y sus raíces como métodos y atributos. Es el punto de entrada de la API legacy de polinomios; las demás funciones ([[np.polyval]], [[np.roots]], [[np.polyder]], [[np.polyint]]) aceptan tanto arrays de coeficientes crudos como objetos `poly1d`. La API moderna recomendada hoy es `np.polynomial.Polynomial`, pero `poly1d` sigue siendo omnipresente en código existente.

## La idea

Un `poly1d` guarda los coeficientes en orden **descendente** de potencias. Un array `c = [c_0, c_1, \dots, c_n]` representa el polinomio

$$
p(x) \;=\; c_0\,x^{n} + c_1\,x^{n-1} + \dots + c_{n-1}\,x + c_n \;=\; \sum_{i=0}^{n} c_i\,x^{\,n-i}
$$

Por ejemplo, `poly1d([1, -3, 2])` es

$$
p(x) = 1\cdot x^{2} - 3\cdot x + 2 = x^{2} - 3x + 2 = (x-1)(x-2)
$$

El objeto **no** evalúa nada al construirse: solo almacena el vector de coeficientes y ofrece operaciones simbólicas/numéricas sobre él.

## Firma

```python
np.poly1d(
    c_or_r,            # array_like: coeficientes (mayor→menor grado), o raíces si r=True
    r=False,           # bool: si True, c_or_r son las raíces, no los coeficientes
    variable=None,     # str: nombre de la variable al imprimir ('x' por defecto)
) -> poly1d
```

## Los parámetros en detalle

### `c_or_r` — coeficientes (o raíces)
`array_like` 1D. Por defecto son los **coeficientes** en orden descendente de potencias: `[1, -3, 2]` → $x^2 - 3x + 2$. Si `r=True`, se interpretan como las **raíces** y el polinomio se construye como $\prod_i (x - r_i)$.

```python
np.poly1d([1, -3, 2])              # x² - 3x + 2  (coeficientes)
np.poly1d([1, 2], r=True)          # (x-1)(x-2) = x² - 3x + 2  (raíces)
```

### `r` — interpretar como raíces
`bool` (defecto `False`). Conmuta la lectura de `c_or_r` entre coeficientes y raíces. Es el switch que más confunde: con `r=True` el grado del polinomio es igual al **número de raíces** que pasas.

### `variable` — símbolo al imprimir
`str` (defecto `'x'`). Solo afecta a la representación textual (`print(p)`), no al cálculo. Útil para imprimir en `t` o `s`.

```python
p = np.poly1d([1, 0, -1], variable='t')
print(p)
#    2
# 1 t - 1
```

### Atributos y métodos clave

| Miembro | Devuelve | Equivalente funcional |
|---------|----------|------------------------|
| `p(x)` | evalúa en `x` (callable) | [[np.polyval]] |
| `p.c` / `p.coeffs` | array de coeficientes | — |
| `p.r` / `p.roots` | array de raíces | [[np.roots]] |
| `p.order` | grado del polinomio (int) | — |
| `p.deriv(m=1)` | derivada como otro `poly1d` | [[np.polyder]] |
| `p.integ(m=1, k=0)` | integral como otro `poly1d` | [[np.polyint]] |

## Casos de uso

### Construir y evaluar
```python
import numpy as np
p = np.poly1d([1, -3, 2])    # x² - 3x + 2
p(0)                         # 2     → es callable
p(1)                         # 0     → x=1 es raíz
p([0, 1, 2])                 # array([2, 0, 0])  → vectorizado
```

### Álgebra de polinomios con operadores
```python
p = np.poly1d([1, -3, 2])    # x² - 3x + 2
q = np.poly1d([1, 0])        # x

(p + q)                      # x² - 2x + 2
(p * q)                      # x³ - 3x² + 2x
p.deriv()                    # 2x - 3   (derivada)
p.integ()                    # (1/3)x³ - (3/2)x² + 2x
```

### Atributos: raíces, coeficientes, grado
```python
p = np.poly1d([1, -3, 2])
p.r        # array([2., 1.])   → raíces
p.c        # array([ 1, -3,  2])
p.order    # 2
```

### Encadenar con un ajuste
```python
p = np.poly1d(np.polyfit(x, y, 2))   # objeto a partir de un ajuste
y_pred = p(x_nuevo)                  # evaluar directamente
pendiente = p.deriv()                # derivada como otro poly1d
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Coeficientes interpretados como raíces (o al revés) | olvidar/sobrar `r=True` | usar `r=True` solo si pasas raíces |
| Orden de potencias invertido | asumir orden ascendente | la convención es **descendente**: `[a, b, c]` = $ax^2+bx+c$ |
| `p[i]` no da lo esperado | el indexado devuelve el coef. de **grado** `i`, no la posición | usar `p.c` para el array en orden descendente |
| Inestabilidad numérica con grados altos | base de potencias mal condicionada | usar `np.polynomial.Polynomial` (API moderna) |

## Notas relacionadas

- [[concepto_shape]] — el array 1D de coeficientes
- [[np.polyval]] — evaluar (lo que hace `p(x)` por dentro)
- [[np.roots]] — las raíces (`p.r`)
- [[np.polyder]] · [[np.polyint]] — derivada e integral (`p.deriv` / `p.integ`)
- [[np.polyfit]] — ajustar y envolver el resultado en un `poly1d`
- [[index]] — API legacy de polinomios
