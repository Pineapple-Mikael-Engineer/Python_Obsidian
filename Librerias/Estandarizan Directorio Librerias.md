---
draft: true
---
# Estándar de Notas — Librerías (Base)

## 🎯 Objetivo

Definir un estándar reutilizable para documentar cualquier librería en Obsidian:

- Escalable (muchas notas sin degradación)
    
- Navegable (graph limpio)
    
- Consistente entre librerías
    
- Integrado con Git (branch por librería)
    

---

## 🧩 Principios del sistema

### 1. Separación de roles

- **Carpetas** → organización temática interna
    
- **Tags** → agrupación global (cross-library)
    
- **Frontmatter** → metadata estructurada
    

---

### 2. Naming técnico (archivos)

Formato base:

```text
objeto.metodo.md
modulo.funcion.md
Clase.md
```

Ejemplos:

```text
ax.contour.md
plt.subplots.md
lines.Line2D.md
```

✔️ Optimizado para:

- Búsqueda tipo API
    
- Consistencia con documentación oficial
    

---

### 3. Título (interfaz humana)

Formato:

```yaml
title: nombre_nota — descripción breve
```

Ejemplo:

```yaml
title: ax.contour — Curvas de nivel
```

---

## 🏷️ Sistema de Tags

### 📌 Regla general

> Máximo 3–5 tags por nota

---

### 🔧 Estructura estándar

```yaml
tags:
  - <libreria>
  - api/<tipo>
  - <dominio_funcional>
```

---

### 1. Librería (obligatorio)

```yaml
- matplotlib
- numpy
- pandas
```

---

### 2. Tipo de API

```yaml
- api/metodo
- api/funcion
- api/clase
- api/objeto
- api/config
```

---

### 3. Dominio funcional

```yaml
- plot/lineas
- plot/contornos
- plot/distribuciones
- layout
- styling
- datos
```

---

### 🚫 Exclusiones

No usar en tags:

```yaml
- tiene_retorno
- python
- grafico
```

---

## 🧠 Frontmatter (estructura estándar)

```yaml
---
title: ax.contour — Curvas de nivel

aliases:
  - contour
  - curvas nivel

tags:
  - matplotlib
  - api/metodo
  - plot/contornos

# --- Clasificación ---
lib: matplotlib
obj: Axes
tipo: metodo

# --- Comportamiento ---
retorna: QuadContourSet
muta_estado: true

# --- Dependencias ---
requiere:
  - numpy.meshgrid

draft: false
---
```

---

## 🔧 Definición de campos

### `lib`

```yaml
lib: matplotlib
```

---

### `obj`

```yaml
obj: Axes
```

---

### `tipo`

```yaml
tipo: metodo | funcion | clase | objeto | config
```

---

### `retorna`

```yaml
retorna: QuadContourSet
```

---

### `muta_estado`

```yaml
muta_estado: true
```

---

### `requiere`

```yaml
requiere:
  - numpy.meshgrid
```

---

## 📁 Estructura de carpetas

Principio:

> Organización temática, no duplicar información de tags

Ejemplo:

```text
Matplotlib/
├── Figura_Ejes/
├── Labels_Leyendas/
├── Tipos_Plot/
│   ├── Lineas/
│   ├── Contornos_Imagenes/
```

---

### ⚠️ Regla clave

> Si está en el path → no repetir en tags

---

## 🌿 Integración con Git

### Estrategia

- 1 branch por librería:
    

```bash
feat/Librerias/Matplotlib
feat/Librerias/CoolProp
```

- Base común:
    

```bash
feat/Librerias-base
```

---

### Flujo recomendado

```bash
git checkout feat/Librerias-base
# definir estándares

git checkout feat/Librerias/Matplotlib
# aplicar estándar
```

---

## 🔗 Uso de Wikilinks

### 📌 Principio general

> Los wikilinks se usan para **referenciar conceptos**, no para saturar la nota.

---

### 🔹 Regla de frecuencia

- Máximo **1–2 apariciones por nota**
    
- Solo en la **primera mención significativa**
    
- Segunda aparición solo si hay cambio de contexto relevante
    

---

### 🔹 Ubicación permitida

✔️ En párrafos (preferido)  
✔️ Ocasionalmente en listas

⚠️ En tablas → evitar (pueden romper formato)

---

### 🔹 Ubicación prohibida

❌ Headers (`#`, `##`, etc.)  
❌ Bloques de código  
❌ Frontmatter  
❌ Títulos

---

### 🔹 Estilo de uso

Ejemplo correcto:

```markdown
Las curvas pueden etiquetarse usando [[ax.clabel]]
```

Después de la primera mención:

```markdown
Las etiquetas permiten identificar niveles sin necesidad de repetir el enlace.
```

---

### 🔹 Sección final obligatoria

Todas las notas deben terminar con:

```markdown
## Notas relacionadas

- [[nota_1]]
- [[nota_2]]
```

📌 Estas notas deben ser:

- Las que aparecieron en el cuerpo
    
- O las más relevantes conceptualmente
    

---

### ⚠️ Regla clave

> Si ya enlazaste una nota, no la repitas innecesariamente en el cuerpo.

---

## 🧠 Filosofía

- API = grafo de conocimiento
    
- Notas = nodos semánticos
    
- Tags = clusters globales
    
- Frontmatter = estructura consultable
    
- Wikilinks = conexiones intencionales, no automáticas
    

---