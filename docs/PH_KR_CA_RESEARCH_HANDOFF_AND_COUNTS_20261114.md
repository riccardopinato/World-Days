# World Days — PH/KR/CA research handoff and backlog exclusion (2026-11-14)

This is **research progress reconciliation**, not qualified six-language editorial certification.

## Pinned evidence

- Catalog/main baseline: `e7c9fa0fbd2e82002d294ffe348f8a57bc1bf5ab`, 1111 IDs, 325 source-researched IT/EN histories.
- Candidate scope: PR #120 at `957565e7f5467b778a6a7638ab74b1a0c6f6d127`, researched candidates: 180 of initial 333.
- Source dependencies: PR #118 `d1440f6d8ec5b7f427dc4407d364ad90f2308283`; PR #119 `3ece3c825efb6fe7e6ac42182c334e9dcd90f5f0`; PR #120 above.
- Machine ledger: `data/editorial/registry/ph_kr_ca_source_research_handoff_20261114.json`.
- This is a pinned, static snapshot: update the ledger when a source PR changes materially. These PRs are draft/unmerged.

## Counts and interpretation

| Country | Retained for research | Six-locale AI origin drafts | Still missing a draft | Excluded biographies |
|:--|--:|--:|--:|--:|
| Philippines | 91 | 84 | 7 | 153 |
| South Korea | 57 | 57 | 0 | 0 |
| Canada | 32 | 32 | 0 | 0 |
| **Total** | **180** | **173** | **7** | **153** |

**173** exact canonical IDs are excluded from **new narrative drafting**; they remain pending qualified historical and native-language editorial review (173/173). **None** of these 173 are certified as reviewed editorial or published to runtime.

**18** of the 173 are six-locale extensions of the Wave20 IT/EN origins already counted in main. Only **155** are additional unique origin research drafts relative to main. The **153** biographies are excluded from the *editorial work scope*, not deleted from canonical app data and not described as completed.

With the main snapshot unchanged: `1111 - 325 main-researched - 155 external-new - 153 scoped-out = 478` still requiring original research in the current editorial scope. The seven Philippine blockers are included in the 478.

The source branch may later merge, at which point the queue computes union-by-exact-canonical-ID and does not double-count. Handoff source references must be refreshed after changed PR heads. Future catalog additions or source merges require regeneration and revised expectations.

## Non-negotiable gates

The machine metadata/locale-schema checks do not prove independent accuracy, legal recurring status, language quality, copyright clearance, or publication rights. All 173 dossiers remain human-unapproved. The seven source-blocked Philippine IDs require identity/date/legal authority resolution. Do not set `runtimeRichEditorialApproved=true` or merge/publish the content PRs merely because this metadata handoff passes CI.

No catalog entries, app runtime, user data, APKs, or web deployments are modified by this bookkeeping PR.
