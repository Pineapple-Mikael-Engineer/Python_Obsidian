---
title: PropertyPlot.savefig — Guardar diagrama como imagen
aliases:
  - savefig
  - guardar
  - exportar

tags:
  - coolprop
  - api/metodo
  - plots
  - exportacion

# --- Clasificación ---
lib: coolprop
obj: PropertyPlot
tipo: metodo

# --- Comportamiento ---
retorna: None
muta_estado: false

draft: false
---

# PropertyPlot.savefig — Guardar diagrama como imagen

## Firma de la función

```python
PropertyPlot.savefig(
    filename: str,
    dpi: int = 300,
    bbox_inches: str = 'tight'
) -> None
```

## Valor de retorno

`None` — Guarda el diagrama en un archivo de imagen.

## Parámetros en detalle

| Parámetro | Tipo | Descripción | Ejemplo |
|-----------|------|-------------|---------|
| `filename` | `str` | Nombre del archivo (extensión define formato) | `'diagrama.png'`, `'plot.pdf'` |
| `dpi` | `int` | Resolución en puntos por pulgada | `300` (default) |
| `bbox_inches` | `str` | Recorte del área guardada | `'tight'` (default) |

## Uso básico

```python
from CoolProp.Plots import PropertyPlot
import CoolProp.CoolProp as CP

plot = PropertyPlot('R134a', 'PH', unit_system='EUR')
plot.calc_isolines(CP.iT, num=15)
plot.calc_isolines(CP.iQ, num=10)
plot.draw_isolines()

# Guardar como PNG
plot.savefig('diagrama_r134a.png')
```

## Formatos soportados

La extensión del archivo determina el formato:

| Extensión | Formato | Uso típico |
|-----------|---------|------------|
| `.png` | PNG | Web, documentación |
| `.pdf` | PDF | Informes, papers |
| `.svg` | SVG | Vectorial, edición |
| `.jpg` / `.jpeg` | JPEG | Fotos (no recomendado para diagramas) |

```python
plot.savefig('diagrama.pdf')   # PDF vectorial
plot.savefig('diagrama.svg')   # SVG vectorial
```

## Control de calidad (dpi)

```python
# Baja resolución (borroso)
plot.savefig('diagrama_bajo.png', dpi=72)

# Alta resolución (nítido)
plot.savefig('diagrama_alto.png', dpi=600)
```

## Sin mostrar ventana

Útil para scripts batch:

```python
plot.savefig('diagrama.png')
# No se abre ventana interactiva
```

## Integración con matplotlib

`savefig()` es equivalente a `plt.savefig()` de matplotlib:

```python
import matplotlib.pyplot as plt

plot.savefig('diagrama.png')
# Es equivalente a:
plt.savefig('diagrama.png')
```

## Ejemplo con bucle

```python
fluidos = ['Water', 'R134a', 'R290']

for fluid in fluidos:
    plot = PropertyPlot(fluid, 'PH', unit_system='EUR')
    plot.calc_isolines(CP.iT, num=10)
    plot.calc_isolines(CP.iQ, num=8)
    plot.draw_isolines()
    plot.savefig(f'diagrama_{fluid}.png')
    # plot.show()  # No mostrar ventana
```

## Notas relacionadas

- [[PropertyPlot]]
- [[PropertyPlot.show]]
- [[PropertyPlot.draw_isolines]]
