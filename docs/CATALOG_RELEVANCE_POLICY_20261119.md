# World Days — Catalog relevance policy (19 November 2026)

## Product boundary
World Days is a lightweight, visual and descriptive discovery app for world, international, official national, civic and thematic observances, plus notable cultural campaigns lasting a day, week or month. It is **not** a daily biographical birthday/death almanac.

### Include
- World/international observances, and source-backed national observances with an understandable civic, cultural, historical, environmental, educational, health or social theme.
- National independence, constitutional, remembrance and institutional commemorations with public civic meaning.
- Recognized cultural months/weeks and campaigns, transparently described as such, not misrepresented as general paid public holidays.
- Person-named established civic remembrance days such as MLK Day or a formal memorial day. Distinguish founding act, annual date and earlier historical event.

### Exclude from published app
- **Personal birth and death anniversaries**, including those of National Artists, National Living Treasures, writers, individual presidents and politicians, when a cultural institution merely lists a birth/death date. A calendar reference does not prove the anniversary is a national observance.
- Equivalent low-value biographical anniversaries in future imports unless supported by distinct public commemorative designation and a compelling editorial rationale.

### Retain separately
- Original source records and provenance remain in `data/market/`. Never delete source research to remove a record from the consumer-facing catalog.
- A deterministic post-generation curation script applies published-scope exclusions to `assets/data/official_core.json`, 2026 occurrences/index, six editorial locales, and the runtime origin index. The untouched historical **1,111 ID research source snapshot** is still subject to the original staging validators. The **958 ID published consumer catalog** is a separate, deliberately smaller number.
- Include explicit exclusion reason, canonical ID, original authority and primary source in the generated audit archive.
- Future imports must never revive excluded IDs in the app simply by regenerating the source dataset; publication filter runs for all build paths.
- Do not remove individual records from source-only audit logs, research dossiers, or old PR history.

### Completeness claims
A record can have complete EN/IT/ES/FR/DE/PT descriptive coverage and still have an unresearched specific historic founding. Track **editorial locale completeness** and **documented individual origin** separately; avoid passing templated contextual copy off as a factual origin story. AI translation and proportionate validation are sufficient for normal low-risk editorial use; professional translators or historians are not universal gates.

### Initial 2026-11-19 implementation
- 144 NCCA personal birth/death anniversaries from Wave11 + 9 biographical birthday/death IDs from Wave10 = **153 excluded**.
- 1,111 archival source IDs - 153 = **958 published IDs**.
- All six editorial locale packs retain 958 entries, while 519 prior richer editorial entries are preserved; **439 records remain contextual** and require further original event/founding research, not translation completion.
- Strict product QA and CI gates assert ID parity, real source pointers, absence of excluded IDs in active calendar, and no accidental loss of prior richer articles.

