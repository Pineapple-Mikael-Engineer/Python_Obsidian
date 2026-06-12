---
title: sympy.physics.units — analisis dimensional simbolico
tags:
  - sympy
  - indice
draft: false
---

# sympy.physics.units — analisis dimensional simbolico

`sympy.physics.units` convierte las unidades fisicas en **ciudadanos de primera clase del algebra simbolica**. Cada unidad — `meter`, `second`, `kilogram`, `newton`, `joule`, `watt` y cientos mas — es un objeto [[sympy.unidades|Quantity]], una subclase de `Expr`. Eso significa que `10*meter/second` no es un numero con una etiqueta: es una expresion SymPy exacta donde las dimensiones se propagan, se cancelan y se simplifican con las mismas reglas que cualquier polinomio o funcion. No hay conversion manual, no hay factores de escala escritos a mano, no hay error de redondeo.

La funcion [[sympy.convert_to]] cierra el ciclo: dada una expresion con unidades, la reexpresa en las unidades de destino que elijas — ya sea una unidad derivada (`newton`) o una lista de unidades base (`[kilogram, meter, second]`) — devolviendo siempre una `Expr` exacta.

El modulo es util en cualquier calculo de ingenieria o fisica donde la consistencia dimensional importa: cinematica, dinamica, termodinamica, electromagnetismo, o simplemente para verificar que una formula tiene las dimensiones correctas.

---

Ejemplo unificador — cinematica con unidades:

```python
from sympy.physics.units import meter, second, kilogram, newton, convert_to

# Definir magnitudes con unidades incrustadas
d = 50 * meter
t = 5  * second
v = d / t                        # 10*meter/second  (second no se pierde)

# Fuerza sobre una masa en movimiento uniforme (solo para ilustrar convert_to)
m = 2 * kilogram
a = v / t                        # 2*meter/second**2
F = m * a                        # 4*kilogram*meter/second**2

convert_to(F, newton)            # 4*newton
```

La expresion `d / t` cancela dimensiones automaticamente; `convert_to(F, newton)` reconoce que `kilogram*meter/second**2` es exactamente un `newton` y reemplaza sin ninguna tabla de conversion adicional.

---

## Como se relacionan

| Elemento | Rol | Cuando usarlo |
|----------|-----|---------------|
| [[sympy.unidades]] (concepto) | Las unidades como objetos `Quantity`: `meter`, `newton`, `joule`… | Siempre que quieras operar con magnitudes fisicas en SymPy |
| [[sympy.convert_to]] (funcion) | Reexpresar una `Expr` con unidades en otras unidades de destino | Cuando necesitas cambiar la representacion o extraer el coeficiente numerico |

Tabla de decision rapida:

| Necesito… | Usar… |
|-----------|-------|
| Operar con unidades (sumar, multiplicar, dividir magnitudes) | Importar las unidades y usarlas como `Expr` normales |
| Cambiar de unidades (`newton` -> `kg·m/s²`) | `convert_to(expr, target)` |
| Descomponer en unidades SI base | `convert_to(expr, [kilogram, meter, second])` |
| Verificar equivalencia dimensional | `convert_to` — si las dimensiones coinciden la conversion tiene exito |
| Obtener un numero puro tras la conversion | `float(convert_to(...).args[0])` |

> [!info] Exactitud simbolica
> Todo en `sympy.physics.units` es **exacto**: `convert_to(speed_of_light, meter/second)` devuelve `299792458*meter/second` (entero exacto), no un flotante aproximado. El puente a NumPy es `float(resultado.args[0])` una vez que la conversion esta hecha.

## Notas

- [[sympy.unidades]] — el concepto central: `Quantity`, las unidades del SI como objetos `Expr`, `UnitSystem` y operacion algebraica directa.
- [[sympy.convert_to]] — la funcion que reexpresa una `Expr` con unidades en otras unidades de destino; unica via de conversion en el modulo.

## Notas relacionadas

- [[SymPy/index | SymPy]]
