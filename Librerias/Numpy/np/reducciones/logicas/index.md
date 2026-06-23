---
title: np/reducciones/logicas — reducciones lógicas y de conteo
tags:
  - numpy
  - indice
draft: false
---

# np/reducciones/logicas — reducciones lógicas y de conteo

Esta subcarpeta agrupa las **reducciones lógicas y de conteo**: las que toman una **máscara
booleana** (o cualquier array, tratando no-cero como `True`) y la **colapsan** a lo largo de un eje
para responder una pregunta sobre la condición. Todas comparten el mismo patrón de las reducciones:
el eje indicado en `axis` **desaparece** del shape (ver [[concepto_axis_parametro]]), pero en vez de
un total numérico devuelven un **bool** (`any`/`all`) o un **entero** (`count_nonzero`).

La idea central es **reducir una máscara booleana**: primero se construye la máscara con una
comparación vectorizada (`arr > 5`, `arr != 0`, `np.isnan(arr)`), y luego se reduce esa máscara a lo
largo de un eje para preguntar si **existe** alguno, si **todos** cumplen, o **cuántos** lo hacen.

```python
import numpy as np
M = np.array([[1, 0, 3],
              [0, 0, 6]])
mask = M > 0                  # máscara booleana (2, 3)

np.any(mask, axis=1)            # [ True,  True]  → ¿hay algún positivo por fila?
np.all(mask, axis=1)            # [False, False]  → ¿son todos positivos por fila?
np.count_nonzero(mask, axis=1)  # [2, 1]          → cuántos positivos por fila
```

## Tabla de decisión

| La pregunta | Función | Operación | Devuelve |
|---|---|---|---|
| ¿Hay **algún** verdadero? | [[np.any]] | OR ($\bigvee$) a lo largo del eje | `bool` / ndarray de bool |
| ¿Son **todos** verdaderos? | [[np.all]] | AND ($\bigwedge$) a lo largo del eje | `bool` / ndarray de bool |
| ¿**Cuántos** son verdaderos? | [[np.count_nonzero]] | suma de la indicatriz | `int` / ndarray de int |

> [!warning] El caso del eje vacío difiere
> `np.all` de un eje **vacío** es `True` (verdad vacua: todos los cero elementos cumplen), mientras
> que `np.any` de un eje vacío es `False`. `count_nonzero` de un eje vacío es `0`. Conviene tenerlo
> presente al reducir ejes que pueden tener tamaño 0.

## Notas de esta subcarpeta

| Función | Qué hace |
|---|---|
| [[np.any]] | ¿Hay algún elemento no-cero/True a lo largo del eje? Reducción **OR**. Devuelve `bool` (o ndarray de bool). El idioma para `(arr > 0).any(axis=1)`: "¿existe alguna celda que cumpla?". `NaN` cuenta como verdadero. |
| [[np.all]] | ¿Son todos los elementos no-cero/True a lo largo del eje? Reducción **AND**. Devuelve `bool`. OJO: `all` de un eje vacío es `True` (vacuamente). Útil para validar que toda una fila/lote cumple una condición. |
| [[np.count_nonzero]] | Cuenta cuántos elementos son no-cero/True a lo largo del eje. Devuelve `int` (o ndarray de int). EL idioma para contar condiciones (`np.count_nonzero(arr > 5, axis=0)`). Equivale a `np.sum(mask)` pero es más explícito y rápido (sin overflow). `axis` acepta int o tupla. |

## Notas relacionadas

- [[concepto_axis_parametro]] — el eje que se reduce desaparece del shape
- [[concepto_indexing]] — construir y aplicar máscaras booleanas
- [[concepto_vectorizacion]] — por qué la máscara reemplaza al bucle
- [[np.sum]] — sumar una máscara también **cuenta** (`True`=1), equivalente a `count_nonzero`
- [[np.nonzero]] · [[np.where]] — obtener las **posiciones** de los no-ceros, no solo contarlos
