# How to use this toolkit

You have never used Cursor. That is fine. After `./install.sh`, you have an
editor that can help you write papers, make journal figures, build a literature
corpus, and compile LaTeX — if you open a project folder and talk to the
agent in plain English.

A **skill** is a recipe the agent reads. It is not an app and not a menu.
Most of this pack **auto-fires** when the request matches (figures, prose,
citations). You can also type `/name` in chat.

**LaTeX Workshop does not log into Overleaf.** It compiles on your Mac.
Overleaf stays in sync through **Git** (Overleaf git URL, or Overleaf ↔
GitHub). There is no login button.

## What you get

The pack does four jobs:

| Job | What you say | What actually runs |
|---|---|---|
| Write or edit paper prose | “Draft the methods” / “Americanize this” / “unslop this” | `manuscript-prose-style`, `scientific-writing` |
| Make a publication figure | “APS figure of …” / “Nature-style plot” | `figure-style` + `lib/styles.py` |
| Become an expert in a topic | “Exhaustive literature on X” / “what should we read?” | `domain-corpus-bootstrap`, `paper-lookup`, scite |
| MIT slides | “Make a CBA talk from these bullets” | `mit-presentation` + the official MIT template |

It also installs **LaTeX Workshop** so `.tex` files compile and show a PDF
in Cursor, and it adds the **scite** citation server if you do not already
have it. You still need a free [scite.ai](https://scite.ai) account and
must sign in once in the editor if prompted.

It does **not** replace Overleaf. Overleaf can stay the place the paper
lives. Cursor is where the agent edits and where you compile a local PDF
to check the result.

## One-time setup

1. Install [Cursor](https://cursor.com) and open it.
2. In Terminal:

```bash
git clone https://github.com/ricfulop/cba-agentic-engineering-bootstrap.git
cd cba-agentic-engineering-bootstrap
./install.sh
```

3. In Cursor: **Command Palette** (`Cmd+Shift+P`) → **Developer: Reload Window**.
4. **Cursor Settings → Customize** (or the puzzle-piece / plugins panel).
   Confirm **CBA Agentic Engineering Bootstrap Toolkit** is enabled, plus the
   staged companion plugins (Orchestrate, Cursor SDK, Team Kit, Continual
   Learning).
5. Sign in to scite if the MCP panel asks.
6. Install MacTeX if `./install.sh --check` says TeX is missing
   (`./install.sh --with-mactex`, or the [MacTeX](https://www.tug.org/mactex/)
   installer). Without it, LaTeX Workshop cannot build a PDF.

Dock-launched Cursor often cannot see TeX. Either launch Cursor from a
terminal (`open -a Cursor`) or follow the PATH note at the end of this
page.

## Cursor in five minutes

**Open a folder, not a single file.** `File → Open Folder…` and pick the
paper or project directory (the one with `main.tex` or `paper/`). Skills
and LaTeX Workshop attach to that folder.

**Chat is how you invoke everything.** `Cmd+L` (or the chat icon). Type a
normal request. That *is* how you use skills. You do not install them one
by one, and you do not run them from a Skills menu.

Two ways a skill runs:

1. **Automatic.** You say “make an APS figure of the residual plot.” The
   agent reads the skill description, opens `aps-figure-style` /
   `figure-style`, and uses `styles.py`. You never typed a slash.
2. **By name.** In chat, type `/` and the skill name, then your request:

```text
/manuscript-prose-style  Pass this section for American English and noun-phrase headings.
/domain-corpus-bootstrap  Become an expert in photonic cophasing. Offer the corpus first.
/mit-presentation  Five-slide CBA group talk from notes.md
/verify-before-claiming  Check the claims in this abstract against the figures.
```

The `/` menu is autocomplete. If you forget the name, just describe the
job.

**Ask vs Agent.** Ask mode answers and will not edit files. Agent mode can
write `.tex`, `.py`, and figures. For “do the work,” use Agent.

**Always say the venue and the file.** “Edit `paper/latex/main.tex` for
Physical Review E” is enough for the prose and figure skills to pick the
right house style.

## First day — four requests that exercise the pack

Open your project folder, `Cmd+L`, Agent mode:

1. *“Read `paper/latex/main.tex`. List the undefined citations and the
   figures that are not on disk.”*
2. *“Draft a 200-word methods paragraph on [X]. American English,
   noun-phrase headings, no em dashes.”*
3. *“Make an APS double-column figure from `data/residuals.csv`. Use
   styles.py. Save PDF+PNG next to the tex.”*
4. *“We are starting a new topic: [X]. Offer the literature corpus
   bootstrap before any analysis.”*

If the agent skips the corpus offer on a new topic, say
`/domain-corpus-bootstrap`. If it invents a DOI, say “use scite, one
pass, do not loop.”

## Connect LaTeX Workshop to Overleaf

LaTeX Workshop compiles **on your laptop**. Overleaf compiles **in the
cloud**. They share the project through **Git**. There is no “log
Workshop into Overleaf” button.

```text
Overleaf  ←→  Git (Overleaf git or GitHub)  ←→  folder on your Mac  ←→  Cursor + LaTeX Workshop
```

### A. Give the Overleaf project a Git remote

Pick one.

**Overleaf Git** (simplest if your Overleaf plan includes it):

1. Open the project on Overleaf.
2. **Menu → Git**.
3. Copy the URL (`https://git.overleaf.com/…`). Keep the Overleaf git
   token; you will use it once as the password.

**Overleaf ↔ GitHub** (what many CBA papers already use):

1. Overleaf: Account → GitHub, authorize.
2. Project **Menu → GitHub → Sync** (or create the GitHub repo from
   there).
3. Clone that GitHub repo locally. Overleaf and GitHub stay copies of
   each other.

If the project is a **GitHub submodule** pointing at a manuscript repo
(FLARE’s layout): clone the parent with `--recurse-submodules`, then
treat `overleaf-manuscript/` as the TeX root. Pushing “to Overleaf” only
works if `origin` in *that* folder is the Overleaf bridge, not the
GitHub mirror. Check with `git remote -v` inside the manuscript folder.

### B. Clone onto the Mac and open it in Cursor

```bash
git clone <overleaf-or-github-url> my-paper
cd my-paper
open -a Cursor .
```

`File → Open Folder…` on `my-paper` if Cursor is already running.

### C. Point LaTeX Workshop at MacTeX

`install.sh` already installs the **LaTeX Workshop** extension
(`James-Yu.latex-workshop`). You still need the TeX binaries on PATH.

In Cursor: `Cmd+Shift+P` → **Preferences: Open User Settings (JSON)**.
Add (or merge):

```json
{
  "latex-workshop.latex.tools": [
    {
      "name": "latexmk",
      "command": "/Library/TeX/texbin/latexmk",
      "args": [
        "-synctex=1",
        "-interaction=nonstopmode",
        "-file-line-error",
        "-pdf",
        "-outdir=%OUTDIR%",
        "%DOC%"
      ]
    }
  ],
  "latex-workshop.latex.recipes": [
    { "name": "latexmk", "tools": ["latexmk"] }
  ],
  "latex-workshop.latex.outDir": "%DIR%/build",
  "latex-workshop.view.pdf.viewer": "tab"
}
```

`%DIR%/build` keeps `.aux` / `.log` out of the source tree (same idea as
FLARE’s scratch outDir). If your project already has a `.latexmkrc` and a
`.vscode/settings.json` `outDir`, **do not fight them** — use those.

Confirm TeX:

```bash
/Library/TeX/texbin/latexmk -v
```

If that fails, MacTeX is not installed.

### D. Build and preview

1. Open the root `.tex` (`main.tex`, `flare_paper.tex`, …).
2. Green play button in the TeX toolbar, or `Cmd+Option+B`, or
   `Cmd+Shift+P` → **LaTeX Workshop: Build with recipe**.
3. PDF opens in a tab. Click a line in the TeX → jump in the PDF
   (SyncTeX).

A clean compile is not enough: open the PDF and check that every figure
is on a page and no `\c…` / `\ref` printed as raw text.

### E. Send local edits back to Overleaf

```bash
git add paper/latex/main.tex   # explicit paths, not git add -A
git commit -m "…"
git push origin main
```

If `origin` is Overleaf, the project updates there. If `origin` is
GitHub and Overleaf is synced to that repo, Overleaf pulls on the next
sync (sometimes you must click **GitHub → Pull** in the Overleaf menu).

**Do not edit the same paragraph on Overleaf and in Cursor without
pulling first.** Overleaf’s next sync can overwrite you. For FLARE-style
papers, the rule is: prose and numbers on Overleaf, or pull immediately
after an Overleaf session before the agent touches the file.

### F. What usually goes wrong

| Symptom | Cause | Fix |
|---|---|---|
| Workshop: `latexmk: command not found` | Dock-launched Cursor has no TeX PATH | Use `/Library/TeX/texbin/latexmk` in settings, or `open -a Cursor` from a terminal |
| Recipe runs but PDF is empty / stale | `outDir` does not match what you opened | Open the PDF Workshop wrote (`build/main.pdf`), not an old copy |
| `git push` goes to GitHub, Overleaf unchanged | `origin` is the mirror | `git remote -v`; add/use the Overleaf remote; or click Overleaf → GitHub → Pull |
| Agent edits the submodule, Overleaf overwrites tomorrow | Pushed to GitHub, not Overleaf | Push the manuscript remote that Overleaf actually tracks |
| Overleaf Git asks for a password | Token, not your Overleaf login | Overleaf Menu → Git → copy the git token |

## Invoking skills — full cheat sheet

Type `/` in Cursor chat (`Cmd+L`) then the name, or just say the job.
Most pack skills auto-fire when the request matches. Companion plugins
below are **Cursor only** (Zed does not get them).

Zed: same `skills/` names after `./install.sh --zed`. Zed has no LaTeX
Workshop; use the Zed LaTeX extension or Overleaf in the browser for the
PDF.

### This pack (`skills/`)

#### Home-grown

| `/name` | When to use it |
|---|---|
| `/manuscript-prose-style` | Language / de-AI pass: American English, noun-phrase headings, machine-generation tells |
| `/domain-corpus-bootstrap` | New topic: build a reproducible, legally acquired literature corpus before analysis |
| `/aps-figure-style` | Matplotlib figures for APS / Physical Review journals |
| `/nature-figure-style` | Matplotlib figures for Nature-family journals |
| `/science-figure-style` | Matplotlib figures for Science / AAAS (column widths, Helvetica, export workflow) |
| `/figure-style` | Pointer to APS / Nature / Science plus `lib/styles.py` — any publication figure |
| `/mit-presentation` | Academic PowerPoint from the official MIT Arial template (CBA talks, course slides) |

#### C-095 working practices

| `/name` | When to use it |
|---|---|
| `/verify-before-claiming` | Check a number, status, or citation against generating code or a live source before writing it |
| `/prereg-freeze` | Hash-bound preregistration before a confirmatory run; record a deviation |
| `/literature-corpus` | Pointer to `domain-corpus-bootstrap` — new topic, “what should we read,” corpus build |
| `/dual-source-honesty` | Keep fetch-time catalogs distinct from corrected bibliographies; measured vs derived vs estimated |

#### Patched K-Dense

| `/name` | When to use it |
|---|---|
| `/scientific-writing` | Draft a manuscript in full paragraphs (IMRAD, citations, reporting guidelines) |
| `/scientific-visualization` | Design or audit publication figures (layout, uncertainty, color, journal export) |
| `/literature-review` | Systematic review / synthesis across academic databases (scite first; one-pass Crossref if scite is down) |
| `/paper-lookup` | Find a paper, DOI, abstract, or OA PDF (scite if signed in; else one-pass Crossref) |
| `/citation-management` | Extract metadata, validate citations, emit BibTeX |
| `/scientific-critical-thinking` | Evaluate claims and evidence quality (design, bias, GRADE) — not formal review writing |
| `/statistical-analysis` | Choose tests, check assumptions, report results; for model classes use `/statsmodels` |
| `/peer-review` | Write a structured manuscript or grant review with a checklist |
| `/scientific-schematics` | Board-slide / early-review cartoons only. **No AI figures for journal manuscripts** — final figures are `lib/styles.py` |

#### Kitchen-sink extras

| `/name` | When to use it |
|---|---|
| `/astropy` | Units, coordinates, FITS, WCS, time, cosmology in Python |
| `/pymatgen` | Crystal structures, phase diagrams, Materials Project, format conversion |
| `/matplotlib` | Low-level plot control; for journal styling prefer `/figure-style` |
| `/seaborn` | Quick statistical plots (distributions, heatmaps, categorical) |
| `/pymc` | Bayesian models, MCMC, posterior checks |
| `/statsmodels` | OLS / GLM / mixed / ARIMA with diagnostics; for test *selection* use `/statistical-analysis` |
| `/sympy` | Exact symbolic math (algebra, calculus, codegen) |
| `/scikit-learn` | Supervised / unsupervised learning, pipelines, model evaluation |
| `/pymoo` | Multi-objective optimization (NSGA-II/III, Pareto fronts) |
| `/fluidsim` | CFD in Python (Navier–Stokes, shallow water, turbulence) |
| `/pyzotero` | Read/write a Zotero library via the Web API |
| `/venue-templates` | LaTeX / formatting requirements for journals, conferences, posters, grants |
| `/markdown-mermaid-writing` | Markdown documents and Mermaid diagrams as the default text figure |
| `/scholar-evaluation` | Score a paper with the ScholarEval rubric |
| `/research-grants` | NSF / NIH / DOE / DARPA proposal structure, review criteria, budget |

35 skills in `skills/` (every folder on disk).

### Cursor companion plugins (Cursor only)

`install.sh` stages these from `github.com/cursor/plugins` into
`~/.cursor/plugins/local/`. They are **not** in this git repo and **not**
available in Zed. Type `/` then the name. Marketplace fallbacks are in
the README.

#### Orchestrate

`/orchestrate` runs **only** when you type `/orchestrate <goal>`. It does
not auto-fire. It fans out Cursor cloud agents. Needs a personal
`CURSOR_API_KEY` from [Cursor Dashboard → Integrations](https://cursor.com/dashboard/integrations).

| `/name` | When to use it |
|---|---|
| `/orchestrate` | You typed `/orchestrate <goal>` and want a tree of parallel cloud agents. Never implied; never autonomous |

#### Cursor SDK

| `/name` | When to use it |
|---|---|
| `/cursor-sdk` | Writing scripts, CI, or bots against `@cursor/sdk` / cloud agents |

#### Cursor Team Kit

| `/name` | When to use it |
|---|---|
| `/verify-this` | Falsify a claim with fresh local evidence (VERIFIED / NOT VERIFIED / INCONCLUSIVE) |
| `/review-and-ship` | Review this branch, test, commit, open or update a PR |
| `/deslop` | Strip AI-generated code slop and clean style |
| `/fix-ci` | Find failing PR checks, read logs, apply a focused fix |
| `/check-compiler-errors` | Run compile / type-check and report failures |
| `/run-smoke-tests` | Run Playwright smoke tests, debug, confirm the fix |
| `/control-cli` | Harness an interactive CLI / TUI locally (startup, hangs, prompt flows) |
| `/control-ui` | Harness a local browser / IDE / Electron UI (screenshots, a11y, visual diffs) |
| `/fix-merge-conflicts` | Resolve merge conflicts non-interactively, then validate |
| `/workflow-from-chats` | Mine recent chats into skills, rules, or workflow docs |
| `/loop-on-ci` | Watch PR checks and fix until green |
| `/what-did-i-get-done` | Summarize your commits over a time window |
| `/weekly-review` | Weekly synthesis: bugfix vs debt vs net-new |
| `/new-branch-and-pr` | Fresh branch, finish the work, open a PR |
| `/get-pr-comments` | Fetch and summarize review comments on the active PR |
| `/make-pr-easy-to-review` | Tidy history and reviewer guidance without changing behavior |
| `/thermo-nuclear-code-quality-review` | Harsh maintainability audit (abstractions, giant files, spaghetti) |
| `/pr-review-canvas` | Interactive HTML walkthrough of a GitHub PR URL |

#### Continual Learning

Not a daily slash command. Invoke it when you want `AGENTS.md` updated
from transcripts (it delegates to `agents-memory-updater`).

| `/name` | When to use it |
|---|---|
| `/continual-learning` | Mine prior chats and update `AGENTS.md`. Not a daily habit unless you ask for that loop |

21 companion skills (Cursor only). Cheat sheet total: **56**.

Install inventory and Cursor-vs-Zed table: [README.md](README.md).
Zed details: [ZED.md](ZED.md).
