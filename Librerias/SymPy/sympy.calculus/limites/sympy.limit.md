---
title: sympy.limit — limite de una expresion cuando x tiende a un punto
aliases:
  - limit
  - sympy.limit
  - limite
tags:
  - sympy
  - api/funcion
  - calculus/limites
lib: sympy
mod: sympy.calculus
tipo: funcion
retorna: Expr
requiere:
  - Symbol
  - Expr
draft: false
---

# sympy.limit — limite de una expresion cuando x tiende a un punto

`limit(f, x, x0)` calcula el limite simbolico de la expresion `f` cuando la variable `x` tiende al valor `x0`, y **devuelve el resultado ya evaluado** como [[Expr]]. Resuelve indeterminaciones clasicas (`0/0`, `inf/inf`, `1**inf`) usando el algoritmo de Gruntz, asi que `sin(x)/x` cuando `x -> 0` da `1` directamente. Admite limites en el **infinito** (`x0 = oo`) y limites **laterales** mediante `dir`. Cuando el limite no existe como valor finito devuelve un objeto simbolico especial: `oo`/`-oo` (infinito con signo), `zoo` (infinito complejo / sin direccion definida) o `nan` (no determinable).

> Por defecto `dir="+"`: el limite es **por la derecha**. Para el limite por la izquierda usa `dir="-"`, y para exigir que ambos lados coincidan usa `dir="+-"` (devuelve `zoo`/`nan` si difieren).

## Firma

```python
sympy.limit(
    e,            # Expr: la expresion f cuyo limite se busca
    z,            # Symbol: la variable que tiende al punto
    z0,           # Expr: el punto destino (puede ser oo, -oo, un numero o un simbolo)
    dir="+",      # str: "+" derecha | "-" izquierda | "+-" bilateral
) -> Expr
```

## Valor de retorno

| Salida | Significado |
|--------|-------------|
| `Expr` finita | El limite existe y vale ese numero/expresion (`1`, `1/2`, `E`...) |
| `oo` / `-oo` | El limite diverge a mas/menos infinito (real, con signo) |
| `zoo` | Infinito complejo: diverge en magnitud sin signo/direccion unica (p. ej. bilateral de `1/x`) |
| `nan` | Indeterminado: SymPy no puede asignar un valor (limite inexistente o no calculable) |

```python
from sympy import symbols, limit, sin
x = symbols("x")
limit(sin(x)/x, x, 0)     # 1   -> resuelve la indeterminacion 0/0
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Limite en un punto finito | `limit(f, x, 0)` |
| Limite por la derecha | `limit(f, x, 0, "+")` |
| Limite por la izquierda | `limit(f, x, 0, "-")` |
| Limite bilateral (exige coincidencia) | `limit(f, x, 0, "+-")` |
| Limite en el infinito | `limit(f, x, oo)` |
| Limite en menos infinito | `limit(f, x, -oo)` |

```python
from sympy import symbols, limit, sin, oo
x = symbols("x")
limit(sin(x)/x, x, 0)      # 1
limit(1/x, x, oo)          # 0
limit((1 + 1/x)**x, x, oo) # E
```

## Parametros en detalle

### `e` (obligatorio)

La expresion `f` cuyo limite se calcula. Cualquier [[Expr]] valida; las indeterminaciones se resuelven solas.

```python
from sympy import symbols, limit, cos
x = symbols("x")
limit((1 - cos(x)) / x**2, x, 0)   # 1/2   -> indeterminacion 0/0 resuelta
```

### `z`, `z0` (obligatorios)

`z` es la variable y `z0` el punto destino. `z0` puede ser un numero, un simbolo, o `oo`/`-oo` para limites en el infinito (no se pasa `float('inf')`, se usa la `oo` de SymPy).

```python
from sympy import symbols, limit, exp, oo, atan, pi
x = symbols("x")
limit(exp(x), x, oo)     # oo        -> diverge: crece sin cota
limit(exp(x), x, -oo)    # 0
limit(atan(x), x, oo)    # pi/2      -> asintota horizontal finita
```

### `dir`

Direccion de aproximacion. Es la clave de los **limites laterales**:

- `"+"` (default): por la derecha, `z -> z0` con `z > z0`.
- `"-"`: por la izquierda, `z -> z0` con `z < z0`.
- `"+-"`: bilateral; si los dos lados no coinciden devuelve `zoo` o `nan`.

```python
from sympy import symbols, limit
x = symbols("x")
limit(1/x, x, 0, "+")    #  oo    -> por la derecha sube a +inf
limit(1/x, x, 0, "-")    # -oo    -> por la izquierda baja a -inf
limit(1/x, x, 0, "+-")   #  zoo   -> bilateral: lados distintos, infinito complejo
```

> Como el default es `"+"`, `limit(1/x, x, 0)` devuelve `oo`, no `zoo`. Si quieres el comportamiento bilateral "de libro de texto" pide `dir="+-"` explicitamente.

## Casos de uso

### Resolver una indeterminacion clasica

```python
from sympy import symbols, limit, sin, tan
x = symbols("x")
limit(sin(x)/x, x, 0)        # 1
limit(tan(x)/x, x, 0)        # 1
```

### Comportamiento asintotico de una funcion

```python
from sympy import symbols, limit, oo
x = symbols("x")
f = (2*x**2 + 3*x) / (x**2 - 1)
limit(f, x, oo)      # 2     -> asintota horizontal y = 2
```

### Detectar una asintota vertical con limites laterales

```python
from sympy import symbols, limit
x = symbols("x")
g = 1/(x - 2)
limit(g, x, 2, "+")   #  oo
limit(g, x, 2, "-")   # -oo    -> salto de signo: asintota vertical en x = 2
```

### El numero e como limite

```python
from sympy import symbols, limit, oo
x = symbols("x")
limit((1 + 1/x)**x, x, oo)   # E
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Se esperaba `zoo` pero sale `oo` | El default es `dir="+"`, no bilateral | Pedir `limit(f, x, x0, "+-")` para el limite por ambos lados |
| Pasar `float('inf')` como punto | SymPy usa su propio infinito | Importar y usar `oo` (`from sympy import oo`) |
| Resultado `nan` inesperado | Limite realmente inexistente o expresion mal formada | Revisar `f`; probar limites laterales por separado |
| Tratar `oo`/`zoo` como un numero Python | Son objetos simbolicos de SymPy | Compararlos con `oo`/`zoo` simbolicos, no con `math.inf` |
| El simbolo no es el correcto | `z` debe ser el `Symbol` que aparece en `f` | Crear los simbolos con `symbols(...)` y reutilizarlos |

## Limitaciones

- `limit` **evalua** el limite; para mostrar el planteamiento sin resolver usa la clase [[Limit]] y su `.doit()`.
- No es una funcion de continuidad ni resuelve ecuaciones; solo calcula el limite puntual.
- Limites muy patologicos o no elementales pueden devolver `nan` o quedar sin evaluar.
- El resultado simbolico es exacto; para un flotante aplica `.evalf()` sobre la salida.

## Notas relacionadas

- [[Limit]]
- [[Expr]]
- [[sympy.calculus/limites/index | limites]]
- [[sympy.calculus/index | sympy.calculus]]
