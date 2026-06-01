---
title: np.poly1d — Objeto polinomio 1D
aliases:
  - poly1d
  - np.poly1d
tags:
  - numpy
  - api/clase
  - polinomios

# --- Clasificación ---
lib: numpy
mod: np
tipo: clase

# --- Comportamiento ---
retorna: poly1d
inplace: false

# --- Dependencias ---
requiere:
  - concepto_shape

draft: false
---

# np.poly1d — Objeto polinomio 1D

## Firma de la función

```python
np.poly1d(
    c_or_r,
    r=False,
    variable=None
)
```

## Valor de retorno

Crea un **objeto polinomio** que envuelve unos coeficientes y permite evaluar, derivar, integrar y operar con sintaxis algebraica natural. Es la forma orientada a objetos de los polinomios clásicos.

```python
import numpy as np
p = np.poly1d([1, 2, 3])     # x² + 2x + 3
p(0)                         # 3   → es callable (evalúa)
print(p)
#    2
# 1 x + 2 x + 3
```

## Operaciones algebraicas

El objeto soporta operadores como si fuera un polinomio simbólico:

```python
p = np.poly1d([1, 2, 3])
q = np.poly1d([1, 0])        # x

p + q          # suma de polinomios
p * q          # producto
p.deriv()      # derivada (x² + 2x + 3 → 2x + 2)
p.integ()      # integral
p.r            # raíces
p.c            # coeficientes
```

## Crear desde raíces

Con `r=True`, los argumentos son las **raíces**, no los coeficientes:

```python
np.poly1d([1, 2], r=True)    # (x-1)(x-2) = x² - 3x + 2
```

## Atributos y métodos clave

| Miembro | Devuelve |
|---------|----------|
| `p(x)` | evalúa (como [[np.polyval]]) |
| `p.c` / `p.coeffs` | coeficientes |
| `p.r` / `p.roots` | raíces (como [[np.roots]]) |
| `p.deriv(m)` | derivada (como [[np.polyder]]) |
| `p.integ(m)` | integral (como [[np.polyint]]) |
| `p.order` | grado |

## Casos de uso

### Trabajar con un ajuste como objeto

```python
p = np.poly1d(np.polyfit(x, y, 2))
y_pred = p(x_nuevo)          # evaluar
pendiente = p.deriv()        # derivada como otro poly1d
```

## Buenas prácticas

1. Es **callable**: `p(x)` evita llamar a [[np.polyval]] explícitamente.
2. Encadena: `np.poly1d(np.polyfit(...))` da un objeto manipulable.
3. Para trabajo serio, la API moderna `np.polynomial.Polynomial` es más robusta.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Interpretar coeficientes como raíces | olvidar `r=True` | indicar `r=True` si pasas raíces |

## Limitaciones

- API antigua; `np.polynomial.Polynomial` es la recomendada actualmente.

## Notas relacionadas

- [[concepto_shape]]
- [[np.polyfit]]
- [[np.polyval]]
- [[np.roots]]
- [[np.polyder]]
- [[np.polyint]]
