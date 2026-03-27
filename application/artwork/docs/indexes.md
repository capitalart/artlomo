# Artwork indexes (authoritative)

Two JSON indexes govern processed artwork resolution. Do not scan directories or
infer filenames; always consult these files.

- `lab/index/artworks.json` — global map of SKU → processed folder + assets

  filename. Downstream systems must resolve SKU paths via this file before
  touching the filesystem.

- `<artwork_dir>/<slug-sku>-assets.json` — per-artwork declaration of required

  files (master, analyse, thumb, metadata, QC) plus the mockups subfolder. All
  paths are relative to `artwork_dir`; if a path is absent here it must be
  treated as non-existent.

Rules:

- Writes are atomic; callers must never patch these files in-place.

- If `artworks.json` is invalid JSON, abort and fix it before continuing.

- SKU keys are unique. Updating an existing SKU replaces the entry but cannot

  create duplicates.

- A `mockups/` directory is created for future phases but may remain empty. The

  assets file is authoritative from the moment it is written.
