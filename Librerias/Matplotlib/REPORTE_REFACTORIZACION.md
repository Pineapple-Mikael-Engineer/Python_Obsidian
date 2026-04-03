---
title: Reporte de Refactorización - Matplotlib
draft: true
---

# Reporte de Refactorización

## Resumen
- Total notas procesadas: 18
- Notas movidas/renombradas: 14
- Notas draft:true ignoradas: 2
- Links renombrados: 20
- Ambigüedades encontradas: 5

## Notas movidas correctamente
| Nombre original | Nueva ruta | Nuevo nombre |
|----------------|------------|--------------|
| plt.subplots.md | Matplotlib/pyplot/funciones/ | plt.subplots.md |
| GridSpec.md | Matplotlib/gridspec/ | GridSpec.md |
| ax.grid.md | Matplotlib/axes/metodos/formato/ | ax.grid.md |
| Locators.md | Matplotlib/ticker/ | Locators.md |
| ax.tick_params.md | Matplotlib/axes/metodos/formato/ | ax.tick_params.md |
| ax.scatter.md | Matplotlib/axes/metodos/graficos/ | ax.scatter.md |
| ax.plot.md | Matplotlib/axes/metodos/graficos/ | ax.plot.md |
| ax.contour.md | Matplotlib/axes/metodos/graficos/ | ax.contour.md |
| ax.bar.md | Matplotlib/axes/metodos/graficos/ | ax.bar.md |
| ax.barh.md | Matplotlib/axes/metodos/graficos/ | ax.barh.md |
| ax.hist.md | Matplotlib/axes/metodos/graficos/ | ax.hist.md |
| ax.fill_between.md | Matplotlib/axes/metodos/graficos/ | ax.fill_between.md |
| ax.set_title.md | Matplotlib/axes/metodos/formato/ | ax.set_title.md |
| ax.legend.md | Matplotlib/axes/metodos/formato/ | ax.legend.md |

## Notas draft:true ignoradas
| Ruta original | Motivo |
|---------------|--------|
| Librerias/Matplotlib/Tree Matplotlib.md | draft:true (intocable por regla) |
| Librerias/Matplotlib/Multiples_Graficos/Ejes Compartidos.md | draft:true (intocable por regla) |

## Ambigüedades / Problemas (SOLO ESTO SE REPORTA)
| Tipo | Elemento | Nota origen | Posibles opciones | Decisión tomada |
|------|----------|-------------|-------------------|-----------------|
| Nota ambigua | Configuración.md | Librerias/Matplotlib/Configuración.md | `config/rcParams.md`, `config/estilos.md` | No mover/renombrar |
| Nota ambigua | Manejo Arrays Axes.md | Librerias/Matplotlib/Figura_Ejes/Manejo Arrays Axes.md | `axes/Axes.md`, nota nueva fuera del árbol objetivo | No mover/renombrar |
| Nota ambigua | ax.set_xlabel_ylabel.md | Librerias/Matplotlib/Labels_Leyendas/ax.set_xlabel_ylabel.md | `ax.set_xlabel.md`, `ax.set_ylabel.md` | No mover/renombrar |
| Nota ambigua | ax.set_xticks_yticks.md | Librerias/Matplotlib/Ejes_Formato/Ticks/ax.set_xticks_yticks.md | `ax.set_xticks.md`, `ax.set_yticks.md` | No mover/renombrar |
| Nota fuera de árbol objetivo | ax.fill_betweenx.md | Librerias/Matplotlib/Tipos_Plot/Otros/ax.fill_betweenx.md | integrar en `ax.fill_between.md` o crear `ax.fill_betweenx.md` fuera de estándar dado | No mover/renombrar |
