"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const { pathToFileURL } = require("node:url");
const { chromium, expect } = require("playwright/test");

const root = path.resolve(__dirname, "..");
const assets = path.join(root, "android-tablet", "app", "src", "main", "assets", "www");
const output = path.join(root, ".test-output", "tablet");
const sandbox = { window: {} };
vm.runInNewContext(fs.readFileSync(path.join(assets, "catalog.js"), "utf8"), sandbox);
const catalog = sandbox.window.MAP_CATALOG;
const errors = [];
const networkRequests = [];
let browser;

async function settled(page) {
  await page.locator("#main img").evaluateAll((images) => images.forEach((img) => { img.loading = "eager"; }));
  await page.waitForFunction(() => [...document.querySelectorAll("#main img")].every((img) => img.complete && img.naturalWidth > 0));
  await page.waitForFunction(() => [...document.querySelectorAll(".cute-thumb .missing-img")].every((fallback) => getComputedStyle(fallback).display === "none"));
  const thumbnails = await page.locator(".cute-thumb img").evaluateAll((images) => images.map((img) => {
    const container = img.parentElement;
    const fallback = container.querySelector(".missing-img");
    const imageBox = img.getBoundingClientRect();
    const containerBox = container.getBoundingClientRect();
    return {
      src: img.getAttribute("src"),
      fallbackHidden: !fallback || getComputedStyle(fallback).display === "none",
      insideCard: imageBox.width > 0 && imageBox.height > 0 &&
        imageBox.top >= containerBox.top - 1 && imageBox.bottom <= containerBox.bottom + 1,
    };
  }));
  assert(thumbnails.every((item) => item.fallbackHidden && item.insideCard), "Loaded thumbnails must be visible inside their cards: " + JSON.stringify(thumbnails));
}

async function noOverflow(page) {
  assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true, "Page must fit tablet width");
}

(async () => {
  assert.equal(sandbox.window.MAP_RUNTIME, "android");
  assert.equal(catalog.series.length, 2);
  const imagePaths = catalog.series.flatMap((s) => s.classes.flatMap((c) => [c.thumbnail, ...c.maps.flatMap((m) => [m.thumbnail, m.detail])])).filter(Boolean);
  assert.equal(imagePaths.length, 92, "All 43 maps and their available images must be packaged");
  for (const image of imagePaths) assert(fs.existsSync(path.resolve(assets, decodeURIComponent(image))), image);
  for (const asset of ["icos/s0.png", "icos/s1.png", "assets/avatar.png"]) {
    assert(fs.existsSync(path.join(assets, asset)), "Missing local home image: " + asset);
  }
  fs.mkdirSync(output, { recursive: true });
  browser = await chromium.launch({
    executablePath: process.env.MAP_TEST_BROWSER || "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    headless: true,
  });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 }, deviceScaleFactor: 1, isMobile: true, hasTouch: true,
    userAgent: "Mozilla/5.0 (Linux; Android 14; Tablet) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
  });
  await context.setOffline(true);
  const page = await context.newPage();
  page.on("pageerror", (error) => errors.push(error.message));
  page.on("request", (request) => { if (/^https?:/.test(request.url())) networkRequests.push(request.url()); });
  const entry = pathToFileURL(path.join(assets, "index.html")).href;
  await page.goto(entry);
  await expect(page.locator(".cute-series-card")).toHaveCount(2);
  await settled(page);
  await noOverflow(page);
  await expect(page.locator("#syncStatus")).toContainText("地图已随软件离线内置");
  assert.equal(await page.evaluate(() => window.MapHelperAndroid.back()), false, "Home back allows Android Activity to exit");
  await page.screenshot({ path: path.join(output, "home-landscape.png"), fullPage: true });

  for (const series of catalog.series) {
    await page.locator('[data-series-id="' + series.id + '"]').tap();
    await expect(page.locator("#pageTitle")).toHaveText(series.label);
    await expect(page.locator(".cute-dir-card")).toHaveCount(series.classes.length);
    for (const c of series.classes) {
      await page.locator('[data-class-id="' + c.id + '"]').tap();
      await expect(page.locator("#pageTitle")).toHaveText(c.label);
      await expect(page.locator(".cute-map-card")).toHaveCount(c.maps.length);
      await settled(page);
      const first = c.maps.find((m) => m.detail);
      if (first) {
        await page.locator('[data-map-id="' + first.id + '"]').tap();
        await expect(page.locator("#viewerImg")).toBeVisible();
        await expect(page.locator("#zoomLabel")).toHaveText("100%");
        assert.equal(await page.evaluate(() => window.MapHelperAndroid.back()), true);
        await expect(page.locator("#viewer")).toBeHidden();
        await expect(page.locator("#pageTitle")).toHaveText(c.label);
      }
      assert.equal(await page.evaluate(() => window.MapHelperAndroid.back()), true);
      await expect(page.locator("#pageTitle")).toHaveText(series.label);
    }
    assert.equal(await page.evaluate(() => window.MapHelperAndroid.back()), true);
    await expect(page.locator(".cute-series-card")).toHaveCount(2);
  }
  console.log("PASS: offline local assets, both series, all ten categories, map images, Android back routing");

  await page.locator('[data-series-id="phosphor"]').tap();
  await page.locator('[data-class-id="class1"]').tap();
  await settled(page);
  await page.screenshot({ path: path.join(output, "category-landscape.png"), fullPage: true });
  await page.locator('[data-map-id="map1"]').tap();
  await expect(page.locator("#viewerImg")).toBeVisible();
  await page.screenshot({ path: path.join(output, "detail-landscape.png") });
  await page.locator("#zoomIn").tap();
  await expect(page.locator("#zoomLabel")).toHaveText("140%");
  await page.locator("#viewerReset").tap();
  await expect(page.locator("#zoomLabel")).toHaveText("100%");
  const stage = await page.locator("#viewerStage").boundingBox();
  const cx = stage.x + stage.width / 2;
  const cy = stage.y + stage.height / 2;
  const cdp = await context.newCDPSession(page);
  function touches(radius) {
    return [
      { x: cx - radius, y: cy, radiusX: 3, radiusY: 3, force: 1, id: 1 },
      { x: cx + radius, y: cy, radiusX: 3, radiusY: 3, force: 1, id: 2 },
    ];
  }
  await cdp.send("Input.dispatchTouchEvent", { type: "touchStart", touchPoints: touches(30) });
  for (const radius of [45, 60, 80, 100, 120]) {
    await cdp.send("Input.dispatchTouchEvent", { type: "touchMove", touchPoints: touches(radius) });
    await page.waitForTimeout(20);
  }
  await cdp.send("Input.dispatchTouchEvent", { type: "touchEnd", touchPoints: [] });
  assert(parseInt(await page.locator("#zoomLabel").textContent(), 10) >= 200, "Two-finger pinch must zoom the map");
  const before = await page.locator("#viewerImg").evaluate((img) => img.style.transform);
  await cdp.send("Input.dispatchTouchEvent", { type: "touchStart", touchPoints: [{ x: cx, y: cy, id: 1 }] });
  await cdp.send("Input.dispatchTouchEvent", { type: "touchMove", touchPoints: [{ x: cx + 55, y: cy + 20, id: 1 }] });
  await cdp.send("Input.dispatchTouchEvent", { type: "touchEnd", touchPoints: [] });
  assert.notEqual(await page.locator("#viewerImg").evaluate((img) => img.style.transform), before, "Single-finger drag must pan");
  await page.setViewportSize({ width: 800, height: 1280 });
  await expect(page.locator("#zoomLabel")).toHaveText("100%");
  await expect(page.locator("#viewerImg")).toBeVisible();
  const fit = await page.locator("#viewerImg").boundingBox();
  const portraitStage = await page.locator("#viewerStage").boundingBox();
  assert(fit.width <= portraitStage.width && fit.height <= portraitStage.height, "Rotation must refit without clipping");
  await page.screenshot({ path: path.join(output, "detail-portrait.png") });
  await page.locator("#viewerClose").tap();
  await expect(page.locator("#viewer")).toBeHidden({ timeout: 3000 });
  await settled(page);
  await noOverflow(page);
  await page.screenshot({ path: path.join(output, "category-portrait.png"), fullPage: true });
  await page.locator("#backBtn").tap();
  await expect(page.locator(".cute-dir-card")).toHaveCount(6);
  await page.locator("#backBtn").tap();
  await settled(page);
  await noOverflow(page);
  await page.screenshot({ path: path.join(output, "home-portrait.png"), fullPage: true });
  await page.setViewportSize({ width: 600, height: 800 });
  await noOverflow(page);
  await page.screenshot({ path: path.join(output, "home-split-screen.png"), fullPage: true });
  assert.equal((await page.locator("body").innerText()).includes("EXE"), false);
  assert.deepEqual(networkRequests, [], "Android assets must not request API endpoints or remote URLs");
  assert.deepEqual(errors, [], "No JavaScript errors");
  const report = {
    passed: true, offline: true, series: catalog.series.length,
    categories: catalog.series.reduce((n, s) => n + s.classes.length, 0),
    maps: catalog.series.reduce((n, s) => n + s.classes.reduce((total, c) => total + c.maps.length, 0), 0),
    packagedImages: imagePaths.length, touchPinch: true, touchPan: true,
    landscape: true, portrait: true, splitScreen: true, androidBackBridge: true,
    physicalDeviceTested: false,
  };
  fs.writeFileSync(path.join(output, "report.json"), JSON.stringify(report, null, 2), "utf8");
  console.log("PASS: touch pinch/drag, rotation, portrait, split screen, no desktop-only UI, no network requests");
  console.log(JSON.stringify(report, null, 2));
})().catch((error) => { console.error(error); process.exitCode = 1; })
  .finally(async () => { if (browser) await browser.close(); });
