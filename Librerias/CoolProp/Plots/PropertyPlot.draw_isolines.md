---
title: PropertyPlot.draw_isolines — Dibujar isolíneas
aliases:
  - draw_isolines
  - dibujar_isolíneas
  - dibujar_lineas

tags:
  - coolprop
  - api/metodo
  - plots
  - isolines

# --- Clasificación ---
lib: coolprop
obj: PropertyPlot
tipo: metodo

# --- Comportamiento ---
retorna: None
muta_estado: true

draft: false
---

# PropertyPlot.draw_isolines — Dibujar isolíneas

## Firma de la función

```python
PropertyPlot.draw_isolines() -> None
```

## Valor de retorno

`None` — Dibuja las isolíneas previamente calculadas sobre el eje del diagrama.

## Uso básico

```python
from CoolProp.Plots import PropertyPlot
import CoolProp.CoolProp as CP

plot = PropertyPlot('R134a', 'PH', unit_system='EUR')

# Calcular isolíneas
plot.calc_isolines(CP.iT, num=15)
plot.calc_isolines(CP.iQ, num=10)

# Dibujar en el diagrama
plot.draw_isolines()

plot.show()
```

## Orden de dibujo

```python
# Las isolíneas se dibujan en el orden de llamada
plot.calc_isolines(CP.iQ, num=10)   # Calidad primero
plot.calc_isolines(CP.iT, num=15)   # Isotermas después

plot.draw_isolines()  # Las isotermas se dibujan encima de las de calidad
```

## Personalización post-dibujo

```python
plot.draw_isolines()

# Acceder al eje de matplotlib para modificar
ax = plot.axis
ax.set_xlim(200, 500)
ax.grid(True, alpha=0.3)

plot.show()
```

## Sin isolíneas calculadas

Si se llama `draw_isolines()` sin antes llamar a [[PropertyPlot.calc_isolines]]:

```python
plot = PropertyPlot('Water', 'PH')
plot.draw_isolines()  # No dibuja nada (o dibuja el diagrama vacío)
plot.show()  # Diagrama sin isolíneas
```

## Notas relacionadas

- [[PropertyPlot]]
- [[PropertyPlot.calc_isolines]]
- [[PropertyPlot.show]]
