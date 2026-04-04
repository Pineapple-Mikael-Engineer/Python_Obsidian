---
title: PropertyPlot.calc_isolines — Calcular isolíneas
aliases:
  - calc_isolines
  - calcular_isolíneas
  - isolines

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

# PropertyPlot.calc_isolines — Calcular isolíneas

## Firma de la función

```python
PropertyPlot.calc_isolines(
    property_type: int,
    num: int = 20,
    *,
    min_val: float = None,
    max_val: float = None
) -> None
```

## Valor de retorno

`None` — Calcula y almacena internamente las isolíneas para ser dibujadas con [[PropertyPlot.draw_isolines]].

## Parámetros en detalle

| Parámetro | Tipo | Descripción | Ejemplo |
|-----------|------|-------------|---------|
| `property_type` | `int` | Propiedad para las isolíneas | `CP.iT`, `CP.iQ`, `CP.iSmass` |
| `num` | `int` | Número de líneas | `20` (default) |
| `min_val` | `float` | Valor mínimo (opcional) | `300` |
| `max_val` | `float` | Valor máximo (opcional) | `500` |

## Propiedades comunes para isolíneas

| Constante | Propiedad | Diagramas típicos |
|-----------|-----------|-------------------|
| `CP.iT` | Isotermas | P-h, T-s |
| `CP.iP` | Isobaras | T-s, h-s |
| `CP.iQ` | Calidad (título) | P-h, T-s |
| `CP.iSmass` | Isentrópicas | P-h |
| `CP.iH` | Isoentálpicas | T-s |
| `CP.iD` | Isocoras | T-s, P-h |

## Uso básico

```python
from CoolProp.Plots import PropertyPlot
import CoolProp.CoolProp as CP

plot = PropertyPlot('R134a', 'PH', unit_system='EUR')

# Calcular isolíneas
plot.calc_isolines(CP.iT, num=15)      # 15 isotermas
plot.calc_isolines(CP.iQ, num=10)      # 10 líneas de calidad
plot.calc_isolines(CP.iSmass, num=8)   # 8 isentrópicas

# Dibujar
plot.draw_isolines()
plot.show()
```

## Control de rango

```python
# Especificar rango personalizado
plot.calc_isolines(CP.iT, num=10, min_val=250, max_val=350)

# Sin especificar rango, CoolProp lo determina automáticamente
plot.calc_isolines(CP.iT, num=15)
```

## Múltiples llamadas

Se pueden llamar múltiples veces para diferentes tipos de isolíneas:

```python
plot.calc_isolines(CP.iT, num=12)      # Isotermas
plot.calc_isolines(CP.iQ, num=8)       # Calidad
plot.calc_isolines(CP.iP, num=6)       # Isobaras

plot.draw_isolines()  # Dibuja todas
```

## Notas

- `calc_isolines` solo **calcula**, no dibuja. Usar [[PropertyPlot.draw_isolines]] después.
- Si no se llama a `calc_isolines`, `draw_isolines` no dibujará nada.
- Los valores `min_val` y `max_val` deben estar dentro del rango válido del fluido.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `property_type` inválido | Constante no definida | Usar `CP.iT`, `CP.iP`, `CP.iQ`, etc. |
| Rango fuera de límites | `min_val` o `max_val` inválidos | Verificar rango del fluido |

## Notas relacionadas

- [[PropertyPlot]]
- [[PropertyPlot.draw_isolines]]
- [[PropertyPlot.show]]
- [[Constants]]
