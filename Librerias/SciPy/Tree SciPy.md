---
title: Tree SciPy
draft: true
---

# 🌳 Tree SciPy

> Estructura **jerárquica** por **submódulo** (`scipy.optimize`, `scipy.integrate`, `scipy.stats`…)
> cruzado con **temáticas**. SciPy extiende NumPy: el `ndarray` sigue siendo la base.
> `✅` = nota creada · sin marca = roadmap pendiente.

---

## 📁 Tipos de notas

| Tipo | Ubicación | Ejemplo |
|------|-----------|---------|
| **Concepto transversal** | `conceptos_transversales/` | `concepto_relacion_numpy.md` |
| **Función de submódulo** | `scipy.<sub>/<tematica>/` | `scipy.optimize.minimize.md` |
| **Clase / objeto resultado** | `scipy.<sub>/` | `OptimizeResult.md`, `KDTree.md` |

Naming API-style: `scipy.<submodulo>.<funcion>.md` · clases con el **nombre real de la clase** (`KDTree.md`, `CubicSpline.md`, pero también `rv_continuous.md`, `csr_matrix.md` en minúscula si así se llaman en la API).

---

## 📂 Estructura completa (roadmap)

```tree
SciPy/
│
├── ✅ introduccion.md
│
├── 📁 conceptos_transversales/
│   ├── ✅ concepto_relacion_numpy.md
│   ├── ✅ concepto_import_submodulos.md
│   ├── ✅ concepto_objetos_resultado.md
│   └── ✅ concepto_callbacks_vectorizados.md
│
├── 📁 scipy.optimize/
│   ├── 📁 minimizacion/
│   │   ├── ✅ scipy.optimize.minimize.md
│   │   ├── ✅ scipy.optimize.minimize_scalar.md
│   │   └── ✅ scipy.optimize.linprog.md
│   ├── 📁 raices/
│   │   ├── ✅ scipy.optimize.root.md
│   │   ├── ✅ scipy.optimize.fsolve.md
│   │   ├── ✅ scipy.optimize.brentq.md
│   │   └── ✅ scipy.optimize.newton.md
│   ├── 📁 ajuste/
│   │   ├── ✅ scipy.optimize.curve_fit.md
│   │   └── ✅ scipy.optimize.least_squares.md
│   └── ✅ OptimizeResult.md
│
├── 📁 scipy.integrate/
│   ├── 📁 cuadratura/
│   │   ├── ✅ scipy.integrate.quad.md
│   │   ├── ✅ scipy.integrate.dblquad.md
│   │   ├── ✅ scipy.integrate.simpson.md
│   │   └── ✅ scipy.integrate.trapezoid.md
│   └── 📁 edo/
│       ├── ✅ scipy.integrate.solve_ivp.md
│       └── ✅ scipy.integrate.odeint.md
│
├── 📁 scipy.interpolate/
│   ├── ✅ interp1d.md
│   ├── ✅ CubicSpline.md
│   ├── ✅ scipy.interpolate.griddata.md
│   ├── ✅ scipy.interpolate.splrep_splev.md
│   └── ✅ RegularGridInterpolator.md
│
├── 📁 scipy.stats/
│   ├── 📁 distribuciones/
│   │   ├── ✅ rv_continuous.md
│   │   ├── ✅ scipy.stats.norm.md
│   │   ├── ✅ scipy.stats.t.md
│   │   ├── ✅ scipy.stats.chi2.md
│   │   ├── ✅ scipy.stats.uniform.md
│   │   └── ✅ scipy.stats.binom.md
│   ├── 📁 tests/
│   │   ├── ✅ scipy.stats.ttest_ind.md
│   │   ├── ✅ scipy.stats.ttest_rel.md
│   │   ├── ✅ scipy.stats.chisquare.md
│   │   ├── ✅ scipy.stats.shapiro.md
│   │   └── ✅ scipy.stats.kstest.md
│   ├── 📁 descriptiva/
│   │   ├── ✅ scipy.stats.describe.md
│   │   ├── ✅ scipy.stats.pearsonr.md
│   │   ├── ✅ scipy.stats.spearmanr.md
│   │   └── ✅ scipy.stats.linregress.md
│   └── ✅ scipy.stats.gaussian_kde.md
│
├── 📁 scipy.signal/
│   ├── 📁 filtros/
│   │   ├── ✅ scipy.signal.butter.md
│   │   ├── ✅ scipy.signal.filtfilt.md
│   │   └── ✅ scipy.signal.lfilter.md
│   ├── 📁 convolucion/
│   │   ├── ✅ scipy.signal.convolve.md
│   │   └── ✅ scipy.signal.correlate.md
│   ├── 📁 picos/
│   │   └── ✅ scipy.signal.find_peaks.md
│   └── 📁 espectral/
│       ├── ✅ scipy.signal.welch.md
│       ├── ✅ scipy.signal.periodogram.md
│       └── ✅ scipy.signal.spectrogram.md
│
├── 📁 scipy.ndimage/
│   ├── 📁 filtros/
│   │   ├── ✅ scipy.ndimage.gaussian_filter.md
│   │   ├── ✅ scipy.ndimage.median_filter.md
│   │   └── ✅ scipy.ndimage.uniform_filter.md
│   ├── 📁 morfologia/
│   │   ├── ✅ scipy.ndimage.binary_erosion.md
│   │   └── ✅ scipy.ndimage.binary_dilation.md
│   └── 📁 medidas/
│       ├── ✅ scipy.ndimage.label.md
│       └── ✅ scipy.ndimage.center_of_mass.md
│
├── 📁 scipy.linalg/
│   ├── 📁 basicas/
│   │   ├── ✅ scipy.linalg.solve.md
│   │   ├── ✅ scipy.linalg.inv.md
│   │   └── ✅ scipy.linalg.det.md
│   ├── 📁 descomposiciones/
│   │   ├── ✅ scipy.linalg.lu.md
│   │   ├── ✅ scipy.linalg.qr.md
│   │   ├── ✅ scipy.linalg.svd.md
│   │   ├── ✅ scipy.linalg.cholesky.md
│   │   └── ✅ scipy.linalg.eig.md
│   └── 📁 matriciales/
│       ├── ✅ scipy.linalg.expm.md
│       └── ✅ scipy.linalg.norm.md
│
├── 📁 scipy.special/
│   ├── ✅ scipy.special.gamma.md
│   ├── ✅ scipy.special.erf.md
│   ├── ✅ scipy.special.factorial.md
│   ├── ✅ scipy.special.comb.md
│   └── ✅ scipy.special.jv.md
│
├── 📁 scipy.fft/
│   ├── ✅ scipy.fft.fft.md
│   ├── ✅ scipy.fft.ifft.md
│   ├── ✅ scipy.fft.rfft.md
│   └── ✅ scipy.fft.fftfreq.md
│
├── 📁 scipy.spatial/
│   ├── ✅ scipy.spatial.distance.md
│   ├── ✅ KDTree.md
│   ├── ✅ ConvexHull.md
│   └── ✅ Delaunay.md
│
├── 📁 scipy.sparse/
│   ├── ✅ csr_matrix.md
│   ├── ✅ csc_matrix.md
│   ├── ✅ coo_matrix.md
│   └── ✅ scipy.sparse.operaciones.md
│
└── 📁 scipy.constants/
    ├── ✅ scipy.constants.constantes_fisicas.md
    └── ✅ scipy.constants.find_unit.md
```

---

## 📊 Estado actual de implementación

> Rama **limpia** creada desde el commit de skills (sin notas de otras librerías).
> **Arbol completo: las 87 notas redactadas y validadas con `sync_tree.py`.**

| Submódulo | Plan | Estado |
|-----------|------|--------|
| `conceptos_transversales/` | 4 | ✅ **completo** (modelo mental) |
| `scipy.optimize/` | 10 | ✅ **completo** |
| `scipy.integrate/` | 6 | ✅ **completo** |
| `scipy.interpolate/` | 5 | ✅ **completo** |
| `scipy.stats/` | 16 | ✅ **completo** |
| `scipy.signal/` | 9 | ✅ **completo** |
| `scipy.ndimage/` | 7 | ✅ **completo** |
| `scipy.linalg/` | 10 | ✅ **completo** |
| `scipy.special/` | 5 | ✅ **completo** |
| `scipy.fft/` | 4 | ✅ **completo** |
| `scipy.spatial/` | 4 | ✅ **completo** |
| `scipy.sparse/` | 4 | ✅ **completo** |
| `scipy.constants/` | 2 | ✅ **completo** |
| raíz (`introduccion.md`) | 1 | ✅ **completo** |
| **Total** | **87** | ✅ **arbol completo** |

### Criterio y orden sugerido de relleno

1. **conceptos_transversales** (modelo mental: relación con NumPy, import de submódulos, objetos-resultado).
2. Submódulos de mayor valor para ingeniería: `optimize`, `integrate`, `interpolate`, `linalg`.
3. `stats`, `signal`, `special`, `constants`.
4. `fft`, `spatial`, `sparse`, `ndimage`.

### Notas
- SciPy **extiende** NumPy: muchas funciones reciben/devuelven `ndarray`. Enlazar a conceptos NumPy donde aplique (aunque vivan en otra rama, el wikilink es válido como referencia).
- A diferencia de `np.linalg`, **`scipy.linalg.lu` SÍ existe** (y es más completo).

---

## Notas relacionadas

- [[Estandarizan Directorio Librerias]]
