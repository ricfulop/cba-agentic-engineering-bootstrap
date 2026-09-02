#!/usr/bin/env bash
# CBA Agentic Engineering Bootstrap Toolkit installer. macOS-first.
# Idempotent. After first mention, "CBA bootstrap toolkit".
#   ./install.sh          Cursor
#   ./install.sh --zed    Zed
#   ./install.sh --all    both
#   ./install.sh --check  report both targets; exit 1 if core missing
set -euo pipefail

REPO="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_NAME="cba-agentic-engineering-bootstrap"
PLUGIN_NAME_LEGACY="cba-lab-skills"
CURSOR_LOCAL="${HOME}/.cursor/plugins/local"
CURSOR_PLUGIN="${CURSOR_LOCAL}/${PLUGIN_NAME}"
CURSOR_PLUGIN_LEGACY="${CURSOR_LOCAL}/${PLUGIN_NAME_LEGACY}"
CURSOR_SKILLS="${HOME}/.cursor/skills"
ZED_SKILLS="${HOME}/.agents/skills"
ZED_AGENTS="${HOME}/.config/zed/AGENTS.md"
VENV="${HOME}/.cba-cursor-skills-venv"
CACHE="${HOME}/.cache/cba-cursor-skills"
CURSOR_PLUGINS_CACHE="${CACHE}/cursor-plugins"
TEXBIN="/Library/TeX/texbin"
SCITE_HELPER="${REPO}/scripts/scite_mcp.py"
SCITE_URL="https://api.scite.ai/mcp"

DO_CURSOR=1
DO_ZED=0
CHECK_ONLY=0
WITH_MACTEX=0
SKIP_HEAVY="${SKIP_HEAVY:-0}"

usage() {
  cat <<'EOF'
Usage: ./install.sh [--zed|--all|--check] [--with-mactex]

  (default)   Install for Cursor
  --zed       Install for Zed (skills + AGENTS.md; no Cursor plugins)
  --all       Cursor and Zed
  --check     Report present/missing for both targets; exit 1 if core missing
  --with-mactex   brew install --cask mactex-no-gui if latexmk is absent

Environment:
  SKIP_HEAVY=1   Skip pymatgen, fluidsim, pymc
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --zed) DO_CURSOR=0; DO_ZED=1 ;;
    --all) DO_CURSOR=1; DO_ZED=1 ;;
    --check) CHECK_ONLY=1 ;;
    --with-mactex) WITH_MACTEX=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage; exit 2 ;;
  esac
  shift
done

have() { command -v "$1" >/dev/null 2>&1; }

is_link_to() {
  local link="$1" target="$2"
  [[ -L "$link" ]] && [[ "$(readlink "$link")" == "$target" ]]
}

ok() { printf "  [ok]  %s\n" "$1"; }
miss() { printf "  [miss] %s\n" "$1"; }
info() { printf "  [..]  %s\n" "$1"; }

scite_detect() {
  # $1 = cursor|zed → prints present|absent
  python3 "$SCITE_HELPER" "detect-$1" 2>/dev/null || echo "absent"
}

scite_auth_note() {
  info "scite: create a free account at https://scite.ai if you do not have one"
  info "scite: authenticate in the editor MCP UI if prompted (OAuth). No API key is written."
  info "scite: restart the editor after adding the server"
}

ensure_scite_cursor() {
  if [[ "$(scite_detect cursor)" == "present" ]]; then
    echo "scite MCP already configured"
    return 0
  fi
  info "scite MCP absent — adding Streamable HTTP server ${SCITE_URL}"
  added=0
  if have cursor && cursor --help 2>&1 | grep -q -- '--add-mcp'; then
    # Prefer official remote URL (same shape as a working CBA machine).
    if cursor --add-mcp "{\"name\":\"scite\",\"url\":\"${SCITE_URL}\"}" >/dev/null 2>&1; then
      added=1
    fi
  fi
  if [[ "$added" -eq 0 ]]; then
    result="$(python3 "$SCITE_HELPER" merge-cursor 2>/dev/null || echo snippet)"
    case "$result" in
      added|present) added=1 ;;
      snippet)
        info "scite: ~/.cursor/mcp.json has comments; not rewriting. Add this MCP entry:"
        info "  ${SCITE_URL}  (name: scite)"
        ;;
    esac
  fi
  if [[ "$added" -eq 1 ]]; then
    ok "scite MCP added for Cursor (url only; no secrets)"
  fi
  scite_auth_note
}

ensure_scite_zed() {
  if [[ "$(scite_detect zed)" == "present" ]]; then
    echo "scite MCP already configured"
    return 0
  fi
  info "scite MCP absent in Zed — merging context_servers"
  result="$(python3 "$SCITE_HELPER" merge-zed 2>/dev/null || echo snippet)"
  case "$result" in
    present) echo "scite MCP already configured" ;;
    added) ok "scite MCP added for Zed (url only; no secrets)" ;;
    snippet)
      info "scite: Zed settings.json has comments we will not rewrite. Add via Settings → AI → MCP Servers:"
      info "  {\"context_servers\":{\"scite\":{\"url\":\"${SCITE_URL}\"}}}"
      ;;
  esac
  scite_auth_note
}

# ---------------------------------------------------------------------------
# --check
# ---------------------------------------------------------------------------
if [[ "$CHECK_ONLY" -eq 1 ]]; then
  FAIL=0
  echo "CBA Agentic Engineering Bootstrap Toolkit — check"
  echo "repo: $REPO"
  echo
  echo "Core (both editors)"
  if [[ -f "$REPO/.cursor-plugin/plugin.json" ]]; then ok "plugin.json"; else miss "plugin.json"; FAIL=1; fi
  if [[ -f "$REPO/lib/styles.py" ]]; then ok "lib/styles.py"; else miss "lib/styles.py"; FAIL=1; fi
  if [[ -f "$REPO/templates/MIT-PowerPoint-template-Arial-3.pptx" ]]; then
    ok "MIT PowerPoint template"
  else
    miss "MIT PowerPoint template"
    FAIL=1
  fi
  SKILL_N="$(find "$REPO/skills" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')"
  if [[ "$SKILL_N" -ge 30 ]]; then ok "skills/ ($SKILL_N folders)"; else miss "skills/ count $SKILL_N"; FAIL=1; fi
  if have python3; then
    PYV="$(python3 -c 'import sys; print("%d.%d"%sys.version_info[:2])' 2>/dev/null || echo "?")"
    ok "python3 $PYV"
  else
    miss "python3"
    FAIL=1
  fi
  if have uv; then ok "uv"; else miss "uv (install.sh will fetch)"; fi
  if [[ -x "$TEXBIN/latexmk" ]]; then ok "latexmk ($TEXBIN)"; else miss "latexmk ($TEXBIN)"; fi
  if [[ -x "$TEXBIN/pdflatex" ]]; then ok "pdflatex ($TEXBIN)"; else miss "pdflatex ($TEXBIN)"; fi
  echo
  echo "Cursor"
  if have cursor; then ok "cursor CLI"; else miss "cursor CLI — install Cursor from cursor.com"; FAIL=1; fi
  if [[ -e "$CURSOR_PLUGIN/.cursor-plugin/plugin.json" ]]; then
    ok "local plugin $CURSOR_PLUGIN"
  else
    miss "local plugin $CURSOR_PLUGIN"
  fi
  if [[ -d "$CURSOR_SKILLS" ]]; then
    LINKED="$(find "$CURSOR_SKILLS" -maxdepth 1 -type l | wc -l | tr -d ' ')"
    ok "~/.cursor/skills ($LINKED symlinks)"
  else
    miss "~/.cursor/skills"
  fi
  for ext in James-Yu.latex-workshop ms-python.python; do
    if have cursor && cursor --list-extensions 2>/dev/null | grep -qi "$ext"; then
      ok "extension $ext"
    else
      miss "extension $ext"
    fi
  done
  for p in orchestrate cursor-sdk cursor-team-kit continual-learning; do
    if [[ -d "$CURSOR_LOCAL/$p" ]]; then ok "staged plugin $p"; else miss "staged plugin $p"; fi
  done
  if [[ "$(scite_detect cursor)" == "present" ]]; then
    ok "scite Cursor"
  else
    miss "scite Cursor"
  fi
  echo
  echo "Zed"
  if [[ -d "/Applications/Zed.app" || -d "/Applications/Zed Preview.app" ]] || have zed; then
    ok "Zed.app present"
  else
    miss "Zed.app (optional unless you use --zed)"
  fi
  if [[ -d "$ZED_SKILLS" ]]; then
    LINKED="$(find "$ZED_SKILLS" -maxdepth 1 -type l | wc -l | tr -d ' ')"
    ok "~/.agents/skills ($LINKED symlinks)"
  else
    miss "~/.agents/skills"
  fi
  if [[ -f "$ZED_AGENTS" ]] && grep -q "CBA research defaults" "$ZED_AGENTS"; then
    ok "~/.config/zed/AGENTS.md (CBA block)"
  else
    miss "~/.config/zed/AGENTS.md CBA block"
  fi
  if [[ "$(scite_detect zed)" == "present" ]]; then
    ok "scite Zed"
  else
    miss "scite Zed"
  fi
  echo
  if [[ -d "$VENV" ]]; then ok "venv $VENV"; else miss "venv $VENV"; fi
  exit "$FAIL"
fi

echo "CBA Agentic Engineering Bootstrap Toolkit — install"
echo "repo: $REPO"
if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "This script is written for macOS. Continuing anyway."
fi

# ---------------------------------------------------------------------------
# Shared: uv + venv
# ---------------------------------------------------------------------------
if ! have python3; then
  echo "python3 is required." >&2
  exit 1
fi
PY_MAJOR="$(python3 -c 'import sys; print(sys.version_info[0])')"
PY_MINOR="$(python3 -c 'import sys; print(sys.version_info[1])')"
if [[ "$PY_MAJOR" -lt 3 || ( "$PY_MAJOR" -eq 3 && "$PY_MINOR" -lt 12 ) ]]; then
  echo "Python 3.12+ preferred (found ${PY_MAJOR}.${PY_MINOR}). Continuing if uv can pin 3.12."
fi

if ! have uv; then
  info "installing uv"
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="${HOME}/.local/bin:${PATH}"
fi
if ! have uv; then
  echo "uv install failed. Install from https://docs.astral.sh/uv/ and rerun." >&2
  exit 1
fi

info "Python extras → $VENV"
if [[ ! -d "$VENV" ]]; then
  if uv python install 3.12 >/dev/null 2>&1; then
    uv venv --python 3.12 "$VENV"
  else
    uv venv "$VENV"
  fi
fi
# shellcheck disable=SC1091
source "${VENV}/bin/activate"
uv pip install -q matplotlib numpy scipy python-pptx astropy seaborn \
  statsmodels sympy scikit-learn pymoo pyzotero
if [[ "$SKIP_HEAVY" == "1" ]]; then
  info "SKIP_HEAVY=1 — skipped pymatgen, fluidsim, pymc"
else
  uv pip install -q pymatgen pymc || info "heavy extras failed (pymatgen/pymc); continue"
  info "fluidsim is optional/heavy — not installed unless you: uv pip install fluidsim"
fi

# ---------------------------------------------------------------------------
# Shared: LaTeX
# ---------------------------------------------------------------------------
if [[ ! -x "$TEXBIN/latexmk" || ! -x "$TEXBIN/pdflatex" ]]; then
  if [[ "$WITH_MACTEX" -eq 1 ]]; then
    if have brew; then
      info "brew install --cask mactex-no-gui"
      brew install --cask mactex-no-gui
    else
      echo "Homebrew missing; install MacTeX from https://tug.org/mactex/" >&2
    fi
  else
    info "MacTeX not found. Offer: brew install --cask mactex-no-gui"
    info "Re-run with --with-mactex to install it."
  fi
fi

# ---------------------------------------------------------------------------
# Cursor
# ---------------------------------------------------------------------------
if [[ "$DO_CURSOR" -eq 1 ]]; then
  if ! have cursor; then
    echo "cursor CLI not found. Install Cursor from https://cursor.com then rerun." >&2
    exit 1
  fi
  mkdir -p "$CURSOR_LOCAL" "$CURSOR_SKILLS"
  if [[ -e "$CURSOR_PLUGIN_LEGACY" || -L "$CURSOR_PLUGIN_LEGACY" ]]; then
    info "replacing legacy local plugin $PLUGIN_NAME_LEGACY with $PLUGIN_NAME"
    rm -rf "$CURSOR_PLUGIN_LEGACY"
  fi
  info "staging Cursor plugin → $CURSOR_PLUGIN"
  # Copy (not symlink): Cursor may reject plugin trees whose symlink target
  # lives outside ~/.cursor/plugins/local.
  rsync -a --delete \
    --exclude '.git/' --exclude '.venv/' --exclude '__pycache__/' \
    --exclude '.DS_Store' \
    "$REPO/" "$CURSOR_PLUGIN/"

  info "symlinking skills → $CURSOR_SKILLS"
  for skill_dir in "$REPO/skills"/*; do
    [[ -d "$skill_dir" ]] || continue
    name="$(basename "$skill_dir")"
    dest="${CURSOR_SKILLS}/${name}"
    if [[ -e "$dest" && ! -L "$dest" ]]; then
      info "leave existing non-link $dest"
      continue
    fi
    ln -sfn "$skill_dir" "$dest"
  done

  if cursor --list-extensions 2>/dev/null | grep -qi 'James-Yu.latex-workshop'; then
    ok "LaTeX Workshop already installed"
  else
    info "cursor --install-extension James-Yu.latex-workshop"
    cursor --install-extension James-Yu.latex-workshop || info "LaTeX Workshop install failed"
  fi
  if cursor --list-extensions 2>/dev/null | grep -qi 'ms-python.python'; then
    ok "Python extension already installed"
  else
    info "cursor --install-extension ms-python.python"
    cursor --install-extension ms-python.python || info "Python extension install failed"
  fi

  SETTINGS_SNIPPET="${CACHE}/latex-workshop.settings.json"
  mkdir -p "$CACHE"
  cat > "$SETTINGS_SNIPPET" <<EOF
{
  "latex-workshop.latex.tools": [
    {
      "name": "latexmk",
      "command": "${TEXBIN}/latexmk",
      "args": ["-pdf", "-interaction=nonstopmode", "-synctex=1", "-outdir=%OUTDIR%", "%DOC%"]
    }
  ],
  "latex-workshop.latex.outDir": "%DIR%/build",
  "latex-workshop.latex.path": "${TEXBIN}"
}
EOF
  info "LaTeX Workshop snippet written to $SETTINGS_SNIPPET"
  info "Dock-launched Cursor lacks TeX on PATH — launch from a terminal or set latex-workshop.latex.path"

  info "staging Cursor marketplace plugins (no official CLI)"
  mkdir -p "$CACHE"
  if [[ ! -d "${CURSOR_PLUGINS_CACHE}/.git" ]]; then
    git clone --depth 1 https://github.com/cursor/plugins.git "$CURSOR_PLUGINS_CACHE" \
      || info "could not clone cursor/plugins — install from marketplace URLs"
  else
    git -C "$CURSOR_PLUGINS_CACHE" pull --ff-only || true
  fi
  for p in orchestrate cursor-sdk cursor-team-kit continual-learning; do
    src=""
    if [[ -d "${CURSOR_PLUGINS_CACHE}/${p}" ]]; then
      src="${CURSOR_PLUGINS_CACHE}/${p}"
    elif [[ -d "${CURSOR_PLUGINS_CACHE}/plugins/${p}" ]]; then
      src="${CURSOR_PLUGINS_CACHE}/plugins/${p}"
    fi
    if [[ -n "$src" ]]; then
      rsync -a --delete "$src/" "${CURSOR_LOCAL}/${p}/"
      ok "staged $p"
    else
      info "plugin $p not in clone — https://cursor.com/marketplace/cursor/${p}"
    fi
  done
  ensure_scite_cursor
fi

# ---------------------------------------------------------------------------
# Zed
# ---------------------------------------------------------------------------
if [[ "$DO_ZED" -eq 1 ]]; then
  mkdir -p "$ZED_SKILLS" "$(dirname "$ZED_AGENTS")"
  info "symlinking skills → $ZED_SKILLS (Zed global root; not ~/.cursor/skills)"
  for skill_dir in "$REPO/skills"/*; do
    [[ -d "$skill_dir" ]] || continue
    name="$(basename "$skill_dir")"
    dest="${ZED_SKILLS}/${name}"
    if [[ -e "$dest" && ! -L "$dest" ]]; then
      info "leave existing non-link $dest"
      continue
    fi
    ln -sfn "$skill_dir" "$dest"
  done
  MARKER="<!-- BEGIN CBA-LAB-SKILLS -->"
  ENDMARK="<!-- END CBA-LAB-SKILLS -->"
  if [[ -f "$ZED_AGENTS" ]] && grep -q "$MARKER" "$ZED_AGENTS"; then
    ok "Zed AGENTS.md already has CBA block"
  else
    {
      echo
      echo "$MARKER"
      cat "$REPO/zed/AGENTS.md"
      echo "$ENDMARK"
    } >> "$ZED_AGENTS"
    ok "appended CBA block to $ZED_AGENTS"
  fi
  info "Zed does not get Orchestrate / Team Kit / LaTeX Workshop"
  info "Optional: Zed → Extensions → LaTeX  https://zed.dev/extensions/latex"
  ensure_scite_zed
fi

# ---------------------------------------------------------------------------
# Checklist
# ---------------------------------------------------------------------------
echo
echo "======== checklist ========"
echo "  clone kept at: $REPO"
echo "  python venv:   $VENV"
echo "  styles:        $REPO/lib/styles.py"
if [[ "$DO_CURSOR" -eq 1 ]]; then
  echo "  Cursor plugin: $CURSOR_PLUGIN"
  echo "  Cursor skills: $CURSOR_SKILLS (symlinks)"
  echo "  Reload Window, then Customize → enable ${PLUGIN_NAME}"
  echo "  Marketplace: https://cursor.com/marketplace/cursor/orchestrate"
  echo "               https://cursor.com/marketplace/cursor/cursor-sdk"
  echo "               https://cursor.com/marketplace/cursor/cursor-team-kit"
  echo "               https://cursor.com/marketplace/cursor/continual-learning"
  echo "  Dock-launched Cursor lacks TeX on PATH."
fi
if [[ "$DO_ZED" -eq 1 ]]; then
  echo "  Zed skills:    $ZED_SKILLS (symlinks to this clone)"
  echo "  Zed rules:     $ZED_AGENTS"
  echo "  Settings → AI → Skills to confirm. MCP: context_servers (see ZED.md)"
fi
echo "  scite: install adds the MCP URL when missing; you still need a scite.ai account"
echo "  No secrets were written. AGINEER_INPUT_ROOTS was not changed."
echo "==========================="
