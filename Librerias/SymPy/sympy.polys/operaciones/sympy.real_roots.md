---
title: sympy.real_roots — raices reales exactas de un polinomio
aliases:
  - real_roots
  - sympy.real_roots
  - raices reales exactas
tags:
  - sympy
  - api/funcion
  - polys/operaciones
lib: sympy
mod: sympy.polys
tipo: funcion
retorna: list
draft: false
---

# sympy.real_roots — raices reales exactas de un polinomio

`real_roots(p)` devuelve **todas las raices reales exactas** de un polinomio univariable con coeficientes racionales, **de cualquier grado**, repetidas segun su multiplicidad y ordenadas de menor a mayor. Aisla solo las raices reales (descarta las complejas), lo que la hace mas eficiente que pedir todas y filtrar. A diferencia de [[sympy.roots]] y [[sympy.solve]], garantiza resultados **exactos y realmente reales** incluso para grados altos sin formula radical: en ese caso representa la raiz como un `CRootOf` (raiz numerada exacta), evaluable a la precision que se quiera con `evalf`.

> Diferencia clave con `roots`/`solve`: `roots` usa formulas para cubicas/cuarticas que pueden devolver expresiones con `I` aunque la raiz sea real (casus irreducibilis); `real_roots` siempre da expresiones que evaluan a reales puros y aisla exactamente las reales. Frente a un calculo **numerico** como `nroots`/[[sympy.nsolve]], `real_roots` es **exacto**: el `CRootOf` es la raiz verdadera, no una aproximacion.

## Firma

```python
sympy.real_roots(
    f,                 # Expr | Poly: polinomio univariable con coef. racionales
    multiple=True,     # bool: True -> lista plana; False -> pares (raiz, multiplicidad)
    radicals=True,     # bool: usar radicales simples en vez de CRootOf cuando sea posible
    extension=False,   # bool: construir extension algebraica (coef. irracionales)
) -> list
```

> Cuidado: el **segundo argumento posicional es `multiple`**, no la variable. `real_roots` infiere la variable; no se le pasa un generador como a `degree` o `roots`.

## Valor de retorno

| Caso | Tipo | Significado |
|------|------|-------------|
| Por defecto (`multiple=True`) | `list` | Raices reales repetidas por multiplicidad, en orden creciente |
| `multiple=False` | `list` | Lista de pares `(raiz, multiplicidad)` |
| Sin raices reales | `list` | `[]` (lista vacia) |

```python
from sympy import symbols, real_roots
x = symbols("x")
real_roots(x**2 - 2)      # [-sqrt(2), sqrt(2)]   -> exactas, con radicales
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Raices reales (lista plana) | `real_roots(p)` |
| Con multiplicidad explicita | `real_roots(p, multiple=False)` |
| Forzar `CRootOf` (sin radicales) | `real_roots(p, radicals=False)` |

## Parametros en detalle

### `f` (el polinomio)

Polinomio univariable de coeficientes racionales. Las raices racionales salen como numeros, las simples como radicales, y el resto como `CRootOf`.

```python
from sympy import symbols, real_roots
x = symbols("x")
real_roots(x**3 - x)      # [-1, 0, 1]            -> tres raices racionales
real_roots(x**2 + 1)      # []                    -> ninguna raiz real
```

### Multiplicidad (raices repetidas)

Por defecto la raiz repetida aparece varias veces; con `multiple=False` se obtiene el par `(raiz, multiplicidad)`.

```python
from sympy import symbols, real_roots
x = symbols("x")
real_roots((x - 1)**2 * (x - 2))                 # [1, 1, 2]
real_roots((x - 1)**2 * (x - 2), multiple=False) # [(1, 2), (2, 1)]
```

### Grado alto sin radicales: `CRootOf`

Para quinticas y mas, cuando no hay formula cerrada, la raiz se representa exacta como `CRootOf` (raiz numerada del polinomio), evaluable con `evalf`.

```python
from sympy import symbols, real_roots
x = symbols("x")
real_roots(x**5 - x - 1)                 # [CRootOf(x**5 - x - 1, 0)]
[r.evalf(4) for r in real_roots(x**5 - x - 1)]   # [1.167]
```

## Casos de uso

### Solo las raices reales, descartando las complejas

```python
from sympy import symbols, real_roots, roots
x = symbols("x")
p = x**4 - 1
real_roots(p)     # [-1, 1]                    -> solo reales
roots(p)          # {-1: 1, 1: 1, -I: 1, I: 1} -> incluye complejas
```

### Polos reales de un sistema (control)

```python
from sympy import symbols, real_roots
s = symbols("s")
# polinomio caracteristico: raiz doble real en s = -1
real_roots(s**2 + 2*s + 1, multiple=False)   # [(-1, 2)]   -> polo doble real
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Pasar la variable como 2.º argumento | El 2.º posicional es `multiple`, no el generador | Llamar `real_roots(p)`; no pasar `x` |
| Esperar las raices complejas | `real_roots` aisla solo las reales | Usar [[sympy.roots]] o `all_roots` para las complejas |
| Sorprenderse por `CRootOf` | Grado alto sin formula radical | Es exacto; usar `.evalf(n)` para el valor numerico |
| Coeficientes irracionales fallan | Por defecto exige racionales | Pasar `extension=True` (mas lento) |

## Limitaciones

- Solo polinomios **univariables** con coeficientes racionales (o `Float`); para irracionales, `extension=True`.
- Da exactitud, no un numero: para aproximaciones directas estan `nroots` y [[sympy.nsolve]].
- Las raices complejas quedan fuera; usar [[sympy.roots]] o `all_roots` si se necesitan.

## Notas relacionadas

- [[sympy.roots]]
- [[sympy.degree]]
- [[sympy.nsolve]]
- [[sympy.polys/operaciones/index | operaciones]]
