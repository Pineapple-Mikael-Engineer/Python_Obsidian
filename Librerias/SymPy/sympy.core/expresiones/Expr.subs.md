---
title: Expr.subs — sustituir subexpresiones devolviendo una expresion nueva
aliases:
  - subs
  - Expr.subs
  - sustitucion simbolica
tags:
  - sympy
  - api/metodo
  - core/expresiones
lib: sympy
mod: sympy.core
tipo: metodo
obj: Expr
retorna: Expr
requiere:
  - Expr
  - concepto_expr_arbol
draft: false
---

# Expr.subs — sustituir subexpresiones devolviendo una expresion nueva

`expr.subs(old, new)` reemplaza apariciones de `old` por `new` dentro de la expresion y devuelve una **expresion NUEVA** (la original no cambia: `Expr` es inmutable, ver [[concepto_expr_arbol]]). Es el metodo estandar para evaluar parametros, particularizar una formula o intercambiar simbolos. Acepta un par `(old, new)`, un **diccionario** `{old: new, ...}` o una **lista de pares** `[(o1, n1), (o2, n2)]`, que por defecto se aplican **secuencialmente** (cada sustitucion ve el resultado de la anterior). `subs` es matematicamente "inteligente" (puede casar subexpresiones por estructura y forma), a diferencia de `xreplace`, que es un reemplazo estructural exacto y mas rapido.

> Recuerda reasignar: `e = e.subs(x, 5)`. Si solo escribes `e.subs(x, 5)` el resultado se descarta y `e` sigue intacta.

## Firma

```python
expr.subs(
    old, new,            # (forma par) reemplaza old por new
    # --- o bien ---
    seq,                 # dict {old: new} | lista [(old, new), ...]
    *,
    simultaneous=False,  # bool: True -> todos los pares a la vez (no secuencial)
    ...
) -> Expr
```

## Valor de retorno

| Tipo | Significado |
|------|-------------|
| `Expr` | Una expresion **nueva** con las sustituciones aplicadas; la original queda intacta |

```python
from sympy import symbols
x = symbols("x")
(x + 1).subs(x, 5)     # 6        -> Expr nueva
```

## Formas de llamada

| Objetivo | Llamada |
|----------|---------|
| Un solo reemplazo | `e.subs(x, 5)` |
| Varios con diccionario | `e.subs({x: 1, y: 2})` |
| Varios con lista de pares (secuencial) | `e.subs([(x, y), (y, 2)])` |
| Varios a la vez (sin encadenar) | `e.subs([(x, y), (y, x)], simultaneous=True)` |
| Reemplazar una subexpresion entera | `e.subs(x*y, z)` |

```python
from sympy import symbols
x, y, z = symbols("x y z")
(x + 1).subs(x, 5)              # 6
(x + y).subs({x: 1, y: 2})     # 3
(x * y).subs(x * y, z)         # z   -> casa la subexpresion completa
```

## Secuencial vs simultaneous

Con varios pares, `subs` por defecto los aplica **uno tras otro**: el segundo par ve ya el resultado del primero. Eso rompe los **intercambios** (swap). `simultaneous=True` aplica todos a la vez sobre la expresion original.

```python
from sympy import symbols
a, b, x, y = symbols("a b x y")

# Secuencial (default): a->b, luego b->2  =>  (b)+(2) tras a->b da b+b=2b, luego b->2
(a + b).subs([(a, b), (b, 2)])                      # 4
(a + b).subs([(a, b), (b, 2)], simultaneous=True)   # b + 2

# Intercambio x<->y: secuencial colapsa, simultaneous funciona
(x / y).subs([(x, y), (y, x)])                      # 1     -> mal
(x / y).subs([(x, y), (y, x)], simultaneous=True)   # y/x   -> correcto
```

## subs vs xreplace vs replace

| Metodo | Casa por | Velocidad | Cuando |
|--------|----------|-----------|--------|
| `subs` | estructura **y** forma matematica (mas flexible) | mas lento | uso general; sustituir simbolos, valores, subexpresiones |
| `xreplace` | **estructura exacta** (solo nodos identicos) | mas rapido | cuando sabes la subexpresion exacta y quieres rendimiento |
| `replace` | **patron** (`Wild`, tipo de nodo, predicado) | variable | reemplazos por patron/regla, no por valor concreto |

```python
from sympy import symbols, sin
x, y = symbols("x y")

# xreplace: solo nodos estructuralmente identicos
(x + 1).xreplace({x + 1: y})     # y
(sin(x + 1)).xreplace({x: y})    # sin(y + 1)

# replace por tipo de nodo: cambiar toda funcion sin por su argumento
from sympy import Function
(sin(x) + sin(y)).replace(sin, lambda a: a)   # x + y
```

## Casos de uso

### Evaluar una formula en un punto

```python
from sympy import symbols
x, y = symbols("x y")
f = x**2 + y**2
f.subs({x: 3, y: 4})     # 25
```

### Particularizar parametros de un modelo y seguir simbolico

```python
from sympy import symbols
m, a, t = symbols("m a t")
fuerza = m * a
fuerza.subs(m, 2)        # 2*a   -> sigue siendo Expr, no un numero
```

### Sustituir una subexpresion completa para simplificar

```python
from sympy import symbols, sin, cos
x = symbols("x")
expr = sin(x)**2 + cos(x)**2 + 5
expr.subs(sin(x)**2 + cos(x)**2, 1)   # 6
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `e.subs(...)` "no hace nada" | El resultado no se reasigna | `e = e.subs(...)` (las `Expr` son inmutables) |
| Intercambio `x<->y` colapsa a un valor raro | `subs` por lista es **secuencial** | `subs([...], simultaneous=True)` |
| No reemplaza una subexpresion esperada | `subs` casa por estructura/forma, no siempre coincide | Probar `xreplace` con el nodo exacto o `replace` por patron |
| `subs` lento en bucles grandes | `subs` hace casamiento matematico costoso | Usar `xreplace` si basta el reemplazo estructural exacto |
| El orden del dict cambia el resultado | Con varias claves la aplicacion puede encadenarse | Usar `simultaneous=True` para evitar dependencias de orden |

## Limitaciones

- `subs` reemplaza **subexpresiones**, no resuelve ecuaciones; para despejar usa `solve`/`solveset`.
- No garantiza que el resultado quede simplificado; encadena con `simplify`/`expand` si hace falta.
- Para reemplazos por **patron** (comodines) hace falta `replace` con `Wild`, no `subs`.

## Notas relacionadas

- [[concepto_expr_arbol]]
- [[Expr]]
- [[sympy.srepr]]
- [[Expr.evalf]]
- [[sympy.core/expresiones/index | expresiones]]
