---
title: rcParams — Configuración global de matplotlib
aliases:
  - rcParams
  - configuracion global
  - matplotlib settings
tags:
  - matplotlib
  - api/config
  - config/global
lib: matplotlib
tipo: config
muta_estado: true
draft: false
---

# rcParams — Configuración global de matplotlib

## Acceso

`rcParams` es un diccionario global que controla los defaults de matplotlib.

```python
import matplotlib as mpl
import matplotlib.pyplot as plt

# Ver todos los parámetros
mpl.rcParams.keys()

# Ver un parámetro específico
print(plt.rcParams["figure.dpi"])
```

## Modificar parámetros

### Individualmente

```python
plt.rcParams["figure.dpi"] = 120
plt.rcParams["font.size"] = 12
plt.rcParams["lines.linewidth"] = 1.5
plt.rcParams["axes.grid"] = True
```

### Múltiples parámetros a la vez

```python
plt.rcParams.update({
    "figure.figsize": (8, 5),
    "font.size": 12,
    "axes.grid": True,
    "grid.alpha": 0.3
})
```

## Parámetros comunes

| Parámetro | Valor por defecto | Descripción |
|-----------|------------------|-------------|
| `figure.figsize` | `[6.4, 4.8]` | Tamaño de figura en pulgadas |
| `figure.dpi` | `100.0` | Resolución de pantalla |
| `figure.facecolor` | `'white'` | Color de fondo de figure |
| `axes.facecolor` | `'white'` | Color de fondo de axes |
| `axes.grid` | `False` | Grid activado por defecto |
| `axes.labelsize` | `'medium'` | Tamaño de etiquetas |
| `xtick.labelsize` | `'medium'` | Tamaño de ticks en X |
| `ytick.labelsize` | `'medium'` | Tamaño de ticks en Y |
| `lines.linewidth` | `1.5` | Grosor de línea por defecto |
| `lines.markersize` | `6.0` | Tamaño de marcador por defecto |
| `savefig.dpi` | `'figure'` | DPI al guardar (`'figure'` usa figure.dpi) |
| `savefig.bbox` | `'standard'` | Área guardada (`'tight'` recorta bordes) |

## Archivo matplotlibrc

Para mantener configuración persistente entre sesiones:

```bash
# Ubicación: ~/.config/matplotlib/matplotlibrc
```

Contenido del archivo:

```ini
figure.figsize: 8, 5
font.size: 12
axes.grid: True
grid.alpha: 0.3
```

> [!note] rcParams es para defaults globales  
> No usar rcParams para ajustes de una figura específica. En ese caso, pasar argumentos directamente a las funciones.

## Restaurar valores por defecto

```python
plt.rcParams.update(plt.rcParamsDefault)
```

## Notas relacionadas

- [[plt.style.use]]
- [[pyplot.introduccion]]
