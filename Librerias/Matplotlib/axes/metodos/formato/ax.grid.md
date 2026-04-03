---
title: ax.grid — Cuadrícula del gráfico
aliases:
  - grid
  - cuadrícula
  - rejilla

tags:
  - matplotlib
  - api/metodo
  - styling

# --- Clasificación ---
lib: matplotlib
obj: Axes
tipo: metodo

# --- Comportamiento ---
muta_estado: true

draft: false
---

# ax.grid — Cuadrícula del gráfico

## Firma

```python
Axes.grid(
    visible=None,
    which='major',
    axis='both',
    **kwargs
)
```

## Parámetros principales

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `visible` | `bool` | `None` | Activa (`True`) o desactiva (`False`) la cuadrícula |
| `which` | `str` | `'major'` | Qué ticks usar: `'major'`, `'minor'`, `'both'` |
| `axis` | `str` | `'both'` | Eje donde dibujar: `'x'`, `'y'`, `'both'` |
| `**kwargs` | - | - | Propiedades de línea (color, estilo, grosor, alpha) |

## Uso básico

### Activar cuadrícula

```python
ax.grid(True)  # activa
ax.grid(False) # desactiva
```

### Activar con estilo

```python
ax.grid(True, color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
```

## Parámetros de estilo (kwargs)

Los `**kwargs` se pasan a `Line2D`. Ver [[Estilos_Linea]].

| Parámetro | Ejemplo | Descripción |
|-----------|---------|-------------|
| `color` | `color='gray'` | Color de la línea |
| `linestyle` | `linestyle='--'` | Estilo: `'-'`, `'--'`, `':'`, `'-.'` |
| `linewidth` | `linewidth=0.5` | Grosor de la línea |
| `alpha` | `alpha=0.3` | Transparencia |

## which — ticks mayores o menores

### Solo ticks mayores (default)

```python
ax.grid(True, which='major')
```

### Solo ticks menores

```python
ax.grid(True, which='minor')
```

### Ambos con diferente estilo

```python
ax.grid(True, which='major', color='black', linewidth=1)
ax.grid(True, which='minor', color='gray', linewidth=0.5, linestyle=':')
```

## axis — cuadrícula por eje

### Solo eje X

```python
ax.grid(True, axis='x')
```

### Solo eje Y

```python
ax.grid(True, axis='y')
```

### Ambos (default)

```python
ax.grid(True, axis='both')
```

## Casos comunes

### Cuadrícula sutil por defecto

```python
ax.grid(True, alpha=0.3)
```

### Cuadrícula punteada en gris

```python
ax.grid(True, color='gray', linestyle=':', linewidth=0.8)
```

### Cuadrícula solo para valores enteros

Primero configurar ticks, luego grid:

```python
ax.set_xticks(range(0, 11, 2))
ax.grid(True, axis='x')
```

### Sin cuadrícula en X, sí en Y

```python
ax.grid(True, axis='y')
ax.grid(False, axis='x')  # explícitamente desactivar X
```

## Configuración global (rcParams)

Para activar cuadrícula por defecto en todas las figuras:

```python
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.color'] = 'gray'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.5
```

Ver [[Configuracion]].

## Buenas prácticas

1. Usar cuadrícula en análisis exploratorio (ayuda a leer valores)
2. Mantener estilo sutil (colores claros, alpha bajo) para no distraer
3. Usar `which='minor'` solo si los ticks menores aportan información
4. Activar por defecto con `rcParams` si trabajas en modo análisis
5. Para publicaciones, considerar omitir cuadrícula o usar estilos muy sutiles

## Errores comunes

| Error | Solución |
|-------|----------|
| Grid no visible | Verificar que `visible=True` y que `which` corresponda a ticks existentes |
| Grid en minor sin ticks menores | Definir ticks menores con `ax.set_xticks(..., minor=True)` o `AutoMinorLocator` |
| Líneas demasiado gruesas | Usar `linewidth=0.5` o menor |
| Color de grid opaca | Usar `alpha=0.3` a `0.7` para sutileza |

## Notas relacionadas

- [[ax.tick_params]]
- [[Locators]]
- [[Estilos_Linea]]
- [[Configuracion]]
- [[ax.set_xticks_yticks]]
