# Source routing by field

Companion to `SKILL.md` step 3. Recall is dominated by which indexes you query,
and the right set differs enough between fields that a single generic list
loses whole literatures. Run the row for the field, plus the universal row.

## Universal — run these for every X

| source | reach | route |
|---|---|---|
| OpenAlex | 250M+ works, best coverage of the long tail, free API, good author/institution graph | `paper-lookup` |
| Crossref | DOI registry of record; authoritative metadata, weak full-text discovery | `paper-lookup` |
| Semantic Scholar | citation graph, influential-citation flags, TLDRs | `paper-lookup` |
| Unpaywall | OA location resolution — the acquisition workhorse, not a discovery tool | `paper-lookup` |
| CORE | 200M+ open-repository records; catches institutional deposits nothing else indexes | `paper-lookup` |
| scite | citation *context* — supporting vs contrasting vs mentioning, plus editorial notices | `scite` MCP |
| Google Scholar | recall backstop, no API; use only to check for something the indexes missed | manual |

**Patents are a distinct literature and are routinely skipped.** For any topic
with a hardware or process component, run `scite`'s `search_patents` and treat
hits as prior art, not as papers. In several engineering fields the earliest
disclosure of a technique is a patent.

## Astronomy, space and instrumentation

The defining feature of this field is that **the load-bearing literature is
substantially grey**, and the general indexes under-cover it badly.

| source | why it is non-optional | route |
|---|---|---|
| **NASA ADS** | The primary index for astronomy. Covers pre-DOI literature back to the 1800s, indexes conference proceedings and observatory reports, and its bibcode is the stable identifier. Serves scanned PDFs of pre-DOI articles with **no API key** at `articles.adsabs.harvard.edu/pdf/<bibcode>` | public API, `ADS_API_KEY` for search |
| **NASA NTRS** | Technical reports, contractor reports, and the only home of much mission-concept engineering work | public API / web |
| **NIAC final reports** | Phase I/II reports for advanced concepts; frequently the only written record of a funded architecture | NASA NIAC site |
| **SPIE Digital Library** | Astronomical instrumentation is published in SPIE proceedings first and often only. Requires ISBN + volume for a library request | DOI `10.1117/12.*` |
| **arXiv astro-ph** | Near-universal preprint coverage; usually the legal OA copy of a paywalled journal paper | `paper-lookup` |
| Decadal survey white papers (Astro2020 APC/science) | Programmatic arguments and concept proposals, cited as BAAS volumes | ADS, BAAS |
| A&A / AJ / ApJ / MNRAS / PASP / JATIS | The journals themselves | `paper-lookup` |
| KISS, Lunar and Planetary Institute, workshop short courses | Slide decks that state numbers years before a paper does. Label as briefing material | web search |

Traps: IOPscience (`ApJ`, `AJ`, `JATIS`) blocks all crawlers via `robots.txt`
despite OA content. A&A sits behind CDN bot protection. Both are browser-only.

## Materials science, ceramics, metallurgy, plasma

| source | why | route |
|---|---|---|
| APS journals (PRB, PRApplied, PRMaterials, PRL) | The physics core | `paper-lookup` |
| arXiv cond-mat, physics.plasm-ph | Preprints and the legal OA copy | `paper-lookup` |
| Society journals — J. Am. Ceram. Soc., J. Eur. Ceram. Soc., Acta/Scripta Materialia, JOM | Where processing results actually appear; largely Wiley/Elsevier and largely paywalled | `paper-lookup` |
| Materials Project, COD, ICSD, NIST databases | Structures, phase data, thermochemistry — a **non-paper source class**, cite the database entry | `database-lookup`, `pymatgen` |
| IEEE Xplore (Trans. Plasma Sci., Dielectrics) | Discharge physics and pulsed power | `paper-lookup` |
| Theses | Process detail that never reaches a paper. ProQuest, institutional repositories | web search, CORE |

Trap: Wiley and Elsevier CDN bot protection returns 403 to scripts on genuinely
OA content. Browser-only, not a library request.

## Biomedical and life sciences

| source | why | route |
|---|---|---|
| PubMed / PMC | Primary index; PMC gives full text and is the OA route | `paper-lookup` |
| bioRxiv, medRxiv | A **separate sweep**, not a fallback — much of the recent literature is preprint-only | `paper-lookup` |
| ClinicalTrials.gov, FAERS, MAUDE, 510(k) | Regulatory and trial evidence, distinct from papers | `scite` MCP |
| Europe PMC | Broader than PMC, and a reliable OA fetch route | `paper-lookup` |
| Cochrane, PROSPERO | Existing systematic reviews — check before running your own | web |

Follow PRISMA if the result is a formal review; the `literature-review` skill
already implements that protocol and defaults biomedical-first.

## Engineering, EE, photonics, controls

| source | why | route |
|---|---|---|
| IEEE Xplore | The field's primary venue, conferences included | `paper-lookup` |
| Optica (formerly OSA) — Opt. Express, Opt. Lett., JOSA A/B, Appl. Opt. | Optics core; Opt. Express is fully OA | `paper-lookup` |
| SPIE | Proceedings, as above | DOI `10.1117/12.*` |
| ASME, AIAA | Mechanical and aerospace conference literature; AIAA papers are often the only record | publisher |
| arXiv eess, physics.optics | Preprints | `paper-lookup` |
| Standards — ISO, ASTM, IEEE, MIL-STD | Never OA, never a library ILL request; a purchase or an institutional subscription | note separately |

## Chemistry and chemical engineering

PubChem, ChEMBL, ACS/RSC/Wiley journals, Reaxys (subscription), plus
`database-lookup` for the structure and property databases. Note that ACS is
strict about text mining; use the OA copies only.

## Earth, climate and environment

USGS, NOAA, EPA, Copernicus, AGU journals (largely OA), plus the data archives,
which are the actual product in this field far more often than the papers.

## Economics, policy and market context

Rarely peer-reviewed and rarely archival. NBER working papers, agency reports,
and vendor market notes. **Vendor market reports are not citable literature** —
record them as vendor documents outside the catalog, and soften any claim that
rests on one to "vendor roadmaps indicate".

## Choosing the acquisition route

Once a paper is identified, resolution order for a legal copy:

1. arXiv (by ID) — fastest and always legal
2. Unpaywall `best_oa_location`, then its other OA locations
3. OpenAlex OA locations
4. Europe PMC (biomedical), HAL (French institutions), CORE (repositories)
5. NASA ADS scanned-article service (pre-DOI astronomy, no key needed)
6. `citation_pdf_url` or a deposited-file link on an institutional-repository
   landing page
7. Gated preprint title match — accept only with author-and-year agreement

Anything left is either browser-only (bot protection on OA content) or a
genuine institutional request. Distinguish the two; they cost very different
amounts of somebody's time.
