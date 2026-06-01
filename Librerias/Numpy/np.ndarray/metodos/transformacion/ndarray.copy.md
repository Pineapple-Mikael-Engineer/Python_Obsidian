---
title: ndarray.copy — Copia profunda independiente del array
aliases:
  - copy
  - ndarray.copy
tags:
  - numpy
  - api/metodo
  - memoria
lib: numpy
obj: ndarray
tipo: metodo
retorna: ndarray
inplace: false
draft: false
---

# ndarray.copy — Copia profunda independiente del array

## Firma del método

```python
ndarray.copy(order='C') -> ndarray
```

## Valor de retorno

Devuelve un `ndarray` con el **mismo shape y dtype** pero un **buffer de memoria propio e independiente** (ver [[concepto_views_vs_copias]]). Escribir en la copia nunca afecta al original. Su atributo `base` es `None` y `flags.owndata` es `True`.

| Entrada | Llamada | Salida |
|---------|---------|--------|
| `[1, 2, 3]` | `arr.copy()` | `[1, 2, 3]` buffer nuevo |
| vista `arr[1:4]` | `vista.copy()` | datos materializados, independientes |

```python
import numpy as np
a = np.array([1, 2, 3])
c = a.copy()
c.base is a          # None → no comparte
c.flags.owndata      # True
c[0] = 99
a[0]                 # 1  → el original queda intacto
```

## Contraste con view

`copy` y [[ndarray.view]] son opuestos: `view` comparte el buffer (barato, acoplado); `copy` lo duplica (costoso, independiente).

| Aspecto | `copy` | `view` |
|---------|--------|--------|
| Buffer | nuevo, propio | compartido con el original |
| `base` | `None` | apunta al original |
| Coste | proporcional al tamaño | constante (solo cabecera) |
| Escribir afecta al original | nunca | sí |

```python
a = np.arange(5)
v = a.view()    # comparte → v[0]=9 cambia a
c = a.copy()    # independiente → c[0]=9 no toca a
```

## Parámetros en detalle

### `order` — disposición en memoria de la copia

| `order` | Resultado |
|---------|-----------|
| `'C'` (defecto) | contigua por filas |
| `'F'` | contigua por columnas |
| `'A'` | `'F'` si el origen es F-contiguo, si no `'C'` |
| `'K'` | conserva el layout del origen lo más posible |

```python
a = np.arange(6).reshape(2, 3)
a.copy('F').flags['F_CONTIGUOUS']   # True → copia en orden columnas
```

## Casos de uso

### Materializar una vista o slice antes de liberar el original

```python
def primeros(a):
    return a[:3].copy()   # devuelve datos seguros, desligados de a
```

### Proteger el original de mutaciones

```python
base = np.zeros(5)
trabajo = base.copy()
trabajo += 1          # base sigue en ceros
```

### Romper memoria compartida tras un slice

```python
grande = np.arange(1_000_000)
chico = grande[:10].copy()   # 10 elementos propios; grande puede liberarse
```

## Buenas prácticas

1. Usa `copy` siempre que necesites **independencia garantizada** frente a mutaciones del original.
2. Para 1D aplanado con copia garantizada existe el atajo [[ndarray.flatten]].
3. Evita copias innecesarias en datos grandes: si solo lees, una vista basta.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Modificar el original sin querer | se usó una vista, no `copy` | llamar `.copy()` explícito |
| Copia innecesaria en arrays grandes | copiar cuando solo se lee | usar vista/slicing |
| Esperar que copie subobjetos `object` | `copy` es shallow para dtype object | usar `copy.deepcopy` de Python |

## Notas relacionadas

- [[concepto_views_vs_copias]]
- [[ndarray.view]]
- [[ndarray.flatten]]
- [[ndarray.base]]
