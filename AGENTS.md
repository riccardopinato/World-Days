# World Days agent instructions

Source of product truth: `docs/PRODUCT_BIBLE.txt`.
Source of execution truth: `ROADMAP.md`.
App Factory baseline for this repository bootstrap: `App-Factory-Core@fa3c0679de393f1cb13c2fed2be314d1a1269353`.

Rules:
- Flutter/Dart is the default stack.
- English is the canonical editorial language; UI supports EN/IT/ES/FR/DE/PT.
- Local-first: the bundled catalog must remain useful without network access.
- Never promote discovery records to official without primary/originator verification.
- Provider-sensitive features must fail closed and use test/sandbox configuration in development.
- Web Preview proves shared UI/navigation only; it does not certify native capabilities.
- Keep `main` stable; use PRs for substantive changes.
- Update README/ROADMAP whenever product state materially changes.
