---
name: nota-libreria
description: Crea o estandariza una nota .md sobre un elemento de una librería (función, método, atributo, clase, objeto, config, submódulo o concepto) en el vault de Obsidian, siguiendo el estándar del usuario. Úsala cuando el usuario pida documentar/crear/normalizar una nota de una API o un concepto de cualquier librería o lenguaje (NumPy, Matplotlib, CoolProp, pandas, etc.).
---

# Nota de Librería

Genera una nota `.md` para el vault de Obsidian que documenta un elemento de una librería
siguiendo el estándar definido en `Librerias/Estandarizan Directorio Librerias.md` y los
estándares específicos por librería (p. ej. `Librerias/Numpy/Estandar Numpy.md`).

El objetivo es que la nota sea: **escalable, navegable (graph limpio), consistente entre
librerías y consultable por frontmatter**. La API es un grafo de conocimiento; cada nota es
un nodo semántico.

## Antes de escribir

1. **Identifica el tipo de nota** (define toda la estructura):
   - `funcion` — función de módulo: `np.mean`, `plt.subplots`, `CoolProp.PropsSI`
   - `metodo` — método de objeto/clase: `ax.plot`, `ndarray.reshape`, `AbstractState.update`
   - `atributo` — atributo de objeto: `ndarray.shape`, `ndarray.dtype`
   - `clase` / `objeto` — `Line2D`, `GridSpec`, `AbstractState`
   - `config` — configuración: `rcParams`, `plt.style.use`
   - `submodulo` — agrupador: `np.linalg`, `np.random`
   - `concepto` — modelo mental transversal: `broadcasting`, `views_vs_copias`, `estado_termodinamico`
2. **Si existe un estándar específico** de esa librería (`Librerias/<Lib>/Estandar *.md`), léelo
   y respétalo por encima de los defaults de esta skill (campos extra de frontmatter, dominios
   de tags, naming). Si no existe y el usuario va a crear muchas notas, ofrece generarlo.
3. **Ubica la carpeta destino** según el árbol de esa librería (ver skill `tree-libreria`).
   Carpeta = organización temática; no dupliques en tags lo que ya está en el path.

## Naming del archivo (API-style)

Imita la documentación oficial. Sin espacios.

```text
modulo.funcion.md        np.mean.md, plt.subplots.md, CoolProp.PropsSI.md
objeto.metodo.md         ax.plot.md, ndarray.reshape.md, AbstractState.update.md
objeto.atributo.md       ndarray.shape.md
Clase.md                 Line2D.md, GridSpec.md, AbstractState.md
concepto_<tema>.md       concepto_broadcasting.md   (o Concepto_<Tema>.md según la librería)
```

## Frontmatter

Bloque base obligatorio. El `title` es la interfaz humana: `nombre — descripción breve`.

```yaml
---
title: np.reshape — Cambiar forma del array
aliases:
  - reshape

tags:
  - numpy          # <libreria> (obligatorio, minúsculas)
  - api/funcion    # api/<tipo>
  - shape          # <dominio_funcional>

# --- Clasificación ---
lib: numpy
tipo: funcion              # funcion | metodo | atributo | clase | objeto | config | submodulo | concepto
# obj: Axes                # objeto contenedor si es método/atributo
# mod: CoolProp            # módulo si aplica

# --- Comportamiento ---
retorna: ndarray
inplace: false             # NumPy usa `inplace`; Matplotlib/objetos usan `muta_estado`

# --- Dependencias ---
requiere:
  - broadcasting
  - shape

draft: false
---
```

Reglas de frontmatter:
- **tags**: 3–5 como máximo. Estructura `<libreria>` + `api/<tipo>` + `<dominio_funcional>`.
  - Tipos de API: `api/funcion`, `api/metodo`, `api/atributo`, `api/clase`, `api/objeto`, `api/config`, `api/submodulo`. Conceptos usan el tag plano `concepto`.
  - **Nunca** uses como tag: `python`, `datos`, `grafico`, `retorna_valor`, `tiene_retorno`, ni nada ya presente en el path.
- **Comportamiento**: `retorna` (tipo de retorno), y `inplace`/`muta_estado: true|false`. Para `concepto` omite estos.
- **requiere**: conceptos o notas necesarias para entender ésta.
- `aliases`: nombre corto y formas en que lo buscarías.

## Cuerpo — nota de función / método

Orden de secciones (incluye solo las que aporten; respeta este orden):

1. `# titulo` (igual al `title`)
2. `## Firma de la función` — bloque ```python con la firma completa y tipos.
3. `## Valor de retorno` — tabla `| Entrada | Retorno | Ejemplo |` cubriendo los casos
   (escalar vs array, una vs varias líneas, etc.) + ejemplo de código si aclara.
4. `## Formas básicas de llamada` — tabla de variantes de llamada (cuando hay varias).
5. `## Parámetros en detalle` — un `###` por parámetro relevante; usa tablas para tipos
   aceptados y bloques ```python cortos para cada kwarg.
6. `## Casos de uso` — ejemplos reales y progresivos (saturación, proceso, curvas con arrays…).
7. `## Buenas prácticas` — lista numerada.
8. `## Errores comunes` — tabla `| Error | Causa | Solución |`.
9. `## Limitaciones` — cuándo NO usarla / alternativas (ej. `AbstractState` vs `PropsSI`).
10. `## Notas relacionadas` — wikilinks (ver abajo).

## Cuerpo — nota de concepto

Los conceptos **gobiernan**: son el modelo mental, no son secundarios.

1. `# titulo`
2. `## Definicion fundamental` — qué es, en una/dos frases potentes.
3. `## Por que existe` — motivación, con contraste "sin X (tedioso) vs con X (directo)".
4. `## La regla central` — la regla mínima a memorizar (tabla compatible/incompatible).
5. Algoritmo paso a paso y/o **ejemplos progresivos** (`### Nivel 1`, `### Nivel 2`, …).
6. `## Casos que fallan` — errores típicos con su solución.
7. `## Memoria y rendimiento` u otras secciones según el concepto.
8. `## Relacion con otros conceptos` — wikilinks.

## Cuerpo — nota de clase / atributo / config

- **Clase/objeto**: firma del constructor, atributos clave (tabla), métodos principales
  (tabla con wikilinks a sus notas), ejemplo de ciclo de vida, notas relacionadas.
- **Atributo**: qué representa, tipo, si es de solo lectura, ejemplo corto, relacionadas.
- **Config**: qué controla, valores válidos (tabla), ejemplos de uso, relacionadas.

## Reglas de estilo (transversales)

- **Tablas** para todo lo enumerable (tipos aceptados, códigos, errores, retornos). Densas y útiles.
- **Bloques de código** ejecutables y mínimos; comenta el resultado esperado en línea (`# → 996.56`).
- **Wikilinks `[[...]]`** = conexiones intencionales, no automáticas:
  - Máximo **1–2 apariciones por nota en el cuerpo**, en la primera mención significativa.
  - Permitidos en párrafos (preferido) y a veces en listas. Evítalos dentro de tablas.
  - **Prohibidos** en headers, bloques de código, frontmatter y título.
  - Usa alias cuando mejore la lectura: `[[Concepto_backend|backend]]`.
- Un `[[wikilink]]` a una nota que aún no existe es válido: marca trabajo futuro.

## Cierre obligatorio

Toda nota termina con:

```markdown
## Notas relacionadas

- [[nota_1]]
- [[nota_2]]
```

Deben ser las notas enlazadas en el cuerpo o las más relevantes conceptualmente. Si una nota
ya fue enlazada en el cuerpo, no la repitas innecesariamente más arriba.

## Flujo recomendado

1. Confirma con el usuario: librería, tipo de nota, nombre del elemento y carpeta destino.
2. Lee el estándar específico de la librería si existe.
3. Escribe el archivo con naming API-style en la carpeta correcta.
4. Reporta la ruta creada y los wikilinks pendientes (notas que aún no existen) por si quiere
   crearlas o actualizar el Tree con la skill `tree-libreria`.
