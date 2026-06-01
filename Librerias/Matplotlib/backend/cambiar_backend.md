---
title: cambiar_backend — Cómo seleccionar el backend activo
aliases:
  - cambiar backend
  - matplotlib.use
  - MPLBACKEND
  - get_backend

tags:
  - matplotlib
  - api/config
  - render

# --- Clasificación ---
lib: matplotlib
mod: backend
tipo: config

# --- Comportamiento ---
retorna: None
muta_estado: false

# --- Dependencias ---
requiere:
  - concepto_backend
  - backends

draft: false
---

# cambiar_backend — Cómo seleccionar el backend activo

## Definición

Configura **qué motor de render** usa Matplotlib. La regla de oro: si fuerzas el backend por código, hazlo **antes de importar `pyplot`**, porque el backend queda fijado en el momento de la importación. Para el catálogo de motores disponibles ver [[backends]]; para el modelo conceptual ver [[concepto_backend|concepto de backend]].

## Formas de cambiar el backend

| Mecanismo | Dónde | Cuándo aplica |
|-----------|-------|---------------|
| `matplotlib.use("Agg")` | Código, antes de `import pyplot` | Scripts; forzar salida a archivo |
| `%matplotlib inline` / `widget` / `notebook` | Celda de Jupyter | Notebooks |
| Variable de entorno `MPLBACKEND` | Shell, antes de lanzar Python | CI/contenedores; sin tocar el código |
| `matplotlib.get_backend()` | Código | Consultar el backend actual |

## Parámetros / pasos

### 1. Por código: `matplotlib.use()`

```python
import matplotlib
matplotlib.use("Agg")            # debe ir ANTES de pyplot
import matplotlib.pyplot as plt  # toma el backend ya fijado
```

> Invertir el orden (importar `pyplot` y luego `use`) puede no tener efecto o emitir un warning: el backend ya estaba elegido.

### 2. En Jupyter: magics

```python
%matplotlib inline     # imágenes estáticas en la celda (default)
%matplotlib widget     # interactivo en JupyterLab (necesita ipympl)
%matplotlib notebook   # interactivo en Jupyter clásico (nbAgg)
```

### 3. Por entorno: `MPLBACKEND`

```bash
export MPLBACKEND=Agg        # fija el backend para toda la sesión
python script.py             # el script hereda Agg sin tocar el código
```

Útil en servidores y pipelines: separa la configuración del render del código del gráfico.

### 4. Consultar el backend activo

```python
import matplotlib
print(matplotlib.get_backend())   # → 'Agg'  (o 'QtAgg', 'module://...inline', etc.)
```

## Casos de uso

### Servidor sin pantalla (caso típico)

```python
import matplotlib
matplotlib.use("Agg")            # de archivo: evita el error "no display"
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2, 3])
fig.savefig("salida.png")        # no llama a plt.show()
```

### Forzar backend sin editar el script

```bash
MPLBACKEND=PDF python genera_figuras.py   # exporta en PDF vectorial
```

## Buenas prácticas

1. En servidores, contenedores y CI, fija `Agg` (o `MPLBACKEND=Agg`) y usa `savefig`, no `plt.show()`.
2. Llama a `matplotlib.use()` lo más arriba posible, antes de cualquier `import matplotlib.pyplot`.
3. Para reproducibilidad en equipos, prefiere `MPLBACKEND` en el entorno antes que `use()` disperso por el código.
4. Si dudas de qué motor corre, imprime `get_backend()` al inicio.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `use()` no surte efecto | Se importó `pyplot` antes de `use()` | Mover `use()` arriba, antes de `import pyplot` |
| `UserWarning: backend already chosen` | `use()` tardío | Reordenar imports o usar `MPLBACKEND` |
| "no display name and no $DISPLAY" | Backend interactivo en servidor | `matplotlib.use("Agg")` |
| El magic `%matplotlib widget` falla | Falta `ipympl` | Instalar `ipympl` y reiniciar kernel |

## Notas relacionadas

- [[backends]]
- [[concepto_backend]]
- [[plt.show]]
- [[plt.savefig]]
