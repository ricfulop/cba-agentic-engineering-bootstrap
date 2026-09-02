#!/usr/bin/env python3
"""Reference Science/AAAS two-panel line plot. Run from this directory or repo root."""

from __future__ import annotations

import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "lib"
sys.path.insert(0, str(LIB))

import matplotlib.pyplot as plt
import numpy as np

from styles import (
    OKABE_ITO,
    apply_science_style,
    label_science_panel,
    save_science_figure,
    save_science_revision_figures,
    science_double,
)

OUT_DIR = Path(__file__).resolve().parent


def main() -> None:
    apply_science_style()

    x = np.linspace(0, 4 * np.pi, 80)
    fig, axes = plt.subplots(1, 2, figsize=science_double(height=2.2))
    colors = [OKABE_ITO["blue"], OKABE_ITO["vermillion"]]

    for ax, letter, c in zip(axes, "AB", colors):
        ax.plot(x, np.sin(x + (0 if letter == "A" else 1)), color=c, marker="o", markevery=8)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude (a.u.)")
        label_science_panel(ax, letter)

    fig.tight_layout(pad=0.35, w_pad=0.5)

    stem = OUT_DIR / "example_science_double"
    save_science_figure(fig, stem.with_suffix(".pdf"))
    save_science_figure(fig, stem.with_suffix(".png"))
    save_science_revision_figures(fig, stem)
    plt.close(fig)
    print(f"Wrote {stem}.pdf, .png, .eps")


if __name__ == "__main__":
    main()
