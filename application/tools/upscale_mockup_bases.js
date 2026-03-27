#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

let sharp;
try {
  sharp = require("sharp");
} catch (_err) {
  sharp = require("/srv/artlomo/video_worker/node_modules/sharp");
}

const DEFAULT_ROOT = "/srv/artlomo/application/mockups/catalog/assets/mockups/bases";
const TARGET_SIZE = 2048;

function parseArgs(argv) {
  const args = {
    root: DEFAULT_ROOT,
    dryRun: false,
    limit: 0,
    verbose: false,
  };

  for (let i = 2; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--dry-run") {
      args.dryRun = true;
      continue;
    }
    if (arg === "--verbose") {
      args.verbose = true;
      continue;
    }
    if (arg === "--root" && i + 1 < argv.length) {
      args.root = path.resolve(argv[++i]);
      continue;
    }
    if (arg === "--limit" && i + 1 < argv.length) {
      const n = Number(argv[++i]);
      args.limit = Number.isFinite(n) && n > 0 ? Math.floor(n) : 0;
      continue;
    }
  }

  return args;
}

function walkPngs(rootDir) {
  const files = [];
  const stack = [rootDir];
  while (stack.length > 0) {
    const current = stack.pop();
    const entries = fs.readdirSync(current, { withFileTypes: true });
    for (const entry of entries) {
      const full = path.join(current, entry.name);
      if (entry.isDirectory()) {
        stack.push(full);
      } else if (entry.isFile() && entry.name.toLowerCase().endsWith(".png")) {
        files.push(full);
      }
    }
  }
  files.sort();
  return files;
}

async function upscalePng(filePath, dryRun, verbose) {
  const instance = sharp(filePath, { limitInputPixels: false }).rotate();
  const meta = await instance.metadata();
  const beforeW = Number(meta.width || 0);
  const beforeH = Number(meta.height || 0);

  if (beforeW <= 0 || beforeH <= 0) {
    throw new Error("Invalid image dimensions");
  }

  const alreadyTarget = beforeW === TARGET_SIZE && beforeH === TARGET_SIZE;
  if (alreadyTarget) {
    return { changed: false, skipped: true, beforeW, beforeH, afterW: beforeW, afterH: beforeH };
  }

  if (!dryRun) {
    const tmpPath = `${filePath}.tmp-upscale-${Date.now()}`;
    await instance
      .resize({
        width: TARGET_SIZE,
        height: TARGET_SIZE,
        fit: "fill",
        kernel: sharp.kernel.lanczos3,
      })
      .png({
        compressionLevel: 9,
        adaptiveFiltering: true,
        palette: false,
        force: true,
      })
      .toFile(tmpPath);

    fs.renameSync(tmpPath, filePath);
  }

  if (verbose) {
    process.stdout.write(`upscaled: ${filePath}\n`);
  }

  return { changed: true, skipped: false, beforeW, beforeH, afterW: TARGET_SIZE, afterH: TARGET_SIZE };
}

async function main() {
  const args = parseArgs(process.argv);
  if (!fs.existsSync(args.root) || !fs.statSync(args.root).isDirectory()) {
    throw new Error(`Root directory not found: ${args.root}`);
  }

  const allPngs = walkPngs(args.root);
  const targets = args.limit > 0 ? allPngs.slice(0, args.limit) : allPngs;

  let changed = 0;
  let skipped = 0;
  let failed = 0;

  process.stdout.write(`Root: ${args.root}\n`);
  process.stdout.write(`Found PNGs: ${allPngs.length}\n`);
  process.stdout.write(`Processing: ${targets.length}${args.dryRun ? " (dry-run)" : ""}\n`);

  for (const file of targets) {
    try {
      const result = await upscalePng(file, args.dryRun, args.verbose);
      if (result.skipped) {
        skipped += 1;
      } else if (result.changed) {
        changed += 1;
      }
    } catch (err) {
      failed += 1;
      process.stderr.write(`ERROR ${file}: ${err && err.message ? err.message : String(err)}\n`);
    }
  }

  process.stdout.write(`Done. changed=${changed} skipped=${skipped} failed=${failed}\n`);
  if (failed > 0) {
    process.exitCode = 1;
  }
}

main().catch((err) => {
  process.stderr.write(`${err && err.message ? err.message : String(err)}\n`);
  process.exit(1);
});
