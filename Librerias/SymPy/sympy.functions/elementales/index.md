---
title: sympy.functions/elementales — funciones matematicas elementales
tags:
  - sympy
  - indice
draft: false
---

# elementales

Esta carpeta agrupa las **funciones matematicas elementales** de SymPy: las que se estudian en calculo basico y algebra, soportadas de forma **exacta** y simbolica. Son funciones que SymPy reconoce como objetos de primera clase — no solo como expresiones genericas — y sobre las que aplica reglas de simplificacion propias, identidades conocidas y relaciones entre si.

El conjunto cubre: la raiz cuadrada (`sqrt`), la exponencial y el logaritmo natural (`exp`, `log`), las funciones trigonometricas con sus inversas (`sin`, `cos`, `tan`, `atan2`, …) y sus analogas hiperbolicas (`sinh`, `cosh`, `tanh`, …), mas el valor absoluto (`Abs`). Todas comparten el comportamiento base: evaluan **exactamente** en puntos especiales, devuelven la expresion sin evaluar cuando no hay simplificacion disponible, y respetan los **supuestos** del simbolo (`positive`, `real`, etc.) para decidir si simplificar o no.

## Ejemplo unificador

La siguiente expresion encadena cuatro funciones distintas de esta carpeta y produce un resultado exacto:

```python
from sympy import sin, log, exp, sqrt, pi

expr = sin(pi/4) + log(exp(1)) + sqrt(2)
# sin(pi/4)  -> sqrt(2)/2
# log(exp(1)) -> 1
# sqrt(2)    -> sqrt(2)
# Total:     1 + 3*sqrt(2)/2

expr    # 1 + 3*sqrt(2)/2
```

No hay un solo flotante: SymPy maneja la suma y extrae el resultado en forma exacta usando la raiz cuadrada de dos como unidad simbolica.

## Como se relacionan

La pregunta clave es **que tipo de funcion necesitas** y **que simplificacion esperas**.

| Funcion / grupo | Nota | Cuando usarla | Simplifica automaticamente |
|-----------------|------|---------------|---------------------------|
| `sqrt(x)` | [[sympy.sqrt]] | Raiz cuadrada exacta; extrae factores cuadrados perfectos | Si: `sqrt(8)` → `2*sqrt(2)` |
| `exp(x)`, `log(x)` | [[sympy.exp_log]] | Exponencial y logaritmo natural; base de la transcendencia | Parcial: `exp(log(x))` → `x`; `log(x*y)` NO |
| `sin`, `cos`, `tan`, inversas | [[sympy.trigonometricas]] | Trigonometria exacta en radianes; angulos especiales | Si en angulos especiales; identidades requieren `trigsimp` |
| `sinh`, `cosh`, `tanh`, inversas | [[sympy.hiperbolicas]] | Analoga hiperbolica; conversion a `exp` con `rewrite` | Parcial: identidad `cosh^2 - sinh^2` requiere `simplify` |
| `Abs(x)` | [[Abs]] | Valor absoluto simbolico; sensible al signo del simbolo | Solo con supuestos `positive` / `negative` declarados |

Arbol de decision:

- ¿Necesitas `x^(1/2)` exacta con simplificacion de factores? → [[sympy.sqrt]].
- ¿Trabajas con crecimiento exponencial o logaritmos? → [[sympy.exp_log]]. Recuerda que `log` en SymPy siempre es ln; usa `log(x, b)` para otra base.
- ¿Modelas oscilaciones, angulos o geometria? → [[sympy.trigonometricas]]. Para el angulo en el plano con cuadrante correcto, usa `atan2(y, x)`.
- ¿Modelas curvas hiperbolicas o necesitas la forma en `exp`? → [[sympy.hiperbolicas]]. Usa `.rewrite(exp)` para ver la definicion explicita.
- ¿Necesitas el modulo de una expresion simbolica? → [[Abs]]. Declara `positive=True` para que simplifique; sin supuestos queda como `Abs(x)`.

> [!info] Supuestos y simplificacion
> Muchas simplificaciones de esta carpeta **dependen de los supuestos del simbolo**. `sqrt(x**2)` no da `x` sin `positive=True`; `Abs(x)` no da `x` sin `positive=True`; `expand_log(log(x*y))` no separa sin `positive=True`. Declarar supuestos es la palanca clave para obtener formas simplificadas.

## Notas

- [[sympy.sqrt]] — raiz cuadrada exacta; reconocida por SymPy como funcion propia y simplificada mejor que `x**Rational(1,2)` en muchos casos.
- [[sympy.exp_log]] — `exp` y `log`; el par inverso fundamental de la transcendencia. `log` es siempre logaritmo natural; `expand_log` separa productos en sumas de logaritmos.
- [[sympy.trigonometricas]] — `sin`, `cos`, `tan` y sus inversas; evaluan exactamente en angulos especiales. `trigsimp` simplifica identidades. `atan2` para angulos en el plano.
- [[sympy.hiperbolicas]] — `sinh`, `cosh`, `tanh` y sus inversas; analogas hiperbolicas. `rewrite(exp)` expone la definicion en terminos de la exponencial.
- [[Abs]] — valor absoluto simbolico; clase SymPy que respeta supuestos de signo. `rewrite(Piecewise)` expone la definicion por tramos.

## Notas relacionadas

- [[sympy.functions/index | sympy.functions]]
