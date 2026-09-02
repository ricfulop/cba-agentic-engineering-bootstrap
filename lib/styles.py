"""
styles.py
Publication figure style presets for APS (PRL/PRX/PRB), Nature, and Science.

Consolidated from existing figure scripts across:
  - microscopic-origins-overleaf
  - flash-positron-natcomms-overleaf
  - critical-voltage-overleaf
  - voltivity-repo

Usage:
    from styles import apply_aps_style, apply_nature_style, apply_science_style, OKABE_ITO
    from styles import label_science_panel, save_science_figure, science_double
    apply_science_style()
    fig, ax = plt.subplots(figsize=science_double())
"""

import matplotlib.pyplot as plt

# ═══════════════════════════════════════════════════════════════════════════════
# Okabe-Ito colorblind-safe palette (used across all repos)
# ═══════════════════════════════════════════════════════════════════════════════

OKABE_ITO = {
    "blue":       "#0072B2",
    "vermillion": "#D55E00",
    "orange":     "#E69F00",
    "sky_blue":   "#56B4E9",
    "green":      "#009E73",
    "purple":     "#CC79A7",
    "yellow":     "#F0E442",
    "black":      "#000000",
    "gray":       "#999999",
}

OI = OKABE_ITO  # short alias

# Extended palette for crystal/materials figures
MATERIALS = {
    **OKABE_ITO,
    "zr_blue":    "#4a86c8",
    "o_red":      "#e74c3c",
    "gold":       "#FFD700",
    "metallic":   "#FFB347",
    "light_gray": "#C8C8C8",
    "dark_gray":  "#555555",
    "bg":         "#FAFAFA",
}

# ═══════════════════════════════════════════════════════════════════════════════
# Journal column widths (inches)
# ═══════════════════════════════════════════════════════════════════════════════

# APS (PRL, PRX, PRB, PRMaterials)
APS_SINGLE = (3.375, 3.375)        # 85.7 mm single column
APS_DOUBLE = (6.75, 3.2)           # 171.5 mm double column
APS_DOUBLE_TALL = (6.75, 4.0)
APS_DOUBLE_SHORT = (6.75, 2.4)     # compact 3-panel strip

# Nature family (Nature, Nature Comms, Nature Materials, etc.)
NATURE_SINGLE = (3.5, 2.625)       # 89 mm single column
NATURE_1P5 = (5.35, 3.5)           # 136 mm 1.5-column
NATURE_DOUBLE = (7.08, 4.0)        # 180 mm full width

# Science / AAAS print widths
SCIENCE_SINGLE = (2.24, 1.68)      # 5.7 cm / 1 column
SCIENCE_DOUBLE = (4.76, 3.0)       # 12.1 cm / 2 columns
SCIENCE_TRIPLE = (7.24, 4.0)       # 18.4 cm / 3 columns

# ═══════════════════════════════════════════════════════════════════════════════
# APS / PRL / PRX style
# ═══════════════════════════════════════════════════════════════════════════════

_APS_RCPARAMS = {
    # Fonts: STIX serif stack, no LaTeX dependency
    "text.usetex": False,
    "mathtext.fontset": "stix",
    "font.family": "serif",
    "font.serif": ["STIX", "Times New Roman", "DejaVu Serif"],
    "font.size": 10,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 8,
    "legend.title_fontsize": 8,

    # Axes
    "axes.linewidth": 0.5,
    "axes.formatter.use_mathtext": True,
    "axes.grid": False,

    # Lines
    "lines.linewidth": 0.8,
    "lines.markersize": 4,

    # Ticks: inward, all four sides, minor ticks visible
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.top": True,
    "ytick.right": True,
    "xtick.minor.visible": True,
    "ytick.minor.visible": True,
    "xtick.major.size": 3.5,
    "ytick.major.size": 3.5,
    "xtick.minor.size": 2.0,
    "ytick.minor.size": 2.0,
    "xtick.major.width": 0.5,
    "ytick.major.width": 0.5,
    "xtick.minor.width": 0.4,
    "ytick.minor.width": 0.4,
    "xtick.major.pad": 4,
    "ytick.major.pad": 4,

    # Legend
    "legend.framealpha": 0.9,
    "legend.edgecolor": "0.8",
    "legend.handlelength": 1.2,
    "legend.labelspacing": 0.3,

    # DPI: screen preview at 150, save at 600
    "figure.dpi": 150,
    "savefig.dpi": 600,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,

    # Embed fonts as outlines (required by APS)
    "pdf.fonttype": 42,
    "ps.fonttype": 42,

    # Background
    "figure.facecolor": "white",
    "axes.facecolor": "white",
}

_APS_LATEX_RCPARAMS = {
    **_APS_RCPARAMS,
    "text.usetex": True,
    "font.serif": ["cmr10"],
    "mathtext.fontset": "cm",
}


def apply_aps_style(use_latex=False):
    """Apply APS (PRL/PRX/PRB) figure style.

    Args:
        use_latex: If True, use LaTeX rendering with Computer Modern fonts.
                   Requires a working LaTeX installation.
    """
    if use_latex:
        plt.rcParams.update(_APS_LATEX_RCPARAMS)
    else:
        plt.rcParams.update(_APS_RCPARAMS)


def aps_single():
    """Return APS single-column figsize (3.375 x 3.375 in)."""
    return APS_SINGLE


def aps_double(height=3.2):
    """Return APS double-column figsize (6.75 x height in)."""
    return (6.75, height)


# ═══════════════════════════════════════════════════════════════════════════════
# Nature / Nature Communications style
# ═══════════════════════════════════════════════════════════════════════════════

_NATURE_RCPARAMS = {
    # Fonts: Helvetica/Arial sans-serif, smaller than APS
    "text.usetex": False,
    "mathtext.fontset": "custom",
    "mathtext.rm": "Helvetica",
    "mathtext.it": "Helvetica:italic",
    "mathtext.bf": "Helvetica:bold",
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 7,
    "axes.labelsize": 7,
    "xtick.labelsize": 6,
    "ytick.labelsize": 6,
    "legend.fontsize": 6,

    # Axes: no top/right spines
    "axes.linewidth": 0.5,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.formatter.use_mathtext": True,
    "axes.grid": False,

    # Lines
    "lines.linewidth": 0.8,
    "lines.markersize": 3,

    # Ticks: outward, only bottom/left
    "xtick.direction": "out",
    "ytick.direction": "out",
    "xtick.top": False,
    "ytick.right": False,
    "xtick.minor.visible": True,
    "ytick.minor.visible": True,
    "xtick.major.size": 3.0,
    "ytick.major.size": 3.0,
    "xtick.minor.size": 1.5,
    "ytick.minor.size": 1.5,
    "xtick.major.width": 0.5,
    "ytick.major.width": 0.5,

    # Legend: frameless
    "legend.frameon": False,
    "legend.handlelength": 1.0,
    "legend.labelspacing": 0.25,

    # DPI: 300 for both screen and save
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.02,

    # Embed fonts as outlines
    "pdf.fonttype": 42,
    "ps.fonttype": 42,

    # Background
    "figure.facecolor": "white",
    "axes.facecolor": "white",
}


def apply_nature_style():
    """Apply Nature family (Nature, Nature Comms, etc.) figure style."""
    plt.rcParams.update(_NATURE_RCPARAMS)


def nature_single():
    """Return Nature single-column figsize (3.5 x 2.625 in / 89 mm)."""
    return NATURE_SINGLE


def nature_1p5():
    """Return Nature 1.5-column figsize (5.35 x 3.5 in / 136 mm)."""
    return NATURE_1P5


def nature_double(height=4.0):
    """Return Nature full-width figsize (7.08 x height in / 180 mm)."""
    return (7.08, height)


# ═══════════════════════════════════════════════════════════════════════════════
# Science / AAAS style
# ═══════════════════════════════════════════════════════════════════════════════

_SCIENCE_RCPARAMS = {
    # Science prefers Helvetica and final lettering around 7 pt, never below 5 pt.
    "text.usetex": False,
    "mathtext.fontset": "custom",
    "mathtext.rm": "Helvetica",
    "mathtext.it": "Helvetica:italic",
    "mathtext.bf": "Helvetica:bold",
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 7,
    "axes.labelsize": 7,
    "xtick.labelsize": 6,
    "ytick.labelsize": 6,
    "legend.fontsize": 6,

    # Maximize data area; avoid grid lines and duplicated right/top labels.
    "axes.linewidth": 0.5,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.formatter.use_mathtext": True,
    "axes.grid": False,

    # Science asks for distinguishable solid symbols and legible 0.5 pt lines.
    "lines.linewidth": 0.8,
    "lines.markersize": 6,

    # Keep axes simple. Science discourages minor tick marks in scales.
    "xtick.direction": "out",
    "ytick.direction": "out",
    "xtick.top": False,
    "ytick.right": False,
    "xtick.minor.visible": False,
    "ytick.minor.visible": False,
    "xtick.major.size": 3.0,
    "ytick.major.size": 3.0,
    "xtick.major.width": 0.5,
    "ytick.major.width": 0.5,

    # Simple, compact legends.
    "legend.frameon": False,
    "legend.handlelength": 1.0,
    "legend.labelspacing": 0.25,

    # Science initial submission asks for 300 dpi; revised raster files are 300 dpi minimum.
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.02,

    # Keep text editable/searchable in vector exports.
    "pdf.fonttype": 42,
    "ps.fonttype": 42,

    "figure.facecolor": "white",
    "axes.facecolor": "white",
}


def apply_science_style():
    """Apply Science / AAAS figure style."""
    plt.rcParams.update(_SCIENCE_RCPARAMS)


def science_single(height=1.68):
    """Return Science single-column figsize (2.24 x height in / 5.7 cm)."""
    return (2.24, height)


def science_double(height=3.0):
    """Return Science two-column figsize (4.76 x height in / 12.1 cm)."""
    return (4.76, height)


def science_triple(height=4.0):
    """Return Science three-column figsize (7.24 x height in / 18.4 cm)."""
    return (7.24, height)


# Science panel labels and export defaults (AAAS author instructions, 2025)
SCIENCE_PANEL_FONTSIZE = 10
SCIENCE_MIN_FONTSIZE = 5
SCIENCE_SAVE_KW = {"bbox_inches": "tight", "pad_inches": 0.02, "dpi": 300}


def label_science_panel(ax, label, *, x=0.02, y=0.98, fontsize=SCIENCE_PANEL_FONTSIZE):
    """Add an uppercase bold panel label (A, B, C) in the upper-left corner."""
    ax.text(
        x,
        y,
        str(label).strip().upper(),
        transform=ax.transAxes,
        fontsize=fontsize,
        fontweight="bold",
        va="top",
        ha="left",
        clip_on=False,
    )


def save_science_figure(fig, path, **kwargs):
    """Save with Science defaults: 300 dpi, tight bbox, editable vector fonts."""
    from pathlib import Path

    out = Path(path)
    save_kw = {**SCIENCE_SAVE_KW, **kwargs}
    fig.savefig(out, **save_kw)


def save_science_revision_figures(fig, stem, *, also_tiff=False, **kwargs):
    """Write PDF and EPS for revised-manuscript vector figures.

    Args:
        fig: matplotlib Figure.
        stem: Output path without suffix (e.g. ``figures/Fig1``).
        also_tiff: If True, also write ``stem.tiff`` (raster fallback).
    """
    from pathlib import Path

    base = Path(stem)
    save_science_figure(fig, base.with_suffix(".pdf"), **kwargs)
    save_science_figure(fig, base.with_suffix(".eps"), **kwargs)
    if also_tiff:
        save_science_figure(fig, base.with_suffix(".tiff"), **kwargs)


# ═══════════════════════════════════════════════════════════════════════════════
# APS large-font style (for panels rendered at 0.48\textwidth in LaTeX)
# ═══════════════════════════════════════════════════════════════════════════════

_APS_LARGE_RCPARAMS = {
    **_APS_RCPARAMS,
    "font.size": 22,
    "axes.labelsize": 24,
    "xtick.labelsize": 20,
    "ytick.labelsize": 20,
    "legend.fontsize": 16,
    "axes.linewidth": 1.2,
    "lines.linewidth": 2.0,
    "lines.markersize": 8,
    "xtick.major.size": 6,
    "ytick.major.size": 6,
    "xtick.minor.size": 3,
    "ytick.minor.size": 3,
    "xtick.major.width": 1.0,
    "ytick.major.width": 1.0,
    "figure.dpi": 300,
    "savefig.dpi": 300,
}


def apply_aps_large_style():
    """Apply APS large-font style for panels shrunk via 0.48\\textwidth in LaTeX."""
    plt.rcParams.update(_APS_LARGE_RCPARAMS)


# ═══════════════════════════════════════════════════════════════════════════════
# Convenience: get full rcParams dict for external use
# ═══════════════════════════════════════════════════════════════════════════════

def get_style_dict(style="aps"):
    """Return the rcParams dict for a given style name."""
    styles = {
        "aps": _APS_RCPARAMS,
        "aps_latex": _APS_LATEX_RCPARAMS,
        "aps_large": _APS_LARGE_RCPARAMS,
        "nature": _NATURE_RCPARAMS,
        "science": _SCIENCE_RCPARAMS,
    }
    if style not in styles:
        raise ValueError(f"Unknown style: {style}. Available: {list(styles.keys())}")
    return dict(styles[style])
