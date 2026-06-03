---
title: plt.savefig — Guardar la figura actual a archivo
aliases:
  - savefig
  - plt.savefig
tags:
  - matplotlib
  - api/funcion
  - figura
lib: matplotlib
obj: pyplot
tipo: funcion
retorna: None
muta_estado: false
draft: false
---

# plt.savefig — Guardar la figura actual a archivo

## Idea clave

`plt.savefig()` renderiza la **figura actual** y la escribe a disco. No abre ventanas ni necesita pantalla: dispara el render a través del [[concepto_backend|backend]] de archivo (`Agg` para PNG, vectorial para PDF/SVG). El **formato se deduce de la extensión** del nombre.

Es la versión de estado de pyplot equivalente al método OO `fig.savefig` (interfaz de [[Figure]]).

## Firma de la función

```python
matplotlib.pyplot.savefig(
    fname,                  # str | Path | objeto archivo
    dpi=None,               # resolución; 'figure' usa la dpi de la figura
    facecolor='auto',       # color de fondo al exportar
    edgecolor='auto',       # color del borde
    format=None,            # fuerza el formato (si fname no lo indica)
    transparent=False,      # fondo transparente
    bbox_inches=None,       # 'tight' recorta márgenes en blanco
    pad_inches=0.1,         # padding al usar bbox_inches='tight'
    **kwargs
)
```

## Valor de retorno

| Entrada | Retorno | Ejemplo |
|---------|---------|---------|
| ruta válida | `None` (efecto: archivo en disco) | `plt.savefig("fig.png")` |
| extensión `.pdf` | `None`, salida vectorial PDF | `plt.savefig("fig.pdf")` |
| extensión `.svg` | `None`, salida vectorial SVG | `plt.savefig("fig.svg")` |

```python
plt.savefig("salida.png", dpi=300, bbox_inches="tight")
# → None  (crea salida.png en el cwd)
```

## Parámetros en detalle

### `fname` y formato

```python
plt.savefig("grafico.png")   # raster PNG (Agg)
plt.savefig("grafico.pdf")   # vectorial, ideal para papers
plt.savefig("grafico.svg")   # vectorial, editable en navegador/Inkscape
```

| Extensión | Tipo | Uso típico |
|-----------|------|------------|
| `.png` | raster | web, notebooks, presentaciones |
| `.pdf` | vectorial | publicaciones, LaTeX |
| `.svg` | vectorial | edición posterior, web escalable |
| `.jpg` | raster | fotos, sin transparencia |

### `dpi` — resolución de exportación

```python
plt.savefig("fig.png", dpi=300)   # calidad de impresión
```

Solo afecta a formatos raster. En vectoriales el detalle es infinito.

### `bbox_inches='tight'` — recortar bordes

```python
plt.savefig("fig.png", bbox_inches="tight", pad_inches=0.05)
```

Elimina el espacio en blanco sobrante alrededor de la figura. Imprescindible cuando hay leyendas o títulos que se salen del área.

### `transparent` — fondo transparente

```python
plt.savefig("logo.png", transparent=True)   # sin fondo, para superponer
```

## Casos de uso

### Caso 1: exportar con estilo OO (recomendado)

```python
fig, ax = plt.subplots()
ax.plot(x, y)
fig.savefig("resultado.png", dpi=150, bbox_inches="tight")
```

### Caso 2: guardar muchas figuras en bucle

```python
for i, datos in enumerate(series):
    fig, ax = plt.subplots()
    ax.plot(datos)
    fig.savefig(f"fig_{i:03d}.png", dpi=120)
    plt.close(fig)   # liberar memoria entre iteraciones
```

> En un servidor o CI sin pantalla, `savefig` funciona con backend `Agg`, mientras que [[plt.show]] no tendría dónde dibujar.

## Buenas prácticas

1. Llama `savefig` **antes** que [[plt.show]]: algunos backends interactivos limpian la figura tras mostrarla.
2. Usa `bbox_inches='tight'` para evitar márgenes y recortes de leyendas.
3. PDF/SVG para publicación; PNG con `dpi>=200` para raster nítido.
4. En bucles, cierra cada figura con `plt.close(fig)` para no agotar memoria.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Imagen en blanco / vacía | `savefig` después de `show()` que vació la figura | guardar antes de mostrar |
| Leyenda cortada en el borde | falta recorte de márgenes | `bbox_inches='tight'` |
| Formato no reconocido | extensión ausente o rara | pasar `format='png'` explícito |
| Fondo blanco no deseado | `transparent=False` por defecto | `transparent=True` |

## Limitaciones

Guarda **una sola figura** (la actual o `fig`). Para múltiples páginas en un PDF usa `matplotlib.backends.backend_pdf.PdfPages`.

## Notas relacionadas

- [[concepto_backend]]
- [[Figure]]
- [[plt.show]]
- [[plt.close]]
- [[plt.subplots]]
