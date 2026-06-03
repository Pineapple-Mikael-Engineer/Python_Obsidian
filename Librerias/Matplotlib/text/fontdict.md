---
title: fontdict — Propiedades de fuente para texto
aliases:
  - fontdict
  - propiedades de fuente
  - estilo de texto
tags:
  - matplotlib
  - api/objeto
  - styling

# --- Clasificación ---
lib: matplotlib
mod: matplotlib.text
tipo: objeto

# --- Comportamiento ---
muta_estado: false

draft: false
---

# fontdict — Propiedades de fuente para texto

## Definición

`fontdict` es un **diccionario de propiedades de fuente** (familia, tamaño, peso, estilo, color) que se aplica al texto de matplotlib. Las mismas propiedades pueden pasarse de tres maneras intercambiables:

- como **kwargs sueltos**: `ax.set_title("t", fontsize=14, fontweight='bold')`
- como **diccionario** vía el parámetro `fontdict`: `ax.set_title("t", fontdict={'fontsize': 14})`
- como **default global** mediante `rcParams['font.*']`, que afecta a toda la figura.

Cualquier llamada que genere un objeto [[Text]] (`set_title`, `set_xlabel`, `ax.text`, `legend`, ...) acepta estas propiedades. No es una clase con estado propio: es una convención de configuración de estilo.

## Valor de retorno

`fontdict` no retorna nada por sí mismo: es un argumento de configuración. Su efecto es **fijar el estilo** del `Text` que crea la función receptora.

| Forma | Alcance |
|-------|---------|
| kwargs sueltos | solo ese texto concreto |
| `fontdict={...}` | solo ese texto concreto |
| `rcParams['font.*']` | todos los textos de la sesión |

## Parámetros en detalle

| Clave | Alias kwarg | Tipo / valores | Descripción |
|-------|-------------|----------------|-------------|
| `family` | `fontfamily` | `'serif'`, `'sans-serif'`, `'monospace'`, nombre | Familia tipográfica |
| `size` | `fontsize` | float o `'small'`, `'large'`, `'x-large'` | Tamaño en puntos o relativo |
| `weight` | `fontweight` | `'normal'`, `'bold'`, número 0..1000 | Grosor del trazo |
| `style` | `fontstyle` | `'normal'`, `'italic'`, `'oblique'` | Inclinación |
| `color` | `color` / `c` | nombre, hex, RGB(A) | Color del texto |
| `variant` | — | `'normal'`, `'small-caps'` | Variante tipográfica |

### rcParams globales equivalentes

| rcParam | Default | Equivale a |
|---------|---------|-----------|
| `font.family` | `'sans-serif'` | `family` |
| `font.size` | `10.0` | `size` |
| `font.weight` | `'normal'` | `weight` |
| `font.style` | `'normal'` | `style` |

## Casos de uso

### Estilo puntual con kwargs

```python
ax.set_title("Resultados", fontsize=16, fontweight='bold', color='navy')
```

### El mismo estilo como diccionario reutilizable

```python
estilo = {'family': 'serif', 'size': 14, 'weight': 'bold', 'color': 'darkred'}
ax.set_xlabel("Tiempo (s)", fontdict=estilo)
ax.set_ylabel("Amplitud", fontdict=estilo)   # reaprovechado
```

### Default global para toda la figura

```python
import matplotlib as mpl
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.size'] = 12
# a partir de aquí todo el texto hereda estos valores
```

### Combinado con texto matemático

```python
ax.set_title(r'$\alpha$ frente a $\beta$', fontsize=15, fontstyle='italic')
```

## Buenas prácticas

1. Para un único texto, los kwargs sueltos (`fontsize=`, `fontweight=`) son más legibles que `fontdict={...}`.
2. Define un `fontdict` cuando vayas a **reutilizar** el mismo estilo en varios textos: centraliza y evita repetición.
3. Para un look uniforme en toda la figura o el proyecto, configúralo en [[rcParams]] (`font.*`) en lugar de repetirlo nota a nota.
4. Las propiedades de fuente son ortogonales al contenido matemático: el estilo lo da `fontdict`, las fórmulas las da [[LaTeX_mathtext]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| kwarg ignorado | mezclar `fontdict` y el mismo kwarg suelto | usa una sola vía por propiedad |
| Fuente no cambia | el nombre de familia no existe en el sistema | usa familia genérica (`'serif'`) o instala la fuente |
| `weight='bold'` sin efecto | la familia no tiene variante negrita | elige otra familia o usa peso numérico |
| Tamaño inconsistente entre notas | se fijó por texto en vez de global | centraliza en `rcParams['font.size']` |

## Notas relacionadas

- [[Text]]
- [[LaTeX_mathtext]]
- [[rcParams]]
- [[ax.text]]
