---
title: sympy.together — combinar una suma de fracciones en una sola
aliases:
  - together
  - sympy.together
  - comun denominador
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

# sympy.together — combinar una suma de fracciones en una sola

`together(expr)` combina una **suma de fracciones** en una **unica fraccion** con denominador comun: convierte `1/x + 1/y` en `(x + y)/(x*y)`. Reune los sumandos sobre un denominador comun sin desarrollar ni cancelar mas alla de lo necesario. Es la operacion **inversa** de [[sympy.apart]] (que separa una fraccion en parciales) y la forma de dejar una expresion racional como un solo cociente, paso previo habitual para simplificar o factorizar numerador y denominador.

> `together` **une** fracciones en una sola y `apart` la **vuelve a separar** en parciales: son inversas. `together(apart(f))` recupera la fraccion original.

## Firma

```python
sympy.together(
    expr,                # Expr: suma de fracciones a combinar
    deep=False,          # bool: aplicar tambien dentro de subexpresiones/funciones
    fraction=True,       # bool: mantener el resultado como cociente unico
    ...
) -> Expr
```

## Valor de retorno

| Tipo | Forma | Significado |
|------|-------|-------------|
| `Expr` | una sola fraccion | La suma reunida sobre un denominador comun (`num/den`) |

No cancela factores comunes por su cuenta: para eso estan [[sympy.cancel]] o [[sympy.simplify]].

```python
from sympy import symbols, together
x, y = symbols("x y")
together(1/x + 1/y)       # (x + y)/(x*y)
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Combinar suma de fracciones | `together(1/x + 1/y)` |
| Comun denominador con polinomios | `together(1/(x - 1) + 1/(x + 1))` |
| Aplicar dentro de subexpresiones | `together(expr, deep=True)` |

## Parametros en detalle

### `expr` (obligatorio)

La suma de fracciones a reunir. SymPy calcula el denominador comun y suma los numeradores correspondientes.

```python
from sympy import symbols, together
x, y = symbols("x y")
together(1/x + 1/y)              # (x + y)/(x*y)
together(1/(x - 1) + 1/(x + 1))  # 2*x/((x - 1)*(x + 1))
```

### `deep`

Con `deep=True`, aplica la combinacion tambien a las fracciones que aparezcan **dentro** de subexpresiones (p. ej. en el argumento de una funcion), no solo en el nivel superior.

### `fraction`

Controla si el resultado se mantiene como un **unico cociente** `num/den`. Con `fraction=False` puede dejar la expresion menos compactada en ciertos casos; por defecto reune todo en una sola fraccion.

## Casos de uso

### Reunir antes de simplificar o factorizar

Para simplificar una suma de fracciones conviene primero unirlas en un cociente y luego cancelar/factorizar numerador y denominador.

```python
from sympy import symbols, together, cancel
x = symbols("x")
together(1/(x - 1) - 1/(x + 1))   # ((x - 1) - (x + 1))/((x - 1)*(x + 1)) reunido
# -> 2/((x - 1)*(x + 1)) tras simplificar el numerador
```

### Verificar que apart y together son inversas

Tras descomponer en parciales, `together` reconstruye la fraccion original.

```python
from sympy import symbols, apart, together
x = symbols("x")
f = 1/(x**2 - 1)
together(apart(f))                # 1/((x - 1)*(x + 1))   -> equivale a f
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Esperar que cancele factores comunes | `together` solo reune, no simplifica del todo | Encadenar con [[sympy.cancel]] o [[sympy.simplify]] |
| Esperar fracciones separadas | `together` combina, no descompone | Usar [[sympy.apart]] para el camino inverso |
| El resultado no se ve mas simple | El denominador comun no siempre acorta la expresion | Aplicar `factor` al numerador/denominador o `simplify` |
| No actua dentro de una funcion | Por defecto solo el nivel superior | Pasar `deep=True` |

## Notas relacionadas

- [[sympy.apart]]
- [[sympy.cancel]]
- [[sympy.factor]]
- [[sympy.polys/expandir_factorizar/index | expandir_factorizar]]
