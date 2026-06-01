---
title: Estilos de línea — Tipos de trazo (linestyle)
aliases:
  - Estilos_Linea
  - linestyle
  - estilos de linea
tags:
  - matplotlib
  - api/objeto
  - styling
lib: matplotlib
obj: linestyle
tipo: objeto
muta_estado: false
draft: false
---

# Estilos de línea — Tipos de trazo (linestyle)

## Qué es

Una **referencia** de los valores válidos para `linestyle` / `ls`, que define el patrón del trazo de una [[Line2D|línea]] (continua, discontinua, punteada…).

## Los estilos predefinidos

| Código corto | Nombre | Aspecto |
|--------------|--------|---------|
| `'-'` | `'solid'` | línea continua |
| `'--'` | `'dashed'` | guiones |
| `':'` | `'dotted'` | puntos |
| `'-.'` | `'dashdot'` | guion-punto |
| `''` / `'none'` | sin línea | solo marcadores |

```python
import matplotlib.pyplot as plt
ax = plt.gca()
ax.plot(x, y, linestyle='--')      # código corto
ax.plot(x, y, ls='dashed')         # nombre (equivalente)
ax.plot(x, y, ls='')               # sin línea (solo marcadores)
```

## Patrones personalizados (tuplas de guiones)

Para un trazo a medida se usa la forma `(offset, (on, off, on, off, ...))` en puntos:

```python
ax.plot(x, y, linestyle=(0, (5, 2)))        # 5 on, 2 off
ax.plot(x, y, linestyle=(0, (1, 1)))        # punteado fino
ax.plot(x, y, linestyle=(0, (3, 5, 1, 5)))  # guion-punto largo
```

## Grosor y unión con el color/marcador

`linestyle` se combina con `linewidth`/`lw`, `color` (ver [[Colores_Nombres]]) y `marker` (ver [[marker]]) para definir el aspecto completo de la línea. En el formato compacto de `ax.plot`, el estilo va junto al color y marcador: `'r--'` (rojo, discontinua), `'go:'` (verde, círculos, punteada).

```python
ax.plot(x, y, 'r--')               # fmt compacto
ax.plot(x, y, color='r', ls='--')  # equivalente explícito
```

## Buenas prácticas

1. Combina estilo + color para distinguir series cuando se imprime en **blanco y negro**.
2. Usa `ls='none'` con `marker='o'` para un gráfico de solo puntos sin recurrir a `scatter`.
3. Para patrones repetidos en muchas series, define un ciclo con `set_prop_cycle`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Línea sólida inesperada | código mal escrito (`'.-'` vs `'-.'`) | revisar el orden de los símbolos |
| No se ven los marcadores | falta `marker=` (el estilo solo afecta a la línea) | añadir `marker` |
| Tupla de dashes ignorada | formato incorrecto | usar `(offset, (on, off, ...))` |

## Notas relacionadas

- [[Colores_Nombres]]
- [[marker]]
- [[Line2D]]
- [[ax.plot]]
