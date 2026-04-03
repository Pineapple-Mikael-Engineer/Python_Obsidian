---
title: ax.set_xticks_yticks — Control de ticks
aliases:
  - set_xticks
  - set_yticks
  - ticks
  - ejes
  - ax.set_xticks_yticks
tags:
  - matplotlib
  - api/metodo
  - axes/formato
lib: matplotlib
obj: Axes
tipo: metodo
muta_estado: true
requiere: []
draft: false
---

# ax.set_xticks / ax.set_yticks — Control de ticks

## Firmas

```python
Axes.set_xticks(ticks, labels=None, minor=False, **kwargs)
Axes.set_yticks(ticks, labels=None, minor=False, **kwargs)
```

## Parámetros principales

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `ticks` | lista de `float` | - | Posiciones donde colocar los ticks |
| `labels` | lista de `str` | `None` | Etiquetas para cada tick |
| `minor` | `bool` | `False` | Si `True`, controla ticks menores |
| `**kwargs` | - | - | Propiedades de [[Text]] para etiquetas |

## Casos básicos

### Ticks automáticos (default)

```python
# matplotlib elige automáticamente
ax.plot(x, y)
```

### Ticks personalizados (posiciones)

```python
ax.set_xticks([0, 2, 4, 6, 8, 10])
ax.set_yticks([-1, 0, 1])
```

### Ticks personalizados con etiquetas

```python
ax.set_xticks([0, 5, 10])
ax.set_xticklabels(['Inicio', 'Mitad', 'Final'])

# forma moderna (recomendada)
ax.set_xticks([0, 5, 10], labels=['Inicio', 'Mitad', 'Final'])
```

## Ticks mayores y menores

```python
# Ticks mayores (principales)
ax.set_xticks([0, 2, 4, 6, 8, 10])

# Ticks menores (intermedios, más pequeños)
ax.set_xticks([1, 3, 5, 7, 9], minor=True)
```

## Personalización de etiquetas

### Rotación

```python
ax.set_xticklabels(['Ene', 'Feb', 'Mar', 'Abr'], rotation=45)
```

### Tamaño y color

```python
ax.set_xticks([0, 5, 10])
ax.set_xticklabels(['A', 'B', 'C'], fontsize=12, color='red')
```

### Con kwargs

```python
ax.set_xticks([0, 5, 10], labels=['A', 'B', 'C'], fontsize=12, rotation=45)
```

## Formato de ticks con locators y formatters

Para formatos avanzados (fechas, monedas, porcentajes), ver [[Locators]] y TickFormatters.

```python
import matplotlib.ticker as ticker

# Formato de porcentaje
ax.yaxis.set_major_formatter(ticker.PercentFormatter())

# Formato con decimales
ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
```

## Casos comunes

### Ocultar ticks

```python
ax.set_xticks([])  # sin ticks en X
ax.set_yticks([])  # sin ticks en Y
```

### Ticks en posiciones específicas con formato

```python
posiciones = [0, 30, 60, 90, 120]
etiquetas = ['0°', '30°', '60°', '90°', '120°']
ax.set_xticks(posiciones, labels=etiquetas, rotation=45)
```

### Ticks logarítmicos

```python
ax.set_xscale('log')
ax.set_xticks([1, 10, 100, 1000])
ax.get_xaxis().set_major_formatter(ticker.ScalarFormatter())
```

### Fechas como ticks

```python
import matplotlib.dates as mdates

ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
```

## Relación entre métodos

| Método | Propósito |
|--------|-----------|
| `set_xticks` / `set_yticks` | Definir **dónde** están los ticks |
| `set_xticklabels` / `set_yticklabels` | Definir **qué texto** muestran (obsoleto, usar `labels` en `set_xticks`) |
| `tick_params` | Estilo de ticks (tamaño, color, dirección) |
| `set_xlim` / `set_ylim` | Definir límites del eje (no los ticks) |

## Buenas prácticas

1. Usar `labels` dentro de `set_xticks` en lugar de `set_xticklabels` separado
2. Rotar etiquetas largas con `rotation` para evitar solapamiento
3. No sobrecargar con ticks (5-10 es legible, más de 15 es confuso)
4. Usar ticks menores solo cuando aporten información
5. Para fechas, usar `matplotlib.dates` en lugar de etiquetas manuales

## Errores comunes

| Error | Solución |
|-------|----------|
| `len(ticks) != len(labels)` | Deben tener la misma longitud |
| Ticks fuera del rango visible | Definir `set_xlim` antes o después, los ticks fuera no se muestran |
| Usar `set_xticklabels` sin `set_xticks` | No tiene efecto; definir primero las posiciones |
| Etiquetas rotadas se cortan | Usar `fig.tight_layout()` o aumentar márgenes |

## Notas relacionadas

- [[Locators]]
- [[ax.tick_params]]
