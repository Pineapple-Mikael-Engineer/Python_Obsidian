---
title: Reglas — Manim
tags:
  - manim
  - reglas
draft: true
---

# 📐 Reglas de redacción — Manim

Convenciones específicas para documentar **Manim Community Edition** (animación matemática orientada a objetos). Especializan el [[Estandarizan Directorio Librerias | estándar base de librerías]]; ante conflicto, manda el estándar base. El **dónde** vive cada nota lo define [[Tree Manim]].

> [!important] Es Manim **Community Edition** (CE)
> Documentamos la API de **ManimCE** (`pip install manim`, `from manim import *`), NO la ManimGL de 3blue1brown: muchas clases y firmas difieren. Si una API es exclusiva de una versión, avisarlo.

> [!important] El idioma: español normal, CON tildes y ñ en el cuerpo
> El contenido de las notas usa ortografía española correcta: tildes (función, animación, círculo, método) y ñ (tamaño, añadir, diseño). Los símbolos especiales SOLO están prohibidos al **nombrar el archivo** (los nombres van en ASCII: `concepto_scene_construct.md`, `Circle.md`), nunca dentro de la nota. El código y los nombres LaTeX van tal cual.

> [!important] Formato: un párrafo = una línea (no cortar líneas a mano)
> NO partas los párrafos en varias líneas a ~100 columnas. Cada párrafo (y cada celda de tabla, ítem de lista o línea de callout) va en **una sola línea**; el editor hace el ajuste visual. Cortar a mano **rompe los wikilinks** que caen sobre el salto y deja el texto disparejo.

---

## 1. La tríada mental (la idea que gobierna Manim)

Toda nota debe respetar la separación de los tres roles; no confundirlos es la clave de Manim:

| Rol | Qué es | Ejemplo | Hereda de |
|-----|--------|---------|-----------|
| **Scene** | el lienzo + el guion (`construct`) donde ocurre todo | `class Demo(Scene)` | `Scene` |
| **Mobject** | un objeto dibujable (QUÉ se ve) | `Circle()`, `MathTex(...)` | `Mobject`/`VMobject` |
| **Animation** | una transformación en el tiempo (CÓMO cambia) | `Create(c)`, `Transform(a, b)` | `Animation` |

- Un `Circle` **no es** una animación: `Create(Circle())` lo es. No documentar `Circle` como si se reprodujera; se **añade** (`self.add`) o se **anima** (`self.play(Create(...))`).
- `self.play(animacion)` reproduce · `self.add(mobject)` muestra sin animar · `self.wait()` pausa.

---

## 2. Naming de archivos (API-style)

Recuerda: el **nombre del archivo va en ASCII** (sin tildes ni ñ); el contenido, en español normal.

| Tipo de nota | Patrón | Ejemplo |
|--------------|--------|---------|
| Clase (Mobject/Animation/Scene/Camera) | `<NombreReal>.md` | `Circle.md`, `ReplacementTransform.md` |
| Método (de Scene o de posicionamiento) | `<Clase>.<metodo>.md` o `<metodo>.md` | `Scene.play.md`, `next_to.md` |
| Concepto transversal | `concepto_<tema>.md` | `concepto_animate_syntax.md` |
| Patrón (receta) | `<tema>.md` | `mobject_personalizado.md` |
| Índice de carpeta | `index.md` | uno por **cada** directorio |

- Clases con su **nombre real** y mayúsculas exactas (`ThreeDScene`, `MathTex`, `VGroup`).
- El nombre del archivo = exactamente lo que se wikilinkea (`[[Circle]]`).

---

## 3. Frontmatter de una nota de CLASE

La **herencia** y la **categoría** (mobject/animation/scene) son datos de primera clase.

```yaml
---
title: Circle — circunferencia (VMobject de geometria)
aliases:
  - Circle
  - circulo
tags:
  - manim
  - api/clase
  - geometria          # dominio = rama del Tree (geometria | texto | graficos | transformacion ...)
lib: manim
categoria: mobject     # mobject | animation | scene | camera | otro
hereda_de: Arc         # la clase PADRE directa (cadena de herencia)
order: 2               # orden de lectura entre las notas HERMANAS del directorio
requiere:
  - concepto_mobject
draft: false
---
```

- **`categoria`**: distingue los tres roles (`mobject` | `animation` | `scene` | `camera`). Es lo que hace consultable la librería.
- **`hereda_de`**: la clase padre **directa** (`Circle` -> `Arc`). La cadena completa hasta `Mobject` o `Animation` se muestra en el `classDiagram` del cuerpo.
- **`order`** (entero): fija el **orden de lectura** de la nota respecto a sus **hermanas** —las otras notas del **mismo** directorio—; el menor se lee primero. Regla clave del `index`: **el `index.md` NO es hermano de las notas que indexa**, sino de los `index.md` de los **directorios hermanos**; su `order` decide en qué orden se recorren las **subcarpetas**, no las notas de dentro (esas se ordenan entre sí con su propio `order`).
- **`tipo`** para no-clases: `concepto | metodo | patron`.
- Máximo **3–5 tags**; nunca `python`, `animacion` a secas, ni el path repetido.

---

## 4. Índice por carpeta (`index.md`) — OBLIGATORIO y con `classDiagram`

> [!regla] El index es una nota completa, NO un listado
> Cada directorio lleva su `index.md` como **nota madre de pleno derecho**: además de presentar a sus hijas, **enseña el grupo** con ejemplos ejecutables, modos de uso, recetas cortas y los errores o decisiones comunes a todas. Debe incluir un **`classDiagram` de Mermaid** con la rama de herencia de esa carpeta (p. ej. la jerarquía de geometría bajo `VMobject`).

Estructura del `index.md` (desarrollada, no mínima): título + párrafo · `## En accion` (una `Scene` ejecutable real que combine varias clases del grupo + el comando CLI) · `## Herencia` (`classDiagram` decorado) · `## Clases que aporta` (tabla `| Clase | Hereda de | Para que |`) · `## Como elegir` (tabla/árbol de decisión) · `## Patrones y recetas del grupo` (2-3 mini-`Scene` con usos típicos: combinar las clases, el truco que comparten, el error frecuente) · `## Notas relacionadas`. La intención es que, leyendo solo el index, ya se aprenda a usar el grupo.

---

## 5. Estructura de una nota de CLASE (orden de capas)

> [!regla] Profundidad: NO te quedes en dos niveles
> Una nota de clase **no** es una lista de headers `##` con un párrafo debajo cada uno. Cada sección `##` se **desarrolla en sub-secciones `###` (y `####` cuando haga falta)**. La herencia, el constructor, los métodos y los ejemplos casi siempre necesitan **varios `###`** para explicarse de verdad. Una nota que solo llega a `##` es señal de que está sin desarrollar. No importa que la nota quede larga: la intención es que enseñe mucho.

Las secciones `##` (cada una se ramifica en `###`/`####`):

1. `# titulo` + párrafo de **qué es y cuándo usarla** (y su rol: mobject/animation/scene).
2. `## Importacion` — `from manim import Circle`.
3. `## Herencia`
   - `### La cadena` — `classDiagram` de la herencia completa hasta `Mobject`/`Animation`.
   - `### Que aporta cada ancestro` — de dónde vienen color, posición, animación (lo que no define, lo hereda).
4. `## Constructor` — primero el bloque ```python con la firma, tipos y valores por defecto; y DEBAJO, sus parámetros y el retorno como **subsecciones** (`###`/`####`), nunca como `##` hermanos:
   - `### Parametros principales` — tabla `| Parametro | Tipo | Defecto | Controla |`; un parámetro con trampa puede llevar su propio `#### <parametro>` con ejemplo.
   - `### Parametros de estilo` — `color`, `fill_opacity`, `stroke_width`...
   - `### Que construye / devuelve` — qué objeto produce.
5. `## Metodos clave` — agrupados por `###`: `### Transformar` (`shift`, `scale`, `rotate`), `### Estilizar` (`set_color`, `set_fill`), `### Consultar` (`get_center`, `get_width`); una tabla por grupo. Remitir a [[posicionamiento]] / [[estilo]] para los transversales.
6. `## Ejemplo`
   - `### Version minima` — la `Scene` ejecutable más corta + el **comando CLI** (ver §6).
   - `### Version completa` — un ejemplo realista que combine varias capacidades de la clase.
   - `### Variaciones` — los kwargs/métodos más útiles en acción, cada uno con su mini-`Scene`.
7. `## Animarla` (Mobject) / `## Parametros de la animacion` (Animation)
   - `### Crear y transformar` — `Create`, `Transform`, `.animate`.
   - `### run_time y rate_func` · `### Componerla` con [[AnimationGroup]]/[[LaggedStart]].
8. `## Personalizar (subclasear)` — `### Que sobreescribir` + `### Ejemplo de subclase` (un VMobject propio define su geometría en `__init__`; una Animation propia define `interpolate_mobject`).
9. `## Errores comunes` — tabla error -> causa -> solución.
10. `## Notas relacionadas`.

> La profundidad se adapta: una clase central (`Mobject`, `Scene`, `Transform`) tendrá muchos `###` y algún `####`; una figura simple, menos. Pero **el desarrollo en `###`/`####` y el ejemplo ejecutable (Scene + comando) son el listón** de toda nota de clase.

---

## 5b. Estructura de una nota de MÉTODO (`Scene.play`, `next_to`...)

> [!regla] Los parámetros y el retorno van DENTRO de la firma
> El error a evitar: poner `## Firma`, `## Parametros` y `## Devuelve` al **mismo** nivel `##`. Conceptualmente los parámetros y el valor de retorno **son parte de la firma**, así que van como **subsecciones `###` debajo de `## Firma`**. Así la firma destaca como el ancla de la nota.

Estructura de una nota de método:

1. `# título` + párrafo de qué hace y cuándo se usa.
2. `## Firma` — el ancla de la nota:
   - el bloque ```python con la firma completa (tipos y defaults).
   - `### Parametros` — uno por `####` o una tabla `| Parametro | Tipo | Defecto | Que controla |`; los que tengan trampa, con su mini-ejemplo.
   - `### Valor de retorno` — qué devuelve (a menudo `None` o `self` para encadenar).
3. `## Ejemplos` — varios, progresivos, cada uno una `Scene` ejecutable + comando.
4. `## Errores comunes` — tabla.
5. `## Notas relacionadas`.

La misma regla aplica a la firma del constructor de una clase (§5.4): el bloque primero, los parámetros y el retorno como `###` debajo.

---

## 6. Convención Manim — patrones críticos a documentar

- **Todo ejemplo es una `Scene` ejecutable.** Patrón mínimo:
  ```python
  from manim import *

  class Demo(Scene):
      def construct(self):
          c = Circle(color=BLUE)
          self.play(Create(c))
          self.wait()
  ```
  y SIEMPRE el comando para renderizar debajo:
  ```bash
  manim -pql archivo.py Demo      # -p reproduce, q=quality (l=low / h=high)
  ```
- **La sintaxis `.animate`**: `self.play(c.animate.shift(RIGHT))` **anima** el cambio; `c.shift(RIGHT)` lo aplica **al instante** (sin animación). Distinguirlo siempre.
- **Constantes de dirección**: `UP`, `DOWN`, `LEFT`, `RIGHT`, `UL`, `UR`, `DL`, `DR`, `ORIGIN` (vectores numpy). El posicionamiento (`shift`, `next_to`, `to_edge`) usa estas constantes.
- **Colores en MAYÚSCULAS**: `RED`, `BLUE`, `GREEN`, `YELLOW`, `WHITE`... (constantes de Manim).
- **Herencia para personalizar**: un objeto propio subclasea `VMobject` (define sus puntos/geometría en `__init__`); una animación propia subclasea `Animation` (`interpolate_mobject(alpha)`).
- **LaTeX**: `Tex`/`MathTex` requieren una instalación de LaTeX; avisarlo donde aplique.

---

## 7. Mermaid (herencia) — decorado

Los diagramas de herencia usan `classDiagram`. Para flujos (el ciclo de una Scene, el render) o árboles de decisión, usar `flowchart` con esta paleta:

```
    classDef base fill:#5e81ac,stroke:#88c0d0,stroke-width:2px,color:#eceff4;
    classDef grupo fill:#3b4252,stroke:#81a1c1,stroke-width:1.5px,color:#88c0d0;
    classDef hoja fill:#2e3440,stroke:#a3be8c,color:#d8dee9;
```

- Labels de nodo SIEMPRE entre comillas dobles.
- En `classDiagram`, miembros solo como `+metodo()` / `+atributo` (sin corchetes, `=`, `*` ni `...`).

---

## 8. Wikilinks (resumen del estándar base)

- 1–2 apariciones por nota, en la primera mención significativa; en párrafos, no en tablas.
- ❌ Nunca en headers, código, frontmatter ni títulos.
- ❌ Nunca partidos por un salto de línea (ver la regla de formato): un wikilink va entero en su línea.
- A clase: por basename `[[Circle]]`, `[[Transform]]`.
- A `index` de carpeta: con ruta `[[Manim/mobjects/geometria/index | geometria]]`.
- En tablas: escapa el pipe `\|`.
- Sección final **obligatoria** `## Notas relacionadas`.

---

## 9. Flujo de trabajo

1. Diseñar/actualizar [[Tree Manim]] (roadmap).
2. `conceptos_transversales/` + `index.md` raíz a mano (modelo mental Scene/Mobject/Animation + classDiagram global).
3. Rellenar áreas con subagentes + revisión; cada `index.md` con su `classDiagram`.
4. Mantener `categoria`/`hereda_de` correctos (es lo que hace la librería consultable).

---

## Notas relacionadas

- [[Tree Manim]]
- [[Estandarizan Directorio Librerias]]
