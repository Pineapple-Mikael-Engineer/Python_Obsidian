---
title: np.trapz — Integral numérica por regla del trapecio
aliases:
  - trapz
  - np.trapz
  - integral
  - regla del trapecio
tags:
  - numpy
  - api/funcion
  - reducciones

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray o escalar
inplace: false

# --- Dependencias ---
requiere:
  - concepto_axis_parametro

draft: false
---

# np.trapz — Integral numérica por regla del trapecio

## Firma de la función

```python
np.trapz(
    y,
    x=None,
    dx=1.0,
    axis=-1
) -> ndarray | escalar
```

## Valor de retorno

Aproxima la **integral** (área bajo la curva) de `y` mediante la regla del trapecio. Es una reducción: colapsa el eje integrado a un escalar.

| Entrada | Salida |
|---------|--------|
| `y=[0,1,2,3]` (dx=1) | `4.5` |
| `y=[0,1,4,9]`, `x=[0,1,2,3]` | área bajo los puntos |

```python
import numpy as np
y = np.array([0, 1, 2, 3])
np.trapz(y)   # 4.5
```

## Parámetros en detalle

### `y` — valores de la función

Array con las alturas muestreadas.

### `x` — coordenadas (espaciado variable)

Si se da, define el espaciado real entre puntos. Tiene prioridad sobre `dx`.

```python
x = np.linspace(0, np.pi, 100)
y = np.sin(x)
np.trapz(y, x)   # ≈ 2.0  (integral de sin en [0, π])
```

### `dx` — espaciado uniforme

Paso constante entre puntos cuando `x` no se proporciona.

### `axis` — eje de integración

Por defecto `-1`. Ver [[concepto_axis_parametro]].

## Casos de uso

### Energía / trabajo a partir de una curva

```python
tiempo = np.linspace(0, 10, 500)
potencia = curva_potencia(tiempo)
energia = np.trapz(potencia, tiempo)
```

### Área bajo una curva ROC

```python
auc = np.trapz(tpr, fpr)
```

## Buenas prácticas

1. Pasa `x` cuando el muestreo **no** sea uniforme; usa `dx` si lo es.
2. Más puntos → mejor aproximación (menor error del trapecio).
3. Para derivar (lo inverso), usa [[np.gradient]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultado escalado mal | no se pasó `x`/`dx` correcto | indicar el espaciado real |
| Signo inesperado | `x` decreciente | el área sale negativa; ordenar `x` |
| Baja precisión | pocos puntos | aumentar el muestreo |

## Limitaciones

- Aproximación de primer orden (lineal entre puntos).
- En NumPy reciente, `np.trapz` se renombra a `np.trapezoid` (alias mantenido por compatibilidad).

## Notas relacionadas

- [[concepto_axis_parametro]]
- [[np.gradient]]
- [[np.diff]]
- [[np.cumsum]]
