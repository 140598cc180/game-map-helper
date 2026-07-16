# -*- coding: utf-8 -*-
from pathlib import Path
import re
import shutil
import datetime

ROOT = Path(__file__).resolve().parent
APP_JS = ROOT / "app.js"
STYLE_CSS = ROOT / "style.css"
INDEX_HTML = ROOT / "index.html"

NEW_RENDER_HOME = r'''function renderHome() {
  currentDir = null;
  els.title.textContent = "地图小助手";
  els.subtitle.textContent = "选择方向";
  els.back.classList.add("hidden");

  const dirMeta = {
    "北": { label: "北门", theme: "pink" },
    "右": { label: "右门", theme: "purple" },
    "左": { label: "左门", theme: "mint" },
    "南": { label: "南门", theme: "peach" }
  };

  const page = document.createElement("section");
  page.className = "cute-home cute-home-v5";

  const hero = document.createElement("section");
  hero.className = "cute-hero cute-hero-v5";
  hero.innerHTML =
    '<div class="cute-hero-sticker">🎀</div>' +
    '<div class="cute-kicker">Identity V Map Helper</div>' +
    '<h2>第五人格地图小助手</h2>' +
    '<p>选择对应方向，快速查看地图路线。</p>';

  const usage = document.createElement("section");
  usage.className = "cute-usage-card";
  usage.innerHTML =
    '<div class="cute-usage-icon">💡</div>' +
    '<div>' +
      '<div class="cute-usage-title">使用说明</div>' +
      '<div class="cute-usage-text">从出门右侧的门进入，依据门的位置和特征选择相应地图。</div>' +
    '</div>';

  const grid = document.createElement("div");
  grid.className = "cute-dir-grid cute-dir-grid-v5";

  for (const dir of DIRS) {
    const count = MAPS.filter(item => item.dir === dir.key).length;
    const meta = dirMeta[dir.key] || { label: dir.label, theme: "pink" };

    const btn = document.createElement("button");
    btn.className = "cute-dir-card cute-" + meta.theme;
    btn.innerHTML =
      '<span class="cute-dir-bubble cute-paw-icon">🐾</span>' +
      '<span class="cute-dir-name">' + dir.label + '</span>' +
      '<span class="cute-dir-label">' + meta.label + '</span>' +
      '<span class="cute-dir-count">' + count + ' 张地图</span>' +
      '<span class="cute-dir-arrow">进入 →</span>';

    btn.addEventListener("click", function () {
      renderCategory(dir.key, dir.label);
    });

    grid.appendChild(btn);
  }

  const author = document.createElement("section");
  author.className = "cute-author-card";
  author.innerHTML =
    '<div class="cute-avatar-wrap">' +
      '<img class="cute-avatar" src="./assets/avatar.png" alt="cici吃饱饱头像">' +
      '<div class="cute-avatar-fallback">🍚</div>' +
    '</div>' +
    '<div class="cute-author-main">' +
      '<div class="cute-author-heading">🌷 关于作者</div>' +
      '<div class="cute-author-name">cici吃饱饱</div>' +
      '<div class="cute-author-id">第五人格 ID：nku守门员</div>' +
      '<div class="cute-author-tags">' +
        '<span>🗺️ 原创地图整理</span>' +
        '<span>✏️ 原创路线标注</span>' +
        '<span>✨ AI 辅助增强</span>' +
      '</div>' +
      '<a class="cute-contact" href="mailto:jayceja817@gmail.com">📮 jayceja817@gmail.com</a>' +
    '</div>' +
    '<div class="cute-original-note">' +
      '<strong>原创说明</strong>' +
      '<p>本工具中的地图整理、路线规划、界面设计及标注内容均为原创制作，部分图片与视觉效果使用 AI 辅助增强。仅供个人自用与学习交流，不用于商业用途。自制整理不易，请勿未经允许搬运、转载或用于商业传播。</p>' +
    '</div>';

  const avatar = author.querySelector(".cute-avatar");
  const fallback = author.querySelector(".cute-avatar-fallback");

  avatar.addEventListener("load", function () {
    fallback.style.display = "none";
  });

  avatar.addEventListener("error", function () {
    avatar.style.display = "none";
    fallback.style.display = "grid";
  });

  page.append(hero, usage, grid, author);
  els.main.replaceChildren(page);
}'''

NEW_RENDER_CATEGORY = r'''function renderCategory(dirKey, label) {
  currentDir = dirKey;

  const dirMeta = {
    "北": { theme: "pink" },
    "右": { theme: "purple" },
    "左": { theme: "mint" },
    "南": { theme: "peach" }
  };

  const meta = dirMeta[dirKey] || { theme: "pink" };
  const list = MAPS.filter(item => item.dir === dirKey);

  els.title.textContent = "🐾 " + label;
  els.subtitle.textContent = "点击缩略图查看完整地图";
  els.back.classList.remove("hidden");

  const page = document.createElement("section");
  page.className = "cute-category";

  const head = document.createElement("section");
  head.className = "cute-category-head cute-" + meta.theme;
  head.innerHTML =
    '<div class="cute-category-icon">🐾</div>' +
    '<div class="cute-category-copy">' +
      '<div class="cute-category-title">' + label + '</div>' +
      '<div class="cute-category-sub">共 ' + list.length + ' 张地图 · 点击即可打开</div>' +
    '</div>';

  const grid = document.createElement("div");
  grid.className = "cute-map-grid";

  for (let i = 0; i < list.length; i++) {
    const item = list[i];

    const card = document.createElement("button");
    card.className = "cute-map-card";
    card.setAttribute("aria-label", "查看" + item.name);

    const thumb = document.createElement("div");
    thumb.className = "cute-thumb";

    const img = document.createElement("img");
    img.loading = "lazy";
    img.alt = item.name;
    img.src = thumbSrc(item);

    img.onerror = function () {
      thumb.innerHTML = '<div class="missing-img">图片未找到<br>' + item.thumb + '</div>';
    };

    thumb.appendChild(img);

    const info = document.createElement("div");
    info.className = "cute-map-info";
    info.innerHTML =
      '<span class="cute-map-no">' + String(i + 1).padStart(2, "0") + '</span>' +
      '<span class="cute-map-title">' + item.name + '</span>' +
      '<span class="cute-map-open">↗</span>';

    card.append(thumb, info);

    card.addEventListener("click", function () {
      openViewer(item);
    });

    grid.appendChild(card);
  }

  page.append(head, grid);
  els.main.replaceChildren(page);
}'''

EXTRA_CSS = r'''
/* ===== Cute UI v5 refinements ===== */

.topbar {
  position: relative !important;
}

#pageTitle,
#pageSubtitle {
  width: 100%;
  text-align: center !important;
}

.topbar > div,
.topbar .title-wrap,
.topbar .title-group,
.topbar .topbar-title {
  flex: 1 1 auto;
  text-align: center !important;
}

.cute-hero-v5 {
  text-align: center;
}

.cute-hero-v5 .cute-kicker {
  margin-left: auto;
  margin-right: auto;
}

.cute-hero-v5 h2 {
  max-width: 100% !important;
  text-align: center;
}

.cute-hero-v5 p {
  text-align: center;
}

.cute-paw-icon,
.cute-category-icon {
  font-family: "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", sans-serif;
}

.cute-paw-icon {
  font-size: 24px !important;
  transform: rotate(-8deg);
}

.cute-dir-card:nth-child(even) .cute-paw-icon {
  transform: rotate(8deg);
}

.cute-usage-card {
  display: grid;
  grid-template-columns: 44px minmax(0, 1fr);
  gap: 11px;
  align-items: center;
  padding: 11px 13px;
  border: 2px solid rgba(255, 189, 143, 0.34);
  border-radius: 20px;
  background:
    linear-gradient(135deg, rgba(255, 250, 246, 0.96), rgba(255, 234, 220, 0.86));
  box-shadow: 0 12px 27px rgba(117, 87, 95, 0.09);
}

.cute-usage-icon {
  display: grid;
  place-items: center;
  width: 44px;
  height: 44px;
  border-radius: 15px;
  background: rgba(255, 255, 255, 0.76);
  font-size: 23px;
  box-shadow: 0 7px 18px rgba(112, 81, 92, 0.08);
}

.cute-usage-title {
  color: #876776;
  font-size: 13px;
  font-weight: 1000;
}

.cute-usage-text {
  margin-top: 3px;
  color: #756a78;
  font-size: 12px;
  font-weight: 700;
  line-height: 1.5;
}

.cute-map-title {
  font-size: 12px !important;
  line-height: 1.2;
}

.cute-map-info {
  min-height: 38px;
  padding: 6px 7px 7px !important;
}

.cute-map-no {
  min-width: 25px !important;
  height: 21px !important;
  font-size: 10px !important;
}

.cute-map-open {
  font-size: 13px !important;
}

.cute-category-legend,
.cute-tips {
  display: none !important;
}

.cute-category-head {
  grid-template-columns: 48px minmax(0, 1fr) !important;
}

.cute-category-icon {
  font-size: 24px !important;
  transform: rotate(-7deg);
}

@media (max-width: 430px) {
  .cute-map-title {
    font-size: 11px !important;
  }

  .cute-map-info {
    min-height: 36px;
    padding: 5px 6px 6px !important;
  }

  .cute-dir-name {
    font-size: 29px !important;
  }

  .cute-usage-card {
    grid-template-columns: 39px minmax(0, 1fr);
    padding: 9px 10px;
  }

  .cute-usage-icon {
    width: 39px;
    height: 39px;
    font-size: 21px;
  }
}
'''

def replace_map_names(text):
    match = re.search(r"const\s+MAPS\s*=\s*\[(.*?)\];", text, flags=re.S)
    if not match:
        raise RuntimeError("没有找到 const MAPS = [...]。")

    block = match.group(1)
    counters = {"北": 0, "南": 0, "左": 0, "右": 0}
    object_pattern = re.compile(r"\{[^{}]*\}", flags=re.S)

    def patch_object(obj_match):
        obj = obj_match.group(0)
        dir_match = re.search(r'["\']dir["\']\s*:\s*["\']([北南左右])["\']', obj)
        if not dir_match:
            return obj

        direction = dir_match.group(1)
        counters[direction] += 1
        new_name = direction + "图" + str(counters[direction])

        if re.search(r'["\']name["\']\s*:', obj):
            obj = re.sub(
                r'(["\']name["\']\s*:\s*)["\'][^"\']*["\']',
                lambda m: m.group(1) + '"' + new_name + '"',
                obj,
                count=1
            )
        return obj

    new_block = object_pattern.sub(patch_object, block)
    new_text = text[:match.start(1)] + new_block + text[match.end(1):]
    return new_text, counters

def patch_app_js():
    if not APP_JS.exists():
        raise RuntimeError("没有找到 app.js，请确认脚本放在项目根目录。")

    text = APP_JS.read_text(encoding="utf-8")
    backup = ROOT / (
        "app.backup.before_cute_ui_v5_%s.js"
        % datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    )
    shutil.copy2(APP_JS, backup)

    text, counters = replace_map_names(text)

    text, home_count = re.subn(
        r"function renderHome\(\)\s*\{.*?\n\}\n\nfunction renderCategory",
        NEW_RENDER_HOME + "\n\nfunction renderCategory",
        text,
        count=1,
        flags=re.S
    )

    text, category_count = re.subn(
        r"function renderCategory\(dirKey,\s*label\)\s*\{.*?\n\}\n\nfunction openViewer",
        NEW_RENDER_CATEGORY + "\n\nfunction openViewer",
        text,
        count=1,
        flags=re.S
    )

    if home_count == 0:
        raise RuntimeError("没有定位到 renderHome 函数。")
    if category_count == 0:
        raise RuntimeError("没有定位到 renderCategory 函数。")

    APP_JS.write_text(text, encoding="utf-8")

    stat = "，".join(k + "图" + str(v) + "张" for k, v in counters.items())
    return "[OK] app.js 已更新；" + stat

def patch_css():
    if not STYLE_CSS.exists():
        raise RuntimeError("没有找到 style.css。")

    text = STYLE_CSS.read_text(encoding="utf-8")
    backup = ROOT / (
        "style.backup.before_cute_ui_v5_%s.css"
        % datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    )
    shutil.copy2(STYLE_CSS, backup)

    marker = "/* ===== Cute UI v5 refinements ===== */"
    if marker not in text:
        STYLE_CSS.write_text(
            text.rstrip() + "\n\n" + EXTRA_CSS + "\n",
            encoding="utf-8"
        )
        return "[OK] style.css 已追加 v5 细节样式"

    return "[SKIP] style.css 已存在 v5 样式"

def patch_html():
    if not INDEX_HTML.exists():
        return "[SKIP] 没有找到 index.html"

    text = INDEX_HTML.read_text(encoding="utf-8")
    backup = ROOT / (
        "index.backup.before_cute_ui_v5_%s.html"
        % datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    )
    shutil.copy2(INDEX_HTML, backup)

    text = text.replace(
        "<title>第五人格地图助手</title>",
        "<title>第五人格地图小助手</title>"
    )

    text = re.sub(
        r'<script\s+src="\./app\.js(?:\?[^"]*)?"></script>',
        '<script src="./app.js?v=cute-ui-v5"></script>',
        text
    )

    INDEX_HTML.write_text(text, encoding="utf-8")
    return "[OK] index.html 已更新缓存版本号"

def main():
    logs = [
        "Cute UI v5",
        "time: " + str(datetime.datetime.now()),
        "root: " + str(ROOT),
        "",
        patch_app_js(),
        patch_css(),
        patch_html(),
    ]

    output = "\n".join(logs)
    print(output)
    (ROOT / "cute_ui_v5_log.txt").write_text(output, encoding="utf-8")

    print("")
    print("本地预览：")
    print("python -m http.server 8009")
    print("http://localhost:8009/index.html?v=cute5")
    print("")
    print("确认后上传 GitHub：")
    print("git status")
    print("git add .")
    print('git commit -m "refine cute ui"')
    print("git push")

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("[ERROR]", exc)
        input("按回车退出...")
