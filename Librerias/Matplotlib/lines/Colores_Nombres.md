---
title: Colores — Formas de especificar un color en Matplotlib
aliases:
  - Colores_Nombres
  - colores
  - especificar color
tags:
  - matplotlib
  - api/objeto
  - styling
lib: matplotlib
obj: color
tipo: objeto
muta_estado: false
draft: false
---

# Colores — Formas de especificar un color en Matplotlib

## Qué es

Una **referencia** de las formas válidas de indicar un color en cualquier parámetro `color`, `c`, `facecolor`, `edgecolor`, etc. Matplotlib acepta varias notaciones intercambiables.

## Las notaciones de color

| Notación | Ejemplo | Descripción |
|----------|---------|-------------|
| Nombre CSS | `'red'`, `'skyblue'`, `'forestgreen'` | ~148 nombres con color |
| Letra corta | `'r'`, `'g'`, `'b'`, `'c'`, `'m'`, `'y'`, `'k'`, `'w'` | colores básicos |
| Ciclo por defecto | `'C0'`, `'C1'`, … `'C9'` | colores del ciclo actual (property cycle) |
| Hexadecimal | `'#1f77b4'`, `'#FF5733'` | RGB en hex |
| Hex con alfa | `'#1f77b480'` | RGB + transparencia |
| Tupla RGB | `(0.1, 0.2, 0.5)` | valores 0–1 |
| Tupla RGBA | `(0.1, 0.2, 0.5, 0.3)` | RGB + alfa |
| Gris | `'0.5'` | string numérico 0 (negro) – 1 (blanco) |
| Paleta Tableau | `'tab:blue'`, `'tab:orange'` | la paleta `tab10` por nombre |
| Paleta xkcd | `'xkcd:sky blue'` | nombres de la encuesta xkcd |

```python
import matplotlib.pyplot as plt
ax = plt.gca()
ax.plot(x, y, color='tab:blue')
ax.plot(x, y, color='#FF5733')
ax.plot(x, y, color=(0.2, 0.4, 0.6))
ax.plot(x, y, color='0.5')        # gris medio
```

## Los colores `C0`–`C9` (ciclo)

`'C0'` no es un color fijo: es el **primer color del ciclo activo** (cambia con el estilo, ver [[estilos]]). Útil para que la paleta sea coherente con el tema.

```python
ax.plot(x, y1, color='C0')   # 1er color del ciclo
ax.plot(x, y2, color='C1')   # 2o color del ciclo
```

## Transparencia: `alpha`

El canal alfa controla la opacidad (0 transparente, 1 opaco). Se puede dar aparte o en RGBA:

```python
ax.plot(x, y, color='red', alpha=0.3)
ax.plot(x, y, color=(1, 0, 0, 0.3))   # equivalente
```

## Buenas prácticas

1. Para series múltiples, deja que el **ciclo** asigne colores (no fijes uno a uno) o usa `'C0'`–`'C9'`.
2. Prefiere nombres `'tab:...'` o hex para colores reproducibles entre estilos.
3. Para mapear **datos** a color (no un color fijo), usa un colormap (ver [[Colormaps]]).
4. Cuida el contraste y la accesibilidad (daltonismo): la paleta `tab10` y `viridis` son seguras.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `Invalid RGBA argument` | tupla con valores 0–255 | usar valores 0–1 |
| Color inesperado con `'C0'` | depende del ciclo/estilo activo | fijar un color explícito si debe ser estable |
| `'0.5'` da gris, no error | string numérico = escala de grises | usar nombre o hex si querías otro |

## Notas relacionadas

- [[Estilos_Linea]]
- [[marker]]
- [[Colormaps]]
- [[estilos]]
