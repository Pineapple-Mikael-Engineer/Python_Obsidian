---
title: backends — Motores de render disponibles
aliases:
  - backends
  - lista de backends
  - Agg
  - TkAgg

tags:
  - matplotlib
  - api/objeto
  - render

# --- Clasificación ---
lib: matplotlib
mod: backend
tipo: objeto

# --- Comportamiento ---
retorna: None
muta_estado: false

# --- Dependencias ---
requiere:
  - concepto_backend

draft: false
---

# backends — Motores de render disponibles

## Definición

Un **backend** es el motor que convierte la estructura de Artists en memoria en una salida concreta: una ventana, una celda de notebook o un archivo de imagen. Esta nota es la **referencia de catálogo**: qué backends existen y cuándo elegir cada uno. Para el modelo mental completo (cuándo ocurre el render, `show` vs `savefig`) ver el [[concepto_backend|concepto de backend]].

**Idea clave:** el mismo código de ploteo produce salidas distintas según el backend activo, sin tocar una línea del gráfico.

## Dos familias de backends

| Familia | Para qué | Pinta en |
|---------|----------|----------|
| **Interactivos** | abrir ventanas, hacer zoom, paneo | pantalla / celda |
| **No interactivos** (de archivo) | generar imágenes sin pantalla | archivo en disco |

## Catálogo de backends

| Backend | Familia | Salida | Cuándo usarlo |
|---------|---------|--------|---------------|
| `Agg` | No interactivo | PNG (raster) | Servidores/CI sin pantalla; `savefig` |
| `PDF` | No interactivo | PDF (vectorial) | Documentos, papers |
| `SVG` | No interactivo | SVG (vectorial) | Web, gráficos escalables |
| `PS` | No interactivo | PostScript/EPS | Publicación clásica |
| `TkAgg` | Interactivo | ventana (Tk) | Default habitual en escritorio |
| `QtAgg` | Interactivo | ventana (Qt) | Entornos Qt; mejor rendimiento |
| `MacOSX` | Interactivo | ventana nativa | macOS sin toolkit externo |
| `nbAgg` | Interactivo | celda notebook | Jupyter clásico (`%matplotlib notebook`) |
| `inline` | Estático | imagen en celda | Jupyter por defecto (`%matplotlib inline`) |
| `widget` / `ipympl` | Interactivo | celda notebook | JupyterLab interactivo (`%matplotlib widget`) |

`Agg` (*Anti-Grain Geometry*) es el rasterizador por defecto que produce los PNG; varios backends interactivos (`TkAgg`, `QtAgg`) lo usan por dentro para dibujar el lienzo.

## Casos de uso

### Render a archivo sin pantalla

```python
import matplotlib
matplotlib.use("Agg")          # de archivo: no necesita display
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2, 3])
fig.savefig("grafico.png")     # produce el PNG vía Agg
```

### Salida vectorial para un paper

```python
matplotlib.use("PDF")
fig.savefig("figura.pdf")      # vectorial, escalable sin pérdida
```

### Ventana interactiva en escritorio

```python
matplotlib.use("QtAgg")
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([1, 2, 3])
plt.show()                     # abre ventana Qt y bloquea el script
```

## Buenas prácticas

1. En servidores, CI o contenedores sin display, usa siempre un backend **de archivo** (`Agg`, `PDF`, `SVG`) y exporta con `savefig`.
2. Para gráficos que se ampliarán (web, impresión grande), prefiere salida **vectorial** (`SVG`, `PDF`) sobre `Agg` (raster).
3. No mezcles `plt.show()` con un backend no interactivo: no tiene dónde dibujar.
4. En notebooks, deja `inline` para informes estáticos y `widget` solo cuando necesites interacción.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `plt.show()` no abre nada | Backend de archivo activo (`Agg`) | Usar `savefig`, o un backend interactivo |
| Error "no display name" en servidor | Backend interactivo sin pantalla | `matplotlib.use("Agg")` |
| PNG borroso al ampliar | `Agg` es raster | Exportar a `SVG`/`PDF` |
| `widget` no responde en Jupyter | Falta `ipympl` instalado | Instalar `ipympl` y reiniciar el kernel |

## Notas relacionadas

- [[concepto_backend]]
- [[cambiar_backend]]
- [[plt.show]]
- [[plt.savefig]]
