---
title: pyplot vs OO — Las dos interfaces de Matplotlib
aliases:
  - pyplot vs oo
  - interfaz pyplot
  - interfaz orientada a objetos
  - plt vs ax
tags:
  - matplotlib
  - concepto
  - interfaz
lib: matplotlib
tipo: concepto
requiere:
  - concepto_figure_axes
draft: false
---

# pyplot vs OO — Las dos interfaces de Matplotlib

## Definicion fundamental

Matplotlib ofrece **dos formas de hacer lo mismo**, y mezclarlas es la fuente nº1 de confusion:

- **Interfaz pyplot** (`plt.*`): una **maquina de estados** que mantiene un "Axes actual" implicito. `plt.plot(...)` dibuja en el ultimo Axes usado.
- **Interfaz orientada a objetos (OO)**: trabajas con **referencias explicitas** `fig` y `ax` y llamas a sus metodos: `ax.plot(...)`.

## El mismo grafico de las dos formas

```python
import matplotlib.pyplot as plt
import numpy as np
x = np.linspace(0, 10, 100)

# --- Estilo pyplot (estado implicito) ---
plt.plot(x, np.sin(x))
plt.title("Seno")
plt.xlabel("x")
plt.show()

# --- Estilo OO (explicito, recomendado) ---
fig, ax = plt.subplots()
ax.plot(x, np.sin(x))
ax.set_title("Seno")
ax.set_xlabel("x")
fig.savefig("seno.png")
```

## La tabla de traduccion

| pyplot (estado) | OO (explicito) |
|-----------------|----------------|
| `plt.plot(...)` | `ax.plot(...)` |
| `plt.title(...)` | `ax.set_title(...)` |
| `plt.xlabel(...)` | `ax.set_xlabel(...)` |
| `plt.xlim(...)` | `ax.set_xlim(...)` |
| `plt.legend()` | `ax.legend()` |
| `plt.gcf()` | el `fig` que ya tienes |
| `plt.gca()` | el `ax` que ya tienes |

Fijate en el patron: pyplot usa `plt.xlabel(...)`, OO usa `ax.set_xlabel(...)` (prefijo `set_`).

## Por que se recomienda OO

| Aspecto | pyplot | OO |
|---------|--------|-----|
| Varios subplots | ambiguo (¿cual es el actual?) | claro (`axs[i]`) |
| Funciones reutilizables | fragil (depende del estado) | robusto (pasas `ax`) |
| Legibilidad en scripts | corta pero implicita | explicita |
| Uso tipico | exploracion rapida en notebook | codigo de produccion |

> Regla practica: para una grafica rapida en consola, pyplot vale. Para cualquier cosa con varios ejes o dentro de funciones, usa OO (`fig, ax = plt.subplots()`).

## El puente entre ambas: gca / gcf

pyplot se apoya en "get current figure/axes":

```python
plt.plot(...)      # internamente: plt.gca().plot(...)
ax = plt.gca()     # recupera el Axes actual como objeto OO
```

Por eso puedes empezar con pyplot y luego pedir el `ax` para afinarlo con la interfaz OO.

## Casos que confunden

### Mezclar las dos sin querer

```python
fig, ax = plt.subplots()
ax.plot(x, y)
plt.title("...")   # ⚠️ actua sobre el Axes ACTUAL, que casualmente es ax
# Funciona aqui, pero con varios subplots apunta al equivocado. Usa ax.set_title.
```

### plt.show() vs fig.savefig()

`plt.show()` abre la ventana interactiva (depende del [[concepto_backend|backend]]); `fig.savefig()` escribe a archivo. No los confundas.

## Relacion con otros conceptos

- [[concepto_figure_axes]]
- [[concepto_backend]]
- [[plt.subplots]]
- [[ax.set_title]]
