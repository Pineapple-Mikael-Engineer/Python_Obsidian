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
    fluid: str,
    diagram_type: str,
    *,
    unit_system: str = 'SI',
    backend: str = 'HEOS'
)
```

## Parámetros del constructor

| Parámetro | Tipo | Descripción | Ejemplo |
|-----------|------|-------------|---------|
| `fluid` | `str` | Nombre del fluido | `'Water'`, `'R134a'` |
| `diagram_type` | `str` | Tipo de diagrama | `'PH'`, `'TS'`, `'HS'`, `'PS'` |
| `unit_system` | `str` | Sistema de unidades | `'SI'`, `'EUR'` |
| `backend` | `str` | Backend a utilizar | `'HEOS'`, `'IF97'` |

## Tipos de diagrama

| `diagram_type` | Nombre | Ejes | Uso típico |
|----------------|--------|------|------------|
| `'PH'` | Mollier / P-h | Presión - Entalpía | Ciclos de refrigeración, bombas de calor |
| `'TS'` | Temperatura - Entropía | Temperatura - Entropía | Ciclos Rankine, Brayton |
| `'HS'` | Mollier / h-s | Entalpía - Entropía | Turbinas, compresores |
| `'PS'` | Presión - Entropía | Presión - Entropía | Análisis de ciclos |

## Uso básico

```python
from CoolProp.Plots import PropertyPlot
import matplotlib.pyplot as plt

# Crear diagrama P-h para R134a
plot = PropertyPlot('R134a', 'PH', unit_system='SI')

# Dibujar isolíneas
plot.calc_isolines()
plot.draw_isolines()

# Mostrar
plot.show()
```

## Integración con matplotlib

`PropertyPlot` expone el objeto `figure` y `axis` internos, permitiendo personalización avanzada con matplotlib.

### Acceder a figure y axis

```python
plot = PropertyPlot('Water', 'TS')

# Acceder a la figura y ejes de matplotlib
fig = plot.figure
ax = plot.axis

# Ahora usar matplotlib directamente
ax.grid(True, linestyle='--', alpha=0.7)
ax.set_facecolor('#f0f0f0')
fig.suptitle('Diagrama Personalizado', fontsize=14)
```

### Añadir elementos con matplotlib

```python
plot = PropertyPlot('R134a', 'PH', unit_system='EUR')
plot.calc_isolines()
plot.draw_isolines()

# Añadir puntos personalizados
ax = plot.axis
ax.plot(400, 5, 'ro', markersize=8, label='Punto 1')
ax.plot(420, 8, 'bs', markersize=8, label='Punto 2')
ax.legend()

# Añadir anotaciones
ax.annotate('Evaporador', xy=(400, 5), xytext=(380, 10),
            arrowprops=dict(arrowstyle='->'))

plot.show()
```

### Combinar con subplots de matplotlib

```python
import matplotlib.pyplot as plt
from CoolProp.Plots import PropertyPlot

# Crear figura con 2 subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Diagrama P-h en primer subplot
plot_ph = PropertyPlot('Water', 'PH')
plot_ph.axis = ax1  # Asignar ejes existentes
plot_ph.calc_isolines()
plot_ph.draw_isolines()
ax1.set_title('Diagrama P-h')

# Diagrama T-s en segundo subplot
plot_ts = PropertyPlot('Water', 'TS')
plot_ts.axis = ax2
plot_ts.calc_isolines()
plot_ts.draw_isolines()
ax2.set_title('Diagrama T-s')

plt.tight_layout()
plt.show()
```

### Guardar con matplotlib

```python
plot = PropertyPlot('R290', 'PH')
plot.calc_isolines()
plot.draw_isolines()

# Usar matplotlib para guardar
plt.savefig('diagrama.png', dpi=300, bbox_inches='tight')

# O usar método de PropertyPlot
plot.savefig('diagrama_v2.png', dpi=300)
```

### Personalización avanzada con rcParams

```python
import matplotlib.pyplot as plt

# Configurar estilo global de matplotlib
plt.rcParams['font.size'] = 12
plt.rcParams['lines.linewidth'] = 1.5

plot = PropertyPlot('R134a', 'PH')
plot.calc_isolines()
plot.draw_isolines()

# Los cambios de rcParams se aplican al diagrama
plot.show()
```

## Configuración de ejes y título

```python
plot = PropertyPlot('Water', 'TS')

# Configurar ejes
plot.axis_limits(x_min=0, x_max=10, y_min=0, y_max=2000)

# Título
plot.title('Diagrama T-s del Agua')

# Etiquetas personalizadas
plot.xlabel('Entropía (kJ/kg·K)')
plot.ylabel('Temperatura (K)')
```

## Guardar figura

```python
plot.savefig('diagrama_ph_r134a.png', dpi=300)
```

## Sistema de unidades

```python
# SI (default): Pa, K, J/kg
plot_si = PropertyPlot('Water', 'PH', unit_system='SI')

# EUR: bar, °C, kJ/kg (más común en ingeniería europea)
plot_eur = PropertyPlot('Water', 'PH', unit_system='EUR')
```

## Ejemplo completo con integración matplotlib

```python
from CoolProp.Plots import PropertyPlot
import CoolProp.CoolProp as CP
import matplotlib.pyplot as plt

# Crear diagrama
plot = PropertyPlot('R134a', 'PH', unit_system='EUR')

# Calcular y dibujar isolíneas
plot.calc_isolines(CP.iQ, num=10)      # Líneas de calidad
plot.calc_isolines(CP.iT, num=10)      # Líneas isotermas
plot.draw_isolines()

# Personalización con matplotlib
ax = plot.axis
ax.grid(True, linestyle=':', alpha=0.5)
ax.set_xlim(200, 500)
ax.set_ylim(1, 20)
ax.set_title('Diagrama P-h de R134a', fontsize=14, fontweight='bold')
ax.set_xlabel('Entalpía (kJ/kg)')
ax.set_ylabel('Presión (bar)')

# Añadir ciclo de refrigeración
# Evaporación
ax.plot([390, 410], [2, 2], 'r-', linewidth=2)
# Compresión
ax.plot([410, 430], [2, 10], 'r-', linewidth=2)
# Condensación
ax.plot([430, 240], [10, 10], 'r-', linewidth=2)
# Expansión
ax.plot([240, 390], [10, 2], 'r--', linewidth=1.5)

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
