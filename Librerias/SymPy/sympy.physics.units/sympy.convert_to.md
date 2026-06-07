---
title: sympy.convert_to — convertir expresion con unidades a unidades destino
aliases: [convert_to, conversion de unidades]
tags: [sympy, api/funcion, physics.units]
lib: sympy
mod: sympy.physics.units
tipo: funcion
retorna: Expr
requiere: []
draft: false
---

# sympy.convert_to — convertir expresion con unidades a unidades destino

`convert_to(expr, target_units)` toma una expresion SymPy con unidades y la **reexpresa** en las unidades de destino, devolviendo una `Expr` con el coeficiente numerico exacto y las unidades elegidas. El proceso es puramente algebraico: SymPy cancela dimensiones y sustituye las relaciones entre unidades sin recurrir a tablas de conversion flotantes. Si las unidades origen y destino son dimensionalmente equivalentes, la conversion siempre tiene exito; si no lo son, devuelve la expresion sin cambios (no lanza error).

Es la funcion central del modulo [[sympy.unidades]] y el unico punto de contacto necesario para cambiar la representacion de una magnitud fisica.

## Firma

```python
sympy.physics.units.convert_to(
    expr,                   # Expr: expresion con unidades (o Quantity sola)
    target_units,           # Quantity | list[Quantity]: unidad(es) de destino
    unit_system="SI",       # str | UnitSystem: sistema de referencia
) -> Expr
```

## Valor de retorno

| Caso | Retorno | Ejemplo |
|------|---------|---------|
| Conversion exitosa | `Expr` con coeficiente \* unidades destino | `299792458*meter/second` |
| Unidades incompatibles | `Expr` original sin cambios | `meter` (si se intenta -> `second`) |
| Expr ya en las unidades destino | La misma `Expr` | `5*meter` -> `5*meter` |

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Convertir a una sola unidad | `convert_to(expr, newton)` |
| Descomponer en unidades base | `convert_to(expr, [kilogram, meter, second])` |
| Usar un sistema distinto de SI | `convert_to(expr, foot, "cgs")` |
| Constante fisica en unidades base | `convert_to(speed_of_light, meter/second)` |

## Parametros en detalle

### `expr` (obligatorio)

Cualquier `Expr` que contenga al menos un objeto `Quantity`. Puede ser una unidad sola (`newton`), una magnitud numerica (`10*meter/second`) o una expresion algebraica compuesta.

```python
from sympy.physics.units import newton, kilogram, meter, second, convert_to

convert_to(newton, kilogram * meter / second**2)
# kilogram*meter/second**2

convert_to(10 * newton, kilogram * meter / second**2)
# 10*kilogram*meter/second**2
```

### `target_units` (obligatorio)

La unidad o lista de unidades en las que se quiere expresar el resultado.

- **Unidad unica**: `convert_to(expr, newton)` — SymPy agrupa todo en la unidad indicada si es posible.
- **Lista de unidades base**: `convert_to(expr, [kilogram, meter, second])` — descompone en unidades fundamentales.

```python
from sympy.physics.units import joule, kilogram, meter, second, convert_to

convert_to(joule, kilogram * meter**2 / second**2)
# kilogram*meter**2/second**2

convert_to(joule, [kilogram, meter, second])
# kilogram*meter**2/second**2   (mismo resultado con lista)
```

### `unit_system` (opcional, default `"SI"`)

Cadena con el nombre del sistema (`"SI"`, `"MKS"`, `"CGS"`) o un objeto `UnitSystem`. Controla que relaciones entre unidades se usan. En la gran mayoria de casos el default `"SI"` es correcto.

## Casos de uso

### Verificar equivalencia dimensional

```python
from sympy.physics.units import newton, kilogram, meter, second, convert_to

convert_to(1 * newton, kilogram * meter / second**2)
# kilogram*meter/second**2
```

### Descomponer una unidad derivada en unidades SI base

```python
from sympy.physics.units import joule, watt, kilogram, meter, second, convert_to

convert_to(joule, [kilogram, meter, second])
# kilogram*meter**2/second**2

convert_to(watt, [kilogram, meter, second])
# kilogram*meter**2/second**3
```

### Constante de la velocidad de la luz

```python
from sympy.physics.units import speed_of_light, meter, second, convert_to

convert_to(speed_of_light, meter / second)
# 299792458*meter/second
```

### Flujo completo: definir magnitud, operar y convertir

```python
from sympy.physics.units import meter, second, kilogram, newton, convert_to

# Definir magnitudes con unidades
m  = 2 * kilogram
a  = 5 * meter / second**2
F  = m * a                          # 10*kilogram*meter/second**2

# Reexpresar en newtons
convert_to(F, newton)               # 10*newton
```

### Extraer el valor numerico

Tras la conversion, el coeficiente es el primer argumento de `Mul`:

```python
from sympy.physics.units import speed_of_light, meter, second, convert_to

c_si = convert_to(speed_of_light, meter / second)
# 299792458*meter/second
float(c_si.args[0])                 # 299792458.0
```

## Errores comunes

| Situacion | Comportamiento | Solucion |
|-----------|----------------|----------|
| Unidades incompatibles (`meter` -> `second`) | Devuelve la `Expr` original sin error | Verificar que origen y destino comparten dimension |
| Resultado inesperado con lista de destino | La lista puede ser redundante o sobredeterminada | Usa la unidad derivada directamente si existe |
| Querer un `float` puro | `convert_to` devuelve `Expr`, no numero | Extraer `float(resultado.args[0])` tras la conversion |
| Olvidar importar la unidad de destino | `NameError` | Importar explicitamente de `sympy.physics.units` |

## Limitaciones

- `convert_to` **no valida** consistencia dimensional: si las unidades son incompatibles devuelve la expresion sin convertir en vez de lanzar una excepcion, lo que puede pasar desapercibido.
- No opera sobre arrays NumPy directamente; para eso usar `pint` o `astropy.units` con soporte nativo de arrays.
- El `unit_system` `"CGS"` y otros sistemas no SI tienen cobertura parcial; algunas unidades poco comunes pueden no estar registradas.

## Notas relacionadas

- [[sympy.unidades]]
- [[sympy.physics.units/index | sympy.physics.units]]
- [[Tree SymPy]]
