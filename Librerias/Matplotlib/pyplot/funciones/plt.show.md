---
title: plt.show — Mostrar las figuras en ventana interactiva
aliases:
  - show
  - plt.show
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

# plt.show — Mostrar las figuras en ventana interactiva

## Idea clave

`plt.show()` dispara el render de **todas las figuras abiertas** y las muestra en una ventana interactiva. Es el punto donde el [[concepto_backend|backend]] convierte los Artists en memoria a píxeles en pantalla. Con un backend interactivo (`TkAgg`, `QtAgg`...) **bloquea** la ejecución del script hasta que cierras las ventanas.

A diferencia de [[plt.savefig]], que escribe a archivo, `plt.show()` requiere un entorno gráfico: en un servidor headless no tiene dónde dibujar.

## Firma de la función

```python
matplotlib.pyplot.show(
    *,
    block=None   # bool: si bloquea o no la ejecución
)
```

## Valor de retorno

| Entrada | Retorno | Ejemplo |
|---------|---------|---------|
| backend interactivo | `None` (abre ventana, bloquea) | `plt.show()` |
| `block=False` | `None` (ventana no bloqueante) | `plt.show(block=False)` |
| backend `Agg` (archivo) | `None` (no muestra nada) | `plt.show()  # no-op` |

```python
fig, ax = plt.subplots()
ax.plot([1, 2, 3])
plt.show()        # → None  (abre la ventana y bloquea)
```

## Parámetros en detalle

### `block` — control del bloqueo

```python
plt.show(block=True)    # bloquea hasta cerrar (default en scripts)
plt.show(block=False)   # devuelve el control de inmediato
```

| Valor | Comportamiento |
|-------|----------------|
| `True` | el script se detiene hasta cerrar todas las ventanas |
| `False` | continúa la ejecución; la ventana se actualiza de forma asíncrona |
| `None` | autodetecta según contexto (script vs interactivo) |

## Casos de uso

### Caso 1: visualización en script

```python
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_title("Resultado")
plt.show()   # se queda aquí hasta que cierras la ventana
```

### Caso 2: guardar y mostrar

```python
fig, ax = plt.subplots()
ax.plot(x, y)
fig.savefig("salida.png")   # guarda primero
plt.show()                  # luego muestra
```

> En Jupyter con `%matplotlib inline` no necesitas llamar `plt.show()`: cada celda renderiza automáticamente. La llamada explícita es propia de scripts con backend interactivo.

## Buenas prácticas

1. Llama `plt.show()` **una sola vez**, al final del script, no después de cada figura.
2. Guarda con [[plt.savefig]] **antes** de mostrar, por si el backend limpia la figura.
3. En servidores/CI sin pantalla, usa `matplotlib.use("Agg")` y omite `show()`.
4. Para animaciones o actualización en vivo, usa `block=False` junto con `plt.pause()`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| No abre ninguna ventana | backend no interactivo (`Agg`) | usar backend interactivo o `savefig` |
| El script "se cuelga" | `show()` bloqueante esperando cierre | comportamiento normal; usar `block=False` si no lo quieres |
| Figura vacía tras `show()` | se mostró antes de plotear | plotear antes de `show()` |
| `show()` repetido no muestra de nuevo | la figura ya se consumió | recrear la figura |

## Limitaciones

`plt.show()` no produce archivos ni sirve en entornos sin display. Para exportar resultados usa `savefig`. No es la forma de guardar imágenes.

## Notas relacionadas

- [[concepto_backend]]
- [[plt.savefig]]
- [[plt.subplots]]
- [[concepto_pyplot_vs_oo]]
- [[plt.close]]
