---
title: sympy.polys/expandir_factorizar — expandir / factorizar
tags:
  - sympy
  - indice
draft: false
---

# expandir / factorizar

Esta carpeta reune las transformaciones que **reescriben** un polinomio o una expresion racional sin cambiar su valor, solo su **forma**. Son las manipulaciones algebraicas mas usadas a diario: pasar de la forma desarrollada a la factorizada y de vuelta, separar o combinar fracciones, y reordenar un polinomio por potencias de una variable. La idea central que hilvana la carpeta es que casi todas vienen en **pares inversos**: por cada funcion que "abre" una expresion hay otra que la "cierra", de modo que aplicarlas en cadena devuelve el punto de partida. Saber cual usar es saber **en que direccion** quieres mover la expresion (mas plana o mas compacta, separada o unida).

La misma idea, vista en las dos parejas y en el reordenador:

```python
from sympy import symbols, expand, factor, apart, together, collect
x, y = symbols("x y")

expand((x + 1)*(x - 1))          # x**2 - 1               -> desarrollar
factor(x**2 - 1)                 # (x - 1)*(x + 1)        -> factorizar (inversa de expand)

apart(1/(x**2 - 1))              # -1/(2*(x + 1)) + 1/(2*(x - 1))   -> separar en parciales
together(1/x + 1/y)              # (x + y)/(x*y)          -> unir (inversa de apart)

collect(x**2 + y*x**2 + x, x)    # x**2*(y + 1) + x       -> reordenar por potencias de x
```

## Como se relacionan

El modelo mental es **pares inversos** mas un reordenador suelto:

- **`expand` <-> `factor`**: `expand` distribuye y deja la forma plana (suma de terminos); `factor` agrupa y deja la forma de producto. Una deshace a la otra: `factor(expand(p)) == p` para un polinomio factorizable.
- **`apart` <-> `together`**: `apart` separa una fraccion en suma de parciales (una por factor del denominador); `together` reune sumas de fracciones en un solo cociente. Tambien se cancelan: `together(apart(f))` recupera `f`.
- **`collect`**: no tiene inversa. Es un **reordenador** que reescribe la expresion como polinomio en una variable elegida, recogiendo el coeficiente de cada potencia. Suele ir despues de `expand` (terminos sueltos) para luego leer o extraer coeficientes.

| Funcion | Que hace | Inversa de |
|---------|----------|------------|
| [[sympy.expand]] | Distribuye productos y potencias -> forma desarrollada | [[sympy.factor]] |
| [[sympy.factor]] | Escribe como producto de irreducibles -> forma factorizada | [[sympy.expand]] |
| [[sympy.apart]] | Separa una fraccion en fracciones parciales | [[sympy.together]] |
| [[sympy.together]] | Combina sumas de fracciones en un solo cociente | [[sympy.apart]] |
| [[sympy.collect]] | Agrupa por potencias de una variable (reordena) | — (no tiene inversa) |

> [!info] En que direccion mover la expresion
> Si quieres **abrir** (mas terminos, mas plano): `expand` para polinomios, `apart` para fracciones. Si quieres **cerrar** (mas compacto): `factor` para polinomios, `together` para fracciones. Si solo quieres **reordenar** un polinomio por una variable sin abrirlo ni cerrarlo: `collect`.

## Notas

- [[sympy.expand]] — desarrolla productos y potencias hasta la forma plana; es la **inversa** de `factor` y la forma canonica para comparar dos polinomios.
- [[sympy.factor]] — el camino contrario a `expand`: escribe el polinomio como producto de irreducibles sobre Q (o sobre una extension), revelando raices y factores comunes.
- [[sympy.collect]] — el reordenador de la carpeta: sin inversa, agrupa por potencias de una variable; tipicamente despues de `expand` para extraer coeficientes.
- [[sympy.apart]] — la version "fracciones" de `expand`: separa un cociente en parciales; **inversa** de `together`, util antes de integrar funciones racionales.
- [[sympy.together]] — la version "fracciones" de `factor`: reune sumas de fracciones en un solo cociente; **inversa** de `apart`, paso previo a simplificar o cancelar.

## Notas relacionadas

- [[sympy.polys/index | sympy.polys]]
- [[Tree SymPy]]
