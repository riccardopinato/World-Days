# Phase C — Content understanding evidence

Date: 2026-10-15
Repository: riccardopinato/World-Days
PR: #30 — phase-c-editorial-minimum -> main
Factory baseline: 47c47f49a7b46812e3bd6f1231c3524f2b52b826 (Master v26.6 / Golden Index v18)

## V1 content model

World Days now uses two explicitly different content layers.

### Tier 1 — Verified Overview

Required for every launch observance.

Coverage:
- 296 / 296 catalog records;
- EN / IT / ES / FR / DE / PT;
- localized title;
- authority;
- scope;
- verification provenance inherited from the canonical record.

The overview is generated only from already verified catalog metadata. It does not invent or infer history, date rationale, facts, campaign claims or participation guidance.

The runtime status remains conceptually separate from Rich Editorial and is not labelled REVIEWED.

### Tier 2 — Rich Editorial

Current curated coverage:
- 28 / 296 records;
- English source-reviewed master;
- IT / ES / FR / DE / PT reviewed translation parity.

The existing long-form layer keeps:
- summary / Why it matters / Ways to take part;
- optional hook;
- Why this date;
- origin/history;
- quick facts;
- related observances;
- annual campaign theme where separately verified.

Expanding Rich Editorial beyond the current reviewed set is a post-v1 content program.

## Provenance safeguards

Reviewed Rich Editorial is validated against the canonical catalog.

For every REVIEWED English article, CI now requires:
- a canonical observance record;
- a non-empty authority;
- at least one verified source from a strong source tier:
  - A_PRIMARY;
  - B_INSTITUTIONAL;
  - D_ORIGINATOR;
- a non-empty editorial source policy.

Generated Verified Overview content never receives REVIEWED / REVIEWED_TRANSLATION status.

## Consumer behavior

### Today

“Today in 30 seconds” now has complete launch-catalog coverage:
- use localized Rich Editorial summary when available;
- otherwise use the localized Verified Overview.

### Detail

When Rich Editorial is absent:
- the old generic “editorial article coming next” placeholder is not rendered;
- the user sees a clearly labelled Verified Overview;
- authority, market and source cards remain visible immediately below it.

Rich Editorial behavior is unchanged for the reviewed records.

## Localization / code hygiene

All reusable consumer copy is centralized in ARB localization resources.

The structured verified-overview domain record contains data only:
- observance id;
- locale;
- localized title;
- canonical scope;
- authority name;
- verification date.

No translated prose is stored in the domain model.

## Regression coverage

Automated tests verify:
- every launch record produces a Verified Overview in all six locales;
- every overview preserves localized title, authority, scope and non-empty verification date;
- Rich Editorial master remains exactly the existing 28-record reviewed layer;
- a non-rich record renders Verified Overview rather than the old placeholder;
- Today renders a concise verified fallback when Rich Editorial is absent;
- reviewed editorial locale parity remains intact.

## Automated validation

Development checks #205 on functional head 128ab9c0d2a52c2102f347170b51ed0c55b0d18c:

- dataset/content validators: PASS;
- localization generation: PASS;
- Flutter analyze: PASS;
- Flutter tests: **80/80 PASS**;
- Web release build: PASS;
- Android ARM64 PR step: skipped by workflow design.

The workflow itself was superseded by later documentation-only pushes after the Web step had already passed, so GitHub reports the run as cancelled even though every executed validation step completed successfully.

A final CI run on the complete PR head is still required before squash merge.

## Verdict

Phase C v1 content-understanding implementation is complete once the final PR head is green.

The release blocking sequence is now E -> F -> I -> J -> K.
