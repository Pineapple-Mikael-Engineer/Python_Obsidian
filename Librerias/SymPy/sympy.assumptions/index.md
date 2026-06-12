---
title: sympy.assumptions — el sistema de supuestos de SymPy
tags:
  - sympy
  - indice
draft: false
---

# sympy.assumptions

`sympy.assumptions` es el **sistema de razonamiento sobre propiedades de simbolos y expresiones** de SymPy. Su funcion es decirle al motor algebraico lo que se sabe del dominio de una variable — si es real, positiva, entera… — para que pueda hacer simplificaciones que de otro modo no son validas. Sin supuestos, un simbolo es **lo mas general posible** (potencialmente complejo), y SymPy no puede asumir nada sobre el. Con supuestos correctos, las simplificaciones que el algebra justifica ocurren automaticamente.

El sistema ofrece **dos vias complementarias**: la **estatica** (supuestos fijados al crear el simbolo) y la **dinamica** (consultas puntuales con `ask` bajo hipotesis temporales). La eleccion entre ellas determina como SymPy razona a lo largo de la sesion.

## Ejemplo unificador

El mismo calculo con y sin supuestos muestra el impacto concreto:

```python
from sympy import symbols, sqrt, Abs, ask, Q

# Sin supuestos: el simbolo es general (posiblemente complejo)
x = symbols("x")
sqrt(x**2)                                    # sqrt(x**2)  -> no simplifica

# Supuesto estatico: real -> puede ser negativo, sqrt(x**2) = |x|
xr = symbols("x", real=True)
sqrt(xr**2)                                   # Abs(x)

# Supuesto estatico: positivo -> siempre >= 0, sqrt(x**2) = x
xp = symbols("x", positive=True)
sqrt(xp**2)                                   # x
Abs(xp)                                       # x

# Supuesto dinamico: preguntar "si x es positivo, ¿es real?"
# sin redefinir el simbolo x original
ask(Q.real(x), Q.positive(x))                 # True
ask(Q.positive(x), Q.real(x) & Q.positive(x)) # True
ask(Q.positive(x))                             # None  -> sin hipotesis, indeterminado
```

El mismo `x` produce tres resultados distintos segun el supuesto declarado. La decision de usar supuesto estatico o `ask` dinamico es la eleccion central de esta carpeta.

## Como se relacionan

| Criterio | Supuesto estatico (`symbols(real=True, ...)`) | `ask` dinamico (`ask(Q.real(x), hipotesis)`) |
|----------|-----------------------------------------------|----------------------------------------------|
| Cuando usar | La propiedad es **siempre verdadera** en el problema (longitud, indice, angulo real) | Razonamiento **condicional o exploratorio**: "si x fuera positivo, ¿que concluimos?" |
| Permanencia | Fijo en el objeto `Symbol` para toda la sesion | Solo en esa llamada; no modifica el simbolo |
| Efecto en simplificaciones | **Automatico**: `sqrt(xp**2)` se simplifica sin pedirlo | Ninguno sobre el algebra; solo responde `True`/`False`/`None` |
| Retorna | Atributos `.is_*` del simbolo | `True`, `False` o `None` |
| Caso tipico | Declarar `x` real o `n` entero al inicio del script | Explorar propiedades de expresiones sin reescribir el codigo |

Regla rapida: si la propiedad rige **todo el problema**, usala como supuesto estatico. Si la propiedad es una **hipotesis temporal** o se quiere interrogar el sistema sin comprometer el simbolo, usa `ask`.

> [!info] Por que importa
> La mayoria de los casos en que SymPy "no simplifica" se deben a supuestos ausentes. Antes de
> encadenar `simplify` + `expand` + `trigsimp`, revisar si el problema es simplemente que falta
> `real=True` o `positive=True` en la declaracion del simbolo.

## Notas

- [[sympy.supuestos_simbolos]] — como declarar supuestos al crear simbolos (`real`, `positive`, `integer`, etc.) y que simplificaciones habilitan. Incluye la tabla completa de supuestos y sus implicaciones automaticas.
- [[sympy.ask]] — consulta dinamica de propiedades con predicados `Q` e hipotesis temporales. Devuelve `True`, `False` o `None`. Complemento de los supuestos estaticos cuando la propiedad es condicional.

## Notas relacionadas

- [[concepto_symbols_assumptions]]
- [[SymPy/index | SymPy]]
