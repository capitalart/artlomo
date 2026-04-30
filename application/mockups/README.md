# Mockup backend (Phase 1)

Deterministic, index-driven mockup generation. No UI, no routes.

## Invariants

- All path resolution flows through JSON indexes.

  - `lab/index/artworks.json` → locate processed artwork folder and assets file.

  - `<slug>-assets.json` (in the artwork folder) → locate required files (`*-ANALYSE.jpg`, metadata, QC, thumb) and declare the mockups subfolder.

- Never scan directories or guess filenames. If a path is not declared in an index, it does not exist.

- Artwork input is always `<slug>-ANALYSE.jpg` from the assets index. The print master is never used here.

- Hash = `sha256` over raw bytes of: analyse image + base PNG + coordinate JSON.

- Outputs are stable JPEGs: quality 95, subsampling 0, optimize False. Thumbs use long-edge 600px with Lanczos.

## Slot semantics

- `mode="generate"`: slot must be empty; hash mismatch (if provided) is an error; non-destructive.

- `mode="swap"`: slot must exist; old composite and thumb are deleted before writing the new ones; hash mismatches are expected.

- Slot keys are zero-padded (`"01"`, `"02"`).

## Coordinate schema

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}
```

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text
{
  "template": "Bedroom-Adults-01",
  "regions": [
    {"id": "primary", "corners": [TL, TR, BL, BR]},
    ... up to 6 regions
  ]
}

```text

Points must lie within the base PNG bounds. Phase 1 uses all regions with the same artwork.

## Generated assets

- Composite: `mockups/mu-<slug>-<slot>.jpg`

- Thumb: `mockups/thumbs/mu-<slug>-<slot>-THUMB.jpg`

- Slot entry (written atomically into `<slug>-assets.json`):

```text

Points must lie within the base PNG bounds. Phase 1 uses all regions with the same artwork.

