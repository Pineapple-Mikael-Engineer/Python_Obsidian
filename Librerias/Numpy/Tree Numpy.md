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
├── 📁 conceptos_transversales/
│   ├── concepto_ndarray
│   ├── concepto_broadcasting.md
│   ├── concepto_vectorizacion.md
│   ├── concepto_shape.md
│   ├── concepto_dtype.md
│   ├── concepto_views_vs_copias.md
│   ├── concepto_indexing.md
│   ├── concepto_contiguidad_memoria.md
│   ├── concepto_ufuncs.md
│   └── concepto_axis_parametro.md
│
├── 📁 np/
│   │
│   ├── 📁 creacion/
│   │   ├── np.array.md
│   │   ├── np.zeros.md
│   │   ├── np.ones.md
│   │   ├── np.empty.md
│   │   ├── np.arange.md
│   │   ├── np.linspace.md
│   │   ├── np.logspace.md
│   │   ├── np.eye.md
│   │   ├── np.identity.md
│   │   ├── np.full.md
│   │   └── np.fromfunction.md
│   │
│   ├── 📁 manipulacion_forma/
│   │   ├── np.reshape.md
│   │   ├── np.ravel.md
│   │   ├── np.transpose.md
│   │   ├── np.moveaxis.md
│   │   ├── np.swapaxes.md
│   │   ├── np.concatenate.md
│   │   ├── np.stack.md
│   │   ├── np.vstack.md
│   │   ├── np.hstack.md
│   │   ├── np.dstack.md
│   │   ├── np.column_stack.md
│   │   ├── np.split.md
│   │   ├── np.vsplit.md
│   │   ├── np.hsplit.md
│   │   ├── np.expand_dims.md
│   │   ├── np.squeeze.md
│   │   ├── np.tile.md
│   │   ├── np.repeat.md
│   │   └── np.roll.md
│   │
│   ├── 📁 seleccion/
│   │   ├── np.where.md
│   │   ├── np.take.md
│   │   ├── np.put.md
│   │   ├── np.clip.md
│   │   ├── np.choose.md
│   │   ├── np.select.md
│   │   └── np.nonzero.md
│   │
│   ├── 📁 operaciones/
│   │   ├── np.add.md
│   │   ├── np.subtract.md
│   │   ├── np.multiply.md
│   │   ├── np.divide.md
│   │   ├── np.power.md
│   │   ├── np.mod.md
│   │   ├── np.log.md
│   │   ├── np.log2.md
│   │   ├── np.log10.md
│   │   ├── np.exp.md
│   │   ├── np.expm1.md
│   │   ├── np.sin.md
│   │   ├── np.cos.md
│   │   ├── np.tan.md
│   │   ├── np.arcsin.md
│   │   ├── np.arccos.md
│   │   ├── np.arctan.md
│   │   ├── np.sinh.md
│   │   ├── np.cosh.md
│   │   ├── np.tanh.md
│   │   ├── np.sqrt.md
│   │   ├── np.square.md
│   │   ├── np.abs.md
│   │   ├── np.fabs.md
│   │   ├── np.sign.md
│   │   └── np.ceil.md
│   │
│   ├── 📁 reducciones/
│   │   ├── np.sum.md
│   │   ├── np.cumsum.md
│   │   ├── np.nancumsum.md
│   │   ├── np.prod.md
│   │   ├── np.cumprod.md
│   │   ├── np.nancumprod.md
│   │   ├── np.diff.md
│   │   ├── np.gradient.md
│   │   ├── np.trapz.md
│   │   ├── np.mean.md
│   │   ├── np.median.md
│   │   ├── np.average.md
│   │   ├── np.std.md
│   │   ├── np.var.md
│   │   ├── np.min.md
│   │   ├── np.max.md
│   │   ├── np.ptp.md
│   │   ├── np.argmin.md
│   │   ├── np.argmax.md
│   │   ├── np.nanmin.md
│   │   ├── np.nanmax.md
│   │   ├── np.nanargmin.md
│   │   ├── np.nanargmax.md
│   │   ├── np.nansum.md
│   │   ├── np.nanmean.md
│   │   ├── np.nanstd.md
│   │   └── np.nanvar.md
│   │
│   ├── 📁 estadisticas/
│   │   ├── np.corrcoef.md
│   │   ├── np.cov.md
│   │   ├── np.histogram.md
│   │   ├── np.histogram2d.md
│   │   ├── np.histogramdd.md
│   │   ├── np.bincount.md
│   │   ├── np.digitize.md
│   │   └── np.percentile.md
│   │
│   ├── 📁 conjuntos/
│   │   ├── np.unique.md
│   │   ├── np.intersect1d.md
│   │   ├── np.union1d.md
│   │   ├── np.setdiff1d.md
│   │   └── np.setxor1d.md
│   │
│   ├── 📁 io/
│   │   ├── np.loadtxt.md
│   │   ├── np.savetxt.md
│   │   ├── np.genfromtxt.md
│   │   ├── np.load.md
│   │   ├── np.save.md
│   │   ├── np.savez.md
│   │   ├── np.savez_compressed.md
│   │   └── np.memmap.md
│   │
│   └── 📁 polinomios/
│       ├── np.poly1d.md
│       ├── np.polyfit.md
│       ├── np.polyval.md
│       ├── np.polyder.md
│       ├── np.polyint.md
│       └── np.roots.md
│
├── 📁 np.ndarray/
│   │
│   ├── 📁 atributos/
│   │   ├── ndarray.shape.md
│   │   ├── ndarray.dtype.md
│   │   ├── ndarray.size.md
│   │   ├── ndarray.ndim.md
│   │   ├── ndarray.itemsize.md
│   │   ├── ndarray.nbytes.md
│   │   ├── ndarray.T.md
│   │   ├── ndarray.real.md
│   │   ├── ndarray.imag.md
│   │   ├── ndarray.flat.md
│   │   ├── ndarray.strides.md
│   │   ├── ndarray.base.md
│   │   ├── ndarray.ctypes.md
│   │   ├── ndarray.data.md
│   │   └── ndarray.flags.md
│   │
│   └── 📁 metodos/
│       │
│       ├── 📁 forma/
│       │   ├── ndarray.reshape.md
│       │   ├── ndarray.ravel.md
│       │   ├── ndarray.flatten.md
│       │   ├── ndarray.transpose.md
│       │   ├── ndarray.swapaxes.md
│       │   └── ndarray.squeeze.md
│       │
│       ├── 📁 seleccion/
│       │   ├── ndarray.take.md
│       │   ├── ndarray.put.md
│       │   ├── ndarray.compress.md
│       │   └── ndarray.nonzero.md
│       │
│       ├── 📁 reducciones/
│       │   ├── ndarray.sum.md
│       │   ├── ndarray.cumsum.md
│       │   ├── ndarray.prod.md
│       │   ├── ndarray.cumprod.md
│       │   ├── ndarray.mean.md
│       │   ├── ndarray.var.md
│       │   ├── ndarray.std.md
│       │   ├── ndarray.min.md
│       │   ├── ndarray.max.md
│       │   ├── ndarray.argmin.md
│       │   ├── ndarray.argmax.md
│       │   ├── ndarray.ptp.md
│       │   ├── ndarray.clip.md
│       │   └── ndarray.round.md
│       │
│       ├── 📁 transformacion/
│       │   ├── ndarray.astype.md
│       │   ├── ndarray.byteswap.md
│       │   ├── ndarray.view.md
│       │   ├── ndarray.copy.md
│       │   └── ndarray.fill.md
│       │
│       └── 📁 serializacion/
│           ├── ndarray.tofile.md
│           ├── ndarray.tolist.md
│           ├── ndarray.tobytes.md
│           ├── ndarray.dump.md
│           └── ndarray.dumps.md
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

