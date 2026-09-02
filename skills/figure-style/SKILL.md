---
name: figure-style
description: Pointer to APS, Nature, and Science figure skills plus lib/styles.py. Use when making or editing a publication figure.
---

# Figure style

Load the venue skill, then import `styles.py` from this plugin.

| Venue | Skill |
|---|---|
| APS / PRL / PRX / PRB | `aps-figure-style` |
| Nature family | `nature-figure-style` |
| Science / AAAS | `science-figure-style` |

```python
from pathlib import Path
import sys

# Portable locator — do not hard-code a laptop path.
sys.path.insert(0, str(Path.home() / ".cursor/plugins/local/cba-agentic-engineering-bootstrap/lib"))
try:
    from paths import add_styles_to_sys_path
    add_styles_to_sys_path()
except ImportError:
    pass

from styles import apply_aps_style, apply_nature_style, apply_science_style
from styles import OKABE_ITO, MATERIALS

apply_aps_style()  # or apply_nature_style() / apply_science_style()
```

If `lib` is not on that path, walk upward from the script for
`lib/styles.py`, or set `CBA_STYLES_ROOT`. See `lib/paths.py`.

Never bare `plt.figure()`. Never a raw `figsize=(...)` tuple. Captions
live in LaTeX. K-Dense `style_presets` is not the style source in CBA
trees.
