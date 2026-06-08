---
title: sympy.factor — factorizar un polinomio en producto de factores irreducibles
aliases:
  - factor
  - sympy.factor
  - factorizar
tags:
  - sympy
  - api/funcion
  - polys/expandir_factorizar
lib: sympy
mod: sympy
tipo: funcion
retorna: Expr
requiere:
  - Symbol
draft: false
---

# sympy.factor — factorizar un polinomio en producto de factores irreducibles

`factor(expr)` reescribe un polinomio como **producto de factores irreducibles** sobre los racionales: convierte `x**2 - 1` en `(x - 1)*(x + 1)`. Es la operacion **inversa** de [[sympy.expand]] y la forma de revelar raices, simplificar fracciones racionales o identificar la estructura de una expresion. Por defecto factoriza sobre **Q** (coeficientes racionales); con `extension` puede factorizar sobre extensiones algebraicas (p. ej. añadiendo `sqrt(2)`) y separar factores que sobre los racionales son irreducibles.

> `factor` y `expand` son **inversas**: `factor(x**2 - 1)` da `(x - 1)*(x + 1)`, y `expand((x - 1)*(x + 1))` devuelve `x**2 - 1`. Una factoriza, la otra desarrolla.

## Firma

```python
sympy.factor(
    f,                   # Expr: polinomio (o expresion racional) a factorizar
    *gens,               # Symbol(s): generadores/variables (opcional, se deducen)
    deep=False,          # bool: factorizar tambien dentro de argumentos de funciones
    extension=None,      # numero algebraico: extiende el cuerpo (p. ej. sqrt(2))
    ...
) -> Expr
```

## Valor de retorno

| Tipo | Forma | Significado |
|------|-------|-------------|
| `Expr` | producto de factores | El polinomio como producto de irreducibles sobre Q (o la extension dada) |

Si el polinomio ya es **irreducible** sobre Q, lo devuelve sin cambios.

```python
from sympy import symbols, factor
x = symbols("x")
factor(x**2 - 1)          # (x - 1)*(x + 1)
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Factorizar sobre Q | `factor(x**2 - 1)` |
| Factorizar un cubico | `factor(x**3 - 1)` |
| Factorizar multivariante | `factor(x**2*y + x*y)` |
| Factorizar sobre una extension | `factor(x**2 - 2, extension=sqrt(2))` |
| Reconocer cuadrado perfecto | `factor(x**2 + 2*x + 1)` |

## Parametros en detalle

### `f` (obligatorio)

El polinomio o expresion racional a factorizar. SymPy busca la descomposicion en irreducibles sobre los racionales.

```python
from sympy import symbols, factor
x = symbols("x")
factor(x**2 - 1)              # (x - 1)*(x + 1)        -> diferencia de cuadrados
factor(x**2 + 2*x + 1)        # (x + 1)**2             -> cuadrado perfecto
factor(x**3 - 1)              # (x - 1)*(x**2 + x + 1) -> el cuadratico es irreducible sobre Q
```

Con varias variables saca el factor comun:

```python
from sympy import symbols, factor
x, y = symbols("x y")
factor(x**2*y + x*y)          # x*y*(x + 1)
```

### `extension`

Por defecto se factoriza sobre **Q**, donde `x**2 - 2` es irreducible. Pasando `extension=sqrt(2)` se factoriza sobre `Q(sqrt(2))` y aparecen los factores con radicales.

```python
from sympy import symbols, factor, sqrt
x = symbols("x")
factor(x**2 - 2)                       # x**2 - 2                  -> irreducible sobre Q
factor(x**2 - 2, extension=sqrt(2))    # (x - sqrt(2))*(x + sqrt(2))
```

### `deep`

Con `deep=True`, factoriza tambien las expresiones que aparezcan **dentro** de argumentos de funciones (p. ej. el interior de un `sin(...)`), no solo el polinomio externo.

## Casos de uso

### Simplificar una fraccion racional

Factorizar numerador y denominador revela el factor comun que se cancela.

```python
from sympy import symbols, factor
x = symbols("x")
factor(x**2 - 1)              # (x - 1)*(x + 1)
# (x**2 - 1)/(x - 1) -> (x + 1) tras cancelar (x - 1)
```

### Revelar las raices de un polinomio

Cada factor lineal `(x - r)` expone una raiz `r` directamente.

```python
from sympy import symbols, factor
x = symbols("x")
factor(x**3 - 6*x**2 + 11*x - 6)   # (x - 3)*(x - 2)*(x - 1)
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Esperar factores con radicales sobre Q | Por defecto factoriza sobre los racionales | Pasar `extension=sqrt(2)` (o el numero algebraico) |
| `factor` deja el polinomio igual | Es irreducible sobre Q | Probar con `extension` o factorizar sobre los complejos |
| Confundir con desarrollar | `factor` agrupa, no distribuye | Usar [[sympy.expand]] para el camino inverso |
| Resultado no simplificado en fracciones | `factor` no cancela por si solo terminos sumados | Combinar con [[sympy.cancel]] o [[sympy.together]] |

## Notas relacionadas

- [[sympy.expand]]
- [[sympy.collect]]
- [[sympy.apart]]
- [[sympy.polys/expandir_factorizar/index | expandir_factorizar]]
