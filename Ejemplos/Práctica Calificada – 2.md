---
title: Práctica Calificada – 2
draft: false
---

# Práctica Calificada – 2

---

## Ejercicio 1 – Sistema de Cálculo de Bonificaciones (6 puntos)

### Enunciado

**Contexto:**  
Una empresa implementa un sistema para calcular la bonificación anual de sus empleados. La bonificación se calcula en función de su rendimiento y antigüedad.

**Requerimientos:**  
Solicite al usuario:
- Puntuación de rendimiento (0 a 100)
- Años de antigüedad en la empresa
- Número de proyectos exitosos en el año

**Cálculo de la bonificación base:**  
Debe utilizar el **operador ternario** para asignar la bonificación base según la siguiente tabla:

| Rendimiento | Bonificación Base |
|-------------|-------------------|
| $\geq$ 90   | 2000              |
| 70 - 89     | 1200              |
| $<$ 70      | 500               |

**Ejemplo de uso del operador ternario:**
```python
estado = "Aprobado" if promedio >= 14 else "Desaprobado"
```

**Ajustes a la bonificación:**  
Luego de tener la bonificación base, aplique las siguientes reglas usando condicionales anidados:

1. Por antigüedad:
   - Mayor a 10 años → aumentar bonificación en 30%
   - Entre 5 y 10 años → aumentar en 15%
   - Menor a 5 años → sin aumento

2. Por proyectos (después del ajuste por antigüedad):
   - Más de 5 proyectos exitosos → agregar S/300 extra
   - Entre 3 y 5 proyectos → agregar S/150 extra

**Resultado final:**  
Mostrar:
- La bonificación base (asignada con operador ternario)
- La bonificación final después de todos los ajustes
- Un mensaje que indique:
  - **Bonificación alta** si el total > 2500
  - **Bonificación media** si está entre 1500 y 2500
  - **Bonificación estándar** si es < 1500

### Ejemplo de ejecución:
```bash
.
=== SISTEMA DE BONIFICACIONES ===
Ingrese puntuación de rendimiento (0-100): 85
Ingrese años de antigüedad: 12
Ingrese número de proyectos exitosos: 4

RESULTADOS:
Bonificación base: 1200
Bonificación final: 1710.0
Categoría: Bonificación media
```

### Rúbrica de calificación:
| Criterio | Puntaje |
|----------|---------|
| Uso correcto del operador ternario para asignar bonificación base | 2 pts |
| Implementación correcta de condicionales | 2 pts |
| Cálculos aritméticos precisos | 1 pt |
| Presentación clara y ejecución sin errores | 1 pt |
| **Total** | **6 pts** |

### Espacio para código:
```python
print ( "=== SISTEMA DE BONIFICACIONES ===" )

  

rendimiento = float ( input ( "Ingrese puntuación de rendimiento (0 -100) : " ) )

antiguedad = int ( input ( "Ingrese años de antigüedad : " ) )

proyectos = int ( input ( "Ingrese número de proyectos exitosos : "))

  
  

# Bonificación base usando operador ternario anidado

bonificacion_base = 2000 if rendimiento >= 90 else \

1200 if rendimiento >= 70 else 500

bonificacion_final = bonificacion_base

  
  

# Ajuste por antigüedad

if antiguedad > 10:

bonificacion_final = bonificacion_final * 1.30

elif antiguedad >= 5:

bonificacion_final = bonificacion_final * 1.15

  
  

# Ajuste por proyectos

if proyectos > 5:

bonificacion_final = bonificacion_final + 300

elif proyectos >= 3:

bonificacion_final = bonificacion_final + 150

  
  

# Categor í a final

if bonificacion_final > 2500:

categoria = "Bonificación alta "

elif bonificacion_final >= 1500:

categoria = "Bonificación media "

else :

categoria = "Bonificación estándar "

  
  

print ( "\nRESULTADOS : " )

print ( "Bonificación base : " , bonificacion_base )

print ( "Bonificación final : " , bonificacion_final )

print ( "Categoría : " , categoria )
```


---

## Ejercicio 2 – Sistema de Evaluación por Competencias (7 + 2 puntos)

### Enunciado

**Contexto:**  
Un instituto evalúa a sus estudiantes mediante 2 competencias:
- Competencia Técnica (3 notas)
- Competencia Comunicativa (3 notas)

La información debe organizarse en dos **vectores con len() = 3**.

Solicite las 6 notas y construya:
```python
notas_T = [t1, t2, t3]  # Competencia Técnica
notas_C = [c1, c2, c3]  # Competencia Comunicativa
```

**El programa debe calcular:**
- Promedio de Competencia Técnica
- Promedio de Competencia Comunicativa
- Promedio General

**Luego determinar:**

1. **Competencia más fuerte** (comparando promedios)
2. **Si ambas están equilibradas** (diferencia menor a 1.5 puntos)
3. **Estado académico** según promedio general:
   - >= 14 → APROBADO
   - 9 a 13.99 → SUSTITUTORIO
   - < 9 → DESAPROBADO
4. **Desempeño:**
   - Si ambas competencias >= 13 → "Desempeño consistente"
   - En caso contrario → "Desempeño desigual"

**Manipulación adicional de las listas:**

Si el estado académico es **Sustitutorio**:
- Se deberá ingresar la nota de la prueba Sustitutoria
- Esta nota reemplazará a la **nota más baja** (de cualquiera de las dos competencias)
- Se procederá a **re-calcular** todos los promedios y resultados

### Ejemplo de ejecución:
```bash
.
=== SISTEMA DE EVALUACIÓN POR COMPETENCIAS ===
Ingrese nota técnica 1: 12
Ingrese nota técnica 2: 10
Ingrese nota técnica 3: 11
Ingrese nota comunicativa 1: 14
Ingrese nota comunicativa 2: 16
Ingrese nota comunicativa 3: 15

VECTORES DE NOTAS ORIGINAL:
Técnica: [12.0, 10.0, 11.0]
Comunicativa: [14.0, 16.0, 15.0]

RESULTADOS:
Promedio Técnica: 11.0
Promedio Comunicativa: 15.0
Promedio General: 13.0
Competencia más fuerte: Comunicativa
Competencias equilibradas? No
Estado académico: SUSTITUTORIO
Desempeño: Desempeño desigual

****Nota nueva****
Ingrese nota Sustitutoria: 16

VECTORES DE NOTAS ORIGINAL:
Técnica: [12.0, 16.0, 11.0]
Comunicativa: [14.0, 16.0, 15.0]

RESULTADOS:
Promedio Técnica: 13.0
Promedio Comunicativa: 15.0
Promedio General: 14.0
Competencia más fuerte: Comunicativa
Competencias equilibradas? No
Estado académico: APROBADO
Desempeño: Desempeño consistente
```

### Rúbrica de calificación:
| Criterio | Puntaje |
|----------|---------|
| Cálculo correcto de promedios | 2 pts |
| Comparaciones usando condicionales | 3 pts |
| Uso correcto de operadores lógicos | 2 pt |
| Lógica para el re-calculo de la Nota Sustitutoria | 2 pts extra |
| **Total** | **7 + 2 pts** |

### Espacio para código:
```python
print("=== SISTEMA DE EVALUACIÓN POR COMPETENCIAS ===")

# Entrada de datos
t1 = float(input("Ingrese nota técnica 1: "))
t2 = float(input("Ingrese nota técnica 2: "))
t3 = float(input("Ingrese nota técnica 3: "))
c1 = float(input("Ingrese nota comunicativa 1: "))
c2 = float(input("Ingrese nota comunicativa 2: "))
c3 = float(input("Ingrese nota comunicativa 3: "))

# Construcción de lista

notas_T = [t1, t2, t3]
notas_C = [c1, c2, c3]


print("\nVECTORES DE NOTAS ORIGINAL:")
print("Técnica:", notas_T)
print("Comunicativa:", notas_C)

# Promedios
prom_tecnica = (notas_T[0] + notas_T[1] + notas_T[2]) / 3
prom_comunicativa = (notas_C[0] + notas_C[1] + notas_C[2]) / 3
prom_general = (prom_tecnica + prom_comunicativa) / 2

# Competencia más fuerte
if prom_tecnica > prom_comunicativa:
	fuerte = "Técnica"
elif prom_comunicativa > prom_tecnica:
	fuerte = "Comunicativa"
else:
	fuerte = "Iguales"

# Equilibrio
equilibradas = "Sí" if abs(prom_tecnica - prom_comunicativa) < 1.5 else "No"

# Estado académico
if prom_general >= 14:
	estado = "APROBADO"
elif prom_general >= 9:
	estado = "SUSTITUTORIO"
else:
	estado = "DESAPROBADO"

# Desempeño
if prom_tecnica >= 13 and prom_comunicativa >= 13:
	desempeno = "Desempeño consistente"
else:
	desempeno = "Desempeño desigual"

print("\nRESULTADOS:")
print("Promedio Técnica:", prom_tecnica)
print("Promedio Comunicativa:", prom_comunicativa)
print("Promedio General:", prom_general)
print("Competencia más fuerte:", fuerte)
print("Competencias equilibradas?", equilibradas)
print("Estado académico:", estado)
print("Desempeño:", desempeno)

# Recalificación
if estado == "SUSTITUTORIO":

	print("\n ****Nota nueva****")
	nota_susti = float(input("Ingrese nota Sustitutoria: "))

	# Re-Construcción de listas

	nota_min_T = notas_T[0]
	indice_menor_T = 0

	if nota_min_T > notas_T[1]:
		nota_min_T = notas_T[1] 
		indice_menor_T = 1
	
	if nota_min_T > notas_T[2]:
		nota_min_T = notas_T[2] 
		indice_menor_T = 2


	nota_min_C = notas_C[0]
	indice_menor_C = 0

	if nota_min_C > notas_C[1]:
		nota_min_C = notas_C[1] 
		indice_menor_C = 1
	
	if nota_min_C > notas_C[2]:
		nota_min_C = notas_C[2] 
		indice_menor_C = 2

	# Re-Asignacion de Notas
	if nota_min_T <= nota_min_C:
		notas_T[indice_menor_T] = nota_susti
	else:
		notas_C[indice_menor_C] = nota_susti

	
	print("\nVECTORES DE NOTAS ORIGINAL:")
	print("Técnica:", notas_T)
	print("Comunicativa:", notas_C)

	# Promedios
	prom_tecnica = (notas_T[0] + notas_T[1] + notas_T[2]) / 3
	prom_comunicativa = (notas_C[0] + notas_C[1] + notas_C[2]) / 3
	prom_general = (prom_tecnica + prom_comunicativa) / 2

	# Competencia más fuerte
	if prom_tecnica > prom_comunicativa:
		fuerte = "Técnica"
	elif prom_comunicativa > prom_tecnica:
		fuerte = "Comunicativa"
	else:
		fuerte = "Iguales"

	# Equilibrio
	equilibradas = "Sí" if abs(prom_tecnica - prom_comunicativa) < 1.5 else "No"

	# Estado académico
	if prom_general >= 14:
		estado = "APROBADO"
	elif prom_general >= 9:
		estado = "SUSTITUTORIO"
	else:
		estado = "DESAPROBADO"

	# Desempeño
	if prom_tecnica >= 13 and prom_comunicativa >= 13:
		desempeno = "Desempeño consistente"
	else:
		desempeno = "Desempeño desigual"

	print("\nRESULTADOS:")
	print("Promedio Técnica:", prom_tecnica)
	print("Promedio Comunicativa:", prom_comunicativa)
	print("Promedio General:", prom_general)
	print("Competencia más fuerte:", fuerte)
	print("Competencias equilibradas?", equilibradas)
	print("Estado académico:", estado)
	print("Desempeño:", desempeno)
```

---

## Ejercicio 3 – Analizador Avanzado de Colores RGB (7 puntos)

### Enunciado

**Contexto:**  
En diseño gráfico y desarrollo web, los colores se representan con el modelo RGB (Red, Green, Blue), donde cada componente tiene un valor entre 0 y 255. Un laboratorio de diseño necesita un programa que analice colores y determine sus características.

**Requerimientos:**

1. Solicitar al usuario 3 valores enteros (R, G, B) entre 0 y 255. Almacenarlos en una lista llamada `color = [r, g, b]`.

2. El programa **solo continuará** si los 3 valores son válidos (dentro del rango 0 a 255). En caso contrario, mostrar "Ingrese Valores Validos".

3. **Determinar el color predominante:** Sin usar la función `max()`, determine mediante condicionales cuál es el componente con mayor valor.
   - Si R es el mayor (estrictamente mayor que G y B) → Color predominante: Rojo
   - Si G es el mayor → Color predominante: Verde
   - Si B es el mayor → Color predominante: Azul
   - Si hay empate entre dos o más valores (y son los más altos) → "Hay 2 colores empatados: [color1] y [color2]"
   - Si todos son iguales → "No Hay colores Dominantes ni Secundarios"

4. **Calcular el brillo:** El brillo se calcula como el promedio de los tres componentes: (R + G + B) / 3. Determine la categoría:
   - Brillo > 200 → Muy brillante
   - Brillo entre 100 y 200 → Brillo medio
   - Brillo < 100 → Oscuro

5. **Análisis de saturación:** La saturación indica la intensidad del color. Se calcula como la diferencia entre el valor máximo y el mínimo de los componentes.
   - Determine el valor máximo y mínimo de los tres componentes (sin usar max()/min())
   - Saturación = máximo - mínimo
   - Si saturación > 150 → Color muy saturado (vibrante)
   - Si saturación entre 50 y 150 → Color moderadamente saturado
   - Si saturación < 50 → Color poco saturado (grisáceo)

6. **Clasificación del color:** Basado en el componente predominante:
   - **Cálido**: predomina Rojo
   - **Frío**: predomina Azul
   - **Neutro**: predomina Verde o hay empate

### Ejemplos de ejecución:

**Ejemplo 1:**
```bash
.
=== ANALIZADOR AVANZADO DE COLORES RGB ===
Ingrese valor de Rojo (0-255): 250
Ingrese valor de Verde (0-255): 100
Ingrese valor de Azul (0-255): 22

Color analizado: [250, 100, 22]

RESULTADOS DEL ANÁLISIS:
1. Color predominante: Rojo
2. Brillo: 124.0 - Brillo medio
3. Saturación: 228 - Color muy saturado (vibrante)
4. Clasificación térmica: Cálido
```

**Ejemplo 2:**
```bash
.
=== ANALIZADOR AVANZADO DE COLORES RGB ===
Ingrese valor de Rojo (0-255): 150
Ingrese valor de Verde (0-255): 150
Ingrese valor de Azul (0-255): 100

Color analizado: [150, 150, 100]

RESULTADOS DEL ANÁLISIS:
1. Color predominante: Hay 2 colores empatados: Rojo y Verde
2. Brillo: 133.33333333333334 - Brillo medio
3. Saturación: 50 - Color moderadamente saturado
4. Clasificación térmica: Neutro
```

**Ejemplo 3:**
```bash
.
=== ANALIZADOR AVANZADO DE COLORES RGB ===
Ingrese valor de Rojo (0-255): 100
Ingrese valor de Verde (0-255): 100
Ingrese valor de Azul (0-255): 100

Color analizado: [100, 100, 100]

RESULTADOS DEL ANÁLISIS:
1. Color predominante: No Hay colores Dominantes ni Secundarios
2. Brillo: 100.0 - Brillo medio
3. Saturación: 0 - Color poco saturado (grisáceo)
4. Clasificación térmica: Neutro
```

**Ejemplo 4 (validación):**
```bash
.
=== ANALIZADOR AVANZADO DE COLORES RGB ===
Ingrese valor de Rojo (0-255): 400
Ingrese valor de Verde (0-255): 20
Ingrese valor de Azul (0-255): 100

Ingrese Valores Validos
```

### Rúbrica de calificación:
| Criterio | Puntaje |
|----------|---------|
| Almacenamiento correcto en lista y validación de entrada | 1 pt |
| Determinación del color predominante sin usar max() | 1.5 pts |
| Cálculo correcto del brillo y categorización | 1.5 pts |
| Cálculo correcto de saturación (máximo y mínimo) | 1.5 pts |
| Clasificación térmica y uso de condicionales | 1.5 pts |
| **Total** | **7 pts** |

### Espacio para código:
```python
print("=== ANALIZADOR AVANZADO DE COLORES RGB ===")

  

error = False

r = int(input("Ingrese valor de Rojo (0-255): "))

if not (0 <= r <= 255) : error = True

  

g = int(input("Ingrese valor de Verde (0-255): "))

if not (0 <= g <= 255) : error = True

  

b = int(input("Ingrese valor de Azul (0-255): "))

if not (0 <= b <= 255) : error = True

  

if not error:

  

color = [r, g, b]

  

color_nombres = ["Rojo", "Verde", "Azul"]

  

print("\nColor analizado:", color)

  

# Determinar máximo

valor_max = color[0]

  

if valor_max < color[1]:

valor_max = color[1]

  

if valor_max < color[2]:

valor_max = color[2]

  

# Determinando mínimo

valor_min = color[0]

  

if valor_min > color[1]:

valor_min = color[1]

  

if valor_min > color[2]:

valor_min = color[2]

  

# Determinar predominante

colores_max = []

  

if valor_max == color[0]:

colores_max.append(0)

if valor_max == color[1]:

colores_max.append(1)

  

if valor_max == color[2]:

colores_max.append(2)

  

numero_empates = len(colores_max)

  

if numero_empates == 3:

predominante = "No Hay colores Dominantes ni Secundarios"

elif numero_empates == 2:

predominante = f"Hay 2 colores empatados: {color_nombres[colores_max[0]]} y {color_nombres[colores_max[1]]} "

else:

predominante = f"{color_nombres[colores_max[0]]}"

  

# Brillo

brillo = (r + g + b) / 3

  

if brillo > 200:

categoria_brillo = "Muy brillante"

elif brillo >= 100:

categoria_brillo = "Brillo medio"

else:

categoria_brillo = "Oscuro"

  
  
  

# Saturacion

saturacion = valor_max - valor_min

  

if saturacion > 150:

categoria_sat = "Color muy saturado (vibrante)"

elif saturacion >= 50:

categoria_sat = "Color moderadamente saturado"

else:

categoria_sat = "Color poco saturado (grisáceo)"

  

# Clasificación térmica

if predominante == "Rojo":

clasificacion = "Cálido"

elif predominante == "Azul":

clasificacion = "Frío"

else:

clasificacion = "Neutro"

  
  
  

print("\nRESULTADOS DEL ANÁLISIS:")

print("1. Color predominante:", predominante)

print("2. Brillo:", brillo, "-", categoria_brillo)

print("3. Saturación:", saturacion, "-", categoria_sat)

print("4. Clasificación térmica:", clasificacion)

  

else:

print("\nIngrese Valores Validos")
```

---

## Instrucciones Generales de Entrega

- Desarrolle cada ejercicio en un archivo independiente (Ej1.py, Ej2.py, Ej3.py)
- Pegue el código completo en este documento Word
- Incluya captura de ejecución correcta para cada ejercicio
- Solo se permite utilizar:
  - Tipos básicos (int, float, bool)
  - string
  - list (acceso por índice, asignación)
  - condicionales (if, elif, else)
  - operador ternario
  - operadores lógicos (and, or, not)
  - len()
- No se permite usar:
  - for, while
  - max(), min(), sum()
  - funciones definidas por el usuario
  - estructuras no vistas en clase (tuple, dict, set)
  - list comprehension
- El código debe ejecutarse sin errores

---

**Puntaje Total: 20(22) puntos**  
**Distribución: 6 – 7(9) – 7**