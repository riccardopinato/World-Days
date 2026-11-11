# World Days — 1,111+ individual source and story audit

**Checkpoint:** 11 November 2026. The catalog currently has 1,111 canonical identities. The number is a *minimum*, not an automatic cap. The canonical ID, actual issuer, source quality and review state govern editorial publishing.

## Evidence classification — never pretend all entries are finished

The existing English editorial runtime contains **56 REVIEWED articles**. Other candidate/draft articles remain outside runtime, and many catalog records have only source-index metadata. A technically present calendar day is *not* proof of an independently audited individual historical narrative. `tool/editorial_1111_source_audit_queue.py` derives the canonical list by joining the actual generated catalog, existing editorial manifest, English reviewed pack and the newly researched two Irish stories. It outputs `reports/editorial_1111_source_audit_queue.json` with all current canonical IDs and a stable 50-item next-work queue. The report is saved as a GitHub CI artifact for inspection; it is not a source of new published text.

Each record reports: canonical title, scope, country, period, authority and source URLs/tiers, verified introduction year when available, current editorial stage, source-quality risk, real published English history/why/date facts (only when present), separately marked research drafts, unknown fields, and work priority. **Promoters/founders are not inferred merely because an authority is listed.** Unknown origin, motivation, founding year or circumstances remain null until a relevant source supports them.

## Workflow for each individual record

1. **Identity and date:** Check distinct canonical identity, primary date/recurrence and local legal vs institutionally indexed vs cultural classification. Correct cross-year errors before authoring prose.
2. **History:** Establish the actual origin and year, distinguishing an older commemorated event from formal modern declaration. Preserve any unknowns.
3. **Who proposed it:** Identify specific person, organization or government only when an original resolution, statutory act, press release or reliable archive supports the attribution.
4. **Why it matters:** Draft original compact, engaging, source-traceable history; offer 2–5 contextual facts or traditions supported by named sources, without generic invented anecdotes.
5. **Translation and release:** Prepare original EN/IT, then ES/FR/DE/PT with explicit review status. A draft must not be labeled `REVIEWED` or `REVIEWED_TRANSLATION` merely because text exists. Deploy only after each source, length, factual and UI test passes.

## Research priorities

- **P0**: National holiday records derived from the European EURES index or Australian diplomatic protocol — validate against the national government or legal issuer first. Diplomatic listing does not prove that a local public holiday exists.
- **P1**: Philippine NCCA cultural calendars and source-backed research drafts — check individual dates and avoid mislabeling birthdays, anniversaries and cultural months as legal holidays.
- **P2**: Other source-index entries lacking verified history, founding year, proposer or contextual facts — research one by one.
- **P3**: Already reviewed long-form content — inspect completeness and maintain source freshness.

The first illustrative research batch (`data/editorial/candidates/irish_brigid_two_stories_primary_20261111.json`) distinguishes traditional St Brigid’s Day from the statutory holiday created in 2023, using Ireland's government and Workplace Relations Commission sources. These **two stories remain draft** and are not counted in the 56 existing reviewed runtime entries.

No APK, device test, Play publication or unsourced generative bulk prose is involved in this source-audit phase.
