# World Days — Editorial Policy

Baseline: 2026-10-12

World Days keeps factual identity and editorial content in separate datasets.

## Canonical layer

The canonical observance record owns:
- title and aliases
- recurrence/date rules
- scope
- authority and officiality
- source provenance

Editorial copy must never modify those facts.

## Editorial layer

`assets/data/editorial_en.json` is generated from `tool/build_editorial.py`.

The English pack is the editorial master. Each reviewed entry contains:
- original summary
- original "why it matters" section
- 2–4 practical ways to take part
- review date
- a source-policy marker linking the copy back to the canonical authority/originator evidence

Initial Step 5 coverage: **28 reviewed English entries**.

## Writing rules

1. Do not copy prose from UN, WHO, UNESCO, NGOs, Wikipedia, magazines or discovery calendars.
2. Facts must be supportable by sources already attached to the canonical record.
3. Avoid unsupported statistics, campaign slogans and yearly themes in evergreen copy.
4. Do not give medical, legal or crisis advice as if World Days were a professional service.
5. Keep participation suggestions low-risk, realistic and non-judgmental.
6. If a claim requires a yearly update, keep it in a year override or campaign layer rather than evergreen editorial copy.
7. English is the source language. Translations are handled as separate locale packs and must preserve meaning rather than rewrite facts.

## Fallback

Observances without a reviewed article continue to show canonical authority/provenance and an editorial-coming-next state. Missing editorial content must never hide the observance itself.
