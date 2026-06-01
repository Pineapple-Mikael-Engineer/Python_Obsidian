---
title: np.savetxt — Guardar un array en texto
aliases:
  - savetxt
  - np.savetxt
tags:
  - numpy
  - api/funcion
  - io

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: None
inplace: false

# --- Dependencias ---
requiere:
  - concepto_shape

draft: false
---

# np.savetxt — Guardar un array en texto

## Firma de la función

```python
np.savetxt(
    fname,
    X,
    fmt='%.18e',
    delimiter=' ',
    newline='\n',
    header='',
    footer='',
    comments='# '
) -> None
```

## Valor de retorno

**No devuelve nada** (`None`): escribe el array `X` en un archivo de texto legible. Pareja de [[np.loadtxt]]. Pensado para arrays 1D o 2D.

```python
import numpy as np
X = np.array([[1, 2], [3, 4]])
np.savetxt('salida.csv', X, delimiter=',', fmt='%d')
```

## Parámetros en detalle

### `fname`, `X` — destino y datos

`X` debe ser 1D o 2D (arrays de mayor dimensión no se guardan bien en texto).

### `fmt` — formato numérico

Controla precisión y tipo: `'%d'` enteros, `'%.4f'` 4 decimales, `'%.18e'` notación científica (por defecto).

### `delimiter` — separador

`','` para CSV, `'\t'` para TSV.

### `header` — cabecera

Texto en la primera línea (prefijado con `comments`).

```python
np.savetxt('d.csv', X, delimiter=',', header='col1,col2', comments='')
```

## Casos de uso

### Exportar resultados a CSV

```python
np.savetxt('resultados.csv', np.column_stack([x, y]),
           delimiter=',', header='x,y', comments='', fmt='%.3f')
```

## Buenas prácticas

1. Ajusta `fmt` para no perder/exagerar precisión.
2. Para un CSV "limpio" (cabecera sin `#`), usa `comments=''`.
3. Para datos binarios eficientes y multidimensionales, usa [[np.save]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `Expected 1D or 2D array` | `X` tiene >2 dimensiones | aplanar o usar [[np.save]] |
| `#` antes de la cabecera | `comments` por defecto | `comments=''` |
| Archivo enorme/impreciso | `fmt` por defecto científico | usar `fmt='%.4f'` |

## Limitaciones

- Solo 1D/2D; texto ocupa más que binario y es más lento.

## Notas relacionadas

- [[concepto_shape]]
- [[np.loadtxt]]
- [[np.save]]
