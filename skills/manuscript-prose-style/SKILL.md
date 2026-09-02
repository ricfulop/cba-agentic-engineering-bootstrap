# Manuscript Prose Style (research papers, supplements, technical notes)

Use this skill when drafting or editing the prose of a research paper, supplement or technical note in the FLARE, PFR or Voltivity projects, or when the user mentions a language pass, a register pass, Americanization, heading sweep, de-AI-ing, or removing machine-generation tells.

This is the prose counterpart to `aps-figure-style`, `nature-figure-style` and `science-figure-style`. Those govern what a figure looks like; this governs what the text looks like. It exists because three failures kept reaching the author by hand: British spelling, conversational headings, and machine-generation tells.

## Key Conventions

| rule | why |
|---|---|
| American English, always, unless the venue says otherwise | The destination governs, not the sources |
| Headings are noun phrases — never sentences, questions or asides | Journal register |
| Zero invisible characters, zero Unicode punctuation substitutes | Most identifying artifact there is; invisible on the page |
| Paragraphs develop an argument; they do not state and stop | The tell that survives every surface cleanup |
| `\SI`, `\label`, `\cite`, `\ref` multisets unchanged after any prose edit | A language pass that moves a number has broken something |

---

## 1. Language: American English

**American English is the default for every document in these projects.** The
cause of the recurring error is worth naming, because it will recur otherwise:
the surrounding literature is British. A&A and MNRAS house style is British, and
*fibre* dominates the astrophotonics corpus — one FLARE note converted *fibre* →
*fiber* 127 times. An agent that matches the register of the papers it is citing
instead of the register of the venue it is writing for produces a British draft
every time. **Match the destination, not the corpus.**

### 1.1 Exceptions that keep their source spelling

| exception | example |
|---|---|
| Quoted material | A direct quotation is reproduced as its source wrote it |
| Published titles in a bibliography | *Coupling starlight into single-mode fibre optics* stays as published. A bibliography entry is a quotation of a title |
| Proper nouns, institutions, programme names | The *Centre* National d'Études Spatiales |
| Vendor product names | A catalogue part named *Fibre Coupler X* keeps the vendor's spelling |
| **Venue house style** | Nature family prints *Acknowledgements*; APS prints *Acknowledgments*. Two versions of one paper aimed at different venues legitimately differ on that word |

Venue house style **overrides the default**. Check the target venue before
sweeping, and record the decision — the same manuscript submitted to two venues
will not agree with itself, and that is correct.

### 1.2 The siunitx trap

`\metre` is a macro name. It is code, not prose, and converting it produces a
document that does not compile. The scale of the trap, measured on one FLARE
note: of **656 `metre` tokens, 652 were `\metre`** and 4 were the English word.
A naive `s/metre/meter/g` breaks 652 unit macros to fix 4 words.

The same applies to `\centering`, `\color`, `\itemize`, `\definecolor{oiGrey}`,
and every other control sequence and key that happens to contain a British
string.

### 1.3 Safe conversion order

Mask first, substitute second. Mask, in this order:

1. `\begin{thebibliography}…\end{thebibliography}` — published titles
2. siunitx calls (`\SI`, `\SIrange`, `\SIlist`, `\num`, `\numrange`, `\si`, `\ang`, `\qty`) **with every brace group**
3. Every remaining control sequence `\[A-Za-z]+` — catches standalone `\metre`
4. `\label{}`, `\cite{}`, `\ref{}`, `\includegraphics{}`, `\definecolor{}`, `\newcommand{}` and their arguments
5. Inline and display math
6. Comments

**Blank comments before pairing math.** A single `$` inside a comment
desynchronizes `$…$` pairing and silently masks the rest of the file. That defect
was live in the FLARE tool and suppressed 287 candidate words in one document
until it was found.

Words that only *look* British and are correct American English: *advertise*,
*compromise*, *promise*, *exercise*, *precise*, *otherwise*, *pairwise*,
*likewise*, *contour*, *cancellation*, *percentage*.

Reference implementation:
`FLARE/docs/notes/coupling_trades/reports/anglicise_to_american.py` — a
protection-aware substitution over a 210-form table that reports every masked hit
with its line number and reason. Generalize it; do not start a second one.

---

## 2. Headings

`\section`, `\subsection` and run-in `\paragraph{}` headings are **noun phrases**.

A heading may not:

- be a sentence, or carry a finite verb making an assertion
- pose a question
- comment on its own content ("Shape accuracy, and what the vendor figure means.")
- promise a payoff ("Why this matters.")
- read conversationally
- be content-free ("The correction.") — replace it with what the paragraph is about

Where a heading carries a label — `G1:`, `D3:`, `A6:` — **the label stays** and
what follows it is a noun phrase. Punctuation is uniform across a labelled
series: `<label>: <lowercase noun phrase>.`

Real conversions, from the FLARE long note:

| before | after |
|---|---|
| The photonic lantern does not beat étendue. | Étendue cost of the photonic lantern. |
| Three requirements together exclude multicore fiber. | Three concurrent draw requirements on a multicore feed. |
| Tool throughput is not the constraint. | Tool throughput for the production run. |
| Registration accuracy is published by four platforms and delivered by one. | Detection accuracy against delivered placement across the platforms. |
| The height constraint is a property of the process rather than of one machine. | The writable-height limit as a process property. |
| Shrinkage compensation does not close the gap, and the reason is that the part is anchored. | Limits of shrinkage compensation on an anchored part. |

Where a heading carried a claim, the claim is not lost — the body text already
states it. Verify that before deleting it from the heading.

---

## 3. Machine-generation tells

Four layers, each checkable. Run them in order; each is cheaper than the next.

### 3.1 Invisible characters

The most identifying artifact there is, and invisible on the page. Zero
tolerance.

```bash
rg -n '[\x{200B}\x{200C}\x{200D}\x{FEFF}\x{2060}\x{00AD}\x{202F}\x{2009}\x{00A0}]' \
   --glob '*.tex' --glob '*.bib'
```

| codepoint | name |
|---|---|
| U+200B / U+200C / U+200D | zero-width space, non-joiner, joiner |
| U+FEFF | byte-order mark |
| U+2060 | word joiner |
| U+00AD | soft hyphen |
| U+202F / U+2009 / U+00A0 | narrow no-break, thin, no-break space |

In LaTeX, U+00A0 becomes `~`, U+2009 becomes `\,`; the rest are deleted. Check
the BOM separately — it sits at byte 0 and no grep of line content will show it.

### 3.2 Typographic substitutions

These all render acceptably, which is why they persist.

```bash
rg -n '[\x{2014}\x{2013}\x{2018}\x{2019}\x{201C}\x{201D}\x{2026}\x{2212}\x{00D7}\x{2248}\x{2190}-\x{21FF}]' \
   --glob '*.tex'
```

| literal | TeX form |
|---|---|
| — / – | `---` / `--` |
| " " ' ' | `` `` `` / `''` / `` ` `` / `'` |
| … | `\dots` |
| − × ≈ outside math | `$-$` `$\times$` `$\approx$` |
| → ⇒ in prose | write the word |

### 3.3 Phrasing tells

```bash
rg -nwi 'delve|leverage|seamless|pivotal|nuanced|multifaceted|holistic|intricate|realm|landscape|tapestry|testament|underscore|showcase|myriad|plethora|paramount|comprehensive|meticulous' --glob '*.tex'
rg -ni '^\s*(it is worth|it is important to note|note that|crucially|importantly|interestingly|in essence)' --glob '*.tex'
rg -ni 'paves the way|opens the door|sheds light|in the realm of|underscores the|highlights the importance' --glob '*.tex'
rg -ni ', but rather|is not [a-z ]{2,30}, but\b|not only [a-z ]{2,40} but also' --glob '*.tex'
```

| tell | what it looks like |
|---|---|
| Formulaic tricolon | Three parallel items where two or four would be natural |
| "not X, but Y" | The rhetorical A/B swap used as emphasis rather than as contrast |
| Meta-commentary opener | "It is worth noting that…", "Crucially,…" — signposting instead of asserting |
| Grandiose closer | "…underscores the importance of…", "…paves the way for…" |
| Symmetrical architecture | Consecutive sentences on the same syntactic frame |
| Stacked hedges | "may potentially", "roughly on the order of approximately" |
| Vocabulary set | The `rg -nwi` list above |

An ordinary negation is not a tell. "They are not independent, but they are
separable enough" is plain English; judge in context rather than by count.

### 3.4 Provenance

| check | command | expected |
|---|---|---|
| Commit trailers | `git log --all -i --grep='co-authored-by' --grep='generated with' --grep='🤖'` | no hits |
| Generation comments in source | `rg -ni 'generated (with\|by) (an? )?(ai\|llm\|claude\|chatgpt\|gpt\|copilot\|cursor)'` | no hits |
| PDF metadata | `strings -a paper.pdf \| grep -aoE '/(Producer\|Creator) ?\([^)]*\)'` | `LaTeX with hyperref` / `pdfTeX-1.40.29` |

**No AI attribution trailer.** Never add `Co-authored-by:` naming an assistant,
a "generated with" line, or any equivalent to a commit in an academic
repository. Commit messages are permanent and are published with the repository,
which makes them part of the academic record.

**The trailer is injected downstream of the agent.** Cursor's harness rewrites
`git commit` before it reaches the shell, adding
`--trailer "Co-authored-by: Cursor <cursoragent@cursor.com>"`, so this rule
governs what an agent composes and cannot keep the trailer out of the commit.
The controls that can are the Cursor IDE attribution toggle (Cursor Settings →
Agent → Attribution — UI-only, no `settings.json` key) and a local `commit-msg`
hook. **Existing history is not to be rewritten**: report the trailers you find
and stop.

Read a hit from the check above as harness output, not as an agent ignoring the
rule. The disposition of existing history is the author's decision, not the
agent's — rewriting published history has consequences the author must weigh.

---

## 4. Prose shape

**This is the layer that matters most**, because by the time the surface tells
are gone it is the only one left. Two FLARE documents that had already been
through two register passes still had 19 paragraphs failing here.

| failure | what it is |
|---|---|
| States and stops | A paragraph carrying two ideas and developing neither, welded together because the material was compressed to fit |
| Clause stack | One sentence carrying a subordinate, a relative, a colon and a coordinated clause — usually three citations fitted into one breath |
| Connective transition | "The same arithmetic settles channel count." Announces a change of subject without asserting anything. A transition should be a claim |
| Uniform sentence length | Three or four sentences within a few words of each other; reads as a specification |
| Short declarative opener, every time | Every paragraph starting on the same beat |
| Overlong block | Over ~250 words. One FLARE paragraph ran 407 words and 14 sentences across three distinct arguments |

Machine check — `FLARE/docs/notes/coupling_trades/reports/prose_shape.py`, which
reports per paragraph the sentence count, sentence-length spread, deepest clause
nesting and opener length:

```bash
python3 prose_shape.py FILE.tex --flagged
```

Its thresholds: undeveloped = ≤2 sentences and <70 words; uniform = ≥3 sentences
with sd < 6; clause stack = depth ≥ 4; short opener = ≤11 words with ≥3
sentences; overlong = >260 words.

**Flags are not verdicts.** Roughly half are false positives — equation-split
paragraphs, run-in enumerated lists, semicolon-separated gate summaries — which
are conventional and stay. Read every flag in context and judge it.

Fixing prose shape costs words: one FLARE paper went 3907 → 4093 body words,
up 4.8 per cent, and held its page count. Do not recover the words by
compressing elsewhere, and do not add a hedge or weaken an assertion to make
room.

---

## 5. Verification after any prose edit

Take a backup before the first edit and leave it untouched. Then prove these:

| invariant | how |
|---|---|
| `\SI` family, `\label`, `\cite`, `\ref` multisets **identical** | `lang_signature.py FILE.tex OUTDIR` before and after, then diff |
| Page count unchanged | Cold three-pass build, compare |
| Zero errors, zero undefined references or citations | Compare against the pre-edit baseline, not against zero |
| Overfull/underfull box counts unchanged | Same |
| No number moved | Follows from the `\SI` multiset being identical |

`lang_signature.py` reads balanced brace groups rather than matching a flat
regex, so a multi-argument `\SIrange{}{}{}` is compared whole. Build to a scratch
directory so no repository artifact is rewritten, and **render the altered pages
and read them** — a heading conversion can set wrongly, and a paragraph split can
orphan a clause, without producing any warning.

---

## Ownership

Never edit a manuscript another agent is working on; produce a line-numbered
remediation list instead. In FLARE, never edit anything under
`overleaf-manuscript/` — it is a submodule with its own authority rules and a
canon-macro system.
