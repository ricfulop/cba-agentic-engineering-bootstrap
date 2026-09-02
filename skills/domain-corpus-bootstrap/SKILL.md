---
name: domain-corpus-bootstrap
description: Become a domain expert in X by building a reproducible, legally-acquired literature corpus for a new project or topic — topic map, checked-in query manifest, open-access download, priority triage, institutional (library) request list, corpus analysis, and handoff to the AGIneer RLM. Use when a new project, concept folder, or research direction is started, when the user says "become a super expert in X", "exhaustive literature search", "download everything on X", "what should we read", or asks for a list of papers to request from a library.
---

# Domain corpus bootstrap — "become a super expert in X"

Standing procedure. When a new project or domain X appears, the corpus comes
before the analysis. An agent reasoning about X without a corpus is reasoning
from its weights, and neither it nor the user can tell where a claim came from.

**Offer this at the start of any new project or named domain.** Do not wait to
be asked. State the cost (typically a few hours wall-clock, mostly unattended)
and the deliverables below, then get a go/no-go.

## Reference implementation

The reference implementation is `FLARE/literature/` if that repository is
present (stdlib scripts under `literature/scripts/`). Read
`literature/README.md` there before writing any new tooling and generalize
those scripts. If FLARE is not on disk, follow the generic steps below —
do not invent a second pipeline.

| step | script (FLARE reference) | generic to any X? |
|---|---|---|
| seed from cited work | `build_catalog.py` | yes — walks `.tex`/`.md`, extracts bibitems, DOIs, arXiv IDs |
| seed from search history | `extract_scite_lookups.py`, `merge_scite_into_catalog.py` | yes — replays scite MCP calls out of Cursor transcripts |
| OA download | `download_literature.py` | yes |
| second-chance acquisition | `retry_failed_downloads.py` | yes |
| library request list | `build_mit_request_list.py` | yes, retarget the institution |
| register hand-fetched PDFs | `ingest_manual_pdfs.py` | yes |
| canonical filenames | `normalize_pdf_names.py` | yes |
| RLM export | `export_for_rlm.py` | yes |

## Deliverables

A bootstrap is done when all seven exist, and not before.

1. `TOPIC_MAP.md` — what X actually is, decomposed (step 1)
2. `queries.json` — the checked-in query manifest (step 2)
3. `catalog.json` — one entry per unique paper, with priority tiers
4. `pdfs/` — every legally obtainable PDF, canonically named
5. `<INSTITUTION>_REQUESTS.md` — the short, defensible list a librarian can act on
6. `ANALYSIS.md` — themes, canon, lineage, groups, settled vs contested, gaps
7. `rlm_export/` — the AGIneer handoff surface

---

## Step 1 — Scope X into a topic map

A project name is not a search. Turn it into five buckets, written to
`TOPIC_MAP.md`, before touching a database.

| bucket | question it answers | starshade example |
|---|---|---|
| core topic | the thing itself | starshade / external occulter formation-flying starlight suppression |
| sub-topics | its decomposable parts | petal edge scatter, Fresnel/apodization design, deployment mechanics, formation sensing and control, solar glint, micrometeoroid tolerance |
| adjacent physics/engineering | what a practitioner must also know | scalar diffraction and Babinet, boom/membrane structural dynamics, station-keeping ΔV budgets, stray light, contamination |
| competing approaches | what X is argued against | internal coronagraphs, interferometric nulling, apodized pupils, direct imaging with extreme AO |
| foundational theory | what the field rests on | Fresnel diffraction, Cash's offset-hyperbolic apodization, Vanderbei optimization, Marchal |

Two rules.

**Mine in-repo prior art for seeds.** If the project folder already has a
concept note, prior-art assessment, feasibility memo, or a bibliography, the
names, DOIs and programme labels in it are the highest-precision seeds
available — they were chosen by a human who understood the problem. In the
starshade case that is `starshade_concept/PRIOR_ART.md`. Harvest every author,
mission acronym, funding programme (NIAC, APRA, SAT), and DOI out of it first.

**Name the people and programmes, not just the concepts.** Fields this size
are 20–40 people. An author sweep on the six names that recur in the prior art
is usually higher-yield than any keyword query.

---

## Step 2 — Write a checked-in query manifest

The search must be re-runnable by someone else, and auditable when a reviewer
asks "did you look for Y?". A chat transcript is neither.

`queries.json` — one record per query, committed alongside the catalog:

```json
{
  "id": "q014",
  "bucket": "sub-topic:edge-scatter",
  "query": "(starshade OR occulter) AND (\"edge scatter\" OR \"solar glint\") AND (petal OR occulting)",
  "sources": ["ads", "arxiv", "spie", "ntrs"],
  "date_first_run": "2026-08-11",
  "hits": 37,
  "kept": 11,
  "note": "SPIE hits dominate; ADS misses proceedings without DOIs"
}
```

`kept` far below `hits` is fine. `kept` at zero is a finding — record it, because
a negative result ("nobody has published on modular reassembly tolerancing") is
evidence, and it is the evidence most often lost.

See `templates.md` for the full manifest schema and the request-list template.

---

## Step 3 — Choose sources by field

Database choice dominates recall, and the right set varies enormously by field.
Do not run one generic list. **Read `sources-by-field.md`** for the routing
table per domain family (astronomy/space, materials/plasma, biomedical,
engineering/EE, chemistry, earth science).

The three field-specific traps worth knowing up front:

- **Astronomy and space**: the load-bearing literature is substantially grey —
  NASA NTRS, NIAC final reports, decadal white papers, KISS/workshop short
  courses, JPL technical reports — plus SPIE proceedings, which are often the
  only publication of an instrument result. Crossref and Semantic Scholar
  under-index all of this. NASA ADS is the primary index, not a supplement.
- **Materials and plasma**: APS (PRB/PRApplied/PRMaterials), arXiv cond-mat,
  ceramics/metallurgy society journals, plus materials databases (Materials
  Project, COD, ICSD) as a distinct non-paper source class.
- **Biomedical**: PubMed/PMC first, and preprints (bioRxiv/medRxiv) are a
  separate sweep, not a fallback.

Available tooling, in the order to reach for it:

| tool | use |
|---|---|
| `paper-lookup` skill | 10 databases incl. PubMed, PMC, arXiv, OpenAlex, Crossref, Semantic Scholar, CORE, Unpaywall — the workhorse |
| `scite` MCP | citation-context search; also the only source that tells you *how* a paper was cited (supporting/contrasting) |
| `database-lookup` skill | 78 non-paper databases — NASA, NIST, Materials Project, PDB, and similar |
| `exa-search`, `parallel-web` | semantic web search with academic filtering; reaches grey literature the indexes miss |
| `research-lookup` | routed deep-research queries |
| `citation-management` | BibTeX generation and citation validation on the way out |

NASA ADS has no MCP wrapper here. Use its public API directly
(`ADS_API_KEY`/`ADS_DEV_KEY`), and note that its scanned-article service serves
pre-DOI astronomy papers with no key at all — `retry_failed_downloads.py`
already implements that route.

---

## Step 4 — Legal acquisition only

**Hard boundary. No exceptions, and say so in the corpus README.**

- Fetch only URLs advertised as open access by Unpaywall, OpenAlex, arXiv, HAL,
  Europe PMC, CORE, institutional repositories, or the publisher's own OA link.
- Honour `robots.txt` and per-host `Crawl-delay`.
- Never solve a CAPTCHA or proof-of-work challenge, never use credentials, never
  scrape a paywalled publisher page, never use Sci-Hub or any mirror.
- Verify payloads are real PDFs (`%PDF-` magic) before keeping them.

Two counterintuitive findings from the reference implementation, both worth
inheriting:

- **Identify honestly as a script.** HAL (Anubis) and IOPscience (PerimeterX)
  serve PDFs to a client with a bot User-Agent and challenge anything claiming
  to be Chrome. Sending a browser UA first cost the FLARE run 25 recoverable
  papers. Try the bot UA first, browser only as fallback.
- **A `robots.txt` block is not a paywall.** `iopscience.iop.org` is
  `Disallow: /` site-wide, so genuinely open AAS/IOP papers are unreachable to
  any well-behaved script and trivially reachable by a human in a browser. Split
  these into a "free to read, browser only" section — they are minutes of
  clicking, not a library request, and filing them with a librarian wastes
  everyone's time.

---

## Step 5 — Triage into priority tiers

The tiers decide what gets downloaded and what gets requested. Adapt the FLARE
definitions to the project; keep three actionable tiers and a cataloged reserve.

| tier | definition | action |
|---|---|---|
| `p0` | cited in a project document, or foundational to X | fetch; request from library if paywalled |
| `p1` | engaged with during the work (agent or human read it) but not yet cited; directly on-topic | fetch; request if the argument depends on it |
| `p2` | on-topic, returned by search, not yet read | fetch OA only |
| `p3`/`p4` | adjacent or background; cataloged with metadata, never fetched | reserve — fetch on demand |

Ties resolve upward: a paper that is both cited and merely search-returned is
`p0`. Catalog `p3`/`p4` fully — metadata is cheap, thousands of PDFs are not.

**The tier is a judgement call and a human owns it.** An agent can propose the
assignment; the user decides what the project's argument actually rests on.

---

## Step 6 — The institutional request list

This is the deliverable a human outside the project consumes, so it is written
for them, not for us. Two audiences in one document: a librarian who needs to
locate and license the item, and a reviewer who needs to know why it is worth
the request.

Per entry, a librarian needs all of:

- full citation — authors, year, exact title, journal or proceedings, volume,
  issue, pages
- DOI as a resolvable link
- venue detail that distinguishes an item a catalog search will otherwise miss:
  **ISSN for journals, ISBN plus volume number for proceedings series** (SPIE,
  AIP, IEEE), report number for technical reports, handle or database ID for
  theses

Per entry, we need one line of internal justification: which claim in our work
depends on it, quoted from our own text where possible. `build_mit_request_list.py`
pulls the citing sentence out of the manuscripts automatically; that line is
what makes the list defensible rather than a dump.

Structure the document as:

1. **Free to read, browser only** — clear this before filing anything.
2. **Not a library problem** — vendor datasheets, market reports, theses already
   in hand. Separated out so nobody chases them.
3. **Genuine requests, grouped by publisher** — institutions license per
   publisher, so a publisher group can go in as one request. Order groups by
   likelihood the institution holds them.
4. **"If you only do ten"** — the p0 subset with the widest blast radius.

**Keep it short.** A 300-item request list gets ignored; a 20-item list with a
stated reason per item gets filled. Prune to what the argument actually needs.

---

## Step 7 — Deduplicate across versions

One paper, one entry, however many manifestations. Match in this order:

1. normalized DOI (lowercase, strip `https://doi.org/` and `dx.doi.org/`, strip
   trailing punctuation)
2. DataCite arXiv DOIs (`10.48550/arxiv.<id>`) against `arxiv:<id>` keys
3. arXiv ID
4. normalized title, **only** for entries carrying no DOI

Three failure modes the reference implementation hit, all worth guarding:

- **A preprint and its version of record are one paper.** Keep both files if
  useful, but as `alternate_versions` on a single entry with a filename suffix —
  never as two entries.
- **Corrections, errata and deposited datasets get promoted to phantom papers**
  by a loose-DOI extractor that finds them inside another entry's citation text.
  Fold them into the parent as `related_dois`, and subtract them before quoting
  a corpus size.
- **Title matching is dangerous below ~0.5 Jaccard overlap.** A real duplicate
  in the FLARE corpus scored 0.38; the right repair was fixing the malformed
  citation, not loosening the matcher. Report unresolved cases; never guess.

---

## Step 8 — Analyze the corpus

**This is the step that converts PDFs into expertise, and it is the one most
often skipped.** A downloaded corpus nobody has characterized is storage.
Write `ANALYSIS.md` covering:

| section | what it must answer |
|---|---|
| themes | what clusters exist, how big, reproducibly assigned (a classifier over title+venue, not eyeballed) |
| canonical papers | the handful everything cites, and what each one established |
| intellectual lineage | who descends from whom; which result superseded which |
| key groups and people | the 20–40 names, their institutions, what each is known for |
| settled vs contested | what the field agrees on, and the live disagreements with both sides named |
| gap analysis | what the project cites weakly, what it should cite and does not, what nobody has published |
| bibliography health | fabricated, mis-paginated, retracted, or title-less references |

Two disciplines that were learned the hard way:

- **A search-record gap analysis is a shortlist for reading, not a
  recommendation.** The FLARE analysis derived recommendations from what was
  searched rather than from the manuscript text and ran a **30% false-positive
  rate** — it recommended citations for claims the manuscript does not make.
  Never write "supports the manuscript's claim that X" unless X has been grepped
  out of the live source.
- **Check every reference you touch for editorial notices** (retraction,
  correction, expression of concern) before it enters the canon list.

---

## Step 9 — Hand off to the AGIneer RLM

AGIneer's RLM is a *reasoning core*, not a retrieval store: no index, no vector
store, no persistent collection. There is nothing to "load a corpus into." What
it has is a per-run evidence surface — text handed in at question time, with
every conclusion carrying a path and line range back into what was handed in.

Practical consequences for the export:

- **Export metadata cards as a repository tree**, one field per line, one
  greppable block per paper. Search returns one line per hit capped at 500
  characters, so every line must stand alone.
- **PDFs are invisible** (`.pdf` is a binary suffix) and **any file over 500 kB
  is invisible**. A 3 MB `catalog.json` cannot be read. Shard the export.
- **Two roots, chosen per question**: metadata cards for provenance questions
  ("what do we rest on"), extracted full text for content questions ("what does
  this paper say"). Full text is a superset in coverage and worse in precision.
- **Read-only, root-confined.** AGIneer can only read paths under
  `AGINEER_INPUT_ROOTS`. If a run returns `PATH_NOT_ALLOWED`, tell the user to
  add the root to their private MCP config — **never widen it on their behalf**,
  and never commit that machine-specific path.

`export_for_rlm.py` is the reference: dry-run by default, idempotent,
`--granularity metadata|fulltext`, `--tier`, `--commit`.

---

## Step 10 — Re-run and maintain

Corpora go stale silently. Schedule the sweep rather than remembering it.

| trigger | action |
|---|---|
| PDFs arrive from the library | drop into `pdfs/`, run the manual-ingest script, regenerate the request list |
| the project's argument changes | re-run the catalog build; tiers shift as citations move |
| quarterly, or before any submission | re-run the query manifest; record new hits against `date_first_run` |
| a new sub-topic appears | add queries to the manifest, do not start a second corpus |

Rebuilds must never destroy acquisition state — download status, PDF paths and
non-document provenance tags survive a rebuild in the reference implementation,
and any reimplementation must preserve that property.

---

## What is automated and what is not

State this to the user when scoping the work. The unattended fraction is large
but the judgement is not delegable.

| step | status |
|---|---|
| catalog extraction, metadata resolution, dedup | automated |
| OA download, retry, PDF verification, canonical naming | automated |
| request-list generation and grouping | automated |
| RLM export | automated |
| **topic map and query design** | **human** — an agent drafts, the user corrects the scope |
| **priority tier assignment** | **human** — what the argument rests on is an editorial call |
| **paywalled retrieval** | **human** — browser session or library request |
| **analysis synthesis** | **human-led** — lineage, contested points and gaps need reading, and the automated version has a measured false-positive rate |

## Related skills

`paper-lookup`, `database-lookup`, `citation-management`, `literature-review`
(systematic-review protocol; biomedical-first by default — for physics and
materials prefer arXiv/APS/ADS/OpenAlex), `scientific-critical-thinking`
(evidence grading during analysis).

## Additional resources

- Source routing per field: [sources-by-field.md](sources-by-field.md)
- Query manifest schema, request-list and analysis templates:
  [templates.md](templates.md)
