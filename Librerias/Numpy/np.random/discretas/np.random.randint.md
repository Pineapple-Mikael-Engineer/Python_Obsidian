---
title: np.random.randint — Enteros uniformes en [low, high)
aliases:
  - randint
  - random.randint
  - np.random.randint
tags:
  - numpy
  - api/funcion
  - aleatorio
lib: numpy
mod: np.random
tipo: funcion
retorna: ndarray | int
inplace: false
requiere:
  - concepto_shape
draft: false
---

# np.random.randint — Enteros uniformes en [low, high)

Genera enteros aleatorios con distribución **uniforme discreta**: todos los valores del rango son equiprobables. El intervalo es **semiabierto** `[low, high)` —el límite inferior se incluye y el **superior se EXCLUYE**, igual que `range()`—. Es la función de referencia para muestrear enteros (índices, tiradas de dado, etiquetas binarias) en la API clásica de NumPy.

## La idea

Cada muestra es una variable uniforme discreta sobre los $h - \ell$ enteros del rango $\{\ell, \ell+1, \dots, h-1\}$, donde $\ell$ = `low` y $h$ = `high`. Todos con la misma probabilidad:

$$ P(X = k) = \frac{1}{h - \ell} \qquad \text{para } k \in \{\ell, \ell+1, \dots, h-1\} $$

La media teórica es $\frac{\ell + (h-1)}{2}$. La clave operativa es que `high` **nunca aparece**: el soporte llega hasta `high - 1`. Para muestrear de un array concreto en vez de un rango de enteros, usa [[np.random.choice]].

## Firma

```python
np.random.randint(
    low,            # int | array_like[int]: inicio inclusivo (o fin si high=None)
    high=None,      # int | array_like[int] | None: fin EXCLUIDO
    size=None,      # int | tuple[int] | None: forma de la salida
    dtype=int,      # dtype entero del resultado
) -> ndarray | int
```

## Los parámetros en detalle

### `low` — límite inferior (o superior si `high` es `None`)

Si das **un solo argumento**, este actúa como `high` y el rango pasa a ser `[0, low)`. Si das dos, `low` es el inicio **inclusivo**.

```python
np.random.randint(5)        # [0, 5)  → 0,1,2,3,4
np.random.randint(2, 5)     # [2, 5)  → 2,3,4
```

Acepta `array_like` para vectorizar: cada posición usa su propio `low` (broadcasting con `high` y `size`).

### `high` — límite superior EXCLUIDO

El valor `high` **nunca** se genera. Para incluir un tope `N`, usa `high = N + 1`. Esta es la trampa nº 1 de la función.

```python
np.random.randint(1, 6)     # máximo posible: 5
np.random.randint(1, 6 + 1) # ahora el 6 sí es posible (1..6, un dado)
```

### `size` — forma de la salida

Entero o tupla que define el [[concepto_shape|shape]]. Con `None` devuelve un **escalar de Python**; con un valor, un `ndarray` de esa forma.

```python
np.random.randint(0, 100, size=4)       # (4,)
np.random.randint(0, 100, size=(3, 3))  # (3, 3)
```

### `dtype` — tipo entero de salida

Por defecto `int` (entero de plataforma). Puede ajustarse a tipos menores (`np.uint8`, `np.int16`...) para ahorrar memoria; el rango pedido debe caber en el tipo.

```python
np.random.randint(0, 256, size=5, dtype=np.uint8)
```

## size y la forma de salida

`size` se traslada **literalmente** al shape del array de salida; el rango `[low, high)` solo afecta a los **valores**, no a la forma:

$$ \texttt{size}=(n_0, n_1, \dots, n_{k-1}) \;\longrightarrow\; \texttt{shape} = (n_0, n_1, \dots, n_{k-1}) $$

```python
np.random.randint(0, 10, size=(2, 3, 4, 5)).shape       # (2, 3, 4, 5)   → 4D
np.random.randint(0, 10, size=(2, 3, 4, 5, 6)).shape    # (2, 3, 4, 5, 6) → 5D
```

Con `size=None` no hay eje alguno: el retorno es un entero suelto, no un array 0-d.

## Casos de uso

### Simular tiradas de dado

```python
dados = np.random.randint(1, 7, size=1000)   # 1000 tiradas de un d6 (high=7 excluido)
dados.mean()   # ≈ 3.5
```

### Generar máscaras o etiquetas binarias

```python
etiquetas = np.random.randint(0, 2, size=20)  # 0/1 aleatorios, [0, 2)
```

### Índices aleatorios para muestrear filas (con repetición)

```python
datos = np.arange(50).reshape(10, 5)
idx = np.random.randint(0, datos.shape[0], size=3)
muestra = datos[idx]   # 3 filas al azar (posible repetición)
```

> [!tip] Versión moderna: `rng.integers`
> La API recomendada desde NumPy 1.17 usa un `Generator` creado con [[np.random.default_rng]]. El método análogo es **`rng.integers`**, que por defecto también es **semiabierto** `[low, high)`, pero añade el parámetro **`endpoint`**: con `endpoint=True` el rango pasa a ser **cerrado** `[low, high]` (incluye `high`), evitando el clásico `high + 1`.
> ```python
> rng = np.random.default_rng(0)
> rng.integers(1, 7, size=5)                 # [1, 7)  → 1..6   (como randint)
> rng.integers(1, 6, size=5, endpoint=True)  # [1, 6]  → 1..6   (incluye el 6)
> ```

> [!warning] `random_integers` fue eliminada de la documentación
> La vieja `np.random.random_integers` usaba un rango **cerrado** `[low, high]` (inclusivo) y está **deprecada** desde NumPy 1.11; su entrada se **eliminó de la documentación** oficial. No la uses: para un rango semiabierto usa `randint`/`rng.integers`; para uno inclusivo, `randint(low, high + 1)` o `rng.integers(low, high, endpoint=True)`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| El tope nunca aparece | `high` es exclusivo | usar `high + 1`, o `rng.integers(..., endpoint=True)` |
| `ValueError: low >= high` | rango invertido o vacío | asegurar `low < high` |
| Confundir con `random_integers` | aquella incluía `high` (y fue eliminada) | preferir `randint` (`random_integers` fue eliminada) |
| Esperar floats | `randint` da enteros | usar [[np.random.uniform]] para reales |
| Desbordar el `dtype` | el rango no cabe en `uint8`/`int16` | ampliar el `dtype` |

## Notas relacionadas

- [[concepto_shape]] — `size` define la forma de salida
- [[np.random.default_rng]] — `rng.integers`, el reemplazo moderno con `endpoint`
- [[np.random.choice]] — muestrear de un array o sin reemplazo
- [[np.random.binomial]] · [[np.random.uniform]]
