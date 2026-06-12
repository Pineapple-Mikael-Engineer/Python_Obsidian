---
title: text — texto, anotaciones y matemáticas
tags: [matplotlib, indice]
draft: false
---

# text — texto, anotaciones y matemáticas

El módulo `matplotlib.text` cubre todo lo escrito sobre un gráfico: títulos, etiquetas de ejes, leyendas, notas sueltas y anotaciones con flecha. La pieza central es `Text`, el [[concepto_artist|Artist]] que representa **una cadena dibujada**; cada vez que llamas a `ax.set_title`, `ax.set_xlabel` o `ax.text` estás creando uno. `Annotation` es una **subclase** de `Text` que añade un punto señalado y una flecha. Como Artists, ambos comparten `.set_visible`, `.set_alpha`, `.set_zorder` y `.set_color` con líneas y formas: se manipulan con `set_*` / `get_*` en lugar de recrearse. El estilo de fuente (familia, tamaño, peso) y las fórmulas matemáticas (`$...$`) son ortogonales al objeto y se documentan aparte.

## En acción

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 200)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, y)

# Text: una cadena suelta colocada en coordenadas de datos
t = ax.text(1.5, 0.9, "región inicial",
            fontsize=12, color="navy",
            bbox=dict(boxstyle="round", facecolor="wheat"))

# Annotation: texto CON flecha que apunta a un punto concreto
imax = y.argmax()
ax.annotate(r"máximo $\sin(x)=1$",
            xy=(x[imax], y[imax]),          # punto señalado
            xytext=(x[imax] + 1, 1.4),      # dónde va la cadena
            arrowprops=dict(arrowstyle="->", color="crimson"))

plt.show()
```

## Text vs Annotation

```mermaid
flowchart TD
    Q{{"¿El texto señala un punto?"}}
    Q -->|"no, solo una cadena en un sitio"| T(["Text — ax.text(x, y, 'cadena')"])
    Q -->|"sí, con flecha a un punto"| A(["Annotation — ax.annotate(txt, xy, xytext, arrowprops)"])

    A --> HER["Annotation HEREDA de Text"]
    HER --> T

    T --> ESTILO["Estilo del texto"]
    ESTILO --> F(["fontdict — family, size, weight, color"])
    ESTILO --> M(["mathtext / LaTeX — '$\\alpha^2$'"])

    classDef pregunta fill:#5e81ac,stroke:#88c0d0,stroke-width:2px,color:#eceff4;
    classDef grupo fill:#3b4252,stroke:#81a1c1,stroke-width:1.5px,color:#88c0d0;
    classDef hoja fill:#2e3440,stroke:#a3be8c,color:#d8dee9;
    class Q pregunta;
    class HER,ESTILO pregunta;
    class T,A,F,M hoja;
```

La diferencia es de **propósito**: `Text` coloca una cadena; `Annotation` la coloca y, además, traza una flecha desde `xytext` (dónde va el texto) hasta `xy` (qué señala). Confundir esos dos puntos invierte la flecha. Si no pasas `arrowprops`, `annotate` se comporta como un `Text` desplazado.

## Las piezas de este módulo

- [[Text]] — **la clase de texto**. El objeto que devuelve `ax.text`; propiedades clave (`set_text`, `set_position`, `ha`/`va` de alineación, `rotation`, caja de fondo `bbox`) y cómo mutarlo en lugar de recrearlo.
- [[Annotation]] — **texto con flecha**. Subclase de `Text` que añade `xy` (punto señalado), `xytext` (posición del texto) y el dict `arrowprops` (`arrowstyle`, `connectionstyle` para curvar). Mezcla coordenadas de datos y de eje.
- [[fontdict]] — **el estilo de fuente**. Familia, tamaño, peso, estilo y color, vía kwargs sueltos, dict `fontdict={...}` o global con `rcParams['font.*']`.
- [[LaTeX_mathtext]] — **matemáticas en el texto**. `mathtext` (subconjunto TeX sin instalar nada, entre `$...$`) frente a LaTeX completo (`text.usetex=True`). Usa siempre raw strings `r'...'`.

| Quiero… | Ir a |
|---------|------|
| Colocar una cadena suelta y darle estilo | [[Text]] |
| Señalar un punto con una flecha | [[Annotation]] |
| Cambiar fuente, tamaño, peso o color del texto | [[fontdict]] |
| Escribir símbolos griegos, fracciones, integrales | [[LaTeX_mathtext]] |

> [!tip] Coordenadas relativas al eje
> Por defecto el texto va en coordenadas de **datos**. Para anclarlo a una posición fija del recuadro (p. ej. esquina superior izquierda), usa `transform=ax.transAxes` en `ax.text`, o `textcoords='axes fraction'` en `ax.annotate`, con valores 0..1.

## Notas relacionadas

- [[ax.text]] — crear un `Text`
- [[ax.annotate]] — crear una `Annotation`
- [[concepto_artist]] — la herencia común (`set_alpha`, `set_zorder`, `set_visible`)
- [[Tree Matplotlib]] — mapa completo del vault
