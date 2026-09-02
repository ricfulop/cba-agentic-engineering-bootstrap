---
name: science-figure-style
description: >-
  Create publication-quality figures for Science and AAAS Science-family journals:
  Helvetica sans-serif, 5.7/12.1/18.4 cm column widths, colorblind-safe palettes,
  column-scatter preference, and revised-manuscript PDF/EPS/TIFF workflow. Use for
  Science submissions, AAAS figure requirements, or matplotlib figures targeting
  Science print layout.
---

# Science / AAAS Figure Style

Canonical implementation: this plugin's `lib/styles.py`
Official AAAS guide (PDF): https://www.science.org/cms/asset/67f37ac8-4d02-4625-8a05-230568cb8323/author_prep_guide_2025.pdf

**Core principle:** Maximize data area; legibility after reduction; captions carry titles and statistics.

---

## Quick reference

| Element | Specification |
|---------|----------------|
| **1 column** | 5.7 cm (2.24 in) |
| **2 columns** | 12.1 cm (4.76 in) |
| **3 columns** | 18.4 cm (7.24 in) |
| **Font** | Helvetica (Arial fallback); sans-serif |
| **Body / axis labels** | ~7 pt final; **never &lt; 5 pt** |
| **Panel labels** | **A, B, C** — uppercase, **bold**, ~10 pt; upper-left |
| **Markers** | Solid symbols ≥ **6 pt** at final size |
| **Lines** | ≥ **0.5 pt** at final size |
| **Ticks** | Major only; **no** minor ticks, **no** grid |
| **Spines** | Bottom + left only |
| **DPI** | 300 (initial and revised raster minimum) |
| **Vector export** | PDF → EPS → AI (revision) |
| **Raster export** | TIFF @ 300 dpi at **final print size** |
| **Display items** | 3–5 main (up to 6 extended online) |
| **Caption max** | ~200 words; **title in caption**, not in figure |

---

## How to apply (matplotlib)

```python
from pathlib import Path
import sys

sys.path.insert(0, str(Path.home() / ".cursor/plugins/local/cba-agentic-engineering-bootstrap/lib"))
try:
    from paths import add_styles_to_sys_path
    add_styles_to_sys_path()
except ImportError:
    pass

import matplotlib.pyplot as plt
from styles import (
    apply_science_style,
    science_single,
    science_double,
    science_triple,
    label_science_panel,
    save_science_figure,
    save_science_revision_figures,
    OKABE_ITO,
)

apply_science_style()

fig, axes = plt.subplots(1, 2, figsize=science_double(height=2.4))
for ax, letter in zip(axes, "AB"):
    ax.plot([0, 1, 2], [0, 1, 0.5], color=OKABE_ITO["blue"], marker="o")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Voltage (V)")
    label_science_panel(ax, letter)

save_science_figure(fig, "fig1.pdf")                    # initial / vector
save_science_revision_figures(fig, "fig1")              # fig1.pdf + fig1.eps
plt.close(fig)
```

### Column widths

```python
fig, ax = plt.subplots(figsize=science_single())   # 2.24 × 1.68 in
fig, ax = plt.subplots(figsize=science_double())   # 4.76 × 3.0 in
fig, ax = plt.subplots(figsize=science_triple())   # 7.24 × 4.0 in
```

Constants: `SCIENCE_SINGLE`, `SCIENCE_DOUBLE`, `SCIENCE_TRIPLE` in `styles.py`.

---

## Science vs Nature vs APS

| Property | Science / AAAS | Nature | APS (PRL/PRX) |
|----------|----------------|--------|---------------|
| Font | Sans (Helvetica) | Sans (Helvetica) | Serif (STIX) |
| Base size | 7 pt | 7 pt | 10 pt |
| Panel labels | **A**, **B** (no parens) | Often lowercase | **(a)**, **(b)** |
| Minor ticks | **Off** | On | On |
| Grid | **Off** | Off | Off |
| Single column | 2.24 in (5.7 cm) | 3.5 in (89 mm) | 3.375 in |
| Save DPI | 300 | 300 | 600 |
| Tick direction | Outward | Outward | Inward (all sides) |

---

## Submission workflow

### Initial manuscript
- Embed figures in `.docx` or combined PDF @ **300 dpi**
- Vector preferred; acceptable: pdf, eps, ai, psd, tif, pict, gif
- **No PowerPoint**

### Revised manuscript
- **One file per figure**, not in Word
- Formats (preference order): PDF, EPS, AI (vector); TIFF (raster ≥ 300 dpi at final size)
- **No upsampling**; keep native-resolution archives
- Inspect every file at **100% zoom** before upload

```python
save_science_revision_figures(fig, "Fig1")   # Fig1.pdf, Fig1.eps
save_science_figure(fig, "Fig2.tiff")        # microscopy raster
```

---

## Layout rules

1. Design at **target column width** from the start — do not scale afterward.
2. **Left-align** composite panels; place panels **close** together.
3. **Do not repeat** shared axis labels across panels.
4. **Do not** add panel **A** on single-panel figures.
5. Legends in **white space** — must not enlarge the figure canvas.
6. Axes must **not extend** beyond data range.
7. **No** duplicate right-hand y-axis labels.

---

## Typography

- Variables: *italic* (`P`, `T`, `μ`); units roman in parentheses: `Pressure (MPa)`
- Capitalize only the **first** word of axis labels (except proper nouns)
- Leading zeros: `0.3` not `.3`
- Large/small axis ranges: powers of ten
- Exponential single values: `6 × 10⁻³` not `6e-03`
- **No colored type**; bold white on dark image regions only
- Vector PDF/EPS: editable text (`pdf.fonttype=42`)

---

## Color and symbols

- Palette: `OKABE_ITO` or `MATERIALS` — colorblind-safe
- **Avoid** red+green, similar hues, grayscale-only group encoding
- Solid markers when possible; `lines.markersize=6` in style preset
- Prefer **hatching** over light screen fills

---

## Graphs and statistics

| Prefer | Avoid |
|--------|-------|
| Column scatter + mean/median + SD/SEM | Bar chart with mean ± error only |
| Individual points visible | `N.S.` in figure (use caption) |
| Narrow, consistent bar widths | Wide or inconsistent bars across figures |
| Square brackets for bar-graph comparisons | Mixing exact P and `*` symbols |

**P values (pick one style per paper):**
- Asterisks: `*` &lt; 0.05, `**` &lt; 0.01, `***` &lt; 0.005 — define in caption
- Exact: `P = 0.02` in figure — **no** symbol for exact values

Report **N**, test, and P in **caption** or main text. Upload underlying data as **`data S1`** (csv/tsv/json/xml).

---

## Images and integrity

- Scale bars on all micrographs; lengths in **caption** (not on image unless essential)
- Separate stitched panels with **lines or gaps**
- Linear adjustments: **whole image/plate** equally
- Nonlinear adjustments: **state in caption**
- No selective enhancement, cropping that hides data, or moving features
- Photoshop: labels on **editable layers**

---

## Captions (legends)

- Bold **title** as first line of caption (not inside figure)
- Panels described in order: **(A)**, **(B)**, …
- ≤ ~200 words; match nomenclature to main text
- Describe **what is shown**, not interpretation (that belongs in Results)

---

## Preflight checklist

- [ ] Width is 2.24 / 4.76 / 7.24 in (or smaller for simple plots/gels)
- [ ] Text ≥ 7 pt, never &lt; 5 pt; panels bold ~10 pt **A, B, C**
- [ ] No grid, no minor ticks, no top/right spines
- [ ] Colorblind-safe; no red/green pairs
- [ ] Vector PDF with editable fonts OR TIFF ≥ 300 dpi at final size
- [ ] Viewed at 100% — balanced labels, lines, markers
- [ ] Caption has title, n, stats, scale-bar lengths
- [ ] Revised: separate files; no PowerPoint / Word embed

---

## Example script

Run the reference composite:

```bash
python skills/science-figure-style/example_figure.py
```

Outputs `example_science_double.pdf` and `.png` in the same directory.

---

## Official sources

- https://www.science.org/content/page/instructions-preparing-initial-manuscript
- https://www.science.org/content/page/instructions-preparing-revised-manuscript
- https://www.science.org/content/page/science-information-authors
- https://www.science.org/content/page/science-signaling-instructions-revised-resubmitted-research (graphs, P values)
