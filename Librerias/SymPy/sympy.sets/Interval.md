---
title: Interval — intervalo real simbolico
aliases: [Interval, intervalo]
tags: [sympy, api/clase, sets]
lib: sympy
mod: sympy.sets
tipo: clase
retorna: Interval
requiere: [Symbol]
draft: false
---

# Interval — intervalo real simbolico

`Interval(a, b)` construye un **intervalo real simbolico** `[a, b]` como objeto de SymPy. A diferencia de una simple tupla, `Interval` conoce su tipo matematico (cerrado, abierto, semiabierto), calcula su medida y participa en operaciones de conjuntos (`union`, `intersect`, `Complement`). Es el tipo de retorno habitual de [[sympy.solveset]] cuando la solucion es un rango continuo, y se usa como argumento `domain` para acotar el espacio de busqueda.

## Firma

```python
sympy.Interval(
    a,                  # extremo izquierdo (Expr o numero)
    b,                  # extremo derecho (Expr o numero)
    left_open=False,    # True -> extremo izquierdo abierto (excluido)
    right_open=False,   # True -> extremo derecho abierto (excluido)
) -> Interval
```

Constructores de conveniencia (sin argumentos booleanos):

```python
Interval.open(a, b)    # (a, b)  — ambos extremos abiertos
Interval.Lopen(a, b)   # (a, b]  — izquierda abierta, derecha cerrada
Interval.Ropen(a, b)   # [a, b)  — izquierda cerrada, derecha abierta
```

## Valor de retorno

| Tipo | Forma | Significado |
|------|-------|-------------|
| `Interval` | `Interval(a, b)` | Intervalo cerrado `[a, b]` |
| `Interval` | `Interval.Ropen(a, b)` | Semiabierto `[a, b)` |
| `Interval` | `Interval.open(a, b)` | Abierto `(a, b)` |
| `EmptySet` | — | Si `a > b` o el intervalo es incoherente |

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Intervalo cerrado `[a, b]` | `Interval(a, b)` |
| Semiabierto `[a, b)` | `Interval(a, b, right_open=True)` o `Interval.Ropen(a, b)` |
| Semiabierto `(a, b]` | `Interval(a, b, left_open=True)` o `Interval.Lopen(a, b)` |
| Abierto `(a, b)` | `Interval.open(a, b)` |
| Longitud del intervalo | `Interval(a, b).measure` |
| Interseccion con otro | `Interval(a, b).intersect(Interval(c, d))` |

## Parametros en detalle

### `a`, `b` — extremos

Cualquier expresion SymPy o numero Python. SymPy los convierte a `Expr` internamente. Se admite `oo` (infinito positivo) y `-oo`.

```python
from sympy import Interval, oo
Interval(0, oo)           # [0, oo)  — semirrecta no negativa
Interval(-oo, oo)         # Reals    -> coincide con S.Reals
```

### `left_open`, `right_open` — apertura de extremos

```python
from sympy import Interval
Interval(0, 1)                          # Interval(0, 1)      -> [0, 1]
Interval(0, 1, right_open=True)         # Interval.Ropen(0, 1) -> [0, 1)
Interval(0, 1, left_open=True)          # Interval.Lopen(0, 1) -> (0, 1]
Interval(0, 1, left_open=True, right_open=True)  # Interval.open(0, 1) -> (0, 1)
```

### `.measure` — longitud (medida de Lebesgue)

```python
from sympy import Interval
Interval(0, 1).measure       # 1
Interval(0, 3).measure       # 3
Interval(0, oo).measure      # oo
```

## Casos de uso

### Pertenencia de un simbolo al intervalo

```python
from sympy import symbols, Interval
x = symbols("x")
x in Interval(0, 1)          # x in Interval(0, 1) -> expresion booleana, no True/False
Interval(0, 1).contains(x)   # (0 <= x) & (x <= 1)
Interval(0, 1).contains(0.5) # True
```

### Dominio en solveset

`solveset` con `domain=Interval(...)` restringe las soluciones al intervalo indicado.

```python
from sympy import symbols, solveset, Interval, sin, pi
x = symbols("x")
solveset(sin(x), x, domain=Interval(0, 2*pi))   # {0, pi, 2*pi}
```

### Operaciones entre intervalos

```python
from sympy import Interval
Interval(0, 3).intersect(Interval(2, 5))   # Interval(2, 3)
Interval(0, 1).union(Interval(2, 3))       # Union(Interval(0, 1), Interval(2, 3))
```

### Intervalo como resultado de solveset sobre inecuacion

```python
from sympy import symbols, solveset, S
x = symbols("x")
solveset(x**2 - 1 < 0, x, domain=S.Reals)  # Interval.open(-1, 1)
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `x in Interval(0, 1)` devuelve una expresion, no `True` | `x` es un `Symbol`; la pertenencia es simbolica | Usar `.contains(valor_numerico)` para evaluar en un punto concreto |
| `Interval(1, 0)` devuelve `EmptySet` | El extremo izquierdo supera al derecho | Verificar orden de los argumentos |
| Confundir `right_open` con `left_open` | Los nombres son simetricos pero se olvidan | Usar los constructores `.open`, `.Ropen`, `.Lopen` que son mas legibles |
| Esperar `float` en `.measure` | SymPy devuelve `Expr` exacta | Usar `.measure.evalf()` si se necesita valor flotante |

## Limitaciones

- `Interval` solo representa intervalos de la **recta real**; para conjuntos multidimensionales se usa `ProductSet`.
- La pertenencia de un `Symbol` devuelve una expresion booleana, no un valor de verdad; hay que evaluar con numeros concretos o razonar sobre la expresion.

## Notas relacionadas

- [[FiniteSet]]
- [[sympy.conjuntos_predefinidos]]
- [[sympy.operaciones_conjuntos]]
- [[sympy.sets/index | sympy.sets]]
- [[Tree SymPy]]
