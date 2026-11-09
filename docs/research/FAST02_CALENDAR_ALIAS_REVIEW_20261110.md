# FAST02 calendar + alias lane — research, not runtime

Baseline: World Days main 456, consolidated PR #67 proposes 492; research PR #64 classifies 24 duplicate records, 36 staged content entries, 84 further source-dated candidate records (22 lower risk and 62 complex), and nine Nepal records lacking PDF source verification.

This independent branch owns the **62 complex candidates**, not the legal/scope notes maintained in the other branch. It establishes a scalable classification process without inventing 2027–2028 dates.

## Source families requiring explicit adjudication

- **Lunar or lunisolar:** Seollal, Tết, Khmer New Year, Chuseok, Poya, Diwali/Deepavali, Buddha Purnima/Vesak, Eid. Two countries celebrating a shared religious festival are not automatically two separate global observances. Distinct local legal designations may be retained under national scope only when evidence supports their historical/official identity.
- **Astronomical:** Japanese spring/autumn equinox dates are officially proclaimed year by year. An estimated date is not an official 2028 occurrence.
- **Intercalary:** Sri Lankan Adhi Poson does not occur every solar year. Never auto-recur as fixed monthly event.
- **Regional/community:** Bangladesh Chaitra Sankranti applies to specified hill districts; Nepal Gai Jatra, Indra Jatra and Jitiya require local authority/scope.
- **Substitute leave:** a replacement weekday is not another festival ID. Independence Day, monarch birthdays and Eid leave ranges must remain one commemorative identity each.
- **Existing aliases:** 24 canonical duplicates already screened; preserve full-catalog generated-ID comparison.

## Gate to integrate

For each of 62 candidates, require source URL that names the commemorative event, candidate's country/scope and official annual occurrence or 2027–28 authority override, de-duplication decision versus the full 492 proposed catalog, six-locales draft titles and qualified editorial sign-off. If missing, leave research-only and show unresolved reason.

Use `tool/fast02_movable_alias_triage.py` for a deterministic per-record report and a failure on any accidental promotion. No APK, release or public deployment.
