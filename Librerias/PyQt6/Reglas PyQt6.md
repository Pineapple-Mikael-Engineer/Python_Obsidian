---
title: Reglas — PyQt6
tags:
  - pyqt6
  - reglas
draft: true
---

# 📐 Reglas de redaccion — PyQt6

Convenciones especificas para documentar **PyQt6** (GUI de escritorio orientada a objetos).
Especializan el [[Estandarizan Directorio Librerias | estandar base de librerias]]; ante
conflicto, manda el estandar base. El **donde** vive cada nota lo define [[Tree PyQt6]].

> [!important] El idioma: SIN TILDES en el cuerpo, pero la ñ SE CONSERVA
> Como NumPy/SciPy/SymPy/VisPy: nada de a/e/i/o/u acentuadas ni en titulo ni en cuerpo.
> **Pero la ñ se mantiene siempre**: `tamaño`, `añadir`, `diseño`, `pequeño`, `señal`,
> `señales` — NO `tamano`/`anadir`/`senal`. Aplica tambien a comentarios de codigo, cadenas
> visibles en la GUI y etiquetas de Mermaid.
> **Excepcion (identificadores, van ASCII):** la clave de frontmatter `senales:`, la carpeta
> `QtCore/senales/`, el archivo `senal_personalizada.md` y cualquier variable de codigo
> (`senal.emit()`) se escriben sin ñ porque son nombres/rutas, no prosa. El resto del codigo
> va tal cual.

---

## 1. Naming de archivos (API-style)

| Tipo de nota | Patron | Ejemplo |
|--------------|--------|---------|
| Clase (base o concreta) | `<NombreReal>.md` | `QPushButton.md`, `QWidget.md`, `QObject.md` |
| Señal / metodo especial de señales | `<nombre>.md` | `pyqtSignal.md`, `connect.md`, `pyqtSlot.md` |
| Concepto transversal | `concepto_<tema>.md` | `concepto_signals_slots.md` |
| Patron POO (receta) | `<tema>.md` | `widget_personalizado.md` |
| Indice de carpeta | `index.md` | uno por **cada** directorio |

- Clases con su **nombre real** de la API, respetando mayusculas (`QMainWindow`, `QVBoxLayout`).
- El nombre del archivo = exactamente lo que se wikilinkea (`[[QPushButton]]`).

---

## 2. Frontmatter de una nota de CLASE

La herencia y las señales son **datos de primera clase**: van en el frontmatter, no solo en prosa.

```yaml
---
title: QPushButton — boton que emite clicked al pulsarse
aliases:
  - QPushButton
  - boton
tags:
  - pyqt6
  - api/clase
  - widgets          # dominio = rama del Tree (core | gui | widgets | ...)
lib: pyqt6
mod: QtWidgets        # modulo Qt exacto: QtCore | QtGui | QtWidgets
tipo: clase
hereda_de: QAbstractButton          # la clase PADRE directa (cadena de herencia)
senales:                            # señales que emite la clase
  - clicked
  - pressed
  - released
  - toggled
requiere:
  - QWidget
  - concepto_signals_slots
draft: false
---
```

- **`hereda_de`**: la clase padre **directa** (ej. `QPushButton` -> `QAbstractButton`). La cadena
  completa hasta `QObject` se muestra en el `classDiagram` del cuerpo, no se repite aqui.
- **`señales`**: lista de señales que la clase **emite** (las que se conectan con `.connect`).
  Omitir si la clase no emite ninguna (p. ej. layouts).
- **`tipo`**: `clase | concepto | patron`. Para conceptos/patrones, sin `hereda_de`/`señales`.
- Maximo **3–5 tags**; nunca `python`, `gui`, ni el path repetido.

---

## 3. Indice por carpeta (`index.md`) — OBLIGATORIO y con `classDiagram`

> [!regla]
> Cada directorio lleva su `index.md` como **nota madre de pleno derecho** (no un listado).
> Debe incluir un **`classDiagram` de Mermaid** con la rama de herencia de esa carpeta.

Estructura del `index.md`:

1. `# titulo` + parrafo: que agrupa esta carpeta y su papel.
2. `## En accion` — ejemplo de codigo ejecutable usando varias clases del grupo.
3. `## Herencia` — un bloque `classDiagram` decorado (paleta Nord, ver §6) con la jerarquia.
4. `## Clases que aporta` — tabla `| Clase | Hereda de | Señales | Rol |`.
5. `## Como elegir` — tabla de decision cuando aplique.
6. `## Notas relacionadas`.

Frontmatter del `index.md`:

```yaml
---
title: QtWidgets/botones — botones y casillas
tags: [pyqt6, indice]
draft: false
---
```

---

## 4. Estructura de una nota de CLASE (orden de capas)

1. `# titulo` + parrafo de **que es y cuando usarla**.
2. `## Importacion` — `from PyQt6.QtWidgets import QPushButton`.
3. `## Herencia` — `classDiagram` de la cadena + una linea de "lo que no define lo hereda"
   (de donde vienen sus metodos/señales). La idea central de Qt.
4. `## Señales` — tabla `| Señal | Cuando se emite | Argumentos |`. Omitir si no emite ninguna.
5. `## Propiedades` — los **atributos importantes**. En Qt son propiedades (getter/setter, no
   atributo directo): tabla `| Propiedad | Tipo | Leer \| escribir | Controla |`. Incluir las
   heredadas mas usadas. Omitir solo si la clase no tiene propiedades relevantes.
6. `## Constructor y metodos` — **con firmas completas**:
   - el/los **constructores** (todas las sobrecargas utiles) en un bloque ```python, con
     **tipos de argumentos y valores por defecto**.
   - tabla `| Firma | Devuelve | Que hace |` de los metodos relevantes, anotando el **tipo de
     cada argumento y el return** (ej. `setText(text: str)` -> `None`; `text()` -> `str`).
     Documentar firmas y returns "cuando haga falta": no inflar getters triviales, si.
7. `## Casos de uso` — ejemplos ejecutables y progresivos.
8. `## Personalizar (subclasear)` — si aplica: que metodos sobreescribir.
9. `## Errores comunes` — tabla error -> causa -> solucion.
10. `## Notas relacionadas`.

> La profundidad se adapta a la clase: una clase central (`QWidget`, `QMainWindow`) llevara
> tablas extensas de propiedades/metodos; una trivial, solo lo esencial. Pero **firmas con
> tipos/return y la seccion de Propiedades son el liston** para toda nota de clase.

> [!ejemplo]
> Todo codigo debe ser ejecutable. Patron minimo de una app:
> ```python
> from PyQt6.QtWidgets import QApplication, QWidget
> import sys
>
> app = QApplication(sys.argv)
> w = QWidget()
> w.show()
> sys.exit(app.exec())   # PyQt6: exec() (sin guion bajo), event loop
> ```

---

## 5. Convencion PyQt6 — patrones criticos a documentar

- **Señales y slots**: documentar siempre las señales que emite una clase (frontmatter +
  tabla). Conectar con `senal.connect(slot)`; emitir con `senal.emit(args)`; declarar propias
  con `pyqtSignal`. Es el mecanismo central de comunicacion.
- **Herencia para personalizar**: cuando una clase se suele subclasear (QWidget, QDialog,
  QAbstractTableModel, QThread), incluir la seccion `## Personalizar` con los metodos a
  sobreescribir (`paintEvent`, `sizeHint`, `mousePressEvent`, `run`, `data`/`rowCount`...).
- **`QObject` y el arbol de objetos**: el `parent` gestiona la memoria (al destruir el padre
  se destruyen los hijos). Mencionarlo donde el parent importe.
- **PyQt6 vs PyQt5/PySide**: en Qt6, `exec()` (no `exec_()`); enums con scope
  (`Qt.AlignmentFlag.AlignCenter`, no `Qt.AlignCenter`); `QAction`/`QShortcut` viven en
  `QtGui`. Avisar de estos cambios donde apliquen.
- **Codigo completo y minimo**: cada ejemplo de ventana debe poder ejecutarse
  (`QApplication`, `show()`, `app.exec()`).

---

## 6. Mermaid (herencia) — decorado Nord

Los diagramas de herencia usan `classDiagram`. Para flujos (event loop, ciclo de señal) o
arboles de decision, usar `flowchart` con esta paleta:

```
    classDef base fill:#5e81ac,stroke:#88c0d0,stroke-width:2px,color:#eceff4;
    classDef grupo fill:#3b4252,stroke:#81a1c1,stroke-width:1.5px,color:#88c0d0;
    classDef hoja fill:#2e3440,stroke:#a3be8c,color:#d8dee9;
```

- Labels de nodo SIEMPRE entre comillas dobles.
- En `classDiagram`, miembros solo como `+metodo()` / `+atributo` (sin corchetes ni `=`).

---

## 7. Wikilinks (resumen del estandar base)

- 1–2 apariciones por nota, en la primera mencion significativa; en parrafos, no en tablas.
- ❌ Nunca en headers, codigo, frontmatter ni titulos.
- A clase: por basename `[[QPushButton]]`, `[[QWidget]]`.
- A `index` de carpeta: con ruta `[[PyQt6/QtWidgets/botones/index | botones]]`.
- En tablas: escapa el pipe `\|`.
- Seccion final **obligatoria** `## Notas relacionadas`.

---

## 8. Flujo de trabajo

1. Diseñar/actualizar [[Tree PyQt6]] (roadmap).
2. `conceptos_transversales/` + `index.md` raiz a mano (modelo mental + classDiagram global).
3. Rellenar modulos con subagentes + revision; cada `index.md` con su `classDiagram`.
4. Mantener `hereda_de`/`señales` correctos (es lo que hace la libreria consultable).

---

## Notas relacionadas

- [[Tree PyQt6]]
- [[Estandarizan Directorio Librerias]]
