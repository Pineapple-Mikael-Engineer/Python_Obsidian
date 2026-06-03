---
title: scipy.integrate.solve_ivp — solucionador moderno de problemas de valor inicial (EDO)
aliases:
  - solve_ivp
  - scipy.integrate.solve_ivp
  - problema de valor inicial
tags:
  - scipy
  - api/funcion
  - edo
lib: scipy
tipo: funcion
mod: scipy.integrate
retorna: OdeResult
requiere:
  - numpy
  - concepto_objetos_resultado
draft: false
---

# scipy.integrate.solve_ivp — solucionador moderno de problemas de valor inicial (EDO)

Integra un sistema de **ecuaciones diferenciales ordinarias** de primer orden `dy/dt = f(t, y)` desde un estado inicial `y0`, sobre el intervalo `t_span = (t0, tf)`. Es la **interfaz recomendada** de SciPy para EDOs en codigo nuevo: ofrece varios metodos (no rigidos y rigidos), salida en puntos elegidos (`t_eval`), interpolacion continua (`dense_output`) y deteccion de eventos (`events`). Devuelve un objeto-resultado con `.t` y `.y`.

> [!important] Firma `f(t, y)` — tiempo primero
> La funcion del lado derecho recibe **primero el tiempo y despues el estado**: `f(t, y)`. Esto esta **invertido** respecto a `odeint`, que usa `f(y, t)`. Es el error de migracion mas comun entre ambas rutinas.

## Firma

```python
scipy.integrate.solve_ivp(
    fun,                 # callable: f(t, y, *args) -> dy/dt (array_like, shape (n,))
    t_span,              # 2-tupla (t0, tf): intervalo de integracion (OBLIGATORIO)
    y0,                  # array_like, shape (n,): estado inicial (OBLIGATORIO)
    method='RK45',       # str | OdeSolver: algoritmo de integracion
    t_eval=None,         # array_like | None: instantes donde almacenar la solucion
    dense_output=False,  # bool: si True, construye un interpolador continuo .sol
    events=None,         # callable | lista de callables: deteccion de cruces por cero
    vectorized=False,    # bool: fun evalua varias columnas de estado a la vez
    args=None,           # tuple | None: argumentos extra fijos para fun/events
    rtol=1e-3,           # float: tolerancia relativa
    atol=1e-6,           # float | array_like: tolerancia absoluta
    **options,           # opciones del metodo: max_step, first_step, jac, ...
) -> OdeResult
```

## Valor de retorno

Devuelve un `OdeResult` (Bunch, acceso por atributo). Campos mas usados:

| Campo | Tipo | Significado |
|-------|------|-------------|
| `t` | `ndarray (n_puntos,)` | Instantes de tiempo de la solucion |
| `y` | `ndarray (n_vars, n_puntos)` | Estado en cada instante; **una fila por variable** |
| `sol` | `OdeSolution \| None` | Interpolador continuo `sol(t)` si `dense_output=True` |
| `t_events` | `lista de ndarray` | Tiempos en que se dispararon los eventos |
| `y_events` | `lista de ndarray` | Estado en cada evento |
| `success` | `bool` | True si la integracion alcanzo `tf` (o un evento terminal) |
| `status` | `int` | 0 exito, 1 evento terminal, -1 fallo del integrador |
| `message` | `str` | Descripcion legible del motivo de parada |
| `nfev` | `int` | Evaluaciones de `fun` |
| `njev` / `nlu` | `int` | Evaluaciones de jacobiano / descomposiciones LU |

> [!warning] Forma de `.y`
> `y` tiene forma `(n_vars, n_puntos)`: cada **fila** es la trayectoria de una variable. Para graficar `y0` frente al tiempo se usa `sol.y[0]`. Esto difiere de `odeint`, que devuelve `(n_puntos, n_vars)` (transpuesto).

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Integracion basica | `solve_ivp(f, (0, 10), y0)` |
| Salida en instantes fijos | `solve_ivp(f, (0, 10), y0, t_eval=np.linspace(0, 10, 200))` |
| Problema rigido | `solve_ivp(f, (0, 10), y0, method='BDF')` |
| Solucion continua interpolable | `solve_ivp(f, (0, 10), y0, dense_output=True)` |
| Detener en un evento | `solve_ivp(f, (0, 10), y0, events=evento)` |
| Con parametros del modelo | `solve_ivp(f, (0, 10), y0, args=(k, m))` |

## Parametros en detalle

### `fun` (obligatorio)

Callable que devuelve `dy/dt`. Su firma es `f(t, y)`: escalar de tiempo primero, vector de estado despues. Debe devolver un array_like de la **misma longitud** que `y0`. Conviene escribirla vectorizada con NumPy, ya que se evalua muchas veces; ver [[concepto_callbacks_vectorizados|callbacks de SciPy]].

```python
import numpy as np
from scipy.integrate import solve_ivp

# Decaimiento exponencial dy/dt = -k*y
def f(t, y):
    return -0.5 * y

sol = solve_ivp(f, (0, 10), y0=[2.0])
sol.y[0, -1]      # → ~0.0135 (≈ 2*exp(-5))
```

### `t_span` (obligatorio)

Tupla `(t0, tf)` con el inicio y fin de la integracion. **No es un array de instantes**, solo los extremos (a diferencia del `t` de `odeint`). Si `tf < t0` la integracion va hacia atras en el tiempo.

### `y0` (obligatorio)

Estado inicial; su longitud `n` define el numero de ecuaciones. Para EDOs de orden superior se reescriben como sistema de primer orden (ver casos de uso).

### `method`

| Metodo | Tipo | Cuando usarlo |
|--------|------|---------------|
| `RK45` | Runge-Kutta 4(5), explicito | Default; problemas **no rigidos** de proposito general |
| `RK23` | Runge-Kutta 2(3), explicito | No rigido, baja precision / poco coste |
| `DOP853` | Runge-Kutta orden 8, explicito | No rigido, **alta precision** |
| `Radau` | Runge-Kutta implicito orden 5 | Problemas **rigidos** |
| `BDF` | Multipaso implicito (formulas de diferencias hacia atras) | Rigidos; admite `jac` |
| `LSODA` | Conmuta auto rigido/no rigido | Cuando no sabes si el sistema es rigido |

Si la integracion avanza con pasos diminutos o falla con tolerancias razonables, el sistema suele ser **rigido**: cambia a `Radau`, `BDF` o `LSODA`.

### `t_eval`

Array de instantes donde **almacenar** la solucion. No cambia el control de paso interno (el integrador elige sus pasos), solo los puntos devueltos en `.t` / `.y`. Todos deben caer dentro de `t_span`.

```python
t = np.linspace(0, 10, 100)
sol = solve_ivp(f, (0, 10), [2.0], t_eval=t)
sol.t.shape       # → (100,)
```

### `dense_output`

Si `True`, construye un interpolador continuo accesible en `sol.sol`, evaluable en cualquier instante (incluso entre pasos) sin reintegrar.

```python
sol = solve_ivp(f, (0, 10), [2.0], dense_output=True)
sol.sol(3.7)      # → estado interpolado en t=3.7
sol.sol(np.linspace(0, 10, 500))   # → ndarray (1, 500)
```

### `events`

Callable(s) `g(t, y)`; SciPy detecta donde `g` **cruza por cero**. Atributos opcionales por evento: `terminal=True` detiene la integracion al dispararse; `direction` filtra el sentido del cruce (+1 ascendente, -1 descendente). Los tiempos quedan en `.t_events`.

```python
def toca_suelo(t, y):
    return y[0]            # altura = 0
toca_suelo.terminal = True
toca_suelo.direction = -1  # solo de descenso

sol = solve_ivp(f_caida, (0, 100), [100.0, 0.0], events=toca_suelo)
sol.t_events[0]   # → instante de impacto
```

### `args`

Tupla de parametros extra inyectados a `fun` (y a los eventos) tras `(t, y)`, evitando closures. Para un solo parametro: `args=(k,)`.

### `rtol` / `atol`

Tolerancias relativa y absoluta del control de error por paso. Bajarlas aumenta la precision y el coste. `atol` admite un array (una tolerancia por variable), util cuando los estados tienen magnitudes muy distintas.

### `vectorized`

Si `True`, `fun` debe aceptar `y` con forma `(n, k)` (varias columnas de estado) y devolver `(n, k)`. Acelera metodos implicitos que estiman el jacobiano por diferencias finitas.

## Casos de uso

### Caida con rozamiento (EDO de primer orden)

```python
import numpy as np
from scipy.integrate import solve_ivp

# dv/dt = g - (c/m) v   (rozamiento lineal con la velocidad)
g, c, m = 9.81, 0.5, 2.0
def caida(t, y):
    v = y[0]
    return [g - (c/m) * v]

sol = solve_ivp(caida, (0, 20), y0=[0.0], t_eval=np.linspace(0, 20, 200))
sol.y[0, -1]      # → velocidad terminal ≈ m*g/c = 39.24 m/s
```

### Oscilador armonico amortiguado (2º orden como sistema)

Una EDO de 2º orden `x'' + 2ζω x' + ω² x = 0` se reescribe con estado `y = [x, x']`:

```python
w, zeta = 2.0, 0.1      # frecuencia natural y amortiguamiento
def oscilador(t, y):
    x, v = y
    return [v, -2*zeta*w*v - w**2 * x]

sol = solve_ivp(oscilador, (0, 30), y0=[1.0, 0.0],
                t_eval=np.linspace(0, 30, 600), method='RK45')
# sol.y[0] -> posicion x(t);  sol.y[1] -> velocidad x'(t)
```

### Sistema depredador-presa (Lotka-Volterra, con `args`)

```python
def lotka(t, y, a, b, c, d):
    presa, depred = y
    return [a*presa - b*presa*depred,
            -c*depred + d*presa*depred]

sol = solve_ivp(lotka, (0, 50), y0=[10, 5], args=(1.0, 0.1, 1.5, 0.075),
                dense_output=True, t_eval=np.linspace(0, 50, 1000))
sol.y[0]          # poblacion de presas a lo largo del tiempo
sol.sol(25.0)     # estado interpolado en t=25
```

## Buenas practicas

1. Comprueba `sol.success` (y `sol.message`) antes de usar `sol.y`.
2. Recuerda la firma `f(t, y)`: **tiempo primero**; al portar codigo de `odeint` esta es la causa numero uno de resultados erroneos.
3. Usa `t_eval` para obtener una rejilla de salida limpia sin alterar el control de paso interno.
4. Si la integracion es lentisima o falla, prueba un metodo rigido (`BDF`, `Radau`, `LSODA`).
5. Para muestrear o graficar suavemente entre pasos, activa `dense_output=True` y evalua `sol.sol(t)`.
6. Pasa parametros del modelo via `args`, no por variables globales ni closures.
7. Da `atol` por variable cuando los estados tengan escalas dispares.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Resultados sin sentido | Firma invertida `f(y, t)` (estilo `odeint`) | Usar `f(t, y)`: tiempo primero |
| `ValueError: t_eval ... outside t_span` | Instantes de `t_eval` fuera de `(t0, tf)` | Acotar `t_eval` dentro de `t_span` |
| Integracion lentisima / `status=-1` | Sistema rigido con metodo explicito | Cambiar a `BDF` / `Radau` / `LSODA` |
| Indexar `sol.y[:, k]` esperando una variable | `.y` es `(n_vars, n_puntos)` | La trayectoria de la variable `i` es `sol.y[i]` |
| `TypeError: f() missing args` | Parametros no inyectados | Pasar `args=(p1, p2)` (tupla) |
| `sol.sol is None` | No se activo el interpolador | Llamar con `dense_output=True` |

## Limitaciones

- Solo resuelve sistemas de **primer orden**; las EDOs de orden superior deben reescribirse como sistema.
- No es para EDOs algebraicas-diferenciales (DAE) ni con retardo (DDE).
- `t_eval` no mejora la precision: solo selecciona puntos de salida; el error lo controlan `rtol`/`atol`.
- La deteccion de eventos asume que `g(t, y)` es continua y cambia de signo en el cruce; raices tangenciales pueden pasarse por alto.

## Notas relacionadas

- [[scipy.integrate.odeint]]
- [[concepto_callbacks_vectorizados]]
- [[concepto_objetos_resultado]]
