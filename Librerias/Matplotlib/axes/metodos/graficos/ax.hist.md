---
title: ax.hist — Histograma
aliases:
  - hist
  - histograma
  - distribución
  - ax.hist
tags:
  - matplotlib
  - api/metodo
  - axes/graficos
lib: matplotlib
obj: Axes
tipo: metodo
muta_estado: true
requiere: []
draft: false
---

# ax.hist — Histograma

## Firma

```python
Axes.hist(
    x,
    bins=None,
    range=None,
    density=False,
    weights=None,
    cumulative=False,
    bottom=None,
    histtype='bar',
    align='mid',
    orientation='vertical',
    rwidth=None,
    log=False,
    color=None,
    label=None,
    stacked=False,
    **kwargs
)
```

## Parámetros principales

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `x` | array-like o lista de arrays | - | Datos a histogramar |
| `bins` | int, sequence o str | `10` | Número de bins o bordes |
| `range` | tupla `(min, max)` | `None` | Rango de datos a incluir |
| `density` | `bool` | `False` | Normalizar a densidad (área = 1) |
| `weights` | array-like | `None` | Pesos para cada dato |
| `cumulative` | `bool` | `False` | Histograma acumulado |
| `histtype` | `str` | `'bar'` | Tipo: `'bar'`, `'step'`, `'stepfilled'`, `'barstacked'` |
| `orientation` | `str` | `'vertical'` | Orientación: `'vertical'`, `'horizontal'` |
| `stacked` | `bool` | `False` | Apilar múltiples datasets |
| `**kwargs` | - | - | Propiedades de [[Rectangle]] o [[Patch]] |

## Valor de retorno

```python
n, bins, patches = ax.hist(x)
```

Retorna una tupla con tres elementos:

| Retorno | Tipo | Descripción |
|---------|------|-------------|
| `n` | array | Valores de los bins (frecuencias o densidades) |
| `bins` | array | Bordes de los bins (longitud = len(n) + 1) |
| `patches` | lista de Rectangle | Objetos de las barras (uno por bin) |

### Modificación posterior

```python
n, bins, patches = ax.hist(x)

# Modificar barras individuales
patches[0].set_color('red')
patches[0].set_alpha(0.8)

# Modificar todas
for patch in patches:
    patch.set_edgecolor('black')
    patch.set_linewidth(1)
```

## Parámetros en detalle

### bins — control de intervalos

| Tipo | Ejemplo | Descripción |
|------|---------|-------------|
| Entero | `bins=20` | Número automático de bins |
| Secuencia | `bins=[0, 2, 4, 6, 8, 10]` | Bordes específicos |
| String | `bins='auto'` | Método automático: `'auto'`, `'fd'`, `'scott'`, `'sturges'` |

```python
# Automático (recomendado)
ax.hist(x, bins='auto')

# Manual con rangos desiguales
ax.hist(x, bins=[0, 1, 2, 5, 10])
```

### range — rango de datos

```python
ax.hist(x, range=(0, 10))  # solo datos entre 0 y 10
```

### density — normalización

```python
ax.hist(x, density=True)   # área total = 1 (función densidad)
ax.hist(x, density=False)  # frecuencias absolutas (default)
```

### cumulative — acumulado

```python
ax.hist(x, cumulative=True)      # frecuencia acumulada
ax.hist(x, cumulative=-1)        # frecuencia acumulada inversa
ax.hist(x, density=True, cumulative=True)  # CDF
```

### histtype — tipo de histograma

| Valor | Descripción |
|-------|-------------|
| `'bar'` | Barras tradicionales (default) |
| `'step'` | Solo contorno (sin relleno) |
| `'stepfilled'` | Contorno con relleno |
| `'barstacked'` | Barras apiladas (múltiples datasets) |

```python
ax.hist(x, histtype='step', color='blue')
ax.hist(x, histtype='stepfilled', alpha=0.5)
```

### orientation — orientación

```python
ax.hist(x, orientation='vertical')   # vertical (default)
ax.hist(x, orientation='horizontal') # horizontal
```

### rwidth — ancho relativo

```python
ax.hist(x, rwidth=0.8)  # barras ocupan 80% del espacio (con espacio entre ellas)
```

### log — escala logarítmica

```python
ax.hist(x, log=True)  # eje Y en escala logarítmica
```

## Múltiples datasets

### Superpuestos (transparentes)

```python
ax.hist(data1, bins=20, alpha=0.5, label='Grupo 1')
ax.hist(data2, bins=20, alpha=0.5, label='Grupo 2')
ax.legend()
```

### Apilados (stacked)

```python
ax.hist([data1, data2, data3], bins=20, stacked=True, label=['A', 'B', 'C'])
ax.legend()
```

### Lado a lado (con desplazamiento manual)

```python
bins = np.linspace(0, 10, 20)
ax.hist(data1, bins, alpha=0.7, label='Grupo 1')
ax.hist(data2, bins, alpha=0.7, label='Grupo 2')
```

## Peso (weights)

```python
# Datos con pesos
datos = [1, 2, 2, 3, 3, 3]
pesos = [0.5, 1, 1, 1.5, 1.5, 1.5]
ax.hist(datos, weights=pesos, bins=3)
```

## Casos comunes

### Histograma básico

```python
ax.hist(data, bins=30, color='steelblue', edgecolor='black', alpha=0.7)
ax.set_xlabel('Valor')
ax.set_ylabel('Frecuencia')
```

### Histograma normalizado (densidad)

```python
ax.hist(data, bins=30, density=True, alpha=0.7)
ax.set_ylabel('Densidad')
```

### CDF (función de distribución acumulada)

```python
ax.hist(data, bins=30, density=True, cumulative=True, histtype='step')
ax.set_ylabel('Probabilidad acumulada')
```

### Histograma horizontal

```python
ax.hist(data, bins=30, orientation='horizontal', color='green', edgecolor='black')
ax.set_xlabel('Frecuencia')
ax.set_ylabel('Valor')
```

### Comparación de dos distribuciones

```python
ax.hist(data1, bins=30, alpha=0.5, label='Grupo 1', color='blue')
ax.hist(data2, bins=30, alpha=0.5, label='Grupo 2', color='red')
ax.legend()
```

### Histograma con línea de media

```python
n, bins, patches = ax.hist(data, bins=30, alpha=0.7)
media = np.mean(data)
ax.axvline(media, color='red', linestyle='--', linewidth=2, label=f'Media = {media:.2f}')
ax.legend()
```

## Buenas prácticas

1. Usar `bins='auto'` para elección automática (más robusto que valor fijo)
2. Para comparar distribuciones, usar `alpha < 1` o `histtype='step'`
3. Usar `density=True` cuando se comparan datasets con diferente tamaño
4. Añadir `edgecolor='black'` para mejorar legibilidad de barras individuales
5. Para muestras grandes (>1000 puntos), aumentar `bins` gradualmente (30-50 es típico)
6. Siempre etiquetar ejes con unidades

## Errores comunes

| Error | Solución |
|-------|----------|
| `bins` demasiado alto (ruido) | Reducir bins o usar `bins='auto'` |
| `bins` demasiado bajo (pérdida de detalle) | Aumentar bins |
| Escala Y no interpretable | Usar `density=True` para probabilidad, `density=False` para conteos |
| Histogramas superpuestos ilegibles | Usar `alpha=0.5` o `histtype='step'` |
| Datos con valores atípicos extremos | Usar `range` para enfocar en rango relevante |

## Notas relacionadas

- [[ax.legend]]
- [[ax.set_xlabel_ylabel]]
