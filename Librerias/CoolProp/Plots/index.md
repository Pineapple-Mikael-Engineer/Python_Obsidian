---
title: Plots — diagramas termodinámicos con PropertyPlot
tags: [coolprop, indice]
draft: false
---

# Plots — diagramas termodinámicos con PropertyPlot

El submódulo `CoolProp.Plots` dibuja los **diagramas termodinámicos** clásicos —presión-entalpía (P-h), temperatura-entropía (T-s), presión-temperatura (P-T)…— con sus **isolíneas** (curvas de temperatura, calidad, entropía o densidad constante) y la **campana de saturación**. Es la forma de visualizar dónde cae un estado o un ciclo (Rankine, refrigeración) sobre el mapa del fluido.

El objeto central es [[PropertyPlot]]; el resto de notas son sus métodos.

## En acción

```python
from CoolProp.Plots import PropertyPlot

# Diagrama presion-entalpia del agua
plot = PropertyPlot("Water", "Ph")   # fluido, tipo de diagrama (Ph, Ts, PT, prho...)
plot.calc_isolines()                 # calcula las familias de isolineas por defecto
plot.draw_isolines()                 # las dibuja sobre los ejes
plot.savefig("diagrama_ph.png")      # exportar
plot.show()                          # o mostrar en pantalla
```

## El flujo de una gráfica

```mermaid
flowchart LR
    P["PropertyPlot(fluido, tipo)"] --> CI["calc_isolines() — calcular curvas"]
    CI --> DI["draw_isolines() — dibujarlas"]
    DI --> O(["show() · savefig()"])

    classDef base fill:#5e81ac,stroke:#88c0d0,stroke-width:2px,color:#eceff4;
    classDef grupo fill:#3b4252,stroke:#81a1c1,stroke-width:1.5px,color:#88c0d0;
    classDef hoja fill:#2e3440,stroke:#a3be8c,color:#d8dee9;
    class P base;
    class CI,DI grupo;
    class O hoja;
```

Internamente `PropertyPlot` envuelve una `Figure`/`Axes` de Matplotlib, así que puedes seguir ajustando el gráfico con la API de Matplotlib si lo necesitas.

## Las notas

- [[PropertyPlot]] — el objeto principal: crea el diagrama para un fluido y un tipo de eje (`Ph`, `Ts`, `PT`, `prho`…) e incluye la campana de saturación.
- [[PropertyPlot.calc_isolines]] — calcula las isolíneas (temperatura, calidad, entropía, densidad constantes) que se superpondrán al diagrama.
- [[PropertyPlot.draw_isolines]] — dibuja sobre los ejes las isolíneas calculadas.
- [[PropertyPlot.savefig]] — exporta el diagrama a un archivo de imagen.
- [[PropertyPlot.show]] — muestra el diagrama en pantalla.

## Tabla de decisión

| Quiero… | Usar |
|---------|------|
| Crear un diagrama (P-h, T-s…) | [[PropertyPlot]] |
| Añadir isolíneas (T, Q, s, ρ constantes) | [[PropertyPlot.calc_isolines]] + [[PropertyPlot.draw_isolines]] |
| Guardar la figura | [[PropertyPlot.savefig]] |
| Mostrarla en pantalla | [[PropertyPlot.show]] |

## Notas relacionadas

- [[AbstractState]] — el cálculo de propiedades que hay detrás de cada punto del diagrama
- [[CoolProp.PropsSI]] — para obtener los valores numéricos que sitúas sobre el diagrama
