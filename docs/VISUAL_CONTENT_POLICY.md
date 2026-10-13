# World Days — Visual Content Policy

Step 8 baseline: 2026-10-13

## Purpose

World Days uses a visual editorial identity without turning the app into a heavy image bundle or making core browsing depend on the network.

The runtime baseline is first-party procedural artwork generated in Flutter from a small canonical `visualKey` taxonomy.

## Canonical visual keys

- `planet`
- `health`
- `people`
- `learning`
- `culture`
- `food`
- `future`
- `community`

Every publishable observance must resolve to one of these keys. The dataset generator assigns the key deterministically and validation rejects unknown or missing keys.

## Runtime rules

1. Today, cards, detail screens, themed collections and share cards must have a complete offline visual fallback.
2. Do not bundle one photograph per observance.
3. Procedural artwork is the default because it is lightweight, theme-safe and attribution-free.
4. Real photography is optional enhancement content, never required for canonical data or navigation.
5. A failed/missing media asset must fall back to the observance visual key without changing factual content.

## Photography provenance gate

No third-party photograph may ship unless the asset has an auditable manifest entry containing:

- asset ID
- source page URL
- original file URL
- creator / rights holder
- license name or SPDX identifier when available
- license URL
- required attribution text
- retrieval date
- SHA-256 of the shipped derivative
- derivative/edit notes
- mapped observance IDs or visual keys
- runtime usage surface

Default acceptable classes are owned assets, public domain, CC0 and CC BY with preserved attribution. CC BY-SA or other reciprocal/restrictive licenses require a separate compatibility review before shipping. Unknown-license images, copied social-media images, logos and campaign artwork are excluded unless explicit rights exist.

## Weight and delivery

Selected photos must be resized and compressed before shipping. Prefer a small reusable visual pack over hundreds of unique files. Future remote visual packs must remain optional, versioned and integrity-checked; the procedural fallback remains bundled.

## Share cards

Share cards are generated locally as 4:5 PNGs from first-party procedural artwork and app typography. Third-party photography is intentionally excluded from generated share cards unless attribution and redistribution rights can travel with the exported asset.

## Current Step 8 truth

This Step 8 ships the procedural visual system, themed collections and locally generated share cards. It does not silently bundle external photography. The repository is photo-ready through this provenance gate; any later curated photography pack must add its manifest and pass license review before merge.
