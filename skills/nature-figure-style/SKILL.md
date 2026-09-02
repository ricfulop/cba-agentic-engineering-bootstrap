# Nature Figure Style (Nature / Nature Communications / Nature Materials)

Use this skill when creating or editing matplotlib figures for Nature family journals (Nature, Nature Communications, Nature Materials, Nature Physics, etc.), or when the user mentions Nature style, NatComms figures, or Nature-formatted figures.

## How to Apply

```python
from pathlib import Path
import sys

sys.path.insert(0, str(Path.home() / ".cursor/plugins/local/cba-agentic-engineering-bootstrap/lib"))
try:
    from paths import add_styles_to_sys_path
    add_styles_to_sys_path()
except ImportError:
    pass
from styles import apply_nature_style, nature_single, nature_1p5, nature_double, OKABE_ITO

# Apply Nature style before creating any figure
apply_nature_style()

# Use Nature column widths
fig, ax = plt.subplots(figsize=nature_single())    # 3.5 x 2.625 in (89 mm single col)
fig, ax = plt.subplots(figsize=nature_1p5())       # 5.35 x 3.5 in (136 mm 1.5-col)
fig, ax = plt.subplots(figsize=nature_double())    # 7.08 x 4.0 in (180 mm full width)
```

## Key Conventions

- **Fonts:** Helvetica/Arial sans-serif, 7pt body, 7pt axis labels, 6pt tick labels, 6pt legend
- **Ticks:** Outward, bottom/left only — **no top/right spines**
- **DPI:** 300 for both screen and save
- **Column widths:** 89 mm (single), 136 mm (1.5-col), 180 mm (full)
- **Palette:** Okabe-Ito colorblind-safe (`OKABE_ITO` dict)
- **Legend:** Frameless (`legend.frameon=False`)
- **Font embedding:** `pdf.fonttype=42`, `ps.fonttype=42`

## Key Differences from APS

| Property | APS | Nature |
|----------|-----|--------|
| Font family | Serif (STIX/Times) | Sans-serif (Helvetica/Arial) |
| Base font size | 10 pt | 7 pt |
| Ticks | Inward, all sides | Outward, bottom/left only |
| Top/right spines | Visible | Hidden |
| Legend frame | Semi-transparent | None |
| Save DPI | 600 | 300 |
| Single column | 3.375 in (85.7 mm) | 3.5 in (89 mm) |

## Color Palette

```python
from styles import OKABE_ITO as OI
ax.plot(x, y, color=OI["blue"])        # #0072B2
ax.plot(x, y, color=OI["vermillion"])  # #D55E00
ax.plot(x, y, color=OI["green"])       # #009E73
```

## Saving Figures

```python
fig.savefig("figure.pdf", dpi=300, bbox_inches="tight", pad_inches=0.02)
fig.savefig("figure.png", dpi=300, bbox_inches="tight", pad_inches=0.02)
```

## Crystal Structure MCP Tools

For lattice diagrams, use `crystal_mcp` tools with the Nature palette and apply Nature style to any matplotlib post-processing.
