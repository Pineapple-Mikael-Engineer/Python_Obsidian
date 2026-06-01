---
title: ax.set_facecolor — Color de fondo del área de ploteo
aliases:
  - set_facecolor
  - ax.set_facecolor
tags:
  - matplotlib
  - api/metodo
  - styling

# --- Clasificación ---
lib: matplotlib
obj: Axes
tipo: metodo

# --- Comportamiento ---
retorna: None
muta_estado: true

draft: false
---

# ax.set_facecolor — Color de fondo del área de ploteo

Define el color de relleno del rectángulo interior del Axes, es decir, el fondo sobre el que se dibujan los datos. No afecta al lienzo completo de la figura: para eso está `fig.set_facecolor`. Es un ajuste puramente estético que mejora el contraste de las series.

## Firma de la función

```python
Axes.set_facecolor(color)
```

## Valor de retorno

Devuelve `None`. Muta el estado del Axes: cambia el color del *patch* de fondo de la región de ploteo.

| Entrada | Retorno | Efecto |
|---------|---------|--------|
| `set_facecolor('white')` | `None` | fondo blanco (defecto típico) |
| `set_facecolor('#f0f0f0')` | `None` | gris muy claro por hex |
| `set_facecolor((0.9, 0.9, 1.0))` | `None` | azul pálido por tupla RGB |
| `set_facecolor('none')` | `None` | fondo transparente |

```python
ax.set_facecolor('lightgray')
print(ax.get_facecolor())   # → (0.827..., 0.827..., 0.827..., 1.0)
```

## Formas básicas de llamada

| Forma de color | Ejemplo |
|----------------|---------|
| Nombre | `ax.set_facecolor('whitesmoke')` |
| Hex | `ax.set_facecolor('#eaeaf2')` |
| Tupla RGB | `ax.set_facecolor((0.95, 0.95, 0.95))` |
| Tupla RGBA | `ax.set_facecolor((0.2, 0.2, 0.2, 0.5))` |
| Gris por cadena | `ax.set_facecolor('0.9')` |
| Transparente | `ax.set_facecolor('none')` |

## Parámetros en detalle

### color

Cualquier especificación de color válida de Matplotlib. El alias es `fc`.

| Tipo | Ejemplo | Notas |
|------|---------|-------|
| Nombre CSS | `'steelblue'` | nombres reconocidos |
| Hex `#rrggbb` | `'#336699'` | con o sin alpha (`#rrggbbaa`) |
| RGB(A) | `(0.2, 0.4, 0.6)` | componentes en [0, 1] |
| Gris | `'0.8'` | cadena con un número en [0, 1] |
| Ciclo Tab | `'C0'`, `'C1'` | colores del ciclo por defecto |
| `'none'` | `'none'` | sin relleno (transparente) |

```python
ax.set_facecolor('C1')          # naranja del ciclo por defecto
ax.set_facecolor((0, 0, 0, 0))  # totalmente transparente
```

## Casos de uso

### Fondo gris suave para resaltar líneas claras

```python
ax.set_facecolor('#f5f5f5')
ax.plot(x, y, color='crimson')
```

### Tema oscuro en el área de datos

```python
ax.set_facecolor('#202020')
ax.plot(x, y, color='cyan')
```

### Fondo transparente (solo se ve el de la figura)

```python
ax.set_facecolor('none')
```

## Buenas prácticas

1. Distinguir bien los dos niveles: `ax.set_facecolor` colorea solo la región de datos; `fig.set_facecolor` colorea el lienzo entero.
2. Mantener suficiente contraste entre el fondo y el color de las series para preservar la legibilidad.
3. Para temas globales, preferir `plt.rcParams['axes.facecolor']` o un estilo con `plt.style.use` en lugar de fijarlo manualmente en cada Axes.
4. Usar `'none'` cuando quieras que el fondo de la figura se vea a través del Axes.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| El lienzo no cambia | Se esperaba teñir toda la figura | Usar `fig.set_facecolor` para el lienzo |
| `ValueError` color inválido | Cadena no reconocida | Usar nombre, hex o tupla RGB válidos |
| Fondo no se ve al exportar | `savefig` con fondo propio | Pasar `facecolor=` también a `savefig` |
| Series ilegibles | Fondo y línea de color similar | Aumentar el contraste de color |

## Notas relacionadas

A diferencia de `fig.set_facecolor` (que pinta el lienzo), este método actúa sobre el *patch* del Axes, la región de ploteo descrita en la [[concepto_anatomia_figura]]. No tiene una función `pyplot` directa equivalente, lo que ilustra la diferencia entre ambas interfaces (ver [[concepto_pyplot_vs_oo]]).

- [[fig.set_facecolor]]
- [[ax.grid]]
- [[concepto_anatomia_figura]]
- [[concepto_pyplot_vs_oo]]
