# CBA research defaults (Zed personal instructions)

Zed loads this file as always-on agent guidance when installed to
`~/.config/zed/AGENTS.md` (see https://zed.dev/docs/ai/instructions).
It is the Zed counterpart of Cursor `rules/cba-research.mdc`.
Cursor `.mdc alwaysApply` is not read by Zed.

- **Figures:** Start with `apply_aps_style()`, `apply_nature_style()`, or
  `apply_science_style()` from the CBA bootstrap toolkit `lib/styles.py`. Never
  bare `plt.figure()`. Colors from `OKABE_ITO` or `MATERIALS`. Sizes from
  the helpers. Captions live in LaTeX, not inside the figure.
- **Prose:** Follow the `manuscript-prose-style` skill. American English
  unless the venue says otherwise. Noun-phrase headings.
- **Citations:** Use scite if configured under Settings → AI → MCP
  Servers (`context_servers`). Never invent DOIs. Web search and X are
  not the citation oracle. Without scite, `paper-lookup` plus one-pass
  Crossref still works.
- **Presentations:** Official MIT PowerPoint template and MIT marks only.
- **Affiliation:** Center for Bits and Atoms, Massachusetts Institute of
  Technology.
- **Honesty:** Corpus before analysis (`domain-corpus-bootstrap`). Verify
  before claiming. Preregister confirmatory protocols. Dual-source
  honesty (catalog vs bibliography; measured vs derived).

Skills live at `~/.agents/skills/` (global) or `<project>/.agents/skills/`
(trusted worktrees only). Zed does not scan `~/.cursor/skills`.
