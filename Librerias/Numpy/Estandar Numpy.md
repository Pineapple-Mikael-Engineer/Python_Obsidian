---
title: Estandar Numpy
draft: true
---

# Estándar de Notas — NumPy

## 🎯 Objetivo

Definir un estándar específico para documentar **NumPy** dentro del vault, manteniendo:

- Consistencia con otras librerías (ej. Matplotlib)
    
- Claridad conceptual (modelo mental fuerte)
    
- Navegabilidad y escalabilidad
    
- Enfoque en **operaciones matemáticas y transformación de datos**
    

---

## 🧠 Filosofía base (MUY IMPORTANTE)

> NumPy no es una librería de objetos, es una librería de **transformaciones sobre datos**

### 🔑 Principio clave

- **Conceptos → gobiernan**
    
- **Funciones → implementan**
    
- **ndarray → estructura base**
    

---

## 📁 Tipos de notas

|Tipo|Ubicación|Ejemplo|
|---|---|---|
|Concepto|`conceptos_transversales/`|`broadcasting.md`|
|Función|`np/<tematica>/`|`np/creacion/np.array.md`|
|Método|`np.ndarray/metodos/`|`ndarray.reshape.md`|
|Atributo|`np.ndarray/atributos/`|`ndarray.shape.md`|
|Submódulo|`np.<submodulo>/`|`np.linalg/`|

---

## ⚠️ Regla crítica

> En NumPy, los **conceptos no son secundarios**  
> Son parte central del sistema

Ejemplos clave:

- broadcasting
    
- vectorización
    
- shape
    
- dtype
    
- views vs copies
    

---

## 🧩 Naming técnico (archivos)

Formato:

```text
np.funcion.md
ndarray.metodo.md
ndarray.atributo.md
```

Ejemplos:

```text
np.mean.md
np.reshape.md
ndarray.flatten.md
ndarray.shape.md
```

---
## Título (interfaz humana)

Formato:

```yaml
title: nombre_nota — descripción breve
```

Ejemplo:

```yaml
title: np.reshape — Cambiar forma del array
```

---

## 🏷️ Sistema de Tags

### 📌 Regla general

- Máximo **3–5 tags**
    
- No redundar con el path
    

---

### 🔧 Estructura

```yaml
tags:
  - numpy
  - api/<tipo>
  - <dominio_funcional>
```

---

### Tipos de API

```yaml
- api/funcion
- api/metodo
- api/atributo
- api/clase
- api/submodulo
```

---

### Dominios funcionales (adaptados a NumPy)

```yaml
- algebra/vectorial
- algebra/matricial
- transformaciones
- estadistica
- indexado
- shape
- dtype
- creacion
- manipulacion
```

---

### 🚫 No usar

```yaml
- python
- datos
- retorna_valor
```

---

## 🧠 Frontmatter (estructura estándar)

```yaml
---
title: np.reshape — Cambiar forma del array

aliases:
  - reshape

tags:
  - numpy
  - api/funcion
  - shape

# --- Clasificación ---
lib: numpy
tipo: funcion

# --- Firma ---
parametros:
  - a
  - newshape

# --- Semántica ---
shape_input: any
shape_output: definida por usuario

dtype_input: any
dtype_output: igual al input

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Conceptos relacionados ---
requiere:
  - broadcasting
  - shape

draft: false
---
```

---

## 🔧 Definición de campos

---

### `lib`

```yaml
lib: numpy
```

Siempre obligatorio.

---

### `tipo`

```yaml
tipo: funcion | metodo | atributo | clase | submodulo
```

---

### `parametros`

Lista simple de argumentos:

```yaml
parametros:
  - a
  - axis
```

No documentar tipos aquí (eso va en el cuerpo).

---

### `shape_input`

Describe forma esperada:

```yaml
shape_input: (n,), (n,m), any
```

---

### `shape_output`

Describe resultado:

```yaml
shape_output: escalar
shape_output: (n,)
shape_output: depende de axis
```

---

### `dtype_input`

Tipos aceptados:

```yaml
dtype_input: int, float, bool
```

---

### `dtype_output`

Resultado:

```yaml
dtype_output: float
dtype_output: igual al input
```

---

### `retorna`

Tipo de retorno:

```yaml
retorna: ndarray
retorna: float
retorna: tuple
```

---

### `inplace`

Indica si modifica el array original:

```yaml
inplace: true | false
```

📌 Reemplaza completamente a `muta_estado`

---

### `requiere`

Conceptos necesarios:

```yaml
requiere:
  - broadcasting
  - indexing
```

---

## 🔗 Uso de Wikilinks

### Reglas

- Máximo **1–2 por nota**
    
- Solo primera mención relevante
    
- No en:
    
    - headers
        
    - código
        
    - frontmatter
        

---

### Ejemplo

```markdown
La operación utiliza [[broadcasting]] para alinear dimensiones.
```

---

## 🧠 Conceptos transversales (núcleo)

Esta carpeta define el modelo mental de NumPy.

Ejemplos obligatorios:

```text
conceptos_transversales/
├── broadcasting.md
├── vectorizacion.md
├── shape.md
├── dtype.md
├── views_vs_copies.md
├── indexing.md
```

---

## 🧠 Filosofía final

- NumPy = sistema matemático
    
- ndarray = estructura base
    
- funciones = transformaciones
    
- conceptos = reglas del sistema
    

