---
title: ax.plot — Gráfico de líneas
aliases:
  - plot
  - gráfico de líneas
  - line plot

tags:
  - matplotlib
  - api/metodo
  - plot/lineas

# --- Clasificación ---
lib: matplotlib
obj: Axes
tipo: metodo

# --- Comportamiento ---
muta_estado: true

draft: false
---

# ax.plot — Gráfico de líneas

## Firma de la función

```python
Axes.plot(
    *args,
    scalex=True,
    scaley=True,
    data=None,
    **kwargs
)
```

## Valor de retorno

La función retorna una lista de objetos [[Line2D]]. La longitud de la lista depende de cuántas líneas se grafican:

| Entrada | Retorno | Ejemplo |
|---------|---------|---------|
| `plot(y)` | lista de 1 `Line2D` | `[linea]` |
| `plot(x, y)` | lista de 1 `Line2D` | `[linea]` |
| `plot(y1, y2, y3)` | lista de 3 `Line2D` | `[linea1, linea2, linea3]` |
| `plot(x, y_matrix)` donde `y_matrix` es 2D | lista de N `Line2D` donde N = número de columnas | `[linea_col0, linea_col1, ...]` |

**Caso con matriz 2D:**

```python
import numpy as np
x = np.linspace(0, 10, 100)
y_matrix = np.array([np.sin(x), np.cos(x), np.sin(x*2)])  # forma (3, 100)

lines = ax.plot(x, y_matrix.T)  # y_matrix.T tiene forma (100, 3)
# lines es lista de 3 objetos Line2D
len(lines)  # 3
```

**Desempaquetado seguro:**

```python
# Para una sola línea
line, = ax.plot(x, y)  # la coma desempaqueta la lista de 1 elemento

# Para múltiples líneas conocidas
line1, line2, line3 = ax.plot(x, y1, x, y2, x, y3)

# Para número variable
lines = ax.plot(x, y_matrix.T)
for line in lines:
    line.set_linewidth(2)
```

## Formas básicas de llamada

| Forma | Ejemplo | Descripción |
|-------|---------|-------------|
| `plot(y)` | `ax.plot(y)` | `x = range(len(y))` |
| `plot(x, y)` | `ax.plot(x, y)` | `x` e `y` misma longitud |
| `plot(x, y, fmt)` | `ax.plot(x, y, 'ro--')` | formato compacto (color+ marcador+estilo) |
| `plot(x1, y1, x2, y2, ...)` | `ax.plot(x1, y1, x2, y2)` | múltiples pares |
| `plot(x1, y1, fmt1, x2, y2, fmt2, ...)` | `ax.plot(x1, y1, 'r-', x2, y2, 'bs--')` | formato por par |

## Parámetros en detalle

### `x`, `y` — datos

| Tipo aceptado | Ejemplo | Nota |
|---------------|---------|------|
| lista | `[1, 2, 3, 4]` | |
| tupla | `(1, 2, 3, 4)` | |
| array NumPy 1D | `np.array([1, 2, 3, 4])` | recomendado |
| array NumPy 2D | `np.array([[1,2],[3,4]])` | cada columna es una línea |
| serie Pandas | `df['columna']` | compatible |

**Reglas:**
- Si se omite `x`, se usa `range(len(y))`
- `x` e `y` deben tener la misma longitud en su primera dimensión
- Si `y` es 2D (N, M), se grafican M líneas, cada una con longitud N
- Si `x` es 2D, debe tener la misma forma que `y`

### `fmt` — formato compacto

String que combina color, marcador y estilo de línea. Los códigos completos están documentados en [[Colores_Nombres]], [[marker]] y [[Estilos_Linea]].

**Resumen rápido:**

| Código | Significado | Ejemplo |
|--------|-------------|---------|
| `'r'`, `'g'`, `'b'`, `'k'` | colores básicos | `'r'` = rojo |
| `'o'`, `'s'`, `'^'`, `'D'` | marcadores | `'o'` = círculo |
| `'-'`, `'--'`, `':'`, `'-.'` | estilos línea | `'--'` = discontinua |

**Ejemplos:**
- `ax.plot(x, y, 'r')` → solo línea roja sólida
- `ax.plot(x, y, 'o')` → solo círculos (sin línea)
- `ax.plot(x, y, '--')` → línea discontinua negra
- `ax.plot(x, y, 'ro--')` → círculos rojos con línea discontinua

### `**kwargs` — parámetros de personalización

#### `color` / `c` — color de la línea

```python
ax.plot(x, y, color='red')
ax.plot(x, y, c='#FF5733')        # hexadecimal
ax.plot(x, y, c=(0.2, 0.4, 0.6))  # RGB (0-1)
ax.plot(x, y, c='0.5')            # escala de grises
```

Ver [[Colores_Nombres]] para más opciones.

#### `linestyle` / `ls` — estilo de línea

```python
ax.plot(x, y, linestyle='solid')   # '-'
ax.plot(x, y, ls='dashed')         # '--'
ax.plot(x, y, ls='dotted')         # ':'
ax.plot(x, y, ls='dashdot')        # '-.'
ax.plot(x, y, ls='none')           # sin línea
```

Ver [[Estilos_Linea]] para más detalles.

#### `linewidth` / `lw` — grosor de línea

```python
ax.plot(x, y, linewidth=2)   # en puntos
ax.plot(x, y, lw=0.5)        # línea muy fina
```

#### `marker` — tipo de marcador

```python
ax.plot(x, y, marker='o')
ax.plot(x, y, marker='s')      # cuadrado
ax.plot(x, y, marker='^')      # triángulo
ax.plot(x, y, marker='none')   # sin marcador
```

Ver [[marker]] para lista completa.

#### `markersize` / `ms` — tamaño del marcador

```python
ax.plot(x, y, marker='o', markersize=8)
ax.plot(x, y, marker='o', ms=12)
```

#### `markeredgewidth` / `mew` — ancho del borde

```python
ax.plot(x, y, marker='o', markeredgewidth=2)
```

#### `markeredgecolor` / `mec` — color del borde

```python
ax.plot(x, y, marker='o', markeredgecolor='black')
ax.plot(x, y, marker='o', mec='k')
```

#### `markerfacecolor` / `mfc` — color de relleno

```python
ax.plot(x, y, marker='o', markerfacecolor='red')
ax.plot(x, y, marker='o', mfc='red')
```

#### `alpha` — transparencia

```python
ax.plot(x, y, alpha=0.5)   # 0 = transparente, 1 = opaco
```

#### `label` — etiqueta para leyenda

```python
ax.plot(x, y, label='señal principal')
```

Luego [[ax.legend]] mostrará esta etiqueta.

#### `zorder` — orden de dibujo

```python
ax.plot(x, y1, zorder=2)   # dibujar encima
ax.plot(x, y2, zorder=1)   # dibujar debajo
```

Valores más altos = más arriba. Por defecto: líneas = 2, marcadores = 3.

## Objeto Line2D

El objeto retornado tiene métodos para modificar la línea después de creada. Ver [[Line2D]] para detalles completos.

```python
line, = ax.plot(x, y)  # la coma desempaqueta la lista
line.set_color('blue')
line.set_linewidth(3)
```

## Casos de uso avanzados

### Línea vertical u horizontal infinita

Para líneas que cruzan todo el gráfico, usar [[axhline_axvline]] en lugar de `ax.plot`.

```python
ax.axvline(x=5, color='red', linestyle='--')
ax.axhline(y=0, color='gray', linestyle=':')
```

### Relleno entre líneas

Ver [[ax.fill_between]].

```python
ax.plot(x, y1, label='superior')
ax.plot(x, y2, label='inferior')
ax.fill_between(x, y1, y2, alpha=0.3)
```

### Escala logarítmica

Ver [[Limites_Escalas]].

```python
ax.plot(x, y)
ax.set_xscale('log')
ax.set_yscale('log')
```

## Buenas prácticas

1. Siempre incluir `label` si se planea usar [[ax.legend]]
2. Definir [[plt.subplots]] con `figsize` antes de graficar
3. Usar `alpha` para solapamiento cuando hay muchas líneas
4. Limitar a 5-6 líneas por axes; usar [[arrays]] para más
5. Preferir colores accesibles (ver [[Colores_Nombres]])
6. Guardar referencia de línea si se modificará después (ver [[Line2D]])

## Errores comunes

| Error | Ejemplo | Solución |
|-------|---------|----------|
| Dimensiones inconsistentes | `x=[1,2,3]`, `y=[1,2]` | `x` e `y` deben tener misma longitud |
| Olvidar que retorna lista | `lines.set_color('red')` | `lines[0].set_color('red')` |
| Formato no reconocido | `ax.plot(x, y, 'z')` | usar código válido de [[Colores_Nombres]], [[marker]] o [[Estilos_Linea]] |
| Mezclar fmt con kwargs redundante | `ax.plot(x, y, 'r--', color='blue')` | usar uno solo |
| Desempaquetado incorrecto con 2D | `line, = ax.plot(x, y_matrix.T)` | `lines = ax.plot(...)` y luego iterar |

## Notas relacionadas

- [[plt.subplots]]
- [[arrays]]
- [[Line2D]]
- [[ax.fill_between]]
- [[axhline_axvline]]
- [[Limites_Escalas]]
- [[ax.legend]]
- [[Colores_Nombres]]
- [[marker]]
- [[Estilos_Linea]]
