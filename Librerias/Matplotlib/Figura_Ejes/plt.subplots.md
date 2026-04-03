---
title: plt.subplots — Creación de figura y ejes
aliases:
  - subplots
  - crear figura y ejes
  - layout básico
  - plt.subplots
tags:
  - matplotlib
  - api/funcion
  - pyplot/funciones
lib: matplotlib
tipo: funcion
muta_estado: true
requiere: []
draft: false
---






# plt.subplots — Creación de figura y ejes

## Idea clave

`plt.subplots()` es una **función de módulo** que actúa como constructor de layout + ejes:

- Crea una instancia de `Figure`
- Crea una grilla de instancias de `Axes`
- Retorna ambos listos para trabajar

Es el punto de entrada moderno para casi cualquier gráfico en matplotlib.

---

## Sintaxis completa

```python
matplotlib.pyplot.subplots(
    nrows=1,          # número de filas
    ncols=1,          # número de columnas
    sharex=False,     # compartir eje X entre subplots
    sharey=False,     # compartir eje Y entre subplots
    squeeze=True,     # eliminar dimensiones de tamaño 1
    subplot_kw=None,  # argumentos para cada Axes
    **fig_kw          # argumentos para Figure (figsize, dpi, etc)
)
```

### Parámetros principales

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `nrows`, `ncols` | `int` | 1, 1 | Dimensiones de la grilla de subplots |
| `sharex`, `sharey` | `bool` o `str` | `False` | Controla compartición de límites y ticks |
| `squeeze` | `bool` | `True` | Determina la forma del array de retorno |
| `subplot_kw` | `dict` | `None` | Argumentos pasados a cada `add_subplot()` |
| `**fig_kw` | `dict` | - | Argumentos de `figure()`: `figsize`, `dpi`, `facecolor` |

### Valor de retorno

```python
fig, axs = plt.subplots(...)
```

| Retorno | Tipo | Descripción |
|---------|------|-------------|
| `fig` | `matplotlib.figure.Figure` | Instancia de Figure. Control global: título, tamaño, guardado, layout. |
| `axs` | `Axes` o `ndarray` de `Axes` | Instancia(s) de Axes. Cada `Axes` es un área de dibujo con sus propios ejes, ticks, etiquetas. |

---

## Reglas de retorno (cómo se comporta `squeeze`)

El valor de `squeeze` controla la forma del objeto `axs`:

| Configuración | `squeeze=True` (default) | `squeeze=False` |
|---------------|--------------------------|-----------------|
| `1, 1` | `axs` = `Axes` (objeto único) | `axs` = array `[[axes.Axes]]` |
| `1, N` | `axs` = array `(N,)` 1D | `axs` = array `(1, N)` 2D |
| `N, 1` | `axs` = array `(N,)` 1D | `axs` = array `(N, 1)` 2D |
| `N, M` | `axs` = array `(N, M)` 2D | `axs` = array `(N, M)` 2D |

> [!tip] `squeeze=True` es cómodo para casos simples, pero puede causar errores si el código espera un array y recibe un solo objeto. Para código robusto, considerar usar `squeeze=False` o aplicar [[Manejo_Arrays_Axes]].

---

## Casos de uso básicos

### Caso 1: un solo gráfico

```python
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, y)
ax.set_xlabel("Tiempo (s)")
ax.set_ylabel("Amplitud")
fig.suptitle("Señal de ejemplo")
```

> [!note] `ax` es un objeto `Axes` único. Se usa directamente con métodos como `.plot()`, `.set_xlabel()`.

### Caso 2: una fila con N gráficos

```python
fig, axs = plt.subplots(1, 3, figsize=(12, 4))

axs[0].plot(x, y1)   # primer subplot
axs[1].plot(x, y2)   # segundo subplot
axs[2].plot(x, y3)   # tercer subplot

# Aplicar formato a todos
for ax in axs:
    ax.set_ylim(0, 1)
    ax.grid(True)
```

> [!tip] Con `1, N`, `axs` es un array 1D. Se indexa con un solo índice: `axs[0]`.

### Caso 3: grilla N x M

```python
fig, axs = plt.subplots(2, 3, figsize=(15, 8))

axs[0, 0].plot(x, y1)   # fila 0, columna 0
axs[0, 1].plot(x, y2)   # fila 0, columna 1
axs[0, 2].plot(x, y3)   # fila 0, columna 2
axs[1, 0].plot(x, y4)   # fila 1, columna 0
axs[1, 1].plot(x, y5)   # fila 1, columna 1
axs[1, 2].plot(x, y6)   # fila 1, columna 2

# Aplanar para iterar (ver [[Manejo_Arrays_Axes]])
for ax in axs.flat:
    ax.set_xlabel("Tiempo")
```

> [!tip] Con `N, M` (ambos >1), `axs` es un array 2D. Se indexa con dos índices: `axs[fila, columna]`.

---

## Parámetros clave en detalle

### `figsize` — control de proporciones

```python
fig, ax = plt.subplots(figsize=(8, 5))  # ancho 8 pulgadas, alto 5
```

Especificar `figsize` es buena práctica para:
- Exportar imágenes con dimensiones consistentes
- Preparar figuras para papers o reportes
- Mantener proporción aspecto adecuada

### `sharex` / `sharey` — compartición de ejes

```python
fig, axs = plt.subplots(2, 2, sharex=True, sharey=True)
```

| Valor | Comportamiento |
|-------|----------------|
| `True` | Todos los subplots comparten eje X e Y |
| `'row'` | Subplots en misma fila comparten eje Y |
| `'col'` | Subplots en misma columna comparten eje X |
| `False` | Sin compartición (default) |

> [!tip] Compartir ejes elimina ticks redundantes y facilita comparación visual directa entre subplots. Ver [[ax.shared_axes]] para más detalles.

### `subplot_kw` — personalización por Axes

```python
# Crear subplots 3D
fig, axs = plt.subplots(1, 2, subplot_kw={'projection': '3d'})

# Crear subplots con fondo polar
fig, axs = plt.subplots(1, 2, subplot_kw={'projection': 'polar'})
```

### `**fig_kw` — argumentos de Figure

```python
fig, ax = plt.subplots(
    figsize=(10, 6),
    dpi=120,
    facecolor='lightgray',
    edgecolor='black',
    frameon=True
)
```

---

## Comparación con API alternativa

### `plt.figure()` + `add_subplot()` (estilo antiguo)

```python
fig = plt.figure(figsize=(8, 5))
ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 2)
ax3 = fig.add_subplot(2, 2, 3)
ax4 = fig.add_subplot(2, 2, 4)
```

### `plt.subplots()` (estilo moderno)

```python
fig, axs = plt.subplots(2, 2, figsize=(8, 5))
# axs[0,0], axs[0,1], axs[1,0], axs[1,1]
```

| Aspecto | `subplots()` | `add_subplot()` |
|---------|--------------|-----------------|
| Líneas de código | 1 | N+1 |
| Acceso a axes | Indexación por coordenadas | Variables individuales |
| Compartición de ejes | Parámetros integrados | Manual, propenso a errores |
| Escalabilidad | Alta (cambias N y M fácil) | Baja (requiere reescribir) |

> [!tip] `subplots()` es el estándar moderno. Reservar `add_subplot()` para casos donde necesitas construir la figura de forma dinámica o no rectangular (ver [[GridSpec]]).

---

## Buenas prácticas

### 1. Usar `fig, ax = plt.subplots()` siempre
Evitar `plt.plot()` directo. La API orientada a objetos es explícita y evita efectos secundarios.

```python
# evitar
plt.plot(x, y)
plt.xlabel("x")

# correcto
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlabel("x")
```

### 2. Controlar `figsize` explícitamente
No confiar en el default. Especificar dimensiones desde el inicio.

### 3. Usar `sharex` / `sharey` en comparaciones
Previene escalas inconsistentes que pueden llevar a interpretaciones erróneas.

### 4. Centralizar configuración global en `fig`

```python
fig.suptitle("Resultados del experimento")
fig.tight_layout()  # ajusta márgenes automáticamente
fig.savefig("resultados.png", dpi=150)
```

### 5. Pensar en `Axes` como unidades independientes
Cada `ax` tiene:
- Su propio sistema de coordenadas
- Sus propios ticks y etiquetas
- Sus propias transformaciones

### Errores comunes

```python
# confundir retorno cuando es único
fig, axs = plt.subplots(2, 1)   # axs es array 1D
axs.plot(x, y)                  # error: array no tiene .plot()

# correcto
fig, axs = plt.subplots(2, 1)
axs[0].plot(x, y)
axs[1].plot(x, y)
```

```python
# asumir que axs siempre es 2D
fig, axs = plt.subplots(1, 3)   # axs es 1D
axs[0, 1].plot(x, y)            # error: muy pocos índices

# correcto
fig, axs = plt.subplots(1, 3)
axs[1].plot(x, y)               # indexación 1D
```

---

## Notas relacionadas

- [[Manejo_Arrays_Axes]]
- [[GridSpec]]
- [[ax.shared_axes]]
- [[Configuracion]]
- [[ax.plot]]
- [[pyplot.plt.show]]
- [[pyplot.plt.savefig]]