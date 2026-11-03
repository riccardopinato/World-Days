# Golden Factory v28 — CivilDate consumer pilot (World Days)

Scope: non-visual, no new permission/storage/network/billing/release contract.
Preserves public RecurrenceEngine API and published observance behavior.

Source of vendored reference:
App-Factory-Core/reference_engines/lib/src/civil_date.dart
original Git blob: bc85a8848dc563ea148ec979f05b1a7bc72816e3
donor references: World-Days@622e5c2f00c08b0905207c6765c9b51e199e706f
and Anna's Diary@827bb61620960d8867eb03e453d142013aada786.
The vendor file is copied byte-identical, not a new runtime Git dependency.

Actual app integration: lib/domain/recurrence_engine.dart delegates fixed dates,
nth weekday, last weekday and last-day-of-month to the reusable Golden date
reference while keeping World Days-specific recurrence rule classes, authority
overrides, one-off/cross-year semantics and public result type unchanged.

Gate: `flutter analyze` + `flutter test` + Web build in World Days CI on the
exact PR head, plus focused consumer parity test. Provenance and runtime boundary
are recorded separately; not device/notification/provider certification.
If successful, this is first consumer source-integrated pilot, not evidence
that GPX or all possible recurrence policies work on production devices.
