---
title: Práctica Calificada – 1
draft: false
---


# Práctica Calificada – 1

---

## Ejercicio 1 – Sistema de Reporte Digital de Salud (6 puntos)

### Enunciado

**Contexto:**  
Una clínica privada desea automatizar la generación de reportes médicos básicos.

**Requerimientos:**  
Desarrolle un programa que solicite:

- Nombre completo
- Año de nacimiento
- Estatura en metros
- Peso en kilogramos
- Frecuencia cardíaca en reposo
- Presión sistólica
- Presión diastólica

**Cálculos a realizar:**

- Edad (año actual fijo: 2026)
- Estatura en centímetros
- IMC = peso / estatura²
- IPA = sistólica / diastólica

**Debe usar:**
- f-strings
- Formato decimal con :.2f
- Alineación de texto

### Ejemplo de salida esperada

```bash
.
==============================================
SISTEMA DE REGISTRO CLINICO
==============================================

Ingrese nombre completo : Juan Perez
Ingrese anio nacimiento : 2005
Ingrese estatura (m)    : 1.75
Ingrese peso (kg)       : 70
Frecuencia cardiaca     : 72
Presion sistolica       : 120
Presion diastolica      : 80

==============================================
REPORTE DE SALUD
==============================================

Paciente                : Juan Perez
Edad                    : 21 anios
Estatura                : 1.75 m (175.00 cm)
Peso                    : 70.00 kg
IMC                     : 22.86
Frecuencia Cardiaca     : 72 ppm
Presion Arterial        : 120/80
Indice Presion (IPA)    : 1.50
==============================================
```

### Rúbrica de calificación

| Criterio | Puntaje |
|----------|---------|
| Cálculos correctos | 2 pts |
| Uso correcto de f-strings y formato | 2 pts |
| Presentación alineada profesional | 1 pt |
| Casting correcto y ejecución sin errores | 1 pt |
| **Total** | **6 pts** |

### Espacio para código

```python
print("==============================================")
print("SISTEMA DE REGISTRO CLINICO")
print("==============================================\n")

# Solicitar datos al usuario
nombre = input("Ingrese nombre completo : ")
anio_nacimiento = int(input("Ingrese anio nacimiento : "))
estatura_m = float(input("Ingrese estatura (m)    : "))
peso = float(input("Ingrese peso (kg)       : "))
frecuencia = int(input("Frecuencia cardiaca     : "))
presion_sist = int(input("Presion sistolica       : "))
presion_diast = int(input("Presion diastolica      : "))

# Cálculos
anio_actual = 2026
edad = anio_actual - anio_nacimiento
estatura_cm = estatura_m * 100
imc = peso / (estatura_m ** 2)
ipa = presion_sist / presion_diast

# Mostrar reporte con formato
print("\n==============================================")
print("REPORTE DE SALUD")
print("==============================================\n")

print(f"{'Paciente':<25}: {nombre}")
print(f"{'Edad':<25}: {edad} anios")
print(f"{'Estatura':<25}: {estatura_m} m ({estatura_cm:.2f} cm)")
print(f"{'Peso':<25}: {peso:.2f} kg")
print(f"{'IMC':<25}: {imc:.2f}")
print(f"{'Frecuencia Cardiaca':<25}: {frecuencia} ppm")
print(f"{'Presion Arterial':<25}: {presion_sist}/{presion_diast}")
print(f"{'Indice Presion (IPA)':<25}: {ipa:.2f}")

print("==============================================")
```


---

## Ejercicio 2 – Sistema Corporativo de Identificación (6 puntos)

### Enunciado

**Contexto:**  
La empresa MyFactoryCompany necesita automatizar la creación de correos institucionales y códigos internos.

**Requerimientos:**  
Solicite:

- Primer nombre
- Primer apellido
- Segundo apellido
- Año de ingreso
- Sector (1–4)

**Generar:**

**Correo institucional:**
```
primer_nombre.apellido1.primera_letra_apellido2@myfactorycompany.te
```
(todo en minúsculas)

**ID empresarial:**
```
AAAA S NNN LL
```
Donde:
- **AAAA** → Año de ingreso
- **S** → Sector
- **NNN** → (suma unicode nombre + apellido1) mod 1000 (formato 3 dígitos)
- **LL** → Primera letra nombre + última letra apellido2 (mayúsculas)

### Ejemplo de salida esperada

```bash
.
==============================================
SISTEMA DE REGISTRO EMPRESARIAL
==============================================

Primer nombre      : Juan
Primer apellido    : Perez
Segundo apellido   : Gomez
Anio ingreso       : 2024
Sector (1-4)       : 2

==============================================
DATOS GENERADOS
==============================================

Correo institucional :
juan.perez.g@myfactorycompany.te

ID empresarial :
20242013JG
==============================================
```

### Rúbrica de calificación

| Criterio | Puntaje |
|----------|---------|
| Manipulación correcta de cadenas | 2 pts |
| Uso correcto de indexación y métodos (.lower, .upper) | 2 pts |
| Cálculo correcto con ord() y formato :03d | 1 pt |
| Presentación clara | 1 pt |
| **Total** | **6 pts** |

### Espacio para código

```python
print("==============================================")
print("SISTEMA DE REGISTRO EMPRESARIAL")
print("==============================================\n")

# Solicitar datos al usuario
nombre = input("Primer nombre      : ")
apellido1 = input("Primer apellido    : ")
apellido2 = input("Segundo apellido   : ")
anio_ingreso = input("Anio ingreso       : ")
sector = input("Sector (1-4)       : ")

# Generar correo institucional
primera_letra_ap2 = apellido2[0].lower()
correo = f"{nombre.lower()}.{apellido1.lower()}.{primera_letra_ap2}@myfactorycompany.te"

# Calcular suma Unicode
suma_unicode = ord(nombre[0]) + ord(apellido1[0])
codigo_nnn = suma_unicode % 1000

# Generar código LL
primera_letra_nombre = nombre[0].upper()
ultima_letra_ap2 = apellido2[-1].upper()
ll = primera_letra_nombre + ultima_letra_ap2

# Generar ID empresarial
id_empresarial = f"{anio_ingreso}{sector}{codigo_nnn:03d}{ll}"

# Mostrar resultados
print("\n==============================================")
print("DATOS GENERADOS")
print("==============================================\n")

print("Correo institucional :")
print(correo)
print("\nID empresarial :")
print(id_empresarial)
print("==============================================")
```


---

## Ejercicio 3 – Sistema Orbital de Decodificación Numérica (8 puntos)

### Enunciado

**Contexto:**  
La empresa aeroespacial Orbital Cargo Systems codifica cápsulas mediante un número entero de 6 dígitos.

**Estructura del código:**
```
AB CD EF
```
- **AB** → Tipo de cápsula
- **CD** → Lote
- **EF** → Prioridad

**Requerimientos:**  
Solicite el código de 6 dígitos e implemente:

- Extraer AB, CD y EF usando // y %
- Suma de todos los dígitos
- Producto de los dos últimos dígitos
- Diferencia entre los dos primeros dígitos
- Número invertido matemáticamente (sin convertir a string)

### Ejemplo de salida esperada

```bash
.
==============================================
SISTEMA ORBITAL DE DECODIFICACION
==============================================

Ingrese codigo : 482731

==============================================
RESULTADO
==============================================

Tipo capsula            : 48
Numero lote             : 27
Codigo prioridad        : 31
Suma total digitos      : 25
Producto ultimos digitos: 3
Diferencia primeros     : 4
Codigo invertido        : 137284
==============================================
```

### Rúbrica de calificación

| Criterio | Puntaje |
|----------|---------|
| Uso correcto de // y % | 3 pts |
| Descomposición correcta de bloques numéricos | 2 pts |
| Inversión matemática sin strings | 2 pts |
| Orden y presentación | 1 pt |
| **Total** | **8 pts** |

### Espacio para código

```python
print("==============================================")
print("SISTEMA ORBITAL DE DECODIFICACION")
print("==============================================\n")

# Solicitar código de 6 dígitos
codigo = int(input("Ingrese codigo : "))

# Extraer dígitos individuales
digito1 = codigo // 100000
digito2 = (codigo // 10000) % 10
digito3 = (codigo // 1000) % 10
digito4 = (codigo // 100) % 10
digito5 = (codigo // 10) % 10
digito6 = codigo % 10

# Extraer bloques
tipo_capsula = codigo // 10000  # AB
lote = (codigo // 100) % 100     # CD
prioridad = codigo % 100          # EF

# Calcular suma total de dígitos
suma_digitos = digito1 + digito2 + digito3 + digito4 + digito5 + digito6

# Calcular producto de los dos últimos dígitos
producto_ultimos = digito5 * digito6

# Calcular diferencia entre los dos primeros dígitos
diferencia_primeros = digito1 - digito2

# Invertir número matemáticamente
invertido = (digito6 * 100000) + (digito5 * 10000) + (digito4 * 1000) + (digito3 * 100) + (digito2 * 10) + digito1

# Mostrar resultados
print("\n==============================================")
print("RESULTADO")
print("==============================================\n")

print(f"{'Tipo capsula':<25}: {tipo_capsula}")
print(f"{'Numero lote':<25}: {lote}")
print(f"{'Codigo prioridad':<25}: {prioridad}")
print(f"{'Suma total digitos':<25}: {suma_digitos}")
print(f"{'Producto ultimos digitos':<25}: {producto_ultimos}")
print(f"{'Diferencia primeros':<25}: {diferencia_primeros}")
print(f"{'Codigo invertido':<25}: {invertido}")

print("==============================================")
```


---

## Instrucciones Generales de Entrega

- Desarrolle cada ejercicio en un archivo independiente (Ej1.py, Ej2.py, Ej3.py)
- **Entrega especial:** Pegue el código completo de los tres ejercicios en un único documento Word
- Incluya una captura de pantalla donde se observe claramente la ejecución correcta de cada programa
- **Restricciones:**
  - No se permite el uso de condicionales
  - No se permite el uso de bucles
  - No se permiten funciones definidas por el usuario
  - Solo se permite el uso de lo desarrollado en la clase 1
- El código debe ejecutarse sin errores

---

**Puntaje Total: 20 puntos**  
**Distribución: 6 – 6 – 8**