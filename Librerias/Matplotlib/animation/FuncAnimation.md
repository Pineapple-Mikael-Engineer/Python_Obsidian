---
title: FuncAnimation — Animación por re-dibujado de Artists
aliases:
  - FuncAnimation
  - animation.FuncAnimation
  - animacion

tags:
  - matplotlib
  - api/clase
  - animacion

# --- Clasificación ---
lib: matplotlib
obj: FuncAnimation
mod: animation
tipo: clase

# --- Comportamiento ---
retorna: Animation
muta_estado: false

# --- Dependencias ---
requiere:
  - concepto_backend
  - concepto_artist

draft: false
---

# FuncAnimation — Animación por re-dibujado de Artists

## Definición

`FuncAnimation` es la clase del módulo `matplotlib.animation` que construye una **animación** llamando repetidamente a una función `func(frame)` que **actualiza los Artists** de una figura ya existente. No crea nuevos ejes en cada cuadro: muta el contenido de los Artists (datos de líneas, posiciones, textos) y pide al [[concepto_backend|backend]] que redibuje.

La instancia que devuelve **debe guardarse en una variable**. Si no se conserva la referencia, el recolector de basura la elimina y la animación nunca corre.

## Firma de la función

```python
matplotlib.animation.FuncAnimation(
    fig,              # Figure sobre la que se anima
    func,             # función func(frame, *fargs) que actualiza los Artists
    frames=None,      # iterable, int (range), generador o None
    init_func=None,   # estado inicial; útil con blit=True
    interval=200,     # ms entre cuadros
    blit=False,       # redibuja solo lo que cambia (optimización)
    repeat=True,      # reinicia al terminar
    fargs=None,       # args extra para func/init_func
)
```

## Parámetros en detalle

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `fig` | `Figure` | — | Figura donde se renderiza la animación |
| `func` | `callable` | — | Recibe el `frame` actual; actualiza los Artists. Con `blit=True` debe **retornar** la lista de Artists modificados |
| `frames` | `int`, iterable, generador, `None` | `None` | Fuente de cuadros. `int` equivale a `range(int)` |
| `init_func` | `callable` | `None` | Dibuja el fotograma base limpio antes del primer cuadro |
| `interval` | `int` | `200` | Milisegundos entre cuadros (200 ms = 5 fps) |
| `blit` | `bool` | `False` | Si `True`, solo se redibujan los Artists que cambian (más fluido) |
| `repeat` | `bool` | `True` | Vuelve a empezar tras el último cuadro |

### `func(frame)` — el corazón de la animación

```python
def update(frame):
    linea.set_ydata(np.sin(x + frame / 10))  # muta el Artist, no recrea
    return (linea,)                           # tupla obligatoria si blit=True
```

### `blit` — qué redibuja

| `blit` | Qué hace | Cuándo usar |
|--------|----------|-------------|
| `False` | Redibuja la figura completa cada cuadro | Simple; fondos/ejes que cambian |
| `True` | Redibuja solo los Artists devueltos por `func` | Animaciones fluidas; `func`/`init_func` deben retornar los Artists |

## Casos de uso

### Animar una señal (guardando la referencia)

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
x = np.linspace(0, 2 * np.pi, 200)
(linea,) = ax.plot(x, np.sin(x))

def update(frame):
    linea.set_ydata(np.sin(x + frame / 10))
    return (linea,)

anim = FuncAnimation(fig, update, frames=120, interval=50, blit=True)
plt.show()   # backend interactivo: la ventana anima
```

La variable `anim` mantiene viva la animación mientras el script o el notebook estén activos.

### Exportar a archivo (GIF / MP4)

```python
anim = FuncAnimation(fig, update, frames=120, interval=50)
anim.save("salida.gif", writer="pillow", fps=20)   # GIF: necesita Pillow
anim.save("salida.mp4", writer="ffmpeg", fps=30)   # MP4: necesita ffmpeg
```

| Formato | `writer` | Requisito externo |
|---------|----------|-------------------|
| `.gif` | `"pillow"` | Pillow instalado |
| `.mp4` | `"ffmpeg"` | ffmpeg en el `PATH` |

Para exportar sin pantalla en un servidor, combina con el backend `Agg` (ver [[concepto_backend]]).

## Buenas prácticas

1. **Guarda siempre la instancia** en una variable de nivel de módulo (`anim = ...`).
2. Crea los Artists **una sola vez** fuera de `func`; dentro solo muta sus datos (`set_ydata`, `set_offsets`, `set_text`).
3. Con `blit=True`, `func` e `init_func` deben **retornar** los Artists modificados como tupla/lista.
4. Ajusta `interval` para la fluidez (fps ≈ 1000 / interval); para `save` usa `fps` explícito.
5. Para vídeos largos, exporta con `save` en lugar de mostrar en ventana.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| La animación no se mueve / desaparece enseguida | No se guardó la referencia; el GC la eliminó | Asignar a una variable: `anim = FuncAnimation(...)` |
| `blit=True` no actualiza nada | `func` no retorna los Artists | `return (linea,)` al final de `func` |
| Cada cuadro añade un gráfico nuevo | Se llama a `ax.plot()` dentro de `func` | Crear el Artist una vez y mutar con `set_*` |
| `save` lanza error de writer | Falta `ffmpeg`/`pillow` | Instalar el writer o cambiar de formato |
| Nada se ve al exportar en servidor | Backend interactivo sin pantalla | Usar `Agg` y `anim.save(...)` |

## Limitaciones

- No está pensada para datos en streaming infinito sin control de `frames`: usa un generador finito o `cache_frame_data=False`.
- Para animar fotogramas ya pre-renderizados (imágenes independientes) suele convenir `ArtistAnimation` en lugar de `FuncAnimation`.

## Notas relacionadas

- [[concepto_backend]]
- [[concepto_artist]]
- [[plt.show]]
- [[plt.savefig]]
- [[ArtistAnimation]]
