---
title: scipy.integrate.quad — integral definida 1D de una funcion callable
aliases:
  - quad
  - scipy.integrate.quad
  - cuadratura adaptativa
tags:
  - scipy
  - api/funcion
  - integracion
lib: scipy
tipo: funcion
mod: scipy.integrate
retorna: tuple (float, float)
requiere:
  - numpy
  - concepto_callbacks_vectorizados
draft: false
---

# scipy.integrate.quad — integral definida 1D de una funcion callable

Calcula la integral definida de una **funcion callable** `f(x)` de una variable en el intervalo `[a, b]` mediante **cuadratura adaptativa** (rutinas Fortran QUADPACK). No recibe datos tabulados: recibe una funcion que SciPy evalua en los puntos que el algoritmo decide. Devuelve una **tupla** `(valor, error_absoluto_estimado)`, no un solo numero. Admite limites infinitos (`±np.inf`) para integrales impropias, parametros extra via `args` y aviso de singularidades via `points`.

> Distincion clave: `quad` integra una **funcion** (la muestrea adaptativamente). Para integrar **datos ya muestreados** (un array `y` ya tabulado) se usan `simpson` o `trapezoid`. No confundir ambos mundos.

## Firma

```python
scipy.integrate.quad(
    func,                # callable: f(x, *args) -> float  (x escalar)
    a,                   # float: limite inferior (puede ser -np.inf)
    b,                   # float: limite superior (puede ser +np.inf)
    args=(),             # tuple: argumentos extra fijos para func
    full_output=0,       # int: 1 -> devuelve dict con diagnostico interno
    epsabs=1.49e-8,      # float: tolerancia de error absoluto
    epsrel=1.49e-8,      # float: tolerancia de error relativo
    limit=50,            # int: maximo de subintervalos adaptativos
    points=None,         # secuencia: abscisas de singularidad/quiebre (solo intervalo finito)
    weight=None,         # str | None: peso para integrandos oscilatorios/singulares
    wvar=None,           # parametros del peso
    ...
) -> tuple
```

## Valor de retorno

| Posicion | Tipo | Significado |
|----------|------|-------------|
| `[0]` | `float` | Valor estimado de la integral |
| `[1]` | `float` | Cota superior del error absoluto del resultado |
| `[2]` | `dict` | Solo si `full_output=1`: diagnostico (evaluaciones, subintervalos, etc.) |

```python
valor, error = quad(func, a, b)   # desempaquetado tipico
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Integral en intervalo finito | `quad(f, 0, 1)` |
| Integral impropia (semi-infinita) | `quad(f, 0, np.inf)` |
| Integral impropia (toda la recta) | `quad(f, -np.inf, np.inf)` |
| Con parametros extra | `quad(f, a, b, args=(k,))` |
| Con singularidad conocida en c | `quad(f, a, b, points=[c])` |
| Con diagnostico interno | `quad(f, a, b, full_output=1)` |

## Parametros en detalle

### `func` (obligatorio)

Funcion `f(x)` con `x` **escalar** que devuelve un escalar. Es el integrando. SciPy la llama muchas veces, asi que conviene escribirla con operaciones de NumPy; ver [[concepto_callbacks_vectorizados]].

```python
import numpy as np
from scipy.integrate import quad

valor, error = quad(np.sin, 0, np.pi)
valor    # → 2.0   (∫ sin x dx en [0, pi])
error    # → ~2.2e-14
```

### `a`, `b` (obligatorios)

Limites de integracion. Pueden ser `±np.inf` para **integrales impropias**; QUADPACK aplica una transformacion interna del dominio.

```python
# Gaussiana sobre toda la recta: ∫ e^{-x^2} dx = sqrt(pi)
valor, error = quad(lambda x: np.exp(-x**2), -np.inf, np.inf)
valor            # → 1.7724538...
np.sqrt(np.pi)   # → 1.7724538...   (coincide)
```

### `args`

Tupla de constantes que se inyectan a `func` tras `x`. Evita closures y mantiene la firma limpia. Para un solo extra recordar la coma: `args=(k,)`.

```python
def integrando(x, a, b):
    return a * x + b

# ∫ (2x + 5) dx en [0, 1] = 6.0
valor, error = quad(integrando, 0, 1, args=(2.0, 5.0))
valor    # → 6.0
```

### `points`

Lista de abscisas donde el integrando tiene **singularidades, picos o quiebres** dentro de `(a, b)`. Fuerza al algoritmo a subdividir ahi, mejorando precision. Solo valido en intervalos finitos (no con `±inf`).

```python
# |x| tiene un quiebre en x=0; avisarlo mejora la precision
valor, error = quad(lambda x: np.abs(x), -1, 1, points=[0])
valor    # → 1.0
```

### `epsabs`, `epsrel`

Tolerancias de error absoluto y relativo. El algoritmo para cuando alcanza cualquiera de las dos. Bajarlas exige mas evaluaciones.

### `full_output`

Con `full_output=1`, el tercer elemento de la tupla es un diccionario con el numero de evaluaciones (`neval`), subintervalos y demas diagnostico. Util para depurar integrandos dificiles.

## Casos de uso

### Integral de un perfil fisico

```python
import numpy as np
from scipy.integrate import quad

# Trabajo W = ∫ F(x) dx de una fuerza variable sobre [0, 2] m
F = lambda x: 50 * np.exp(-0.5 * x)        # N
W, err = quad(F, 0, 2)
W        # → ~63.2 J
```

### Integrando con parametro de un modelo

```python
# Decaimiento radiactivo: dosis acumulada ∫ A0 e^{-λ t} dt en [0, T]
def actividad(t, A0, lam):
    return A0 * np.exp(-lam * t)

dosis, err = quad(actividad, 0, 10, args=(100.0, 0.3))
dosis    # → ~316.7
```

### Integral impropia de cola

```python
# Probabilidad de cola de una exponencial: ∫ λ e^{-λ x} dx en [x0, inf) = e^{-λ x0}
lam, x0 = 2.0, 1.5
p, err = quad(lambda x: lam * np.exp(-lam * x), x0, np.inf)
p                    # → 0.0497...
np.exp(-lam * x0)    # → 0.0497...   (coincide)
```

## Buenas practicas

1. **Desempaqueta siempre la tupla**: `valor, error = quad(...)`. El segundo elemento es la incertidumbre, no parte del resultado.
2. Revisa que `error` sea pequeño frente a `valor`; si no, el resultado es poco fiable.
3. Usa `points=[...]` cuando conozcas singularidades o quiebres interiores; mejora precision y velocidad.
4. Pasa constantes con `args` en vez de variables globales o closures.
5. Para limites infinitos usa `np.inf`, no numeros grandes arbitrarios: QUADPACK los maneja con transformacion analitica.
6. Vectoriza el integrando con NumPy aunque reciba escalares; facilita reutilizarlo y evita sorpresas.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Tratar el retorno como float | `quad` devuelve `(valor, error)` | Desempaquetar: `v, e = quad(...)` |
| `IntegrationWarning: divergent` | Integral no converge o singularidad no avisada | Usar `points=[...]`, revisar el integrando o subir `limit` |
| Precision baja con pico interno | El adaptativo no lo detecta | Indicar la abscisa en `points` |
| `TypeError: func() takes 1 arg` | Parametros extra no pasados | `quad(f, a, b, args=(p,))` |
| `points` con limite infinito da error | `points` solo en intervalo finito | Partir la integral o quitar `points` |
| Resultado con array como integrando | `quad` espera escalar->escalar | Usar `quad_vec` para integrandos vectoriales |

## Limitaciones

- Integra solo funciones **escalares de una variable**; para integrandos que devuelven arrays usar `quad_vec`.
- Para integrales dobles/triples existen `dblquad` y `tplquad`.
- No integra arrays de datos ya muestreados: para eso estan `simpson` y `trapezoid`.
- Integrandos muy oscilatorios o con singularidades fuertes pueden requerir `weight`/`wvar` o subdivision manual.

## Notas relacionadas

- [[scipy.integrate.dblquad]]
- [[scipy.integrate.simpson]]
- [[scipy.integrate.trapezoid]]
- [[concepto_callbacks_vectorizados]]
