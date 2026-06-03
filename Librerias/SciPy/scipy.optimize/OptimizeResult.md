---
title: OptimizeResult — objeto-resultado de scipy.optimize (Bunch)
aliases:
  - OptimizeResult
  - scipy.optimize.OptimizeResult
  - resultado de optimizacion
tags:
  - scipy
  - api/clase
  - optimizacion
lib: scipy
tipo: clase
mod: scipy.optimize
requiere:
  - concepto_objetos_resultado
draft: false
---

# OptimizeResult — objeto-resultado de scipy.optimize (Bunch)

Objeto-resultado que devuelven la mayoria de rutinas de `scipy.optimize`: `minimize`, `minimize_scalar`, `root`, `least_squares`, `linprog`, etc. Es un **Bunch**: un contenedor que se comporta a la vez como diccionario y como objeto, de modo que cada dato se accede como **atributo** (`res.x`) o como **clave** (`res["x"]`). Agrupa el resultado principal con los metadatos de convergencia del algoritmo.

Esta nota documenta el objeto en si; el patron general de objetos-resultado de SciPy se trata en [[concepto_objetos_resultado]].

## Doble acceso: atributo y clave

```python
from scipy.optimize import minimize

res = minimize(lambda v: (v[0] - 3)**2, x0=[0.0])
res.x          # acceso por atributo (preferido, legible)  -> array([3.])
res["x"]       # acceso por clave (util si la clave es dinamica) -> array([3.])
res.keys()     # campos disponibles en este resultado concreto
print(res)     # repr legible con todos los campos y sus valores
```

> No todos los campos existen en todos los resultados: cada rutina expone los suyos. `res.keys()` o `print(res)` muestran que hay realmente en un resultado dado.

## Atributos clave

| Atributo | Tipo | Significado |
|----------|------|-------------|
| `x` | `ndarray` / `float` | **Resultado principal**: la solucion encontrada |
| `success` | `bool` | True si el algoritmo termino correctamente |
| `status` | `int` | Codigo numerico de terminacion (0 suele ser exito) |
| `message` | `str` | Descripcion legible del motivo de parada |
| `fun` | `float` / `ndarray` | Valor de la funcion objetivo en `x` (residuos en `least_squares`) |
| `jac` | `ndarray` | Gradiente / jacobiano en `x` (si el metodo lo expone) |
| `hess` / `hess_inv` | `ndarray` | Hessiano o su inversa aproximada (segun metodo) |
| `nit` | `int` | Numero de iteraciones realizadas |
| `nfev` | `int` | Evaluaciones de la funcion objetivo |
| `njev` | `int` | Evaluaciones del jacobiano/gradiente |
| `nhev` | `int` | Evaluaciones del hessiano |

> Campos especificos por rutina: `linprog` añade `slack` y `con`; `least_squares` añade `cost`, `optimality`, `active_mask`; `root` usa `x` como raiz. Usar `res.keys()` para descubrirlos.

## Regla de oro: comprueba `success` antes de usar `x`

> El campo principal (`x`) **solo es valido si `success` lo es**. Leer la solucion sin mirar la convergencia es el error numero uno en optimizacion numerica.

```python
res = minimize(objetivo, x0)
if not res.success:
    raise RuntimeError(f"No convergio: {res.message}")
usar(res.x)
```

Para `linprog`, ademas de `success`, conviene mirar `status` (2 = infactible, 3 = no acotado).

## Como inspeccionarlo

```python
print(res)              # vista completa: todos los campos y valores
list(res.keys())        # nombres de los campos presentes en ESTE resultado
res.get("slack")        # acceso seguro: None si la clave no existe
"jac" in res            # comprobar si un campo esta disponible
```

```text
# Ejemplo de print(res) para un minimize tipico:
  message: Optimization terminated successfully.
  success: True
   status: 0
      fun: 1.7e-16
        x: [ 3.000e+00]
      nit: 2
      jac: [ 0.000e+00]
 hess_inv: [[ 5.000e-01]]
     nfev: 8
     njev: 4
```

## Buenas practicas

1. Ramifica siempre con `if not res.success: ...` antes de leer `res.x`.
2. Accede por atributo (`res.x`) por legibilidad; usa `res["clave"]` solo cuando la clave sea dinamica.
3. Usa `print(res)` o `res.keys()` cuando no recuerdes que campos expone una rutina concreta.
4. Loguea `res.message` y `res.nit`/`res.nfev` al depurar convergencia lenta o fallida.
5. Para acceso opcional a campos que pueden no existir, usa `res.get("campo")` en vez de indexar directamente.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Usas `res.x` y los numeros son absurdos | No convergio; `res.success is False` | Comprobar `success`/`message`; ajustar `x0`/`method` |
| `res[0]` falla (KeyError / TypeError) | Es un Bunch, no una tupla ni lista | Acceder por nombre: `res.x` |
| Desempaquetas `x, ok = minimize(...)` | La rutina devuelve **un** objeto, no una tupla | `res = minimize(...)`; luego `res.x` |
| `AttributeError: 'OptimizeResult' has no attribute ...` | Ese campo no existe en esta rutina | `res.keys()` / `print(res)` para ver los disponibles |
| Ignoras `status` en `linprog` | `success` no distingue infactible vs no acotado | Revisar `res.status` (2/3) ademas de `success` |

## Limitaciones

- Es un **contenedor de datos**, no realiza calculos: solo agrupa salida y diagnostico.
- Los campos disponibles **dependen de la rutina y del metodo**; no hay un conjunto fijo garantizado mas alla de `x`/`success`/`status`/`message`.
- No todas las rutinas de `scipy.optimize` devuelven un `OptimizeResult`: `curve_fit` devuelve una **tupla** `(popt, pcov)`.

## Notas relacionadas

- [[concepto_objetos_resultado]]
- [[scipy.optimize.minimize]]
- [[scipy.optimize.minimize_scalar]]
- [[scipy.optimize.linprog]]
