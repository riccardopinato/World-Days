# Institutional 100 — Canada / Camden (11 November 2026)

## Exactly 100 indexed candidates, not 100 official catalog admissions

This batch contains **100 traceable institution-index source rows**:
- **46** Canadian Heritage entries from https://www.canada.ca/en/canadian-heritage/services/important-commemorative-days.html .
- **54** London Borough of Camden inclusion-calendar entries from https://www.camden.gov.uk/camden-s-inclusion-calendar .

All entries contain a source-as-indexed English label, a 2026 date notation, source URL and market context, with **explicit false identity/recurrence/dedup gates**, editorial status `NOT_REVIEWED` and no invented introduction year.

**Not all source rows are unique new days.** The source lists repeat some global days already included in World Days, and fixed 2026 lunar/religious dates cannot be assumed to recur on the same Gregorian day. Camden's civic inclusion calendar records community observances without necessarily being the legal establishing authority. A Canadian national commemoration may be public, civic or regional in effect, not necessarily a statutory holiday.

## Verifiable steps

- `python3 tool/validate_institutional_100_research.py` enforces **exactly 100** valid-index rows, 46/54 split, distinct source-row identifiers and all publication gates false.
- Resolve canonical identity using the generated **latest main catalog** (not only normalized title) and compare scope/authority/aliases before admission.
- For candidate admission obtain the actual public authority or organizer, recurrence over three or more years, correct national versus global or regional scope, and six UI title locales.
- Keep reviewed long-form history and first-established year separate; unknown year is `null`.
- National Canada Wave08 is a separate curated source-code PR **#81** proposing 27 carefully selected canonical records; do not inflate this 100-row discovery batch by adding them a second time.
- User request is **100-item batches** going forward. The research packet satisfies discovery batch size, **not** a 100-record production publication milestone.

Baseline `main` was **511** distinct records when this packet branch was created. Do not assert larger on-main count without green CI and actual merge. No APK, Android physical device, signing or Play rollout.
