# Zed

Verified against Zed docs (2026): [Skills](https://zed.dev/docs/ai/skills),
[Instructions](https://zed.dev/docs/ai/instructions),
[MCP](https://zed.dev/docs/ai/mcp).

## Install

```bash
./install.sh --zed     # Zed only
./install.sh --all     # Cursor + Zed
./install.sh --check   # reports both targets
```

`install.sh --zed` does **not** run `cursor --install-extension`, does
**not** clone `github.com/cursor/plugins`, and does **not** write
`~/.cursor/plugins/local`. Those are Cursor-only.

## Where things land

| Item | Path | Notes |
|---|---|---|
| Global skills | `~/.agents/skills/<name>` | Official Zed global root. Flat layout only. Symlinks to this clone's `skills/<name>` |
| Project skills | `<worktree>/.agents/skills/` | Trusted worktrees only; this pack does not install here |
| Always-on rules | `~/.config/zed/AGENTS.md` | Personal instructions. `install.sh` appends a marked CBA block if the file already exists |
| MCP | `~/.config/zed/settings.json` → `context_servers` | Settings → AI → MCP Servers |

Zed does **not** scan `~/.cursor/skills`. If Cursor install already
symlinked skills there, `--zed` still adds `~/.agents/skills` links
pointing at the **same** `skills/` bodies (no second copy).

A symlink is the documented way to point Zed at another location.

## MCP (scite)

`./install.sh --zed` (or `--all`) adds this entry when `context_servers`
has no scite server. You still need a scite.ai account; authenticate in
Settings → AI → MCP Servers if the editor prompts. No API key is written.
If `settings.json` has comments the installer will not rewrite, add the
same stub by hand:

```json
{
  "context_servers": {
    "scite": {
      "url": "https://api.scite.ai/mcp"
    }
  }
}
```

Authenticate in the Zed UI if the server requests OAuth. Do not paste
API keys into this repository.

## LaTeX

Install the Zed [LaTeX](https://zed.dev/extensions/latex) extension
(texlab). Build with latexmk from the extension, a terminal, TeXShop, or
Overleaf. LaTeX Workshop (`James-Yu.latex-workshop`) is Cursor/VS Code
only.

Example user setting (optional):

```json
{
  "lsp": {
    "texlab": {
      "settings": {
        "texlab": {
          "build": {
            "onSave": false,
            "executable": "latexmk",
            "args": ["-pdf", "-interaction=nonstopmode", "-synctex=1", "%f"]
          }
        }
      }
    }
  }
}
```

Put `/Library/TeX/texbin` on `PATH` before launching Zed from the Dock,
or set the texlab executable to that full path.

## Limitations

**Works in both (same files)**

- All `SKILL.md` skills (prose, figures, corpus, patched K-Dense,
  library wrappers, `mit-presentation`, C-095)
- `lib/styles.py` and the MIT PowerPoint template
- Python extras via uv (`~/.cba-cursor-skills-venv`)
- MacTeX / latexmk (editor-agnostic)

**Cursor-only (`install.sh` stages them; Zed users skip)**

- Orchestrate, Cursor SDK, Team Kit, Continual Learning
- LaTeX Workshop
- Cursor Customize / `~/.cursor/plugins/local`
- Cursor-specific SKILL frontmatter as Cursor interprets it
  (`allowed-tools`; Zed honors `name`, `description`,
  `disable-model-invocation`)
- Cursor MCP CLI / cloud agents / `/orchestrate`
- Local-plugin-imports admin gate

**Zed gaps**

- Skill catalog is name + description only, capped at **50 KB** total.
  Skills that do not fit are dropped with a UI warning. Keep descriptions
  short; this kitchen sink is large.
- No Team Kit workflows (verify-this, review-and-ship, deslop)
- `.mdc alwaysApply` is Cursor; Zed uses `~/.config/zed/AGENTS.md`
- Hooks, canvases, and Cursor SDK are unavailable
- External Agents and Terminal Threads do not inherit Zed's personal
  `AGENTS.md` unless that CLI reads it itself
- Project-local skills stay dark until you trust the worktree
