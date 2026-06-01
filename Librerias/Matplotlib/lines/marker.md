---
title: marker — Catálogo de estilos de marcador
aliases:
  - marker
  - marcadores
  - markers

tags:
  - matplotlib
  - api/objeto
  - styling

# --- Clasificación ---
lib: matplotlib
obj: marker
mod: matplotlib.lines
tipo: objeto

# --- Comportamiento ---
retorna: None
muta_estado: false

draft: false
---

# marker — Catálogo de estilos de marcador

## Definición

`marker` es el código que define la **forma del símbolo** dibujado en cada punto de datos. Se pasa como `marker=` (o dentro del `fmt` compacto) a métodos como [[ax.plot]] y `ax.scatter`. No es una función ni muta estado: es una referencia de valores aceptados. Cada marcador se renderiza sobre la línea como parte del [[Line2D]] o de la colección de puntos.

## Marcadores principales (string de un carácter)

| Código | Forma | Uso típico |
|--------|-------|------------|
| `'.'` | punto pequeño | nubes densas |
| `','` | píxel | scatter masivo |
| `'o'` | círculo | el más usado |
| `'v'` | triángulo hacia abajo | series direccionales |
| `'^'` | triángulo hacia arriba | series direccionales |
| `'<'` | triángulo izquierda | — |
| `'>'` | triángulo derecha | — |
| `'s'` | cuadrado | categorías |
| `'p'` | pentágono | — |
| `'*'` | estrella | resaltar puntos |
| `'h'` | hexágono (vértice arriba) | — |
| `'H'` | hexágono (lado arriba) | — |
| `'+'` | cruz fina | datos sobre fondo |
| `'x'` | equis fina | exclusiones |
| `'X'` | equis rellena | énfasis |
| `'D'` | diamante (rombo) | — |
| `'d'` | diamante delgado | — |
| `'|'` | línea vertical | rugplots |
| `'_'` | línea horizontal | rugplots |
| `'1'` `'2'` `'3'` `'4'` | tri (abajo/arriba/izq/der) | redes, grafos |
| `'P'` | plus rellena | énfasis |

## Marcadores especiales (no-string)

| Valor | Significado |
|-------|-------------|
| `'none'` o `None` | sin marcador (solo línea) |
| `''` | sin marcador |
| `0`..`11` (int) | tick-marks: caret arriba/abajo/izq/der, etc. |
| `(numsides, style, angle)` | polígono/estrella/asterisco personalizado |
| `'$...$'` | usa texto/LaTeX como marcador, p. ej. `'$\\heartsuit$'` |
| objeto `Path` | marcador con forma arbitraria |

## Casos de uso

### Marcador junto a línea

```python
ax.plot(x, y, marker='o')        # círculos sobre la línea
ax.plot(x, y, marker='s', ms=8)  # cuadrados de tamaño 8
```

### Solo marcadores (sin línea) vía fmt compacto

```python
ax.plot(x, y, 'o')               # solo círculos
ax.plot(x, y, '^--r')            # triángulos + línea roja discontinua
```

El `fmt` combina color + marcador + estilo de línea en un único string.

### Marcador como texto / símbolo

```python
ax.plot(x, y, marker='$\\clubsuit$', ms=12)
ax.plot(x, y, marker=(5, 1, 0))   # estrella de 5 puntas
```

### Personalizar relleno y borde del marcador

```python
ax.plot(x, y, marker='o',
        markerfacecolor='white',  # relleno (mfc)
        markeredgecolor='black',  # borde (mec)
        markeredgewidth=1.5)      # grosor borde (mew)
```

## Buenas prácticas

1. Usa `marker='o'` como opción por defecto: legible en casi cualquier fondo.
2. Para muchos puntos prefiere `'.'` o `','`: ocupan menos y reducen ruido visual.
3. Distingue series por **forma** además de color (accesibilidad daltónica): `'o'`, `'s'`, `'^'`.
4. Controla la densidad con `markevery` cuando hay miles de puntos.
5. Para "solo marcadores" usa `linestyle='none'` o el `fmt` sin guion.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Marcador no aparece | `marker` correcto pero `ms` muy pequeño o `linestyle` tapa | sube `markersize`; verifica `ls` |
| `ValueError: Unrecognized marker style` | código inexistente (ej. `'z'`) | usa un código de la tabla |
| Línea desaparece al poner solo marcador en `fmt` | el `fmt` sin guion implica `ls='none'` | añade `'-'`, p. ej. `'o-'` |
| LaTeX no renderiza | falta `$...$` o escape | usa `marker='$\\alpha$'` con string raw o doble barra |
| Marcadores saturan el gráfico | demasiados puntos | aplica `markevery=N` |

## Notas relacionadas

- [[ax.plot]]
- [[Line2D]]
- [[Estilos_Linea]]
- [[Colores_Nombres]]
