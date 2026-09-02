# Templates

Companion to `SKILL.md`. Copy and adapt; do not invent a parallel schema.

## 1. `TOPIC_MAP.md`

```markdown
# Topic map — <X>

Prepared <date>. Scoping only; no acquisition, no analysis.

## Core topic
One paragraph: what X is, in the terms a practitioner would use.

## Sub-topics
| sub-topic | why it matters to this project | seed names / DOIs |
|---|---|---|

## Adjacent physics and engineering
| area | what we must be competent in | seed names / DOIs |
|---|---|---|

## Competing approaches
| approach | claimed advantage over X | who advocates it |
|---|---|---|

## Foundational theory
| result | who | why everything rests on it |
|---|---|---|

## People and programmes
| name / programme | institution | known for |
|---|---|---|

## Seeds harvested from in-repo prior art
Source document, and every author, DOI, acronym and programme taken from it.
```

## 2. `queries.json`

```json
{
  "schema_version": 1,
  "domain": "<X>",
  "created": "2026-08-11",
  "queries": [
    {
      "id": "q001",
      "bucket": "core | sub-topic:<name> | adjacent:<name> | competing:<name> | foundational | author:<name>",
      "query": "the exact query string, Boolean operators and phrase quoting included",
      "sources": ["ads", "arxiv", "openalex", "scite", "ntrs", "spie"],
      "date_first_run": "2026-08-11",
      "date_last_run": "2026-08-11",
      "hits": 0,
      "kept": 0,
      "note": "why this query, and what it missed"
    }
  ]
}
```

Rules:

- The query string is verbatim, including quoting. A paraphrased query is not
  reproducible.
- `kept: 0` records a real negative result. Keep the record; do not delete the
  query.
- Author sweeps get their own `author:` bucket. They usually outperform keyword
  queries in small fields.
- On a re-sweep, update `date_last_run` and `hits`; never overwrite
  `date_first_run`.

## 3. Institutional request list

```markdown
# <Institution> library requests — <project>

Generated <date> by `<script>`. Regenerate after every acquisition round.

Everything here has already been through the open-access pipeline and an
automated second-chance pass. Neither solves CAPTCHAs, defeats bot protection,
uses credentials, or touches a URL not advertised as open access.

**State of the library:** N of M priority papers held. Of the K missing, A
genuinely need institutional access, B are free to read and need only a
browser, C are not library items.

| | p0 | p1 | p2 | Total |
|---|---:|---:|---:|---:|
| **Needs institutional access** | | | | |
| Free to read, browser only | | | | |

### If you only do ten
1. **Author Year**, Title — <https://doi.org/...>

---

## Start here: free to read, no request needed
<publisher groups; one line why the script could not take it>

## Not a library problem
<vendor datasheets, market reports, items already in hand>

---

## Requests, grouped by publisher

### <Publisher> — N papers
- `p0` Authors (Year). *Exact title*. Journal, volume(issue), pages.
  - DOI: <https://doi.org/...>
  - ISSN <....-....> / proceedings ISBN <...>, volume <...>
  - Why we need it: <the claim in our work that depends on it, quoted>
```

The two fields most often omitted and most often needed: **ISSN for journals,
ISBN plus volume number for proceedings series** (SPIE, AIP, IEEE). A librarian
cannot reliably locate a proceedings paper from a DOI alone.

## 4. `ANALYSIS.md` outline

```markdown
# <X> corpus analysis

Regenerated <date> from `catalog.json` (N entries). Companions: README.md
(pipeline and schema), catalog.json, pdfs/, <INSTITUTION>_REQUESTS.md.

## 1. Scope and method
Sources combined, how deduplicated, and the coverage limits stated plainly —
what this record cannot see, and why the absence of a theme is weak evidence.

## 2. The corpus at a glance
Tier counts, overlap between discovery routes.

## 3. Thematic breakdown
Reproducible classifier over title+venue, with the prose reading beneath it.
Say what fraction the classifier could not place.

## 4. Canonical papers
The handful everything cites, what each established, and the citation counts
with their caveat (a count mixes formal citation with prose mention).

## 5. Intellectual lineage and key groups
Who descends from whom, which result superseded which, the 20-40 names.

## 6. Settled versus contested
Two lists. For each contested point, both positions and their best citation.

## 7. Gap analysis
7a. Accepted and now cited. 7b. Examined and rejected, with reasons.
7c. Still open, at lower weight. 7d. Themes thin relative to their design
weight. 7e. Claims leaning on weak citations.

## 8. Bibliography health
Fabricated, mis-paginated, retracted, title-less, orphaned.

## 9. Download status
Tier table: held / no OA copy / fetch failed. OA colour distribution.

## 10. How to rerun everything
Ordered commands, and the ordering constraints between them.

## 11. Open questions for the user
Decisions this analysis is not entitled to make.
```

Two required disciplines, both learned from a measured failure:

- A gap analysis derived from the search record is a **shortlist for reading**,
  not a recommendation. Do not write "supports the manuscript's claim that X"
  unless X has been grepped out of the live source. The unguarded version ran a
  30% false-positive rate.
- Record rejected recommendations with their reasons (§7b). A rejection is a
  result, and without it the next run re-proposes the same paper.

## 5. PDF filename convention

`<year>_<firstauthor>_<title-slug>.pdf`, no exceptions, derived from the
catalog entry. The name is a claim about identity: the file is the paper the
catalog holds under that year, author and title, and nothing else.

A second manifestation of a paper already held (version of record beside its
preprint) takes a suffix — `..._josab-published.pdf` — and is recorded as an
`alternate_versions` entry on the owning paper, never as a second paper.

Renames go through `git mv` so history and any LFS pointer follow the file.

## 6. Catalog entry — minimum viable schema

Keyed by lowercase DOI → `arxiv:<id>` → `title:<normalized-slug>`.

| field | meaning |
|---|---|
| `id`, `doi`, `arxiv_id` | identifiers |
| `title`, `authors`, `first_author`, `year`, `venue`, `work_type` | normalized metadata |
| `sources` | provenance tags, multiple expected: `document:<path>`, `query:<id>`, `manual` |
| `priority` | `p0`–`p4` |
| `cited_by_files`, `cite_count`, `raw_citation` | where it is used in our own work |
| `resolution` | how metadata was resolved, including `unresolved` |
| `oa_status` | OA colour |
| `pdf_path`, `download_status`, `alternate_versions` | acquisition state |
| `merged_ids` | previous keys folded in |
| `related_dois` | corrections, errata, deposited datasets belonging to this paper |

`resolution` and `oa_status` are load-bearing: an entry that says `unresolved`
is honest, and one that silently carries a guessed title is not.
