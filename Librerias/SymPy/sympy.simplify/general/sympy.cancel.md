---
title: sympy.cancel — cancelar factores comunes de una expresion racional
aliases:
  - cancel
  - sympy.cancel
  - cancelar factores comunes
tags:
  - sympy
  - api/funcion
  - simplify/general
lib: sympy
mod: sympy
tipo: funcion
retorna: Expr
requiere:
  - Symbol
draft: false
---

# sympy.cancel — cancelar factores comunes de una expresion racional

`cancel(expr)` toma una **expresion racional** (un cociente de polinomios) y **cancela los factores comunes** entre numerador y denominador, devolviendola en la forma canonica `p/q` con `p` y `q` polinomios sin factor comun: `cancel((x**2 - 1)/(x - 1))` -> `x + 1`. A diferencia de [[sympy.simplify]], es una operacion **especifica y predecible**: hace exactamente una cosa (poner la fraccion como `p/q` reducida) y siempre da la **misma** forma para la misma entrada, sin probar caminos ni adivinar. Es rapida y la eleccion correcta cuando lo que quieres es "limpiar" un cociente; reserva `simplify` para cuando no sabes que necesitas.

> `cancel` es la version **canonica y rapida** de simplificar fracciones: pone todo sobre comun denominador, factoriza y cancela, y deja un unico `p/q` reducido. Donde `factor` muestra la estructura en producto, `cancel` solo elimina lo comun y reduce.

## Firma

```python
sympy.cancel(
    f,                   # Expr: la expresion racional a reducir
    *gens,               # Symbol(s): generadores/variables (opcional, se deducen)
    extension=None,      # numero algebraico: cuerpo sobre el que cancelar
) -> Expr
```

## Valor de retorno

| Tipo | Forma | Significado |
|------|-------|-------------|
| `Expr` | `p/q` reducido | El cociente en forma canonica, sin factor comun entre numerador y denominador |

Si no hay factor comun, devuelve la expresion (reescrita como un solo cociente) sin cancelar nada.

```python
from sympy import symbols, cancel
x = symbols("x")
cancel((x**2 - 1)/(x - 1))   # x + 1
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Cancelar el factor comun | `cancel((x**2 - 1)/(x - 1))` |
| Reducir un cociente cualquiera | `cancel((x**2 + 2*x + 1)/(x**2 + x))` |
| Unir sumas de fracciones en `p/q` | `cancel(1/x + 1/(x + 1))` |
| Multivariante | `cancel((x**2*y + x*y)/(x*y))` |

## Parametros en detalle

### `f` (obligatorio)

La expresion racional a reducir. `cancel` la lleva a `p/q`, factoriza implicitamente y cancela lo comun.

```python
from sympy import symbols, cancel
x, y = symbols("x y")
cancel((x**2 - 1)/(x - 1))            # x + 1
cancel((x**2 + 2*x + 1)/(x**2 + x))   # (x + 1)/x
cancel((x**2 - y**2)/(x - y))         # x + y
```

Tambien combina y reduce una **suma** de fracciones a un unico cociente canonico:

```python
from sympy import symbols, cancel
x = symbols("x")
cancel(1/x + 1/(x + 1))   # (2*x + 1)/(x**2 + x)
```

### `extension`

Por defecto cancela sobre los racionales **Q**. Con `extension` (p. ej. `sqrt(2)`) cancela sobre la extension algebraica, permitiendo eliminar factores que sobre Q son irreducibles.

## Casos de uso

### Eliminar una singularidad removible

Cuando numerador y denominador comparten una raiz, `cancel` quita el factor y revela el valor "verdadero" de la expresion.

```python
from sympy import symbols, cancel
x = symbols("x")
# (x**2 - 1)/(x - 1) tiene un hueco en x=1; al cancelar queda x + 1
cancel((x**2 - 1)/(x - 1))   # x + 1
```

### Reducir antes de derivar o integrar

Una fraccion ya reducida es mas barata de derivar/integrar y evita arrastrar factores comunes innecesarios.

```python
from sympy import symbols, cancel
x = symbols("x")
cancel((x**3 - x)/(x**2 - 1))   # x
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Esperar la forma factorizada en producto | `cancel` deja `p/q` expandido, no en factores | Usar `factor` si quieres ver los factores |
| Usar `simplify` para esto | `simplify` es lento y no canonico | `cancel` es especifico, rapido y predecible |
| No cancela radicales sobre Q | Por defecto cancela sobre los racionales | Pasar `extension=sqrt(2)` (o el numero algebraico) |
| Esperar fracciones parciales | `cancel` reune en un cociente, no separa | Usar `apart` para descomponer en parciales |
| Olvidar que reune sumas en un solo `p/q` | `cancel` pone todo sobre comun denominador | Si solo quieres unir, considera `together` |

## Limitaciones

- Opera solo sobre **expresiones racionales** (cocientes de polinomios); no toca funciones trascendentes salvo el cociente externo.
- Devuelve la forma `p/q` **expandida**, no factorizada: para ver factores usa `factor`; para separar en parciales, `apart`.
- Cancela sobre Q salvo que indiques `extension`.

## Notas relacionadas

- [[sympy.simplify]]
- [[sympy.factor]]
- [[sympy.apart]]
- [[sympy.simplify/general/index | general]]
