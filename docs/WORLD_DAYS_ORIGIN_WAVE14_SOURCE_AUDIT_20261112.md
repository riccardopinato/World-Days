# Editorial origin Wave14 — 16 new EN/IT histories (2026-11-12)

Status: **branch research draft, not merged or human-certified**. App Factory baseline read once: Master v27, Golden Index v29, Registry v2; main baseline `309536f9ba7015f6f22bf293f2c8679b92de163d`. This report never retroactively increases main coverage.

## Completed in this wave (16 existing canonical IDs)

| Original 100-draft queue position | Canonical ID | Formal introduction | First observed (only when proven) |
|---:|---|---:|---|
| 20 | international-day-for-the-right-to-the-truth-concerning-gross-human-rights-violations-and-for-the-dignity-of-victims | 2010 | Unknown |
| 21 | international-day-of-remembrance-of-the-victims-of-slavery-and-the-transatlantic-slave-trade | 2007 | 2008 annual UN observance |
| 23 | international-day-for-mine-awareness-and-assistance-in-mine-action | 2005 | 2006 |
| 24 | international-day-of-conscience | 2019 | Unknown |
| 25 | international-day-of-reflection-on-the-1994-genocide-against-the-tutsi-in-rwanda | 2003 | 2004 |
| 26 | international-day-of-human-space-flight | 2011 | Unknown |
| 27 | world-art-day | 2019 UNESCO | Unknown earlier IAA origins |
| 29 | world-creativity-and-innovation-day | 2017 UN | 2002 pre-UN |
| 31 | international-mother-earth-day | 2009 UN | Unknown; Earth Day predates proclamation |
| 32 | international-day-of-multilateralism-and-diplomacy-for-peace | 2018 | 2019 |
| 33 | international-chernobyl-disaster-remembrance-day | 2016 | 2017 |
| 35 | world-tuna-day | 2016 | Unknown |
| 36 | world-portuguese-language-day | 2019 UNESCO | CPLP date established 2009, first event unknown |
| 38 | international-day-of-argania | 2021 | 2021 |
| 39 | international-day-of-plant-health | 2022 UN | 2022 |
| 40 | international-day-of-living-together-in-peace | 2017 | Unknown |

Every source URL is attached per record in `data/editorial/batches/origin_stories_wave14_20261112.json`. Italian and English each contain original narrative, separately attributed promoter, purpose and 3–4 facts. Precise date rationale is stated only where substantiated. No claim that EN/IT is human-reviewed. ES/FR/DE/PT require translated drafts and qualified native review.

## Not silently skipped — needs separate individual source investigation

- **#22 `international-day-of-solidarity-with-detained-and-missing-staff-members`**: catalog reference A/RES/49/59 concerns safety of UN staff; not sufficient by itself to certify the exact day origin or first commemoration. Investigate UN staff solidarity/Alec Collett original historical documents.
- **#28 `international-wellness-day`**: new A/RES/80/249; original act, exact adoption date, proposer and first observance not individually checked in this run.
- **#30 `international-day-of-greening-the-planet`**: new A/RES/80/300; same documentary checks still needed.
- **#34 `international-day-in-memory-of-the-victims-of-earthquakes`**: A/RES/79/285; original adoption and rationale require a dedicated check.
- **#37 `time-of-remembrance-and-reconciliation-for-those-who-lost-their-lives-during-the-second-world-war`**: A/RES/59/26 refers to both 8 and 9 May; reconcile canonical fixed-date model before writing a history that could misstate the observance.

All five remain incomplete and should be revisited when individual primary evidence is verified. Next sequential draft is **#41** after those deferred items; do not mistake deferred for certified.

## Acceptance gates

1. Generate dataset, origin index, and completion waves from this exact branch.
2. Run every relevant Python validator including `tool/validate_origin_100_original_drafts_20261112.py` and `tool/validate_editorial_origin_completion_waves.py`.
3. Run Flutter analyze/tests and Web release build from the same head.
4. Reconcile review threads, acquire qualified editorial/native-language reviews, and merge only when all protection gates pass. No APK, Play Store or production deploy.
5. **After merge**, recompute official main coverage. Conditional only: 55 existing + 16 unique additions = 71 source-researched origins, pending 1,040 of 1,111, *if* all are accepted without collision.
