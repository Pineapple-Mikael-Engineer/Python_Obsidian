---
title: Reglas — Manim
tags:
  - manim
  - reglas
draft: true
---

# 📐 Reglas de redaccion — Manim

Convenciones especificas para documentar **Manim Community Edition** (animacion matematica
orientada a objetos). Especializan el [[Estandarizan Directorio Librerias | estandar base de
librerias]]; ante conflicto, manda el estandar base. El **donde** vive cada nota lo define
[[Tree Manim]].

> [!important] Es Manim **Community Edition** (CE)
> Documentamos la API de **ManimCE** (`pip install manim`, `from manim import *`), NO la ManimGL
> de 3blue1brown: muchas clases/firmas difieren. Si una API es exclusiva de una version, avisarlo.

> [!important] El idioma: SIN TILDES en el cuerpo
> Como SciPy/SymPy/VisPy/PyQt6: nada de a/e/i/o/u acentuadas ni en titulo ni en cuerpo (solo se
> conserva la ñ: tamaño, añadir, diseño). El codigo y los nombres LaTeX van tal cual.

---

## 1. La triada mental (la idea que gobierna Manim)

Toda nota debe respetar la separacion de los tres roles; no confundirlos es la clave de Manim:

| Rol | Que es | Ejemplo | Hereda de |
|-----|--------|---------|-----------|
| **Scene** | el lienzo + el guion (`construct`) donde ocurre todo | `class Demo(Scene)` | `Scene` |
| **Mobject** | un objeto dibujable (QUE se ve) | `Circle()`, `MathTex(...)` | `Mobject`/`VMobject` |
| **Animation** | una transformacion en el tiempo (COMO cambia) | `Create(c)`, `Transform(a, b)` | `Animation` |

- Un `Circle` **no es** una animacion: `Create(Circle())` lo es. No documentar `Circle` como si se
  reprodujera; se **anade** (`self.add`) o se **anima** (`self.play(Create(...))`).
- `self.play(animacion)` reproduce · `self.add(mobject)` muestra sin animar · `self.wait()` pausa.

---

## 2. Naming de archivos (API-style)

| Tipo de nota | Patron | Ejemplo |
|--------------|--------|---------|
| Clase (Mobject/Animation/Scene/Camera) | `<NombreReal>.md` | `Circle.md`, `ReplacementTransform.md` |
| Metodo (de Scene o de posicionamiento) | `<Clase>.<metodo>.md` o `<metodo>.md` | `Scene.play.md`, `next_to.md` |
| Concepto transversal | `concepto_<tema>.md` | `concepto_animate_syntax.md` |
| Patron (receta) | `<tema>.md` | `mobject_personalizado.md` |
| Indice de carpeta | `index.md` | uno por **cada** directorio |

- Clases con su **nombre real** y mayusculas exactas (`ThreeDScene`, `MathTex`, `VGroup`).
- El nombre del archivo = exactamente lo que se wikilinkea (`[[Circle]]`).

---

## 3. Frontmatter de una nota de CLASE

La **herencia** y la **categoria** (mobject/animation/scene) son datos de primera clase.

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

- **`categoria`**: distingue los tres roles (`mobject` | `animation` | `scene` | `camera`). Lo que
  hace consultable la libreria.
- **`hereda_de`**: la clase padre **directa** (`Circle` -> `Arc`). La cadena completa hasta `Mobject`
  o `Animation` se muestra en el `classDiagram` del cuerpo.
- **`order`** (entero): fija el **orden de lectura** de la nota respecto a sus **hermanas** —las otras
  notas del **mismo** directorio—; el menor se lee primero. Regla clave del `index`: **el `index.md`
  NO es hermano de las notas que indexa**, sino de los `index.md` de los **directorios hermanos**; su
  `order` decide en que orden se recorren las **subcarpetas**, no las notas de dentro (esas se ordenan
  entre si con su propio `order`).
- **`tipo`** para no-clases: `concepto | metodo | patron`.
- Maximo **3–5 tags**; nunca `python`, `animacion` a secas, ni el path repetido.

---

## 4. Indice por carpeta (`index.md`) — OBLIGATORIO y con `classDiagram`

> [!regla]
> Cada directorio lleva su `index.md` como **nota madre** (no un listado). Debe incluir un
> **`classDiagram` de Mermaid** con la rama de herencia de esa carpeta (p. ej. la jerarquia de
> geometria bajo `VMobject`, o la de las animaciones de creacion bajo `Animation`).

Estructura del `index.md`: titulo + parrafo · `## En accion` (una `Scene` ejecutable usando varias
clases del grupo + el comando CLI) · `## Herencia` (`classDiagram` decorado) · `## Clases que aporta`
(tabla `| Clase | Hereda de | Para que |`) · `## Como elegir` (tabla de decision) · `## Notas
relacionadas`.

---

## 5. Estructura de una nota de CLASE (orden de capas)

> [!regla] Profundidad: NO te quedes en dos niveles
> Una nota de clase **no** es una lista de headers `##` con un parrafo debajo cada uno. Cada seccion
> `##` se **desarrolla en sub-secciones `###` (y `####` cuando haga falta)**. La herencia, el
> constructor, los metodos y los ejemplos casi siempre necesitan **varios `###`** para explicarse de
> verdad. Una nota que solo llega a `##` es senal de que esta sin desarrollar.

Las secciones `##` (cada una se ramifica en `###`/`####`):

1. `# titulo` + parrafo de **que es y cuando usarla** (y su rol: mobject/animation/scene).
2. `## Importacion` — `from manim import Circle`.
3. `## Herencia`
   - `### La cadena` — `classDiagram` de la herencia completa hasta `Mobject`/`Animation`.
   - `### Que aporta cada ancestro` — de donde vienen color, posicion, animacion (lo que no define, lo hereda).
4. `## Constructor`
   - `### Firma` — bloque ```python con la firma, tipos y valores por defecto.
   - `### Parametros principales` — tabla `| Parametro | Tipo | Defecto | Controla |`; un parametro
     con trampa puede llevar su propio `#### <parametro>` con ejemplo.
   - `### Parametros de estilo` — `color`, `fill_opacity`, `stroke_width`...
5. `## Metodos clave` — agrupados por `###`: `### Transformar` (`shift`, `scale`, `rotate`),
   `### Estilizar` (`set_color`, `set_fill`), `### Consultar` (`get_center`, `get_width`); una tabla
   por grupo. Remitir a [[posicionamiento]] / [[estilo]] para los transversales.
6. `## Ejemplo`
   - `### Version minima` — la `Scene` ejecutable mas corta + el **comando CLI** (ver §6).
   - `### Version completa` — un ejemplo realista que combine varias capacidades de la clase.
   - `### Variaciones` — los kwargs/metodos mas utiles en accion, cada uno con su mini-`Scene`.
7. `## Animarla` (Mobject) / `## Parametros de la animacion` (Animation)
   - `### Crear y transformar` — `Create`, `Transform`, `.animate`.
   - `### run_time y rate_func` · `### Componerla` con [[AnimationGroup]]/[[LaggedStart]].
8. `## Personalizar (subclasear)` — `### Que sobreescribir` + `### Ejemplo de subclase` (un VMobject
   propio define su geometria en `__init__`; una Animation propia define `interpolate_mobject`).
9. `## Errores comunes` — tabla error -> causa -> solucion.
10. `## Notas relacionadas`.

> La profundidad se adapta: una clase central (`Mobject`, `Scene`, `Transform`) tendra muchos `###`
> y algun `####`; una figura simple, menos. Pero **el desarrollo en `###`/`####` y el ejemplo
> ejecutable (Scene + comando) son el liston** de toda nota de clase.

---

## 6. Convencion Manim — patrones criticos a documentar

- **Todo ejemplo es una `Scene` ejecutable.** Patron minimo:
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
- **La sintaxis `.animate`**: `self.play(c.animate.shift(RIGHT))` **anima** el cambio;
  `c.shift(RIGHT)` lo aplica **al instante** (sin animacion). Distinguirlo siempre.
- **Constantes de direccion**: `UP`, `DOWN`, `LEFT`, `RIGHT`, `UL`, `UR`, `DL`, `DR`, `ORIGIN`
  (vectores numpy). El posicionamiento (`shift`, `next_to`, `to_edge`) usa estas constantes.
- **Colores en MAYUSCULAS**: `RED`, `BLUE`, `GREEN`, `YELLOW`, `WHITE`... (constantes de Manim).
- **Herencia para personalizar**: un objeto propio subclasea `VMobject` (define sus puntos/geometria
  en `__init__`); una animacion propia subclasea `Animation` (`interpolate_mobject(alpha)`).
- **LaTeX**: `Tex`/`MathTex` requieren una instalacion de LaTeX; avisarlo donde aplique.

---

## 7. Mermaid (herencia) — decorado

Los diagramas de herencia usan `classDiagram`. Para flujos (el ciclo de una Scene, el render) o
arboles de decision, usar `flowchart` con esta paleta:

```
    classDef base fill:#5e81ac,stroke:#88c0d0,stroke-width:2px,color:#eceff4;
    classDef grupo fill:#3b4252,stroke:#81a1c1,stroke-width:1.5px,color:#88c0d0;
    classDef hoja fill:#2e3440,stroke:#a3be8c,color:#d8dee9;
```

- Labels de nodo SIEMPRE entre comillas dobles.
- En `classDiagram`, miembros solo como `+metodo()` / `+atributo` (sin corchetes, `=`, `*` ni `...`).

---

## 8. Wikilinks (resumen del estandar base)

- 1–2 apariciones por nota, en la primera mencion significativa; en parrafos, no en tablas.
- ❌ Nunca en headers, codigo, frontmatter ni titulos.
- A clase: por basename `[[Circle]]`, `[[Transform]]`.
- A `index` de carpeta: con ruta `[[Manim/mobjects/geometria/index | geometria]]`.
- En tablas: escapa el pipe `\|`.
- Seccion final **obligatoria** `## Notas relacionadas`.

---

## 9. Flujo de trabajo

1. Disenar/actualizar [[Tree Manim]] (roadmap).
2. `conceptos_transversales/` + `index.md` raiz a mano (modelo mental Scene/Mobject/Animation +
   classDiagram global).
3. Rellenar areas con subagentes + revision; cada `index.md` con su `classDiagram`.
4. Mantener `categoria`/`hereda_de` correctos (es lo que hace la libreria consultable).

---

## Notas relacionadas

- [[Tree Manim]]
- [[Estandarizan Directorio Librerias]]
