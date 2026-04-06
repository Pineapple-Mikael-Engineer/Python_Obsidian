---
draft: true
---

## 🟢 NIVEL 1 - FUNDAMENTOS (Introducción, Pyplot, Figure, Axes)

### Ejercicio 1: Tu primera figura
Crear una figura con `plt.subplots()` que contenga una línea simple (`y = x²`). Personalizar:
- Título: "Mi primera gráfica"
- Etiqueta X: "Valores X"
- Etiqueta Y: "Valores Y cuadrados"
- Grid activado

### Ejercicio 2: Múltiples subplots
Usando `plt.subplots(2, 2)`, graficar en cada subplot:
1. Línea: y = x
2. Línea: y = x²
3. Línea: y = √x
4. Línea: y = x³

Ajustar el espaciado entre subplots (`tight_layout()`)

### Ejercicio 3: Configuración global con rcParams
- Cambiar el tamaño de fuente global a 12
- Cambiar el estilo de línea por defecto a '--'
- Cambiar el color por defecto a 'red'
- Crear una gráfica simple para verificar los cambios

---

## 🟡 NIVEL 2 - MÉTODOS DE AXES (Formato, Spines, Anotaciones)

### Ejercicio 4: Personalización completa de ejes
Crear una gráfica de `y = sin(x)` para x de 0 a 4π:
- Usar `ax.set_xticks()` para mostrar solo [0, π, 2π, 3π, 4π]
- Usar `ax.set_xticklabels()` con ['0', 'π', '2π', '3π', '4π']
- Usar `ax.tick_params()` para rotar las etiquetas 45°
- Configurar spines: ocultar el spine superior y derecho

### Ejercicio 5: Anotaciones y leyenda
Graficar tres líneas: `y1 = x`, `y2 = x²`, `y3 = e^x` (x de -2 a 2)
- Agregar leyenda con nombres personalizados
- Agregar anotación señalando el punto donde y1 = y2
- Agregar anotación señalando el mínimo de y2
- Usar `ax.grid()` con transparencia (alpha=0.3)

---

## 🟠 NIVEL 3 - GRÁFICOS ESPECÍFICOS

### Ejercicio 6: Bar chart y barh
Datos de ventas trimestrales: Q1=150, Q2=220, Q3=180, Q4=250
1. Crear `ax.bar()` vertical
2. Crear `ax.barh()` horizontal
3. Para el vertical: agregar etiquetas con los valores encima de cada barra
4. Para el horizontal: cambiar colores por trimestre

### Ejercicio 7: Histograma y scatter plot
Generar 1000 números aleatorios con distribución normal (media=0, std=1):
- `ax.hist()` con 30 bins, color='skyblue', borde='black'
- Agregar línea vertical en la media y mediana
- En otra figura, crear `ax.scatter()` comparando dos arrays aleatorios con correlación

### Ejercicio 8: Fill between y contour
Crear gráfica de `y = x²` y `y = x⁴` para x de -2 a 2:
- Usar `ax.fill_between()` para rellenar el área entre ambas curvas
- Cambiar color del relleno con alpha=0.3
- Agregar `ax.contour()` con niveles personalizados (usar datos 2D)

---

## 🔴 NIVEL 4 - AVANZADO (GridSpec, Ticker, Toolkits)

### Ejercicio 9: Layout complejo con GridSpec
Crear un layout con:
- Panel grande arriba (80% altura)
- Dos paneles pequeños abajo (20% altura, dividido 50%-50%)
- En el panel grande: gráfico de líneas
- Panel izquierdo abajo: histograma
- Panel derecho abajo: scatter plot

### Ejercicio 10: Locators personalizados
Graficar datos de temperatura por hora (0-24):
- Usar `MultipleLocator` para ticks cada 2 horas
- Usar `FormatStrFormatter` para mostrar 'XXh'
- Agregar `MaxNLocator` para limitar a 8 ticks máximo en Y

### Ejercicio 11: Gráfico 3D (toolkits mplot3d)
Crear figura 3D con:
- Superficie de `z = sin(√(x² + y²))` para x,y de -5 a 5
- Configurar ángulo de vista (elev=30, azim=45)
- Agregar barra de colores

---

## ⭐ NIVEL 5 - PROYECTOS INTEGRADORES

### Proyecto 1: Dashboard de análisis de datos
Crear dashboard 2x2 con GridSpec:
1. **Arriba izq**: Scatter plot con correlación
2. **Arriba der**: Histograma superpuesto (dos distribuciones)
3. **Abajo izq**: Barras con error bars
4. **Abajo der**: Gráfico de líneas con relleno entre curvas
- Usar `plt.style.use()` para aplicar un estilo profesional ('seaborn-v0_8-darkgrid' o 'ggplot')
- Personalizar todos los spines y ticks

### Proyecto 2: Animación (animation)
Crear animación de una onda sinusoidal que se desplaza:
- 100 frames
- Onda que se mueve hacia la derecha
- Agregar punto que sigue el máximo de la onda
- Guardar como GIF o MP4

### Proyecto 3: Personalización completa con patches
Crear una figura que muestre:
- Un rectángulo (`patches.Rectangle`)
- Un círculo (`patches.Circle`)
- Una flecha (`patches.FancyArrowPatch`)
- Una elipse (`patches.Ellipse`)
- Todo sobre un mismo axes, con leyenda personalizada

---

