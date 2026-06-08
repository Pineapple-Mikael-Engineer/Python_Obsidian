---
title: sympy.unidades — magnitudes fisicas simbolicas con unidades SI
aliases: [unidades, Quantity, meter, kilogram]
tags: [sympy, api/concepto, physics.units]
lib: sympy
mod: sympy.physics.units
tipo: concepto
draft: false
---

# sympy.unidades — magnitudes fisicas simbolicas con unidades SI

En `sympy.physics.units` las unidades fisicas **son expresiones SymPy**. `meter`, `second`, `kilogram`, `newton`, `joule`, `watt` y cientos mas son objetos [[Quantity]] — una subclase de `Expr` — y se operan con los mismos operadores aritmeticos de cualquier expresion: `10*meter/second` es una `Expr` con unidades incrustadas, no un numero flotante desnudo. El resultado hereda la naturaleza exacta y algebraica de SymPy: las dimensiones se propagan automaticamente y no hay conversion manual ni factor de escala perdido.

El sistema de referencia (SI, MKS, CGS, etc.) queda en un objeto `UnitSystem`; SymPy incluye `SI` predefinido. La conversion entre unidades se delega a [[sympy.convert_to]].

## Unidades disponibles

Las unidades se importan del submodulo directamente. El conjunto completo esta en `sympy.physics.units.definitions`; las mas usadas:

| Magnitud | Unidades importables | Dimension |
|----------|----------------------|-----------|
| Longitud | `meter`, `kilometer`, `centimeter`, `foot`, `inch` | `length` |
| Tiempo | `second`, `minute`, `hour` | `time` |
| Masa | `kilogram`, `gram`, `pound` | `mass` |
| Fuerza | `newton`, `dyne`, `pound_force` | `force` |
| Energia | `joule`, `calorie`, `electronvolt` | `energy` |
| Potencia | `watt`, `horsepower` | `power` |
| Presion | `pascal`, `bar`, `atmosphere` | `pressure` |
| Carga | `coulomb` | `charge` |
| Voltaje | `volt` | `voltage` |
| Constantes | `speed_of_light`, `gravitational_constant`, `planck` | — |

```python
from sympy.physics.units import (
    meter, second, kilogram, newton, joule, watt,
    kilometer, hour, pascal,
)
```

## Casos de uso

### Aritmetica con unidades

Las unidades se combinan con `*` y `/` exactamente como cualquier simbolo SymPy.

```python
from sympy.physics.units import meter, second, kilogram

v = 10 * meter / second          # 10*meter/second
t = 5 * second
d = v * t                        # 50*meter   (second se cancela)

F = 3 * kilogram * meter / second**2   # 3*kilogram*meter/second**2 = 3 N
```

### Constantes fisicas

Las constantes son `Quantity` con valor fijo; se pueden combinar y luego convertir.

```python
from sympy.physics.units import speed_of_light, meter, second, convert_to

c = speed_of_light               # speed_of_light  (simbolo)
convert_to(c, meter / second)    # 299792458*meter/second
```

### Trabajo con UnitSystem

`UnitSystem` define las unidades base del sistema. `SI` es el sistema predefinido de `sympy.physics.units`.

```python
from sympy.physics.units.systems import SI
from sympy.physics.units import meter, second

SI.get_dimension_system()        # <DimensionSystem ...>
# Consultar si una expr es dimensionalmente consistente con SI:
# se usa internamente por convert_to para simplificar
```

### Dimension de una expresion

Cada `Quantity` tiene una dimension registrada; `Dimension` es otra clase de `sympy.physics.units`.

```python
from sympy.physics.units import newton, meter, kilogram, second
from sympy.physics.units.util import quantity_simplify

expr = 1 * kilogram * meter / second**2
quantity_simplify(expr)          # newton   (equivale a 1 N)
```

## Limitaciones

- Las unidades no comprueban consistencia dimensional **automaticamente**: `meter + second` no lanza error, devuelve la suma simbolica sin sentido. La consistencia la garantiza el programador o la impone `convert_to`.
- Para obtener un numero puro hay que extraerlo tras la conversion: `float(convert_to(...).args[0])`.
- No todas las unidades del SI extendido estan predefinidas; algunas poco comunes hay que construirlas como `Quantity` custom.
- El modulo `sympy.physics.units` es distinto de `astropy.units` o `pint`: no propaga incertidumbres ni tiene integracion directa con arrays NumPy.

## Notas relacionadas

- [[sympy.convert_to]]
- [[sympy.physics.units/index | sympy.physics.units]]
- [[Tree SymPy]]
