---
title: plt.clf — Limpiar la figura actual conservando la ventana
aliases:
  - clf
  - plt.clf
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

# plt.clf — Limpiar la figura actual conservando la ventana

## Idea clave

`plt.clf()` (*clear figure*) vacía la figura actual: elimina todos sus ejes y Artists, pero **conserva la ventana/figura viva** para reutilizarla. Es el punto intermedio entre no hacer nada y [[plt.close]] (que destruye la figura por completo).

Contrasta con `plt.cla()`, que limpia **solo el Axes** activo, dejando intactos los demás ejes de la figura.

## Firma de la función

```python
matplotlib.pyplot.clf()
```

No recibe argumentos: siempre actúa sobre la figura actual.

## Valor de retorno

| Entrada | Retorno | Ejemplo |
|---------|---------|---------|
| (ninguna) | `None`, figura vaciada | `plt.clf()` |

```python
plt.plot([1, 2, 3])
plt.clf()        # → None  (la figura queda en blanco, la ventana sigue)
plt.plot([3, 2, 1])   # se redibuja sobre la misma figura
```

## clf vs cla vs close

| Función | Alcance | Conserva la figura | Uso típico |
|---------|---------|--------------------|------------|
| `plt.cla()` | un solo Axes | sí | redibujar un subplot |
| `plt.clf()` | toda la figura (todos los ejes) | sí (vacía) | reusar la ventana con contenido nuevo |
| `plt.close()` | toda la figura | no (la destruye) | liberar memoria en bucles |

## Casos de uso

### Caso 1: reutilizar la misma figura en una animación manual

```python
for frame in frames:
    plt.clf()              # vacía el contenido anterior
    plt.plot(frame.x, frame.y)
    plt.pause(0.05)        # actualiza la misma ventana
```

### Caso 2: regenerar contenido sin abrir ventanas nuevas

```python
plt.figure(1)
plt.plot(serie_a)
plt.clf()                  # borra serie_a
plt.plot(serie_b)          # serie_b en la misma figura 1
```

> Si en cambio creas una figura nueva por iteración, no uses `clf`: cierra cada una con `plt.close(fig)` para no acumular memoria. Para gráficos estructurados prefiere la API OO con [[plt.subplots]].

## Buenas prácticas

1. Usa `clf` cuando quieras **reaprovechar** la misma figura/ventana con datos nuevos.
2. Si solo cambia un subplot, `cla()` es más preciso y barato que `clf`.
3. Para terminar definitivamente con una figura, usa `close`, no `clf`.
4. En código OO equivalente, llama `fig.clear()` en vez de la función de estado.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| La figura "se llena" de gráficos superpuestos | no limpiar entre redibujados | `plt.clf()` antes de volver a plotear |
| Memoria crece pese a `clf` | `clf` no cierra la figura, solo la vacía | usar `plt.close(fig)` cuando ya no se necesite |
| Se borran subplots que querías conservar | `clf` limpia toda la figura | usar `plt.cla()` para un único Axes |

## Limitaciones

`clf` no libera la figura del gestor de pyplot: la ventana sigue contando como abierta. Para reducir el número de figuras abiertas y la memoria asociada, hay que cerrarlas.

## Notas relacionadas

- [[plt.close]]
- [[plt.figure]]
- [[plt.subplots]]
- [[concepto_figure_axes]]
