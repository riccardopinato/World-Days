# World Days — local civil-day / DST repair

Baseline: main@474fdc405217bf05ab28bd250b2e613c86e0506e

DateTime.add(Duration(days: 1)) is elapsed-time arithmetic, not a local
calendar-day shift. During Europe/Rome DST changes a civil day is 23 or 25h.

The new LocalCivilDay adapter (Golden CivilDate ISO keys) is consumed by
Today/Tomorrow, Calendar upcoming/weekday headers, the per-date occurrence
index, ReminderPlanBuilder and the 45-day Home Widget projection.

The app shell schedules a timer until the next actual local midnight and
observes foreground resume. It refreshes the Today screen/streak and
native retention projection after date rollover; the daily quiz is keyed
by civil date to clear a previous answer.

CI adds timezone-isolated Flutter date/retention tests in Europe/Rome:
2026-03-29 (23-hour day), 2026-10-25 (25-hour day), year rollover,
leap day 2028, unique reminder IDs, wall-clock delivery and widget dates.

Release constraints: no data schema, permissions, billing or monetization
change. Android notification delivery and overnight widget rollover are
NOT physically certified by Flutter tests; Phase F/J remain open.
