---
title: Reglas — CoolProp
tags:
  - coolprop
  - reglas
draft: true
---

# 📐 Reglas de redacción — CoolProp

Convenciones para documentar **CoolProp** (propiedades termodinámicas y de transporte de fluidos). Especializan el [[Estandarizan Directorio Librerias|estándar base de librerías]]; ante conflicto, manda el estándar base. El **dónde** vive cada nota lo define [[Tree CoolProp]].

> [!important] El idioma: español normal, CON tildes y ñ en el cuerpo
> El contenido usa ortografía española correcta: tildes (presión, entalpía, densidad, cálculo) y ñ (diseño, tamaño). Los símbolos especiales SOLO están prohibidos al **nombrar el archivo** (los nombres van en ASCII: `CoolProp.PropsSI.md`, `concepto_estado_termodinamico.md`), nunca dentro de la nota. El código y los identificadores de la API van tal cual.

> [!important] Formato: un párrafo = una línea (no cortar líneas a mano)
> NO partas los párrafos en varias líneas a ~100 columnas. Cada párrafo (y cada celda de tabla, ítem de lista o línea de callout) va en **una sola línea**; el editor hace el ajuste visual. Cortar a mano **rompe los wikilinks** que caen sobre el salto y deja el texto disparejo.

---

## 1. La idea que gobierna CoolProp

Toda nota debe respetar el modelo mental termodinámico:

- **El estado de un fluido puro queda definido por DOS propiedades independientes** (P y T, P y Q, T y Q...). Fijadas esas dos, todas las demás propiedades quedan determinadas. Ver [[concepto_estado_termodinamico]].
- **Dos interfaces para lo mismo**: la función de alto nivel [[CoolProp.PropsSI|PropsSI]] (una propiedad por llamada, cómoda) y el objeto de bajo nivel [[AbstractState]] (fija el estado una vez y consulta muchas, eficiente en bucles y mezclas). Toda nota debe situar de qué interfaz habla.
- **El cálculo lo hace un backend intercambiable** (`HEOS` por defecto, `IF97`, `REFPROP`, `SRK`...), seleccionable con la sintaxis `BACKEND::Fluido`. Ver [[concepto_backend]].
- **Unidades SI estrictas, siempre**: Pa, K, J/kg, kg/m³, J/(kg·K)... Nunca bar, °C ni kJ sin convertir. Ver [[concepto_propiedades_SI]].

---

## 2. Naming de archivos (API-style)

Recuerda: el **nombre del archivo va en ASCII** (sin tildes ni ñ); el contenido, en español normal.

| Tipo de nota | Patrón | Ejemplo |
|--------------|--------|---------|
| Función de módulo | `CoolProp.<funcion>.md` | `CoolProp.PropsSI.md`, `CoolProp.HAPropsSI.md` |
| Clase / objeto | `<Clase>.md` | `AbstractState.md` |
| Método de objeto | `<Clase>.<metodo>.md` | `AbstractState.update.md` |
| Concepto transversal | `concepto_<tema>.md` | `concepto_backend.md` |
| Backend | `backend.<NOMBRE>.md` | `backend.HEOS.md` |
| Constantes / config | `<Modulo>.md` | `Constants.md` |
| Índice de carpeta | `index.md` | uno por **cada** directorio |

- El nombre del archivo = exactamente lo que se wikilinkea (`[[CoolProp.PropsSI]]`, `[[AbstractState.update]]`).
- Los conceptos en minúscula con prefijo `concepto_` (coherente con el resto del vault).

---

## 3. Frontmatter

Bloque base; los campos de comportamiento dependen del tipo.

```yaml
---
title: CoolProp.PropsSI — propiedades termodinamicas de fluidos
aliases:
  - PropsSI
tags:
  - coolprop          # libreria (obligatorio)
  - api/funcion       # api/<tipo>: funcion | metodo | clase | config
  - propiedades       # dominio funcional
lib: coolprop
mod: CoolProp         # modulo (funciones) — u obj: AbstractState (metodos)
tipo: funcion         # funcion | metodo | clase | config | constantes | concepto
retorna: float        # tipo de retorno (omitir en conceptos)
muta_estado: false    # true en metodos como update/set_* ; omitir en conceptos
draft: false
---
```

- **`tipo`**: `funcion` | `metodo` | `clase` | `config` | `constantes` | `concepto`.
- **`obj`** (métodos/atributos) o **`mod`** (funciones de módulo): la clase o el módulo contenedor.
- **`retorna`** y **`muta_estado`**: comportamiento; los métodos que fijan estado (`update`, `set_mass_fractions`, `specify_phase`) llevan `muta_estado: true`.
- Máximo **3–5 tags**; nunca `python`, `datos`, ni el path repetido.

---

## 4. Índice por carpeta (`index.md`) — OBLIGATORIO y enriquecido

> [!regla] El index es una nota completa, NO un listado
> Cada directorio lleva su `index.md` como **nota madre**: además de listar a sus hijas, **enseña el grupo** con un ejemplo ejecutable real, un árbol de decisión y los errores comunes. Donde aporte, incluye un diagrama **Mermaid** (un `flowchart` de decisión, p. ej. "¿PropsSI o AbstractState?", o "¿qué backend elijo?").

Estructura del `index.md`: título + párrafo · `## En accion` (un ejemplo ejecutable que combine varias piezas del grupo) · `## ...` (tabla de lo que aporta, con wikilinks) · `## Como elegir` (árbol/tabla de decisión, idealmente Mermaid) · `## Errores comunes` o `## Patrones` · `## Notas relacionadas`.

---

## 5. Estructura de una nota de FUNCIÓN o MÉTODO

Sigue el orden del estándar base (skill `nota-libreria`). Incluye solo las secciones que aporten, en este orden:

1. `# titulo` (igual al `title`).
2. `## Firma de la función` — bloque ```python con la firma completa y tipos.
3. `## Valor de retorno` — qué devuelve, con tabla `| Entrada | Retorno | Ejemplo |` cuando varía (escalar vs array, etc.).
4. `## Parámetros en detalle` — un `###` por parámetro relevante; tablas para tipos aceptados y bloques ```python cortos por kwarg.
5. `## Casos de uso` — ejemplos reales y progresivos (saturación, proceso isentrópico, curvas con arrays...).
6. `## Errores comunes` — tabla `| Error | Causa | Solución |`.
7. `## Limitaciones` — cuándo NO usarla / alternativas (p. ej. `AbstractState` frente a `PropsSI` en bucles).
8. `## Notas relacionadas` — wikilinks.

> Todo ejemplo de código es **ejecutable y mínimo**, con `from CoolProp.CoolProp import PropsSI` o `import CoolProp.CoolProp as CP`, y comenta el resultado esperado en línea (`# -> 996.56`). Mantén las **unidades SI** en todos los ejemplos.

---

## 5b. Estructura de una nota de CLASE / CONCEPTO

- **Clase/objeto** (`AbstractState`): descripción · firma del constructor · parámetros · flujo de trabajo típico · tabla de métodos clave (con wikilinks a sus notas) · ejemplos · errores comunes · notas relacionadas.
- **Concepto** (gobierna el modelo mental, no es secundario): `## Definicion` (qué es, en una/dos frases) · `## Por que existe` (motivación, contraste) · `## La regla central` (lo mínimo a memorizar) · ejemplos progresivos (`### Nivel 1`, `### Nivel 2`...) · `## Casos que fallan` · `## Relacion con otros conceptos` (wikilinks).

---

## 6. Convención CoolProp — detalles críticos a documentar

- **Unidades SI siempre**: presión en Pa (no bar), temperatura en K (no °C), energías en J/kg. Si un ejemplo parte de °C o bar, **convertir explícitamente** (`T = 25 + 273.15`).
- **Las claves de propiedad** (`'T'`, `'P'`, `'D'`, `'H'`, `'S'`, `'Q'`, `'C'`=Cp, `'O'`=Cv...) y los pares de entrada de `AbstractState` (`PT_INPUTS`, `PQ_INPUTS`...) viven en [[Constants]] y [[concepto_propiedades_SI]]; remitir ahí, no redefinirlos en cada nota.
- **Backend con `BACKEND::Fluido`**: `'HEOS::Water'`, `'IF97::Water'`, `'REFPROP::R134a'`. El backend por defecto es `HEOS`. Ver [[concepto_backend]].
- **Mezclas**: nombre con `&` (`'R32&R134a'`) y fracciones con `set_mass_fractions`/`set_mole_fractions` o el kwarg `fractions` de `PropsSI`.
- **PropsSI vs AbstractState**: en bucles o muchas consultas del mismo estado, `AbstractState` es mucho más rápido (fija el estado una vez). Recordarlo en las notas de `PropsSI`.

---

## 7. Mermaid — decorado

Para árboles de decisión (qué interfaz, qué backend, qué par de inputs) usar `flowchart` con esta paleta:

```
    classDef pregunta fill:#5e81ac,stroke:#88c0d0,stroke-width:2px,color:#eceff4;
    classDef grupo fill:#3b4252,stroke:#81a1c1,stroke-width:1.5px,color:#88c0d0;
    classDef hoja fill:#2e3440,stroke:#a3be8c,color:#d8dee9;
```

- Labels de nodo SIEMPRE entre comillas dobles.
- Si se documenta herencia (p. ej. backends como variantes), `classDiagram` con miembros solo `+metodo()` / `+atributo`.

---

## 8. Wikilinks (resumen del estándar base)

- 1–2 apariciones por nota, en la primera mención significativa; en párrafos, no en tablas.
- ❌ Nunca en headers, código, frontmatter ni títulos.
- ❌ Nunca partidos por un salto de línea: un wikilink va entero en su línea.
- A función/clase: por basename `[[CoolProp.PropsSI]]`, `[[AbstractState]]`.
- A `index` de carpeta: con ruta `[[CoolProp/backends/index | backends]]`.
- En tablas: escapa el pipe `\|`.
- Sección final **obligatoria** `## Notas relacionadas`.

---

## 9. Flujo de trabajo

1. Mantener [[Tree CoolProp]] sincronizado con el disco (marcar `✅` lo creado).
2. `conceptos_transversales/` primero (modelo mental: estado, backend, unidades).
3. Rellenar funciones de módulo y `backends/` con subagentes + revisión; cada `index.md` con su decisión Mermaid.
4. Verificar: 0 wikilinks rotos/partidos, unidades SI en los ejemplos, tildes presentes, fences pares.

---

## Notas relacionadas

- [[Tree CoolProp]]
- [[Estandarizan Directorio Librerias]]
