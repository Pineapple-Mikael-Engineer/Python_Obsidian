---
title: plt.style.use — Estilos predefinidos
aliases:
  - style.use
  - estilos matplotlib
tags:
  - matplotlib
  - api/funcion
  - config/estilos
lib: matplotlib
obj: pyplot
tipo: funcion
retorna: None
muta_estado: true
draft: false
---

# plt.style.use — Estilos predefinidos

## Firma

```python
plt.style.use(style)
```

## Parámetros

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `style` | `str` o `list` | Nombre del estilo o lista de estilos a combinar |

## Estilos disponibles

```python
plt.style.use("ggplot")           # estilo similar a ggplot2 de R
plt.style.use("seaborn-v0_8")     # estilo seaborn
plt.style.use("classic")          # estilo clásico de matplotlib
plt.style.use("dark_background")  # fondo oscuro
plt.style.use("bmh")              # estilo Bayesian Methods for Hackers
```

Listar todos los estilos disponibles:

```python
print(plt.style.available)
```

## Uso temporal (contexto)

El estilo se aplica solo dentro del bloque `with`:

```python
with plt.style.context("dark_background"):
    fig, ax = plt.subplots()
    ax.plot(x, y)  # este gráfico usa estilo oscuro
# fuera del contexto, vuelve al estilo anterior
```

## Combinar múltiples estilos

```python
# Los estilos posteriores sobrescriben a los anteriores
plt.style.use(['ggplot', 'dark_background'])
```

## Notas relacionadas

- [[config.rcParams]]
- [[pyplot.introduccion]]