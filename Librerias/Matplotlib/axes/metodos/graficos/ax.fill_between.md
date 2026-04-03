---
title: fill_between — Relleno entre curvas
aliases:
  - fill_between
  - área sombreada
  - banda confianza
tags:
  - matplotlib
  - axes
  - graficos
  - relleno
draft: false
lib: matplotlib
obj: Axes
tipo: metodo
---

# fill_between — Relleno entre curvas

## Firma

```python
Axes.fill_between(
    x,
    y1,
    y2=0,
    where=None,
    interpolate=False,
    step=None,
    **kwargs
)
```

## Parámetros principales

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `x` | array-like (N,) | - | Coordenadas X |
| `y1` | array-like (N,) o escalar | - | Primera curva |
| `y2` | array-like (N,) o escalar | `0` | Segunda curva |
| `where` | array de bool (N,) | `None` | Rellenar solo donde `True` |
| `interpolate` | `bool` | `False` | Interpolar entre puntos where |
| `step` | `str` | `None` | Estilo escalonado: `'pre'`, `'post'`, `'mid'` |
| `**kwargs` | - | - | Propiedades de [[Polygon]] |

## Valor de retorno

```python
poly = ax.fill_between(x, y1, y2)
```

Retorna una **lista de objetos [[Polygon]]**. La longitud de la lista depende de cuántos polígonos contiguos se generan:

| Caso | Longitud de lista | Ejemplo |
|------|-------------------|---------|
| Relleno continuo sin `where` | 1 | `[Polygon]` |
| `where` con N regiones separadas | N | `[Polygon1, Polygon2, ...]` |
| `where` con valores `False` que dividen | número de regiones `True` | |

### Ejemplo con regiones separadas

```python
x = np.linspace(0, 10, 100)
y = np.sin(x)
condition = y > 0

polygons = ax.fill_between(x, 0, y, where=condition, alpha=0.3)
len(polygons)  # 3 (regiones donde seno positivo: 0-π, 2π-3π, 4π-5π)
```

### Modificación posterior del objeto Polygon

Cada `Polygon` se puede modificar después de creado usando sus métodos:

```python
polygons = ax.fill_between(x, y1, y2, alpha=0.3, color='blue')

# Acceder a un polígono específico
primer_poly = polygons[0]

# Modificar propiedades
primer_poly.set_color('red')
primer_poly.set_alpha(0.5)
primer_poly.set_hatch('/')  # patrón de sombreado
primer_poly.set_edgecolor('black')
primer_poly.set_linewidth(1.5)

# Ocultar/mostrar
primer_poly.set_visible(False)

# Eliminar del axes
primer_poly.remove()
```

### Métodos principales de Polygon

| Método | Descripción | Ejemplo |
|--------|-------------|---------|
| `set_color()` | Cambia color de relleno | `poly.set_color('green')` |
| `set_alpha()` | Cambia transparencia | `poly.set_alpha(0.6)` |
| `set_hatch()` | Cambia patrón de sombreado | `poly.set_hatch('x')` |
| `set_edgecolor()` | Cambia color del borde | `poly.set_edgecolor('black')` |
| `set_linewidth()` | Cambia grosor del borde | `poly.set_linewidth(2)` |
| `set_visible()` | Muestra u oculta | `poly.set_visible(False)` |
| `remove()` | Elimina del gráfico | `poly.remove()` |
| `get_xy()` | Obtiene vértices del polígono | `verts = poly.get_xy()` |
| `set_xy()` | Modifica vértices | `poly.set_xy(nuevos_vertices)` |

### Ejemplo de modificación dinámica

```python
fig, ax = plt.subplots()
x = np.linspace(0, 10, 100)
y = np.sin(x)

poly, = ax.fill_between(x, 0, y, alpha=0.3, color='blue')
line, = ax.plot(x, y, color='blue')

# Función de animación
def update(frame):
    y_new = np.sin(x + frame / 10)
    line.set_ydata(y_new)
    
    # Actualizar polígono
    vertices = poly.get_xy()
    vertices[:, 1] = np.concatenate([y_new, [0]])  # actualizar Y
    poly.set_xy(vertices)
    
    return line, poly
```

## Uso básico

### Relleno debajo de una curva

```python
ax.fill_between(x, y, alpha=0.3)  # y2 = 0 por defecto
```

### Relleno entre dos curvas

```python
ax.fill_between(x, y1, y2, alpha=0.3, color='gray')
```

### Banda de confianza (media ± desviación)

```python
media = np.sin(x)
std = 0.2 * np.ones_like(x)

ax.plot(x, media, color='blue')
ax.fill_between(x, media - std, media + std, alpha=0.3, color='blue', label='±1σ')
```

## Parámetros de estilo (kwargs)

Los `**kwargs` se pasan a `Polygon`.

| Parámetro | Ejemplo | Descripción |
|-----------|---------|-------------|
| `color` / `facecolor` | `color='red'` | Color del relleno |
| `alpha` | `alpha=0.3` | Transparencia (0 a 1) |
| `label` | `label='Banda'` | Etiqueta para [[ax.legend]] |
| `edgecolor` | `edgecolor='black'` | Color del borde |
| `linewidth` | `linewidth=0.5` | Grosor del borde |
| `linestyle` | `linestyle='--'` | Estilo del borde |
| `hatch` | `hatch='/'` | Patrón de sombreado (`'/'`, `'\\'`, `'x'`, `'-'`, `'|'`, `'+'`, `'o'`, `'.'`, `'*'`) |
| `zorder` | `zorder=1` | Orden de dibujo (menor = detrás) |

## where — relleno condicional

### Rellenar solo donde condición se cumple

```python
condition = y1 > y2
ax.fill_between(x, y1, y2, where=condition, alpha=0.3, color='green')
ax.fill_between(x, y1, y2, where=~condition, alpha=0.3, color='red')
```

### Efecto visual de interpolate

Sin `interpolate=True`, el relleno se detiene abruptamente en los bordes de `where`. Con `interpolate=True`, se interpola linealmente en los límites.

```python
# Sin interpolación (bordes verticales abruptos)
ax.fill_between(x, y1, y2, where=condition, interpolate=False)

# Con interpolación (transición suave)
ax.fill_between(x, y1, y2, where=condition, interpolate=True)
```

### Ejemplo: positivo en verde, negativo en rojo

```python
x = np.linspace(0, 4*np.pi, 100)
y = np.sin(x)

ax.fill_between(x, y, where=y > 0, color='green', alpha=0.3)
ax.fill_between(x, y, where=y <= 0, color='red', alpha=0.3)
ax.plot(x, y, color='black')
```

## step — relleno escalonado

Para datos discretos o histogramas. Controla dónde ocurre el cambio de valor.

| `step` | Comportamiento |
|--------|----------------|
| `'pre'` | El valor cambia antes del punto (escalón izquierdo) |
| `'post'` | El valor cambia después del punto (escalón derecho) |
| `'mid'` | El valor cambia en el punto medio entre muestras |

```python
x = [0, 1, 2, 3, 4]
y = [0, 2, 1, 3, 2]

fig, axs = plt.subplots(1, 3, figsize=(12, 4))
axs[0].fill_between(x, y, step='pre')
axs[0].set_title('step="pre"')
axs[1].fill_between(x, y, step='post')
axs[1].set_title('step="post"')
axs[2].fill_between(x, y, step='mid')
axs[2].set_title('step="mid"')
```

## Casos comunes

### Banda de confianza con línea media

```python
mean = np.sin(x)
std = 0.1 + 0.1 * np.abs(x) / max(x)

ax.plot(x, mean, color='blue', label='Media')
ax.fill_between(x, mean - std, mean + std, alpha=0.3, color='blue', label='±1σ')
ax.legend()
```

### Región debajo de una curva (área)

```python
ax.fill_between(x, y, alpha=0.4, color='skyblue', label='Área bajo curva')
```

### Destacar región específica del eje X

```python
region = (x >= 2) & (x <= 4)
ax.fill_between(x, 0, y, where=region, alpha=0.4, color='yellow')
```

### Sombreado con borde y hatch

```python
ax.fill_between(
    x, y1, y2,
    alpha=0.2,
    facecolor='lightblue',
    edgecolor='black',
    linewidth=0.5,
    hatch='/'
)
```

## Combinación con plot (orden de dibujo)

```python
fig, ax = plt.subplots()

# Primero el relleno (detrás)
ax.fill_between(x, mean - std, mean + std, alpha=0.3, color='gray', zorder=1)

# Luego la línea (encima)
ax.plot(x, mean, color='black', linewidth=2, zorder=2)
```

El orden de llamado importa, pero `zorder` es más explícito y robusto. Valores más altos = más arriba.

## Buenas prácticas

1. Usar `alpha` entre 0.2 y 0.4 para rellenos (no opacar la línea)
2. Llamar `fill_between` antes que `plot` o usar `zorder` explícito
3. Usar `label` con `_nolegend_` si no quieres que aparezca en leyenda
4. Para bandas de confianza, usar mismo color que la línea pero con alpha bajo
5. Usar `where` para destacar regiones de interés (positivo/negativo, umbrales)
6. Guardar referencia al retorno si se modificará después (animaciones, actualizaciones)
7. Para múltiples regiones separadas, acceder por índice a cada `Polygon`

## Errores comunes

| Error | Solución |
|-------|----------|
| `x` e `y1` longitudes diferentes | Deben tener misma longitud N |
| `where` con valores NaN o inf | Asegurar que where es booleano sin valores inválidos |
| Relleno cubre la línea | Llamar `fill_between` antes que `plot` o usar `zorder` |
| Borde no deseado | Usar `edgecolor='none'` o `linewidth=0` |
| `step` no funciona con `where` simultáneo | Usar `step` solo cuando no hay `where` |
| Modificar `Polygon` y no ver cambios | Llamar `fig.canvas.draw()` si es en tiempo real |
| Confundir `facecolor` con `color` | Ambos funcionan, pero `facecolor` es más explícito |

## Notas relacionadas

- [[ax.plot]]
- [[Polygon]]
- [[ax.legend]]
- [[ax.fill_betweenx]]
- [[Animacion]]
