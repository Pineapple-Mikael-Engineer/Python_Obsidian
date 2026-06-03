---
title: scipy.integrate.simpson — regla de Simpson sobre datos muestreados
aliases:
  - simpson
  - scipy.integrate.simpson
  - simps
  - regla de Simpson
tags:
  - scipy
  - api/funcion
  - integracion
lib: scipy
tipo: funcion
mod: scipy.integrate
retorna: float
requiere:
  - numpy
  - scipy.integrate.trapezoid
draft: false
---

# scipy.integrate.simpson — regla de Simpson sobre datos muestreados

Integra **datos ya muestreados** (un array `y` de valores tabulados) aplicando la **regla de Simpson** (interpolacion parabolica por tramos). NO recibe una funcion callable: recibe muestras. Las abscisas se dan via `x` (array de posiciones) o, si el muestreo es uniforme, via `dx` (espaciado). Devuelve un **float** (o un array si se reduce un eje de un arreglo nD). Para funciones suaves es mas preciso que `trapezoid`.

> Distincion clave: `simpson` integra un **array de muestras** `y` (datos ya tabulados, p.ej. una señal medida). `quad`/`dblquad` integran una **funcion callable**. Si tienes una funcion y no datos, usa `quad`.

## Firma

```python
scipy.integrate.simpson(
    y,             # array_like: valores muestreados a integrar
    x=None,        # array_like | None: abscisas de las muestras (no uniformes permitidas)
    dx=1.0,        # float: espaciado entre muestras (solo si x is None)
    axis=-1,       # int: eje a lo largo del cual integrar
) -> float
```

> Nota historica: hasta SciPy 1.6 esta funcion se llamaba `simps`. El nombre `simps` quedo **deprecado** y se eliminó en versiones recientes a favor de `simpson`. El parametro de manejo de intervalos pares (`even`) tambien fue deprecado y retirado.

## Valor de retorno

| Tipo | Significado |
|------|-------------|
| `float` | Integral aproximada del array completo (caso 1D) |
| `ndarray` | Si `y` es nD: integral a lo largo de `axis`, reduciendo esa dimension |

## Formas basicas de llamada

| Situacion | Llamada |
|-----------|---------|
| Muestreo uniforme con paso conocido | `simpson(y, dx=h)` |
| Abscisas explicitas (uniformes o no) | `simpson(y, x=x)` |
| Muestreo uniforme paso 1 | `simpson(y)` |
| Array nD, integrar un eje | `simpson(Y, x=x, axis=0)` |

## Parametros en detalle

### `y` (obligatorio)

Array de **valores ya muestreados** de la funcion a integrar. Es el dato central: `simpson` no evalua ninguna funcion, solo combina estos numeros. Tipicamente proviene de `y = f(x)` evaluado sobre una rejilla, o de mediciones.

```python
import numpy as np
from scipy.integrate import simpson

x = np.linspace(0, np.pi, 101)   # numero impar de puntos -> par de intervalos
y = np.sin(x)                    # datos muestreados
simpson(y, x=x)                  # → 2.0000   (∫ sin x dx en [0, pi])
```

### `x`

Abscisas de las muestras. Permite **espaciado no uniforme**. Si se da `x`, se ignora `dx`. Debe tener la misma longitud que `y` a lo largo de `axis`.

```python
x = np.array([0.0, 0.3, 0.7, 1.0])   # espaciado irregular
y = x**2
simpson(y, x=x)                       # → ~0.333   (∫ x^2 en [0,1] = 1/3)
```

### `dx`

Espaciado **uniforme** entre muestras, usado solo cuando `x is None`. Por defecto `1.0`.

```python
h = 0.01
x = np.arange(0, 1 + h, h)
simpson(np.exp(x), dx=h)    # → ~1.7183   (∫ e^x en [0,1] = e - 1)
```

### `axis`

Eje del array nD a lo largo del cual integrar. Util para integrar muchas series a la vez (p.ej. una columna por sensor).

### Numero par vs impar de muestras (par vs impar de intervalos)

Simpson requiere un **numero par de intervalos** (impar de puntos) para aplicarse limpiamente. Si el numero de intervalos es **impar** (numero par de puntos), SciPy no puede usar Simpson en todos los tramos: trata el ultimo intervalo de forma especial (combinacion con una correccion), lo que introduce una pequeña asimetria. Para maxima precision, procura un numero impar de muestras.

## Casos de uso

### Integrar una funcion evaluada en una rejilla fina

```python
import numpy as np
from scipy.integrate import simpson

x = np.linspace(0, 2, 201)
y = np.exp(-x**2)              # muestras de la gaussiana
area = simpson(y, x=x)        # area bajo la curva en [0, 2]
area                          # → ~0.8821
```

### Integrar una señal temporal muestreada (datos, no funcion)

```python
# Energia de una señal: ∫ v(t)^2 dt con muestreo uniforme a fs = 1000 Hz
fs = 1000.0
t = np.arange(0, 1.0, 1/fs)
v = np.sin(2*np.pi*5*t)            # señal medida
energia = simpson(v**2, dx=1/fs)  # → ~0.5
```

### Integrar varias series a la vez por eje

```python
# Matriz (n_sensores, n_muestras): integrar cada fila en el tiempo
Y = np.random.rand(4, 101)
t = np.linspace(0, 10, 101)
integrales = simpson(Y, x=t, axis=1)   # shape (4,)
```

## Buenas practicas

1. Usa `simpson` cuando tengas **datos muestreados**; si tienes una funcion callable, usa `quad` (mas preciso y con control de error).
2. Procura un **numero impar de muestras** (par de intervalos) para que Simpson se aplique sin correccion especial.
3. Pasa `x` si el muestreo es **no uniforme**; usa `dx` solo con paso constante.
4. Para funciones suaves, Simpson supera a `trapezoid`; con datos ruidosos o no suaves la ventaja desaparece y `trapezoid` puede ser preferible.
5. Usa `simpson`, no el antiguo `simps` (deprecado/eliminado).
6. Verifica que `len(x) == y.shape[axis]`; un desajuste lanza error.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Pasar una funcion como `y` | `simpson` espera un array, no un callable | Evaluar `y = f(x)` primero, o usar `quad` |
| `AttributeError: no attribute 'simps'` | `simps` fue deprecado/eliminado | Usar `simpson` |
| Resultado impreciso con pocos puntos | Muestreo grueso o intervalos impares | Mas muestras; numero impar de puntos |
| `ValueError` de longitudes | `x` e `y` no coinciden en `axis` | Igualar longitudes |
| Olvidar `dx` con paso != 1 | Por defecto `dx=1.0` escala mal el resultado | Pasar `dx` real o `x` |

## Limitaciones

- Solo integra **datos muestreados**; no evalua funciones ni estima error de integracion (no devuelve cota de error como `quad`).
- La precision depende del muestreo; no es adaptativa.
- Con numero impar de intervalos aplica una correccion que rompe la simetria del esquema.
- No maneja limites infinitos ni singularidades: eso es territorio de `quad`.

## Notas relacionadas

- [[scipy.integrate.trapezoid]]
- [[scipy.integrate.quad]]
- [[concepto_relacion_numpy]]
