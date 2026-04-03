---
title: ax.set_yticks — Control de ticks del eje Y
aliases:
  - set_yticks
  - ticks y
  - yticks
tags:
  - matplotlib
  - api/metodo
  - axes/formato
lib: matplotlib
obj: Axes
tipo: metodo
retorna: list
muta_estado: true
draft: false
---

# ax.set_yticks — Control de ticks del eje Y

## Firma

```python
Axes.set_yticks(ticks, labels=None, minor=False, **kwargs)
```

## Parámetros

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `ticks` | lista de `float` | - | Posiciones donde colocar los ticks |
| `labels` | lista de `str` | `None` | Etiquetas para cada tick |
| `minor` | `bool` | `False` | Si `True`, controla ticks menores |
| `**kwargs` | - | - | Propiedades de [[Text]] para etiquetas |

## Valor de retorno

Retorna una lista de objetos [[Text]] (uno por etiqueta).

## Uso básico

### Ticks automáticos (default)

```python
# matplotlib elige automáticamente
ax.plot(x, y)
```

### Ticks personalizados (posiciones)

```python
ax.set_yticks([-1, 0, 1])
```

### Ticks personalizados con etiquetas

```python
# forma antigua (obsoleta pero aún funciona)
ax.set_yticks([-1, 0, 1])
ax.set_yticklabels(['Bajo', 'Medio', 'Alto'])

# forma moderna (recomendada)
ax.set_yticks([-1, 0, 1], labels=['Bajo', 'Medio', 'Alto'])
```

## Ticks mayores y menores

```python
# Ticks mayores (principales)
ax.set_yticks([-1, 0, 1])

# Ticks menores (intermedios, más pequeños)
ax.set_yticks([-0.5, 0.5], minor=True)
```

## Personalización de etiquetas

### Rotación

```python
ax.set_yticks([-1, 0, 1])
ax.set_yticklabels(['Bajo', 'Medio', 'Alto'], rotation=45)
```

### Tamaño y color

```python
ax.set_yticks([-1, 0, 1])
ax.set_yticklabels(['A', 'B', 'C'], fontsize=12, color='blue')
```

### Con kwargs (forma moderna)

```python
ax.set_yticks([-1, 0, 1], labels=['A', 'B', 'C'], fontsize=12, rotation=45)
```

## Formato de ticks con locators y formatters

Para formatos avanzados (fechas, monedas, porcentajes), ver [[Locators]] y [[Formatters]].

```python
import matplotlib.ticker as ticker

# Formato de porcentaje
ax.yaxis.set_major_formatter(ticker.PercentFormatter())

# Formato con decimales
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
```

## Casos comunes

### Ocultar ticks

```python
ax.set_yticks([])  # sin ticks en Y
```

### Ticks en posiciones específicas con formato

```python
posiciones = [0, 25, 50, 75, 100]
etiquetas = ['0%', '25%', '50%', '75%', '100%']
ax.set_yticks(posiciones, labels=etiquetas)
```

### Ticks logarítmicos

```python
ax.set_yscale('log')
ax.set_yticks([0.1, 1, 10, 100])
ax.get_yaxis().set_major_formatter(ticker.ScalarFormatter())
```

### Fechas como ticks

```python
import matplotlib.dates as mdates

ax.yaxis.set_major_locator(mdates.YearLocator())
ax.yaxis.set_major_formatter(mdates.DateFormatter('%Y'))
```

## Relación con otros métodos

| Método | Propósito |
|--------|-----------|
| `set_yticks` | Definir **dónde** están los ticks |
| `set_yticklabels` | Definir **qué texto** muestran (obsoleto, usar `labels` en `set_yticks`) |
| [[ax.tick_params]] | Estilo de ticks (tamaño, color, dirección) |
| [[ax.set_ylim]] | Definir límites del eje (no los ticks) |

## Buenas prácticas

1. Usar `labels` dentro de `set_yticks` en lugar de `set_yticklabels` separado
2. Rotar etiquetas largas con `rotation` para evitar solapamiento
3. No sobrecargar con ticks (5-10 es legible, más de 15 es confuso)
4. Usar ticks menores solo cuando aporten información
5. Para fechas, usar `matplotlib.dates` en lugar de etiquetas manuales

## Errores comunes

| Error | Solución |
|-------|----------|
| `len(ticks) != len(labels)` | Deben tener la misma longitud |
| Ticks fuera del rango visible | Definir `set_ylim` antes o después, los ticks fuera no se muestran |
| Usar `set_yticklabels` sin `set_yticks` | No tiene efecto; definir primero las posiciones |
| Etiquetas rotadas se cortan | Usar `fig.tight_layout()` o aumentar márgenes |

## Notas relacionadas

- [[ax.set_xticks]]
- [[ax.tick_params]]
- [[ax.set_ylim]]
- [[ax.set_yscale]]
- [[Locators]]
- [[Formatters]]
- [[Text]]
