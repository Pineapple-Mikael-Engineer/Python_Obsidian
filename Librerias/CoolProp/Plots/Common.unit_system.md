---
title: Common.unit_system — Unidades de los ejes en los diagramas
aliases:
  - unit_system
  - sistemas de unidades de Plots
  - unidades de los diagramas

tags:
  - coolprop
  - api/config
  - plots

# --- Clasificación ---
lib: coolprop
mod: CoolProp.Plots

tipo: config

draft: false
---

# Common.unit_system — Unidades de los ejes en los diagramas

`unit_system` controla **en qué unidades se dibujan los ejes** de un [[PropertyPlot]]. CoolProp calcula siempre internamente en SI estricto (Pa, K, J/kg), pero un diagrama presión-entalpía o temperatura-entropía es mucho más legible si la presión va en kPa o bar y la entalpía en kJ/kg. `unit_system` es exactamente eso: una capa de **presentación** sobre los ejes; no cambia ningún cálculo termodinámico, solo cómo se rotulan y escalan las curvas que ya se han calculado en SI.

> [!important] Solo afecta a la visualización
> `unit_system` vive únicamente en el módulo `CoolProp.Plots`. El resto de CoolProp —[[CoolProp.PropsSI]] y [[AbstractState]]— ignora por completo esta opción y trabaja siempre en SI estricto. Ver [[concepto_propiedades_SI]].

> [!note] Requiere matplotlib
> `CoolProp.Plots` se apoya en `matplotlib` (debe estar instalado). Si el import falla con `ModuleNotFoundError: matplotlib`, instala `matplotlib` antes de usar `PropertyPlot` y, por tanto, `unit_system`.

## Sistemas disponibles

Se pasa como argumento `unit_system=` al construir el [[PropertyPlot]]. El valor por defecto es `'SI'`.

| Sistema | Presión | Temperatura | Energía |
|---------|---------|-------------|---------|
| `'SI'` | Pa | K | J (J/kg, J/(kg·K)) |
| `'KSI'` | kPa | K | kJ (kJ/kg, kJ/(kg·K)) |
| `'EUR'` | bar | °C | kJ (kJ/kg, kJ/(kg·K)) |

`'KSI'` (kilo-SI) es el más legible y el habitual en diagramas de ingeniería: mantiene la temperatura en kelvin pero pasa la presión a kPa y las energías a kJ, evitando los exponentes incómodos del SI puro. `'EUR'` es el sistema técnico europeo, cómodo en HVAC y refrigeración (presión en bar, temperatura en °C).

## Uso básico

```python
import matplotlib
matplotlib.use('Agg')                  # backend sin ventana (opcional, para guardar a archivo)
from CoolProp.Plots import PropertyPlot

# Diagrama P-h del agua con ejes en kPa y kJ/kg
plot = PropertyPlot('Water', 'PH', unit_system='KSI')
plot.calc_isolines()                   # isolíneas por defecto
plot.draw_isolines()                   # dibujarlas
plot.savefig('diagrama_ph_ksi.png')    # los ejes salen rotulados en kPa y kJ/kg
```

El mismo diagrama con `unit_system='SI'` mostraría la presión en Pa (hasta ~2.2e7) y la entalpía en J/kg; con `'KSI'` esas cifras quedan en kPa y kJ/kg, mucho más fáciles de leer en el eje.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ModuleNotFoundError: matplotlib` | `CoolProp.Plots` no encuentra matplotlib | Instalar `matplotlib` |
| Esperar que el SI cambie en `PropsSI` tras fijar `'KSI'` | `unit_system` es solo para los diagramas | Convertir a mano fuera de `Plots`; el resto de CoolProp siempre es SI |
| Ejes con valores inesperados | Mezclar el sistema del diagrama con datos propios en otras unidades | Dibujar tus puntos en las MISMAS unidades del `unit_system` elegido |

## Notas relacionadas

- [[PropertyPlot]]
- [[concepto_propiedades_SI]]
- [[CoolProp.PropsSI]]
- [[AbstractState]]
