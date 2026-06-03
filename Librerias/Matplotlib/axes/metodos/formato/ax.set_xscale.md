---
title: ax.set_xscale — Escala del eje X
aliases:
  - set_xscale
  - ax.set_xscale
tags:
  - matplotlib
  - api/metodo
  - formato

# --- Clasificación ---
lib: matplotlib
obj: Axes
tipo: metodo

# --- Comportamiento ---
retorna: None
muta_estado: true

draft: false
---

# ax.set_xscale — Escala del eje X

Cambia la transformación matemática del eje horizontal: de la escala lineal por defecto a logarítmica, log simétrica o logística. Es la herramienta clave cuando los datos abarcan varios órdenes de magnitud y una escala lineal los aplastaría contra un extremo.

## Firma de la función

```python
Axes.set_xscale(
    value,
    **kwargs
)
```

## Valor de retorno

Devuelve `None`. Es un método que muta el estado del Axes: reemplaza el objeto de escala del eje X y reubica ticks y *gridlines* en consecuencia.

| Entrada | Retorno | Efecto |
|---------|---------|--------|
| `set_xscale('linear')` | `None` | escala uniforme (defecto) |
| `set_xscale('log')` | `None` | escala logarítmica base 10 |
| `set_xscale('symlog')` | `None` | log que admite ceros y negativos |
| `set_xscale('logit')` | `None` | escala para probabilidades en (0, 1) |

```python
ax.set_xscale('log')
print(ax.get_xscale())   # → 'log'
```

## Formas básicas de llamada

| Valor | Cuándo usarlo |
|-------|---------------|
| `'linear'` | datos en un rango acotado (por defecto) |
| `'log'` | datos positivos sobre muchos órdenes de magnitud |
| `'symlog'` | datos que cruzan cero o incluyen negativos |
| `'logit'` | proporciones/probabilidades estrictamente en (0, 1) |

## Parámetros en detalle

### value

Nombre de la escala (cadena) o un objeto `ScaleBase`. Es el único argumento obligatorio.

| Escala | Transformación | Restricción de dominio |
|--------|----------------|------------------------|
| `'linear'` | `x` | ninguna |
| `'log'` | `log10(x)` | `x > 0` |
| `'symlog'` | lineal cerca de 0, log fuera | ninguna |
| `'logit'` | `log(x / (1 - x))` | `0 < x < 1` |

### kwargs específicos de cada escala

Ciertas escalas aceptan parámetros extra:

```python
ax.set_xscale('log', base=2)              # logaritmo en base 2
ax.set_xscale('symlog', linthresh=0.1)    # umbral del tramo lineal central
```

| Escala | kwarg habitual | Significado |
|--------|----------------|-------------|
| `'log'` | `base` | base del logaritmo (10 por defecto) |
| `'symlog'` | `linthresh` | semiancho de la zona lineal en torno a 0 |
| `'log'` | `subs` | posiciones de ticks menores |

## Casos de uso

### Datos en varios órdenes de magnitud

```python
ax.plot(frecuencias, ganancia)
ax.set_xscale('log')      # 1, 10, 100, 1000... equiespaciados
```

### Eje con valores positivos y negativos

```python
ax.set_xscale('symlog', linthresh=1)   # log lejos de 0, lineal cerca
```

### Logaritmo en otra base

```python
ax.set_xscale('log', base=2)   # útil para tamaños 2, 4, 8, 16...
```

## Buenas prácticas

1. Usar `'log'` solo con datos estrictamente positivos; los ceros o negativos quedan fuera del dominio y se descartan.
2. Para datos que cruzan cero, `'symlog'` con un `linthresh` razonable evita la discontinuidad del logaritmo.
3. Ajustar la escala antes de afinar los límites con `ax.set_xlim`, porque cambiar la escala reubica los ticks.
4. Comprobar el resultado con `ax.get_xscale()` cuando se depura.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Datos desaparecen en `'log'` | Valores ≤ 0 fuera de dominio | Filtrar/desplazar datos o usar `'symlog'` |
| `ValueError` por valor desconocido | Cadena de escala mal escrita | Usar `'linear'`, `'log'`, `'symlog'` o `'logit'` |
| Ticks ilegibles | Escala log sin formatear | Ajustar `LogLocator`/`LogFormatter` |
| `'logit'` falla | Datos fuera de (0, 1) | Reservar `'logit'` para probabilidades |

## Notas relacionadas

El equivalente en `pyplot` es `plt.xscale()`, que opera sobre el Axes activo (ver [[concepto_pyplot_vs_oo]]). La escala determina cómo se distribuyen los ticks del eje X dentro de la [[concepto_anatomia_figura]].

- [[ax.set_yscale]]
- [[ax.set_xlim]]
- [[concepto_anatomia_figura]]
- [[concepto_pyplot_vs_oo]]
