---
title: scipy.signal.welch — densidad espectral de potencia por el metodo de Welch
aliases:
  - welch
  - scipy.signal.welch
  - metodo de Welch
  - PSD welch
tags:
  - scipy
  - api/funcion
  - analisis-espectral
lib: scipy
tipo: funcion
mod: scipy.signal
retorna: tuple (ndarray, ndarray)
requiere:
  - numpy
  - scipy.signal.periodogram
draft: false
---

# scipy.signal.welch — densidad espectral de potencia por el metodo de Welch

Estima la **densidad espectral de potencia (PSD)** de una señal mediante el **metodo de Welch**: divide la señal en segmentos solapados, calcula el periodograma de cada segmento (tras aplicar una ventana) y **promedia** esos periodogramas. Ese promedio reduce drasticamente la varianza del estimador frente a un periodograma unico, a costa de menor resolucion en frecuencia. Es el estimador espectral **estandar en la practica** para señales ruidosas. Devuelve una **tupla** `(f, Pxx)`: el array de frecuencias y el array de densidad de potencia.

> El metodo de Welch internamente apoya su FFT en la maquinaria de transformada rapida; SciPy expone esa base como `scipy.fft`. Welch no es mas que un periodograma promediado por segmentos, ver [[scipy.signal.periodogram]].

## Firma

```python
scipy.signal.welch(
    x,                    # array_like: señal de entrada (1D, o ND con axis)
    fs=1.0,               # float: frecuencia de muestreo en Hz
    window='hann',        # str | tuple | array: ventana por segmento
    nperseg=None,         # int: muestras por segmento (default 256 o len(x))
    noverlap=None,        # int: muestras solapadas (default nperseg // 2)
    nfft=None,            # int: longitud de FFT (zero-padding si > nperseg)
    detrend='constant',   # str | callable | False: quita tendencia por segmento
    return_onesided=True, # bool: espectro de un solo lado (señal real)
    scaling='density',    # 'density' (V^2/Hz) | 'spectrum' (V^2)
    axis=-1,              # int: eje a lo largo del cual calcular
    average='mean',       # 'mean' | 'median': como combinar segmentos
) -> tuple
```

## Valor de retorno

Devuelve la tupla `(f, Pxx)`. Se desempaqueta tipicamente como `f, Pxx = welch(...)`.

| Posicion | Nombre | Tipo | Forma | Significado |
|----------|--------|------|-------|-------------|
| `[0]` | `f` | `ndarray` | `(nperseg//2 + 1,)` | Frecuencias de muestreo del espectro (en Hz si se dio `fs`) |
| `[1]` | `Pxx` | `ndarray` | igual que `f` | Densidad espectral de potencia en cada frecuencia |

Con `scaling='density'`, `Pxx` esta en unidades de `V^2/Hz`; con `scaling='spectrum'`, en `V^2` (potencia por bin).

```python
f, Pxx = welch(x, fs=1000)
f.shape, Pxx.shape   # → ((129,), (129,))  con nperseg=256 por defecto
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| PSD con defaults | `welch(x, fs)` |
| Controlar resolucion/varianza | `welch(x, fs, nperseg=1024)` |
| Cambiar ventana | `welch(x, fs, window='hamming')` |
| Solape personalizado | `welch(x, fs, nperseg=512, noverlap=384)` |
| Potencia por bin (no densidad) | `welch(x, fs, scaling='spectrum')` |
| Robusto a transitorios | `welch(x, fs, average='median')` |

## Parametros en detalle

### `x` (obligatorio)

Señal de entrada. Normalmente un array 1D de muestras temporales; con `axis` puede ser ND.

### `fs`

Frecuencia de muestreo en Hz. Si se omite (`fs=1.0`), las frecuencias de salida quedan **normalizadas** en ciclos por muestra (rango `[0, 0.5]`). Darla correctamente es lo que hace que `f` salga en Hz reales.

```python
import numpy as np
from scipy.signal import welch

fs = 1000.0                                  # Hz
t = np.arange(0, 5, 1/fs)
x = np.sin(2*np.pi*50*t) + 0.5*np.random.randn(t.size)
f, Pxx = welch(x, fs, nperseg=1024)
f[np.argmax(Pxx)]    # → ~50.0   (frecuencia dominante recuperada)
```

### `nperseg`

Muestras por segmento. Es el **compromiso central**: segmentos largos → mejor resolucion en frecuencia pero menos segmentos para promediar (mas varianza); segmentos cortos → mas promediado (menos varianza) pero peor resolucion. Potencias de 2 favorecen la FFT.

### `noverlap`

Muestras compartidas entre segmentos consecutivos. Por defecto `nperseg // 2` (50 % de solape), valor recomendado con la ventana Hann. Mas solape genera mas segmentos a promediar.

### `window`

Ventana aplicada a cada segmento antes de la FFT, para reducir fugas espectrales. `'hann'` es el default y suele bastar; alternativas tipicas: `'hamming'`, `'blackman'`, o `('kaiser', beta)`.

### `scaling`

`'density'` (default) devuelve `V^2/Hz`: la **densidad** integra a la potencia total y es independiente de `nperseg`. `'spectrum'` devuelve `V^2`: potencia concentrada por bin, util para leer la amplitud de tonos discretos.

### `average`

Como combinar los periodogramas de los segmentos: `'mean'` (default) o `'median'`. La mediana es mas **robusta** ante segmentos con transitorios o picos espurios.

## Casos de uso

### Hallar la frecuencia dominante de una señal ruidosa

```python
import numpy as np
from scipy.signal import welch

fs = 2000.0
t = np.arange(0, 10, 1/fs)
# Dos tonos enterrados en ruido
x = (np.sin(2*np.pi*120*t) + 0.3*np.sin(2*np.pi*375*t)
     + 2.0*np.random.randn(t.size))

f, Pxx = welch(x, fs, nperseg=2048)
picos = f[np.argsort(Pxx)[-2:]]
np.sort(picos)   # → ~[120., 375.]   (tonos recuperados pese al ruido)
```

### Potencia total por integracion de la PSD

```python
# La densidad integra a la potencia total (teorema de Parseval)
potencia = np.trapezoid(Pxx, f)
potencia    # → ~varianza de x
```

## Buenas practicas

1. **Pasa siempre `fs`** para que las frecuencias salgan en Hz reales y no normalizadas.
2. Ajusta `nperseg` segun el objetivo: subelo si necesitas separar tonos cercanos, bajalo si la PSD se ve ruidosa.
3. Manten el solape por defecto (50 %) con la ventana Hann; es la combinacion bien condicionada.
4. Usa `scaling='density'` para comparar entre configuraciones; `'spectrum'` solo para leer amplitud de tonos discretos.
5. Cambia a `average='median'` cuando la señal tenga golpes o transitorios que contaminan la media.
6. Desempaqueta la tupla: `f, Pxx = welch(...)`; el primer elemento es el eje de frecuencias, no parte de la potencia.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Frecuencias en `[0, 0.5]` y no en Hz | No se paso `fs` | Pasar `fs` con la tasa de muestreo real |
| PSD muy ruidosa pese a Welch | `nperseg` demasiado grande (pocos segmentos) | Reducir `nperseg` o subir el solape |
| No se distinguen tonos cercanos | `nperseg` demasiado pequeño (baja resolucion) | Aumentar `nperseg` |
| `ValueError: noverlap must be less than nperseg` | Solape >= longitud de segmento | Garantizar `noverlap < nperseg` |
| Tratar el retorno como un solo array | `welch` devuelve `(f, Pxx)` | Desempaquetar la tupla |
| Amplitudes no coinciden con lo esperado | Confusion `density` vs `spectrum` | Elegir el `scaling` acorde a la magnitud buscada |

## Limitaciones

- Asume señal **estacionaria** dentro de cada segmento; para señales cuyo espectro cambia en el tiempo usar `spectrogram`.
- El promediado sacrifica resolucion en frecuencia: no resuelve tonos mas juntos que `fs / nperseg`.
- No devuelve fase, solo potencia; para informacion de fase se necesita la FFT/STFT directa.
- Para una estimacion rapida sin promediar (o didactica) basta `periodogram`, asumiendo mayor varianza.

## Notas relacionadas

- [[scipy.signal.periodogram]]
- [[scipy.signal.spectrogram]]
- [[concepto_relacion_numpy]]
- [[concepto_objetos_resultado]]
