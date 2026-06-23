---
title: ndarray.copy — copia profunda con buffer propio e independiente
aliases:
  - copy
  - ndarray.copy
tags:
  - numpy
  - api/metodo
  - memoria
lib: numpy
mod: np.ndarray
obj: ndarray
tipo: metodo
retorna: ndarray
inplace: false
requiere:
  - concepto_views_vs_copias
  - concepto_contiguidad_memoria
draft: false
---

# ndarray.copy — copia profunda con buffer propio e independiente

`copy` duplica el array en un **buffer de memoria nuevo**, totalmente independiente del original: mismo shape, mismo dtype, mismos valores, pero datos físicos distintos. Es la operación que **rompe el aliasing** — escribir en la copia nunca afecta al array de origen ni al revés. Es la contracara de [[ndarray.view]] (que comparte el buffer) y la herramienta para materializar una [[concepto_views_vs_copias|vista]] cuando se necesita que sobreviva o que sea segura de mutar.

## La idea

`copy` **materializa** los datos del array en memoria nueva. A diferencia de una vista, que reutiliza el buffer del original cambiando solo los metadatos, `copy` reserva un buffer propio y lo rellena con los valores actuales.

$$ \texttt{ndarray}\ \big[\text{buffer}=B\big] \ \xrightarrow{\ \texttt{copy}()\ }\ \texttt{ndarray}\ \big[\text{buffer}=B'\ \text{nuevo, independiente}\big] $$

Tras la copia se cumple `c.base is None` y `c.flags.owndata == True`: la copia **posee** su buffer. El coste es proporcional al tamaño del array (a diferencia de una vista, que es constante).

## Firma

```python
ndarray.copy(order='C') -> ndarray
```

## Los parámetros en detalle

### `order` — disposición en memoria de la copia

Único parámetro. Fija el layout del buffer nuevo (ver [[concepto_contiguidad_memoria|contigüidad]]). El defecto es `'C'` (a diferencia de `np.copy`, cuyo defecto es `'K'`):

| `order` | Resultado |
|---------|-----------|
| `'C'` (defecto) | C-contiguo (por filas) |
| `'F'` | F-contiguo (por columnas) |
| `'A'` | `'F'` si el origen es F-contiguo, si no `'C'` |
| `'K'` | conserva el layout del origen lo más posible |

```python
a = np.arange(6).reshape(2, 3)
a.copy('F').flags['F_CONTIGUOUS']   # True  → copia en orden columnas
a.copy().flags['C_CONTIGUOUS']      # True  → defecto C, aunque 'a' no lo fuera
```

> [!note] `arr.copy()` frente a `np.copy(arr)`
> El método y la función hacen lo mismo, pero su `order` por defecto difiere: el método usa `'C'`, la función `'K'` (conserva el layout). Además `np.copy` no preserva subclases por defecto y el método sí.

## ¿Vista o copia?

**Siempre copia.** Es precisamente lo que la distingue del slicing y de [[ndarray.view]]. El array devuelto tiene buffer propio: `base is None`, `flags.owndata == True`, y `np.shares_memory(original, copia)` es `False`.

```python
import numpy as np
a = np.array([1, 2, 3])
c = a.copy()
c.base is None              # True   → no comparte
c.flags.owndata            # True
np.shares_memory(a, c)     # False
c[0] = 99
a[0]                       # 1      → el original queda intacto
```

Contraste directo con la vista:

| Aspecto | `copy()` | `view()` |
|---------|----------|----------|
| Buffer | nuevo, propio | compartido con el original |
| `base` | `None` | apunta al original |
| Coste | proporcional al tamaño | constante (solo cabecera) |
| Escribir afecta al original | nunca | sí |

## Valor de retorno

Un `ndarray` nuevo con el **mismo shape y dtype** que `self`, su propio buffer (layout según `order`) y los mismos valores en el momento de la copia.

| Entrada | Llamada | Salida |
|---------|---------|--------|
| `[1, 2, 3]` | `arr.copy()` | `[1, 2, 3]` con buffer nuevo |
| vista `arr[1:4]` | `vista.copy()` | datos materializados, independientes |
| `arr` C-contiguo | `arr.copy('F')` | mismos valores, F-contiguo |

> [!warning] Copia profunda del buffer, pero shallow para dtype `object`
> `copy` duplica el buffer, pero si el dtype es `object` copia las **referencias**, no los objetos apuntados. Para una copia verdaderamente recursiva de un array de objetos usa `copy.deepcopy` de la stdlib.

## Casos de uso

### Romper el aliasing: materializar una vista antes de mutarla

El motivo número uno para usar `copy`. Un slice es una vista; mutarlo corrompe el original.

```python
arr = np.arange(10)
sub = arr[::2]            # VISTA — modificar sub cambia arr
sub[0] = 999
arr[0]                    # 999  ← se modificó sin querer

safe = arr[::2].copy()    # COPIA — independiente de arr
safe[0] = -1
arr[0]                    # 999  ← intacto esta vez
```

### Devolver datos seguros desde una función

```python
def primeros(a):
    return a[:3].copy()   # el llamador puede mutar el resultado sin tocar 'a'
```

### Liberar un array grande conservando una porción

```python
grande = np.arange(1_000_000)
chico = grande[:10].copy()   # 10 elementos propios
del grande                   # se puede liberar: 'chico' no depende de él
```

### Ejemplo realista: proteger un array base entre iteraciones

```python
base = np.zeros((512, 512))     # estado de referencia
for paso in range(epochs):
    trabajo = base.copy()       # parte siempre del mismo punto
    trabajo += np.random.randn(512, 512)
    # ... base sigue en ceros, intacto
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Modificar el original sin querer | se usó una vista (slice), no `copy` | llamar `.copy()` explícito |
| Copia innecesaria en arrays grandes | copiar cuando solo se lee | usar una vista/slicing |
| Esperar copia recursiva de objetos | `copy` es shallow para dtype `object` | `copy.deepcopy` de Python |
| Asumir el mismo layout que el origen | el defecto del método es `'C'`, no `'K'` | pasar `order='K'` o `'A'` para conservarlo |

## Notas relacionadas

- [[concepto_views_vs_copias]] — el modelo vista/copia y cómo verificarlo
- [[concepto_contiguidad_memoria]] — qué significa el parámetro `order`
- [[ndarray.view]] — el opuesto: comparte el buffer en vez de duplicarlo
- [[ndarray.base]] — comprobar si un array posee o comparte su buffer
