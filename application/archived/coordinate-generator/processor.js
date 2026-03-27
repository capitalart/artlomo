"use strict";

const sharp = require("sharp");
const fs = require("fs/promises");
const path = require("path");

sharp.cache(false);

function parsePayload(rawArg) {
  if (!rawArg || typeof rawArg !== "string") {
    throw new Error("Missing JSON payload argument");
  }
  const parsed = JSON.parse(rawArg);
  if (!parsed || typeof parsed !== "object") {
    throw new Error("Invalid JSON payload");
  }
  return parsed;
}

async function generateUploadThumb(payload) {
  const srcPath = String(payload.src_path || "").trim();
  const destPath = String(payload.dest_path || "").trim();
  const longEdge = clampInt(payload.long_edge || 600, 1, 10000);
  const targetKb = clampInt(payload.target_kb || 100, 10, 50000);

  if (!srcPath || !destPath) {
    throw new Error("generate_upload_thumb requires src_path and dest_path");
  }

  await fs.mkdir(path.dirname(destPath), { recursive: true });

  let best = null;
  let quality = 85;
  for (let i = 0; i < 10; i += 1) {
    const out = await sharp(srcPath, { limitInputPixels: false })
      .rotate()
      .resize({
        width: longEdge,
        height: longEdge,
        fit: "inside",
        kernel: sharp.kernel.lanczos3,
        withoutEnlargement: true,
      })
      .jpeg({ quality, mozjpeg: true, progressive: true })
      .toBuffer();
    best = { quality, size: out.length, buffer: out };
    if (out.length <= targetKb * 1024 || quality <= 50) {
      break;
    }
    quality -= 5;
  }

  if (!best) {
    throw new Error("Unable to generate upload thumbnail");
  }
  await fs.writeFile(destPath, best.buffer);

  return {
    ok: true,
    action: "generate_upload_thumb",
    bytes: best.size,
    quality: best.quality,
    target_kb: targetKb,
  };
}

async function saveOriginalAsSeo(payload) {
  const srcPath = String(payload.src_path || "").trim();
  const destPath = String(payload.dest_path || "").trim();
  const buyerLongEdge = clampInt(payload.buyer_long_edge || 14400, 1, 50000);

  if (!srcPath || !destPath) {
    throw new Error("save_original_as_seo requires src_path and dest_path");
  }

  const srcExt = path.extname(srcPath).toLowerCase();
  await fs.mkdir(path.dirname(destPath), { recursive: true });

  const srcMeta = await metadataFor(srcPath);
  const srcLongEdge = Math.max(srcMeta.width, srcMeta.height);

  if ((srcExt === ".jpg" || srcExt === ".jpeg") && srcLongEdge === buyerLongEdge) {
    await fs.copyFile(srcPath, destPath);
    return { ok: true, action: "save_original_as_seo", mode: "copied", width: srcMeta.width, height: srcMeta.height };
  }

  const ratio = buyerLongEdge / Math.max(1, srcLongEdge);
  const outW = Math.max(1, Math.round(srcMeta.width * ratio));
  const outH = Math.max(1, Math.round(srcMeta.height * ratio));

  await sharp(srcPath, { limitInputPixels: false })
    .rotate()
    .resize(outW, outH, { fit: "fill", kernel: sharp.kernel.lanczos3 })
    .jpeg({ quality: 95, mozjpeg: true, progressive: true })
    .toFile(destPath);

  const outMeta = await metadataFor(destPath);
  const outLongEdge = Math.max(outMeta.width, outMeta.height);
  if (outLongEdge !== buyerLongEdge) {
    throw new Error(`Buyer image long edge invariant failed; expected ${buyerLongEdge}, got ${outLongEdge}`);
  }
  return { ok: true, action: "save_original_as_seo", mode: "resized", width: outMeta.width, height: outMeta.height };
}

async function renderThumb500(payload) {
  const basePath = String(payload.base_path || "").trim();
  const outputPath = String(payload.output_path || "").trim();
  const outputSize = clampInt(payload.output_size || 500, 1, 5000);
  const quality = clampInt(payload.quality || 92, 1, 100);

  if (!basePath || !outputPath) {
    throw new Error("render_thumb_500 requires base_path and output_path");
  }

  await fs.mkdir(path.dirname(outputPath), { recursive: true });
  await sharp(basePath, { limitInputPixels: false })
    .rotate()
    .resize(outputSize, outputSize, {
      fit: "contain",
      kernel: sharp.kernel.lanczos3,
      background: { r: 255, g: 255, b: 255, alpha: 1 },
    })
    .flatten({ background: { r: 255, g: 255, b: 255 } })
    .jpeg({ quality, mozjpeg: true, progressive: true })
    .toFile(outputPath);

  return { ok: true, action: "render_thumb_500", width: outputSize, height: outputSize };
}

function clamp01(value) {
  const n = Number(value);
  if (!Number.isFinite(n)) return 0.5;
  return Math.max(0, Math.min(1, n));
}

function clampInt(value, min, max) {
  const n = Number(value);
  if (!Number.isFinite(n)) return min;
  return Math.max(min, Math.min(max, Math.round(n)));
}

function clampFloat(value, min, max, fallback) {
  const n = Number(value);
  if (!Number.isFinite(n)) return fallback;
  return Math.max(min, Math.min(max, n));
}

async function metadataFor(path) {
  const meta = await sharp(path, { limitInputPixels: false }).metadata();
  const width = Number(meta.width || 0);
  const height = Number(meta.height || 0);
  if (width <= 0 || height <= 0) {
    throw new Error("Unable to read input dimensions");
  }
  return { width, height };
}

function normalizePoint(x, y, width, height) {
  const w = Math.max(1, Number(width) || 1);
  const h = Math.max(1, Number(height) || 1);
  return {
    x: Math.max(0, Math.min(1, Number(x) / w)),
    y: Math.max(0, Math.min(1, Number(y) / h)),
  };
}

async function scanTransparentZones(payload) {
  const imagePath = String(payload.image_path || "").trim();
  const alphaThreshold = clampInt(payload.alpha_threshold || 5, 0, 255);
  const minArea = clampInt(payload.min_area || 10, 1, 100000000);
  const maxRegions = clampInt(payload.max_regions || 6, 1, 50);

  if (!imagePath) {
    throw new Error("scan_transparent_zones requires image_path");
  }

  const { data, info } = await sharp(imagePath, { limitInputPixels: false })
    .ensureAlpha()
    .raw()
    .toBuffer({ resolveWithObject: true });

  const width = Number(info.width || 0);
  const height = Number(info.height || 0);
  const channels = Number(info.channels || 0);
  if (width <= 0 || height <= 0 || channels < 4) {
    throw new Error("Unable to read RGBA pixel data");
  }

  const pixelCount = width * height;
  const visited = new Uint8Array(pixelCount);
  const queue = new Int32Array(pixelCount);
  const candidates = [];

  const isOpaque = (idx) => {
    const alpha = data[idx * channels + 3];
    return alpha > alphaThreshold;
  };

  for (let y = 0; y < height; y += 1) {
    for (let x = 0; x < width; x += 1) {
      const start = y * width + x;
      if (visited[start] === 1 || !isOpaque(start)) {
        continue;
      }

      let qHead = 0;
      let qTail = 0;
      queue[qTail++] = start;
      visited[start] = 1;

      let area = 0;
      let touchesBorder = false;
      let minX = Number.POSITIVE_INFINITY;
      let maxX = Number.NEGATIVE_INFINITY;
      let minY = Number.POSITIVE_INFINITY;
      let maxY = Number.NEGATIVE_INFINITY;
      let sumX = 0;
      let sumY = 0;

      while (qHead < qTail) {
        const cur = queue[qHead++];
        const cy = Math.floor(cur / width);
        const cx = cur - cy * width;
        area += 1;
        sumX += cx;
        sumY += cy;

        if (cx <= 0 || cy <= 0 || cx >= width - 1 || cy >= height - 1) {
          touchesBorder = true;
        }

        if (cx < minX) minX = cx;
        if (cx > maxX) maxX = cx;
        if (cy < minY) minY = cy;
        if (cy > maxY) maxY = cy;

        for (let ny = Math.max(0, cy - 1); ny <= Math.min(height - 1, cy + 1); ny += 1) {
          for (let nx = Math.max(0, cx - 1); nx <= Math.min(width - 1, cx + 1); nx += 1) {
            if (nx === cx && ny === cy) continue;
            const ni = ny * width + nx;
            if (visited[ni] === 1 || !isOpaque(ni)) continue;
            visited[ni] = 1;
            queue[qTail++] = ni;
          }
        }
      }

      if (touchesBorder || area < minArea) {
        continue;
      }

      candidates.push({
        cy: sumY / Math.max(1, area),
        cx: sumX / Math.max(1, area),
        zone: {
          points: [
            normalizePoint(minX, minY, width, height),
            normalizePoint(maxX, minY, width, height),
            normalizePoint(maxX, maxY, width, height),
            normalizePoint(minX, maxY, width, height),
          ],
        },
      });
    }
  }

  candidates.sort((a, b) => {
    if (a.cy !== b.cy) return a.cy - b.cy;
    return a.cx - b.cx;
  });

  return {
    ok: true,
    action: "scan_transparent_zones",
    normalized: true,
    width,
    height,
    zones: candidates.slice(0, maxRegions).map((item) => item.zone),
  };
}

async function readImageMeta(payload) {
  const imagePath = String(payload.image_path || "").trim();
  if (!imagePath) {
    throw new Error("read_image_meta requires image_path");
  }
  const { width, height } = await metadataFor(imagePath);
  return { ok: true, action: "read_image_meta", width, height };
}

async function generateProxy(payload) {
  const masterPath = String(payload.master_path || "").trim();
  const outputPath = String(payload.output_path || "").trim();
  const longEdge = clampInt(payload.long_edge || 7200, 1, 50000);
  const quality = clampInt(payload.quality || 80, 1, 100);

  if (!masterPath || !outputPath) {
    throw new Error("generate_proxy requires master_path and output_path");
  }

  const { width, height } = await metadataFor(masterPath);
  const ratio = longEdge / Math.max(width, height);
  const targetW = Math.max(1, Math.round(width * ratio));
  const targetH = Math.max(1, Math.round(height * ratio));

  await sharp(masterPath, { limitInputPixels: false })
    .rotate()
    .resize(targetW, targetH, { kernel: sharp.kernel.lanczos3, fit: "fill" })
    .jpeg({ quality, mozjpeg: true, progressive: true })
    .toFile(outputPath);

  return { ok: true, action: "generate_proxy", width: targetW, height: targetH };
}

async function renderDetail(payload) {
  const masterPath = String(payload.master_path || "").trim();
  const outputPath = String(payload.output_path || "").trim();
  const normX = clamp01(payload.norm_x);
  const normY = clamp01(payload.norm_y);
  const outputSize = clampInt(payload.output_size || 2048, 1, 10000);
  const quality = clampInt(payload.quality || 95, 1, 100);

  if (!masterPath || !outputPath) {
    throw new Error("render_detail requires master_path and output_path");
  }

  const { width: masterW, height: masterH } = await metadataFor(masterPath);

  const centerX = normX * masterW;
  const centerY = normY * masterH;
  const half = outputSize / 2;

  let left = Math.round(centerX - half);
  let top = Math.round(centerY - half);
  let right = Math.round(centerX + half);
  let bottom = Math.round(centerY + half);

  if (left < 0) {
    left = 0;
    right = Math.min(outputSize, masterW);
  }
  if (top < 0) {
    top = 0;
    bottom = Math.min(outputSize, masterH);
  }
  if (right > masterW) {
    right = masterW;
    left = Math.max(0, masterW - outputSize);
  }
  if (bottom > masterH) {
    bottom = masterH;
    top = Math.max(0, masterH - outputSize);
  }

  const cropW = Math.max(1, right - left);
  const cropH = Math.max(1, bottom - top);

  await sharp(masterPath, { limitInputPixels: false })
    .rotate()
    .extract({ left, top, width: cropW, height: cropH })
    .resize(outputSize, outputSize, {
      fit: "cover",
      kernel: sharp.kernel.lanczos3,
      position: "centre",
    })
    .jpeg({ quality, mozjpeg: true, progressive: true })
    .toFile(outputPath);

  return {
    ok: true,
    action: "render_detail",
    master_width: masterW,
    master_height: masterH,
    center_px_x: centerX,
    center_px_y: centerY,
    crop_width: cropW,
    crop_height: cropH,
  };
}

async function generateMockup(payload) {
  const masterPath = String(payload.master_path || "").trim();
  const outputPath = String(payload.output_path || "").trim();
  const outW = clampInt(payload.width || 2048, 1, 10000);
  const outH = clampInt(payload.height || 2048, 1, 10000);
  const quality = clampInt(payload.quality || 90, 1, 100);

  if (!masterPath || !outputPath) {
    throw new Error("generate_mockup requires master_path and output_path");
  }

  await sharp(masterPath, { limitInputPixels: false })
    .rotate()
    .resize(outW, outH, {
      fit: "cover",
      kernel: sharp.kernel.lanczos3,
      position: "centre",
    })
    .jpeg({ quality, mozjpeg: true, progressive: true })
    .toFile(outputPath);

  return { ok: true, action: "generate_mockup", width: outW, height: outH };
}

async function compositeMockup(payload) {
  const masterPath = String(payload.master_path || "").trim();
  const basePath = String(payload.base_path || "").trim();
  const outputPath = String(payload.output_path || "").trim();
  const outputSize = clampInt(payload.output_size || 2048, 1, 10000);
  const quality = clampInt(payload.quality || 90, 1, 100);
  const overscanPct = clampFloat(payload.overscan_pct || 0.002, 0, 0.05, 0.002);
  const normCenterX = clamp01(payload.norm_center_x);
  const normCenterY = clamp01(payload.norm_center_y);
  const zoneWidthPct = clampFloat(payload.zone_width_pct || 1.0, 0.0001, 4, 1.0);
  const zoneHeightPct = clampFloat(payload.zone_height_pct || 1.0, 0.0001, 4, 1.0);

  if (!masterPath || !basePath || !outputPath) {
    throw new Error("composite_mockup requires master_path, base_path, and output_path");
  }

  const baseBuffer = await sharp(basePath, { limitInputPixels: false })
    .rotate()
    .resize(outputSize, outputSize, {
      fit: "cover",
      kernel: sharp.kernel.lanczos3,
      position: "centre",
    })
    .png({ compressionLevel: 9, adaptiveFiltering: true, palette: false, force: true })
    .toBuffer();

  const artworkW = Math.max(1, Math.round(outputSize * zoneWidthPct * (1 + overscanPct)));
  const artworkH = Math.max(1, Math.round(outputSize * zoneHeightPct * (1 + overscanPct)));

  const artworkBuffer = await sharp(masterPath, { limitInputPixels: false })
    .rotate()
    .resize(artworkW, artworkH, {
      fit: "cover",
      kernel: sharp.kernel.lanczos3,
      position: "centre",
    })
    .png({ compressionLevel: 9, adaptiveFiltering: true, palette: false, force: true })
    .toBuffer();

  const left = Math.round(normCenterX * outputSize - artworkW / 2);
  const top = Math.round(normCenterY * outputSize - artworkH / 2);

  await sharp({
    create: {
      width: outputSize,
      height: outputSize,
      channels: 4,
      background: { r: 255, g: 255, b: 255, alpha: 1 },
    },
  })
    .composite([
      { input: artworkBuffer, left, top },
      { input: baseBuffer, left: 0, top: 0 },
    ])
    .flatten({ background: { r: 255, g: 255, b: 255 } })
    .jpeg({ quality, mozjpeg: true, progressive: true })
    .toFile(outputPath);

  return {
    ok: true,
    action: "composite_mockup",
    output_size: outputSize,
    overscan_pct: overscanPct,
    artwork_width: artworkW,
    artwork_height: artworkH,
    artwork_left: left,
    artwork_top: top,
  };
}

async function run() {
  const payload = parsePayload(process.argv[2]);
  const action = String(payload.action || "").trim();

  if (action === "generate_proxy") {
    return generateProxy(payload);
  }
  if (action === "read_image_meta") {
    return readImageMeta(payload);
  }
  if (action === "scan_transparent_zones") {
    return scanTransparentZones(payload);
  }
  if (action === "render_detail") {
    return renderDetail(payload);
  }
  if (action === "generate_mockup") {
    return generateMockup(payload);
  }
  if (action === "generate_upload_thumb") {
    return generateUploadThumb(payload);
  }
  if (action === "save_original_as_seo") {
    return saveOriginalAsSeo(payload);
  }
  if (action === "render_thumb_500") {
    return renderThumb500(payload);
  }
  if (action === "composite_mockup") {
    return compositeMockup(payload);
  }

  throw new Error(`Unsupported action: ${action || "(missing)"}`);
}

run()
  .then((result) => {
    process.stdout.write(JSON.stringify(result));
  })
  .catch((err) => {
    process.stderr.write(`processor.js failed: ${err && err.message ? err.message : String(err)}\n`);
    process.exit(1);
  });
