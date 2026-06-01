---
title: ax.set_yscale — Escala del eje Y
aliases:
  - set_yscale
  - ax.set_yscale
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

# ax.set_yscale — Escala del eje Y

Cambia la transformación matemática del eje vertical: de lineal a logarítmica, log simétrica o logística. Es la versión vertical de `set_xscale` y resulta esencial cuando la variable representada (concentraciones, intensidades, poblaciones) abarca varios órdenes de magnitud.

## Firma de la función

```python
Axes.set_yscale(
    value,
    **kwargs
)
```

## Valor de retorno

Devuelve `None`. Muta el estado del Axes: sustituye el objeto de escala del eje Y y recoloca ticks y *gridlines*.

| Entrada | Retorno | Efecto |
|---------|---------|--------|
| `set_yscale('linear')` | `None` | escala uniforme (defecto) |
| `set_yscale('log')` | `None` | escala logarítmica base 10 |
| `set_yscale('symlog')` | `None` | log que admite ceros y negativos |
| `set_yscale('logit')` | `None` | escala para probabilidades en (0, 1) |

```python
ax.set_yscale('log')
print(ax.get_yscale())   # → 'log'
```

## Formas básicas de llamada

| Valor | Cuándo usarlo |
|-------|---------------|
| `'linear'` | rango acotado (por defecto) |
| `'log'` | valores positivos sobre muchos órdenes de magnitud |
| `'symlog'` | valores que cruzan cero o negativos |
| `'logit'` | proporciones/probabilidades en (0, 1) |

## Parámetros en detalle

### value

Nombre de la escala (cadena) o un objeto `ScaleBase`. Único argumento obligatorio.

| Escala | Transformación | Restricción de dominio |
|--------|----------------|------------------------|
| `'linear'` | `y` | ninguna |
| `'log'` | `log10(y)` | `y > 0` |
| `'symlog'` | lineal cerca de 0, log fuera | ninguna |
| `'logit'` | `log(y / (1 - y))` | `0 < y < 1` |

### kwargs específicos de cada escala

```python
ax.set_yscale('log', base=10)             # base explícita
ax.set_yscale('symlog', linthresh=0.5)    # umbral lineal central
```

| Escala | kwarg habitual | Significado |
|--------|----------------|-------------|
| `'log'` | `base` | base del logaritmo (10 por defecto) |
| `'symlog'` | `linthresh` | semiancho de la zona lineal en torno a 0 |
| `'log'` | `subs` | posiciones de ticks menores |

## Casos de uso

### Magnitud que crece exponencialmente

```python
ax.plot(tiempo, poblacion)
ax.set_yscale('log')      # crecimiento exponencial como recta
```

### Espectro con valores muy dispares

```python
ax.plot(longitud_onda, intensidad)
ax.set_yscale('log')      # picos y fondo visibles a la vez
```

### Valores que incluyen negativos

```python
ax.set_yscale('symlog', linthresh=1)
```

## Buenas prácticas

1. Reservar `'log'` para datos estrictamente positivos; ceros y negativos se descartan.
2. Combinar escala logarítmica en Y con lineal en X (gráfico semilog) para detectar crecimiento exponencial.
3. Fijar la escala antes que los límites con `ax.set_ylim`, ya que el cambio de escala recoloca los ticks.
4. Verificar con `ax.get_yscale()` durante la depuración.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Puntos faltan en `'log'` | Valores ≤ 0 | Filtrar datos o usar `'symlog'` |
| `ValueError` escala inválida | Nombre mal escrito | Usar `'linear'`, `'log'`, `'symlog'` o `'logit'` |
| Ejes desalineados entre subgráficos | Distinta escala por error | Aplicar la misma escala a todos |
| Etiquetas log saturadas | Demasiados ticks menores | Ajustar `subs` o el `LogLocator` |

## Notas relacionadas

El equivalente en `pyplot` es `plt.yscale()`, que actúa sobre el Axes activo (ver [[concepto_pyplot_vs_oo]]). La escala fija el reparto de ticks del eje Y dentro de la [[concepto_anatomia_figura]].

- [[ax.set_xscale]]
- [[ax.set_ylim]]
- [[concepto_anatomia_figura]]
- [[concepto_pyplot_vs_oo]]
