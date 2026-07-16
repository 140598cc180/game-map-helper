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
  document.body.classList.add("cute-home-view");
  document.body.classList.remove("cute-category-view");

  els.title.textContent = "";
  els.subtitle.textContent = "";
  els.back.classList.add("hidden");

  const dirMeta = {
    "北": { label: "北门", theme: "pink" },
    "右": { label: "右门", theme: "purple" },
    "左": { label: "左门", theme: "mint" },
    "南": { label: "南门", theme: "peach" }
  };

  const page = document.createElement("section");
  page.className = "cute-home cute-home-v7";

  const hero = document.createElement("section");
  hero.className = "cute-hero cute-hero-v7";
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
  grid.className = "cute-dir-grid cute-dir-grid-v7";

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
  author.className = "cute-author-card cute-author-card-v7";
  author.innerHTML =
    '<div class="cute-author-top">' +
      '<div class="cute-avatar-wrap">' +
        '<img class="cute-avatar" src="./assets/avatar.png" alt="cici吃饱饱头像">' +
        '<div class="cute-avatar-fallback">🍚</div>' +
      '</div>' +
      '<div class="cute-author-main">' +
        '<div class="cute-author-heading">🌷 关于作者</div>' +
        '<div class="cute-author-name">cici吃饱饱</div>' +
        '<div class="cute-author-id">第五人格 ID：nku守门员</div>' +
      '</div>' +
    '</div>' +
    '<div class="cute-author-tags cute-author-tags-v7">' +
      '<span>🗺️ 原创地图整理</span>' +
      '<span>✏️ 原创路线标注</span>' +
      '<span>✨ AI 辅助增强</span>' +
    '</div>' +
    '<a class="cute-contact cute-contact-v7" href="mailto:jayceja817@gmail.com">📮 jayceja817@gmail.com</a>' +
    '<div class="cute-original-note cute-original-note-v7">' +
      '<strong>原创说明</strong>' +
      '<p>本工具中的地图整理、路线规划、界面设计及标注内容均为原创制作，部分图片与视觉效果使用 AI 辅助增强。仅供个人自用与学习交流，不用于商业用途。自制整理不易，请勿未经允许搬运、转载或用于商业传播。</p>' +
    '</div>';

  const avatar = author.querySelector(".cute-avatar");
  const fallback = author.querySelector(".cute-avatar-fallback");
  avatar.addEventListener("load", function () { fallback.style.display = "none"; });
  avatar.addEventListener("error", function () {
    avatar.style.display = "none";
    fallback.style.display = "grid";
  });

  page.append(hero, usage, grid, author);
  els.main.replaceChildren(page);
}'''

NEW_RENDER_CATEGORY = r'''function renderCategory(dirKey, label) {
  currentDir = dirKey;
  document.body.classList.remove("cute-home-view");
  document.body.classList.add("cute-category-view");

  const dirMeta = {
    "北": { theme: "pink" },
    "右": { theme: "purple" },
    "左": { theme: "mint" },
    "南": { theme: "peach" }
  };

  const meta = dirMeta[dirKey] || { theme: "pink" };
  const list = MAPS.filter(item => item.dir === dirKey);

  els.title.textContent = label;
  els.subtitle.textContent = "";
  els.back.classList.remove("hidden");

  const page = document.createElement("section");
  page.className = "cute-category cute-category-v7";

  const head = document.createElement("section");
  head.className = "cute-category-head cute-category-head-v7 cute-" + meta.theme;
  head.innerHTML = '<div class="cute-category-one-line">共 ' + list.length + ' 张地图 · 点击即可打开</div>';

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
    card.addEventListener("click", function () { openViewer(item); });
    grid.appendChild(card);
  }

  page.append(head, grid);
  els.main.replaceChildren(page);
}'''

EXTRA_CSS = r'''
/* ===== Cute UI v7 mobile repair ===== */
html { -webkit-text-size-adjust: 100%; text-size-adjust: 100%; }
body { overflow-x: hidden; }

body.cute-home-view .topbar { display: none !important; }
body.cute-home-view .app-shell { padding-top: calc(10px + env(safe-area-inset-top)) !important; }

body.cute-category-view .topbar {
  position: relative !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  min-height: 54px;
  padding: 6px 52px 8px !important;
  box-sizing: border-box;
}

body.cute-category-view .topbar .icon-btn:first-child,
body.cute-category-view #backBtn,
body.cute-category-view .back-btn {
  position: absolute !important;
  left: 8px !important;
  top: 50% !important;
  transform: translateY(-50%) !important;
}

body.cute-category-view #pageTitle {
  width: 100% !important;
  margin: 0 !important;
  color: #5b5268 !important;
  font-size: 23px !important;
  line-height: 1.1 !important;
  text-align: center !important;
  white-space: nowrap;
}

body.cute-category-view #pageSubtitle { display: none !important; }
body.cute-category-view .topbar > div,
body.cute-category-view .title-wrap,
body.cute-category-view .title-group,
body.cute-category-view .topbar-title {
  width: 100% !important;
  min-width: 0 !important;
  text-align: center !important;
}

.cute-category-head-v7 {
  display: block !important;
  padding: 10px 12px !important;
  border-radius: 18px !important;
  text-align: center !important;
}

.cute-category-one-line {
  color: #6f6478;
  font-size: 14px;
  font-weight: 900;
  line-height: 1.35;
  white-space: nowrap;
}

.cute-category-icon,
.cute-category-copy,
.cute-category-title,
.cute-category-sub,
.cute-category-legend { display: none !important; }

.cute-author-card-v7 {
  display: block !important;
  width: 100% !important;
  box-sizing: border-box !important;
  margin: 0 0 18px !important;
  padding: 13px !important;
  overflow: hidden !important;
  border: 2px solid rgba(184, 160, 255, 0.30) !important;
  border-radius: 22px !important;
  background: rgba(255, 255, 255, 0.90) !important;
  box-shadow: 0 14px 34px rgba(106, 82, 115, 0.11) !important;
}

.cute-author-top {
  display: grid !important;
  grid-template-columns: 66px minmax(0, 1fr) !important;
  gap: 11px !important;
  align-items: center !important;
}

.cute-author-card-v7 .cute-avatar-wrap,
.cute-author-card-v7 .cute-avatar,
.cute-author-card-v7 .cute-avatar-fallback {
  width: 66px !important;
  height: 66px !important;
  box-sizing: border-box !important;
}

.cute-author-card-v7 .cute-avatar,
.cute-author-card-v7 .cute-avatar-fallback { border-radius: 20px !important; }
.cute-author-card-v7 .cute-author-main { min-width: 0 !important; }
.cute-author-card-v7 .cute-author-heading { font-size: 11px !important; line-height: 1.3 !important; }
.cute-author-card-v7 .cute-author-name { margin-top: 2px !important; font-size: 19px !important; line-height: 1.15 !important; }
.cute-author-card-v7 .cute-author-id { margin-top: 4px !important; font-size: 11px !important; line-height: 1.4 !important; }

.cute-author-tags-v7 {
  display: flex !important;
  flex-wrap: wrap !important;
  gap: 5px !important;
  margin-top: 10px !important;
}

.cute-author-tags-v7 span {
  padding: 4px 7px !important;
  border-radius: 999px !important;
  background: #faf3ff !important;
  color: #7c6d88 !important;
  font-size: 9px !important;
  line-height: 1.2 !important;
  white-space: nowrap !important;
}

.cute-contact-v7 {
  display: block !important;
  width: 100% !important;
  box-sizing: border-box !important;
  margin-top: 9px !important;
  padding: 7px 9px !important;
  border: 1px solid rgba(255, 159, 199, 0.34) !important;
  border-radius: 11px !important;
  background: rgba(255, 241, 247, 0.90) !important;
  color: #8d5f7a !important;
  font-size: 11px !important;
  line-height: 1.35 !important;
  text-decoration: none !important;
  overflow-wrap: anywhere !important;
  word-break: break-all !important;
}

.cute-original-note-v7 {
  display: block !important;
  margin-top: 10px !important;
  padding: 10px !important;
  border: 1px solid rgba(184, 160, 255, 0.22) !important;
  border-radius: 13px !important;
  background: rgba(248, 243, 255, 0.82) !important;
}

.cute-original-note-v7 strong { display: block !important; color: #806b88 !important; font-size: 11px !important; line-height: 1.3 !important; }
.cute-original-note-v7 p {
  display: block !important;
  margin: 5px 0 0 !important;
  color: #7e7385 !important;
  font-size: 10px !important;
  line-height: 1.6 !important;
  text-align: left !important;
  overflow-wrap: anywhere !important;
}

.app-shell { padding-bottom: calc(96px + env(safe-area-inset-bottom)) !important; }

@media (max-width: 430px) {
  .cute-category-one-line { font-size: 13px !important; }
  .cute-author-card-v7 { padding: 11px !important; border-radius: 19px !important; }
  .cute-author-top { grid-template-columns: 58px minmax(0, 1fr) !important; gap: 9px !important; }
  .cute-author-card-v7 .cute-avatar-wrap,
  .cute-author-card-v7 .cute-avatar,
  .cute-author-card-v7 .cute-avatar-fallback { width: 58px !important; height: 58px !important; }
  .cute-author-card-v7 .cute-author-name { font-size: 17px !important; }
  .cute-author-tags-v7 { gap: 4px !important; }
  .cute-author-tags-v7 span { padding: 3px 6px !important; font-size: 8px !important; }
}
'''

def backup(path: Path, tag: str):
    if path.exists():
        dst = ROOT / f"{path.stem}.backup.before_{tag}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}{path.suffix}"
        shutil.copy2(path, dst)


def patch_app_js():
    if not APP_JS.exists():
        raise RuntimeError("没有找到 app.js")
    text = APP_JS.read_text(encoding="utf-8")
    backup(APP_JS, "cute_ui_v7")

    text, n1 = re.subn(
        r"function renderHome\(\)\s*\{.*?\n\}\n\nfunction renderCategory",
        NEW_RENDER_HOME + "\n\nfunction renderCategory",
        text,
        count=1,
        flags=re.S,
    )
    text, n2 = re.subn(
        r"function renderCategory\(dirKey,\s*label\)\s*\{.*?\n\}\n\nfunction openViewer",
        NEW_RENDER_CATEGORY + "\n\nfunction openViewer",
        text,
        count=1,
        flags=re.S,
    )
    if n1 == 0 or n2 == 0:
        raise RuntimeError("没有找到 renderHome 或 renderCategory")
    APP_JS.write_text(text, encoding="utf-8")


def patch_css():
    if not STYLE_CSS.exists():
        raise RuntimeError("没有找到 style.css")
    text = STYLE_CSS.read_text(encoding="utf-8")
    backup(STYLE_CSS, "cute_ui_v7")
    if "/* ===== Cute UI v7 mobile repair ===== */" not in text:
        STYLE_CSS.write_text(text.rstrip() + "\n\n" + EXTRA_CSS + "\n", encoding="utf-8")


def patch_html():
    if not INDEX_HTML.exists():
        return
    text = INDEX_HTML.read_text(encoding="utf-8")
    backup(INDEX_HTML, "cute_ui_v7")
    text = re.sub(
        r'<script\s+src="\./app\.js(?:\?[^\"]*)?"></script>',
        '<script src="./app.js?v=cute-ui-v7"></script>',
        text,
    )
    INDEX_HTML.write_text(text, encoding="utf-8")


def main():
    patch_app_js()
    patch_css()
    patch_html()
    print("[OK] v7 修复完成")
    print("预览：python -m http.server 8012")
    print("打开：http://localhost:8012/index.html?v=cute7")
    print("上传：git add .")
    print('      git commit -m "fix cute mobile layout"')
    print("      git push")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("[ERROR]", exc)
        input("按回车退出...")
