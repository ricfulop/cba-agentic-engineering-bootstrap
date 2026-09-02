"""Locate this plugin's lib/ so figure scripts can import styles.py.

Search order (first hit wins):

1. CBA_STYLES_ROOT (directory that contains styles.py)
2. Walk upward from the current working directory for lib/styles.py
3. ~/.cursor/plugins/local/cba-agentic-engineering-bootstrap/lib
   (legacy: ~/.cursor/plugins/local/cba-lab-skills/lib)
4. This file's own parent (when imported from the clone)

# do not ship personal paths
"""

from __future__ import annotations

import os
from pathlib import Path


def styles_dir() -> Path:
    env = os.environ.get("CBA_STYLES_ROOT")
    if env:
        candidate = Path(env).expanduser()
        if (candidate / "styles.py").is_file():
            return candidate
        if candidate.name != "lib" and (candidate / "lib" / "styles.py").is_file():
            return candidate / "lib"

    here = Path.cwd()
    for parent in [here, *here.parents]:
        lib = parent / "lib"
        if (lib / "styles.py").is_file():
            return lib

    home = Path.home()
    local_plugins = home / ".cursor" / "plugins" / "local"
    for plugin_name in (
        "cba-agentic-engineering-bootstrap",
        "cba-lab-skills",
    ):
        plugin_lib = local_plugins / plugin_name / "lib"
        if (plugin_lib / "styles.py").is_file():
            return plugin_lib

    bundled = Path(__file__).resolve().parent
    if (bundled / "styles.py").is_file():
        return bundled

    raise ImportError(
        "CBA bootstrap toolkit lib/styles.py not found. Run ./install.sh "
        "from the clone, or set CBA_STYLES_ROOT to the directory that "
        "contains styles.py."
    )


def add_styles_to_sys_path() -> Path:
    import sys

    root = styles_dir()
    text = str(root)
    if text not in sys.path:
        sys.path.insert(0, text)
    return root
