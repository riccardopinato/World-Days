# World Days agent instructions

Source of product truth: `docs/PRODUCT_BIBLE.txt`.
Source of execution truth: `ROADMAP.md`.
App Factory baseline for this repository bootstrap: `App-Factory-Core@47c47f49a7b46812e3bd6f1231c3524f2b52b826`.

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
