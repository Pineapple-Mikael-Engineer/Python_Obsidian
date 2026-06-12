---
title: sympy.supuestos_simbolos — supuestos estaticos en la declaracion de simbolos
aliases: [supuestos, assumptions]
tags: [sympy, api/concepto, assumptions]
lib: sympy
mod: sympy.assumptions
tipo: concepto
draft: false
---

# sympy.supuestos_simbolos — supuestos estaticos en la declaracion de simbolos

Al crear un simbolo con `symbols(...)`, se pueden declarar **supuestos** (*assumptions*) como argumentos clave: `real=True`, `positive=True`, `integer=True`, etc. Estos supuestos son **estaticos** — quedan fijados en el objeto `Symbol` para toda la sesion — y le dicen a SymPy que propiedades puede asumir verdaderas al simplificar, resolver o evaluar. Sin supuestos, un simbolo es el mas general posible (potencialmente complejo), y eso bloquea muchas simplificaciones. Declarar los supuestos correctos es el primer paso para obtener resultados utiles.

Vease [[concepto_symbols_assumptions]] para el modelo mental completo sobre el rol de los supuestos en SymPy.

## Como funciona

```python
symbols("nombre", supuesto=True, ...)
```

Los supuestos se pasan como `kwargs` booleanos al crear el simbolo. Una vez creado, el simbolo expone esos supuestos como atributos `.is_*` que devuelven `True`, `False` o `None` (desconocido, logica de tres valores).

```python
from sympy import symbols

xp = symbols("x", positive=True)
xp.is_positive   # True
xp.is_real       # True   -> positivo implica real
xp.is_integer    # None   -> no declarado, desconocido
```

## Casos de uso

### Efecto en sqrt y valor absoluto

```python
from sympy import symbols, sqrt, Abs

x  = symbols("x")                    # sin supuestos
xr = symbols("x", real=True)
xp = symbols("x", positive=True)

sqrt(x**2)    # sqrt(x**2)   -> no puede simplificar (x podria ser complejo)
sqrt(xr**2)   # Abs(x)       -> real: puede ser negativo, |x| es lo correcto
sqrt(xp**2)   # x            -> positivo: siempre >= 0, la raiz es x mismo
Abs(xp)       # x            -> positivo implica Abs(x) = x
```

### Efecto en expresiones trigonometricas y exponenciales

```python
from sympy import symbols, cos, pi, log, exp

n = symbols("n", integer=True)
cos(2*pi*n)        # 1       -> entero: SymPy sabe que 2*pi*n es multiplo de 2*pi

xp = symbols("x", positive=True)
log(exp(xp))       # x       -> positivo habilita log(exp(x)) = x
```

### Multiples supuestos combinados

```python
from sympy import symbols

n = symbols("n", integer=True, positive=True)
n.is_integer        # True
n.is_positive       # True
n.is_negative       # False   -> positivo implica no negativo
n.is_real           # True    -> entero implica real
```

### Dos simbolos con el mismo nombre, distintos supuestos, son objetos distintos

```python
from sympy import symbols

a  = symbols("a")
ap = symbols("a", positive=True)

a == ap    # False   -> mismo nombre, distintos supuestos = objetos distintos
```

## Tabla de supuestos

| Supuesto | Significado matematico | Implicaciones automaticas | Efecto tipico en SymPy |
|----------|------------------------|---------------------------|------------------------|
| `real=True` | x in R | — | habilita comparaciones de orden, evita ramas complejas |
| `positive=True` | x > 0 | `real`, `nonzero`, `nonnegative` | `sqrt(x**2) -> x`; `log(exp(x)) -> x`; `Abs(x) -> x` |
| `negative=True` | x < 0 | `real`, `nonzero`, `nonpositive` | signo conocido; `Abs(x) -> -x` |
| `nonnegative=True` | x >= 0 | `real` | `sqrt(x**2) -> x` igual que positive |
| `integer=True` | x in Z | `rational`, `real` | `cos(2*pi*n) -> 1`; `(-1)**(2*n) -> 1` |
| `rational=True` | x in Q | `real` | permite operar con fracciones exactas sin asumir entero |
| `complex=True` | x in C | — | el mas general (comportamiento por defecto) |
| `finite=True` | x no es infinito | — | descarta casos de limite; habilita ciertas simplificaciones |
| `commutative=True` | x*y == y*x | — | `True` por defecto; `False` para algebra de matrices no conmutativa |

> [!info] Logica de tres valores
> Los atributos `.is_*` devuelven `True`, `False` o `None`. `None` no significa "falso":
> significa **desconocido**. SymPy no asume; solo concluye lo que puede demostrar.

## Supuestos estaticos vs consulta dinamica

| Aspecto | Supuesto estatico | `ask` dinamico |
|---------|-------------------|----------------|
| Cuando se declara | Al crear el simbolo | En el momento de la consulta |
| Alcance | Todo el ciclo de vida del simbolo | Solo la consulta concreta |
| Modifica el simbolo | Si (permanente) | No |
| Caso tipico | La propiedad es siempre verdadera en el problema | Hipotesis temporal o condicional |
| Herramienta | `symbols("x", real=True)` | `ask(Q.real(x), hipotesis)` |

Para la consulta dinamica vease [[sympy.ask]].

## Errores comunes

| Sintoma | Causa | Solucion |
|---------|-------|----------|
| `sqrt(x**2)` no simplifica a `x` | Falta `positive=True` | `symbols("x", positive=True)` |
| Resultado diferente al esperado en otro modulo | Se creo el simbolo dos veces con distintos supuestos | Crear el simbolo una vez y reutilizarlo |
| `.is_positive` devuelve `None` esperando `False` | Logica de 3 valores: `None` es desconocido, no `False` | Declarar el supuesto explicitamente |
| `positive=True` no actua como se espera | Se aplico a una expresion, no al simbolo | Los supuestos van en `symbols(...)`, no en `simplify` |

## Notas relacionadas

- [[concepto_symbols_assumptions]]
- [[sympy.ask]]
- [[sympy.assumptions/index | sympy.assumptions]]
