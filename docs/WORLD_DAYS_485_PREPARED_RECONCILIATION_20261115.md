# World Days — reconciliation of all 485 prewritten unique historical stories

Date: 2026-11-15
Factory baseline: App-Factory-Core @ c5adc147046beb7024629466d10eeb799c3c2619
Catalog baseline: 1111 canonical unique observance IDs.

## Identity-based counting, not arithmetic on translation drafts

| Dataset | Historical source-linked IDs | What this count means |
| --- | ---: | --- |
| 21 original history batches already on main (primary + Wave01 through Wave20) | 325 | Unique EN/IT source-research dossiers; not 325 six-locale human approvals |
| 173 PH/KR/CA source-SHA-pinned AI certifications previously merged in #133/#134 | 173 | Six-locale AI reviewed; zero independent human signoffs |
| Overlap between the previous two groups | -18 | Same canonical IDs from Wave20; counted only once |
| First five country histories in open PR #122 (CZ/SK/IT/FI/EE) | +5 | New canonical IDs, six-locale originals; research source-review, not human certified |
| **Total prepared unique historical stories** | **485** | 325 + 173 - 18 + 5; 626 additional canonical IDs do not have a source-researched story in this exact inventory |

## Integration architecture

- Retain all **56 original legacy Rich Editorial** articles; do not treat them as new origin dossiers.
- Retain all **173 AI_CERTIFIED** in six locales with original pinned sources, including corrections of Raoul Wallenberg, Panagyaman and W.A.T.C.H.
- Add precisely **82** non-overlapping six-locale Wave20 histories from frozen PR #118 SHA `47cff4c5b22e55156e9444a3240511530a6f01f9`. English and Italian texts and source/year fields must match main Wave20 byte-for-byte after JSON decode. One qualifying correction removes unnecessary speculative 1994 first-ceremony wording in four other locales for the Carpathian-Dukla remembrance; source remains immutable. They are `AI_SOURCE_REVIEWED_SIX_LOCALE`, not human certified.
- Add **5** six-locale national histories from PR #122 at source HEAD `00801cae31957e48166ccd2c760883fd0f96171f`, retaining verified founding-year-versus-history distinctions. They are also `AI_SOURCE_REVIEWED_SIX_LOCALE`.
- The rich editorial count becomes **56 + 173 + 82 + 5 = 316** across EN/IT/ES/FR/DE/PT, subject to CI and merge.
- Existing **325** primary-source EN/IT history dossiers are already generated into bundled `assets/data/origin_review_index.json`, but historically blocked from visibility. Enable the explicitly labelled **research preview**, only for these 325, and hide it if that ID already has one of the 316 Rich Editorial articles. For ES/FR/DE/PT, display the available English source narrative with a visible fallback notice, *never* pretend the source is translated.
- Never set `runtimeRichEditorialApproved=true` for raw research. The new separate `runtimeResearchPreviewAllowed` flag requires real `primaryResearch`, supporting URLs and `PRIMARY_RESEARCHED_ORIGIN_IT_EN` status.
- Publication/certification levels are separate: existing source research, AI source/locale review, AI certified, independently human certified, CI, runtime build, Store release. These flags are not interchangeable.

## Validation

- `tool/publish_prepared_sixlocale_87.py`: exact snapshot identity, all 82 EN/IT main equality, five national dossier identities, all six narrative fields, source links, no duplicate IDs, chronological year parity and explicit corrections.
- `tool/validate_prepared_485_reachability.py`: 325 source dossiers, 173 certificates, 18 overlaps, 5 new IDs, 485 unique prepared, 316 Rich Editorial, 325 source-preview eligible, no unauthorized rich approval and six-language parity.
- `tool/validate_origin_runtime_approval_gate.py`: research preview cannot silently promote raw drafts to qualified Rich Editorial.
- Flutter data test validates 87 additional six-locale entries and the persisted 173 AI certifications.
- Dataset/content-pack version: `2026.11.15.2`. All generated content is preserved offline; no new remote provider. No automatic public Web Preview deployment or Play Store publishing.

## What this does NOT close

- **Not all 485** have individually verified native human translations and independent fact signoff. Remaining older EN/IT original-history dossiers must be translated/reviewed in ES/FR/DE/PT before labeling them six-locale certified.
- **7 Philippine source/identity conflicts** outside the 173 remain blocked; do not fabricate their dates or initial legislation.
- Earlier research-only PRs (#118/#119/#120/#122) remain open unless explicitly merged later; copied frozen source stories do not imply merging those entire PRs.
- **626 catalog IDs** outside this prepared historical-story inventory still need true individual historical authoring, source verification, translations and release gates. They have canonical source metadata/overview only.
- Runtime verification requires exact-head CI green; APK signing/physical review and Web deployment remain distinct.

This ledger is a content inventory and build integration record. Do not cite it as an independent human history review, physical-device certification or proof of public availability.

## Remote-pack size optimization (15 November 2026)

The CDN content pack retains the **5 MiB** limit unchanged. To avoid re-transmitting six copies per story of audit-only SHA/head/source URL metadata which `EditorialEntry.fromJson` never reads, `tool/build_content_pack.py` removes only `aiEditorialProvenance` from the remote payload. Full audit metadata and all localized prose/facts remain in the **bundled generated editorial JSON** and the **immutable Git review ledgers**; remote and bundle equality is validated after removing just that field. This preserves all displayed facts and does not weaken the source gate or increase the size cap.
