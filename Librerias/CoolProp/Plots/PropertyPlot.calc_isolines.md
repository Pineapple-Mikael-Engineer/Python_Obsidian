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
    iso_range: Union[List[float], np.ndarray] = None
) -> None
```

## Valor de retorno

`None` — Calcula y almacena internamente las isolíneas para ser dibujadas con [[PropertyPlot.draw_isolines]].

## Parámetros en detalle

| Parámetro | Tipo | Descripción | Ejemplo |
|-----------|------|-------------|---------|
| `property_type` | `int` | Propiedad para las isolíneas | `CP.iT`, `CP.iQ`, `CP.iSmass` |
| `num` | `int` | Número de líneas a dibujar | `20` (default) |
| `iso_range` | `list` o `ndarray` | Rango **exactamente 2 valores** `[min, max]` | `[254, 1800]` o `np.linspace(254, 1800, 2)` |

## Comportamiento de iso_range

**Importante:** `iso_range` debe contener **exactamente 2 valores** (mínimo y máximo). CoolProp distribuye automáticamente las `num` isolíneas dentro de ese rango.

```python
# Correcto: iso_range con 2 valores
plot.calc_isolines(CP.iT, iso_range=[254, 1800], num=12)  # 12 isotermas entre 254 y 1800

# Incorrecto: iso_range con más de 2 valores (falla)
plot.calc_isolines(CP.iT, iso_range=[254, 300, 350, 1800], num=12)  # ERROR
```

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

### Sin especificar rango (CoolProp elige automáticamente)

```python
from CoolProp.Plots import PropertyPlot
import CoolProp.CoolProp as CP

plot = PropertyPlot('R134a', 'PH', unit_system='EUR')

# CoolProp determina el rango automáticamente
plot.calc_isolines(CP.iT, num=15)      # 15 isotermas
plot.calc_isolines(CP.iQ, num=10)      # 10 líneas de calidad

plot.draw_isolines()
plot.show()
```

### Especificando rango manualmente

```python
# Rango de isotermas entre 250K y 350K
T_range = [250, 350]
plot.calc_isolines(CP.iT, iso_range=T_range, num=12)

# Usando numpy (debe tener exactamente 2 valores)
T_range = np.linspace(250, 350, 2)  # [250, 350]
plot.calc_isolines(CP.iT, iso_range=T_range, num=12)
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
- `iso_range` debe contener **exactamente 2 valores** (mínimo y máximo).
- Para dibujar isolíneas en valores específicos (ej: solo 300K, 350K, 400K), no se puede con `calc_isolines`. Se debe dibujar manualmente con [[matplotlib.pyplot]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `property_type` inválido | Constante no definida | Usar `CP.iT`, `CP.iP`, `CP.iQ`, etc. |
| `iso_range` con más de 2 valores | Formato incorrecto | Usar `[min, max]` o `np.linspace(min, max, 2)` |
| Rango fuera de límites | Valores fuera del rango del fluido | Verificar rango válido del fluido |

## Notas relacionadas

- [[PropertyPlot]]
- [[PropertyPlot.draw_isolines]]
- [[PropertyPlot.show]]
- [[Constants]]
