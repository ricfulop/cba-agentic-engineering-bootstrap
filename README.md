<p align="center">
  <img src="brand/cba-logo.svg" alt="MIT Center for Bits and Atoms" width="280">
</p>

# CBA Agentic Engineering Bootstrap Toolkit

Cursor (and Zed) research plugin for colleagues at the MIT Center for Bits
and Atoms. Figures, prose, literature corpus, official MIT decks, and a
patched K-Dense methods subset. Kitchen-sink: core skills plus optional
library wrappers.

Plugin name: `cba-agentic-engineering-bootstrap`.
Author: Ric Fulop / MIT Center for Bits and Atoms.

Public repository: https://github.com/ricfulop/cba-agentic-engineering-bootstrap

New to Cursor? Start at [HOWTO.md](HOWTO.md).

---

## Install

macOS first. Keep this clone; skills are symlinked from it.

```bash
git clone https://github.com/ricfulop/cba-agentic-engineering-bootstrap.git
cd cba-agentic-engineering-bootstrap
./install.sh          # Cursor
./install.sh --zed    # Zed
./install.sh --all    # both
./install.sh --check  # report present / missing (both targets)
```

Kitchen-sink Python extras are the default. Skip the heavy stack with
`SKIP_HEAVY=1 ./install.sh` (skips pymatgen, fluidsim, pymc). Offer MacTeX
with `./install.sh --with-mactex` (not run otherwise).

After a Cursor install: **Reload Window**, then open **Customize** and
confirm `cba-agentic-engineering-bootstrap` plus the staged Cursor
plugins are enabled. On Teams/Enterprise, local plugin imports may be
gated by an admin setting.

After a Zed install: open **Settings → AI → Skills** and confirm the
symlinked skills under `~/.agents/skills/`. Personal always-on rules land
in `~/.config/zed/AGENTS.md` (existing file is appended, not overwritten).

`install.sh` adds the public scite MCP (`https://api.scite.ai/mcp`) when it
is missing — Cursor via `cursor --add-mcp` or `~/.cursor/mcp.json`, Zed
via `context_servers` in `settings.json`. You still need a [scite.ai](https://scite.ai)
account and must authenticate in the editor UI if prompted. No API key is
written. Without scite, `paper-lookup` plus one-pass Crossref still works.

---

## What gets installed

| Piece | Where | Notes |
|---|---|---|
| This plugin | `~/.cursor/plugins/local/cba-agentic-engineering-bootstrap` | Cursor plugin discovery |
| Skills (same tree) | `~/.cursor/skills/<name>` and/or `~/.agents/skills/<name>` | Symlinks to this clone; no duplicated bodies |
| Python extras | `~/.cba-cursor-skills-venv` | matplotlib, numpy, scipy, python-pptx, astropy, seaborn, statsmodels, sympy, scikit-learn, pymoo, pyzotero; pymatgen unless `SKIP_HEAVY` |
| LaTeX Workshop | Cursor extension `James-Yu.latex-workshop` | Cursor only |
| Cursor companion plugins | staged from `github.com/cursor/plugins` into `~/.cursor/plugins/local/` | orchestrate, cursor-sdk, cursor-team-kit, continual-learning — **not vendored in this git repo** |
| Official MIT PPTX | `templates/MIT-PowerPoint-template-Arial-3.pptx` | Academic MIT use only |
| `styles.py` | `lib/styles.py` | Every figure starts here |
| scite MCP | Cursor `mcpServers.scite` / Zed `context_servers.scite` | Added when missing (`https://api.scite.ai/mcp`). Account + UI auth still required |

Marketplace URLs if staging fails:

- https://cursor.com/marketplace/cursor/orchestrate
- https://cursor.com/marketplace/cursor/cursor-sdk
- https://cursor.com/marketplace/cursor/cursor-team-kit
- https://cursor.com/marketplace/cursor/continual-learning

---

## Skills (one tree)

A single `skills/` directory. Cursor plugin layout is the source of truth.
Zed loads the same `SKILL.md` folders from `~/.agents/skills/` (official
global path; Zed does not scan `~/.cursor/skills`).

**Home-grown**

- `manuscript-prose-style` — American English, noun-phrase headings
- `domain-corpus-bootstrap` — corpus before analysis
- `aps-figure-style` / `nature-figure-style` / `science-figure-style`
- `mit-presentation` — official MIT PowerPoint template

**C-095 working practices** (thin skills)

- `verify-before-claiming`
- `prereg-freeze`
- `literature-corpus` (pointer to `domain-corpus-bootstrap`)
- `figure-style` (pointer to APS/Nature/Science + `lib/styles.py`)
- `dual-source-honesty`

**Patched K-Dense** (`skill-author: K-Dense Inc.`, MIT license)

- `scientific-writing`, `scientific-visualization`, `literature-review`
- `paper-lookup`, `citation-management`, `scientific-critical-thinking`
- `statistical-analysis`, `peer-review`
- `scientific-schematics` — **included, with the paper override: no AI
  figures for manuscripts**

**Optional extras (kitchen sink)**

- `astropy`, `pymatgen`, `matplotlib`, `seaborn`, `pymc`, `statsmodels`
- `sympy`, `scikit-learn`, `pymoo`, `fluidsim`, `pyzotero`
- `venue-templates`, `markdown-mermaid-writing`, `scholar-evaluation`
- `research-grants`

---

## After install — research defaults

- **Citations:** scite MCP (install adds it when missing). Do not use web
  search or X as the citation oracle. You still need a scite account.
  Without a working scite login, `paper-lookup` plus a one-pass Crossref
  check still works. Remote URL: `https://api.scite.ai/mcp`.
- **Figures:** `lib/styles.py`. Never bare `plt.figure()`.
- **Prose:** `manuscript-prose-style`. American English unless the venue
  says otherwise.
- **Corpus before analysis.** Verify before claiming. Preregister
  confirmatory protocols. Dual-source honesty (catalog vs bibliography;
  measured vs derived).
- **Affiliation:** Center for Bits and Atoms, Massachusetts Institute
  of Technology.

Always-on copies of those rules:

- Cursor: `rules/cba-research.mdc` (`alwaysApply`)
- Zed: `zed/AGENTS.md` → `~/.config/zed/AGENTS.md`

---

## Cursor vs Zed

| Works in both | Cursor only | Zed gap |
|---|---|---|
| All `SKILL.md` skills | Orchestrate, Cursor SDK, Team Kit, Continual Learning | No Team Kit workflows (verify-this, review-and-ship) |
| `lib/styles.py`, MIT PPTX | LaTeX Workshop | Install the Zed [LaTeX](https://zed.dev/extensions/latex) extension (texlab + latexmk), or build from a terminal / TeXShop / Overleaf |
| Python extras via uv | `~/.cursor/plugins/local` + Customize | 50 KB skill-catalog budget; keep descriptions short |
| MacTeX / latexmk | `cursor --install-extension` | `.mdc alwaysApply` is Cursor; Zed uses `AGENTS.md` |
| scite if you add the MCP | Cursor MCP CLI / cloud agents / `/orchestrate` | MCP is `context_servers` in Zed `settings.json` |

Full table: `ZED.md`.

Dock-launched Cursor lacks TeX on `PATH`. Launch from a terminal or set
`latex-workshop.latex.tools` so `/Library/TeX/texbin` is visible.

---

## Brand and license

MIT marks (template + `brand/` SVGs) are for **MIT-affiliated academic
use**. See `brand/BRAND.md`. The template is MIT official and is **not
relicensed**.

Original CBA / Ric material in this repository is MIT licensed (`LICENSE`).
K-Dense skills remain MIT-licensed with `skill-author: K-Dense Inc.`
See `THIRD_PARTY_NOTICES.md`.
