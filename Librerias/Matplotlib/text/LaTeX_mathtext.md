---
title: LaTeX y mathtext — Matemáticas en el texto
aliases:
  - LaTeX
  - mathtext
  - LaTeX en matplotlib
  - texto matemático
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

# LaTeX y mathtext — Matemáticas en el texto

## Definición

matplotlib renderiza **expresiones matemáticas** dentro de cualquier cadena de texto (títulos, labels de ejes, leyendas, anotaciones). Hay dos vías:

- **mathtext** (por defecto): un *subconjunto* de la sintaxis TeX que matplotlib dibuja por su cuenta, **sin instalar nada**. Se activa encerrando la expresión entre signos de dólar: `r'$\alpha^2 + \beta_i$'`.
- **LaTeX completo**: delega el renderizado a una instalación real de LaTeX activando `rcParams['text.usetex'] = True`. Soporta toda la sintaxis TeX y paquetes, pero **requiere LaTeX instalado** en el sistema.

Cualquier texto que produce un objeto [[Text]] acepta estas expresiones. Usa siempre *raw strings* (`r'...'`) para que las barras invertidas no se interpreten como secuencias de escape de Python.

## Valor de retorno

mathtext y `usetex` no son funciones: son **modos de interpretación** de la cadena. No retornan un valor propio; afectan a cómo se dibuja el texto.

| Vía | Cómo se activa | Requiere instalación |
|-----|----------------|----------------------|
| mathtext | `$...$` dentro de la cadena | No |
| LaTeX completo | `rcParams['text.usetex'] = True` | Sí (distribución LaTeX) |

## Parámetros en detalle

### Sintaxis mathtext (subset de TeX)

| Sintaxis | Resultado | Ejemplo |
|----------|-----------|---------|
| `^` | superíndice | `$x^2$` → x² |
| `_` | subíndice | `$x_i$` → xᵢ |
| `{ }` | agrupa varios caracteres | `$x^{2n}$` |
| `\frac{a}{b}` | fracción | `$\frac{1}{2}$` |
| `\sqrt{x}` | raíz | `$\sqrt{x+1}$` |
| `\sum`, `\int`, `\prod` | sumatorio, integral, productorio | `$\sum_{i=0}^{n} x_i$` |
| `\alpha \beta \gamma` | letras griegas | `$\alpha + \beta$` |
| `\mathbf{x}` | negrita matemática | `$\mathbf{v}$` |
| `\,` `\;` | espacios finos | `$a \, b$` |

### rcParams asociados

| rcParam | Default | Efecto |
|---------|---------|--------|
| `text.usetex` | `False` | `True` delega todo el texto a LaTeX externo |
| `mathtext.fontset` | `'dejavusans'` | fuente del modo mathtext (`'cm'`, `'stix'`, ...) |
| `mathtext.default` | `'it'` | estilo por defecto dentro de `$...$` |

## Casos de uso

### Label de eje con símbolos griegos

```python
fig, ax = plt.subplots()
ax.set_xlabel(r'$\theta$ (rad)')
ax.set_ylabel(r'$\sin(\theta)$')
```

### Título con fracción y superíndice

```python
ax.set_title(r'Energía: $E = \frac{1}{2} m v^2$')
```

### Sumatorio en una anotación

```python
ax.text(0.5, 0.5, r'$\sum_{i=1}^{n} x_i^2$')
```

### LaTeX completo (requiere instalación)

```python
import matplotlib as mpl
mpl.rcParams['text.usetex'] = True
ax.set_title(r'\textbf{Resultado} con $\mathcal{L}$')
```

## Buenas prácticas

1. Usa **siempre** raw strings (`r'...'`): evita que `\n`, `\t`, `\b`, etc. rompan la expresión.
2. Para la mayoría de gráficos basta mathtext: no actives `text.usetex` salvo que necesites paquetes o fuentes LaTeX exactas.
3. Combina texto normal y matemático en una misma cadena: `r'Velocidad $v$ en m/s'`.
4. Si quieres además controlar familia/tamaño/peso de la fuente, eso lo gestiona [[fontdict]], no mathtext.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `\alpha` aparece literal | falta encerrar en `$...$` | escribe `r'$\alpha$'` |
| Símbolo desaparece o da error | barra invertida escapada por Python | usa raw string `r'...'` |
| `usetex` falla al renderizar | LaTeX no instalado en el sistema | instala LaTeX o quédate en mathtext |
| Espaciado matemático raro | espacios normales dentro de `$...$` | usa `\,` o `\;` para espacios finos |
| Comando TeX no soportado | mathtext es solo un subset | activa `text.usetex` o reescribe la expresión |

## Notas relacionadas

- [[Text]]
- [[fontdict]]
- [[rcParams]]
- [[ax.text]]
