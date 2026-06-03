---
title: scipy.integrate.odeint — integrador clasico de EDO (interfaz antigua, LSODA)
aliases:
  - odeint
  - scipy.integrate.odeint
  - integrar edo odeint
tags:
  - scipy
  - api/funcion
  - edo
lib: scipy
tipo: funcion
mod: scipy.integrate
retorna: ndarray
requiere:
  - numpy
  - concepto_objetos_resultado
draft: false
---

# scipy.integrate.odeint — integrador clasico de EDO (interfaz antigua, LSODA)

Integra un sistema de **ecuaciones diferenciales ordinarias** de primer orden evaluando la solucion en un **array de instantes `t`** dado. Es la interfaz **historica** de SciPy para EDOs: envuelve el integrador LSODA de la libreria FORTRAN ODEPACK, que conmuta automaticamente entre metodos para problemas rigidos y no rigidos. Devuelve un `ndarray` con una fila por instante.

> [!warning] Interfaz antigua — usa `solve_ivp` en codigo nuevo
> `odeint` es la API previa. Para codigo nuevo se recomienda `solve_ivp`, que ofrece eventos, salida densa, eleccion explicita de metodo y un objeto-resultado homogeneo. `odeint` se mantiene por compatibilidad.

> [!important] Firma `func(y, t)` — estado primero (¡invertida!)
> Por defecto la funcion recibe **primero el estado y despues el tiempo**: `func(y, t)`. Esto es lo **contrario** a `solve_ivp`, que usa `f(t, y)`. Para reutilizar una funcion al estilo `solve_ivp` pasa `tfirst=True`, y entonces `odeint` la llamara como `func(t, y)`.

## Firma

```python
scipy.integrate.odeint(
    func,                # callable: func(y, t, *args) -> dy/dt  (estado primero)
    y0,                  # array_like, shape (n,): estado inicial (OBLIGATORIO)
    t,                   # array_like, shape (m,): instantes de salida (OBLIGATORIO)
    args=(),             # tuple: argumentos extra fijos para func/Dfun
    Dfun=None,           # callable | None: jacobiano d(func)/dy
    col_deriv=0,         # int: 1 si Dfun da derivadas por columnas
    full_output=0,       # int: 1 devuelve tambien un dict de diagnostico
    tfirst=False,        # bool: si True, func usa la firma func(t, y) (estilo solve_ivp)
    rtol=None,           # float: tolerancia relativa
    atol=None,           # float | array_like: tolerancia absoluta
    hmax=0.0, hmin=0.0,  # float: paso maximo / minimo (0 = automatico)
    mxstep=0,            # int: maximo de pasos internos por intervalo
) -> ndarray            # (o (ndarray, infodict) si full_output=1)
```

## Valor de retorno

Devuelve un `ndarray` de forma `(len(t), len(y0))`: **una fila por instante** de `t`, una columna por variable de estado.

| Salida | Tipo | Significado |
|--------|------|-------------|
| `y` | `ndarray (m, n)` | Solucion; fila `i` = estado en `t[i]`, columna `j` = variable `j` |
| `infodict` | `dict` | Solo si `full_output=1`: diagnostico (`nfe`, `nst`, `hu`, `tcur`, ...) |

> [!warning] Forma transpuesta respecto a solve_ivp
> `odeint` devuelve `(n_puntos, n_vars)`; `solve_ivp` devuelve `.y` con forma `(n_vars, n_puntos)`. La trayectoria de la primera variable es `y[:, 0]` en `odeint` pero `sol.y[0]` en `solve_ivp`.

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Integracion basica | `odeint(func, y0, t)` |
| Con parametros del modelo | `odeint(func, y0, t, args=(k, m))` |
| Con jacobiano analitico | `odeint(func, y0, t, Dfun=jac)` |
| Reutilizar firma `func(t, y)` | `odeint(func, y0, t, tfirst=True)` |
| Con diagnostico | `y, info = odeint(func, y0, t, full_output=1)` |

## Parametros en detalle

### `func` (obligatorio)

Callable que devuelve `dy/dt`, con firma `func(y, t)` por defecto (**estado primero**). Debe devolver un array_like de la misma longitud que `y0`. Conviene vectorizarla con NumPy; ver [[concepto_callbacks_vectorizados|callbacks de SciPy]]. Si `tfirst=True`, la firma pasa a `func(t, y)`.

```python
import numpy as np
from scipy.integrate import odeint

# Decaimiento exponencial dy/dt = -k*y  (estado primero)
def f(y, t):
    return -0.5 * y

t = np.linspace(0, 10, 200)
y = odeint(f, y0=[2.0], t=t)
y[-1, 0]          # → ~0.0135 (≈ 2*exp(-5))
```

### `y0` (obligatorio)

Estado inicial; su longitud `n` fija el numero de ecuaciones y el numero de columnas del resultado.

### `t` (obligatorio)

Array de instantes de salida. `t[0]` es el instante de `y0`; el resto son los puntos donde se devuelve la solucion. **No es un intervalo `(t0, tf)`** como el `t_span` de `solve_ivp`, sino la rejilla completa de salida. Debe ser monotono (creciente o decreciente).

### `args`

Tupla de parametros extra fijos pasados a `func` (y a `Dfun`) tras los argumentos posicionales. Para uno solo: `args=(k,)`.

### `tfirst`

Si `True`, `odeint` llama a la funcion como `func(t, y)` en lugar de `func(y, t)`. Es el puente directo para reutilizar una funcion escrita para `solve_ivp` sin reordenar argumentos.

```python
def f_tfirst(t, y):       # firma estilo solve_ivp
    return -0.5 * y
y = odeint(f_tfirst, [2.0], t, tfirst=True)
```

### `Dfun`

Jacobiano `d(func)/dy` opcional; acelera y estabiliza la integracion de sistemas rigidos. Respeta la misma convencion de orden de argumentos que `func` (y `tfirst`).

### `full_output`

Si `1`, devuelve `(y, infodict)`. El diccionario incluye contadores utiles para diagnostico: `nfe` (evaluaciones de `func`), `nst` (pasos), `hu` (ultimo paso usado), entre otros.

### `rtol` / `atol`

Tolerancias relativa y absoluta del control de error. `atol` admite un array (una por variable) cuando los estados tienen magnitudes dispares.

## Casos de uso

### Caida con rozamiento (equivalente al ejemplo de solve_ivp)

```python
import numpy as np
from scipy.integrate import odeint

g, c, m = 9.81, 0.5, 2.0
def caida(y, t):          # OJO: estado primero
    v = y[0]
    return [g - (c/m) * v]

t = np.linspace(0, 20, 200)
y = odeint(caida, y0=[0.0], t=t)
y[-1, 0]          # → velocidad terminal ≈ m*g/c = 39.24 m/s
```

### Sistema depredador-presa (Lotka-Volterra, con `args`)

```python
def lotka(y, t, a, b, c, d):
    presa, depred = y
    return [a*presa - b*presa*depred,
            -c*depred + d*presa*depred]

t = np.linspace(0, 50, 1000)
y = odeint(lotka, [10, 5], t, args=(1.0, 0.1, 1.5, 0.075))
y[:, 0]           # poblacion de presas (columna 0)
y[:, 1]           # poblacion de depredadores (columna 1)
```

### Migracion desde solve_ivp

El mismo problema, mostrando los **dos puntos que cambian**: la firma de la funcion y la forma del retorno.

```python
# --- solve_ivp ---  f(t, y);  .y es (n_vars, n_puntos)
from scipy.integrate import solve_ivp
def f_ivp(t, y):  return [-0.5 * y[0]]
sol = solve_ivp(f_ivp, (0, 10), [2.0], t_eval=t)
traj_ivp = sol.y[0]          # fila 0

# --- odeint ---   func(y, t);  retorno es (n_puntos, n_vars)
def f_odeint(y, t):  return [-0.5 * y[0]]
out = odeint(f_odeint, [2.0], t)
traj_odeint = out[:, 0]      # columna 0

# Atajo: reutilizar la funcion de solve_ivp tal cual con tfirst=True
out2 = odeint(f_ivp, [2.0], t, tfirst=True)
```

Las dos confusiones tipicas al portar son: dejar la firma `f(t, y)` sin `tfirst=True` (estado y tiempo cruzados) e indexar el retorno como si fuera `.y` de `solve_ivp` (la forma esta transpuesta).

## Buenas practicas

1. Para codigo nuevo prefiere `solve_ivp`; reserva `odeint` para mantener codigo existente.
2. Ten siempre presente la firma `func(y, t)`: **estado primero**, salvo que actives `tfirst=True`.
3. Recuerda que `t` es la **rejilla de salida completa**, no un par `(t0, tf)`.
4. Indexa el resultado como `y[:, j]` para extraer la variable `j` (forma `(m, n)`).
5. Usa `full_output=1` para diagnosticar integraciones lentas o que no convergen.
6. Pasa parametros via `args`; proporciona `Dfun` en sistemas rigidos cuando sea posible.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Resultados sin sentido | Firma `func(t, y)` sin `tfirst=True` | Usar `func(y, t)` o pasar `tfirst=True` |
| Indexar `y[i]` esperando una variable | El retorno es `(n_puntos, n_vars)` | La variable `j` es `y[:, j]` |
| `Excess work done` / integracion estancada | Sistema muy rigido o `mxstep` bajo | Subir `mxstep`, dar `Dfun`, o migrar a `solve_ivp` con `BDF` |
| Pasar `(t0, tf)` como `t` | Se confunde con el `t_span` de `solve_ivp` | `t` debe ser el array completo de instantes |
| `TypeError: func() missing args` | Parametros no inyectados | Pasar `args=(p1, p2)` (tupla) |
| Esperar un objeto con `.t`/`.y` | `odeint` devuelve un ndarray, no un Bunch | Usar indexado de array; para objeto-resultado usar `solve_ivp` |

## Limitaciones

- Solo resuelve sistemas de **primer orden**; las EDOs de orden superior deben reescribirse como sistema.
- **No tiene deteccion de eventos** ni salida densa continua; para eso usar `solve_ivp`.
- El metodo es fijo (LSODA); no se puede elegir explicitamente otro integrador como en `solve_ivp`.
- El retorno es un `ndarray` plano sin metadatos de exito/estado; el diagnostico requiere `full_output=1`.

## Notas relacionadas

- [[scipy.integrate.solve_ivp]]
- [[concepto_callbacks_vectorizados]]
- [[concepto_objetos_resultado]]
