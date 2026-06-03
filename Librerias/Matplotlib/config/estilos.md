---
title: estilos — Hojas de estilo predefinidas
aliases:
  - estilos
  - style sheets
  - hojas de estilo

tags:
  - matplotlib
  - api/config
  - styling

# --- Clasificación ---
lib: matplotlib
obj: pyplot
mod: matplotlib.style
tipo: config

# --- Comportamiento ---
retorna: None
muta_estado: true

draft: false
---

# estilos — Hojas de estilo predefinidas

## Qué controla

Las **hojas de estilo** son colecciones de parámetros que cambian la apariencia global de las figuras (colores, fuentes, rejilla, fondo, ciclo de color) de una sola vez. Bajo el capó, cada estilo sobrescribe entradas de [[rcParams]]; aplicar uno con [[plt.style.use]] muta el estado global de matplotlib hasta que se cambie o reinicie. Sirven para dar consistencia visual sin configurar parámetro por parámetro.

## Estilos disponibles más usados

| Estilo | Aspecto |
|--------|---------|
| `'default'` | configuración base de matplotlib |
| `'classic'` | apariencia clásica (pre-2.0) |
| `'ggplot'` | inspirado en ggplot2 de R: fondo gris, rejilla blanca |
| `'seaborn-v0_8'` | paletas suaves estilo seaborn (familia con variantes) |
| `'seaborn-v0_8-darkgrid'` | seaborn con rejilla oscura |
| `'bmh'` | "Bayesian Methods for Hackers": limpio y editorial |
| `'dark_background'` | fondo negro, texto claro |
| `'fivethirtyeight'` | estilo del medio FiveThirtyEight, líneas gruesas |
| `'grayscale'` | escala de grises (impresión B/N) |
| `'fast'` | optimizado para renderizado rápido |

Listar todos los disponibles en tu instalación:

```python
import matplotlib.pyplot as plt
print(plt.style.available)
# → ['Solarize_Light2', 'bmh', 'dark_background', 'ggplot', ...]
```

## Formas de aplicar

| Forma | Efecto | Alcance |
|-------|--------|---------|
| `plt.style.use('ggplot')` | aplica un estilo | global, persistente |
| `plt.style.use(['ggplot', 'dark_background'])` | combina; el último gana | global, persistente |
| `with plt.style.context('bmh'):` | aplica solo dentro del bloque | temporal |
| editar [[rcParams]] tras `use` | ajuste fino encima del estilo | global |

## Casos de uso

### Aplicar un estilo a todo el script

```python
plt.style.use('ggplot')
fig, ax = plt.subplots()
ax.plot(x, y)        # ya usa fondo gris y rejilla del estilo
```

### Estilo temporal con context manager

```python
with plt.style.context('dark_background'):
    fig, ax = plt.subplots()
    ax.plot(x, y)    # solo este gráfico es oscuro
# fuera del with, vuelve al estilo previo
```

### Combinar estilos (composición)

```python
# base seaborn + ajustes oscuros encima
plt.style.use(['seaborn-v0_8', 'dark_background'])
```

### Estilo + ajuste fino manual

```python
plt.style.use('bmh')
plt.rcParams['figure.figsize'] = (10, 4)   # sobreescribe encima del estilo
```

### Estilo propio desde archivo

```python
plt.style.use('./mi_estilo.mplstyle')   # archivo con pares clave: valor
```

## Buenas prácticas

1. Aplica el estilo **antes** de crear figuras; cambiarlo después no reestiliza lo ya dibujado.
2. Usa `plt.style.context(...)` para no contaminar el estado global en notebooks.
3. Combina estilos en lista cuando quieras una base + overlay; recuerda que el último prevalece.
4. Para ajustes puntuales encima de un estilo, edita [[rcParams]] tras llamar a `use`.
5. Versiona un `.mplstyle` propio en el repo para reproducibilidad entre máquinas.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `OSError: 'seaborn'` no encontrado | nombres antiguos renombrados a `seaborn-v0_8*` | usa el nombre vigente de `plt.style.available` |
| El estilo "no se aplica" | se llamó después de crear la figura | aplica antes de `plt.subplots()` |
| Estilo persiste entre celdas | `use` es global y persistente | usa `with plt.style.context(...)` |
| Combinación con efecto inesperado | el último estilo de la lista sobrescribe | ordena la lista de menos a más prioritario |
| Colores propios ignorados | el estilo fija el `axes.prop_cycle` | pasa `color=` explícito o ajusta `rcParams` |

## Notas relacionadas

- [[plt.style.use]]
- [[rcParams]]
- [[Colores_Nombres]]
