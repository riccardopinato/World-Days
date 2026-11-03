# Phase G runtime follow-up: bounded manifests and rollback resistance

Proposed hardening:
- Manifest HTTP GET is streamed and limited to 64 KiB, like payload
  streaming already bounded to its advertised size.
- HTTP redirects are disabled for both endpoints; unexpected 3xx is an
  error rather than following requests to an unapproved origin.
- Dotted numeric remote catalog versions older/equal to the current
  active/bundled catalog cannot be installed (stale CDN rollback defense).
- Fixture tests cover normal manifest, overflow, redirect rejection and
  numeric version 2026.10.14.9 versus 2026.10.14.10.

Offline bundled fallback, SHA-256 validation and rollback to a previously
verified local version remain unchanged. No code/config execution path
is introduced.
