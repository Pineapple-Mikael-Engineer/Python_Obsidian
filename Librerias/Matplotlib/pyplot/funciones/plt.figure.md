---
title: plt.figure — Crear o activar una figura
aliases:
  - figure
  - plt.figure
tags:
  - matplotlib
  - api/funcion
  - figura
lib: matplotlib
obj: pyplot
tipo: funcion
retorna: Figure
muta_estado: true
draft: false
---

# plt.figure — Crear o activar una figura

## Idea clave

`plt.figure()` crea una nueva instancia de `Figure` (el lienzo de nivel superior) o **activa una existente** si se pasa un identificador ya usado. Convierte esa figura en la **figura actual**, sobre la que operan después las funciones de estado de pyplot (`plt.plot`, `plt.savefig`, `plt.clf`...).

Es el constructor de bajo nivel: el moderno [[plt.subplots]] lo invoca internamente vía `**fig_kw`.

## Firma de la función

```python
matplotlib.pyplot.figure(
    num=None,         # int | str | Figure: identificador de la figura
    figsize=None,     # (ancho, alto) en pulgadas
    dpi=None,         # resolución en puntos por pulgada
    facecolor=None,   # color de fondo del lienzo
    edgecolor=None,   # color del borde
    frameon=True,     # dibujar el marco de fondo
    clear=False,      # si num ya existe, limpiarla antes de devolver
    **kwargs
)
```

## Valor de retorno

| Entrada | Retorno | Ejemplo |
|---------|---------|---------|
| sin `num` | `Figure` nueva (número autoincremental) | `fig = plt.figure()` |
| `num` nuevo | `Figure` nueva con ese id | `plt.figure(2)` |
| `num` existente | la `Figure` ya creada (la activa) | `plt.figure(1)  # reactiva fig 1` |
| `num` + `clear=True` | la `Figure` existente, vaciada | `plt.figure(1, clear=True)` |

```python
fig = plt.figure(figsize=(8, 5), dpi=120)
type(fig)        # → <class 'matplotlib.figure.Figure'>
fig.number       # → 1
```

## Parámetros en detalle

### `num` — identidad de la figura

```python
plt.figure("dashboard")   # figura nombrada (la ventana lleva el título)
plt.figure(3)             # figura por número
```

| Tipo | Comportamiento |
|------|----------------|
| `None` | crea figura nueva con número correlativo |
| `int` | activa esa figura si existe; si no, la crea |
| `str` | igual que int pero con etiqueta de texto en la ventana |
| `Figure` | activa esa instancia concreta |

### `figsize` y `dpi` — tamaño físico y resolución

```python
plt.figure(figsize=(10, 6))   # 10 x 6 pulgadas → 1200 x 720 px a dpi=120
```

El tamaño en píxeles es `figsize * dpi`. Define `dpi` alto al exportar para impresión.

### `facecolor` / `edgecolor` — apariencia del lienzo

```python
plt.figure(facecolor="#f0f0f0", edgecolor="black", frameon=True)
```

## Casos de uso

### Caso 1: figura simple con estilo OO posterior

```python
fig = plt.figure(figsize=(6, 4))
ax = fig.add_subplot(1, 1, 1)
ax.plot([1, 2, 3], [4, 5, 6])
```

### Caso 2: varias figuras independientes

```python
plt.figure(1); plt.plot(x, y1)   # figura 1 = actual
plt.figure(2); plt.plot(x, y2)   # figura 2 = actual
plt.figure(1); plt.title("vuelvo a la 1")  # reactiva la figura 1
```

> En la práctica moderna se prefiere [[plt.subplots]], que devuelve `fig` y `ax` juntos y evita depender de la figura actual implícita.

## Buenas prácticas

1. Para gráficos normales usa `plt.subplots()`; reserva `plt.figure()` para cuando construyes la figura dinámicamente (con `add_subplot`/`GridSpec`).
2. Especifica siempre `figsize` para resultados reproducibles.
3. Usa `num` con nombre (`str`) para reabrir/actualizar una figura concreta sin acumular ventanas.
4. Cierra con [[plt.close]] las figuras que ya no uses para liberar memoria.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Acumulación de figuras / aviso "more than 20 figures" | crear figuras en bucle sin cerrarlas | llamar `plt.close(fig)` tras guardar |
| El plot va a la figura equivocada | la "figura actual" cambió implícitamente | usar la API OO (`fig.add_subplot`) o `plt.figure(num)` explícito |
| `figsize` ignorado al reactivar | `num` ya existía; los kwargs no se reaplican | crear nueva o pasar `clear=True` |

## Limitaciones

`plt.figure()` solo crea el lienzo, no ejes: necesitas `add_subplot`/`add_axes`. Si quieres figura + ejes en una llamada, usa `plt.subplots()`.

## Notas relacionadas

- [[concepto_figure_axes]]
- [[concepto_pyplot_vs_oo]]
- [[plt.subplots]]
- [[plt.close]]
- [[plt.savefig]]
