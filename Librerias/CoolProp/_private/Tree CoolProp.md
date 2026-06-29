---
title: Tree CoolProp
tags:
  - coolprop
  - meta
draft: true
---

# 🌡️ Tree CoolProp

> Organización **jerárquica por interfaz y rol** en CoolProp. La idea de fondo: el **estado** de un fluido puro queda definido por **dos propiedades independientes**, y a partir de ahí se derivan todas las demás. CoolProp ofrece dos caminos para lo mismo — la función de alto nivel `PropsSI` (una propiedad por llamada) y el objeto de bajo nivel `AbstractState` (fija un estado y consulta muchas) —, y el cálculo lo realiza un **backend** intercambiable (`HEOS`, `IF97`, `REFPROP`, `SRK`...). `✅` = nota creada · sin marca = roadmap pendiente.

---

## 📁 Tipos de notas

| Tipo | Ubicación | Ejemplo |
|------|-----------|---------|
| **Concepto transversal** | `conceptos_transversales/` | `concepto_estado_termodinamico.md` |
| **Función de módulo** | raíz | `CoolProp.PropsSI.md` |
| **Clase / objeto** | raíz | `AbstractState.md` |
| **Método de objeto** | `AbstractState_metodos/`, `Plots/` | `AbstractState.update.md` |
| **Config / constantes** | raíz | `Constants.md` |
| **Backend** | `backends/` | `backend.HEOS.md` |
| **Índice de carpeta** | `index.md` | uno por carpeta |

> Naming API-style: la función con su nombre cualificado (`CoolProp.PropsSI.md`), el método como `<Clase>.<metodo>.md` (`AbstractState.update.md`), el backend como `backend.<NOMBRE>.md`, el concepto como `concepto_<tema>.md`. El nombre del archivo va en ASCII; el contenido, en español con tildes.

---

## 📂 Estructura

```tree
CoolProp/
│
├── index.md                              # ✅ las dos interfaces + classDiagram/flowchart
│
├── 📁 _private/
│   ├── Tree CoolProp.md                  # ✅ este mapa
│   └── Reglas CoolProp.md                # ✅ convenciones de redaccion
│
├── 📁 conceptos_transversales/            # el modelo mental (lo mas importante)
│   ├── index.md                          # mapa de conceptos
│   ├── concepto_estado_termodinamico.md  # 2 propiedades independientes definen el estado
│   ├── concepto_backend.md               # el motor de calculo (HEOS/IF97/REFPROP/SRK) y BACKEND::Fluido
│   └── concepto_propiedades_SI.md        # claves de propiedad y unidades SI estrictas
│
├── CoolProp.PropsSI.md                   # ✅ alto nivel: una propiedad por llamada
├── CoolProp.HAPropsSI.md                 # aire humedo (Humid Air): T, W, RH, h...
├── CoolProp.PhaseSI.md                   # la fase como string ("liquid", "gas"...)
├── CoolProp.get_global_param_string.md   # consultar metadata global (version, fluidos...)
├── CoolProp.set_reference_state.md       # fijar el estado de referencia de h y s
├── CoolProp.get_fluid_param_string.md    # metadata textual de un fluido (CAS, aliases, formula)
├── CoolProp.get_parameter_information.md # info (nombre/unidad) de un parametro por su indice
│
├── AbstractState.md                      # ✅ bajo nivel: fija un estado y consulta mucho
├── Constants.md                          # ✅ PT_INPUTS, iT, iphase_*...
│
├── 📁 AbstractState_metodos/
│   ├── index.md                          # ✅
│   ├── AbstractState.update.md           # ✅ fija el estado con un par de inputs
│   ├── AbstractState.specify_phase.md    # forzar la fase antes de update (evita ambiguedad)
│   ├── AbstractState.rho.md              # ✅
│   ├── AbstractState.hmass.md            # ✅
│   ├── AbstractState.smass.md            # ✅
│   ├── AbstractState.umass.md            # ✅
│   ├── AbstractState.cpmass.md           # ✅
│   ├── AbstractState.cvmass.md           # ✅
│   ├── AbstractState.T.md                # ✅
│   ├── AbstractState.p.md                # ✅
│   ├── AbstractState.Q.md                # ✅
│   ├── AbstractState.phase.md            # ✅
│   ├── AbstractState.first_partial_deriv.md   # ✅
│   ├── AbstractState.second_partial_deriv.md  # ✅
│   ├── AbstractState.set_mass_fractions.md    # ✅
│   ├── AbstractState.set_mole_fractions.md    # ✅
│   ├── AbstractState.get_mass_fractions.md    # ✅
│   ├── AbstractState.get_mole_fractions.md    # ✅
│   ├── AbstractState.saturation_ancillary.md  # ✅
│   └── AbstractState.saturation_pressure.md   # ✅
│
├── 📁 backends/                           # el motor de calculo intercambiable
│   ├── index.md                          # como elegir backend; sintaxis BACKEND::Fluido
│   ├── backend.HEOS.md                   # Helmholtz (por defecto, el mas general)
│   ├── backend.IF97.md                   # agua/vapor IAPWS-IF97 (rapido, estandar industrial)
│   ├── backend.REFPROP.md                # NIST REFPROP (alta precision, requiere licencia)
│   └── backend.SRK.md                    # ecuacion cubica Soave-Redlich-Kwong
│
└── 📁 Plots/
    ├── index.md                          # ✅ diagramas termodinamicos
    ├── PropertyPlot.md                   # ✅ P-h, T-s con isolineas
    ├── PropertyPlot.calc_isolines.md     # ✅
    ├── PropertyPlot.draw_isolines.md     # ✅
    ├── PropertyPlot.show.md              # ✅
    ├── PropertyPlot.savefig.md           # ✅
    └── Common.unit_system.md             # sistemas de unidades del modulo de plots
```

---

## 📊 Roadmap (estado de implementación)

| Bloque | Estado | Prioridad |
|--------|:---:|-----------|
| `index.md` + `AbstractState` + `PropsSI` + `Constants` | ✅ hecho | 🔴 núcleo |
| `AbstractState_metodos/` (19 métodos + index) | ✅ hecho | 🔴 núcleo |
| `Plots/` (PropertyPlot + métodos) | ✅ hecho | 🟡 visualización |
| `conceptos_transversales/` (estado, backend, SI) | ⬜ pendiente | 🔴 modelo mental |
| Funciones de módulo (HAPropsSI, PhaseSI, get_fluid_param_string...) | ⬜ pendiente | 🟠 API de alto nivel |
| `backends/` (HEOS, IF97, REFPROP, SRK) | ⬜ pendiente | 🟠 el motor |
| `AbstractState.specify_phase` + `Plots/Common.unit_system` | ⬜ pendiente | 🟢 detalles |

---

## Notas relacionadas

- [[Reglas CoolProp]]
- [[Estandarizan Directorio Librerias]]

**Chat**: [Chat](https://chat.deepseek.com/a/chat/s/3f9b810d-1e24-4c5b-a6ce-030d7b348583)
