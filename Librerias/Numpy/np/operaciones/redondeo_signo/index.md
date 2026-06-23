---
title: np/operaciones/redondeo_signo — redondeo, signo y valor absoluto (ufuncs)
tags:
  - numpy
  - indice
draft: false
---

# np/operaciones/redondeo_signo — redondeo, signo y valor absoluto (ufuncs)

Las [[concepto_ufuncs|ufuncs]] **element-wise** que llevan un valor real a un entero (redondeos) o que
extraen su signo y magnitud (signo / valor absoluto). Todas conservan el shape (no hay `axis` ni
colapso de ejes) y aparecen constantemente en cálculo numérico, discretización, normalización y
detección de signos.

Se agrupan en dos familias:

- **Redondeos** — [[np.floor]], [[np.ceil]], [[np.trunc]], [[np.rint]] y [[np.round]]: llevan cada
  valor a un entero según una **dirección** distinta.
- **Signo y valor absoluto** — [[np.abs]], [[np.fabs]] y [[np.sign]]: separan magnitud y signo.

## Redondeo: la tabla que lo explica todo

La única diferencia entre los cinco redondeos es **hacia dónde** mandan el valor. Se ve de golpe con
un positivo y un negativo (`2.5` y `-2.5`, donde además aparece el empate `.5`):

| `x` | [[np.floor]] (→ −∞) | [[np.ceil]] (→ +∞) | [[np.trunc]] (→ 0) | [[np.rint]] (más cercano) | [[np.round]] (más cercano) |
|-----|---------------------|--------------------|--------------------|---------------------------|----------------------------|
| `2.5` | `2.` | `3.` | `2.` | `2.` | `2.` |
| `-2.5` | `-3.` | `-2.` | `-2.` | `-2.` | `-2.` |
| `2.7` | `2.` | `3.` | `2.` | `3.` | `3.` |
| `-2.7` | `-3.` | `-2.` | `-2.` | `-3.` | `-3.` |

Lectura rápida:
- `floor` baja hacia $-\infty$; `ceil` sube hacia $+\infty$; `trunc` va hacia **cero** (= `floor` en
  positivos, = `ceil` en negativos).
- `rint` y `round` van al **entero más cercano** y dan el mismo valor; difieren en el resto:
  `round` admite `decimals` y conserva el dtype (float→float), `rint` es la ufunc pura y siempre
  devuelve float.

> [!warning] Redondeo bancario (*half-to-even*) en `round` y `rint`
> En los empates exactos `.5`, NumPy **no** redondea "hacia arriba" sino al entero **par** más
> cercano. Por eso `round(0.5) = 0`, `round(2.5) = 2` pero `round(1.5) = 2`. Es lo que más
> sorprende; está pensado para no sesgar estadísticamente una serie de redondeos. Si necesitas
> half-up clásico, usa `np.floor(x + 0.5)`.

Todos los redondeos **devuelven float** (incluido `round`, que conserva el dtype de entrada);
convierte con `.astype(int)` si necesitas enteros de verdad.

## Signo y valor absoluto

| ufunc | Qué hace |
|-------|----------|
| [[np.abs]] | valor absoluto elemento a elemento; alias de `np.absolute`; para **complejos** devuelve el módulo $\sqrt{re^2+im^2}$; es la versión de uso general |
| [[np.fabs]] | valor absoluto solo para flotantes; **no** acepta complejos ni conserva enteros (siempre float); usar `np.abs` salvo que quieras forzar float |
| [[np.sign]] | devuelve `-1`, `0` o `1` según el signo; para complejos devuelve el vector unitario en la misma dirección |

La distinción clave: **`abs` soporta complejos** (módulo) y conserva el dtype; **`fabs` no** y
siempre da float.

## Funciones de este grupo

- [[np.floor]] — suelo, hacia $-\infty$ (`floor(-2.5) = -3`).
- [[np.ceil]] — techo, hacia $+\infty$.
- [[np.trunc]] — truncamiento hacia cero (`trunc(-2.7) = -2`).
- [[np.rint]] — al entero más cercano (half-to-even), devuelve float.
- [[np.round]] — al más cercano con `decimals` (half-to-even); alias `np.around`.
- [[np.abs]] — valor absoluto / módulo (complejos).
- [[np.fabs]] — valor absoluto solo float.
- [[np.sign]] — signo (`-1`, `0`, `1`).

## Notas relacionadas

- [[concepto_ufuncs]]
- [[concepto_broadcasting]]
- [[Librerias/Numpy/np/operaciones/index\|np/operaciones — ufuncs element-wise]]
