# APS Figure Style (PRL / PRX / PRB / PRMaterials)

Use this skill when creating or editing matplotlib figures for APS journals (Physical Review Letters, Physical Review X, Physical Review B, Physical Review Materials, etc.), or when the user mentions APS style, PRL figures, PRX figures, or publication-quality physics figures.

## How to Apply

```python
from pathlib import Path
import sys

# Portable: walk cwd, ~/.cursor/plugins/local/cba-agentic-engineering-bootstrap/lib, or this clone.
sys.path.insert(0, str(Path.home() / ".cursor/plugins/local/cba-agentic-engineering-bootstrap/lib"))
try:
    from paths import add_styles_to_sys_path
    add_styles_to_sys_path()
except ImportError:
    pass
from styles import apply_aps_style, aps_double, aps_single, OKABE_ITO, MATERIALS

# Apply APS style before creating any figure
apply_aps_style()  # STIX serif, no LaTeX required
# apply_aps_style(use_latex=True)  # Use if LaTeX is available

# Use APS column widths
fig, ax = plt.subplots(figsize=aps_double())       # 6.75 x 3.2 in (double column)
fig, ax = plt.subplots(figsize=aps_single())       # 3.375 x 3.375 in (single column)
fig, ax = plt.subplots(figsize=aps_double(2.4))    # 6.75 x 2.4 in (compact strip)
```

## Key Conventions

- **Fonts:** STIX serif (or Computer Modern with LaTeX), 10pt body, 10pt axis labels, 9pt tick labels, 8pt legend
- **Ticks:** Inward, all four sides (top/right included), minor ticks visible
- **DPI:** 150 screen / 600 save. Always save PDF at 600 DPI with `pdf.fonttype=42`
- **Column widths:** 3.375 in (single), 6.75 in (double)
- **Palette:** Okabe-Ito colorblind-safe (`OKABE_ITO` dict with keys: blue, vermillion, orange, sky_blue, green, purple, yellow, black, gray)
- **For large panels** rendered at `0.48\textwidth`: use `apply_aps_large_style()` with 22pt fonts

## Color Palette

```python
from styles import OKABE_ITO as OI
ax.plot(x, y, color=OI["blue"])        # #0072B2
ax.plot(x, y, color=OI["vermillion"])  # #D55E00
ax.plot(x, y, color=OI["green"])       # #009E73
ax.plot(x, y, color=OI["orange"])      # #E69F00
```

For crystal/materials figures, use `MATERIALS` dict which extends Okabe-Ito with zr_blue (#4a86c8), o_red (#e74c3c), gold (#FFD700), etc.

## Saving Figures

```python
fig.savefig("figure.pdf", dpi=600, bbox_inches="tight", pad_inches=0.05)
fig.savefig("figure.png", dpi=300, bbox_inches="tight", pad_inches=0.05)
```

## Crystal Structure MCP Tools

For lattice diagrams, use `crystal_mcp` tools which automatically use APS-compatible styling:
- `crystal.import_structure` → `crystal.render_lattice` → `crystal.export_tikz`
- Atom colors: `{"Zr": "#4a86c8", "O": "#e74c3c"}` matches the materials palette
