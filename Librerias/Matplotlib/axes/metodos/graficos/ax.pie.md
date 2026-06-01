---
title: ax.pie — Gráfico de sectores
aliases:
  - pie
  - ax.pie
  - gráfico de sectores
  - tarta
  - pastel

tags:
  - matplotlib
  - api/metodo
  - plot/sectores

# --- Clasificación ---
lib: matplotlib
obj: Axes
tipo: metodo

# --- Comportamiento ---
retorna: tuple
muta_estado: true

# --- Dependencias ---
requiere:
  - concepto_figure_axes

draft: false
---

# ax.pie — Gráfico de sectores

## Firma de la función

```python
Axes.pie(
    x,
    explode=None,
    labels=None,
    colors=None,
    autopct=None,
    pctdistance=0.6,
    shadow=False,
    labeldistance=1.1,
    startangle=0,
    radius=1,
    counterclock=True,
    wedgeprops=None,
    textprops=None,
    **kwargs
)
```

## Valor de retorno

Retorna una **tupla** cuya longitud depende de si se pidieron porcentajes con `autopct`. Sus elementos son listas de [[concepto_artist]].

| Llamada | Retorno | Elementos |
|---------|---------|-----------|
| sin `autopct` | `(wedges, texts)` | 2 listas |
| con `autopct` | `(wedges, texts, autotexts)` | 3 listas |

| Elemento | Contiene | Tipo |
|----------|----------|------|
| `wedges` | las cuñas (sectores) | lista de `Wedge` (`Patch`) |
| `texts` | las etiquetas exteriores | lista de `Text` |
| `autotexts` | los porcentajes dentro de cada cuña (solo con `autopct`) | lista de `Text` |

```python
wedges, texts, autotexts = ax.pie(x, labels=lab, autopct='%1.1f%%')
wedges[0].set_edgecolor('white')   # reestilizar una cuña
autotexts[0].set_color('white')    # color del porcentaje
```

Atención al desempaquetado: con `autopct` son **tres** valores; sin él, **dos**.

## Parámetros en detalle

### `x` — los valores

Secuencia de tamaños de cada sector. Si la suma es ≤ 1 se usan tal cual como fracciones; si es mayor, se **normaliza** dividiendo por el total. No deben ser negativos.

```python
ax.pie([30, 20, 50])         # se normaliza: 30%, 20%, 50%
ax.pie([0.3, 0.2, 0.5])      # ya suman 1.0
```

### `labels` — etiquetas de cada sector

```python
ax.pie([30, 20, 50], labels=['A', 'B', 'C'])
```

### `autopct` — mostrar el porcentaje dentro de cada cuña

Cuando se pasa, el retorno incluye `autotexts`. Acepta un formato printf o un callable.

```python
ax.pie(x, autopct='%1.1f%%')         # '%' literal duplicado → "33.3%"
ax.pie(x, autopct='%d%%')            # entero
ax.pie(x, autopct=lambda p: f'{p:.0f}%')  # callable
```

### `startangle` — ángulo inicial

Grados desde el eje X positivo, en sentido antihorario por defecto.

```python
ax.pie(x, startangle=90)    # empezar arriba (12 en punto)
ax.pie(x, startangle=90, counterclock=False)  # y avanzar en horario
```

### `explode` — separar sectores

```python
ax.pie(x, explode=[0, 0.1, 0])   # destaca el segundo sector
```

### `colors` — colores por sector

```python
ax.pie(x, colors=['#4C72B0', '#DD8452', '#55A868'])
```

### `wedgeprops` / `textprops` — estilo fino

```python
ax.pie(x, wedgeprops={'edgecolor': 'white', 'linewidth': 1})
ax.pie(x, wedgeprops={'width': 0.4})   # anillo (donut) en vez de tarta
```

## Casos de uso

### Tarta básica con porcentajes

```python
import matplotlib.pyplot as plt

valores = [35, 25, 20, 20]
etiquetas = ['Renovables', 'Gas', 'Nuclear', 'Carbón']

fig, ax = plt.subplots()
ax.pie(valores, labels=etiquetas, autopct='%1.1f%%', startangle=90)
ax.set_title("Mix energético")
ax.axis('equal')   # círculo perfecto (no elipse)
```

### Gráfico de anillo (donut)

```python
ax.pie(valores, labels=etiquetas,
       wedgeprops={'width': 0.4},   # agujero central
       startangle=90)
```

### Destacar un sector

```python
ax.pie(valores, labels=etiquetas,
       explode=[0.1, 0, 0, 0],      # separa el primero
       autopct='%1.0f%%', shadow=True)
```

## Buenas prácticas

1. Llama a `ax.set_aspect('equal')` o `ax.axis('equal')` para que el círculo no salga ovalado.
2. Usa `startangle=90` para empezar arriba, más natural de leer.
3. Limita a 4–6 sectores; con más, una barra es más legible.
4. Recuerda desempaquetar 3 valores si pasas `autopct`, 2 si no.
5. Doblar el `%` en `autopct` (`'%1.1f%%'`) para que aparezca el símbolo.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `too many values to unpack` | `autopct` activo devuelve 3 valores | `wedges, texts, autotexts = ax.pie(...)` |
| Tarta ovalada | el Axes no es cuadrado | `ax.axis('equal')` |
| Porcentajes sin `%` | falta doblar el símbolo | usar `'%1.1f%%'` |
| Sectores en orden inesperado | sentido antihorario desde 0° | ajustar `startangle` / `counterclock` |
| `x` con negativos | los tamaños deben ser ≥ 0 | filtrar o transformar los datos |

## Notas relacionadas

- [[concepto_artist]]
- [[Axes]]
- [[concepto_figure_axes]]
- [[ax.plot]]
- [[plt.subplots]]
