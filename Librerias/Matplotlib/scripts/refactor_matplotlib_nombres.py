#!/usr/bin/env python3
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "REPORTE_RENOMBRES.md"
EXCLUDED_FILES = {
    "MIGRACION_MAPEO.md",
    "NOTAS_PENDIENTES.md",
    "REPORTE_RENOMBRES.md",
}

# Mapeo explícito solicitado por el usuario.
RENAME_MAP: Dict[str, str] = {
    "Animacion.md": "animation.FuncAnimation.md",
    "Artist.md": "artist.Artist.md",
    "Axes.md": "axes.Axes.md",
    "Colores_Nombres.md": "colors.nombres.md",
    "Colormaps.md": "cm.Colormaps.md",
    "DateFormatter.md": "ticker.DateFormatter.md",
    "Estilos_Linea.md": "lines.linestyle.md",
    "Formatters.md": "ticker.Formatters.md",
    "FuncFormatter.md": "ticker.FuncFormatter.md",
    "LaTeX.md": "text.latex.md",
    "Limites_Escalas.md": "axes.limites_escalas.md",
    "Line2D.md": "lines.Line2D.md",
    "LogNorm.md": "colors.LogNorm.md",
    "Multiples_Leyendas.md": "axes.multiples_leyendas.md",
    "Normalize.md": "colors.Normalize.md",
    "Patch.md": "patches.Patch.md",
    "PathCollection.md": "collections.PathCollection.md",
    "Personalizacion_Leyendas.md": "axes.personalizacion_leyendas.md",
    "Polygon.md": "patches.Polygon.md",
    "QuadContourSet.md": "contour.QuadContourSet.md",
    "Rectangle.md": "patches.Rectangle.md",
    "Text.md": "text.Text.md",
    "TickFormatters.md": "ticker.Formatters.md",
    "ax.axvline.md": "ax.axvline.md",
    "ax.boxplot.md": "ax.boxplot.md",
    "ax.clabel.md": "ax.clabel.md",
    "ax.contourf.md": "ax.contourf.md",
    "ax.ecdf.md": "ax.ecdf.md",
    "ax.set_xlim_ylim.md": "ax.set_xlim_ylim.md",
    "ax.set_xscale_yscale.md": "ax.set_xscale_yscale.md",
    "ax.set_xticklabels.md": "ax.set_xticklabels.md",
    "ax.text.md": "ax.text.md",
    "axhline_axvline.md": "ax.axhline_axvline.md",
    "errorbar.md": "ax.errorbar.md",
    "fig.legend.md": "figure.fig.legend.md",
    "fig.suptitle.md": "figure.fig.suptitle.md",
    "fill_between.md": "ax.fill_between.md",
    "linestyle.md": "lines.linestyle.md",
    "marker.md": "lines.marker.md",
    "np.meshgrid.md": "numpy.meshgrid.md",
    "plt.colorbar.md": "pyplot.plt.colorbar.md",
    "plt.savefig.md": "pyplot.plt.savefig.md",
    "plt.show.md": "pyplot.plt.show.md",
}

# Alias de detección para links con rutas antiguas.
LINK_ALIAS_MAP: Dict[str, str] = {
    "axhline_axvline": "ax.axhline_axvline",
    "errorbar": "ax.errorbar",
    "fill_between": "ax.fill_between",
    "marker": "lines.marker",
    "linestyle": "lines.linestyle",
    "TickLocators": "ticker.Locators",
    "Locators": "ticker.Locators",
}
for old, new in RENAME_MAP.items():
    LINK_ALIAS_MAP[Path(old).stem] = Path(new).stem

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(#[^\]|]+)?(\|[^\]]+)?\]\]")


@dataclass
class ProcessResult:
    path: Path
    links_total: int
    links_updated: int
    links_unresolved: List[str]


def split_frontmatter(text: str) -> Tuple[str, str]:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[4:end], text[end + 5 :]
    return "", text


def parse_simple_yaml(front: str) -> Dict[str, object]:
    data: Dict[str, object] = {}
    key = None
    for raw in front.splitlines():
        if not raw.strip():
            continue
        if raw.startswith("  - ") and key:
            data.setdefault(key, [])
            data[key].append(raw[4:].strip())
            continue
        if ":" in raw:
            k, v = raw.split(":", 1)
            key = k.strip()
            val = v.strip()
            if not val:
                data[key] = []
            elif val == "[]":
                data[key] = []
            elif val.lower() in {"true", "false"}:
                data[key] = val.lower() == "true"
            else:
                data[key] = val
    return data


def dump_frontmatter(data: Dict[str, object]) -> str:
    lines = ["---"]
    ordered = [
        "title",
        "aliases",
        "tags",
        "lib",
        "obj",
        "tipo",
        "retorna",
        "muta_estado",
        "requiere",
        "draft",
    ]
    for k in ordered:
        if k not in data:
            continue
        v = data[k]
        if isinstance(v, list):
            if not v:
                lines.append(f"{k}: []")
            else:
                lines.append(f"{k}:")
                for item in v:
                    lines.append(f"  - {item}")
        else:
            lines.append(f"{k}: {str(v).lower() if isinstance(v, bool) else v}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def infer_tipo(stem: str) -> str:
    if stem.startswith("ax.") or stem.startswith("figure.fig."):
        return "metodo"
    if stem.startswith("plt.") or stem.startswith("pyplot.plt."):
        return "funcion"
    token = stem.split(".")[-1]
    if token[:1].isupper():
        return "clase"
    return "objeto"


def infer_tag(stem: str, tipo: str) -> str:
    if stem.startswith("ax."):
        return "axes/metodos"
    if stem.startswith("plt.") or stem.startswith("pyplot.plt."):
        return "pyplot/funciones"
    if stem.startswith("figure."):
        return "figure/metodos"
    if "." in stem:
        return f"modulo/{stem.split('.', 1)[0]}"
    return f"api/{tipo}"


def normalize_link_target(raw_target: str) -> str:
    base = raw_target.split("/")[-1].strip()
    if not base:
        return raw_target
    return LINK_ALIAS_MAP.get(base, base)


def rewrite_wikilinks(body: str, existing_stems: set[str]) -> Tuple[str, int, int, List[str]]:
    unresolved: List[str] = []
    total = 0
    updated = 0

    def _sub(match: re.Match[str]) -> str:
        nonlocal total, updated
        total += 1
        target = match.group(1)
        anchor = match.group(2) or ""
        alias = match.group(3) or ""
        normalized = normalize_link_target(target)
        if normalized != target:
            updated += 1
        candidate_stem = normalized
        if candidate_stem in existing_stems:
            return f"[[{normalized}{anchor}{alias}]]"
        # Si no existe la nota destino, la reportamos y dejamos el link tal cual quedó normalizado.
        candidate = target.split("/")[-1].strip()
        unresolved_name = candidate_stem if candidate_stem else candidate
        if unresolved_name and unresolved_name not in unresolved:
            unresolved.append(unresolved_name)
        return f"[[{normalized}{anchor}{alias}]]" if normalized != target else match.group(0)

    new_body = WIKILINK_RE.sub(_sub, body)
    return new_body, total, updated, unresolved


def apply_frontmatter(path: Path, front: str) -> str:
    parsed = parse_simple_yaml(front)
    stem = path.stem

    title_desc = "documentación"
    old_title = str(parsed.get("title", "")).strip()
    if "—" in old_title:
        title_desc = old_title.split("—", 1)[1].strip()
    elif old_title:
        title_desc = old_title

    aliases = parsed.get("aliases", parsed.get("alias", []))
    if isinstance(aliases, str):
        aliases = [aliases]
    aliases = list(dict.fromkeys([*(aliases or []), stem]))

    tipo = infer_tipo(stem)
    tags = ["matplotlib", f"api/{tipo}", infer_tag(stem, tipo)]

    out: Dict[str, object] = {
        "title": f"{stem} — {title_desc}",
        "aliases": aliases,
        "tags": tags,
        "lib": "matplotlib",
        "tipo": tipo,
        "draft": bool(parsed.get("draft", False)),
    }

    if stem in {"Tree_Matplotlib", "Tree Matplotlib"}:
        out["draft"] = True

    if tipo == "metodo" and stem.startswith("ax."):
        out["obj"] = "Axes"
    if "obj" in parsed and parsed["obj"]:
        out["obj"] = parsed["obj"]

    if "retorna" in parsed and parsed["retorna"]:
        out["retorna"] = parsed["retorna"]

    out["muta_estado"] = bool(parsed.get("muta_estado", tipo in {"metodo", "funcion"}))

    req = parsed.get("requiere", [])
    if isinstance(req, str):
        req = [req]
    if req == ["[]"]:
        req = []
    out["requiere"] = req

    return dump_frontmatter(out)


def rename_files(md_files: List[Path]) -> List[Tuple[Path, Path]]:
    renamed: List[Tuple[Path, Path]] = []
    for path in md_files:
        new_name = RENAME_MAP.get(path.name)
        if not new_name or new_name == path.name:
            continue
        target = path.with_name(new_name)
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            path.rename(target)
            renamed.append((path, target))
    return renamed


def process_file(path: Path, existing_stems: set[str]) -> ProcessResult:
    text = path.read_text(encoding="utf-8")
    front, body = split_frontmatter(text)
    new_front = apply_frontmatter(path, front)
    new_body, total, updated, unresolved = rewrite_wikilinks(body, existing_stems)
    path.write_text(new_front + new_body, encoding="utf-8")
    return ProcessResult(path=path, links_total=total, links_updated=updated, links_unresolved=unresolved)


def main() -> None:
    md_files = [
        p
        for p in ROOT.rglob("*.md")
        if "Matplotlib_backup" not in p.parts and p.name not in EXCLUDED_FILES
    ]

    renames = rename_files(md_files)

    # Recargar después de renombres.
    md_files = [
        p
        for p in ROOT.rglob("*.md")
        if "Matplotlib_backup" not in p.parts and p.name not in EXCLUDED_FILES
    ]

    existing_stems = {p.stem for p in md_files}
    results: List[ProcessResult] = [process_file(p, existing_stems) for p in sorted(md_files)]

    unresolved_set = sorted({item for r in results for item in r.links_unresolved})

    lines: List[str] = [
        "# Reporte de refactorización de nombres",
        "",
        "## Archivos renombrados físicamente",
        "",
        "| Archivo original | Archivo nuevo |",
        "|------------------|---------------|",
    ]
    if renames:
        for old, new in renames:
            lines.append(f"| {old.relative_to(ROOT)} | {new.relative_to(ROOT)} |")
    else:
        lines.append("| (sin renombres físicos detectados) | - |")

    lines += [
        "",
        "## Archivos procesados",
        "",
        "| Archivo | Wikilinks totales | Wikilinks actualizados |",
        "|---------|-------------------|------------------------|",
    ]
    for r in results:
        lines.append(
            f"| {r.path.relative_to(ROOT)} | {r.links_total} | {r.links_updated} |"
        )

    lines += ["", "## Links sin resolver", ""]
    if unresolved_set:
        for item in unresolved_set:
            lines.append(f"- [[{item}]]")
    else:
        lines.append("- Ninguno")

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Procesados: {len(results)} archivos")
    print(f"Renombrados físicamente: {len(renames)}")
    print(f"Sin resolver: {len(unresolved_set)}")


if __name__ == "__main__":
    main()
