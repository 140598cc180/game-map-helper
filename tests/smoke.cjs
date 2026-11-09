"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const net = require("node:net");
const vm = require("node:vm");
const { spawn } = require("node:child_process");
const { once } = require("node:events");
const { pathToFileURL } = require("node:url");
const { chromium, expect } = require("playwright/test");

const root = path.resolve(__dirname, "..");
const output = path.join(root, ".test-output");
const exe = path.join(root, "地图系列小助手.exe");
const errors = [];
const children = [];
let browser;
let fixture;
const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function freePort() {
  const server = net.createServer();
  server.listen(0, "127.0.0.1");
  await once(server, "listening");
  const port = server.address().port;
  await new Promise((resolve) => server.close(resolve));
  return port;
}
async function startServer(file) {
  const port = await freePort();
  const child = spawn(file, ["--serve", "--port", String(port)], { windowsHide: true, stdio: "ignore" });
  children.push(child);
  let spawnError;
  child.on("error", (error) => { spawnError = error; });
  const url = "http://127.0.0.1:" + port + "/";
  for (let attempt = 0; attempt < 60; attempt++) {
    if (spawnError) throw spawnError;
    if (child.exitCode !== null) throw new Error("Server exited: " + child.exitCode);
    try {
      const response = await fetch(url + "catalog.js");
      if (response.ok) return url;
    } catch {}
    await delay(100);
  }
  throw new Error("Local server did not become ready");
}
async function settleImages(page) {
  await page.locator("#main img").evaluateAll((images) => images.forEach((img) => { img.loading = "eager"; }));
  await page.waitForFunction(() => [...document.querySelectorAll("#main img")].every((img) => img.complete && img.naturalWidth > 0));
  await page.waitForTimeout(50);
  await assertThumbnailsRendered(page);
}
async function assertThumbnailsRendered(page) {
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
async function readCatalog(url) {
  const response = await fetch(url + "catalog.js");
  assert.equal(response.status, 200);
  const sandbox = { window: {} };
  vm.runInNewContext(await response.text(), sandbox);
  return sandbox.window.MAP_CATALOG;
}
function write(relative, bytes) {
  const full = path.join(fixture, relative);
  fs.mkdirSync(path.dirname(full), { recursive: true });
  fs.writeFileSync(full, bytes);
}
async function stop(child) {
  if (child.exitCode !== null || child.signalCode !== null) return;
  child.kill();
  await Promise.race([once(child, "exit"), delay(4000)]);
}

(async () => {
  fs.mkdirSync(output, { recursive: true });
  const realUrl = await startServer(exe);
  const real = await readCatalog(realUrl);
  assert.equal(real.series.length, 2);
  assert.equal(real.series[0].id, "nightmare-woman");
  assert.equal(real.series[0].classes.length, 4);
  assert.equal(real.series[0].classes.reduce((n, c) => n + c.maps.length, 0), 28);
  assert.equal(real.series[1].id, "phosphor");
  assert.equal(real.series[1].classes.length, 6);
  assert.equal(real.series[1].classes.reduce((n, c) => n + c.maps.length, 0), 15);
  for (const series of real.series) {
    for (const c of series.classes) {
      assert(c.maps.every((m, n) => !n || m.number > c.maps[n - 1].number));
      for (const imagePath of [c.thumbnail, ...c.maps.flatMap((m) => [m.thumbnail, m.detail])].filter(Boolean)) {
        const response = await fetch(new URL(imagePath, realUrl));
        assert.equal(response.status, 200, imagePath);
        assert(response.headers.get("content-type").startsWith("image/"));
        assert((await response.arrayBuffer()).byteLength > 0);
      }
    }
  }
  assert.equal((await fetch(realUrl + "MapHelper.cs")).status, 404);
  assert.equal((await fetch(realUrl + "%2e%2e/MapHelper.cs")).status, 404);
  assert.equal((await fetch(realUrl + "api/catalog")).status, 404);
  assert.equal((await fetch(realUrl + "api/catalog", { method: "POST" })).status, 405);
  const head = await fetch(realUrl, { method: "HEAD" });
  assert.equal(head.status, 200);
  assert.equal((await head.arrayBuffer()).byteLength, 0);
  console.log("PASS: real image catalog, all image routes, HEAD, source isolation");

  const browserPath = process.env.MAP_TEST_BROWSER || "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe";
  browser = await chromium.launch({ executablePath: browserPath, headless: true });
  const page = await browser.newPage({ viewport: { width: 1000, height: 900 } });
  page.on("pageerror", (error) => errors.push(error.message));
  await page.goto(realUrl);
  await expect(page.locator(".cute-series-card")).toHaveCount(2);
  await expect(page.locator(".cute-usage-text")).toContainText("-1 层直接左转");
  await expect(page.locator(".cute-usage-text")).toContainText("逆时针走");
  await expect(page.locator(".cute-author-tags")).toContainText("网络地图搜集");
  await expect(page.locator(".cute-contact")).toContainText("微信：LittleLion_cc817");
  await expect(page.locator(".cute-original-note")).toContainText("地图本身非原创");
  await expect(page.locator(".cute-original-note")).toContainText("有改进建议欢迎联系");
  const decoded = await page.evaluate(async (paths) => {
    return Promise.all(paths.map(async (src) => {
      const img = new Image(); img.src = src;
      try { await img.decode(); return { src, ok: true }; }
      catch { return { src, ok: false }; }
    }));
  }, real.series.flatMap((s) => s.classes.flatMap((c) => [c.thumbnail, ...c.maps.flatMap((m) => [m.thumbnail, m.detail])])).filter(Boolean));
  assert(decoded.every((image) => image.ok), JSON.stringify(decoded.filter((image) => !image.ok)));
  await settleImages(page); await page.screenshot({ path: path.join(output, "home-desktop.png"), fullPage: true });
  await page.goto(realUrl + "#/series/phosphor/class3");
  await expect(page.locator(".cute-thumb img")).toHaveCount(4);
  await page.waitForFunction(() => [...document.querySelectorAll(".cute-thumb img")].every((img) => img.complete && img.naturalWidth > 0));
  await assertThumbnailsRendered(page);
  await page.screenshot({ path: path.join(output, "phosphor-class3-loaded.png"), fullPage: true });
  console.log("PASS: class 3 thumbnails render inside cards with loading placeholders hidden");
  const mapCardWidth = (await page.locator(".cute-map-card").first().boundingBox()).width;
  for (const [classId, count] of [["class4", 1], ["class5", 2], ["class1", 3]]) {
    await page.goto(realUrl + "#/series/phosphor/" + classId);
    await expect(page.locator(".cute-map-card")).toHaveCount(count);
    await settleImages(page);
    const width = (await page.locator(".cute-map-card").first().boundingBox()).width;
    assert(Math.abs(width - mapCardWidth) < 1, "Sparse categories must keep the same thumbnail size: " + classId);
    if (count === 1) await page.screenshot({ path: path.join(output, "phosphor-class4-fixed-columns.png"), fullPage: true });
  }
  await page.goto(realUrl);
  await page.locator('[data-series-id="nightmare-woman"]').click();
  await expect(page.locator("#pageTitle")).toHaveText("噩梦之女");
  await expect(page.locator(".cute-dir-card")).toHaveCount(4);
  await page.locator('[data-class-id="class1"]').click();
  await expect(page.locator("#pageTitle")).toHaveText("北门");
  await expect(page.locator(".cute-map-card")).toHaveCount(real.series[0].classes[0].maps.length);
  await settleImages(page); await page.screenshot({ path: path.join(output, "category-desktop.png"), fullPage: true });
  const mapCards = await page.locator(".cute-map-card").evaluateAll((cards) => cards.map((card) => {
    const rect = card.getBoundingClientRect();
    return { top: Math.round(rect.top), width: rect.width };
  }));
  const rows = new Map();
  for (const card of mapCards) rows.set(card.top, (rows.get(card.top) || 0) + 1);
  assert.equal(rows.size, 2, "Eight maps must wrap into two rows");
  assert([...rows.values()].every((count) => count <= 4), "Each map row must contain at most four cards");
  assert(mapCards.every((card) => Math.abs(card.width - mapCardWidth) < 1), "Map card width must stay consistent across categories");
  console.log("PASS: one to four maps retain their size; eight maps wrap into rows of four");
  const readyMap = real.series[1].classes.flatMap((c) => c.maps.filter((m) => m.detail).map((m) => ({ c, m })))[0];
  if (readyMap) {
    await page.goto(realUrl + "#/series/phosphor/" + readyMap.c.id + "/" + readyMap.m.id);
    await expect(page.locator("#viewerImg")).toBeVisible();
    await expect(page.locator("#viewerTitle")).toContainText("磷光症");
    await expect(page.locator("#zoomLabel")).toHaveText("100%");
    const fit = await page.locator("#viewerImg").boundingBox();
    const stage = await page.locator("#viewerStage").boundingBox();
    assert(fit.width <= stage.width && fit.height <= stage.height, "Fitted image must stay inside stage");
    await settleImages(page); await page.screenshot({ path: path.join(output, "detail-desktop.png") });
    await page.locator("#zoomIn").click();
    await expect(page.locator("#zoomLabel")).toHaveText("140%");
    await page.locator("#viewerReset").click();
    await expect(page.locator("#zoomLabel")).toHaveText("100%");
    await page.locator("#viewerStage").dblclick();
    await expect(page.locator("#zoomLabel")).toHaveText("250%");
    await page.mouse.move(stage.x + stage.width / 2, stage.y + stage.height / 2);
    await page.mouse.wheel(0, -100);
    await expect(page.locator("#zoomLabel")).not.toHaveText("250%");
    const before = await page.locator("#viewerImg").evaluate((img) => img.style.transform);
    await page.mouse.down();
    await page.mouse.move(stage.x + stage.width / 2 + 45, stage.y + stage.height / 2 + 30, { steps: 5 });
    await page.mouse.up();
    const after = await page.locator("#viewerImg").evaluate((img) => img.style.transform);
    assert.notEqual(after, before, "Panning must move a zoomed map");
    await page.keyboard.press("Escape");
    await expect(page.locator("#viewer")).toBeHidden();
    assert.equal(await page.locator("#app").evaluate((el) => el.inert), false);
    await page.locator("#backBtn").click();
    await expect(page.locator(".cute-dir-card")).toHaveCount(6);
    await page.goBack();
    await expect(page.locator("#pageTitle")).toHaveText(readyMap.c.label);
    await page.goForward();
    await expect(page.locator(".cute-dir-card")).toHaveCount(6);
  }
  for (const width of [360, 390, 560]) {
    await page.setViewportSize({ width, height: 880 });
    await page.goto(realUrl);
    await expect(page.locator(".cute-series-card")).toHaveCount(2);
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true, "Home overflow at " + width);
    const homeCopyFits = await page.locator(".cute-usage-text, .cute-contact, .cute-original-note-v7").evaluateAll((items) => items.every((item) => item.scrollWidth <= item.clientWidth));
    assert.equal(homeCopyFits, true, "Home instructions and author details must wrap at " + width);
    const squares = await page.locator(".cute-series-card").evaluateAll((cards) => cards.map((c) => ({ width: c.getBoundingClientRect().width, height: c.getBoundingClientRect().height })));
    assert(squares.every((s) => Math.abs(s.width - squares[0].width) < 2 && Math.abs(s.height - squares[0].height) < 2), "Series cards must retain the original equal sizing at " + width + ": " + JSON.stringify(squares));
    if (width === 390) { await settleImages(page); await page.screenshot({ path: path.join(output, "home-mobile.png"), fullPage: true }); }
    await page.locator('[data-series-id="phosphor"]').click();
    await expect(page.locator(".cute-dir-card")).toHaveCount(6);
    await page.locator('[data-class-id="class1"]').click();
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true, "Category overflow at " + width);
    if (width === 390) { await settleImages(page); await page.screenshot({ path: path.join(output, "category-mobile.png"), fullPage: true }); }
  }
  console.log("PASS: desktop/mobile layouts, routing, detail fit, zoom, wheel, pan, keyboard");

  fixture = fs.mkdtempSync(path.join(os.tmpdir(), "phosphor-map-test-"));
  const fixtureExe = path.join(fixture, path.basename(exe));
  fs.copyFileSync(exe, fixtureExe);
  fs.copyFileSync(path.join(root, "catalog.js"), path.join(fixture, "catalog.js"));
  const fixtureUrl = await startServer(fixtureExe);
  const fixtureCatalog = await readCatalog(fixtureUrl);
  assert.equal(fixtureCatalog.series.map((s) => s.id).join(","), real.series.map((s) => s.id).join(","));
  const apiRequests = [];
  page.on("request", (request) => { if (request.url().includes("/api/")) apiRequests.push(request.url()); });
  await page.goto(fixtureUrl);
  await expect(page.locator(".cute-series-card")).toHaveCount(2);
  await page.locator('[data-series-id="phosphor"]').click();
  await expect(page.locator(".cute-dir-card")).toHaveCount(6);
  await page.locator('[data-class-id="class1"]').click();
  await expect(page.locator(".cute-map-card")).toHaveCount(3);
  write("class1/map99/c1m99detail.jpg", Buffer.from([1, 2, 3]));
  await page.waitForTimeout(3500);
  await expect(page.locator(".cute-map-card")).toHaveCount(3);
  assert.deepEqual(apiRequests, [], "Offline catalogs must not request scan APIs");
  console.log("PASS: static offline catalog, no API calls or runtime folder discovery");
  await page.goto(pathToFileURL(path.join(root, "index.html")).href);
  await expect(page.locator(".cute-series-card")).toHaveCount(2);
  assert.deepEqual(errors, [], "No JavaScript runtime errors");
  const report = { passed: true, actual: real.series.map((s) => ({ label: s.label, categories: s.classes.length, maps: s.classes.reduce((n, c) => n + c.maps.length, 0), ready: s.classes.flatMap((c) => c.maps).filter((m) => m.detail).length })), screenshots: fs.readdirSync(output).filter((f) => f.endsWith(".png")) };
  fs.writeFileSync(path.join(output, "report.json"), JSON.stringify(report, null, 2), "utf8");
  console.log("PASS: file preview and zero JavaScript errors");
  console.log(JSON.stringify(report, null, 2));
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
}).finally(async () => {
  if (browser) await browser.close().catch(() => {});
  for (const child of children) await stop(child);
  if (fixture && path.basename(fixture).startsWith("phosphor-map-test-") && path.dirname(fixture) === os.tmpdir()) fs.rmSync(fixture, { recursive: true, force: true });
});
