---
title: ax.scatter — Diagrama de dispersión
aliases:
  - scatter
  - dispersión
  - puntos
tags:
  - matplotlib
  - axes
  - graficos
  - dispersion
draft: false
lib: matplotlib
obj: Axes
tipo: metodo
---

# ax.scatter — Diagrama de dispersión

## Firma

```python
Axes.scatter(
    x,
    y,
    s=None,
    c=None,
    marker=None,
    cmap=None,
    norm=None,
    vmin=None,
    vmax=None,
    alpha=None,
    linewidths=None,
    edgecolors=None,
    **kwargs
)
```

## Parámetros principales

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `x`, `y` | array-like (N,) | - | Coordenadas de los puntos |
| `s` | escalar o array (N,) | `20` | Tamaño del marcador (puntos cuadrados) |
| `c` | color, secuencia o array (N,) | `None` | Color de los puntos |
| `marker` | `str` | `'o'` | Estilo del marcador (ver [[marker]]) |
| `cmap` | `str` o `Colormap` | `None` | Mapa de colores para `c` numérico |
| `norm` | `Normalize` | `None` | Normalización para `c` |
| `vmin`, `vmax` | `float` | `None` | Límites para la normalización |
| `alpha` | `float` | `None` | Transparencia (0 a 1) |
| `linewidths` | escalar o array (N,) | `1.5` | Ancho del borde del marcador |
| `edgecolors` | color o `'face'` | `'face'` | Color del borde |

## Valor de retorno

```python
collection = ax.scatter(x, y)
```

Retorna un objeto `PathCollection` (una colección de marcadores). A diferencia de `ax.plot` que retorna una lista de `Line2D`, `scatter` retorna una sola colección que contiene todos los puntos.

### Modificación posterior

```python
scat = ax.scatter(x, y, c=z, cmap='viridis')

# Modificar propiedades de toda la colección
scat.set_alpha(0.7)
scat.set_cmap('plasma')
scat.set_array(nuevos_colores)  # cambiar colores
scat.set_offsets(nuevas_posiciones)  # mover puntos
scat.remove()  # eliminar del axes
```

### Métodos principales de PathCollection

| Método | Descripción |
|--------|-------------|
| `set_offsets()` | Cambia posiciones de los puntos |
| `set_array()` | Cambia valores para colorear |
| `set_cmap()` | Cambia mapa de colores |
| `set_alpha()` | Cambia transparencia |
| `set_edgecolors()` | Cambia color de bordes |
| `set_facecolors()` | Cambia color de relleno |
| `set_sizes()` | Cambia tamaños |
| `remove()` | Elimina del gráfico |

## Tamaño de puntos (s)

### Tamaño constante

```python
ax.scatter(x, y, s=50)  # todos del mismo tamaño
```

### Tamaño variable (por punto)

```python
sizes = 20 * np.random.rand(100)  # array de 100 tamaños
ax.scatter(x, y, s=sizes)
```

> [!note] El valor `s` está en **puntos cuadrados** (points^2). Un punto cuadrado de 100 es un cuadrado de 10x10 puntos.

## Color de puntos (c)

### Color único

```python
ax.scatter(x, y, c='red')
ax.scatter(x, y, c='#FF5733')
```

### Color por categoría (string)

```python
categorias = ['grupo1', 'grupo2', 'grupo1', 'grupo3']
colores = {'grupo1': 'blue', 'grupo2': 'red', 'grupo3': 'green'}
c_colores = [colores[cat] for cat in categorias]
ax.scatter(x, y, c=c_colores)
```

### Color por valor numérico (con colormap)

```python
valores = np.random.rand(100)  # valores entre 0 y 1
scat = ax.scatter(x, y, c=valores, cmap='viridis')
plt.colorbar(scat)  # añade barra de color
```

### Límites de color (vmin, vmax)

```python
ax.scatter(x, y, c=valores, cmap='coolwarm', vmin=0, vmax=1)
```

## Marcadores (marker)

```python
ax.scatter(x, y, marker='s')  # cuadrados
ax.scatter(x, y, marker='^')  # triángulos
ax.scatter(x, y, marker='D')  # diamantes
```

Ver [[marker]] para lista completa.

## Transparencia (alpha)

```python
ax.scatter(x, y, alpha=0.5)  # puntos semitransparentes
```

Útil cuando hay muchos puntos solapados.

## Bordes (edgecolors, linewidths)

```python
# Bordes negros gruesos, relleno azul
ax.scatter(x, y, facecolors='blue', edgecolors='black', linewidths=1.5)

# Solo bordes (sin relleno)
ax.scatter(x, y, facecolors='none', edgecolors='red', linewidths=2)

# Borde con color por defecto
ax.scatter(x, y, edgecolors='face')  # mismo color que relleno
```

## Casos comunes

### Dispersión básica

```python
ax.scatter(x, y, alpha=0.6)
```

### Burbujas (tamaño variable)

```python
sizes = areas * 100  # área proporcional a valor
ax.scatter(x, y, s=sizes, alpha=0.5)
```

### Mapa de calor 2D (color por densidad)

```python
scat = ax.scatter(x, y, c=densidad, cmap='hot', alpha=0.8)
plt.colorbar(scat, label='Densidad')
```

### Grupos con diferentes colores y marcadores

```python
grupo1 = datos[datos['grupo'] == 'A']
grupo2 = datos[datos['grupo'] == 'B']

ax.scatter(grupo1['x'], grupo1['y'], c='blue', marker='o', label='Grupo A')
ax.scatter(grupo2['x'], grupo2['y'], c='red', marker='s', label='Grupo B')
ax.legend()
```

### Puntos con bordes destacados

```python
ax.scatter(x, y, facecolors='lightblue', edgecolors='darkblue', linewidths=2, s=80)
```

## Diferencia entre plot y scatter

| Aspecto | `ax.plot` | `ax.scatter` |
|---------|-----------|--------------|
| Retorna | lista de `Line2D` | `PathCollection` |
| Tamaño variable | No (mismo marcador) | Sí (array `s`) |
| Color variable | No | Sí (array `c`) |
| Rendimiento (muchos puntos) | Más rápido | Más lento |
| Uso típico | Líneas, pocos puntos | Muchos puntos, variables visuales |

Para **miles de puntos**, `ax.plot` con marcador puede ser más rápido que `scatter`.

## Buenas prácticas

1. Usar `alpha` para puntos solapados (0.3 a 0.7)
2. Para más de 5000 puntos, considerar `plot` en lugar de `scatter`
3. Usar `colormap` secuencial (`'viridis'`, `'plasma'`) para datos ordenados
4. Usar `colormap` divergente (`'coolwarm'`, `'RdBu'`) para datos con punto cero
5. Añadir [[plt.colorbar]] cuando se usa `c` numérico
6. Usar `edgecolors='none'` para eliminar bordes si no son necesarios

## Errores comunes

| Error | Solución |
|-------|----------|
| `len(x) != len(y)` | Deben tener misma longitud |
| `s` con longitud diferente a `x` | `s` debe ser escalar o array de misma longitud |
| Colorbar no aparece | Guardar retorno `scat = ax.scatter(...)` y pasar a `plt.colorbar(scat)` |
| Marcadores con borde grueso y relleno transparente | Usar `facecolors='none'`, `edgecolors='red'` |
| Colormap no se aplica | `c` debe ser numérico, no string |

## Notas relacionadas

- [[ax.plot]]
- [[marker]]
- [[Colores_Nombres]]
- [[Colormaps]]
- [[plt.colorbar]]
- [[PathCollection]]
