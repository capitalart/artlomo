"use strict";

const fs = require("fs");
const path = require("path");
const { spawn } = require("child_process");
const { spawnSync } = require("child_process");

function clamp01(value) {
  const n = Number(value);
  if (!Number.isFinite(n)) return 0.5;
  return Math.max(0, Math.min(1, n));
}

function clampRange(value, min, max, fallback) {
  const n = Number(value);
  if (!Number.isFinite(n)) return fallback;
  return Math.max(min, Math.min(max, n));
}

function finiteOr(value, fallback) {
  const n = Number(value);
  return Number.isFinite(n) ? n : fallback;
}

function summarizeFfmpegError(stderrText) {
  const text = String(stderrText || "");
  const lines = text
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);
  if (!lines.length) return "ffmpeg failed with empty stderr";

  const interesting = lines.filter((line) => {
    const l = line.toLowerCase();
    return (
      l.includes("xfade") ||
      l.includes("error") ||
      l.includes("invalid") ||
      l.includes("failed") ||
      l.includes("constant frame rate") ||
      l.includes("timebase") ||
      l.includes("pix_fmt")
    );
  });

  const xfadeFocused = interesting.filter((line) => {
    const l = line.toLowerCase();
    return (
      l.includes("xfade") ||
      l.includes("constant frame rate") ||
      l.includes("failed to configure output pad") ||
      l.includes("error reinitializing filters")
    );
  });

  const source = xfadeFocused.length ? xfadeFocused : (interesting.length ? interesting : lines);
  return source.slice(-3).join(" | ").slice(0, 1200);
}

/**
 * Compute cover-mode transform for artwork scaling.
 * Scales artwork to fill output canvas without letterboxing.
 * 
 * @param {number} imgW - Image width
 * @param {number} imgH - Image height
 * @param {number} outW - Output width (square)
 * @param {number} outH - Output height (square)
 * @param {number} zoomScale - Additional zoom scale (1.0 = no zoom, >1.0 = zoomed in)
 * @param {number} panX01 - Pan position X normalized 0..1 (0.5 = center, default)
 * @param {number} panY01 - Pan position Y normalized 0..1 (0.5 = center, default)
 * @returns {Object} {drawW, drawH, offsetX, offsetY} for canvas drawing
 */
function computeCoverTransform(imgW, imgH, outW, outH, zoomScale = 1.0, panX01 = 0.5, panY01 = 0.5) {
  const imgW_num = Number(imgW) || 1;
  const imgH_num = Number(imgH) || 1;
  const outW_num = Number(outW) || 1024;
  const outH_num = Number(outH) || 1024;
  const zoom = Math.max(1.0, Number(zoomScale) || 1.0);
  const panX = clamp01(panX01);
  const panY = clamp01(panY01);

  // Compute the scale needed to cover the output (let image extend beyond if needed)
  const scaleX = outW_num / imgW_num;
  const scaleY = outH_num / imgH_num;
  const coverScale = Math.max(scaleX, scaleY);

  // Apply additional zoom
  const effectiveScale = coverScale * zoom;

  // Dimensions after scaling
  const drawW = imgW_num * effectiveScale;
  const drawH = imgH_num * effectiveScale;

  // Maximum offsets when image is larger than output (can show any part)
  const maxOffsetX = drawW - outW_num;
  const maxOffsetY = drawH - outH_num;

  // Pan position within the valid range
  const offsetX = -(panX * maxOffsetX);
  const offsetY = -(panY * maxOffsetY);

  return {
    drawW: Math.round(drawW * 100) / 100,
    drawH: Math.round(drawH * 100) / 100,
    offsetX: Math.round(offsetX * 100) / 100,
    offsetY: Math.round(offsetY * 100) / 100,
    coverScale: Math.round(coverScale * 10000) / 10000,
  };
}

const SUBPIXEL_OVERSCAN_FACTOR = 1.002;
const INTERNAL_MOTION_CANVAS_SCALE = 2;

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

function safeReadJson(filePath) {
  try {
    if (!filePath || !fs.existsSync(filePath)) return null;
    return JSON.parse(fs.readFileSync(filePath, "utf8"));
  } catch (_err) {
    return null;
  }
}

function extractSlot(slug, mockupPath) {
  const base = path.basename(mockupPath, path.extname(mockupPath));
  const prefix = `mu-${slug}-`;
  if (!base.startsWith(prefix)) return null;
  const slot = base.slice(prefix.length);
  return /^\d+$/.test(slot) ? slot.padStart(2, "0") : null;
}

function findZoneJsonPath(templateSlug, coordinatesRoot) {
  if (!templateSlug || !coordinatesRoot) return null;
  const fileName = `${templateSlug}.json`;
  const direct = path.join(coordinatesRoot, fileName);
  if (fs.existsSync(direct)) return direct;

  const parts = String(templateSlug).split("-").filter(Boolean);
  const upper = parts.map((p) => p.toUpperCase());
  const muIdx = upper.indexOf("MU");
  const aspect = (parts[0] || "").toLowerCase();
  const category = muIdx > 1 ? parts.slice(1, muIdx).join("-").toLowerCase() : "";

  const candidates = [];
  if (aspect) candidates.push(path.join(coordinatesRoot, aspect, fileName));
  if (aspect && category) candidates.push(path.join(coordinatesRoot, aspect, category, fileName));
  for (const candidate of candidates) {
    if (fs.existsSync(candidate)) return candidate;
  }

  const stack = [coordinatesRoot];
  while (stack.length) {
    const current = stack.pop();
    let entries = [];
    try {
      entries = fs.readdirSync(current, { withFileTypes: true });
    } catch (_err) {
      continue;
    }
    for (const entry of entries) {
      const full = path.join(current, entry.name);
      if (entry.isDirectory()) {
        stack.push(full);
      } else if (entry.isFile() && entry.name === fileName) {
        return full;
      }
    }
  }

  return null;
}

/**
 * Read PNG image dimensions by parsing the IHDR chunk header (first 24 bytes).
 * This avoids spawning an external process or requiring an image library.
 * @param {string} pngPath - Absolute path to the PNG file
 * @returns {{ width: number, height: number } | null}
 */
function readPngDimensions(pngPath) {
  if (!pngPath) return null;
  try {
    const PNG_SIGNATURE_LEN = 8;
    const IHDR_DATA_OFFSET = PNG_SIGNATURE_LEN + 4 + 4; // sig + length + "IHDR"
    const buf = Buffer.alloc(24);
    const fd = fs.openSync(pngPath, "r");
    const bytesRead = fs.readSync(fd, buf, 0, 24, 0);
    fs.closeSync(fd);
    if (bytesRead < 24) return null;
    // Verify PNG signature: first 8 bytes
    if (
      buf[0] !== 0x89 || buf[1] !== 0x50 || buf[2] !== 0x4e || buf[3] !== 0x47 ||
      buf[4] !== 0x0d || buf[5] !== 0x0a || buf[6] !== 0x1a || buf[7] !== 0x0a
    ) {
      return null;
    }
    const width = buf.readUInt32BE(IHDR_DATA_OFFSET);
    const height = buf.readUInt32BE(IHDR_DATA_OFFSET + 4);
    if (width > 0 && height > 0) return { width, height };
    return null;
  } catch (_err) {
    return null;
  }
}

function extractZoneTarget(zonePayload, canvasDims) {
  const zones = zonePayload && zonePayload.zones;
  if (!Array.isArray(zones) || zones.length === 0) return null;
  const first = zones[0];
  const points = first && first.points;
  if (!Array.isArray(points) || points.length < 4) return null;

  const xs = [];
  const ys = [];
  for (const pt of points) {
    if (!pt || typeof pt !== "object") continue;
    const x = Number(pt.x);
    const y = Number(pt.y);
    if (!Number.isFinite(x) || !Number.isFinite(y)) continue;
    xs.push(x);
    ys.push(y);
  }

  if (xs.length < 2 || ys.length < 2) return null;

  const centerX = (Math.min(...xs) + Math.max(...xs)) / 2;
  const centerY = (Math.min(...ys) + Math.max(...ys)) / 2;

  const dims = zonePayload.dimensions || {};
  // Priority: zone JSON dimensions > companion PNG dimensions > max(xs)/max(ys) fallback.
  // max(xs) fallback is inaccurate when zone points don't reach the canvas edge (common
  // for 2048px templates where zone points max out at ~1434px).
  const sourceW =
    Number(dims.canvas_width_px) ||
    (canvasDims && canvasDims.width) ||
    Math.max(...xs) ||
    1;
  const sourceH =
    Number(dims.canvas_height_px) ||
    (canvasDims && canvasDims.height) ||
    Math.max(...ys) ||
    1;

  if (sourceW <= 0 || sourceH <= 0) return null;

  if (centerX <= 1 && centerY <= 1 && Math.max(...xs) <= 1.2 && Math.max(...ys) <= 1.2) {
    return { x: clamp01(centerX), y: clamp01(centerY) };
  }

  return { x: clamp01(centerX / sourceW), y: clamp01(centerY / sourceH) };
}

function resolveMockupTargets(payload) {
  const slug = String(payload.slug || "").trim();
  const processedRoot = payload.processed_root;
  const coordinatesRoot = payload.coordinates_root;
  const mockupPaths = Array.isArray(payload.mockup_paths) ? payload.mockup_paths : [];

  const assetsPath = path.join(processedRoot, slug, `${slug}-assets.json`);
  const assetsPayload = safeReadJson(assetsPath);
  const assetsMap =
    assetsPayload &&
      assetsPayload.mockups &&
      assetsPayload.mockups.assets &&
      typeof assetsPayload.mockups.assets === "object"
      ? assetsPayload.mockups.assets
      : {};

  return mockupPaths.map((mockupPath) => {
    const slot = extractSlot(slug, mockupPath);
    const slotMeta = slot ? assetsMap[slot] : null;
    const templateSlug = slotMeta && typeof slotMeta.template_slug === "string" ? slotMeta.template_slug.trim() : "";
    const category = slotMeta && typeof slotMeta.category === "string" ? slotMeta.category.trim() : "";
    
    if (!templateSlug) {
      return { path: mockupPath, targetX: 0.5, targetY: 0.5, hasTarget: false, category: "" };
    }

    const zonePath = findZoneJsonPath(templateSlug, coordinatesRoot);
    const zonePayload = zonePath ? safeReadJson(zonePath) : null;
    // Read companion PNG for accurate canvas dimensions; zone JSON format_version 2.0
    // does not embed dimensions, causing max(xs) fallback to give wrong normalization.
    const pngPath = zonePath ? zonePath.replace(/\.json$/, ".png") : null;
    const canvasDims = pngPath && fs.existsSync(pngPath) ? readPngDimensions(pngPath) : null;
    const target = zonePayload ? extractZoneTarget(zonePayload, canvasDims) : null;

    return {
      path: mockupPath,
      targetX: target ? target.x : 0.5,
      targetY: target ? target.y : 0.5,
      hasTarget: Boolean(target),
      category: category,
    };
  });
}

/**
 * Compute pan direction toward a target point (artwork center).
 * @param {number} tx - Target X coordinate (normalized 0..1)
 * @param {number} ty - Target Y coordinate (normalized 0..1)
 * @returns {string} direction: "up"|"down"|"left"|"right"
 */
function computeDirectionFromTargetPoint(tx, ty) {
  const x = clamp01(Number(tx) || 0.5);
  const y = clamp01(Number(ty) || 0.5);

  const dx = Math.abs(x - 0.5);
  const dy = Math.abs(y - 0.5);

  // Near center fallback
  if (dx < 0.12 && dy < 0.12) {
    return "right";
  }

  // Determine primary axis
  if (dx > dy) {
    return x < 0.5 ? "left" : "right";
  } else {
    return y < 0.5 ? "up" : "down";
  }
}

/**
 * Resolve final pan direction using manual setting, auto-aim, and blend weight.
 * @param {Object} options
 * @param {string} options.manualDirection - Manual direction setting (up/down/left/right)
 * @param {boolean} options.autoAim - Whether auto-aim is enabled
 * @param {number} options.aimWeight - Aim weight 0.0 (pure manual) to 1.0 (pure aim)
 * @param {number} options.targetX - Target X coordinate (normalized 0..1)
 * @param {number} options.targetY - Target Y coordinate (normalized 0..1)
 * @param {boolean} options.hasTarget - Whether valid target coordinates are available
 * @returns {string} Final resolved direction
 */
function resolveFinalDirection({
  manualDirection,
  autoAim,
  aimWeight,
  targetX,
  targetY,
  hasTarget
}) {
  // No aim or no target → use manual
  if (!autoAim || !hasTarget) {
    return manualDirection;
  }

  const aimDirection = computeDirectionFromTargetPoint(targetX, targetY);

  // Pure aim mode
  if (aimWeight >= 0.99) {
    return aimDirection;
  }

  // Pure manual mode
  if (aimWeight <= 0.01) {
    return manualDirection;
  }

  // Blended mode:
  // If manual matches aim → keep it
  if (manualDirection === aimDirection) {
    return manualDirection;
  }

  // If aimWeight > 0.5 bias toward aim
  return aimWeight > 0.5 ? aimDirection : manualDirection;
}

function buildPanExpressions(targetX, targetY, direction, frames, clampTarget, options = {}) {
  const rawX = clamp01(targetX);
  const rawY = clamp01(targetY);
  const edgeBuffer = clampTarget ? 0.2 : 0;
  const tx = clamp01(Math.min(1 - edgeBuffer, Math.max(edgeBuffer, rawX)));
  const ty = clamp01(Math.min(1 - edgeBuffer, Math.max(edgeBuffer, rawY)));
  const motionProfile = String(options.motionProfile || "legacy").trim().toLowerCase();
  const maxTravelNorm = clampRange(options.maxTravelNorm, 0.05, 0.5, 0.18);
  const denom = Math.max(1, Number(frames || 1) - 1);
  const linearProgress = `on/${denom}`;
  
  // Apply ease-out cubic for smooth deceleration at the end
  // Ease-out cubic: 1 - (1-t)^3
  // This makes the pan start fast and slow down smoothly at the end
  const eased = `1-pow(1-${linearProgress},3)`;
  const progress = eased;
  
  // Pan range available at the current zoom level
  const rangeX = "(iw-iw/zoom)";
  const rangeY = "(ih-ih/zoom)";
  
  // Target position within the available pan range
  let aimTargetX = tx;
  let aimTargetY = ty;
  if (motionProfile === "distance_normalized") {
    const dx = tx - 0.5;
    const dy = ty - 0.5;
    const dist = Math.sqrt((dx * dx) + (dy * dy));
    if (dist > 1e-9) {
      const scale = Math.min(1, maxTravelNorm / dist);
      aimTargetX = clamp01(0.5 + (dx * scale));
      aimTargetY = clamp01(0.5 + (dy * scale));
    }
  }

  const targetXPos = `${aimTargetX.toFixed(6)}*${rangeX}`;
  const targetYPos = `${aimTargetY.toFixed(6)}*${rangeY}`;
  const centerXPos = `0.5*${rangeX}`;
  const centerYPos = `0.5*${rangeY}`;
  const leftXPos = `0`;
  const rightXPos = `${rangeX}`;
  const topYPos = `0`;
  const bottomYPos = `${rangeY}`;
  
  let xExpr, yExpr;
  
  switch (direction) {
    case "aim": {
      // Smoothly move from center toward artwork target on pan-range coordinates.
      // Using range-space (not iw/ih) avoids clamping artifacts that forced corners.
      const blendX = `${centerXPos}+(${targetXPos}-(${centerXPos}))*${progress}`;
      const blendY = `${centerYPos}+(${targetYPos}-(${centerYPos}))*${progress}`;
      xExpr = `max(0,min(${rangeX},${blendX}))`;
      yExpr = `max(0,min(${rangeY},${blendY}))`;
      break;
    }
    case "center":
      xExpr = `max(0,min(${rangeX},${centerXPos}))`;
      yExpr = `max(0,min(${rangeY},${centerYPos}))`;
      break;
    case "top-left":
      xExpr = `max(0,min(${rangeX},${leftXPos}+(${rightXPos}-${leftXPos})*(1-${progress})))`;
      yExpr = `max(0,min(${rangeY},${topYPos}+(${bottomYPos}-${topYPos})*(1-${progress})))`;
      break;
    case "top-right":
      xExpr = `max(0,min(${rangeX},${leftXPos}+(${rightXPos}-${leftXPos})*${progress}))`;
      yExpr = `max(0,min(${rangeY},${topYPos}+(${bottomYPos}-${topYPos})*(1-${progress})))`;
      break;
    case "bottom-right":
      xExpr = `max(0,min(${rangeX},${leftXPos}+(${rightXPos}-${leftXPos})*${progress}))`;
      yExpr = `max(0,min(${rangeY},${topYPos}+(${bottomYPos}-${topYPos})*${progress}))`;
      break;
    case "bottom-left":
      xExpr = `max(0,min(${rangeX},${leftXPos}+(${rightXPos}-${leftXPos})*(1-${progress})))`;
      yExpr = `max(0,min(${rangeY},${topYPos}+(${bottomYPos}-${topYPos})*${progress}))`;
      break;
    case "up":
      xExpr = `max(0,min(${rangeX},${centerXPos}))`;
      yExpr = `max(0,min(${rangeY},${rangeY}*(1-${progress})))`;
      break;
    case "down":
      xExpr = `max(0,min(${rangeX},${centerXPos}))`;
      yExpr = `max(0,min(${rangeY},${rangeY}*${progress}))`;
      break;
    case "left":
      xExpr = `max(0,min(${rangeX},${rangeX}*(1-${progress})))`;
      yExpr = `max(0,min(${rangeY},${centerYPos}))`;
      break;
    case "right":
      xExpr = `max(0,min(${rangeX},${rangeX}*${progress}))`;
      yExpr = `max(0,min(${rangeY},${centerYPos}))`;
      break;
    default:
      // No directional pan, hold on target.
      xExpr = `max(0,min(${rangeX},${targetXPos}))`;
      yExpr = `max(0,min(${rangeY},${targetYPos}))`;
  }
  
  return { x: xExpr, y: yExpr };
}

function buildMasterExpressions(masterMode, frames, panDirection = null) {
  const denom = Math.max(1, Number(frames || 1) - 1);
  const linearProgress = `on/${denom}`;
  
  // Apply ease-out cubic for smooth deceleration at the end
  // Ease-out cubic: 1 - (1-t)^3
  const eased = `1-pow(1-${linearProgress},3)`;
  const progress = eased;
  
  // If explicit pan direction provided, use it
  if (panDirection && typeof panDirection === 'string') {
    const dir = panDirection.toLowerCase();
    if (dir === 'center') {
      return {
        x: "(iw-iw/zoom)/2",
        y: "(ih-ih/zoom)/2",
      };
    }
    if (dir === 'top-left') {
      return {
        x: `max(0,min(iw-iw/zoom,(iw-iw/zoom)*(1-${progress})))`,
        y: `max(0,min(ih-ih/zoom,(ih-ih/zoom)*(1-${progress})))`,
      };
    }
    if (dir === 'top-right') {
      return {
        x: `max(0,min(iw-iw/zoom,(iw-iw/zoom)*(${progress})))`,
        y: `max(0,min(ih-ih/zoom,(ih-ih/zoom)*(1-${progress})))`,
      };
    }
    if (dir === 'bottom-right') {
      return {
        x: `max(0,min(iw-iw/zoom,(iw-iw/zoom)*(${progress})))`,
        y: `max(0,min(ih-ih/zoom,(ih-ih/zoom)*(${progress})))`,
      };
    }
    if (dir === 'bottom-left') {
      return {
        x: `max(0,min(iw-iw/zoom,(iw-iw/zoom)*(1-${progress})))`,
        y: `max(0,min(ih-ih/zoom,(ih-ih/zoom)*(${progress})))`,
      };
    }
    if (dir === 'left') {
      return {
        x: `max(0,min(iw-iw/zoom,(iw-iw/zoom)*(1-${progress})))`,
        y: "(ih-ih/zoom)/2",
      };
    }
    if (dir === 'right') {
      return {
        x: `max(0,min(iw-iw/zoom,(iw-iw/zoom)*(${progress})))`,
        y: "(ih-ih/zoom)/2",
      };
    }
    if (dir === 'up') {
      return {
        x: "(iw-iw/zoom)/2",
        y: `max(0,min(ih-ih/zoom,(ih-ih/zoom)*(1-${progress})))`,
      };
    }
    if (dir === 'down') {
      return {
        x: "(iw-iw/zoom)/2",
        y: `max(0,min(ih-ih/zoom,(ih-ih/zoom)*(${progress})))`,
      };
    }
  }
  
  // Fallback to orientation-based panning (legacy behavior)
  if (masterMode === "landscape") {
    return {
      x: `max(0,min(iw-iw/zoom,(iw-iw/zoom)*(${progress})))`,
      y: "(ih-ih/zoom)/2",
    };
  }
  if (masterMode === "portrait") {
    return {
      x: "(iw-iw/zoom)/2",
      y: `max(0,min(ih-ih/zoom,(ih-ih/zoom)*(1-${progress})))`,
    };
  }
  return {
    x: "(iw-iw/zoom)/2",
    y: "(ih-ih/zoom)/2",
  };
}

function buildFilter(slides, video, masterMode, compositorMode = "concat") {
  const outputSize = Number(video.output_size || video.width || 1024);
  const width = outputSize;
  const height = outputSize;
  const motionWidth = Math.max(width, Math.round(width * INTERNAL_MOTION_CANVAS_SCALE));
  const motionHeight = Math.max(height, Math.round(height * INTERNAL_MOTION_CANVAS_SCALE));
  const fps = clampRange(video.fps, 1, 120, 24);
  const crossfadeSeconds = clampRange(video.crossfade_seconds, 0, 5, 0.5);
  const crossfadeFrames = crossfadeSeconds > 0 ? Math.max(1, Math.round(crossfadeSeconds * fps)) : 0;
  const requestedDuration = Number(video.duration_seconds);
  const mainArtworkSeconds = clampRange(video.main_artwork_seconds, 0.5, 120, 4.0);
  const minSlideSeconds = Math.max(0.35, crossfadeSeconds + 0.15);
  let slideSeconds = clampRange(video.slide_seconds, minSlideSeconds, 120, 2.5);
  const motionProfile = ["legacy", "distance_normalized"].includes(String(video.motion_profile || "").trim().toLowerCase())
    ? String(video.motion_profile || "legacy").trim().toLowerCase()
    : "distance_normalized";
  const timingMode = ["time_continuous", "frame_quantized"].includes(String(video.timing_mode || "").trim().toLowerCase())
    ? String(video.timing_mode || "time_continuous").trim().toLowerCase()
    : "frame_quantized";
  const useFrameQuantizedTiming = timingMode === "frame_quantized";
  const crossfadeUsed = useFrameQuantizedTiming ? (crossfadeFrames / fps) : crossfadeSeconds;
  const includeMasterSlide = slides.length > 0 && slides[0].role === "master";
  const remainingSlides = includeMasterSlide ? Math.max(0, slides.length - 1) : slides.length;
  
  // Extract artwork and mockups settings with fallback to legacy fields
  const artworkSettings = video.artwork || {};
  const mockupsSettings = video.mockups || {};
  
  const legacyZoom = Number(video.zoom_intensity || 1.1);
  const legacyPanning = Boolean(video.panning_enabled);
  
  const artworkZoomIntensity = clampRange(artworkSettings.zoom_intensity || legacyZoom, 1.0, 2.25, 1.1);
  const artworkZoomDuration = clampRange(
    finiteOr(artworkSettings.zoom_duration, finiteOr(video.artwork_zoom_duration, 3.0)),
    0,
    120,
    3.0
  );
  const artworkPanEnabled = artworkSettings.pan_enabled !== undefined ? Boolean(artworkSettings.pan_enabled) : legacyPanning;
  const artworkPanDirection = String(artworkSettings.pan_direction || "up");
  
  const mockupZoomIntensity = clampRange(mockupsSettings.zoom_intensity || legacyZoom, 1.0, 2.25, 1.1);
  const mockupZoomDuration = clampRange(mockupsSettings.zoom_duration, 0, 120, 2.0);
  const mockupPanEnabled = mockupsSettings.pan_enabled !== undefined ? Boolean(mockupsSettings.pan_enabled) : false;
  const mockupPanDirection = String(mockupsSettings.pan_direction || "up");
  
  // Debug flag for pan resolution (safe for production) - must come before any DEBUG_PAN usage
  const DEBUG_PAN = process.env.ARTLOMO_VIDEO_DEBUG_PAN === "1";
  
  // Load per-mockup shot settings and create ID-based lookup
  const mockupShots = Array.isArray(video.mockup_shots) ? video.mockup_shots : [];
  const shotById = new Map(mockupShots.map(s => [String(s.id), s]));
  
  // DEBUG: Log what shots we have
  if (DEBUG_PAN || process.env.RENDER_DEBUG) {
    console.log("[RENDER] Mockup shots in payload:", mockupShots.length, "shots");
    mockupShots.forEach((shot, idx) => {
      const hasCoords = shot.coordinates ? "yes" : "no";
      console.log(`[RENDER]   [${idx}] id=${shot.id}, pan_dir=${shot.pan_direction}, has_coords=${hasCoords}`);
    });
  }
  
  // Load computed per-mockup durations (from Python service)
  const computedMockupDurations = video.computed_mockup_durations && typeof video.computed_mockup_durations === "object"
    ? video.computed_mockup_durations
    : {};
  const selectedMockupIds = Array.isArray(video.selected_mockups) ? video.selected_mockups : [];
  
  // Debug logging (set RENDER_DEBUG env var to enable)
  if (process.env.RENDER_DEBUG) {
    console.log("[DEBUG] Artwork settings:", { artworkPanEnabled, artworkPanDirection, artworkZoomIntensity, mainArtworkSeconds });
    console.log("[DEBUG] Mockup settings:", { mockupPanEnabled, mockupPanDirection, mockupZoomIntensity, shotCount: mockupShots.length });
    console.log("[DEBUG] Computed durations:", Object.keys(computedMockupDurations).length, "mockups");
    if (Object.keys(computedMockupDurations).length > 0) {
      const sample = Object.entries(computedMockupDurations).slice(0, 3);
      console.log("[DEBUG] Sample durations:", sample);
    }
  }
  
  let masterSeconds = includeMasterSlide ? Math.max(mainArtworkSeconds, artworkZoomDuration) : 0;
  let mockupSeconds = slideSeconds;

  if (Number.isFinite(requestedDuration) && requestedDuration > 0) {
    if (includeMasterSlide) {
      const maxMaster = remainingSlides > 0
        ? Math.max(minSlideSeconds, requestedDuration - (remainingSlides * minSlideSeconds))
        : requestedDuration;
      masterSeconds = clampRange(masterSeconds, minSlideSeconds, maxMaster, Math.max(mainArtworkSeconds, 3.0));
      if (remainingSlides > 0) {
        const remainingDuration = Math.max(minSlideSeconds, requestedDuration - masterSeconds);
          // xfade overlap is applied at every master/mockup boundary, so the
          // fallback math needs one crossfade per remaining slide to hit the
          // requested total duration when computed_mockup_durations is absent.
          mockupSeconds = (remainingDuration + (remainingSlides * crossfadeUsed)) / remainingSlides;
        mockupSeconds = Math.max(minSlideSeconds, mockupSeconds);
      }
    } else {
      mockupSeconds = Math.max(minSlideSeconds, requestedDuration / slides.length);
    }
  }

  const panningEnabled = artworkPanEnabled; // Legacy support
  const zoomIntensity = artworkZoomIntensity; // Legacy support
  const masterZoomEnd = artworkZoomIntensity;  // Use the actual artworkZoomIntensity setting

  const slideConfigs = slides.map((slide, slideIndex) => {
    let duration;
    
    if (slide.role === "master") {
      // Master slide uses main_artwork_seconds (or fall back to artworkZoomDuration)
      duration = masterSeconds || mockupSeconds;
    } else {
      // Mockup slide: look up computed duration by mockup index
      const mockupIndex = slideIndex - (includeMasterSlide ? 1 : 0);
      if (mockupIndex >= 0 && mockupIndex < selectedMockupIds.length) {
        const mockupId = selectedMockupIds[mockupIndex];
        const computedDuration = computedMockupDurations[mockupId];
        if (Number.isFinite(computedDuration) && computedDuration > 0) {
          duration = computedDuration;
        } else {
          // Fallback to default mockupSeconds if no computed duration
          duration = mockupSeconds;
        }
      } else {
        // Fallback for out-of-bounds indices
        duration = mockupSeconds;
      }
    }

    if (!Number.isFinite(duration) || duration <= 0) {
      duration = mockupSeconds;
    }
    duration = Math.max(minSlideSeconds, Number(duration));
    
    const frames = Math.max(1, Math.round(duration * fps));
    const quantizedDuration = frames / fps;
    const durationUsed = useFrameQuantizedTiming ? quantizedDuration : duration;
    return { ...slide, duration, durationUsed, quantizedDuration, frames };
  });

  const parts = [];

  // Pan requires available crop range; keep a moderate fixed zoom when zoom animation is off.
  const PAN_ONLY_ZOOM = 1.18;

  for (let i = 0; i < slideConfigs.length; i += 1) {
    const slide = slideConfigs[i];
    const slideFrames = Math.max(1, slide.frames);
    const zoomDenom = Math.max(1, slideFrames - 1);
    const zoomProgress = `min(1,on/${zoomDenom})`;
    let zoomExpr;
    if (slide.role === "master") {
      const easeCoeff = masterZoomEnd > 1.0 ? masterZoomEnd - 1 : 0;
      // Apply cubic ease-in-out easing: start at 1, end at masterZoomEnd
      // Easing: 1 + easeCoeff * t^2 * (3 - 2*t) where t is normalized progress 0..1
      // Simplified: zoom(t) = 1 + easeCoeff * t * t * (3 - 2*t)
      zoomExpr = `1+${easeCoeff.toFixed(7)}*${zoomProgress}*${zoomProgress}*(3-2*${zoomProgress})`;
    } else {
      // Use mockup zoom intensity for non-master slides (ID-based lookup)
      const mockupIndex = i - (includeMasterSlide ? 1 : 0);
      const mockupId = mockupIndex >= 0 && mockupIndex < selectedMockupIds.length
        ? selectedMockupIds[mockupIndex]
        : null;
      const shotData = mockupId ? shotById.get(String(mockupId)) : null;

      const isMandatory = slide.category === "mandatory-one";
      const panEnabled = !isMandatory && (shotData?.pan_enabled !== undefined
        ? Boolean(shotData.pan_enabled)
        : Boolean(mockupPanEnabled));
      
      // Mandatory mockups (size charts) are always stationary - no zoom
      // Check if zoom is enabled for this mockup (default: true if not specified)
      const mockupZoomEnabled = !isMandatory && (shotData ? (shotData.zoom_enabled !== false) : true);
      
      // Use per-mockup zoom intensity if available, otherwise use global default
      let slideZoomIntensity = mockupZoomIntensity;
      if (mockupZoomEnabled && shotData && shotData.zoom_intensity !== undefined) {
        slideZoomIntensity = clampRange(shotData.zoom_intensity, 1.0, 2.25, mockupZoomIntensity);
        if (DEBUG_PAN || process.env.RENDER_DEBUG) {
          console.log(`[ZOOM] Mockup ${mockupIndex} (${mockupId}): Using per-mockup zoom_intensity=${shotData.zoom_intensity} → clamped=${slideZoomIntensity.toFixed(2)}`);
        }
      } else if (DEBUG_PAN || process.env.RENDER_DEBUG) {
        console.log(`[ZOOM] Mockup ${mockupIndex} (${mockupId}): No per-mockup zoom, using global mockupZoomIntensity=${mockupZoomIntensity}`);
      }
      
      if (mockupZoomEnabled && slideZoomIntensity > 1.0) {
        const easeCoeff = slideZoomIntensity - 1;
        // Apply cubic ease-in-out easing: start at 1, end at slideZoomIntensity
        // Easing: 1 + easeCoeff * t^2 * (3 - 2*t) where t is normalized progress 0..1
        zoomExpr = `1+${easeCoeff.toFixed(7)}*${zoomProgress}*${zoomProgress}*(3-2*${zoomProgress})`;
      } else {
        // Zoom disabled for this mockup, or zoom intensity is 1.0 (no zoom)
        // If pan is enabled, apply a tiny fixed zoom so there is room to pan.
        zoomExpr = panEnabled ? String(PAN_ONLY_ZOOM) : "1";
      }
    }

    let xExpr;
    let yExpr;

    if (slide.role === "master") {
      if (artworkPanEnabled) {
        const master = buildMasterExpressions(masterMode, slideFrames, artworkPanDirection);
        xExpr = master.x;
        yExpr = master.y;
      } else {
        xExpr = "(iw-iw/zoom)/2";
        yExpr = "(ih-ih/zoom)/2";
      }
    } else {
      // Mockup slide - use per-mockup shot settings (ID-based lookup)
      const mockupIndex = i - (includeMasterSlide ? 1 : 0);
      const mockupId = mockupIndex >= 0 && mockupIndex < selectedMockupIds.length
        ? selectedMockupIds[mockupIndex]
        : null;
      const shotData = mockupId ? shotById.get(String(mockupId)) : null;
      
      // STEP 1: Check if shotData has per-mockup coordinates (override global zone target)
      let targetX = slide.targetX;  // Default to global zone coordinates
      let targetY = slide.targetY;
      let hasTarget = slide.hasTarget;
      
      // DIAGNOSTIC: Log what we have for every mockup
      if (DEBUG_PAN || process.env.RENDER_DEBUG) {
        console.log(`[COORD-DEBUG] Mockup ${mockupIndex} (${mockupId}):`, {
          hasShotData: !!shotData,
          shotDataKeys: shotData ? Object.keys(shotData) : [],
          hasCoordinates: shotData && shotData.coordinates ? true : false,
          coordinatesKeys: shotData && shotData.coordinates ? Object.keys(shotData.coordinates) : [],
          currentTarget: { x: targetX, y: targetY },
          slideTarget: { x: slide.targetX, y: slide.targetY }
        });
      }
      
      if (shotData && shotData.coordinates && shotData.coordinates.artwork_rect_norm) {
        const rect = shotData.coordinates.artwork_rect_norm;
        // Calculate center of the artwork rectangle (normalized 0..1)
        targetX = clamp01(Number(rect.x) + Number(rect.w) / 2);
        targetY = clamp01(Number(rect.y) + Number(rect.h) / 2);
        hasTarget = true;  // Per-mockup coordinates are always valid
        console.log("[COORD] Using per-mockup coordinates for", mockupId, { rect, calculatedCenter: { x: targetX, y: targetY } });
      } else if (DEBUG_PAN || process.env.RENDER_DEBUG) {
        console.log("[COORD] No per-mockup coordinates found for", mockupId, "using global zone target");
      }
      
      // Mandatory mockups (size charts) are always stationary - no panning
      const isMandatory = slide.category === "mandatory-one";
      
      // STEP 2: Normalize settings
      let panEnabled = !isMandatory && (shotData?.pan_enabled !== undefined
        ? Boolean(shotData.pan_enabled)
        : Boolean(mockupPanEnabled));
      
      let manualDirection = shotData?.pan_direction
        ? String(shotData.pan_direction).trim().toLowerCase()
        : String(mockupPanDirection || "up").trim().toLowerCase();
      
      // Validate manualDirection
      const validDirections = ["center", "top-left", "top-right", "bottom-right", "bottom-left", "up", "down", "left", "right", "none", "aim"];
      if (!validDirections.includes(manualDirection)) {
        manualDirection = "up";
      }
      
      // Handle special directions
      let autoAim = false;
      
      if (manualDirection === "none") {
        panEnabled = false;
        manualDirection = "up"; // Normalize for internal use
      } else if (manualDirection === "aim") {
        autoAim = true;
        panEnabled = true;
        manualDirection = "none"; // Normalize; won't be used unless hasTarget is false
      }
      
      // Backward compatibility: read legacy auto_target/pan_to_artwork_center fields
      if (!autoAim && (shotData?.pan_to_artwork_center || shotData?.auto_target)) {
        autoAim = true;
      }
      
      const aimWeight = Number(shotData?.aim_weight ?? 1.0); // Default: full aim

      // When aim is requested but no target coordinates are available (e.g. assets.json
      // has no template_slug for this slot), disable panning for this slide.
      // This prevents a misleading directional pan that points away from the artwork.
      if (autoAim && !hasTarget) {
        panEnabled = false;
        console.warn("[PAN] Aim requested but no target coordinates for", mockupId, "- disabling pan for this slide");
      }

      // If pan is enabled but zoom animation is off, force a tiny constant zoom
      // so there is room to pan even when zoom is otherwise disabled.
      if (panEnabled && zoomExpr === "1") {
        zoomExpr = String(PAN_ONLY_ZOOM);
      }
      
      
      // STEP 4: Resolve final direction using clean pan engine
      // If auto-aim is active and we have a target, prefer smooth aim interpolation
      const finalDirection = (autoAim && hasTarget && aimWeight >= 0.5)
        ? "aim"
        : resolveFinalDirection({
            manualDirection,
            autoAim,
            aimWeight,
            targetX: targetX,
            targetY: targetY,
            hasTarget: hasTarget
          });
      
      // LOG DIRECTION DECISION
      if (autoAim) {
        console.log(`[DIRECTION] Mockup ${mockupIndex} (${mockupId}):`, {
          autoAim,
          hasTarget,
          aimWeight,
          targetCoord: { x: targetX.toFixed(3), y: targetY.toFixed(3) },
          decisionPath: (autoAim && hasTarget && aimWeight >= 0.5) ? "direct-aim" : "resolve-function",
          finalDirection,
          willUseFormula: finalDirection === "aim" ? "smooth-aim-zoom" : "manual-" + finalDirection
        });
      }
      
      // STEP 6: Debug logging (safe for prod)
      if (DEBUG_PAN) {
        console.log("[PAN]", {
          mockupId,
          mockupIndex,
          manualDirection,
          autoAim,
          aimWeight,
          finalDirection,
          targetX: targetX,
          targetY: targetY,
          hasTarget: hasTarget
        });
      }
      
      // General debug logging
      if (process.env.RENDER_DEBUG) {
        console.log(`[DEBUG] Slide ${i} (mockupId ${mockupId}):`, {
          hasShotData: !!shotData,
          panEnabled,
          finalDirection,
          mockupZoomEnabled: shotData ? (shotData.zoom_enabled !== false) : true,
          hasTarget: slide.hasTarget,
        });
      }
      
      // Apply pan expressions or center if disabled
      if (!panEnabled) {
        xExpr = "(iw-iw/zoom)/2";
        yExpr = "(ih-ih/zoom)/2";
      } else {
        // STEP 5: Use resolved direction in pan expressions
        const panExprs = buildPanExpressions(
          targetX,
          targetY,
          finalDirection,
          slideFrames,
          false,
          {
            motionProfile,
          }
        );
        xExpr = panExprs.x;
        yExpr = panExprs.y;
      }
    }

    parts.push(
      `[${i}:v]setsar=1:1,` +
      // Fill square by scaling up, then crop excess from top/bottom or sides
      // This preserves aspect ratio while filling entire output without letterbox bars
      `scale=${motionWidth}:${motionHeight}:force_original_aspect_ratio=increase,` +
      `crop=${motionWidth}:${motionHeight}:(in_w-${motionWidth})/2:(in_h-${motionHeight})/2,` +
      `scale=w='trunc(iw*${SUBPIXEL_OVERSCAN_FACTOR}/2)*2':h='trunc(ih*${SUBPIXEL_OVERSCAN_FACTOR}/2)*2',` +
      "zoompan=" +
      `z='${zoomExpr}':` +
      `x='${xExpr}':` +
      `y='${yExpr}':` +
      `d=${slideFrames}:s=${motionWidth}x${motionHeight}:fps=${fps},` +
      `scale=${width}:${height},` +
      `trim=duration=${slide.durationUsed}[raw${i}]`
    );
  }

  // Normalize each segment to identical stream characteristics before composition.
  // FFmpeg 7 xfade is stricter about matching fps/timebase/pixel format inputs.
  for (let i = 0; i < slideConfigs.length; i += 1) {
    parts.push(
      `[raw${i}]fps=${fps},format=yuv420p,settb=AVTB,setpts=N/(${fps}*TB),setsar=1:1[v${i}]`
    );
  }

  // Compose slides. xfade gives smooth transitions; fade_concat is a smoother
  // fallback than hard cuts when xfade fails in stricter environments.
  const mode = String(compositorMode || "concat").trim().toLowerCase();
  if (mode === "xfade") {
    let current = "v0";
    const xfadeDuration = Math.max(1 / fps, crossfadeUsed);
    if (useFrameQuantizedTiming) {
      let timelineFrames = slideConfigs[0].frames;
      for (let i = 1; i < slideConfigs.length; i += 1) {
        const out = `x${i}`;
        const offsetFrames = Math.max(0, timelineFrames - crossfadeFrames);
        const offset = offsetFrames / fps;
        parts.push(`[${current}][v${i}]xfade=transition=fade:duration=${xfadeDuration.toFixed(6)}:offset=${offset.toFixed(6)}[${out}]`);
        current = out;
        timelineFrames += slideConfigs[i].frames - crossfadeFrames;
      }
    } else {
      let timeline = slideConfigs[0].durationUsed;
      for (let i = 1; i < slideConfigs.length; i += 1) {
        const out = `x${i}`;
        const offset = Math.max(0, timeline - crossfadeUsed);
        parts.push(`[${current}][v${i}]xfade=transition=fade:duration=${xfadeDuration.toFixed(6)}:offset=${offset.toFixed(6)}[${out}]`);
        current = out;
        timeline += slideConfigs[i].durationUsed - crossfadeUsed;
      }
    }
    parts.push(`[${current}]format=yuv420p[vout]`);
  } else if (mode === "fade_concat") {
    const labels = [];
    for (let i = 0; i < slideConfigs.length; i += 1) {
      const isFirst = i === 0;
      const isLast = i === (slideConfigs.length - 1);
      const fadeDur = Math.max(0, Math.min(crossfadeUsed / 2, slideConfigs[i].durationUsed / 3));
      let current = `v${i}`;
      if (!isFirst && fadeDur > 0) {
        const withIn = `vin${i}`;
        parts.push(`[${current}]fade=t=in:st=0:d=${fadeDur.toFixed(6)}[${withIn}]`);
        current = withIn;
      }
      if (!isLast && fadeDur > 0) {
        const withOut = `vfade${i}`;
        const outStart = Math.max(0, slideConfigs[i].durationUsed - fadeDur);
        parts.push(`[${current}]fade=t=out:st=${outStart.toFixed(6)}:d=${fadeDur.toFixed(6)}[${withOut}]`);
        current = withOut;
      }
      labels.push(`[${current}]`);
    }
    if (labels.length === 1) {
      parts.push(`${labels[0]}format=yuv420p[vout]`);
    } else {
      parts.push(`${labels.join("")}concat=n=${labels.length}:v=1:a=0[vcat]`);
      parts.push("[vcat]format=yuv420p[vout]");
    }
  } else {
    if (slideConfigs.length === 1) {
      parts.push("[v0]format=yuv420p[vout]");
    } else {
      const concatInputs = slideConfigs.map((_, idx) => `[v${idx}]`).join("");
      parts.push(`${concatInputs}concat=n=${slideConfigs.length}:v=1:a=0[vcat]`);
      parts.push("[vcat]format=yuv420p[vout]");
    }
  }

  let computedDuration;
  if (mode === "xfade") {
    if (useFrameQuantizedTiming) {
      const totalFrames = slideConfigs.reduce((acc, slide) => acc + slide.frames, 0);
      computedDuration = (totalFrames - ((slideConfigs.length - 1) * crossfadeFrames)) / fps;
    } else {
      computedDuration = slideConfigs.reduce((acc, slide) => acc + slide.durationUsed, 0) - (slideConfigs.length - 1) * crossfadeUsed;
    }
  } else {
    if (useFrameQuantizedTiming) {
      const totalFrames = slideConfigs.reduce((acc, slide) => acc + slide.frames, 0);
      computedDuration = totalFrames / fps;
    } else {
      computedDuration = slideConfigs.reduce((acc, slide) => acc + slide.durationUsed, 0);
    }
  }
  const totalDuration = Number.isFinite(requestedDuration) && requestedDuration > 0
    ? requestedDuration
    : computedDuration;
  return { filterComplex: parts.join(";"), totalDuration, fps, compositorUsed: mode };
}

function writeRenderStatus(statusPath, payload) {
  if (!statusPath) return;
  try {
    fs.mkdirSync(path.dirname(statusPath), { recursive: true });
    fs.writeFileSync(statusPath, JSON.stringify(payload, null, 2));
  } catch (_err) {
    // Best effort only.
  }
}

async function run() {
  const payload = parsePayload(process.argv[2]);
  
  // Debug logging - set RENDER_DEBUG env var to enable
  if (process.env.RENDER_DEBUG) {
    console.log("[DEBUG] === RENDER START ===");
    console.log("[DEBUG] Payload received:", JSON.stringify({
      slug: payload.slug,
      video: {
        fps: payload.video?.fps,
        output_size: payload.video?.output_size,
        artwork: payload.video?.artwork,
        mockups: payload.video?.mockups,
        mockup_shots_count: Array.isArray(payload.video?.mockup_shots) ? payload.video.mockup_shots.length : 0,
        include_master_slide: payload.video?.include_master_slide,
      }
    }, null, 2));
  }

  const slug = String(payload.slug || "").trim();
  const masterPath = String(payload.master_path || "").trim();
  const processedRoot = payload.processed_root ? String(payload.processed_root).trim() : "";
  const masterMode = String(payload.master_mode || "square").trim().toLowerCase();
  const outputPath = String(payload.output_path || "").trim();
  const ffmpegBin = String(payload.ffmpeg_bin || "ffmpeg").trim() || "ffmpeg";
  const renderStatusPath = payload.render_status_path ? String(payload.render_status_path) : "";
  const video = payload.video || {};
  const includeMasterSlide = Boolean(video.include_master_slide);

  const artworkSource = String(video.artwork_source || "auto").trim().toLowerCase();

  const closeupProxyPath = processedRoot
    ? path.join(processedRoot, slug, `${slug}-CLOSEUP-PROXY.jpg`)
    : "";
  const masterCandidatePath = processedRoot
    ? path.join(processedRoot, slug, `${slug}-MASTER.jpg`)
    : masterPath;
  let resolvedMasterPath = masterPath;
  if (artworkSource === "closeup_proxy") {
    resolvedMasterPath = closeupProxyPath && fs.existsSync(closeupProxyPath) ? closeupProxyPath : masterCandidatePath;
  } else if (artworkSource === "master") {
    resolvedMasterPath = masterCandidatePath || masterPath;
  } else {
    resolvedMasterPath = closeupProxyPath && fs.existsSync(closeupProxyPath) ? closeupProxyPath : masterCandidatePath;
  }

  if (!slug || !resolvedMasterPath || !outputPath) {
    throw new Error("Missing required payload values: slug/master_path/output_path");
  }

  // Runtime diagnostics for parity investigations.
  process.stdout.write(`render.js ffmpeg_path=${ffmpegBin}\n`);
  if (process.env.RENDER_DEBUG || process.env.ARTLOMO_VIDEO_LOG_FFMPEG_VERSION === "1") {
    try {
      const v = spawnSync(ffmpegBin, ["-hide_banner", "-version"], { encoding: "utf8" });
      const line = String((v && v.stdout) || "").split("\n").find(Boolean) || String((v && v.stderr) || "").split("\n").find(Boolean) || "unknown";
      process.stdout.write(`render.js ffmpeg_version=${line.trim()}\n`);
    } catch (_err) {
      process.stdout.write("render.js ffmpeg_version=unavailable\n");
    }
  }

  const targets = resolveMockupTargets(payload);
  if (!targets.length) {
    throw new Error("No mockup_paths provided to Node worker");
  }

  fs.mkdirSync(path.dirname(outputPath), { recursive: true });

  const slides = [
    ...(includeMasterSlide ? [{ path: resolvedMasterPath, role: "master", targetX: 0.5, targetY: 0.5, category: "" }] : []),
    ...targets.map((target) => ({ path: target.path, role: "mockup", targetX: target.targetX, targetY: target.targetY, hasTarget: target.hasTarget, category: target.category })),
  ];
  if (!slides.length) {
    throw new Error("No renderable slides available after storyboard filtering");
  }

  const requestedModeRaw = String(video.compositor || process.env.ARTLOMO_VIDEO_COMPOSITOR || "auto").trim().toLowerCase();
  const requestedMode = ["auto", "xfade", "fade_concat", "concat"].includes(requestedModeRaw) ? requestedModeRaw : "auto";
  const modeAttempts = requestedMode === "auto"
    ? ["xfade", "fade_concat", "concat"]
    : requestedMode === "xfade"
      ? ["xfade"]
      : requestedMode === "fade_concat"
        ? ["fade_concat"]
      : ["concat"];

  let lastErr = null;
  for (let idx = 0; idx < modeAttempts.length; idx += 1) {
    const mode = modeAttempts[idx];
    const frameGenerationStart = Date.now();
    const { filterComplex, totalDuration, fps, compositorUsed } = buildFilter(slides, video, masterMode, mode);
    const frameGenerationEnd = Date.now();

    process.stdout.write(`render.js compositor=${compositorUsed} requested=${requestedMode} attempt=${idx + 1}/${modeAttempts.length}\n`);
    process.stdout.write(`render.js output_path=${outputPath} fps=${fps}\n`);
    if (process.env.RENDER_DEBUG) {
      console.log("[DEBUG] filter_complex:", filterComplex);
    }
    process.stdout.write(`render.js timing frame_generation_ms=${frameGenerationEnd - frameGenerationStart}\n`);

    const totalFrames = Math.max(1, Math.round(Number(fps || 24) * Number(totalDuration || 0)));
    const startedAt = new Date().toISOString();
    writeRenderStatus(renderStatusPath, {
      slug,
      frames_completed: 0,
      total_frames: totalFrames,
      started_at: startedAt,
    });

    const cmdArgs = ["-y"];
    for (const slide of slides) {
      cmdArgs.push("-loop", "1", "-i", slide.path);
    }
    cmdArgs.push(
      "-filter_complex",
      filterComplex,
      "-map",
      "[vout]",
      "-r",
      String(fps),
      "-t",
      totalDuration.toFixed(3),
      "-progress",
      "pipe:1",
      "-nostats",
      "-c:v",
      String(video.codec || "libx264"),
      "-preset",
      String(video.encoder_preset || video.preset || "fast"),
      "-crf",
      String(Number(video.crf || 20)),
      "-threads",
      "0",
      "-pix_fmt",
      "yuv420p",
      "-movflags",
      "+faststart",
      outputPath
    );

    const ffmpegEncodeStart = Date.now();
    const ffmpeg = spawn(ffmpegBin, cmdArgs, { stdio: ["ignore", "pipe", "pipe"] });
    let stderr = "";
    let buffer = "";
    let lastFrame = 0;
    let lastWrite = 0;

    const flushStatus = (frame) => {
      const now = Date.now();
      if (now - lastWrite < 250) return;
      lastWrite = now;
      writeRenderStatus(renderStatusPath, {
        slug,
        frames_completed: frame,
        total_frames: totalFrames,
        started_at: startedAt,
      });
    };

    if (ffmpeg.stdout) {
      ffmpeg.stdout.on("data", (chunk) => {
        buffer += chunk.toString();
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";
        for (const line of lines) {
          const [key, value] = line.trim().split("=");
          if (key === "frame") {
            const frameVal = Number(value || 0);
            if (Number.isFinite(frameVal) && frameVal > lastFrame) {
              lastFrame = Math.min(totalFrames, Math.floor(frameVal));
              flushStatus(lastFrame);
            }
          }
          if (key === "progress" && value === "end") {
            lastFrame = totalFrames;
            flushStatus(lastFrame);
          }
        }
      });
    }

    if (ffmpeg.stderr) {
      ffmpeg.stderr.on("data", (chunk) => {
        stderr += chunk.toString();
      });
    }

    const exitCode = await new Promise((resolve) => {
      ffmpeg.on("close", resolve);
    });
    const ffmpegEncodeEnd = Date.now();
    process.stdout.write(`render.js timing ffmpeg_encode_ms=${ffmpegEncodeEnd - ffmpegEncodeStart}\n`);

    if (exitCode === 0 && fs.existsSync(outputPath) && fs.statSync(outputPath).size > 0) {
      writeRenderStatus(renderStatusPath, {
        slug,
        frames_completed: totalFrames,
        total_frames: totalFrames,
        started_at: startedAt,
      });
      process.stdout.write(JSON.stringify({ ok: true, slug, output_path: outputPath, compositor: compositorUsed }));
      return;
    }

    lastErr = (stderr || "ffmpeg failed").slice(-4000);
    process.stderr.write(`render.js compositor attempt failed: ${compositorUsed}; reason=${summarizeFfmpegError(stderr)}\n`);
    if (idx < modeAttempts.length - 1) {
      process.stderr.write("render.js falling back to alternate compositor\n");
    }
  }

  throw new Error(lastErr || "Output video missing or empty");
}

run().catch((err) => {
  process.stderr.write(`render.js failed: ${err && err.message ? err.message : String(err)}\n`);
  process.exit(1);
});
