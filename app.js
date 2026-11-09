"use strict";

(() => {
  const themes = ["pink", "purple", "mint", "peach", "blue", "yellow"];
  const $ = (id) => document.getElementById(id);
  const el = {
    app: $("app"), main: $("main"), topbar: $("topbar"), title: $("pageTitle"),
    back: $("backBtn"), refresh: $("refreshBtn"), footerRefresh: $("footerRefresh"), status: $("syncStatus"),
    viewer: $("viewer"), viewerTitle: $("viewerTitle"), stage: $("viewerStage"), image: $("viewerImg"),
    message: $("viewerMessage"), close: $("viewerClose"), fit: $("viewerReset"),
    plus: $("zoomIn"), minus: $("zoomOut"), zoom: $("zoomLabel"),
  };
  const android = window.MAP_RUNTIME === "android";
  let catalog = window.MAP_CATALOG || { series: [] };
  let renderedPage = undefined;
  let activeMap = null;
  let returnFocus = null;
  let previousOverflow = "";
  const pointers = new Map();
  const view = { scale: 1, fit: 1, x: 0, y: 0, width: 0, height: 0 };

  function node(tag, className, text) {
    const n = document.createElement(tag);
    if (className) n.className = className;
    if (text !== undefined) n.textContent = text;
    return n;
  }

  // Some mobile WebViews suppress compatibility clicks after a pinch gesture.
  // Handle a deliberate touch tap directly; preserve mouse and keyboard clicks.
  function activate(button, action) {
    let start = null;
    let suppressClickUntil = 0;
    button.addEventListener("pointerdown", (event) => {
      if (event.pointerType === "touch" && event.isPrimary)
        start = { id: event.pointerId, x: event.clientX, y: event.clientY };
    });
    button.addEventListener("pointercancel", () => { start = null; });
    button.addEventListener("pointerup", (event) => {
      if (!start || event.pointerId !== start.id) return;
      const tap = Math.hypot(event.clientX - start.x, event.clientY - start.y) < 12;
      start = null;
      if (tap && !button.disabled) {
        suppressClickUntil = Date.now() + 800;
        event.preventDefault();
        action(event);
      }
    });
    button.addEventListener("touchend", (event) => {
      if (Date.now() < suppressClickUntil) event.preventDefault();
    }, { passive: false });
    button.addEventListener("click", (event) => {
      if (event.detail !== 0 && Date.now() < suppressClickUntil) { event.preventDefault(); return; }
      action(event);
    });
  }

  function picture(src, alt, className, fallbackText) {
    const wrap = node("div", className);
    const fallback = node("div", "missing-img", src && fallbackText ? "正在加载…" : fallbackText);
    wrap.append(fallback);
    if (src) {
      const image = node("img");
      image.alt = alt;
      image.loading = "lazy";
      image.decoding = "async";
      image.addEventListener("load", () => { fallback.hidden = true; });
      image.addEventListener("error", () => {
        image.remove();
        fallback.hidden = false;
        if (fallbackText) fallback.textContent = fallbackText;
        else if (fallback.querySelector("small")) fallback.querySelector("small").textContent = "类别图标读取失败";
      });
      image.src = src;
      wrap.append(image);
    }
    return wrap;
  }

  function route() {
    const match = /^#\/series\/([a-z0-9-]+)(?:\/(class[1-9]\d*))?(?:\/(map[1-9]\d*))?$/.exec(location.hash);
    return match ? { seriesId: match[1], classId: match[2] || null, mapId: match[3] || null } : { seriesId: null, classId: null, mapId: null };
  }

  function navigate(hash, replace = false) {
    history[replace ? "replaceState" : "pushState"](null, "", hash || location.pathname + location.search);
    renderRoute();
  }

  function seriesName(series) {
    return series.id === "nightmare-woman" ? "噩梦之女困难" : "磷光症噩梦";
  }

  function renderHome() {
    el.topbar.classList.add("hidden");
    el.back.classList.add("hidden");
    document.body.classList.add("cute-home-view");
    document.body.classList.remove("cute-category-view");
    document.title = "第五人格地图小助手";
    const page = node("section", "cute-home cute-home-v7");
    const hero = node("section", "cute-hero cute-hero-v7");
    hero.innerHTML = '<div class="cute-hero-sticker">🎀</div><div class="cute-kicker">Identity V Map Helper</div><h2>第五人格地图小助手</h2><p>选择对应方向，快速查看地图路线。</p>';
    const usage = node("section", "cute-usage-card");
    usage.innerHTML = '<div class="cute-usage-icon">💡</div><div><div class="cute-usage-title">使用说明</div><div class="cute-usage-text">噩梦之女困难：侧门地图。<br>磷光症噩梦：右门地图。噩梦难度下，到 -1 层直接左转，打开地图查看右下角的形状，选择对应类别；然后逆时针走，观察特征，选择对应地图。</div></div>';
    const grid = node("div", "cute-dir-grid cute-dir-grid-v7 cute-series-grid");
    for (const series of catalog.series) {
      const categories = series.classes || [];
      const maps = categories.flatMap((c) => c.maps || []);
      const name = seriesName(series);
      const card = node("button", "cute-dir-card cute-series-card cute-" + (series.id === "nightmare-woman" ? "pink" : "purple"));
      card.dataset.seriesId = series.id;
      card.setAttribute("aria-label", name + "，" + categories.length + " 类，" + maps.length + " 张地图");
      const role = series.id === "nightmare-woman" ? "侧门地图" : "右门地图";
      const cover = node("span", "series-cover");
      const icon = node("img");
      icon.src = "./icos/" + (series.id === "nightmare-woman" ? "s0.png" : "s1.png");
      icon.alt = name;
      icon.loading = "eager";
      cover.append(icon);
      const caption = node("span", "series-caption");
      caption.append(
        node("span", "series-title", name),
        node("span", "series-explain", role + " · " + series.difficulty),
        node("span", "series-meta", series.lastUpdated + " 更新 · " + categories.length + " 类 · " + maps.length + " 张地图"),
        node("span", "series-enter", "进入 →")
      );
      card.append(cover, caption);
      activate(card, () => navigate("#/series/" + series.id));
      grid.append(card);
    }
    const author = node("section", "cute-author-card cute-author-card-v7");
    author.innerHTML =
      '<div class="cute-author-top">' +
        '<div class="cute-avatar-wrap">' +
          '<img class="cute-avatar" src="./assets/avatar.png" alt="cici吃饱饱头像">' +
          '<div class="cute-avatar-fallback">🍚</div>' +
        '</div>' +
        '<div class="cute-author-main">' +
          '<div class="cute-author-heading">🌷 关于作者</div>' +
          '<div class="cute-author-name">cici吃饱饱</div>' +
          '<div class="cute-author-id">' +
            '<span>第五人格 ID：nku守门员</span>' +
            '<span class="cute-play-note">🎮 欢迎找我陪玩</span>' +
          '</div>' +
        '</div>' +
      '</div>' +
      '<div class="cute-author-tags cute-author-tags-v7">' +
        '<span>🗺️ 网络地图搜集</span>' +
        '<span>✏️ 原创路线标注</span>' +
        '<span>✨ AI 辅助增强</span>' +
      '</div>' +
      '<a class="cute-contact cute-contact-v7" href="mailto:jayceja817@gmail.com">' +
        '<span class="cute-email-text">📮 jayceja817@gmail.com</span>' +
        '<span class="cute-qq-text">🐧 QQ：1405985556</span>' +
        '<span class="cute-wechat-text">💬 微信：LittleLion_cc817</span>' +
      '</a>' +
      '<div class="cute-original-note cute-original-note-v7">' +
        '<strong>原创说明</strong>' +
        '<p>地图来自网络搜集，地图本身非原创，地图标注为原创。部分图片与视觉效果使用 AI 辅助增强。工具仅供个人自用与学习交流，不用于商业用途。目前制作还比较粗糙，有改进建议欢迎联系，我会根据建议修改完善，后续不断更新迭代。</p>' +
      '</div>';
    const avatar = author.querySelector(".cute-avatar");
    const fallback = author.querySelector(".cute-avatar-fallback");
    avatar.addEventListener("load", () => { fallback.style.display = "none"; });
    avatar.addEventListener("error", () => { avatar.style.display = "none"; fallback.style.display = "grid"; });
    page.append(hero, usage, grid, author);
    el.main.replaceChildren(page);
  }

  function renderSeries(series) {
    document.body.classList.remove("cute-home-view");
    document.body.classList.add("cute-category-view");
    el.topbar.classList.remove("hidden");
    el.back.classList.remove("hidden");
    el.title.textContent = series.label;
    el.back.title = "返回系列选择";
    el.back.setAttribute("aria-label", "返回系列选择");
    document.title = series.label + " · 地图小助手";
    const page = node("section", "cute-category cute-category-v7");
    const maps = (series.classes || []).flatMap((c) => c.maps || []);
    const head = node("section", "cute-category-head cute-category-head-v7 cute-" + series.theme);
    head.append(node("div", "cute-category-one-line", "共 " + series.classes.length + " 类、" + maps.length + " 张地图 · 选择类别"));
    const grid = node("div", "cute-dir-grid cute-dir-grid-v7");
    for (const c of series.classes) {
      const ready = c.maps.filter((m) => m.detail).length;
      const card = node("button", "cute-dir-card cute-" + themes[(c.number - 1) % themes.length]);
      card.dataset.classId = c.id;
      card.setAttribute("aria-label", c.label + "，" + c.maps.length + " 张地图，" + ready + " 张可查看");
      const emblem = node("span", "cute-dir-bubble cute-paw-icon");
      if (c.thumbnail) {
        const icon = node("img");
        icon.src = c.thumbnail;
        icon.alt = c.label;
        icon.width = icon.height = 56;
        icon.style.cssText = "display:block;width:56px;height:56px;object-fit:contain";
        emblem.append(icon);
      } else {
        emblem.textContent = "🐾";
      }
      card.append(emblem, node("span", "cute-dir-name", c.label), node("span", "cute-dir-label", seriesName(series)), node("span", "cute-dir-count", c.maps.length + " 张地图"), node("span", "cute-dir-arrow", "进入 →"));
      activate(card, () => navigate("#/series/" + series.id + "/" + c.id));
      grid.append(card);
    }
    page.append(head, grid);
    el.main.replaceChildren(page);
  }

  function renderCategory(series, c) {
    document.body.classList.remove("cute-home-view");
    document.body.classList.add("cute-category-view");
    el.topbar.classList.remove("hidden");
    el.back.classList.remove("hidden");
    el.title.textContent = c.label;
    el.back.title = "返回" + series.label + "类别";
    el.back.setAttribute("aria-label", "返回" + series.label + "类别");
    document.title = c.label + " · " + series.label + "地图小助手";
    const page = node("section", "cute-category cute-category-v7");
    const ready = c.maps.filter((m) => m.detail).length;
    const head = node("section", "cute-category-head cute-category-head-v7 cute-" + themes[(c.number - 1) % themes.length]);
    head.append(node("div", "cute-category-one-line", "共 " + c.maps.length + " 张地图 · " + ready + " 张可查看 · 点击即可打开"));
    const grid = node("div", "cute-map-grid");
    for (const m of c.maps) {
      const card = node("button", "cute-map-card");
      card.dataset.mapId = m.id;
      card.disabled = !m.detail;
      card.setAttribute("aria-label", m.label + (m.detail ? "，查看详细地图" : "，详细地图待添加"));
      const thumb = picture(m.thumbnail || m.detail, m.label, "cute-thumb", m.thumbnail ? "缩略图读取失败" : "地图图片待添加");
      if (!m.detail || !m.thumbnail) thumb.append(node("span", "thumb-badge", !m.detail ? "详图待添加" : "使用详图预览"));
      const info = node("div", "cute-map-info");
      info.append(node("span", "cute-map-no", String(m.number).padStart(2, "0")), node("span", "cute-map-title", m.label), node("span", "cute-map-open", m.detail ? "↗" : "待补"));
      card.append(thumb, info);
      activate(card, () => navigate("#/series/" + series.id + "/" + c.id + "/" + m.id));
      grid.append(card);
    }
    if (!c.maps.length) grid.append(node("div", "empty-state", "这个类别还没有地图。\n添加地图后重新生成离线版本即可查看。"));
    page.append(head, grid);
    el.main.replaceChildren(page);
  }

  function renderRoute(force = false) {
    const r = route();
    const series = catalog.series.find((item) => item.id === r.seriesId);
    const c = series && series.classes.find((item) => item.id === r.classId);
    const key = c ? "category/" + series.id + "/" + c.id : series ? "series/" + series.id : "home";
    if (force || key !== renderedPage) {
      if (c) renderCategory(series, c);
      else if (series) renderSeries(series);
      else renderHome();
      if (key !== renderedPage) window.scrollTo(0, 0);
      renderedPage = key;
    }
    const m = c && c.maps.find((item) => item.id === r.mapId);
    if (m) openViewer(series, c, m); else hideViewer();
  }

  function syncStatus(message) {
    if (message) { el.status.textContent = message; return; }
    const maps = catalog.series.flatMap((s) => s.classes.flatMap((c) => c.maps));
    const ready = maps.filter((m) => m.detail).length;
    el.status.textContent = ready + " / " + maps.length + " 张可查看 · 地图已随软件离线内置";
  }

  function refresh() { location.reload(); }

  function showMessage(text, retry = false) {
    el.image.classList.add("hidden");
    el.message.classList.remove("hidden");
    el.message.replaceChildren(node("span", "", text));
    if (retry) {
      const button = node("button", "viewer-btn", "重新加载");
      activate(button, () => { const map = activeMap; activeMap = null; if (map) openViewer(map.series, map.category, map.item); });
      el.message.append(button);
    }
    el.plus.disabled = el.minus.disabled = el.fit.disabled = true;
  }

  function openViewer(series, category, item) {
    const key = series.id + "/" + category.id + "/" + item.id + "/" + (item.detail || "pending");
    if (activeMap && activeMap.key === key) return;
    const opening = el.viewer.classList.contains("hidden");
    if (opening) {
      returnFocus = el.main.querySelector('[data-map-id="' + item.id + '"]') || document.activeElement;
      previousOverflow = document.body.style.overflow;
    }
    activeMap = { key, series, category, item };
    pointers.clear();
    el.stage.classList.remove("dragging");
    el.viewerTitle.textContent = series.label + " · " + category.label + " · " + item.label;
    el.viewer.classList.remove("hidden");
    el.app.inert = true;
    document.body.style.overflow = "hidden";
    showMessage(item.detail ? "正在加载详细地图…" : "这张地图的详细图片还没有添加。\n补图并重新生成离线版本后即可查看。");
    el.zoom.textContent = "100%";
    if (opening) el.close.focus();
    el.image.onload = null;
    el.image.onerror = null;
    if (!item.detail) { el.image.removeAttribute("src"); return; }
    el.image.onload = () => {
      if (!activeMap || activeMap.key !== key) return;
      view.width = el.image.naturalWidth;
      view.height = el.image.naturalHeight;
      el.image.style.width = view.width + "px";
      el.image.style.height = view.height + "px";
      el.image.classList.remove("hidden");
      el.message.classList.add("hidden");
      el.plus.disabled = el.minus.disabled = el.fit.disabled = false;
      fitImage();
    };
    el.image.onerror = () => {
      if (activeMap && activeMap.key === key) showMessage("详细图片暂时无法读取。\n如果正在复制图片，请稍后重试。", true);
    };
    el.image.src = item.detail;
  }

  function hideViewer() {
    if (el.viewer.classList.contains("hidden")) return;
    el.viewer.classList.add("hidden");
    el.app.inert = false;
    document.body.style.overflow = previousOverflow;
    el.image.onload = el.image.onerror = null;
    el.image.removeAttribute("src");
    activeMap = null;
    pointers.clear();
    el.stage.classList.remove("dragging");
    if (returnFocus && !returnFocus.isConnected && returnFocus.dataset.mapId) returnFocus = el.main.querySelector('[data-map-id="' + returnFocus.dataset.mapId + '"]');
    if (returnFocus && returnFocus.isConnected) returnFocus.focus({ preventScroll: true });
  }

  function closeViewer() {
    const r = route();
    navigate(r.seriesId && r.classId ? "#/series/" + r.seriesId + "/" + r.classId : "", true);
  }

  function backOneLevel() {
    const r = route();
    if (r.seriesId && r.classId) navigate("#/series/" + r.seriesId);
    else if (r.seriesId) navigate("");
  }

  function draw() {
    const xLimit = Math.max(0, (view.width * view.scale - el.stage.clientWidth) / 2);
    const yLimit = Math.max(0, (view.height * view.scale - el.stage.clientHeight) / 2);
    view.x = Math.max(-xLimit, Math.min(xLimit, view.x));
    view.y = Math.max(-yLimit, Math.min(yLimit, view.y));
    el.image.style.transform = "translate(-50%, -50%) translate(" + view.x + "px, " + view.y + "px) scale(" + view.scale + ")";
    el.zoom.textContent = Math.round(view.scale / view.fit * 100) + "%";
  }

  function fitImage() {
    if (!activeMap || el.image.classList.contains("hidden") || !view.width) return;
    view.fit = Math.min((el.stage.clientWidth - 24) / view.width, (el.stage.clientHeight - 24) / view.height, 1);
    view.fit = Math.max(.001, view.fit);
    view.scale = view.fit;
    view.x = view.y = 0;
    draw();
  }

  function zoomBy(factor, point) {
    if (!activeMap || el.image.classList.contains("hidden")) return;
    const next = Math.max(view.fit, Math.min(view.fit * 12, view.scale * factor));
    const ratio = next / view.scale;
    const bounds = el.stage.getBoundingClientRect();
    const x = point ? point.x - bounds.left - bounds.width / 2 : 0;
    const y = point ? point.y - bounds.top - bounds.height / 2 : 0;
    view.x = x - (x - view.x) * ratio;
    view.y = y - (y - view.y) * ratio;
    view.scale = next;
    draw();
  }

  el.stage.addEventListener("wheel", (event) => {
    event.preventDefault();
    zoomBy(Math.exp(-Math.max(-100, Math.min(100, event.deltaY)) * .003), { x: event.clientX, y: event.clientY });
  }, { passive: false });
  el.stage.addEventListener("dblclick", (event) => {
    if (view.scale > view.fit * 1.1) fitImage();
    else zoomBy(2.5, { x: event.clientX, y: event.clientY });
  });
  el.stage.addEventListener("pointerdown", (event) => {
    if (event.pointerType === "mouse" && event.button !== 0) return;
    if (el.image.classList.contains("hidden")) return;
    pointers.set(event.pointerId, { x: event.clientX, y: event.clientY });
    el.stage.setPointerCapture(event.pointerId);
    el.stage.classList.add("dragging");
  });
  el.stage.addEventListener("pointermove", (event) => {
    const before = pointers.get(event.pointerId);
    if (!before) return;
    const previous = [...pointers.values()];
    pointers.set(event.pointerId, { x: event.clientX, y: event.clientY });
    const current = [...pointers.values()];
    if (current.length === 1) {
      view.x += event.clientX - before.x;
      view.y += event.clientY - before.y;
      draw();
    } else if (current.length === 2) {
      const oldDistance = Math.hypot(previous[0].x - previous[1].x, previous[0].y - previous[1].y);
      const distance = Math.hypot(current[0].x - current[1].x, current[0].y - current[1].y);
      const midpoint = { x: (current[0].x + current[1].x) / 2, y: (current[0].y + current[1].y) / 2 };
      view.x += midpoint.x - (previous[0].x + previous[1].x) / 2;
      view.y += midpoint.y - (previous[0].y + previous[1].y) / 2;
      if (oldDistance > 0) zoomBy(distance / oldDistance, midpoint);
    }
  });
  function endPointer(event) {
    pointers.delete(event.pointerId);
    if (!pointers.size) el.stage.classList.remove("dragging");
  }
  ["pointerup", "pointercancel", "lostpointercapture"].forEach((name) => el.stage.addEventListener(name, endPointer));
  activate(el.plus, () => zoomBy(1.4));
  activate(el.minus, () => zoomBy(1 / 1.4));
  activate(el.fit, fitImage);
  activate(el.close, closeViewer);
  activate(el.back, backOneLevel);
  activate(el.refresh, () => refresh(true));
  activate(el.footerRefresh, () => refresh(true));
  window.addEventListener("popstate", () => renderRoute());
  window.addEventListener("hashchange", () => renderRoute());
  window.addEventListener("resize", fitImage);
  document.addEventListener("keydown", (event) => {
    const viewerOpen = !el.viewer.classList.contains("hidden");
    if (viewerOpen) {
      if (event.key === "Escape") { event.preventDefault(); closeViewer(); }
      if (event.key === "+" || event.key === "=") { event.preventDefault(); zoomBy(1.4); }
      if (event.key === "-") { event.preventDefault(); zoomBy(1 / 1.4); }
      if (event.key === "0") { event.preventDefault(); fitImage(); }
      if (event.key === "Tab") {
        const buttons = [...el.viewer.querySelectorAll("button:not(:disabled)")];
        const first = buttons[0], last = buttons[buttons.length - 1];
        if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
        else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
      }
    } else if ((event.key === "Backspace" || event.key === "Escape") && route().seriesId) {
      event.preventDefault(); backOneLevel();
    }
  });
  if (android) {
    el.footerRefresh.textContent = "重新加载";
    el.refresh.setAttribute("aria-label", "重新加载地图");
    el.refresh.title = "重新加载地图";
    window.MapHelperAndroid = Object.freeze({
      back() {
        if (!el.viewer.classList.contains("hidden")) { closeViewer(); return true; }
        if (route().classId) { navigate("#/series/" + route().seriesId, true); return true; }
        if (route().seriesId) { navigate("", true); return true; }
        return false;
      },
    });
  }
  renderRoute();
  syncStatus();
})();
