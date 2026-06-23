---
title: np/operaciones/trigonométricas — trigonometría, hiperbólicas y conversiones (ufuncs)
tags:
  - numpy
  - indice
draft: false
---

# np/operaciones/trigonométricas — trigonometría, hiperbólicas y conversiones (ufuncs)

Las [[concepto_ufuncs|ufuncs]] trigonométricas de NumPy: las **directas** (`sin`/`cos`/`tan`), sus
**inversas** (`arcsin`/`arccos`/`arctan`/`arctan2`), las **hiperbólicas** (`sinh`/`cosh`/`tanh`), las
**conversiones** de unidad (`deg2rad`/`rad2deg`) y `hypot` (hipotenusa). Son la base de cualquier
cálculo periódico, de señales o geométrico. Todas son element-wise: conservan el shape (las binarias,
`arctan2` e `hypot`, alinean por [[concepto_broadcasting|broadcasting]]).

> [!warning] Todo va en RADIANES
> Las directas esperan radianes en la entrada; las inversas devuelven radianes en la salida. Si tus
> datos están en grados, convierte **antes** con [[np.deg2rad]] (o `* np.pi / 180`) y **lee** los
> resultados en grados con [[np.rad2deg]]. Pasar grados a `np.sin` no da error: da un valor
> silenciosamente incorrecto.

## Función ↔ inversa

Cada función directa tiene su inversa, con dominio y rango acotados (en radianes):

| Directa | Inversa | Dominio de la inversa | Rango de la inversa |
|---|---|---|---|
| [[np.sin]] | [[np.arcsin]] | $[-1, 1]$ | $[-\pi/2,\ \pi/2]$ |
| [[np.cos]] | [[np.arccos]] | $[-1, 1]$ | $[0,\ \pi]$ |
| [[np.tan]] | [[np.arctan]] | $\mathbb{R}$ | $(-\pi/2,\ \pi/2)$ |

> [!tip] `arctan2(y, x)` frente a `arctan(y/x)`
> `np.arctan` solo ve el cociente `y/x`, así que **pierde el cuadrante** (rango $(-\pi/2, \pi/2)$) y no
> distingue, p. ej., $(1, 1)$ de $(-1, -1)$. [[np.arctan2]] recibe `y` y `x` por separado, conserva
> los signos y devuelve el ángulo **correcto en los cuatro cuadrantes** (rango $(-\pi, \pi]$). Para el
> ángulo de un vector, usa siempre `arctan2`.

## Funciones de este grupo

| Grupo | ufunc | Descripción |
|---|---|---|
| **Directas** | [[np.sin]] | seno; rango de salida $[-1, 1]$ |
| | [[np.cos]] | coseno; rango de salida $[-1, 1]$ |
| | [[np.tan]] | tangente; singularidades en $\pi/2 + n\pi$ (valores enormes, sin error) |
| **Inversas** | [[np.arcsin]] | arcoseno; dominio $[-1, 1]$, rango $[-\pi/2, \pi/2]$ |
| | [[np.arccos]] | arcocoseno; dominio $[-1, 1]$, rango $[0, \pi]$ |
| | [[np.arctan]] | arcotangente, rango $(-\pi/2, \pi/2)$; pierde el cuadrante |
| | [[np.arctan2]] | arcotangente de `(y, x)`; ángulo correcto en los 4 cuadrantes (binaria) |
| **Hiperbólicas** | [[np.sinh]] | seno hiperbólico; crece exponencialmente (riesgo de overflow) |
| | [[np.cosh]] | coseno hiperbólico; siempre $\ge 1$ |
| | [[np.tanh]] | tangente hiperbólica; rango $(-1, 1)$, usada como activación en redes |
| **Conversiones** | [[np.deg2rad]] | grados → radianes ($x \cdot \pi/180$); alias `np.radians` |
| | [[np.rad2deg]] | radianes → grados ($x \cdot 180/\pi$); alias `np.degrees` |
| **Geometría** | [[np.hypot]] | hipotenusa $\sqrt{x^2+y^2}$ sin overflow intermedio (binaria) |

## Notas relacionadas

- [[concepto_ufuncs]]
- [[concepto_broadcasting]]
- [[Librerias/Numpy/np/operaciones/index\|np/operaciones — ufuncs element-wise]]
