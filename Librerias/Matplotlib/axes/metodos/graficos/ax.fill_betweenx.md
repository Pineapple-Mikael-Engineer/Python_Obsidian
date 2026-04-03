---
title: ax.fill_betweenx — Relleno horizontal entre curvas
aliases:
  - fill_betweenx
  - área horizontal
  - banda horizontal
  - ax.fill_betweenx
tags:
  - matplotlib
  - api/metodo
  - axes/metodos
lib: matplotlib
obj: Axes
tipo: metodo
muta_estado: true
requiere: []
draft: false
---






# ax.fill_betweenx — Relleno horizontal entre curvas


## Firma

```python
Axes.fill_betweenx(
    y,
    x1,
    x2=0,
    where=None,
    interpolate=False,
    step=None,
    **kwargs
)
```

## Parámetros principales

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `y` | array-like (N,) | - | Coordenadas Y |
| `x1` | array-like (N,) o escalar | - | Primera curva (valores X) |
| `x2` | array-like (N,) o escalar | `0` | Segunda curva (valores X) |
| `where` | array de bool (N,) | `None` | Rellenar solo donde `True` |
| `interpolate` | `bool` | `False` | Interpolar entre puntos where |
| `step` | `str` | `None` | Estilo escalonado: `'pre'`, `'post'`, `'mid'` |
| `**kwargs` | - | - | Propiedades de [[patches.Polygon]] |

## Valor de retorno

```python
poly = ax.fill_betweenx(y, x1, x2)
```

Retorna una **lista de objetos [[patches.Polygon]]** (similar a `ax.fill_between`). Cada polígono representa una región contigua de relleno.

### Modificación posterior

```python
polygons = ax.fill_betweenx(y, x1, x2, alpha=0.3, color='blue')

# Modificar propiedades
polygons[0].set_color('red')
polygons[0].set_alpha(0.5)
polygons[0].set_hatch('/')
```

Ver ax.fill_between para detalles completos de modificación.

## Diferencia clave con fill_between

| Aspecto | `fill_between` | `fill_betweenx` |
|---------|----------------|-----------------|
| Variable independiente | X (horizontal) | Y (vertical) |
| Relleno | Vertical (entre curvas en Y) | Horizontal (entre curvas en X) |
| Caso típico | Bandas de confianza | Intervalos horizontales |

```python
# Vertical: relleno entre y1 e y2 para cada x
ax.fill_between(x, y1, y2)

# Horizontal: relleno entre x1 y x2 para cada y
ax.fill_betweenx(y, x1, x2)
```

## Uso básico

### Relleno a la derecha de una curva

```python
ax.fill_betweenx(y, x, alpha=0.3)  # x2 = 0 por defecto
```

### Relleno entre dos curvas horizontales

```python
ax.fill_betweenx(y, x1, x2, alpha=0.3, color='gray')
```

### Banda horizontal de confianza

```python
media_x = np.cos(y)
std = 0.2 * np.ones_like(y)

ax.plot(media_x, y, color='blue')
ax.fill_betweenx(y, media_x - std, media_x + std, alpha=0.3, color='blue', label='±1σ')
```

## Parámetros de estilo (kwargs)

Mismos que ax.fill_between:

| Parámetro | Ejemplo | Descripción |
|-----------|---------|-------------|
| `color` / `facecolor` | `color='red'` | Color del relleno |
| `alpha` | `alpha=0.3` | Transparencia |
| `label` | `label='Banda'` | Etiqueta para ax.legend |
| `edgecolor` | `edgecolor='black'` | Color del borde |
| `linewidth` | `linewidth=0.5` | Grosor del borde |
| `hatch` | `hatch='/'` | Patrón de sombreado |

## where — relleno condicional

### Rellenar solo donde condición se cumple

```python
condition = x1 > x2
ax.fill_betweenx(y, x1, x2, where=condition, alpha=0.3, color='green')
ax.fill_betweenx(y, x1, x2, where=~condition, alpha=0.3, color='red')
```

### Ejemplo: positivo en verde, negativo en rojo

```python
y = np.linspace(0, 4*np.pi, 100)
x = np.sin(y)

ax.fill_betweenx(y, x, where=x > 0, color='green', alpha=0.3)
ax.fill_betweenx(y, x, where=x <= 0, color='red', alpha=0.3)
ax.plot(x, y, color='black')
```

## step — relleno escalonado horizontal

Similar a `ax.fill_between` pero aplicado al eje Y.

```python
y = [0, 1, 2, 3, 4]
x = [0, 2, 1, 3, 2]

ax.fill_betweenx(y, x, step='pre')
ax.fill_betweenx(y, x, step='post')
ax.fill_betweenx(y, x, step='mid')
```

## Casos comunes

### Banda horizontal de confianza

```python
mean_x = np.sin(y)
std = 0.1 + 0.1 * np.abs(y) / max(y)

ax.plot(mean_x, y, color='blue', label='Media')
ax.fill_betweenx(y, mean_x - std, mean_x + std, alpha=0.3, color='blue', label='±1σ')
ax.legend()
```

### Región a la derecha de una curva (área)

```python
ax.fill_betweenx(y, x, alpha=0.4, color='skyblue', label='Área a la derecha')
```

### Destacar región específica del eje Y

```python
region = (y >= 2) & (y <= 4)
ax.fill_betweenx(y, 0, x, where=region, alpha=0.4, color='yellow')
```

### Intervalo horizontal entre dos curvas

```python
ax.fill_betweenx(y, x_left, x_right, alpha=0.3, color='lightgreen', edgecolor='green', linewidth=0.5)
```

## Combinación con plot (orden de dibujo)

```python
fig, ax = plt.subplots()

# Primero el relleno (detrás)
ax.fill_betweenx(y, mean_x - std, mean_x + std, alpha=0.3, color='gray', zorder=1)

# Luego la línea (encima)
ax.plot(mean_x, y, color='black', linewidth=2, zorder=2)
```

## Relación entre fill_between y fill_betweenx

Ambos son complementarios. La elección depende de cuál es tu variable independiente:

| Variable independiente en X | Variable independiente en Y |
|-----------------------------|-----------------------------|
| Usar `fill_between` | Usar `fill_betweenx` |
| `y = f(x)` típico | `x = f(y)` o datos rotados |

### Transformación entre ambos

```python
# Estos dos son equivalentes (transponiendo datos)
ax.fill_between(x, y1, y2)
ax.fill_betweenx(y, x1, x2)  # con x1, x2 funciones de y
```

## Buenas prácticas

1. Usar `alpha` entre 0.2 y 0.4 para rellenos sutiles
2. Llamar `fill_betweenx` antes que `plot` o usar `zorder` explícito
3. Usar `label` con `_nolegend_` si no quieres que aparezca en leyenda
4. Para bandas horizontales de confianza, usar mismo color que la línea con alpha bajo
5. Verificar que `y` esté ordenado (ascendente o descendente) para mejor visualización

## Errores comunes

| Error | Solución |
|-------|----------|
| `y` y `x1` longitudes diferentes | Deben tener misma longitud N |
| Confundir `fill_between` con `fill_betweenx` | Recordar: `_betweenx` es para relleno horizontal (depende de Y) |
| Relleno cubre la línea | Llamar `fill_betweenx` antes que `plot` o usar `zorder` |
| `y` no está ordenado | Ordenar `y` y los datos correspondientes |
| Borde no deseado | Usar `edgecolor='none'` o `linewidth=0` |

## Notas relacionadas

- [[ax.fill_between]]
- [[ax.legend]]
- [[ax.plot]]
