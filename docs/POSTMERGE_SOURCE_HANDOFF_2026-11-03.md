# World Days — post-merge source handoff, 2026-11-03

**Status: implementation merged; Store certification BLOCKED.**

## Source / governance

- PR #44 merged with squash commit:
  `7c67f553b371d5b5e7a1d04b629d8ef7aa3a6dbe`.
- All components (#39–#42) are included exactly once.
- Ruleset #26445843: active on default main, strict `validate`,
  requires PR and resolved conversations, blocks force-push/deletion,
  bypass empty. Issue #37 closed.
- Source `pubspec.yaml`: `0.4.0+4`. This is **not** an assertion that
  versionCode 4 is eligible for upload to the real Play account.

## Machine verification

- Integrated head CI:
  [Development #41630766103](https://github.com/riccardopinato/World-Days/actions/runs/41630766103)
  PASS (104 Flutter / 9 Europe/Rome / analyze / Web).
- Integrated Android admission:
  [#41630765848](https://github.com/riccardopinato/World-Days/actions/runs/41630765848)
  PASS (immutable pubspec.lock / non-production-signed ARM64 APK
  24,176,292 bytes, SHA-256
  `43279482a78019f116b0fd96a5826094447c794299f09103110d855afa04a31d`).
- For post-merge `main`, only the final result of
  [Development #41637425080](https://github.com/riccardopinato/World-Days/actions/runs/41637425080)
  and [Web deploy #41637424946](https://github.com/riccardopinato/World-Days/actions/runs/41637424946)
  counts, plus any actual downloaded `main` artifact.

## Owner-only / external gates

Use [issue #43](https://github.com/riccardopinato/World-Days/issues/43),
`docs/PLAY_PHASE_K_SUBMISSION_PREP_2026-11-03.md` and
`docs/PLAY_STORE_LISTING_DRAFT_2026-11-03.md` for the ordered plan.

Do not upload the PR/CI test APK as a Play release. To generate a
source-identical **signed** APK/AAB, dispatch the existing
`Production Android Release` from protected `main` only after the
Play versionCode is verified against all previous Play uploads and
the required secrets are present. The workflow fails closed if the
main protection gate is absent. Production APK/AAB must be verified
with `apksigner`, checksums and the generated manifest.

A green CI, branch protection or generated evidence document cannot
certify physical widget/notification delivery, Google Play billing
or published store declarations. Keep final verdict **NOT CERTIFIED**
until user-owned evidence is recorded.
