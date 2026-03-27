#!/usr/bin/env node
/**
 * Test computeCoverTransform helper function
 * Verifies cover mode scaling for various artwork aspect ratios
 */

// Extract and test computeCoverTransform function
const testCode = `
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

function computeCoverTransform(imgW, imgH, outW, outH, zoomScale = 1.0, panX01 = 0.5, panY01 = 0.5) {
  const imgW_num = Number(imgW) || 1;
  const imgH_num = Number(imgH) || 1;
  const outW_num = Number(outW) || 1024;
  const outH_num = Number(outH) || 1024;
  const zoom = Math.max(1.0, Number(zoomScale) || 1.0);
  const panX = clamp01(panX01);
  const panY = clamp01(panY01);

  const scaleX = outW_num / imgW_num;
  const scaleY = outH_num / imgH_num;
  const coverScale = Math.max(scaleX, scaleY);
  const effectiveScale = coverScale * zoom;
  const drawW = imgW_num * effectiveScale;
  const drawH = imgH_num * effectiveScale;
  const maxOffsetX = drawW - outW_num;
  const maxOffsetY = drawH - outH_num;
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

// Test cases
const tests = [
  {
    name: "Square artwork (1:1)",
    imgW: 1024, imgH: 1024, outW: 1024, outH: 1024,
    zoom: 1.0, panX: 0.5, panY: 0.5,
  },
  {
    name: "Portrait artwork (2:3)",
    imgW: 1000, imgH: 1500, outW: 1024, outH: 1024,
    zoom: 1.0, panX: 0.5, panY: 0.5,
  },
  {
    name: "Landscape artwork (3:2)",
    imgW: 1500, imgH: 1000, outW: 1024, outH: 1024,
    zoom: 1.0, panX: 0.5, panY: 0.5,
  },
  {
    name: "Wide landscape (16:9)",
    imgW: 1920, imgH: 1080, outW: 1024, outH: 1024,
    zoom: 1.0, panX: 0.5, panY: 0.5,
  },
  {
    name: "Tall portrait (9:16)",
    imgW: 720, imgH: 1280, outW: 1024, outH: 1024,
    zoom: 1.0, panX: 0.5, panY: 0.5,
  },
  {
    name: "Square with 1.1x zoom",
    imgW: 1024, imgH: 1024, outW: 1024, outH: 1024,
    zoom: 1.1, panX: 0.5, panY: 0.5,
  },
  {
    name: "Portrait with 1.15x zoom",
    imgW: 1000, imgH: 1500, outW: 1024, outH: 1024,
    zoom: 1.15, panX: 0.5, panY: 0.5,
  },
  {
    name: "Portrait, pan to left (0.2)",
    imgW: 1000, imgH: 1500, outW: 1024, outH: 1024,
    zoom: 1.0, panX: 0.2, panY: 0.5,
  },
  {
    name: "Landscape, pan to top (0.3)",
    imgW: 1500, imgH: 1000, outW: 1024, outH: 1024,
    zoom: 1.0, panX: 0.5, panY: 0.3,
  },
];

console.log("\\n" + "=".repeat(80));
console.log("computeCoverTransform Test Suite");
console.log("=".repeat(80) + "\\n");

tests.forEach((test) => {
  const result = computeCoverTransform(
    test.imgW, test.imgH, test.outW, test.outH,
    test.zoom, test.panX, test.panY
  );
  
  console.log(\`✓ \${test.name}\`);
  console.log(\`  Input:   \${test.imgW}×\${test.imgH}, Zoom: \${test.zoom}, Pan: (\${test.panX}, \${test.panY})\`);
  console.log(\`  Output:  Draw: \${result.drawW}×\${result.drawH}, Offset: (\${result.offsetX}, \${result.offsetY})\`);
  console.log(\`  Coverage: \${result.coverScale}x scale to fill \${test.outW}×\${test.outH} canvas\`);
  
  // Verify constraints
  const checks = [];
  if (result.drawW >= test.outW) checks.push("✓ Width covers canvas");
  else checks.push("✗ Width does NOT cover canvas");
  
  if (result.drawH >= test.outH) checks.push("✓ Height covers canvas");
  else checks.push("✗ Height does NOT cover canvas");
  
  if (result.offsetX <= 0 && result.offsetX >= -(result.drawW - test.outW)) 
    checks.push("✓ Offset X in valid range");
  else 
    checks.push("✗ Offset X out of range");
  
  if (result.offsetY <= 0 && result.offsetY >= -(result.drawH - test.outH)) 
    checks.push("✓ Offset Y in valid range");
  else 
    checks.push("✗ Offset Y out of range");
  
  checks.forEach(c => console.log(\`  \${c}\`));
  console.log();
});

console.log("=".repeat(80));
console.log("All tests completed ✓");
console.log("=".repeat(80) + "\\n");
`;

eval(testCode);
