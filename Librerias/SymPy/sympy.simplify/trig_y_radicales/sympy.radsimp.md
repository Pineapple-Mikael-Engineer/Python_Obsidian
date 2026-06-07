---
title: sympy.radsimp — racionalizar denominadores y simplificar radicales
aliases:
  - radsimp
  - sympy.radsimp
  - racionalizar denominador
tags:
  - sympy
  - api/funcion
  - simplify/trig_y_radicales
lib: sympy
mod: sympy.simplify
tipo: funcion
retorna: Expr
requiere:
  - Symbol
draft: false
---

# sympy.radsimp — racionalizar denominadores y simplificar radicales

`radsimp(expr)` **racionaliza** los denominadores de una expresion: elimina las raices del denominador multiplicando por el conjugado adecuado, de modo que el resultado tenga denominador sin radicales. Es el simplificador **especializado** en radicales y cocientes con raices, el caso que `simplify` no siempre normaliza de forma predecible. El ejemplo canonico es racionalizar `1/(sqrt(2) + 1)`, que se convierte en `sqrt(2) - 1` al multiplicar arriba y abajo por `sqrt(2) - 1`. Funciona tambien con sumas de varios radicales en el denominador.

> `radsimp` ataca el **denominador**. Para simplificar radicales **anidados** (raices dentro de raices, como `sqrt(3 + 2*sqrt(2))`) existe la funcion hermana `sqrtdenest` (no documentada aqui, vive en el codigo), que "desanida" cuando es posible: `sqrtdenest(sqrt(3 + 2*sqrt(2)))` da `1 + sqrt(2)`.

## Firma

```python
sympy.radsimp(
    expr,                # Expr: expresion con radicales en el denominador
    symbolic=True,       # bool: racionalizar tambien denominadores simbolicos
    max_terms=4,         # int: tope de terminos del denominador a racionalizar
) -> Expr
```

## Valor de retorno

| Tipo | Forma | Significado |
|------|-------|-------------|
| `Expr` | expresion con denominador racional | La misma expresion con las raices movidas fuera del denominador |

Si el denominador ya es racional (sin radicales), devuelve la expresion **sin cambios**.

```python
from sympy import radsimp, sqrt
radsimp(1/(sqrt(2) + 1))   # -1 + sqrt(2)
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Racionalizar un radical simple | `radsimp(1/(sqrt(2) + 1))` |
| Racionalizar suma de dos radicales | `radsimp(1/(sqrt(3) + sqrt(2)))` |
| Racionalizar tres terminos | `radsimp(1/(1 + sqrt(2) + sqrt(3)))` |
| Limitar la expansion | `radsimp(expr, max_terms=2)` |

## Parametros en detalle

### `expr` (obligatorio)

La expresion cuyo denominador se quiere racionalizar. Multiplica numerador y denominador por el conjugado para dejar el denominador libre de raices.

```python
from sympy import radsimp, sqrt
radsimp(1/(sqrt(2) + 1))         # -1 + sqrt(2)
radsimp(1/(sqrt(3) + sqrt(2)))   # -sqrt(2) + sqrt(3)
radsimp(sqrt(2)/(sqrt(2) + sqrt(3)))   # -2 + sqrt(6)
```

Maneja sumas de **mas de dos** radicales en el denominador:

```python
from sympy import radsimp, sqrt
radsimp(1/(1 + sqrt(2) + sqrt(3)))   # (-sqrt(6) + sqrt(2) + 2)/4
```

### `symbolic`

Con `symbolic=True` (por defecto) intenta racionalizar tambien denominadores que contienen simbolos, no solo numeros. Ponerlo a `False` limita la racionalizacion a denominadores puramente numericos.

### `max_terms`

Tope de terminos del denominador que `radsimp` esta dispuesta a racionalizar (la racionalizacion de muchos radicales crece muy rapido). Subirlo permite atacar denominadores con mas sumandos a costa de expresiones mayores.

## Casos de uso

### Limpiar un resultado con raiz en el denominador

Un cociente con radical en el denominador es valido pero incomodo de leer o comparar; racionalizarlo da una forma canonica sin raices abajo.

```python
from sympy import radsimp, sqrt
radsimp(1/(sqrt(2) + 1))   # -1 + sqrt(2)
```

### Preparar una expresion antes de evaluar o comparar

Tras racionalizar, dos expresiones equivalentes con distinta forma de denominador coinciden, y la evaluacion numerica es mas estable.

```python
from sympy import radsimp, sqrt
expr = sqrt(2)/(sqrt(2) + sqrt(3))
radsimp(expr)   # -2 + sqrt(6)
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| No simplifica `sqrt(3 + 2*sqrt(2))` | Eso es un radical **anidado**, no un denominador | Usar `sqrtdenest`, que devuelve `1 + sqrt(2)` |
| Esperar que toque trigonometricas o potencias | `radsimp` solo ataca radicales en denominadores | Usar [[sympy.trigsimp]] o [[sympy.powsimp]] |
| Resultado enorme con muchos radicales | El conjugado de muchos terminos explota | Bajar `max_terms` o reestructurar la expresion |
| Sin cambios | El denominador ya era racional | Verificar que realmente hay raices en el denominador |

## Notas relacionadas

- [[sympy.trigsimp]]
- [[sympy.powsimp]]
- [[sympy.simplify/trig_y_radicales/index | trig_y_radicales]]
