---
title: scipy.optimize.least_squares — minimos cuadrados no lineales robustos
aliases:
  - least_squares
  - minimos cuadrados scipy
  - ajuste robusto residuos
tags:
  - scipy
  - api/funcion
  - optimize/ajuste
lib: scipy
tipo: funcion
mod: scipy.optimize
retorna: OptimizeResult
requiere:
  - numpy
draft: false
---

# scipy.optimize.least_squares — minimos cuadrados no lineales robustos

Minimiza `0.5 * sum(rho(fun(x)**2))` sobre una funcion de **residuos** `fun(x)` que devuelve el **vector de residuos** (no la suma de cuadrados). Es el motor de bajo nivel detras de `curve_fit`, pero expone control total de cotas, funcion de perdida robusta (`loss`), jacobiano y metodo. Usalo cuando necesitas ajustar con outliers, restringir parametros o resolver un sistema sobredeterminado que no es un simple `f(x, *p)` contra datos.

> A diferencia de `curve_fit`, **`fun` devuelve el vector de residuos** `r = modelo - datos`, y el resultado **es un OptimizeResult** (`.x`, `.cost`, `.fun`, `.jac`, `.success`).

## Firma

```python
scipy.optimize.least_squares(
    fun, x0, jac='2-point', bounds=(-inf, inf), method='trf',
    ftol=1e-08, xtol=1e-08, gtol=1e-08, x_scale=1.0,
    loss='linear', f_scale=1.0, diff_step=None, tr_solver=None,
    tr_options={}, jac_sparsity=None, max_nfev=None, verbose=0, args=(), kwargs={}
)
```

## Valor de retorno

Devuelve un objeto resultado (`OptimizeResult`) con, entre otros:

| Atributo | Tipo | Significado |
|----------|------|-------------|
| `x` | `ndarray` | Parametros optimos hallados |
| `cost` | `float` | Valor de la funcion de coste `0.5 * sum(rho(f^2))` en `x` |
| `fun` | `ndarray` | Vector de **residuos** evaluado en `x` |
| `jac` | `ndarray` / sparse | Jacobiano modificado en `x` |
| `grad` | `ndarray` | Gradiente del coste en `x` |
| `optimality` | `float` | Medida de optimalidad de primer orden (norma inf del gradiente proyectado) |
| `active_mask` | `ndarray` | Que cotas estan activas en la solucion |
| `nfev`, `njev` | `int` | Numero de evaluaciones de `fun` y del jacobiano |
| `status` | `int` | Codigo de razon de parada |
| `success` | `bool` | `True` si convergio segun una tolerancia |
| `message` | `str` | Descripcion textual de la parada |

## Formas basicas de llamada

```python
import numpy as np
from scipy.optimize import least_squares

# residuos de un modelo a*exp(-b*x) contra datos
def residuos(p, x, y):
    a, b = p
    return a * np.exp(-b * x) - y

x = np.linspace(0, 4, 50)
y = 2.5 * np.exp(-1.3 * x)

# 1) basico (method='trf' por defecto)
res = least_squares(residuos, x0=[1.0, 1.0], args=(x, y))
# res.x ≈ [2.5, 1.3], res.success == True

# 2) con cotas
res = least_squares(residuos, x0=[1, 1], args=(x, y), bounds=([0, 0], [10, 5]))

# 3) robusto a outliers
res = least_squares(residuos, x0=[1, 1], args=(x, y), loss='soft_l1', f_scale=0.1)
```

## Parametros en detalle

### `fun`
Callable que devuelve el **vector de residuos** `fun(x, *args, **kwargs) -> ndarray (m,)`, con `m >= n` (n = numero de parametros). El algoritmo minimiza la norma de ese vector; **no le pases la suma de cuadrados**. Vectoriza con NumPy: se evalua muchas veces.

### `x0`
Estimacion inicial de los parametros (array de longitud `n`). Como toda optimizacion local, condiciona la convergencia y el minimo alcanzado.

### `jac`
Como obtener el jacobiano `∂fun_i/∂x_j`: `'2-point'` (default, diferencias finitas), `'3-point'` (mas preciso, mas caro), `'cs'` (complex-step, muy preciso si `fun` lo admite) o un **callable** que devuelve la matriz `(m, n)`. Un jacobiano analitico acelera y estabiliza.

### `bounds`
Par `(low, high)` (escalares o arrays de longitud `n`). Soportado por `trf` y `dogbox`; **no** por `lm`.

### `method`

| Metodo | Descripcion | Bounds | Uso tipico |
|--------|-------------|--------|------------|
| `'trf'` | Trust Region Reflective (default) | si | Robusto, problemas grandes/dispersos, con cotas |
| `'dogbox'` | Region de confianza tipo dogleg con caja | si | Problemas pequeños con cotas |
| `'lm'` | Levenberg-Marquardt (via MINPACK) | no | Rapido en problemas sin cotas, bien condicionados |

### `loss`
Funcion de perdida `rho` que controla la **robustez a outliers** reescalando los residuos grandes:

| `loss` | Efecto | Cuando |
|--------|--------|--------|
| `'linear'` | Minimos cuadrados clasico (default) | Sin outliers, errores gaussianos |
| `'soft_l1'` | Transicion suave L2→L1 | Outliers moderados (recomendado general) |
| `'huber'` | Cuadratica cerca de 0, lineal lejos | Outliers, comportamiento bien estudiado |
| `'cauchy'` | Fuerte atenuacion de residuos grandes | Outliers severos |
| `'arctan'` | Atenuacion aun mas agresiva | Outliers extremos |

Solo `method='trf'` y `'dogbox'` admiten `loss` distinto de `'linear'` (`'lm'` solo soporta `'linear'`).

### `f_scale`
Valor de escala del margen entre residuos "inlier" y "outlier" para las perdidas robustas. Aproximadamente, residuos con `|r| > f_scale` se tratan como outliers. **Critico al usar `loss` robusto**: ajustalo al nivel de ruido esperado.

### `x_scale`
Escala caracteristica de cada parametro. `'jac'` la estima automaticamente desde el jacobiano; util cuando los parametros tienen ordenes de magnitud muy distintos.

### `args`, `kwargs`
Constantes extra inyectadas a `fun` (y a `jac` si es callable), igual que en el resto de rutinas de SciPy. `args` debe ser una tupla.

### `ftol`, `xtol`, `gtol`
Tolerancias de parada por cambio en el coste, en los parametros y en el gradiente, respectivamente.

## Casos de uso

### Ajuste resistente a outliers

```python
import numpy as np
from scipy.optimize import least_squares

def modelo(p, x):
    a, b, c = p
    return a * np.exp(-b * x) + c

def residuos(p, x, y):
    return modelo(p, x) - y

rng = np.random.default_rng(0)
x = np.linspace(0, 5, 60)
y = modelo([4, 1.2, 0.5], x) + 0.05 * rng.normal(size=x.size)
y[::10] += 3.0                      # inyecta outliers groseros

# minimos cuadrados clasico -> se deforma por los outliers
lin = least_squares(residuos, [3, 1, 0], args=(x, y), loss='linear')

# robusto -> ignora los outliers
rob = least_squares(residuos, [3, 1, 0], args=(x, y), loss='soft_l1', f_scale=0.1)
# rob.x ≈ [4.0, 1.2, 0.5]  (mucho mas cercano a la verdad que lin.x)
```

### Cotas fisicas y jacobiano analitico

```python
def jac(p, x, y):
    a, b, c = p
    e = np.exp(-b * x)
    J = np.empty((x.size, 3))
    J[:, 0] = e                      # d/da
    J[:, 1] = -a * x * e             # d/db
    J[:, 2] = 1.0                    # d/dc
    return J

res = least_squares(
    residuos, [3, 1, 0], jac=jac, args=(x, y),
    bounds=([0, 0, -1], [10, 5, 1]), method='trf',
)
# res.optimality pequeño y res.success == True indican buen ajuste
```

### Errores estandar de los parametros desde el jacobiano

`least_squares` no entrega `pcov`; se reconstruye desde `res.jac`:

```python
res = least_squares(residuos, [3, 1, 0], args=(x, y))
J = res.jac
dof = max(0, res.fun.size - res.x.size)
sigma2 = 2 * res.cost / dof                  # varianza residual estimada
cov = np.linalg.inv(J.T @ J) * sigma2
perr = np.sqrt(np.diag(cov))                 # σ de cada parametro (1σ)
```

## Buenas practicas

- Recuerda devolver **residuos**, no su suma de cuadrados.
- Para outliers, combina `loss` robusto con un `f_scale` acorde al ruido; sin `f_scale` adecuado, `loss` apenas cambia el resultado.
- Provee `jac` analitico cuando puedas: menos evaluaciones y mejor condicionamiento.
- Usa `x_scale='jac'` si los parametros tienen magnitudes dispares.
- Si solo ajustas `f(x, *p)` a datos limpios sin necesidad de `loss`/`jac` personalizados, `curve_fit` es mas comodo.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Resultado raro pese a buen `x0` | `fun` devuelve la suma de cuadrados, no el vector | Devuelve `modelo - datos` (vector de residuos) |
| `ValueError: ... bounds not supported` | `method='lm'` con `bounds` o `loss` robusto | Usa `method='trf'` o `'dogbox'` |
| `loss` robusto no cambia nada | `f_scale` mal escalado | Ajusta `f_scale` al orden del ruido de inliers |
| `res.success == False` | No convergio (mal `x0`, mal escalado) | Mejora `x0`, usa `x_scale='jac'`, revisa tolerancias |
| Ajuste lento | `fun` con bucles Python o jacobiano por diferencias caro | Vectoriza `fun`; aporta `jac` analitico |
| `m < n` | Menos residuos que parametros (subdeterminado) | Aporta mas datos/residuos |

## Limitaciones

- Optimizacion **local**: el minimo depende de `x0`.
- No devuelve matriz de covarianza directamente; hay que derivarla de `res.jac`.
- `method='lm'` no admite cotas ni perdidas robustas.
- Asume que `fun` es diferenciable (al menos numericamente) y razonablemente suave.

## Notas relacionadas

- [[scipy.optimize.curve_fit]]
- [[OptimizeResult]]
- [[concepto_objetos_resultado]]
- [[concepto_callbacks_vectorizados]]
- [[concepto_relacion_numpy]]
