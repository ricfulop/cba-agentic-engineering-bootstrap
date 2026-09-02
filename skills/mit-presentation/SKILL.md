---
name: mit-presentation
description: Build academic PowerPoint decks from the official MIT Arial template. Use for CBA talks, course slides, and MIT-affiliated research decks.
---

# MIT presentation

Official MIT PowerPoint template, Arial, MIT red (163, 31, 52).
Affiliation default: Center for Bits and Atoms, Massachusetts Institute
of Technology.

Use the official MIT template and MIT marks only. Do not add
confidential FAR footers or third-party lockups.

## Files

| path | role |
|---|---|
| `templates/MIT-PowerPoint-template-Arial-3.pptx` | official MIT template |
| `brand/` | MIT logo-2 RGB (mit-red, white, black) |
| `skills/mit-presentation/scripts/mit_pptx.py` | thin python-pptx helper |

Marks are for MIT-affiliated academic use. See `brand/BRAND.md`.

## How to build

```bash
# from the plugin clone
python skills/mit-presentation/scripts/mit_pptx.py \
  --title "Talk title" \
  --subtitle "Optional subtitle" \
  --outfile talk.pptx
```

The script opens the official template and adds slides on its layouts
(title, section divider, quote). Content slides reuse a template layout
and fill Arial text; they do not draw a custom chrome.

## Rules

- Arial throughout
- MIT red RGB (163, 31, 52) for emphasis; black/white from the template
- Affiliation: Center for Bits and Atoms, Massachusetts Institute of Technology
- Research numbers still go through `verify-before-claiming`
