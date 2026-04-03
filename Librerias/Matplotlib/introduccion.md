---
title: Introducción a pyplot — Flujo básico y buenas prácticas
aliases:
  - introduccion
  - flujo basico
tags:
  - matplotlib
  - api/config
  - pyplot/intro
lib: matplotlib
obj: pyplot
tipo: config
draft: false
---

# Introducción a pyplot — Flujo básico y buenas prácticas

## Importación estándar

```python
import matplotlib.pyplot as plt
import numpy as np
```

La convención universal es importar `pyplot` como `plt`. NumPy es el compañero natural para generar datos.

Alternativas menos comunes:

```python
import matplotlib as mpl
from matplotlib import pyplot as plt
```

---

## Flujo mínimo de uso

```python
fig, ax = plt.subplots()

ax.plot(x, y)

ax.set_xlabel("x")
ax.set_ylabel("y")

plt.show()
```

## Modelo mental

`pyplot` es un submódulo de matplotlib que proporciona una interfaz estilo MATLAB. La organización fundamental es:

| Objeto | Rol | Creación |
|--------|-----|----------|
| **Figure (`fig`)** | Contenedor global. Es la ventana o página que contiene todo. | `plt.figure()`, `plt.subplots()` |
| **Axes (`ax`)** | Área de dibujo individual. Contiene ejes, ticks, títulos. Una figure puede tener múltiples axes. | `fig.add_subplot()`, `plt.subplots()` |

```python
fig, ax = plt.subplots()  # patrón recomendado para un solo gráfico
fig, axs = plt.subplots(2, 3)  # 2 filas, 3 columnas → axs es array de axes
```

> [!tip] Trabajar siempre sobre `ax`  
> La API orientada a objetos (`ax.plot()`, `ax.set_xlabel()`) es más clara, evita conflictos y es necesaria para gráficos complejos. La API estilo MATLAB (`plt.plot()`, `plt.xlabel()`) solo funciona en el axes "actual", lo que causa confusión con múltiples subgráficos.

---

## Sintaxis base recurrente

| Acción | Código | Parámetros útiles |
|--------|--------|-------------------|
| Gráfico de líneas | `ax.plot(x, y, label="...", color="...", marker="o")` | `linewidth`, `linestyle`, `alpha` |
| Gráfico de dispersión | `ax.scatter(x, y, c=z, s=20)` | `c` (color), `s` (tamaño), `cmap` |
| Etiqueta eje X | `ax.set_xlabel("texto", fontsize=12, fontweight="bold")` | `labelpad` (espacio), `color` |
| Etiqueta eje Y | `ax.set_ylabel("texto")` | igual que set_xlabel |
| Título | `ax.set_title("texto", fontsize=14, loc="center")` | `pad` (espacio), `fontweight` |
| Leyenda | `ax.legend(loc="best", fontsize=10)` | `frameon`, `ncol`, `bbox_to_anchor` |
| Cuadrícula | `ax.grid(True, linestyle="--", alpha=0.7)` | `axis` (`'both'`, `'x'`, `'y'`) |
| Límites | `ax.set_xlim(0, 10)` | también `ax.set_ylim()` |
| Escalas | `ax.set_xscale("log")` | `'linear'`, `'log'`, `'symlog'` |

---

## Buenas prácticas

1. **Usar API orientada a objetos siempre**
   ```python
   # correcto
   fig, ax = plt.subplots()
   ax.plot(x, y)
   ax.set_xlabel("x")
   ```

2. **Definir `label` desde el inicio**
   ```python
   ax.plot(x, y, label="mi_serie")  # luego ax.legend() automático
   ```

3. **Activar grid en análisis exploratorio**
   ```python
   ax.grid(True, alpha=0.3)  # ayuda a leer valores
   ```

4. **Usar `figsize` para controlar proporciones**
   ```python
   fig, ax = plt.subplots(figsize=(10, 4))  # ancho x alto en pulgadas
   ```

5. **Cerrar figuras después de guardar en bucles**
   ```python
   for i in range(100):
       fig, ax = plt.subplots()
       ax.plot(data[i])
       plt.savefig(f"plot_{i}.png")
       plt.close(fig)  # evitar memory leak
   ```

## Anti-patrones a evitar

```python
# estilo implícito (difícil de controlar con múltiples subplots)
plt.plot(x, y)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Título")
plt.show()
```

```python
# mezcla de API (causa confusión)
fig, ax = plt.subplots()
plt.plot(x, y)  # plt.plot() dibuja en el axes actual, pero no es claro
plt.xlabel("x")  # aplica al axes actual
ax.set_title("Título")  # mezcla
```

```python
# crear figura y no guardar referencia
plt.subplots()  # se pierde referencia, no se puede modificar después
```

```python
# correcto - todo explícito
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Título")
plt.show()
```

---

## Snippet base reutilizable

```python
import matplotlib.pyplot as plt
import numpy as np

# Datos de ejemplo
x = np.linspace(0, 10, 100)
y = np.sin(x)
y2 = np.cos(x)

# Crear figura y ejes
fig, ax = plt.subplots(figsize=(10, 6))

# Graficar
ax.plot(x, y, label="sin(x)", linewidth=2, color="blue")
ax.plot(x, y2, label="cos(x)", linewidth=2, color="red", linestyle="--")

# Formato
ax.set_xlabel("x (radianes)", fontsize=12)
ax.set_ylabel("y", fontsize=12)
ax.set_title("Funciones trigonométricas", fontsize=14, fontweight="bold")
ax.legend(loc="upper right", fontsize=10)
ax.grid(True, alpha=0.3)

# Ajustar límites (opcional)
ax.set_xlim(0, 10)
ax.set_ylim(-1.5, 1.5)

# Mostrar
plt.tight_layout()
plt.show()
```

---

## Notas relacionadas

- [[plt.subplots]]
- [[ax.plot]]
- [[lines.marker]]
- [[lines.linestyle]]
- [[ax.set_xlabel]]
- [[ax.set_ylabel]]
- [[ax.set_title]]
- [[ax.legend]]
- [[ax.grid]]
- [[ax.set_xlim]]
- [[ax.set_ylim]]
- [[ax.set_xscale]]
- [[ax.set_yscale]]
- [[plt.show]]
- [[plt.savefig]]
- [[colors.nombres]]
- [[cm.Colormaps]]

