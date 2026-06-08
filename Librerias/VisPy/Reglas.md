---
title: Reglas — VisPy
draft: true
tags:
  - vispy
  - reglas
---

# 📐 Reglas de redaccion — VisPy

Convenciones especificas para documentar **VisPy** (visualizacion cientifica GPU) en el vault.
Especializan el [[Estandarizan Directorio Librerias | estandar base de librerias]]; ante
conflicto, manda el estandar base. El **donde** vive cada nota lo define [[Tree VisPy]].

---

## 1. Naming de archivos (API-style)

| Tipo de nota | Patron | Ejemplo |
|--------------|--------|---------|
| Clase principal | `<NombreReal>.md` | `Canvas.md`, `SceneCanvas.md`, `Program.md` |
| Visual de scene | `<NombreReal>.md` | `Line.md`, `Markers.md`, `Volume.md` |
| Camara | `<NombreReal>.md` | `TurntableCamera.md`, `PanZoomCamera.md` |
| Funcion / config top-level | `vispy.<funcion>.md` | `vispy.use.md`, `vispy.get_colormap.md` |
| Concepto transversal | `concepto_<tema>.md` | `concepto_scene_graph.md` |
| Indice de carpeta | `index.md` | uno por **cada** directorio |

- **Sin tildes** en nombres de archivo **y tambien en titulo y cuerpo** (solo se conserva la n~),
  igual que SciPy/NumPy/SymPy. El nombre evita ademas espacios y signos.
- El nombre del archivo = exactamente lo que se wikilinkea (`[[Canvas]]`, `[[Line]]`).
- Clases con su **nombre real** de la API, respetando mayusculas (`SceneCanvas`, `ViewBox`).

---

## 2. Indice por carpeta (`index.md`) — OBLIGATORIO

> [!regla]
> **Cada directorio lleva su `index.md`** como **nota madre de pleno derecho**, no un listado.
> Debe **aportar informacion nueva**: que es el directorio, el modelo mental y como se
> relacionan sus hijos (cuando usar cada uno).

Estructura del `index.md`:

1. `# titulo` y parrafo que explica **que es** este submodulo/tematica y su papel en VisPy.
2. Un **ejemplo de codigo unificador** o la idea clave que hilvana las notas de la carpeta.
3. `## Como se relacionan`: tabla de decision *cuando usar cada hijo* y como se conectan.
4. `## Notas`: lista de hijos anotando su relacion (subcarpetas con ruta completa,
   hojas por basename). Sin marca *(pendiente)* una vez escritas.
5. `## Notas relacionadas` (padre, Tree, conceptos afines).

Frontmatter de un `index.md`:

```yaml
---
title: vispy.scene/visuals/2d — visuals 2D de alto nivel
tags:
  - vispy
  - indice
draft: false
---
```

> `index.md` no lleva `lib/tipo/retorna`; es un hub de navegacion, no una nota de API.

---

## 3. Frontmatter de una nota de API

```yaml
---
title: Line — visual de lineas y curvas 2D/3D
aliases:
  - Line
  - lineas vispy
tags:
  - vispy
  - api/clase          # api/clase | api/funcion | api/metodo | api/concepto
  - scene/visuals      # dominio funcional = rama del Tree
lib: vispy
mod: vispy.scene.visuals   # modulo exacto
tipo: clase
retorna: Line              # tipo de retorno (para funciones/metodos)
requiere:
  - SceneCanvas
  - ViewBox
draft: false
---
```

- `tipo`: `clase | funcion | metodo | concepto`.
- `retorna`: el tipo de objeto que devuelve (para funciones/metodos); omitir en clases y conceptos.
- Maximo **3–5 tags**; nunca `python`, `grafico` ni el path repetido.
- Para conceptos: `tipo: concepto`, sin `retorna`/`requiere` (a menos que haya dependencias claras).

---

## 4. Estructura de una nota de API (orden de capas)

Lo mas consultado arriba:

1. `# titulo` y parrafo de **que es y cuando usarlo** (una o dos oraciones potentes).
2. `## Importacion` — el import correcto:
   ```python
   from vispy.scene.visuals import Line
   # o
   from vispy import scene
   line = scene.visuals.Line(...)
   ```
3. `## Constructor / Firma` — parametros mas importantes con tipos y valores por defecto.
4. `## Parametros clave` — tabla o subsecciones con los parametros mas usados; ejemplos en codigo.
5. `## Casos de uso` — ejemplos reales y progresivos (2D, 3D, animacion, numpy array…).
6. `## Metodos y atributos` (para clases) — tabla con los mas relevantes.
7. `## Errores comunes` — tabla error → causa → solucion.
8. `## Notas relacionadas` — wikilinks.

> [!ejemplo]
> Todo codigo debe ser **ejecutable** y mostrar el efecto esperado en comentario:
> ```python
> import vispy.app as app
> from vispy.scene.visuals import Line
> import numpy as np
>
> canvas = app.Canvas(keys='interactive')
> # ... setup ...
> canvas.show()
> app.run()   # bloquea hasta cerrar la ventana
> ```

---

## 5. Convencion VisPy — patrones criticos a documentar

> [!info] Seleccion de backend
> Siempre que un ejemplo use una ventana nativa, incluir al inicio:
> ```python
> import vispy
> vispy.use('pyqt5')   # o 'pyglet', 'glfw', 'jupyter_rfb'
> ```
> Sin esto el ejemplo falla si el backend por defecto no esta instalado.

- **Ciclo de vida minimo** de `SceneCanvas` (el patron mas comun):
  ```python
  canvas = scene.SceneCanvas(keys='interactive', show=True)
  view = canvas.central_widget.add_view()
  view.camera = 'turntable'
  # agregar visuals:
  line = scene.visuals.Line(pos, parent=view.scene)
  app.run()
  ```
- **Agregar visuals**: siempre con `parent=view.scene` (o `parent=canvas.scene` para overlays).
  No usar `.add()` directo (eso es para nodos de transformacion, no para visuals).
- **Actualizar datos en animacion**: actualizar `visual.set_data(...)` dentro del callback de
  `Timer` (no reasignar el visual completo). Llamar `canvas.update()` para forzar redibujado.
- **gloo vs scene**: documentar siempre para cual API aplica la nota. Nunca mezclarlos en
  un mismo ejemplo sin explicar por que.
- **Numpy arrays**: los datos de visuals son siempre arrays NumPy (`float32` o `uint8`).
  Indicar el dtype esperado en la firma y en los ejemplos.

---

## 6. Wikilinks (resumen del estandar base)

- 1–2 apariciones por nota, en la **primera mencion significativa**; en parrafos, no en tablas.
- ❌ Nunca en headers, codigo, frontmatter ni titulos.
- A nota hoja: por basename `[[Line]]`, `[[SceneCanvas]]`.
- A `index` de carpeta: con ruta `[[vispy.scene/cameras/index | cameras]]`
  (el basename `index` colisiona — nunca `[[index]]` solo).
- A la raiz: `[[VisPy/index | VisPy]]` (si existe el index raiz).
- En tablas: escapa el pipe `\|`.
- Seccion final **obligatoria** `## Notas relacionadas`.

---

## 7. Flujo de trabajo

1. Disenar/actualizar [[Tree VisPy]] (roadmap).
2. `conceptos_transversales/` + `index.md` (raiz) a mano (modelo mental del event loop y scene graph).
3. Rellenar submodulos con subagentes (`nota-libreria`) + revision.
4. Mantener cada `index.md` al dia con su contenido (nota madre rica, draft: false).
5. `python3 .claude/skills/tree-libreria/sync_tree.py Librerias/VisPy` → marcar ✅ en el Tree.

---

## Notas relacionadas

- [[Tree VisPy]]
- [[Estandarizan Directorio Librerias]]
