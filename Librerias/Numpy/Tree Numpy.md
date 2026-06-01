---
title: Tree NumPy — Estructura de notas por módulos y temáticas
draft: true
---

# 🌳 Tree NumPy

> Estructura que combina **organización por módulos** (`np`, `np.linalg`, `np.random`) y **temáticas** (`creacion/`, `operaciones/`, `reducciones/`) con anidamiento variable según complejidad.

---

## 📁 Tipos de notas

| Tipo | Ubicación | Ejemplo |
|------|-----------|---------|
| **Concepto** | `conceptos_transversales/` | `broadcasting.md` |
| **Función** | `np/<tematica>/` | `np/creacion/np.array.md` |
| **Método** | `np.ndarray/metodos/<subtematica>/` | `np.ndarray/metodos/forma/ndarray.reshape.md` |
| **Atributo** | `np.ndarray/atributos/` | `ndarray.shape.md` |
| **Submódulo completo** | `np.<submodulo>/` | `np.linalg/`, `np.random/` |

---

## 📂 Estructura completa

```text
NumPy/
│
├── 📁 conceptos_transversales/        (10/10 ✅ completo)
│   ├── ✅ concepto_ndarray.md
│   ├── ✅ concepto_broadcasting.md
│   ├── ✅ concepto_vectorizacion.md
│   ├── ✅ concepto_shape.md
│   ├── ✅ concepto_dtype.md
│   ├── ✅ concepto_views_vs_copias.md
│   ├── ✅ concepto_indexing.md
│   ├── ✅ concepto_contiguidad_memoria.md
│   ├── ✅ concepto_ufuncs.md
│   └── ✅ concepto_axis_parametro.md
│
├── 📁 np/
│   │
│   ├── 📁 creacion/                   (11/11 ✅ completo)
│   │   ├── ✅ np.array.md
│   │   ├── ✅ np.zeros.md
│   │   ├── ✅ np.ones.md
│   │   ├── ✅ np.empty.md
│   │   ├── ✅ np.arange.md
│   │   ├── ✅ np.linspace.md
│   │   ├── ✅ np.logspace.md
│   │   ├── ✅ np.eye.md
│   │   ├── ✅ np.identity.md
│   │   ├── ✅ np.full.md
│   │   └── ✅ np.fromfunction.md
│   │
│   ├── 📁 manipulacion_forma/         (19/19 ✅ completo · subdividida por conveniencia)
│   │   │
│   │   ├── 📁 cambio_forma/
│   │   │   ├── ✅ np.reshape.md
│   │   │   ├── ✅ np.ravel.md
│   │   │   ├── ✅ np.squeeze.md
│   │   │   └── ✅ np.expand_dims.md
│   │   │
│   │   ├── 📁 reordenar_ejes/
│   │   │   ├── ✅ np.transpose.md
│   │   │   ├── ✅ np.moveaxis.md
│   │   │   └── ✅ np.swapaxes.md
│   │   │
│   │   ├── 📁 combinar/
│   │   │   ├── ✅ np.concatenate.md
│   │   │   ├── ✅ np.stack.md
│   │   │   ├── ✅ np.vstack.md
│   │   │   ├── ✅ np.hstack.md
│   │   │   ├── ✅ np.dstack.md
│   │   │   └── ✅ np.column_stack.md
│   │   │
│   │   ├── 📁 dividir/
│   │   │   ├── ✅ np.split.md
│   │   │   ├── ✅ np.vsplit.md
│   │   │   └── ✅ np.hsplit.md
│   │   │
│   │   └── 📁 repetir_desplazar/
│   │       ├── ✅ np.tile.md
│   │       ├── ✅ np.repeat.md
│   │       └── ✅ np.roll.md
│   │
│   ├── 📁 seleccion/                  (7/7 ✅ completo)
│   │   ├── ✅ np.where.md
│   │   ├── ✅ np.take.md
│   │   ├── ✅ np.put.md
│   │   ├── ✅ np.clip.md
│   │   ├── ✅ np.choose.md
│   │   ├── ✅ np.select.md
│   │   └── ✅ np.nonzero.md
│   │
│   ├── 📁 operaciones/                (26/26 ✅ completo · subdividida por conveniencia)
│   │   │
│   │   ├── 📁 aritmeticas/
│   │   │   ├── ✅ np.add.md
│   │   │   ├── ✅ np.subtract.md
│   │   │   ├── ✅ np.multiply.md
│   │   │   ├── ✅ np.divide.md
│   │   │   ├── ✅ np.power.md
│   │   │   └── ✅ np.mod.md
│   │   │
│   │   ├── 📁 trigonometricas/
│   │   │   ├── ✅ np.sin.md
│   │   │   ├── ✅ np.cos.md
│   │   │   ├── ✅ np.tan.md
│   │   │   ├── ✅ np.arcsin.md
│   │   │   ├── ✅ np.arccos.md
│   │   │   ├── ✅ np.arctan.md
│   │   │   ├── ✅ np.sinh.md
│   │   │   ├── ✅ np.cosh.md
│   │   │   └── ✅ np.tanh.md
│   │   │
│   │   ├── 📁 exponenciales_log/
│   │   │   ├── ✅ np.exp.md
│   │   │   ├── ✅ np.expm1.md
│   │   │   ├── ✅ np.log.md
│   │   │   ├── ✅ np.log2.md
│   │   │   ├── ✅ np.log10.md
│   │   │   ├── ✅ np.sqrt.md
│   │   │   └── ✅ np.square.md
│   │   │
│   │   └── 📁 redondeo_signo/
│   │       ├── ✅ np.abs.md
│   │       ├── ✅ np.fabs.md
│   │       ├── ✅ np.sign.md
│   │       └── ✅ np.ceil.md
│   │
│   ├── 📁 reducciones/                (29/29 ✅ completo · subdividida por conveniencia)
│   │   │
│   │   ├── 📁 agregacion/
│   │   │   ├── ✅ np.sum.md
│   │   │   ├── ✅ np.prod.md
│   │   │   ├── ✅ np.cumsum.md
│   │   │   └── ✅ np.cumprod.md
│   │   │
│   │   ├── 📁 promedios/
│   │   │   ├── ✅ np.mean.md
│   │   │   ├── ✅ np.median.md
│   │   │   ├── ✅ np.average.md
│   │   │   ├── ✅ np.std.md
│   │   │   └── ✅ np.var.md
│   │   │
│   │   ├── 📁 extremos/
│   │   │   ├── ✅ np.min.md
│   │   │   ├── ✅ np.max.md
│   │   │   ├── ✅ np.ptp.md
│   │   │   ├── ✅ np.argmin.md
│   │   │   └── ✅ np.argmax.md
│   │   │
│   │   ├── 📁 diferencial/
│   │   │   ├── ✅ np.diff.md
│   │   │   ├── ✅ np.gradient.md
│   │   │   └── ✅ np.trapz.md
│   │   │
│   │   └── 📁 nan_safe/                (12/12 ✅ · variantes que ignoran NaN)
│   │       ├── ✅ np.nansum.md
│   │       ├── ✅ np.nanprod.md
│   │       ├── ✅ np.nancumsum.md
│   │       ├── ✅ np.nancumprod.md
│   │       ├── ✅ np.nanmean.md
│   │       ├── ✅ np.nanmedian.md
│   │       ├── ✅ np.nanstd.md
│   │       ├── ✅ np.nanvar.md
│   │       ├── ✅ np.nanmin.md
│   │       ├── ✅ np.nanmax.md
│   │       ├── ✅ np.nanargmin.md
│   │       └── ✅ np.nanargmax.md
│   │
│   ├── 📁 estadisticas/               (8/8 ✅ completo)
│   │   ├── ✅ np.corrcoef.md
│   │   ├── ✅ np.cov.md
│   │   ├── ✅ np.histogram.md
│   │   ├── ✅ np.histogram2d.md
│   │   ├── ✅ np.histogramdd.md
│   │   ├── ✅ np.bincount.md
│   │   ├── ✅ np.digitize.md
│   │   └── ✅ np.percentile.md
│   │
│   ├── 📁 conjuntos/                  (5/5 ✅ completo)
│   │   ├── ✅ np.unique.md
│   │   ├── ✅ np.intersect1d.md
│   │   ├── ✅ np.union1d.md
│   │   ├── ✅ np.setdiff1d.md
│   │   └── ✅ np.setxor1d.md
│   │
│   ├── 📁 io/                         (8/8 ✅ completo)
│   │   ├── ✅ np.loadtxt.md
│   │   ├── ✅ np.savetxt.md
│   │   ├── ✅ np.genfromtxt.md
│   │   ├── ✅ np.load.md
│   │   ├── ✅ np.save.md
│   │   ├── ✅ np.savez.md
│   │   ├── ✅ np.savez_compressed.md
│   │   └── ✅ np.memmap.md
│   │
│   └── 📁 polinomios/                 (6/6 ✅ completo)
│       ├── ✅ np.poly1d.md
│       ├── ✅ np.polyfit.md
│       ├── ✅ np.polyval.md
│       ├── ✅ np.polyder.md
│       ├── ✅ np.polyint.md
│       └── ✅ np.roots.md
│
├── 📁 np.ndarray/                     (49/49 ✅ completo · objeto base)
│   │
│   ├── 📁 atributos/                  (15/15 ✅)
│   │   ├── ✅ ndarray.shape.md
│   │   ├── ✅ ndarray.dtype.md
│   │   ├── ✅ ndarray.size.md
│   │   ├── ✅ ndarray.ndim.md
│   │   ├── ✅ ndarray.itemsize.md
│   │   ├── ✅ ndarray.nbytes.md
│   │   ├── ✅ ndarray.T.md
│   │   ├── ✅ ndarray.real.md
│   │   ├── ✅ ndarray.imag.md
│   │   ├── ✅ ndarray.flat.md
│   │   ├── ✅ ndarray.strides.md
│   │   ├── ✅ ndarray.base.md
│   │   ├── ✅ ndarray.ctypes.md
│   │   ├── ✅ ndarray.data.md
│   │   └── ✅ ndarray.flags.md
│   │
│   └── 📁 metodos/                    (34/34 ✅)
│       │
│       ├── 📁 forma/
│       │   ├── ✅ ndarray.reshape.md
│       │   ├── ✅ ndarray.ravel.md
│       │   ├── ✅ ndarray.flatten.md
│       │   ├── ✅ ndarray.transpose.md
│       │   ├── ✅ ndarray.swapaxes.md
│       │   └── ✅ ndarray.squeeze.md
│       │
│       ├── 📁 seleccion/
│       │   ├── ✅ ndarray.take.md
│       │   ├── ✅ ndarray.put.md
│       │   ├── ✅ ndarray.compress.md
│       │   └── ✅ ndarray.nonzero.md
│       │
│       ├── 📁 reducciones/
│       │   ├── ✅ ndarray.sum.md
│       │   ├── ✅ ndarray.cumsum.md
│       │   ├── ✅ ndarray.prod.md
│       │   ├── ✅ ndarray.cumprod.md
│       │   ├── ✅ ndarray.mean.md
│       │   ├── ✅ ndarray.var.md
│       │   ├── ✅ ndarray.std.md
│       │   ├── ✅ ndarray.min.md
│       │   ├── ✅ ndarray.max.md
│       │   ├── ✅ ndarray.argmin.md
│       │   ├── ✅ ndarray.argmax.md
│       │   ├── ✅ ndarray.ptp.md
│       │   ├── ✅ ndarray.clip.md
│       │   └── ✅ ndarray.round.md
│       │
│       ├── 📁 transformacion/
│       │   ├── ✅ ndarray.astype.md
│       │   ├── ✅ ndarray.byteswap.md
│       │   ├── ✅ ndarray.view.md
│       │   ├── ✅ ndarray.copy.md
│       │   └── ✅ ndarray.fill.md
│       │
│       └── 📁 serializacion/
│           ├── ✅ ndarray.tofile.md
│           ├── ✅ ndarray.tolist.md
│           ├── ✅ ndarray.tobytes.md
│           ├── ✅ ndarray.dump.md
│           └── ✅ ndarray.dumps.md
│
├── 📁 np.linalg/
│   │
│   ├── 📁 normas_condiciones/
│   │   ├── np.linalg.norm.md
│   │   ├── np.linalg.cond.md
│   │   └── np.linalg.matrix_rank.md
│   │
│   ├── 📁 determinantes/
│   │   ├── np.linalg.det.md
│   │   └── np.linalg.slogdet.md
│   │
│   ├── 📁 inversas/
│   │   ├── np.linalg.inv.md
│   │   └── np.linalg.pinv.md
│   │
│   ├── 📁 eigen/
│   │   ├── np.linalg.eig.md
│   │   ├── np.linalg.eigvals.md
│   │   ├── np.linalg.eigh.md
│   │   └── np.linalg.eigvalsh.md
│   │
│   ├── 📁 descomposiciones/
│   │   ├── np.linalg.svd.md
│   │   ├── np.linalg.qr.md
│   │   ├── np.linalg.lu.md
│   │   └── np.linalg.cholesky.md
│   │
│   ├── 📁 sistemas_ecuaciones/
│   │   ├── np.linalg.solve.md
│   │   ├── np.linalg.tensorsolve.md
│   │   └── np.linalg.lstsq.md
│   │
│   └── 📁 productos/
│       ├── np.linalg.dot.md
│       ├── np.linalg.multi_dot.md
│       ├── np.linalg.matrix_power.md
│       └── np.linalg.matrix_transpose.md
│
├── 📁 np.random/
│   │
│   ├── 📁 semilla_estado/
│   │   ├── np.random.seed.md
│   │   ├── np.random.get_state.md
│   │   └── np.random.set_state.md
│   │
│   ├── 📁 uniformes/
│   │   ├── np.random.rand.md
│   │   ├── np.random.random.md
│   │   ├── np.random.random_sample.md
│   │   ├── np.random.ranf.md
│   │   ├── np.random.sample.md
│   │   └── np.random.uniform.md
│   │
│   ├── 📁 normales/
│   │   ├── np.random.randn.md
│   │   ├── np.random.standard_normal.md
│   │   └── np.random.normal.md
│   │
│   ├── 📁 discretas/
│   │   ├── np.random.randint.md
│   │   ├── np.random.random_integers.md
│   │   ├── np.random.binomial.md
│   │   ├── np.random.poisson.md
│   │   └── np.random.choice.md
│   │
│   ├── 📁 continuas_especiales/
│   │   ├── np.random.exponential.md
│   │   ├── np.random.gamma.md
│   │   ├── np.random.beta.md
│   │   ├── np.random.chisquare.md
│   │   ├── np.random.f.md
│   │   ├── np.random.t.md
│   │   ├── np.random.laplace.md
│   │   ├── np.random.logistic.md
│   │   └── np.random.lognormal.md
│   │
│   └── 📁 permutaciones/
│       ├── np.random.permutation.md
│       └── np.random.shuffle.md
│
├── 📁 np.fft/
│   ├── np.fft.fft.md
│   ├── np.fft.ifft.md
│   ├── np.fft.fft2.md
│   ├── np.fft.ifft2.md
│   ├── np.fft.fftn.md
│   ├── np.fft.ifftn.md
│   ├── np.fft.rfft.md
│   ├── np.fft.irfft.md
│   ├── np.fft.hfft.md
│   ├── np.fft.ihfft.md
│   ├── np.fft.fftfreq.md
│   ├── np.fft.rfftfreq.md
│   ├── np.fft.fftshift.md
│   ├── np.fft.ifftshift.md
│   └── np.fft.fft.md
│
├── 📁 np.ma/
│   ├── np.ma.masked_where.md
│   ├── np.ma.masked_equal.md
│   ├── np.ma.masked_invalid.md
│   ├── np.ma.masked_inside.md
│   ├── np.ma.masked_outside.md
│   ├── np.ma.filled.md
│   ├── np.ma.compress.md
│   ├── np.ma.fix_invalid.md
│   └── np.ma.getmask.md
│
├── 📁 np.polynomial/
│   ├── np.polynomial.Polynomial.md
│   ├── np.polynomial.Legendre.md
│   ├── np.polynomial.Chebyshev.md
│   ├── np.polynomial.Hermite.md
│   ├── np.polynomial.Laguerre.md
│   └── np.polynomial.polyval.md
│
└── 📁 np.testing/
    ├── np.testing.assert_equal.md
    ├── np.testing.assert_almost_equal.md
    ├── np.testing.assert_allclose.md
    ├── np.testing.assert_array_equal.md
    ├── np.testing.assert_array_almost_equal.md
    └── np.testing.assert_string_equal.md
```

---

## 📊 Estado actual de implementación

> Sincronizado con el disco. `✅` = nota creada · sin marca = esqueleto pendiente.
> El resto del árbol es el **plan/roadmap** de la librería.

| Carpeta | Existentes | Plan | Estado |
|---------|-----------|------|--------|
| `conceptos_transversales/` | 10 | 10 | ✅ núcleo completo |
| `np/creacion/` | 11 | 11 | ✅ completo |
| `np/manipulacion_forma/` | 19 | 19 | ✅ completo (subdividida) |
| `np/reducciones/` | 29 | 29 | ✅ completo (subdividida, incl. `nan_safe/`) |
| `np/seleccion/` | 7 | 7 | ✅ completo |
| `np/operaciones/` | 26 | 26 | ✅ completo (subdividida en 4 ufunc-grupos) |
| `np/estadisticas/` | 8 | 8 | ✅ completo |
| `np/conjuntos/` | 5 | 5 | ✅ completo |
| `np/io/` | 8 | 8 | ✅ completo |
| `np/polinomios/` | 6 | 6 | ✅ completo |
| `np.ndarray/` (atributos+métodos) | 49 | 49 | ✅ completo (15 atrib + 34 métodos) |
| **Total** | **178** | — | — |
|  | | | **🎉 namespace `np/` + objeto `np.ndarray` COMPLETOS** |

### Notas existentes

```text
conceptos_transversales/  → COMPLETO (10): ndarray, broadcasting, vectorizacion, shape, dtype,
                            views_vs_copias, indexing, contiguidad_memoria, ufuncs, axis_parametro
np/creacion/              → COMPLETO (11): array, zeros, ones, empty, full, arange, linspace,
                            logspace, eye, identity, fromfunction
np/manipulacion_forma/    → COMPLETO (19): cambio_forma, reordenar_ejes, combinar, dividir, repetir_desplazar
np/reducciones/           → COMPLETO (29): agregacion, promedios, extremos, diferencial, nan_safe
np/seleccion/             → COMPLETO (7): where, take, put, clip, choose, select, nonzero
np/operaciones/           → COMPLETO (26): aritmeticas, trigonometricas, exponenciales_log, redondeo_signo
np/estadisticas/          → COMPLETO (8): corrcoef, cov, histogram, histogram2d, histogramdd, bincount, digitize, percentile
np/conjuntos/             → COMPLETO (5): unique, intersect1d, union1d, setdiff1d, setxor1d
np/io/                    → COMPLETO (8): loadtxt, savetxt, genfromtxt, load, save, savez, savez_compressed, memmap
np/polinomios/            → COMPLETO (6): poly1d, polyfit, polyval, polyder, polyint, roots
np.ndarray/atributos/     → COMPLETO (15): shape, dtype, size, ndim, itemsize, nbytes, T, real, imag, flat, strides, base, ctypes, data, flags
np.ndarray/metodos/       → COMPLETO (34): forma(6), seleccion(4), reducciones(14), transformacion(5), serializacion(5)
```

### Cambios de estructura aplicados

- `manipulacion_forma/` se **subdividió** en `cambio_forma/`, `reordenar_ejes/`, `combinar/`,
  `dividir/` y `repetir_desplazar/` (19 funciones en plano era difícil de navegar).
- `reducciones/` se **subdividió** en `agregacion/`, `promedios/`, `extremos/`, `diferencial/`
  y `nan_safe/`. El bloque `nan_safe/` agrupa todas las variantes `nan*` que ignoran NaN;
  se añadieron `np.nanprod` y `np.nanmedian` (no estaban en el plano original) → 29 notas.
- `operaciones/` se **subdividió** en `aritmeticas/`, `trigonometricas/`, `exponenciales_log/`
  y `redondeo_signo/` (26 ufuncs en plano). Todas etiquetadas como `transformaciones` (dominio).
- Corregido el wikilink `concepto_dtype_sistema` → `concepto_dtype` (canónico) en `concepto_ndarray`.

---

