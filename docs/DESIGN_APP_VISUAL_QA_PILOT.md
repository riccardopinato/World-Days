# Design-App Visual QA real-screen pilot — World Days

Status: IMPLEMENTED_PENDING_CI (do not claim device certification).

Source: `riccardopinato/Design-App@8c49dda98f8a074abac2ae84262d7e3948ab6324`
Visual QA v0.1 harness. This test adapts the 9-scenario concept to a genuine
first-party widget **ObservanceCard**, with real World Days theme, localization,
data model and onTap/onFavorite callbacks.

No production source, runtime dependency, entitlement, AdMob, catalog or
notification behavior is changed. This is test-only adoption.

Test: `test/ui/design_app_visual_pilot_test.dart`.

Evidence to collect:
- CI `flutter analyze` and `flutter test` exact PR head;
- responsive sizes 360/412/800/landscape, 1.6 and 2.0 text, dark, safe/IME;
- actual localized long Italian title, favorite and click interactions;
- Web/Android build gates preserved by existing app workflows.

Not verified by widget tests:
- Android/iOS physical rendering and touch;
- keyboard input method interaction, cutouts, screen readers;
- new APK size impact (test-only source has no runtime code);
- full app-navigation states or screenshot pixel baseline for this component.

Promotion of Design-App Visual QA from LIBRARY_VERIFIED to COPY_READY
requires independent review of this CI evidence and relevant Golden requirements.
