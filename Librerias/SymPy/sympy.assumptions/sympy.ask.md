---
title: sympy.ask — consulta dinamica de propiedades con hipotesis temporales
aliases: [ask, Q]
tags: [sympy, api/funcion, assumptions]
lib: sympy
mod: sympy.assumptions
tipo: funcion
retorna: bool | None
requiere: [Symbol]
draft: false
---

# sympy.ask — consulta dinamica de propiedades con hipotesis temporales

`ask(proposition, assumptions)` es la via **dinamica** del sistema de supuestos: permite preguntar si una expresion cumple una propiedad bajo hipotesis temporales, **sin redefinir el simbolo**. Devuelve `True`, `False` o `None` (indeterminado). La proposicion y las hipotesis se construyen con los **predicados `Q`** (`Q.positive`, `Q.real`, `Q.integer`, etc.). Es el complemento de los supuestos estaticos: donde estos fijan una propiedad para toda la sesion, `ask` la consulta de forma puntual y condicional.

## Firma

```python
sympy.ask(
    proposition,    # Q.<predicado>(expr): lo que se quiere saber
    assumptions,    # Q.<predicado>(expr) o combinacion con & / | / ~  [opcional]
) -> True | False | None
```

## Valor de retorno

| Resultado | Significado |
|-----------|-------------|
| `True` | La proposicion se puede **demostrar** bajo las hipotesis dadas |
| `False` | La proposicion es **refutable** bajo las hipotesis dadas |
| `None` | **Indeterminado**: no hay suficiente informacion para concluir |

## Casos de uso

### Consulta basica sobre un simbolo con supuestos estaticos

```python
from sympy import symbols, ask, Q

xp = symbols("x", positive=True)
xi = symbols("n", integer=True)

ask(Q.positive(xp))    # True   -> el simbolo declara positive=True
ask(Q.integer(xi))     # True
ask(Q.even(2*xi))      # True   -> 2*entero es par: SymPy lo deduce
ask(Q.real(xp))        # True   -> positivo implica real
```

### Consulta sobre simbolo sin supuestos estaticos

```python
from sympy import symbols, ask, Q

x = symbols("x")       # sin supuestos

ask(Q.positive(x))     # None   -> sin informacion, indeterminado
ask(Q.real(x))         # None
ask(Q.integer(x))      # None
```

### Hipotesis temporales: preguntar "si x es real y positivo, ¿es positivo?"

```python
from sympy import symbols, ask, Q

x = symbols("x")

ask(Q.real(x), Q.positive(x))                 # True  -> positivo implica real
ask(Q.positive(x), Q.real(x) & Q.positive(x)) # True
ask(Q.negative(x), Q.positive(x))             # False -> contradiccion
```

### Operadores logicos en hipotesis

```python
from sympy import symbols, ask, Q

x, y = symbols("x y")

ask(Q.positive(x + y), Q.positive(x) & Q.positive(y))   # True
ask(Q.real(x), Q.integer(x))                             # True  -> entero implica real
ask(Q.even(x), Q.integer(x))                             # None  -> entero no implica par
```

### Deduccion sobre expresiones compuestas

```python
from sympy import symbols, ask, Q

x = symbols("x", real=True)

ask(Q.positive(x**2))          # None  -> real al cuadrado es >= 0, pero puede ser 0
ask(Q.nonnegative(x**2))       # True  -> real**2 siempre >= 0
ask(Q.real(x**2 + 1))          # True
```

## Predicados Q

| Predicado | Pregunta |
|-----------|---------|
| `Q.positive(expr)` | expr > 0 |
| `Q.negative(expr)` | expr < 0 |
| `Q.nonnegative(expr)` | expr >= 0 |
| `Q.nonpositive(expr)` | expr <= 0 |
| `Q.real(expr)` | expr pertenece a R |
| `Q.complex(expr)` | expr pertenece a C |
| `Q.integer(expr)` | expr pertenece a Z |
| `Q.rational(expr)` | expr pertenece a Q |
| `Q.irrational(expr)` | real e irracional |
| `Q.prime(expr)` | expr es primo |
| `Q.even(expr)` | expr es par (entero par) |
| `Q.odd(expr)` | expr es impar (entero impar) |
| `Q.finite(expr)` | expr no es infinito |
| `Q.commutative(expr)` | expr conmuta bajo multiplicacion |
| `Q.zero(expr)` | expr == 0 |
| `Q.nonzero(expr)` | expr != 0 |

Los predicados se combinan con los operadores `&` (y), `|` (o) y `~` (negacion).

## Supuestos estaticos vs ask dinamico

| Aspecto | Supuesto estatico | `ask` dinamico |
|---------|-------------------|----------------|
| Declaracion | `symbols("x", real=True)` | `ask(Q.real(x), hipotesis)` |
| Permanencia | Fijo en el simbolo | Solo en la llamada |
| Modifica el objeto | Si | No |
| Uso tipico | Propiedad siempre verdadera en el problema | Razonamiento condicional o exploratorio |
| Retorna | Atributo `.is_*` (`True`/`False`/`None`) | `True`/`False`/`None` |

Vease [[sympy.supuestos_simbolos]] para la via estatica.

## Limitaciones

- `ask` razona con un **motor de inferencia**: puede no deducir propiedades que son matematicamente evidentes pero para las que no tiene reglas programadas.
- Con expresiones muy complejas puede devolver `None` aunque la respuesta sea `True` o `False`.
- `ask` no modifica el simbolo: si se necesita que SymPy simplifique automaticamente bajo una propiedad, hay que declararla de forma estatica al crear el simbolo.
- No acepta ecuaciones arbitrarias como hipotesis: las hipotesis deben expresarse con predicados `Q`.

## Errores comunes

| Sintoma | Causa | Solucion |
|---------|-------|----------|
| `ask` devuelve `None` aunque la propiedad es "obvia" | El motor de inferencia no tiene la regla necesaria | Declarar el supuesto de forma estatica en el simbolo |
| Se esperaba `False` y llega `None` | `None` significa "no puedo concluir", no "falso" | Proporcionar mas hipotesis o usar supuestos estaticos |
| `ask(Q.positive(x))` con `x` definido como `positive=True` devuelve `None` | Se importo `ask` pero no `Q`, o se uso una version antigua | `from sympy import ask, Q` |
| Error al combinar hipotesis con `and` de Python | `and` no funciona con predicados `Q` | Usar `&` en vez de `and` |

## Notas relacionadas

- [[sympy.supuestos_simbolos]]
- [[concepto_symbols_assumptions]]
- [[sympy.assumptions/index | sympy.assumptions]]
