---
title: fig.tight_layout — Ajuste automático de espaciados
aliases:
  - tight_layout
  - fig.tight_layout
tags:
  - matplotlib
  - api/metodo
  - layout
lib: matplotlib
obj: Figure
tipo: metodo
retorna: None
muta_estado: true
draft: false
---

# fig.tight_layout — Ajuste automático de espaciados

## Idea clave

`fig.tight_layout()` recalcula automáticamente los márgenes y la separación entre subplots para que **etiquetas, ticks y títulos no se solapen** ni se salgan del lienzo. Reposiciona los `Axes` dentro del `Figure` (de ahí `muta_estado: true`) pero no devuelve nada.

Opera sobre la jerarquía contenedora descrita en [[concepto_figure_axes]]: ajusta dónde se colocan los Axes dentro del lienzo.

---

## Firma

```python
Figure.tight_layout(
    pad=1.08,       # padding entre el borde de la figura y los Axes (fracción de fuente)
    h_pad=None,     # padding vertical entre subplots adyacentes
    w_pad=None,     # padding horizontal entre subplots adyacentes
    rect=None       # (left, bottom, right, top) región normalizada a ocupar
)
```

---

## Valor de retorno

| Entrada | Retorno | Ejemplo |
|---------|---------|---------|
| Cualquier llamada | `None` | `fig.tight_layout()  # → None` |

No retorna valor: su efecto es mutar las posiciones de los Axes en el Figure.

```python
r = fig.tight_layout()
print(r)        # → None
```

---

## Parámetros en detalle

### `pad` — margen general

```python
fig.tight_layout(pad=2.0)   # más aire alrededor de todo
fig.tight_layout(pad=0.5)   # más compacto
```

### `h_pad` / `w_pad` — separación entre subplots

```python
fig.tight_layout(h_pad=3.0, w_pad=1.0)   # más espacio vertical que horizontal
```

| Parámetro | Controla |
|-----------|----------|
| `pad` | Distancia al borde del Figure |
| `h_pad` | Hueco vertical entre filas de subplots |
| `w_pad` | Hueco horizontal entre columnas de subplots |
| `rect` | Caja normalizada a la que se confina el layout |

### `rect` — reservar espacio (p. ej. para un suptitle)

```python
fig.suptitle("Panel")
fig.tight_layout(rect=[0, 0, 1, 0.95])   # deja el 5% superior libre para el título
```

---

## Casos de uso

### Evitar etiquetas recortadas

```python
import matplotlib.pyplot as plt

fig, axs = plt.subplots(2, 2)
for ax in axs.flat:
    ax.set_xlabel("Tiempo (s)")
    ax.set_ylabel("Amplitud (V)")

fig.tight_layout()   # las etiquetas ya no se pisan entre subplots
```

### Combinado con título global

```python
fig, axs = plt.subplots(1, 3, figsize=(12, 4))
fig.suptitle("Comparación")
fig.tight_layout(rect=[0, 0, 1, 0.93])   # reserva banda para el suptitle
```

---

## Buenas prácticas

1. Llamar a `tight_layout()` **al final**, después de añadir todas las etiquetas, títulos y leyendas.
2. Si usas `fig.suptitle()`, reserva espacio con `rect` para que no quede tapado.
3. Para layouts complejos o animaciones, preferir `layout='constrained'` en [[plt.subplots]]: es más robusto y se ajusta dinámicamente.
4. Antes de `fig.savefig()`, aplicar `tight_layout()` para que la exportación no recorte texto.

---

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Etiquetas siguen recortadas | Se llamó antes de añadir labels | Llamar al final del script |
| Warning "tight_layout not applied" | Layout incompatible (ej. colorbars manuales) | Usar `constrained_layout` |
| Suptitle tapado | No se reservó banda superior | `tight_layout(rect=[0,0,1,0.95])` |
| Resultados inconsistentes con `constrained_layout` | Mezclar ambos mecanismos | Elegir uno solo |

---

## Limitaciones

`tight_layout()` es heurístico y se ejecuta una vez. Para figuras que cambian de tamaño, con colorbars compartidas o subplots anidados, `constrained_layout` (activado con `layout='constrained'` al crear la figura) ofrece un ajuste continuo y más fiable.

---

## Notas relacionadas

- [[concepto_figure_axes]]
- [[Figure]]
- [[plt.subplots]]
- [[fig.suptitle]]
