---
name: dual-source-honesty
description: Keep fetch-time catalogs distinct from corrected bibliographies; keep measured, derived, and estimated values distinct. Use when cataloging papers or quoting a number's status.
---

# Dual-source honesty

Two records can disagree. A disagreement is a decision request, not
permission to copy one side over the other.

## Literature

- The fetch-time catalog (`catalog.json` or equivalent) is what the
  search returned. Leave it as-is.
- Bibliography field corrections go in `refs.bib` (or the project's
  bibliography) plus a register.
- Empty author lists stay empty rather than invented. Truncated
  three-author records that were not confirmed stay `and others`.
- A catalog count is not a reading count.

## Numbers

Workbook or table status words are load-bearing and are not synonyms:

| status | meaning |
|---|---|
| MEASURED | an instrument or a run produced it |
| DERIVED | computed from named inputs that exist |
| CATALOG | a vendor or index field |
| ESTIMATE | judgment, bounded if possible |
| blank / NR / TBD / PLACEHOLDER | unknown — do not fill from adjacent cells |

Do not infer procurement metadata from a model-spec column, or a canon
value from manuscript prose. When two owners hold disjoint fields, record
the decision rather than silently merging.

## What this is not

Private correspondence pasted into chat is background, not quotable
material, unless the author clears the specific quote.
