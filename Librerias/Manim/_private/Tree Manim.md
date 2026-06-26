---
title: Tree Manim
tags:
  - manim
  - meta
draft: true
---

# 🎬 Tree Manim

> Organización **jerárquica por rol en el modelo de Manim** (Community Edition). Manim es, como PyQt6, una librería muy **orientada a objetos**: se construye una **Scene**, se le añaden **Mobjects** (objetos matemáticos dibujables) y se los transforma con **Animations**. Por eso la **herencia** es dato de primera clase (campo `hereda_de` + `classDiagram` en cada index): casi todo lo dibujable hereda de `Mobject`/`VMobject` y casi toda transformación hereda de `Animation`. `✅` = nota creada · sin marca = roadmap pendiente.

---

## 📁 Tipos de notas

| Tipo | Ubicación | Ejemplo |
|------|-----------|---------|
| **Concepto transversal** | `conceptos_transversales/` | `concepto_scene_construct.md` |
| **Clase (Mobject/Animation/Scene)** | `<area>/` | `mobjects/geometria/Circle.md` |
| **Método de posicionamiento/estilo** | `posicionamiento/`, `estilo/` | `posicionamiento/next_to.md` |
| **Patrón / receta** | `patrones/` | `mobject_personalizado.md` |
| **Índice de carpeta** | `index.md` | nota madre con `classDiagram` de su rama |

> Naming API-style con el **nombre real** de la clase, respetando mayúsculas (`Circle.md`, `ReplacementTransform.md`, `ThreeDScene.md`). El método se nombra por su nombre (`next_to.md`). El nombre del archivo va en ASCII; el contenido, en español normal.

---

## 📂 Estructura completa (núcleo de animación 2D + intro 3D)

```tree
Manim/
│
├── index.md                              # modelo Manim: Scene + Mobject + Animation + classDiagram global
│
├── 📁 conceptos_transversales/            # el modelo mental (lo mas importante)
│   ├── concepto_scene_construct.md       # la Scene y construct(): el lienzo y el guion
│   ├── concepto_mobject.md               # Mobject: el arbol de objetos dibujables (points, submobjects)
│   ├── concepto_animation.md             # que es una Animation; self.play y run_time
│   ├── concepto_animate_syntax.md        # la sintaxis .animate (mobject.animate.shift(...))
│   ├── concepto_sistema_coordenadas.md   # UP/DOWN/LEFT/RIGHT/ORIGIN, unidades, el frame
│   ├── concepto_updaters.md              # updaters: animacion frame a frame y reactiva
│   ├── concepto_herencia_mobjects.md     # subclasear VMobject/Animation para lo propio
│   └── concepto_render_cli.md            # el flujo de render: manim -pql archivo.py Escena
│
├── 📁 escena/                             # Scene y sus variantes (donde ocurre todo)
│   ├── Scene.md                          # la clase base; se subclasea y se sobreescribe construct()
│   ├── MovingCameraScene.md              # camara que se mueve/zooma
│   ├── ThreeDScene.md                    # escenas 3D (set_camera_orientation)
│   ├── ZoomedScene.md
│   └── 📁 metodos/
│       ├── Scene.play.md                 # reproducir animaciones
│       ├── Scene.add.md                  # anadir mobjects sin animar
│       ├── Scene.wait.md                 # pausa
│       ├── Scene.remove.md
│       └── Scene.bring_to_front.md       # z-order
│
├── 📁 mobjects/                           # los objetos dibujables (que se ve)
│   ├── Mobject.md                        # CLASE BASE de todo lo dibujable
│   ├── VMobject.md                       # objeto VECTORIZADO (la mayoria): fill, stroke, points
│   ├── 📁 agrupacion/
│   │   ├── VGroup.md                     # agrupa VMobjects (se animan/posicionan juntos)
│   │   └── Group.md
│   ├── 📁 geometria/
│   │   ├── Circle.md
│   │   ├── Square.md
│   │   ├── Rectangle.md
│   │   ├── Polygon.md
│   │   ├── Triangle.md
│   │   ├── Line.md
│   │   ├── Arrow.md
│   │   ├── Vector.md
│   │   ├── Dot.md
│   │   ├── Arc.md
│   │   └── Ellipse.md
│   ├── 📁 texto/
│   │   ├── Text.md                       # texto normal (Pango)
│   │   ├── MarkupText.md
│   │   ├── Tex.md                        # LaTeX
│   │   ├── MathTex.md                    # LaTeX en modo matematico
│   │   └── Title.md
│   ├── 📁 graficos/
│   │   ├── Axes.md                       # ejes cartesianos
│   │   ├── NumberPlane.md                # plano con rejilla
│   │   ├── NumberLine.md
│   │   ├── FunctionGraph.md
│   │   └── ParametricFunction.md
│   ├── 📁 3d/
│   │   ├── ThreeDAxes.md
│   │   ├── Surface.md
│   │   ├── Sphere.md
│   │   └── Cube.md
│   └── 📁 tablas_extras/
│       ├── Table.md
│       ├── Matrix.md
│       ├── Brace.md
│       └── SurroundingRectangle.md
│
├── 📁 animaciones/                        # como cambian los mobjects (Animation)
│   ├── Animation.md                      # CLASE BASE de toda animacion
│   ├── 📁 creacion/
│   │   ├── Create.md
│   │   ├── Write.md                      # texto/formulas
│   │   ├── DrawBorderThenFill.md
│   │   ├── FadeIn.md
│   │   ├── GrowFromCenter.md
│   │   └── ShowIncreasingSubsets.md
│   ├── 📁 transformacion/
│   │   ├── Transform.md                  # morfa A en B
│   │   ├── ReplacementTransform.md       # A pasa a SER B (la habitual)
│   │   ├── TransformMatchingTex.md       # empareja sub-partes de LaTeX
│   │   ├── TransformMatchingShapes.md
│   │   └── FadeTransform.md
│   ├── 📁 movimiento/
│   │   ├── Rotate.md
│   │   ├── MoveAlongPath.md
│   │   └── Homotopy.md
│   ├── 📁 indicacion/
│   │   ├── Indicate.md
│   │   ├── Flash.md
│   │   ├── Circumscribe.md
│   │   ├── Wiggle.md
│   │   └── FocusOn.md
│   ├── 📁 desaparicion/
│   │   ├── FadeOut.md
│   │   ├── Uncreate.md
│   │   └── Unwrite.md
│   └── 📁 composicion/
│       ├── AnimationGroup.md             # varias a la vez
│       ├── LaggedStart.md                # en cascada
│       └── Succession.md                 # en secuencia
│
├── 📁 posicionamiento/                    # el sistema de coordenadas (donde colocar)
│   ├── constantes_direccion.md           # UP/DOWN/LEFT/RIGHT/UL/UR/.../ORIGIN
│   ├── shift_move_to.md                  # .shift (relativo) vs .move_to (absoluto)
│   ├── next_to.md                        # colocar relativo a otro mobject
│   ├── to_edge_to_corner.md
│   ├── align_to.md
│   └── arrange.md                        # distribuir un VGroup
│
├── 📁 dinamico/                           # animacion continua / reactiva
│   ├── ValueTracker.md                   # un numero animable
│   ├── add_updater.md                    # funcion por frame
│   ├── always_redraw.md                  # redibujar cada frame
│   └── DecimalNumber.md                  # numero en pantalla que cambia
│
├── 📁 camara/
│   ├── Camera.md
│   ├── MovingCamera.md
│   └── ThreeDCamera.md
│
├── 📁 estilo/                             # color y apariencia
│   ├── colores.md                        # RED/BLUE/..., set_color, gradientes, set_color_by_gradient
│   ├── set_style.md                      # fill_opacity, stroke_width, set_fill, set_stroke
│   └── rate_functions.md                 # smooth, linear, there_and_back, rush_into...
│
├── 📁 config_cli/
│   ├── config.md                         # objeto config: calidad, fondo, fps, tamano
│   └── cli.md                            # manim -pql/-pqh archivo.py Escena; flags utiles
│
└── 📁 patrones/                           # recetas POO (lo que distingue saber Manim)
    ├── escena_basica.md                  # el esqueleto minimo construct()
    ├── mobject_personalizado.md          # subclasear VMobject (un objeto propio)
    ├── animacion_personalizada.md        # subclasear Animation (interpolate_mobject)
    └── grafica_de_funcion.md             # Axes + plot + area + recta tangente
```

---

## 📊 Roadmap (estado de implementación)

> Rama **limpia** creada desde el commit de skills (`8e98b49`), sin notas de otras librerías. Núcleo de animación 2D primero; 3D y temas avanzados como roadmap.

| Bloque | Notas (aprox.) | Prioridad |
|--------|:---:|-----------|
| `conceptos_transversales/` | 8 | 🔴 primero (modelo mental Scene/Mobject/Animation) |
| `escena/` (Scene + métodos) | ~10 | 🔴 el contenedor de todo |
| `mobjects/` (geometría + texto + gráficos) | ~35 | 🟠 lo que se ve |
| `animaciones/` (creación + transform + ...) | ~25 | 🟠 lo que se mueve |
| `posicionamiento/` | 6 | 🟠 imprescindible para componer |
| `dinamico/` (updaters, ValueTracker) | 4 | 🟡 lo potente |
| `estilo/` + `config_cli/` | 5 | 🟢 apariencia y render |
| `camara/` + `mobjects/3d/` | ~7 | 🟢 3D (después) |
| `patrones/` | 4 | 🟡 recetas |

### Orden sugerido de relleno

1. **`conceptos_transversales`** + `index.md` raíz — Scene/construct, Mobject, Animation, coordenadas.
2. **`escena/Scene`** + sus métodos (`play`, `add`, `wait`) — el guion.
3. **`mobjects`** base (`Mobject`, `VMobject`, `VGroup`) + `geometria/` + `texto/`.
4. **`posicionamiento/`** — colocar y componer los mobjects.
5. **`animaciones`** (`creacion`, `transformacion`, `.animate`) — darles vida.
6. **`graficos/`** (Axes/plot), **`dinamico/`** (updaters/ValueTracker), **`estilo`**, **`patrones`**.
7. **3D** (`ThreeDScene`, `camara`, `mobjects/3d`) y `config_cli` al final.

---

## Notas relacionadas

- [[Reglas Manim]]
- [[Estandarizan Directorio Librerias]]
