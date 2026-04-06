---
title: PropertyPlot — Diagramas termodinámicos
aliases:
  - PropertyPlot
  - diagramas
  - plots
  - graficos_termodinamicos

tags:
  - coolprop
  - api/clase
  - plots
  - graficos

# --- Clasificación ---
lib: coolprop
obj: PropertyPlot
tipo: clase

# --- Comportamiento ---
muta_estado: true

draft: false
---

# PropertyPlot — Diagramas termodinámicos

## Descripción

`PropertyPlot` es la clase principal del módulo `Plots` de CoolProp. Permite generar diagramas termodinámicos estándar (P-H, T-s, H-s, etc.) con isolíneas automáticas.

**Motor interno:** `PropertyPlot` está construido sobre `matplotlib`. No hereda directamente de clases de matplotlib, pero utiliza `Figure` y `Axes` internamente, lo que permite combinarlo con funciones estándar de matplotlib.

**Dependencia:** Requiere `matplotlib` instalado.

## Firma del constructor

```python
class PropertyPlot(
    fluid_ref: Union[str, AbstractState],
    graph_type: str,
    *,
    unit_system: str = 'SI',
    tp_limits: str = 'DEF',
    **kwargs
)
```

## Parámetros del constructor

| Parámetro | Tipo | Descripción | Ejemplo |
|-----------|------|-------------|---------|
| `fluid_ref` | `str` o `AbstractState` | Nombre del fluido o instancia de `AbstractState` | `'Water'`, `state` |
| `graph_type` | `str` | Tipo de diagrama (ver tabla) | `'PH'`, `'TS'`, `'HS'` |
| `unit_system` | `str` | Sistema de unidades | `'SI'`, `'EUR'`, `'KSI'` |
| `tp_limits` | `str` | Límites predefinidos del diagrama | `'DEF'`, `'ACHP'`, `'ORC'`, `'NONE'` |
| `**kwargs` | `dict` | Argumentos adicionales para matplotlib | `figsize=(10, 8)` |

## Tipos de diagrama (graph_type)

| Valor | Nombre | Ejes | Uso típico |
|-------|--------|------|------------|
| `'PH'` | Mollier / P-h | Presión - Entalpía | Ciclos de refrigeración, bombas de calor |
| `'TS'` | Temperatura - Entropía | Temperatura - Entropía | Ciclos Rankine, Brayton |
| `'HS'` | Mollier / h-s | Entalpía - Entropía | Turbinas, compresores |
| `'PS'` | Presión - Entropía | Presión - Entropía | Análisis de ciclos |
| `'PT'` | Presión - Temperatura | Presión - Temperatura | Curvas de saturación |
| `'TD'` | Temperatura - Densidad | Temperatura - Densidad | Propiedades de fluidos |
| `'PD'` | Presión - Densidad | Presión - Densidad | Compresibilidad |

## Sistemas de unidades (unit_system)

| Sistema | Presión | Temperatura | Entalpía / Entropía | Uso típico |
|---------|---------|-------------|---------------------|------------|
| `'SI'` | Pa | K | J/kg, J/(kg·K) | Científico (default) |
| `'KSI'` | kPa | K | kJ/kg, kJ/(kg·K) | Ingeniería |
| `'EUR'` | bar | °C | kJ/kg, kJ/(kg·K) | Europeo (común en HVAC) |

```python
# Sistema europeo (más común en ingeniería práctica)
plot = PropertyPlot('R134a', 'PH', unit_system='EUR')
```

## Límites predefinidos (tp_limits)

| Valor | Aplicación | Rango típico |
|-------|------------|--------------|
| `'DEF'` | Por defecto | Factor 1.01-2.25 alrededor del punto crítico |
| `'ACHP'` | Aire acondicionado / bomba de calor | Presiones típicas de evaporación y condensación |
| `'ORC'` | Ciclo Rankine orgánico | Temperaturas bajas a medias |
| `'NONE'` | Sin límites predefinidos | El usuario define ejes manualmente |

## Uso básico

```python
from CoolProp.Plots import PropertyPlot
import CoolProp.CoolProp as CP

# Crear diagrama P-h para R134a (sistema europeo)
plot = PropertyPlot('R134a', 'PH', unit_system='EUR')

# Calcular isolíneas
plot.calc_isolines(CP.iT, num=15)      # Isotermas
plot.calc_isolines(CP.iQ, num=10)      # Líneas de calidad

# Dibujar
plot.draw_isolines()
plot.show()
```

## Integración con matplotlib

`PropertyPlot` expone los objetos `figure` y `axis` internos para personalización avanzada.

### Acceder a figure y axis

```python
plot = PropertyPlot('Water', 'TS')

fig = plot.figure  # Figura de matplotlib
ax = plot.axis     # Ejes de matplotlib

# Personalización directa
ax.grid(True, linestyle='--', alpha=0.7)
ax.set_facecolor('#f0f0f0')
fig.suptitle('Diagrama Personalizado', fontsize=14)
```

### Añadir puntos y líneas personalizados

```python
plot = PropertyPlot('R134a', 'PH', unit_system='EUR')
plot.calc_isolines(CP.iT, num=12)
plot.draw_isolines()

ax = plot.axis

# Añadir punto de evaporación
ax.plot(400, 2, 'ro', markersize=8, label='Evaporador')

# Añadir punto de condensación
ax.plot(430, 10, 'bs', markersize=8, label='Condensador')

ax.legend()
plot.show()
```

### Crear subplots

```python
import matplotlib.pyplot as plt
from CoolProp.Plots import PropertyPlot

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Diagrama P-h en primer subplot
plot_ph = PropertyPlot('Water', 'PH')
plot_ph.axis = ax1
plot_ph.calc_isolines(CP.iT, num=10)
plot_ph.draw_isolines()
ax1.set_title('Diagrama P-h')

# Diagrama T-s en segundo subplot
plot_ts = PropertyPlot('Water', 'TS')
plot_ts.axis = ax2
plot_ts.calc_isolines(CP.iP, num=10)
plot_ts.draw_isolines()
ax2.set_title('Diagrama T-s')

plt.tight_layout()
plt.show()
```

## Control de ejes

```python
# Establecer límites manualmente
plot.axis_limits(x_min=200, x_max=600, y_min=1, y_max=20)

# Título y etiquetas personalizadas
plot.title('Diagrama P-h de R134a')
plot.xlabel('Entalpía (kJ/kg)')
plot.ylabel('Presión (bar)')
```

## Guardar figura

```python
# Usando método de PropertyPlot
plot.savefig('diagrama.png', dpi=300)

# Usando matplotlib directamente
import matplotlib.pyplot as plt
plt.savefig('diagrama.pdf')
```

## Ejemplo completo: Ciclo de refrigeración

```python
from CoolProp.Plots import PropertyPlot
import CoolProp.CoolProp as CP
import matplotlib.pyplot as plt

# Crear diagrama
plot = PropertyPlot('R134a', 'PH', unit_system='EUR')
plot.calc_isolines(CP.iT, num=10)
plot.calc_isolines(CP.iQ, num=8)
plot.draw_isolines()

# Configurar ejes
plot.title('Ciclo de Refrigeración R134a')
plot.xlabel('Entalpía (kJ/kg)')
plot.ylabel('Presión (bar)')

# Datos del ciclo (valores de ejemplo)
evap_P = 2    # bar
cond_P = 10   # bar

# Dibujar ciclo
ax = plot.axis

# Evaporación (isobara a baja presión)
ax.hlines(evap_P, 380, 400, 'r', linewidth=2)
# Compresión
ax.plot([400, 425], [2, 10], 'r', linewidth=2)
# Condensación (isobara a alta presión)
ax.hlines(cond_P, 425, 240, 'r', linewidth=2)
# Expansión
ax.plot([240, 380], [10, 2], 'r--', linewidth=1.5)

plt.show()
```

## Notas relacionadas

- [[PropertyPlot.calc_isolines]]
- [[PropertyPlot.draw_isolines]]
- [[PropertyPlot.show]]
- [[PropertyPlot.savefig]]
- [[Common.unit_system]]
- [[AbstractState]]
- [[matplotlib.pyplot]]
