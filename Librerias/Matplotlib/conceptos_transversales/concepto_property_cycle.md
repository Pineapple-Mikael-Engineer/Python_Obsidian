---
title: Property cycle — Colores y estilos automaticos por serie
aliases:
  - property cycle
  - prop_cycle
  - ciclo de propiedades
  - C0 C1 C2
tags:
  - matplotlib
  - concepto
  - styling
lib: matplotlib
tipo: concepto
requiere:
  - none
draft: false
---

# Property cycle — Colores y estilos automaticos por serie

## Definicion fundamental

Cuando dibujas **varias series sin especificar color**, Matplotlib no las pinta todas iguales: les asigna automaticamente colores (y, si lo configuras, estilos) **sucesivos de un ciclo**. Ese ciclo es el **property cycle**, guardado en `rcParams['axes.prop_cycle']`.

**Regla mental:** cada vez que un Axes dibuja una serie sin color explicito, avanza un paso en el ciclo y toma la siguiente combinacion. Por eso dos `ax.plot` seguidos salen de colores distintos **sin que lo pidas**.

## Por que existe

Sin el ciclo tendrias que asignar un color a mano a cada serie para distinguirlas. El property cycle da una **paleta por defecto coherente y diferenciable** (la paleta "tab10") y libera al usuario de la decision en el caso comun.

```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([1, 2, 3])      # color C0 (azul)
ax.plot([2, 3, 4])      # color C1 (naranja) — sin pedirlo
ax.plot([3, 4, 5])      # color C2 (verde)
```

## Los colores 'C0'..'C9'

Las cadenas `'C0'`, `'C1'`, ... `'C9'` **no son colores fijos**: son referencias *al ciclo*. `'C0'` significa "el primer color del prop_cycle actual". Si cambias el ciclo, cambian.

```python
ax.plot(x, y1, color="C0")   # primer color del ciclo
ax.plot(x, y2, color="C3")   # cuarto color del ciclo
```

| Sintaxis | Significado | Fijo o relativo |
|----------|-------------|-----------------|
| `'C0'..'C9'` | posicion N del ciclo | relativo al ciclo |
| `'red'`, `'#1f77b4'` | color literal | fijo (ver [[Colores_Nombres]]) |
| sin `color=` | siguiente del ciclo, auto-avanza | relativo |

## Como personalizarlo

| Alcance | Como | Efecto |
|---------|------|--------|
| Un solo Axes | `ax.set_prop_cycle(color=[...])` | ese subgrafo |
| Global (sesion) | `plt.rcParams['axes.prop_cycle'] = cycler(...)` | toda la figura nueva |
| Ciclar varias props | `cycler(color=[...]) + cycler(linestyle=[...])` | combina por pares |

```python
from cycler import cycler

# Ciclo solo de colores en este Axes
ax.set_prop_cycle(color=["#e41a1c", "#377eb8", "#4daf4a"])

# Combinar color Y estilo de linea: avanzan juntos
ax.set_prop_cycle(cycler(color=["r", "g", "b"]) +
                  cycler(linestyle=["-", "--", ":"]))
```

Para fijarlo en toda la sesion se edita [[rcParams]] (`'axes.prop_cycle'`).

## Suma vs producto de cyclers

| Operador | Resultado | Longitud |
|----------|-----------|----------|
| `cyclerA + cyclerB` | empareja 1-a-1 (zip) | requiere igual longitud |
| `cyclerA * cyclerB` | producto cartesiano | longitudes multiplicadas |

```python
# +  → (rojo,-), (verde,--), (azul,:)          3 combinaciones
# *  → (rojo,-), (rojo,--), (rojo,:), (verde,-)...  9 combinaciones
```

## Casos que confunden o que fallan

### El ciclo se reinicia por Axes, no por Figure

Cada Axes tiene su **propio cursor**. Dos subgrafos empiezan ambos en `C0`; no continuan la cuenta del otro.

```python
fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.plot(y)   # C0
ax2.plot(y)   # C0 tambien, no C1
```

### El ciclo solo avanza si NO das color

Pasar `color=` (literal o `'Cn'`) **no consume** un paso del ciclo automatico para la siguiente serie sin color. El cursor solo avanza con asignaciones automaticas.

### 'C0' no es siempre azul

Es azul con el ciclo por defecto, pero si has cambiado `prop_cycle`, `'C0'` es lo que ahora ocupe la primera posicion. No lo trates como un nombre de color fijo (para eso usa [[Colores_Nombres]]).

### set_prop_cycle resetea el cursor

Llamar a `ax.set_prop_cycle(...)` no solo cambia la paleta: **vuelve a empezar** desde la primera entrada.

## Relacion con otros conceptos

- [[Colores_Nombres]]
- [[rcParams]]
- [[concepto_artist]]
- [[concepto_color_mapping]]
