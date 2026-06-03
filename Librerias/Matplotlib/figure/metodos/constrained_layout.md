---
title: constrained_layout — Motor de layout automático
aliases:
  - constrained_layout
  - layout constrained
  - motor de layout
tags:
  - matplotlib
  - api/config
  - layout

# --- Clasificación ---
lib: matplotlib
obj: Figure
tipo: config

# --- Comportamiento ---
muta_estado: true

draft: false
---

# constrained_layout — Motor de layout automático

## Definición

`constrained_layout` es un **motor de layout** de matplotlib que recalcula automáticamente los espaciados (márgenes, separación entre subplots, hueco para colorbars y leyendas) de modo que ningún elemento decorativo se solape. A diferencia de un método puntual, es un **estado de la figura**: una vez activo, se vuelve a aplicar en cada redibujado.

Se activa de tres formas equivalentes:

```python
fig, ax = plt.subplots(layout='constrained')   # forma moderna (recomendada)
fig.set_layout_engine('constrained')            # activarlo tras crear la figura
plt.figure(constrained_layout=True)             # kwarg histórico
```

Es la alternativa **moderna y más robusta** a [[fig.tight_layout]]. No los mezcles: `tight_layout` se ejecuta una sola vez y puede chocar con el motor constrained si ambos intentan gestionar el mismo espaciado.

## Valor de retorno

| Forma de uso | Retorna | Efecto |
|--------------|---------|--------|
| `plt.subplots(layout='constrained')` | `(Figure, Axes)` | crea la figura ya con el motor activo |
| `fig.set_layout_engine('constrained')` | `None` | muta la figura: instala el motor |
| `fig.get_layout_engine()` | `LayoutEngine` | objeto motor para ajustar parámetros |

No produce un objeto de datos: su efecto es **mutar el estado de layout** de la `Figure`.

## Parámetros en detalle

Los parámetros se pasan al instalar el motor con `set_layout_engine` o vía `fig.get_layout_engine().set(...)`.

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `w_pad`, `h_pad` | `float` (pulgadas) | `0.04167` | Padding alrededor de cada Axes (horizontal / vertical) |
| `wspace`, `hspace` | `float` (fracción) | `0` | Espacio entre subplots como fracción del ancho/alto del Axes |
| `rect` | `tuple` | `(0,0,1,1)` | Rectángulo `(left, bottom, w, h)` donde encajar todo el layout |

```python
fig.set_layout_engine('constrained')
fig.get_layout_engine().set(w_pad=0.1, hspace=0.05)
```

## Casos de uso

### Evitar labels recortados sin esfuerzo

```python
fig, axs = plt.subplots(2, 2, layout='constrained')
for ax in axs.flat:
    ax.set_xlabel("eje X largo que se recortaría")
    ax.set_ylabel("eje Y")
# los labels no se solapan ni se cortan: el motor lo resuelve
```

### Hueco automático para colorbar

```python
fig, ax = plt.subplots(layout='constrained')
im = ax.imshow(datos)
fig.colorbar(im, ax=ax)   # constrained reserva el espacio sin descuadrar el Axes
```

### Activarlo después de crear la figura

```python
fig, axs = plt.subplots(1, 3)
fig.set_layout_engine('constrained')   # muta la figura ya existente
```

### Ajustar el padding global

```python
fig, axs = plt.subplots(2, 2, layout='constrained')
fig.get_layout_engine().set(w_pad=0.15, h_pad=0.15)
```

## Buenas prácticas

1. Prefiérelo como motor por defecto: pásalo con `layout='constrained'` al crear la figura en lugar de llamar a [[fig.tight_layout]] al final.
2. Es ideal cuando hay colorbars, leyendas externas o labels largos, escenarios donde `tight_layout` suele quedarse corto.
3. No combines `constrained` con `tight_layout` ni con `subplots_adjust`: producen ajustes en conflicto.
4. Combínalo con [[plt.subplot_mosaic]], que ya lo usa por defecto.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Layout no se ajusta | la figura usa el motor `'tight'` o ninguno | crea con `layout='constrained'` o `set_layout_engine` |
| Warning de motores en conflicto | se llamó a `tight_layout()` con constrained activo | elige uno solo de los dos |
| `subplots_adjust` ignorado | constrained controla el espaciado | desactiva constrained o usa `w_pad`/`h_pad` |
| Inset descuadrado | un Axes posicionado a mano con [[fig.add_axes]] | el motor no gestiona ejes de posición fija |

## Notas relacionadas

- [[fig.tight_layout]]
- [[plt.subplots]]
- [[plt.subplot_mosaic]]
- [[concepto_figure_axes]]
