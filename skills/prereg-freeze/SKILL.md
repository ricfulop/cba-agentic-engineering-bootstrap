---
name: prereg-freeze
description: Hash-bound preregistration before confirmatory runs. Use when freezing a protocol, recording a deviation, or starting a confirmatory campaign.
---

# Preregistration freeze

Confirmatory work is hash-bound. Freeze the protocol before the run, not
after.

1. Write the protocol (estimands, gates, exclusions, analysis).
2. Freeze it as a dated record (`protocol_freeze.json` or equivalent)
   with a content hash.
3. Do not overwrite a freeze. A protocol change is a new record
   (`protocol_freeze_v2.json`, …), not an amendment in place.
4. Deviations are append-only numbered D-entries.
5. Weights and gates that were frozen are do-not-retune.
6. A new study is a new freeze, not a silent widening of the last one.

There is no discovery claim from a search that was not preregistered as
discovery. Pilot and exploratory results keep that classification.

Do not start confirmatory N-runs from a demonstrator package that was
never frozen for that purpose.
