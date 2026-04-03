---
title: ax.tick_params — Estilo de ticks
aliases:
  - tick_params
  - estilo ticks
  - personalizar ticks

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

# ax.tick_params — Estilo de ticks

## Firma

```python
Axes.tick_params(
    axis='both',
    **kwargs
)
```

## Parámetro axis

| Valor | Aplica a |
|-------|----------|
| `'x'` | Solo eje X |
| `'y'` | Solo eje Y |
| `'both'` | Ambos ejes (default) |

## Parámetros de personalización

### Tamaño y forma

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `length` | Longitud del tick (puntos) | `length=6` |
| `width` | Ancho del tick (puntos) | `width=2` |
| `pad` | Espacio entre tick y etiqueta (puntos) | `pad=8` |

### Color

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `color` | Color del tick | `color='red'` |
| `labelcolor` | Color de la etiqueta | `labelcolor='blue'` |

### Dirección

| Parámetro | Valores | Descripción |
|-----------|---------|-------------|
| `direction` | `'in'`, `'out'`, `'inout'` | Hacia dentro, fuera o ambos del axes |

### Visibilidad

| Parámetro | Valores | Descripción |
|-----------|---------|-------------|
| `bottom` / `top` | `True`, `False`, `'on'`, `'off'` | Mostrar ticks en eje X (abajo/arriba) |
| `left` / `right` | `True`, `False`, `'on'`, `'off'` | Mostrar ticks en eje Y (izquierda/derecha) |
| `labelbottom` / `labeltop` | `True`, `False` | Mostrar etiquetas en eje X |
| `labelleft` / `labelright` | `True`, `False` | Mostrar etiquetas en eje Y |

### Ticks mayores y menores

| Parámetro | Descripción |
|-----------|-------------|
| `which` | `'major'`, `'minor'`, `'both'` (default: `'major'`) |

## Casos básicos

### Ticks más largos y gruesos

```python
ax.tick_params(axis='both', length=8, width=2)
```

### Ticks hacia adentro

```python
ax.tick_params(direction='in')
```

### Cambiar color de ticks y etiquetas

```python
ax.tick_params(axis='x', color='red', labelcolor='darkred')
```

## Casos comunes

### Ocultar ticks (pero mantener etiquetas)

```python
ax.tick_params(bottom=False, left=False)  # oculta las marcas
```

### Ocultar etiquetas (pero mantener ticks)

```python
ax.tick_params(labelbottom=False, labelleft=False)
```

### Ocultar completamente eje X

```python
ax.tick_params(axis='x', bottom=False, labelbottom=False)
```

### Personalizar solo ticks menores

```python
ax.tick_params(which='minor', length=4, width=1, color='gray')
ax.tick_params(which='major', length=8, width=2, color='black')
```

### Aumentar espacio entre tick y etiqueta

```python
ax.tick_params(pad=10)  # más separación
```

### Configuración por eje

```python
ax.tick_params(axis='x', rotation=45, labelsize=10)
ax.tick_params(axis='y', labelsize=12, color='blue')
```

## Combinación con otros métodos

```python
# Posición de ticks
ax.set_xticks([0, 2, 4, 6, 8, 10])

# Estilo de ticks
ax.tick_params(axis='x', length=6, width=1.5, rotation=45)

# Etiquetas personalizadas
ax.set_xticklabels(['cero', 'dos', 'cuatro', 'seis', 'ocho', 'diez'])
```

## Buenas prácticas

1. Usar `tick_params` para estilo, `set_xticks` para posiciones
2. Mantener `length` y `width` consistentes entre ejes
3. Usar `direction='in'` para gráficos con bordes ajustados
4. Para gráficos con muchos datos, reducir `length` y aumentar `pad`
5. Usar `which='minor'` para diferenciar visualmente ticks menores

## Errores comunes

| Error | Solución |
|-------|----------|
| `rotation` no tiene efecto | `rotation` no es parámetro de `tick_params`; usar `set_xticklabels(rotation=45)` o `ax.tick_params(axis='x', labelrotation=45)` (versiones recientes) |
| Confundir `pad` (tick-etiqueta) con `labelpad` (etiqueta-eje) | `pad` en tick_params, `labelpad` en `set_xlabel` |
| Cambiar color de tick pero no de etiqueta | Usar `color` para tick, `labelcolor` para etiqueta |
| Olvidar `which` y modificar solo mayores | Especificar `which='both'` o `which='minor'` según necesidad |

## Notas relacionadas

- [[ax.set_xticks_yticks]]
- [[Locators]]
- [[Formatters]]
- [[ax.set_xlabel_ylabel]]
- [[ax.grid]]
