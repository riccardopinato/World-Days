# World Days agent instructions

Source of product truth: `docs/PRODUCT_BIBLE.txt`.
Source of execution truth: `ROADMAP.md`.
App Factory baseline for this repository bootstrap: `App-Factory-Core@5f6b2489df2ac85fb85ccfea059983a090689de4`.

Rules:
- Flutter/Dart is the default stack.
- English is the canonical editorial language; UI supports EN/IT/ES/FR/DE/PT.
- Local-first: the bundled catalog must remain useful without network access.
- Never promote discovery records to official without primary/originator verification.
- Provider-sensitive features must fail closed and use test/sandbox configuration in development.
- Web Preview proves shared UI/navigation only; it does not certify native capabilities.
- Keep `main` stable; use PRs for substantive changes.
- Update README/ROADMAP whenever product state materially changes.
- Visual content keeps a lightweight offline fallback; third-party media requires explicit license/provenance metadata.
