---
draft: true
---


# 1️⃣ Estándar Global Mermaid (NORD · DARK · QUARTZ-SAFE)

## 🎨 Colores (referencia mental)

|Rol|Color|
|---|---|
|Texto|`#eceff4` _(Quartz fuerza esto)_|
|Fondo base|`#2e3440`|
|Raíz / foco|`#3b4252`|
|Categoría|`#434c5e`|
|Subcategoría|`#4c566a`|
|Acento fuerte|`#88c0d0`|
|Acento medio|`#81a1c1`|
|Acento estructural|`#5e81ac`|
|Error / Fin|`#bf616a`|
|Éxito / Highlight|`#d08770`|

---

# 2️⃣ Plantilla BASE (SIEMPRE incluir)

👉 **Esta va al inicio de TODOS los diagramas**

```css
classDef raiz fill:#3b4252,stroke:#88c0d0,stroke-width:3px,color:#eceff4,font-weight:bold;
classDef categoria fill:#434c5e,stroke:#81a1c1,stroke-width:2px,color:#eceff4;
classDef subcategoria fill:#4c566a,stroke:#5e81ac,stroke-width:1.5px,color:#eceff4;
classDef proceso fill:#3b4252,stroke:#88c0d0,stroke-width:1.2px,color:#eceff4;
classDef especial fill:#bf616a,stroke:#d08770,stroke-width:2px,color:#eceff4,font-weight:bold;
classDef ejemplo fill:#2e3440,stroke:#81a1c1,stroke-width:1px,stroke-dasharray:3 3,color:#eceff4,font-size:11px;

%% Flechas seguras (OBSIDIAN-PROOF)
linkStyle default stroke:#81a1c1,stroke-width:1.6px
```

---

# 3️⃣ Flowchart – **Flujos Lógicos** (decisiones, validaciones)

👉 Para **algoritmos, procesos, validaciones, pasos**

```mermaid
flowchart TD
	classDef raiz fill:#3b4252,stroke:#88c0d0,stroke-width:3px,color:#eceff4,font-weight:bold;
	classDef categoria fill:#434c5e,stroke:#81a1c1,stroke-width:2px,color:#eceff4;
	classDef subcategoria fill:#4c566a,stroke:#5e81ac,stroke-width:1.5px,color:#eceff4;
	classDef proceso fill:#3b4252,stroke:#88c0d0,stroke-width:1.2px,color:#eceff4;
	classDef especial fill:#bf616a,stroke:#d08770,stroke-width:2px,color:#eceff4,font-weight:bold;
	classDef ejemplo fill:#2e3440,stroke:#81a1c1,stroke-width:1px,stroke-dasharray:3 3,color:#eceff4,font-size:11px;
	
	%% Flechas seguras (OBSIDIAN-PROOF)
	linkStyle default stroke:#81a1c1,stroke-width:1.6px
	
    Start((Inicio)):::raiz
    Start --> Check{¿Condición?}:::categoria

    Check -- Sí --> Process[Procesar]:::proceso
    Check -- No --> Error((Error)):::especial

    Process --> End((Fin)):::raiz
    Error --> End

    %% Flechas semánticas
    linkStyle 1 stroke:#88c0d0,stroke-width:2px
    linkStyle 2 stroke:#bf616a,stroke-width:1.6px,stroke-dasharray:3 3
```

📌 **Regla mental**

- Rombo = decisión
    
- Círculo = inicio/fin
    
- Rectángulo = acción
    

---

# 4️⃣ Flowchart – **Conceptual / Clasificación**

👉 Para **temas, conceptos, taxonomías, teoría**

```mermaid
flowchart TD
	classDef raiz fill:#3b4252,stroke:#88c0d0,stroke-width:3px,color:#eceff4,font-weight:bold;
	classDef categoria fill:#434c5e,stroke:#81a1c1,stroke-width:2px,color:#eceff4;
	classDef subcategoria fill:#4c566a,stroke:#5e81ac,stroke-width:1.5px,color:#eceff4;
	classDef proceso fill:#3b4252,stroke:#88c0d0,stroke-width:1.2px,color:#eceff4;
	classDef especial fill:#bf616a,stroke:#d08770,stroke-width:2px,color:#eceff4,font-weight:bold;
	classDef ejemplo fill:#2e3440,stroke:#81a1c1,stroke-width:1px,stroke-dasharray:3 3,color:#eceff4,font-size:11px;
	
	%% Flechas seguras (OBSIDIAN-PROOF)
	linkStyle default stroke:#81a1c1,stroke-width:1.6px

    Root((Tema Principal)):::raiz

    Root --> A{Categoría A}:::categoria
    Root --> B{Categoría B}:::categoria

    A --> A1[Subtema A1]:::subcategoria
    A --> A2[Subtema A2]:::subcategoria

    B --> B1[Subtema B1]:::subcategoria
    B --> B2[Subtema B2]:::subcategoria

    A1 --> Ex1["Ejemplo"]:::ejemplo
    B2 --> Ex2["Caso típico"]:::ejemplo
```

📌 **No hay flujo temporal**  
👉 Solo **estructura mental**

---

# 5️⃣ Flowchart – **Jerárquico**

👉 Para **OOP, niveles, capas, herencia, sistemas teóricos**

```mermaid
flowchart TD
	classDef raiz fill:#3b4252,stroke:#88c0d0,stroke-width:3px,color:#eceff4,font-weight:bold;
	classDef categoria fill:#434c5e,stroke:#81a1c1,stroke-width:2px,color:#eceff4;
	classDef subcategoria fill:#4c566a,stroke:#5e81ac,stroke-width:1.5px,color:#eceff4;
	classDef proceso fill:#3b4252,stroke:#88c0d0,stroke-width:1.2px,color:#eceff4;
	classDef especial fill:#bf616a,stroke:#d08770,stroke-width:2px,color:#eceff4,font-weight:bold;
	classDef ejemplo fill:#2e3440,stroke:#81a1c1,stroke-width:1px,stroke-dasharray:3 3,color:#eceff4,font-size:11px;
	
	%% Flechas seguras (OBSIDIAN-PROOF)
	linkStyle default stroke:#81a1c1,stroke-width:1.6px

    Root((Sistema)):::raiz

    Root --> L1A[Nivel 1A]:::categoria
    Root --> L1B[Nivel 1B]:::categoria

    L1A --> L2A[Nivel 2]:::subcategoria
    L1A --> L2B[Nivel 2]:::subcategoria

    L2A --> D1[Detalle]:::proceso
```

📌 **Regla**

- De arriba → abajo = abstracción → concreción
    

---

# 6️⃣ Flowchart – **Arquitectura / Sistemas**

👉 Para **software, módulos, pipelines, data flow**

```mermaid
flowchart LR
	classDef raiz fill:#3b4252,stroke:#88c0d0,stroke-width:3px,color:#eceff4,font-weight:bold;
	classDef categoria fill:#434c5e,stroke:#81a1c1,stroke-width:2px,color:#eceff4;
	classDef subcategoria fill:#4c566a,stroke:#5e81ac,stroke-width:1.5px,color:#eceff4;
	classDef proceso fill:#3b4252,stroke:#88c0d0,stroke-width:1.2px,color:#eceff4;
	classDef especial fill:#bf616a,stroke:#d08770,stroke-width:2px,color:#eceff4,font-weight:bold;
	classDef ejemplo fill:#2e3440,stroke:#81a1c1,stroke-width:1px,stroke-dasharray:3 3,color:#eceff4,font-size:11px;
	
	%% Flechas seguras (OBSIDIAN-PROOF)
	linkStyle default stroke:#81a1c1,stroke-width:1.6px

    Input((Entrada)):::especial
    Core[Sistema Central]:::raiz
    Output((Salida)):::proceso

    Input --> Core
    Core --> M1[Módulo A]:::categoria
    Core --> M2[Módulo B]:::categoria

    M1 --> F1[Función]:::subcategoria
    M2 --> F2[Función]:::subcategoria

    F1 --> Output
    F2 --> Output

    %% Flujo principal
    linkStyle 0 stroke:#d08770,stroke-width:2px
```

---

# 7️⃣ Subgraphs (uso correcto)

👉 **Solo para contexto**, nunca para jerarquía principal

```css
subgraph sg1 [Contexto]
    A --> B
end

style sg1 fill:3b4252,stroke:#5e81ac,stroke-width:1.5px,stroke-dasharray:5 5
```

---

# 8️⃣ Guía rápida: ¿qué tipo uso?

|Quiero explicar…|Usa|
|---|---|
|Un algoritmo|Flow lógico|
|Clasificar ideas|Conceptual|
|Niveles / capas|Jerárquico|
|Software / pipeline|Arquitectura|
|Enseñar|Conceptual + ejemplos|
|Documentar código|Jerárquico + arquitectura|

