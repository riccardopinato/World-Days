# World Days — Remote Content Pack v1

Status: **Phase G + G.1 implementation complete**. Store/release certification remains governed by the exact-artifact gates in `ROADMAP.md`.

## Purpose

World Days remains local-first. The bundled catalog is always a usable fallback.
Remote packs only update canonical/catalog/editorial content without requiring a
new app release.

The remote channel never stores or owns user data. Favorites, reminder
preferences, streaks, theme/language/market choices and Remove Ads entitlement
stay outside the pack lifecycle.

## Hosting

Production manifest:

`https://riccardopinato.github.io/World-Days/content/manifest.json`

Payloads are immutable versioned JSON files under:

`https://riccardopinato.github.io/World-Days/content/`

GitHub Pages deployment publishes the generated content directory together with
the Web Preview.

## Manifest contract

Schema v1 fields:

- `packId = world-days-catalog`
- `version`
- `kind = catalog`
- `sizeBytes`
- `sha256`
- HTTPS `payloadUrl`
- `generatedAt`

Runtime rejects:
- unsupported schema/pack IDs;
- unsafe version strings;
- payload URLs outside the pinned `https://riccardopinato.github.io/World-Days/content/` origin/path;
- unexpected payload filename shapes, query strings or fragments;
- non-hex SHA-256 values;
- zero/oversized packs;
- source/provenance records without verification metadata;
- size mismatches;
- checksum mismatches;
- payloads that fail catalog parsing/domain validation;
- pack-version vs canonical dataset-version drift.

The v1 safety cap is 5 MiB. The mobile transport now streams response chunks
through a hard byte cutoff derived from the manifest before the JSON bytes are
materialized, so an origin cannot exceed the declared download budget merely
by returning a larger body.

## Pack contents

The payload contains the generated:
- canonical `official_core.json`;
- 2026 occurrence index;
- reviewed editorial packs EN/IT/ES/FR/DE/PT.

Because `official_core.json` carries `yearOverrides`, the same channel also
updates annual campaign/theme metadata and authoritative date overrides.

## Runtime lifecycle

1. App starts from bundled content unless a previously verified active pack is
   available.
2. Stored active bytes are re-verified before use.
3. If the active pack is corrupt, the manager attempts the previous verified
   version.
4. Manifest checks run asynchronously and never block local startup.
5. Payload bytes are streamed through a hard maximum equal to the signed-off
   manifest size and stay inactive until size, SHA-256 and catalog validation
   all pass.
6. Versioned payload/manifest files are written first.
7. A small active/previous pointer switches only after successful validation.
8. A crash-safe pointer backup preserves the last usable pointer if activation
   is interrupted.
9. Old content files are purged after a successful swap, keeping active and
   previous versions.
10. If no valid stored version exists, World Days falls back to immutable
    bundled assets.

## User experience

On supported mobile platforms, Settings exposes Content updates:
- check for updates;
- update available state;
- download/verifying state;
- install update;
- active version.

Web deliberately uses the bundled catalog only. The Web build does not claim
filesystem persistence parity with Android/iOS.

## Native requirements

Android requires INTERNET permission. The generated platform scaffold is
configured by `tool/configure_native_content_pack.py` and CI validates it with
`tool/validate_native_content_pack.py`.

iOS uses HTTPS only and requires no ATS exception for the GitHub Pages endpoint.

## CI / release evidence

`tool/build_content_pack.py` deterministically creates the payload and
manifest from generated catalog assets.

`tool/validate_content_pack.py` validates:
- manifest shape;
- HTTPS hosted payload path;
- byte size;
- SHA-256;
- required files;
- record identity integrity;
- occurrence/editorial references;
- source + verification metadata;
- approved payload origin/path and filename shape.

Flutter tests cover:
- clean verified install;
- bundled-version no-op;
- checksum mismatch;
- manifest network failure;
- payload network failure;
- rollback from corrupt active content;
- offline/bundled fallback;
- unsafe/off-origin manifest rejection;
- hard streamed byte-cap overflow;
- actual World Days content-pack decoding and version coherence.

## Explicit v1 boundaries

- JSON pack download is intentionally small, streamed and hard-capped;
  resumable large-file transfer is not needed.
- Web stays on bundled content.
- No content update can mutate user-owned state.
- The remote channel is not a code/config execution channel.
- Content quality/provenance remains governed by the existing editorial/data
  policies; checksum verification proves integrity, not truthfulness.


## Phase G.1 release parity

Signed Android QA and Production Android Release both execute the same
content-pack build/validation and native-network validation gates used by
development CI.

After GitHub Pages deploys, `tool/smoke_remote_content_pack.py` polls the
public manifest until the new version propagates, then verifies the public
payload byte length, SHA-256, version and pack identity against the locally
generated manifest. This closes the gap between build-time validation and the
actual hosted content channel.
