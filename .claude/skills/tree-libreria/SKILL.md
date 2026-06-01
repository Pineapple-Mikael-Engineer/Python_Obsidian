---
name: tree-libreria
description: Crea, mejora o actualiza una nota "Tree <Librería>" del vault de Obsidian — el árbol de carpetas/notas de una librería. Soporta dos criterios de organización: SECUENCIAL (lineal/sucesivo, ruta de aprendizaje) o JERÁRQUICO (conceptual/clasificativo, por módulos+temáticas). Úsala cuando el usuario pida diseñar, reorganizar, ampliar o sincronizar el árbol de una librería con las notas existentes.
---

# Tree de Librería

Gestiona la nota `Tree <Librería>.md` que define la estructura de carpetas y notas de una
librería en el vault. Un Tree es el **mapa de navegación** y el **plan de notas** (existentes
y pendientes) de una librería.

Principio rector del vault: **carpetas = organización temática interna; tags = agrupación
global; frontmatter = metadata**. El Tree solo modela las carpetas/archivos, nunca duplica
información de tags.

## Los dos criterios de organización

Antes de crear o reordenar, decide (o pregunta al usuario) bajo qué criterio se organiza:

### A) JERÁRQUICO — conceptual / clasificativo (default para librerías)
Organiza por **estructura de la API**: módulos (`np`, `np.linalg`, `np.random`) cruzados con
**temáticas** (`creacion/`, `operaciones/`, `reducciones/`). El anidamiento es **variable
según la complejidad**: un submódulo pequeño es una carpeta plana; uno grande se subdivide por
temática. Es el criterio de `Tree Numpy.md` y `Tree CoolProp.md`.

Reglas de clasificación jerárquica:
- Agrupa por **rol y dominio funcional**, no alfabéticamente.
- Tipos de nota y su ubicación típica:
  | Tipo | Ubicación |
  |------|-----------|
  | Concepto transversal | `conceptos_transversales/` (raíz de la librería) |
  | Función de módulo | `<modulo>/<tematica>/` |
  | Método de objeto | `<Objeto>/metodos/<subtematica>/` |
  | Atributo | `<Objeto>/atributos/` |
  | Submódulo completo | `<modulo.submodulo>/<tematica>/` |
- Profundiza una temática solo cuando el nº de notas lo justifique (no crees carpetas de 1).

### B) SECUENCIAL — lineal / sucesivo de conocimientos (ruta de aprendizaje)
Organiza por **orden en que se aprende/usa**, de lo fundamental a lo avanzado. Prefijos
numéricos para fijar el orden. Útil para una introducción guiada o un "camino" dentro de una
librería o tema.

Reglas de clasificación secuencial:
- Cada bloque es un peldaño que **depende del anterior** (prerrequisitos antes que dependientes).
- Numera para imponer orden: `01_`, `02_`, … o `01_fundamentos/`, `02_creacion/`, …
- El orden refleja dependencias conceptuales: `ndarray` → `shape`/`dtype` → `broadcasting`
  → `vectorización` → operaciones → reducciones → submódulos.
- Marca prerrequisitos cruzados con una columna/nota, no rompas la linealidad del árbol.

Un mismo vault puede combinar ambos: estructura física jerárquica + una nota-índice secuencial
("ruta de aprendizaje") que enlaza las notas en orden didáctico. Si el usuario quiere una ruta
sin mover archivos, genera el orden como lista de wikilinks, no como carpetas renombradas.

## Formato de la nota Tree

```markdown
---
title: Tree <Librería>
draft: true
---

# Tree <Librería>

> (1 línea describiendo el criterio: jerárquico por módulos+temáticas, o secuencial por niveles)

​```tree
<Librería>/
│
├── 📁 <carpeta>/
│   ├── archivo.md
│   └── archivo.md
│
└── 📁 <submodulo>/
    └── archivo.md
​```
```

Convenciones del bloque de árbol:
- Lenguaje de fence: ```tree (o ```text). Conserva el que ya use la librería.
- Carpetas con `📁` y `/` final; archivos `.md` como hojas.
- Conectores `│ ├── └──` bien alineados. Líneas en blanco con `│` para separar grupos grandes.
- Naming de archivos = **API-style**, idéntico a la skill `nota-libreria`
  (`np.mean.md`, `ndarray.shape.md`, `ax.plot.md`, `Clase.md`, `concepto_<tema>.md`).

Secciones opcionales útiles (presentes en los trees del vault):
- Tabla **"Tipos de notas"** (Tipo | Ubicación | Ejemplo) al inicio.
- Tabla **"Notas existentes"** (Módulo | Archivos) + contador "N archivos".
- Bloque desplegable **"Notas pendientes por crear (esqueleto)"** con `<details>`.
- `## Notas relacionadas` al final si enlaza a estándar/introducción.

## Crear un Tree nuevo

1. Pregunta/decide el **criterio** (jerárquico vs secuencial) y la **librería**.
2. Esboza la taxonomía de la API: módulos, objetos, submódulos, conceptos transversales.
3. Agrupa las notas por dominio funcional (jerárquico) o por dependencia/nivel (secuencial),
   con anidamiento proporcional a la complejidad.
4. Escribe `Librerias/<Librería>/Tree <Librería>.md` con `draft: true`.
5. Incluye notas pendientes (esqueleto) para que el árbol sea también un plan de trabajo.

## Mejorar / actualizar un Tree existente

1. **Lee el Tree actual** y **escanea las notas reales** en disco de esa librería para
   detectar desincronización:
   - Archivos en disco que faltan en el árbol → añádelos en su rama correcta.
   - Entradas del árbol sin archivo → márcalas como pendientes (no inventes que existen).
2. Aplica el **criterio activo** de forma consistente; si reorganizas, no mezcles criterios
   dentro de la misma rama sin avisarlo.
3. Reequilibra el anidamiento: divide carpetas que crecieron mucho por temática; aplana
   carpetas de 1–2 notas que ya no justifican subnivel.
4. Verifica naming API-style y coherencia con `Estandarizan Directorio Librerias.md` y el
   estándar específico de la librería.
5. Actualiza tablas de "existentes/pendientes" y el contador si la nota las tiene.
6. Reporta: qué se añadió, qué se movió, qué quedó pendiente.

## Verificación contra el disco (siempre antes de editar)

Compara el árbol con la realidad del filesystem para no afirmar de más:

```bash
find "Librerias/<Librería>" -name '*.md' | sort
```

Cruza esa lista con el árbol y separa **existentes** de **pendientes**. Nunca marques como
existente algo que no está en disco; nunca borres del árbol algo pendiente solo porque no
existe aún (es trabajo planificado).

## Relación con `nota-libreria`

El Tree define **dónde** vive cada nota y su naming; `nota-libreria` define **qué** contiene.
Tras crear notas nuevas, vuelve aquí para sincronizar el Tree. Tras diseñar un Tree, usa
`nota-libreria` para rellenar las hojas pendientes.
