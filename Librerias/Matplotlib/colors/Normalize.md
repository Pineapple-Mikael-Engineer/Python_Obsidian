---
title: Normalize — Normalización lineal de datos al rango [0, 1]
aliases:
  - Normalize
  - norma lineal
  - normalización
tags:
  - matplotlib
  - api/clase
  - styling
lib: matplotlib
obj: Normalize
tipo: clase
retorna: Normalize
muta_estado: false
draft: false
---

# Normalize — Normalización lineal de datos al rango [0, 1]

## Idea clave

`Normalize` es la pieza base del mapeo de color: convierte el rango real de tus datos `[vmin, vmax]` a `[0, 1]` de forma **lineal**, que es el rango que el colormap entiende para producir un color. Sin una norma explícita, Matplotlib crea una `Normalize` automática con el mín/máx de los datos. Se pasa con el argumento `norm=` a `imshow`, `scatter`, `pcolormesh` o `contourf`. Es el primer eslabón del [[concepto_color_mapping]] y la clase padre de variantes como [[LogNorm]] y [[BoundaryNorm]].

## Firma del constructor

```python
matplotlib.colors.Normalize(
    vmin=None,   # valor de datos que se mapea a 0.0 (extremo bajo del cmap)
    vmax=None,   # valor de datos que se mapea a 1.0 (extremo alto del cmap)
    clip=False,  # si True, recorta fuera de rango a 0/1 en vez de marcarlos
)
```

## Qué hace / Valor de retorno

| Aspecto | Detalle |
|---------|---------|
| Entrada | valores de datos en escala real |
| Salida | valores en `[0, 1]` que el colormap traduce a color |
| Tipo de mapeo | **lineal**: proporción constante en todo el rango |
| `muta_estado` | `false` — solo describe la transformación; no altera el array |
| Llamable | `norm(x)` devuelve la posición normalizada de `x` |

```python
from matplotlib.colors import Normalize

norm = Normalize(vmin=0, vmax=200)
norm(0)      # → 0.0
norm(100)    # → 0.5
norm(200)    # → 1.0
norm(50)     # → 0.25
```

## Parámetros en detalle

### `vmin` / `vmax` — extremos del rango de datos

```python
# Fija el rango de color independientemente del mín/máx real de los datos
norm = Normalize(vmin=-5, vmax=5)
ax.imshow(anomalias, cmap='coolwarm', norm=norm)
```

Fijar `vmin`/`vmax` explícitos estabiliza la escala de color entre varios gráficos para que sean comparables.

### `clip` — manejo de valores fuera de rango

```python
norm = Normalize(vmin=0, vmax=10, clip=True)
norm(15)     # → 1.0   (recortado; sin clip quedaría >1 → color "over")
```

### Uso vía `norm=`

```python
sc = ax.scatter(x, y, c=z, cmap='viridis', norm=Normalize(0, 100))
fig.colorbar(sc, ax=ax)   # la barra hereda los límites de la norma
```

## Casos de uso

### Escala de color común entre subplots comparables

```python
norm = Normalize(vmin=0, vmax=1)
for ax, M in zip(axs, matrices):
    ax.imshow(M, cmap='magma', norm=norm)   # misma escala → comparables
```

### Datos divergentes con centro fijo

```python
norm = Normalize(vmin=-10, vmax=10)         # 0 cae en el centro del cmap
ax.imshow(desviaciones, cmap='RdBu', norm=norm)
```

## Buenas prácticas

1. Fija `vmin`/`vmax` cuando compares varias figuras: garantiza que el mismo color signifique el mismo valor.
2. Reutiliza la misma instancia `norm` en varios mappables para una leyenda única coherente.
3. Para datos divergentes, elige `vmin`/`vmax` simétricos respecto al centro de referencia.
4. Pasa la norma junto al `cmap`: la pareja norma+colormap define por completo el mapeo de color.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Contraste plano | rango de datos enorme con picos | usar `LogNorm` en vez de la lineal |
| `vmin == vmax` | rango nulo (datos constantes) | dar un rango con `vmin < vmax` |
| Escala distinta entre subplots | norma automática por figura | compartir una sola instancia `Normalize` |
| Outliers dominan el color | `vmax` lo fija el máximo extremo | fijar `vmax` a un percentil razonable |

## Notas relacionadas

- [[LogNorm]]
- [[Colormaps]]
- [[concepto_color_mapping]]
- [[ax.imshow]]
