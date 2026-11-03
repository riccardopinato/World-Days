# World Days — Design-App Visual QA adoption on current main

Original donor concept: riccardopinato/Design-App@8c49dda98f8a074abac2ae84262d7e3948ab6324.
Previously unmerged test-only pilot #34 is superseded by this clean current-base adoption.

The real `ObservanceCard` is tested with 8 responsive scenarios:
360x800, 412x915, 800x1200, landscape, dark, 160% and 200% text,
keyboard/safe-area insets. A ninth test checks Italian localized
favorite/navigation actions. No screenshot pixel baseline is claimed.

Normal Flutter navigation receives a WidgetOrderTraversalPolicy focus
group in both standard phone and wide NavigationRail; the existing
large-text compact navigation retains explicit numeric focus order and
>=48dp touch targets. Tests confirm all three navigation layouts.

The existing `integration_test/app_smoke_test.dart` journey stays
maintained but is **not** run on headless GitHub Linux/Web: Flutter
3.47 reports "Web devices are not supported for integration tests yet"
(run #41625795376). It requires a connected Android device/emulator
and an explicitly recorded Phase F/J device test. The ordinary
Flutter widget/navigation suite remains a required CI check.

**Certification boundary:** widget/integration host tests cannot certify
Android real launcher, screen reader, UMP, Play Billing or notification
delivery, and do not replace exact-artifact Phase F/J testing.
