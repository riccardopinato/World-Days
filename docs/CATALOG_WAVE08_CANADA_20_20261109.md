# Wave08 Canada — 20 federal commemorations (batch integration, 9 Nov 2026)

**Technical metadata only. Not a statement that all twenty are public/statutory leave days.**

## Rollout mathematics

`main` remains **456** official catalog IDs. Consolidated PR #67 carries 16 UNESCO/Japan/India metadata entries and these **20** additional Canadian commemorations, for a **492-ID proposal** (285 global + 207 national), across the same 28 selectable markets. Canada increases from five to **25** national records. The 456 previous IDs must remain unchanged.

## Government/originator evidence

Canadian Heritage lists the dates by month on a *single* official government commemorative calendar: https://www.canada.ca/en/canadian-heritage/services/important-commemorative-days.html. This is **one original document covering 20 records**, not 20 statistically independent websites. For some commemorations, more precise original documents are attached to the record: National Ribbon Skirt Day federal act (2022) https://laws-lois.justice.gc.ca/eng/acts/N-16.2/section-2.html ; Sir John A. Macdonald Day Canadian Heritage Act explainer https://www.canada.ca/en/canadian-heritage/services/important-commemorative-days/sir-john-macdonald-day.html ; January 29 Québec mosque attack proclamation, Persons Day, September 28 British Home Child Day House motion and December 6 memorial proclamation. The Canadian Heritage calendar includes all 20 exact month/day entries.

`data/market/wave08_canada_twenty_20261109.json` lists per-record canonical ID, first-party URLs, the **fixed Gregorian recurrence** (the same 2026–2028 calendar day), six EN/IT/ES/FR/DE/PT draft titles, country and source. New entries are all **national commemorations**; this is not a claim that they are statutory public days off, and none is created as GLOBAL or for other countries.

**Exactly 20 distinct subjects:** National Day of Remembrance for Victims of Air Disasters; Sir John A. Macdonald Day; Québec City Mosque Attack and Action against Islamophobia Remembrance Day; National Indigenous Languages Day; Vimy Ridge anniversary; Armenian Genocide Remembrance Day in Canada; British Home Child Day; Persons Day; Indigenous Veterans Day; National Day of Remembrance and Action on Violence Against Women; National Ribbon Skirt Day; Raoul Wallenberg Day; Lincoln Alexander Day; Red Dress Day; Dutch Heritage Day; National Day of Remembrance for Victims of Terrorism; Day of Commemoration of the Great Upheaval; Emancipation Day in Canada; National Seniors Day; Statute of Westminster anniversary.

Four research candidates excluded from this batch:
- Canadian Multiculturalism Day and National Acadian Day: **already in the 456-record baseline**.
- National Child Day: original government resource equates it with the global World Children's Day commemoration, so no second national identity added before semantic assessment.
- National Day of Observance for COVID-19: continuity/ongoing official designation still needs checking.

**Introduced year evidence:** National Ribbon Skirt Day **2022** (federal act); Sir John A. Macdonald Day **2002** (Canadian Heritage statement). All other 18 records have `introducedYear=null` and display `*`, since even documented historical event dates do not prove when a commemorative designation first began.

## Machine gates and human gates

- `tool/market_wave08.py`: validates all 20 identities, first-party hostnames, fixed 2026–28 dates, source evidence, six draft locale titles, introductory years, no false claims about public holiday status.
- `tool/validate_wave08_content.py`: inspects generated 492 records, country CA=25, full six-locale parity, original title and primary source, 2026 occurrence, STUB editorial status. Prior Waves05–07 remain validated.
- `tool/validate_dataset.py`, `tool/market_coverage.py`, Flutter catalog/around-world tests and release Web build are enforced in one CI on exact PR #67 head.
- **Mandatory editorial gate:** qualified verification of translations, culturally sensitive wording, and whether each national designation is editorially distinct from an existing global memorial. The Canadian government calendar does not automatically approve long-form stories. All 20 remain `STUB`; existing 56 reviewed narratives untouched.
- No merge, Android APK, signing, Play submission or production deploy without separate gates.
