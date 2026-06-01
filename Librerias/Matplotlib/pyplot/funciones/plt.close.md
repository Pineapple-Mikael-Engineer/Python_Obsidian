---
title: plt.close — Cerrar una figura y liberar memoria
aliases:
  - close
  - plt.close
tags:
  - matplotlib
  - api/funcion
  - figura
lib: matplotlib
obj: pyplot
tipo: funcion
retorna: None
muta_estado: true
draft: false
---

# plt.close — Cerrar una figura y liberar memoria

## Idea clave

`plt.close()` cierra una figura, destruye su ventana y libera la memoria que ocupaban sus Artists. Es la contrapartida de [[plt.figure]]: lo que se crea debe cerrarse. Resulta **crítico en bucles** que generan muchas figuras, donde olvidarlo agota la RAM y dispara el aviso *"More than 20 figures have been opened"*.

## Firma de la función

```python
matplotlib.pyplot.close(
    fig=None   # None | int | str | Figure | 'all'
)
```

## Valor de retorno

| Entrada | Retorno | Ejemplo |
|---------|---------|---------|
| `None` | `None`, cierra la figura **actual** | `plt.close()` |
| `Figure` | `None`, cierra esa instancia | `plt.close(fig)` |
| `int` / `str` | `None`, cierra la figura con ese id | `plt.close(2)` |
| `'all'` | `None`, cierra **todas** las figuras | `plt.close('all')` |

```python
fig, ax = plt.subplots()
plt.close(fig)        # → None  (figura destruida)
plt.close('all')      # → None  (limpia todo)
```

## Parámetros en detalle

### `fig` — qué cerrar

```python
plt.close()         # la figura actual
plt.close(fig)      # una instancia concreta (preferido)
plt.close(1)        # por número
plt.close("panel")  # por nombre
plt.close("all")    # todas a la vez
```

| Valor | Comportamiento |
|-------|----------------|
| `None` | cierra la figura activa actual |
| `Figure` | cierra esa figura específica |
| `int` / `str` | cierra la figura identificada por `num` |
| `'all'` | cierra todas las figuras gestionadas por pyplot |

## Casos de uso

### Caso 1: liberar memoria en un bucle (el caso clave)

```python
for i, datos in enumerate(series):
    fig, ax = plt.subplots()
    ax.plot(datos)
    fig.savefig(f"fig_{i}.png")
    plt.close(fig)   # imprescindible: sin esto la RAM crece sin límite
```

### Caso 2: reiniciar el estado entre tests

```python
plt.close('all')   # cierra cualquier figura residual antes de empezar
```

> Cerrar destruye la figura por completo. Si solo quieres vaciar el contenido pero conservar la ventana, usa [[plt.clf]] en su lugar.

## Buenas prácticas

1. En cualquier bucle que cree figuras, cierra cada una tras guardarla con `plt.close(fig)`.
2. Prefiere pasar la instancia `fig` explícita antes que confiar en la figura actual.
3. Usa `plt.close('all')` al inicio de scripts/tests para partir de un estado limpio.
4. No confundas cerrar (destruir) con limpiar (vaciar): para reutilizar la ventana, `clf`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Aviso "More than 20 figures opened" | crear figuras en bucle sin cerrarlas | `plt.close(fig)` por iteración |
| Consumo de memoria creciente | figuras acumuladas en el gestor de pyplot | cerrar tras usar / `plt.close('all')` |
| Operar sobre una figura cerrada | usarla después de `close` | recrearla antes de operar |

## Limitaciones

`plt.close` libera la figura, pero los arrays NumPy y datos a los que aún hay referencias no se liberan hasta que el recolector de basura actúe. No es sustituto de limpiar el contenido: para eso está `clf`/`cla`.

## Notas relacionadas

- [[plt.figure]]
- [[plt.clf]]
- [[plt.savefig]]
- [[concepto_figure_axes]]
