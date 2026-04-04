---
title: PropertyPlot.show — Mostrar diagrama
aliases:
  - show
  - mostrar
  - display

tags:
  - coolprop
  - api/metodo
  - plots
  - visualizacion

# --- Clasificación ---
lib: coolprop
obj: PropertyPlot
tipo: metodo

# --- Comportamiento ---
retorna: None
muta_estado: false

draft: false
---

# PropertyPlot.show — Mostrar diagrama

## Firma de la función

```python
PropertyPlot.show() -> None
```

## Valor de retorno

`None` — Muestra la ventana interactiva con el diagrama.

## Uso básico

```python
from CoolProp.Plots import PropertyPlot
import CoolProp.CoolProp as CP

plot = PropertyPlot('R134a', 'PH', unit_system='EUR')
plot.calc_isolines(CP.iT, num=15)
plot.calc_isolines(CP.iQ, num=10)
plot.draw_isolines()
plot.show()  # Abre ventana interactiva
```

## Integración con matplotlib

`show()` es equivalente a llamar a `plt.show()` de matplotlib:

```python
import matplotlib.pyplot as plt

plot = PropertyPlot('Water', 'TS')
plot.calc_isolines()
plot.draw_isolines()

# Estas dos son equivalentes
plot.show()
plt.show()
```

## Bloqueo de ejecución

`show()` bloquea la ejecución del programa hasta que se cierra la ventana:

```python
plot.show()
print("Esto se ejecuta después de cerrar la ventana")
```

## Sin isolíneas

```python
plot = PropertyPlot('Water', 'PH')
plot.show()  # Muestra diagrama vacío (sin isolíneas)
```

## Uso en scripts

Para scripts que generan múltiples diagramas, usar [[PropertyPlot.savefig]] en lugar de `show()`:

```python
# Guardar sin mostrar ventana
plot.savefig('diagrama.png')
plt.close()  # Liberar memoria
```

## Notas relacionadas

- [[PropertyPlot]]
- [[PropertyPlot.savefig]]
- [[PropertyPlot.draw_isolines]]
