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
  els.title.textContent = "第五人格地图助手";
  els.subtitle.textContent = "固定地图路线速查 · 自用整理版";
  els.back.classList.add("hidden");

  const dirMeta = {
    "北": { emoji: "🧭", desc: "北门地图", color: "cyan" },
    "右": { emoji: "➡️", desc: "右门地图", color: "violet" },
    "左": { emoji: "⬅️", desc: "左门地图", color: "emerald" },
    "南": { emoji: "🔻", desc: "南门地图", color: "amber" },
  };

  const hero = document.createElement("section");
  hero.className = "hero-card";
  hero.innerHTML =
    '<div class="hero-kicker">🎮 Identity V Route Helper</div>' +
    '<div class="hero-title-row">' +
      '<div>' +
        '<h2>第五人格地图路线速查</h2>' +
        '<p>按门的方向选择地图，快速查看推荐路线、入口与检查顺序。</p>' +
      '</div>' +
      '<div class="hero-badge">自用版</div>' +
    '</div>' +
    '<div class="hero-tags">' +
      '<span>🟢 绿色三角 = 入口</span>' +
      '<span>🔴 红线 = 主路线</span>' +
      '<span>🔵 数字 = 检查顺序</span>' +
    '</div>';

  const grid = document.createElement("div");
  grid.className = "home-grid home-grid-polished";

  for (const dir of DIRS) {
    const count = MAPS.filter(item => item.dir === dir.key).length;
    const meta = dirMeta[dir.key] || { emoji: "📍", desc: "地图路线", color: "cyan" };
    const btn = document.createElement("button");
    btn.className = "direction-card direction-card-v2 dir-" + meta.color;
    btn.innerHTML =
      '<span class="direction-emoji">' + meta.emoji + '</span>' +
      '<span class="direction-title">' + dir.label + '</span>' +
      '<span class="direction-desc">' + meta.desc + '</span>' +
      '<span class="direction-count">共 ' + count + ' 张路线图</span>' +
      '<span class="direction-go">点击进入 →</span>';
    btn.addEventListener("click", function () {
      renderCategory(dir.key, dir.label);
    });
    grid.appendChild(btn);
  }

  const info = document.createElement("section");
  info.className = "home-info-card home-info-card-v2";
  info.innerHTML =
    '<div class="section-title">✨ 主要信息</div>' +
    '<div class="home-meta-grid home-meta-grid-v2">' +
      '<div><span>作者</span><strong>🍚 cici吃饱饱</strong></div>' +
      '<div><span>第五人格 ID</span><strong>🧤 nku守门员</strong></div>' +
      '<div><span>问题联系</span><strong>📮 jayceja817@gmail.com</strong></div>' +
    '</div>' +
    '<div class="home-notice home-notice-v2">' +
      '<strong>📌 声明：</strong>本工具仅供个人自用与学习交流，不用于任何商业用途。地图资料借鉴了 B 站 UP 主“凉哈皮”的相关图片内容，并在此基础上进行个人整理与路线标注。自制整理不易，请勿肆意传播或用于商业转载；如有不妥，请通过上方邮箱联系处理。' +
    '</div>';

  els.main.replaceChildren(hero, grid, info);
}'''

NEW_RENDER_CATEGORY = r'''function renderCategory(dirKey, label) {
  currentDir = dirKey;
  const dirMeta = {
    "北": { emoji: "🧭", tip: "北门路线", color: "cyan" },
    "右": { emoji: "➡️", tip: "右门路线", color: "violet" },
    "左": { emoji: "⬅️", tip: "左门路线", color: "emerald" },
    "南": { emoji: "🔻", tip: "南门路线", color: "amber" },
  };
  const meta = dirMeta[dirKey] || { emoji: "📍", tip: "地图路线", color: "cyan" };

  els.title.textContent = meta.emoji + " " + label;
  els.subtitle.textContent = "点击缩略图查看完整详细图";
  els.back.classList.remove("hidden");

  const list = MAPS.filter(item => item.dir === dirKey);

  const summary = document.createElement("section");
  summary.className = "category-summary category-" + meta.color;
  summary.innerHTML =
    '<div class="category-main">' +
      '<div class="category-icon">' + meta.emoji + '</div>' +
      '<div>' +
        '<div class="category-title">' + label + '</div>' +
        '<div class="category-subtitle">' + meta.tip + ' · 共 ' + list.length + ' 张地图</div>' +
      '</div>' +
    '</div>' +
    '<div class="category-hint">🟢 找入口 → 🔴 跟红线 → 🔵 按数字查点</div>';

  const grid = document.createElement("div");
  grid.className = "map-grid map-grid-v2";

  for (let index = 0; index < list.length; index++) {
    const item = list[index];
    const card = document.createElement("button");
    card.className = "map-card map-card-v2";
    card.setAttribute("aria-label", "查看" + item.name);

    const wrap = document.createElement("div");
    wrap.className = "thumb-wrap thumb-wrap-v2";

    const img = document.createElement("img");
    img.loading = "lazy";
    img.alt = item.name;
    img.src = thumbSrc(item);

    img.onerror = function () {
      wrap.innerHTML = '<div class="missing-img">缩略图未找到<br>' + item.thumb + '</div>';
    };

    wrap.appendChild(img);

    const name = document.createElement("div");
    name.className = "map-name map-name-v2";
    name.innerHTML =
      '<span class="map-index">' + String(index + 1).padStart(2, "0") + '</span>' +
      '<span class="map-title-text">' + item.name + '</span>';

    const foot = document.createElement("div");
    foot.className = "map-foot";
    foot.innerHTML = '<span>🗺️ 查看路线</span><span>打开 →</span>';

    card.append(wrap, name, foot);
    card.addEventListener("click", function () {
      openViewer(item);
    });
    grid.appendChild(card);
  }

  els.main.replaceChildren(summary, grid);
}'''

EXTRA_CSS = r'''
/* ===== UI beautify v2 ===== */
:root {
  --cyan: #38bdf8;
  --violet: #a78bfa;
  --emerald: #34d399;
  --amber: #fbbf24;
}

body::before {
  content: "";
  position: fixed;
  inset: 0;
  pointer-events: none;
  background:
    linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
  background-size: 28px 28px;
  mask-image: radial-gradient(circle at top, rgba(0,0,0,0.55), transparent 72%);
}

.topbar {
  border-bottom: 1px solid rgba(148, 163, 184, 0.12);
}

#pageTitle {
  text-shadow: 0 8px 28px rgba(56, 189, 248, 0.18);
}

.hero-card {
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(148, 163, 184, 0.24);
  border-radius: 28px;
  padding: 24px;
  margin-top: 8px;
  background:
    radial-gradient(circle at top right, rgba(56,189,248,0.20), transparent 28rem),
    radial-gradient(circle at bottom left, rgba(167,139,250,0.16), transparent 24rem),
    linear-gradient(135deg, rgba(15,23,42,0.96), rgba(30,41,59,0.82));
  box-shadow: 0 24px 70px rgba(0,0,0,0.34);
}

.hero-card::after {
  content: "🗺️";
  position: absolute;
  right: 24px;
  bottom: -18px;
  font-size: 116px;
  opacity: 0.08;
  transform: rotate(-10deg);
}

.hero-kicker {
  display: inline-flex;
  align-items: center;
  padding: 6px 12px;
  border-radius: 999px;
  background: rgba(56,189,248,0.12);
  border: 1px solid rgba(56,189,248,0.30);
  color: #bae6fd;
  font-size: 13px;
  font-weight: 800;
  letter-spacing: 0.04em;
}

.hero-title-row {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 18px;
  align-items: center;
  margin-top: 14px;
}

.hero-title-row h2 {
  margin: 0;
  font-size: clamp(28px, 6vw, 46px);
  line-height: 1.05;
  letter-spacing: -0.05em;
}

.hero-title-row p {
  margin-top: 10px;
  max-width: 720px;
  color: #cbd5e1;
  line-height: 1.7;
  font-size: 15px;
}

.hero-badge {
  display: grid;
  place-items: center;
  width: 84px;
  height: 84px;
  border-radius: 26px;
  color: #07111f;
  background: linear-gradient(135deg, #67e8f9, #c4b5fd);
  font-weight: 1000;
  box-shadow: 0 14px 34px rgba(56,189,248,0.24);
  transform: rotate(3deg);
}

.hero-tags {
  position: relative;
  z-index: 1;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 18px;
}

.hero-tags span {
  border: 1px solid rgba(148, 163, 184, 0.22);
  border-radius: 999px;
  padding: 8px 12px;
  color: #e5e7eb;
  background: rgba(15,23,42,0.56);
  font-size: 13px;
  font-weight: 700;
}

.home-grid-polished {
  margin-top: 18px;
}

.direction-card-v2 {
  min-height: 190px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 22px;
}

.direction-card-v2::after {
  opacity: 0.8;
}

.direction-emoji {
  width: 52px;
  height: 52px;
  display: grid;
  place-items: center;
  border-radius: 18px;
  background: rgba(255,255,255,0.12);
  border: 1px solid rgba(255,255,255,0.14);
  font-size: 28px;
  margin-bottom: 8px;
}

.direction-desc {
  position: relative;
  z-index: 1;
  color: #cbd5e1;
  font-weight: 700;
  font-size: 14px;
}

.direction-go {
  position: relative;
  z-index: 1;
  margin-top: auto;
  width: fit-content;
  border-radius: 999px;
  padding: 7px 11px;
  color: #07111f;
  background: rgba(226,232,240,0.92);
  font-size: 13px;
  font-weight: 900;
}

.dir-cyan { box-shadow: 0 18px 44px rgba(56,189,248,0.12); }
.dir-violet { box-shadow: 0 18px 44px rgba(167,139,250,0.12); }
.dir-emerald { box-shadow: 0 18px 44px rgba(52,211,153,0.12); }
.dir-amber { box-shadow: 0 18px 44px rgba(251,191,36,0.12); }

.dir-cyan .direction-emoji { background: rgba(56,189,248,0.18); }
.dir-violet .direction-emoji { background: rgba(167,139,250,0.18); }
.dir-emerald .direction-emoji { background: rgba(52,211,153,0.18); }
.dir-amber .direction-emoji { background: rgba(251,191,36,0.18); }

.home-info-card-v2 {
  margin-bottom: 24px;
}

.section-title {
  display: inline-flex;
  align-items: center;
  min-height: 34px;
  padding: 6px 14px;
  border-radius: 999px;
  background: rgba(251,191,36,0.12);
  border: 1px solid rgba(251,191,36,0.26);
  color: #fde68a;
  font-weight: 1000;
}

.home-meta-grid-v2 > div {
  transition: transform 0.16s ease, border-color 0.16s ease;
}

.home-meta-grid-v2 > div:hover {
  transform: translateY(-2px);
  border-color: rgba(125,211,252,0.38);
}

.home-notice-v2 strong {
  color: #ffffff;
}

.category-summary {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 14px;
  align-items: center;
  margin: 4px 0 16px;
  padding: 18px;
  border: 1px solid rgba(148,163,184,0.24);
  border-radius: 24px;
  background: linear-gradient(135deg, rgba(15,23,42,0.88), rgba(30,41,59,0.72));
  box-shadow: 0 18px 48px rgba(0,0,0,0.24);
}

.category-main {
  display: flex;
  align-items: center;
  gap: 14px;
  min-width: 0;
}

.category-icon {
  flex: 0 0 auto;
  width: 58px;
  height: 58px;
  display: grid;
  place-items: center;
  border-radius: 20px;
  background: rgba(255,255,255,0.10);
  border: 1px solid rgba(255,255,255,0.14);
  font-size: 30px;
}

.category-title {
  font-size: 26px;
  font-weight: 1000;
  letter-spacing: -0.04em;
}

.category-subtitle {
  margin-top: 4px;
  color: #cbd5e1;
  font-size: 14px;
}

.category-hint {
  justify-self: end;
  border-radius: 999px;
  padding: 9px 13px;
  background: rgba(15,23,42,0.62);
  border: 1px solid rgba(148,163,184,0.22);
  color: #e5e7eb;
  font-size: 13px;
  font-weight: 800;
  white-space: nowrap;
}

.category-cyan .category-icon { background: rgba(56,189,248,0.16); }
.category-violet .category-icon { background: rgba(167,139,250,0.16); }
.category-emerald .category-icon { background: rgba(52,211,153,0.16); }
.category-amber .category-icon { background: rgba(251,191,36,0.16); }

.map-grid-v2 {
  grid-template-columns: repeat(auto-fill, minmax(188px, 1fr));
}

.map-card-v2 {
  border-radius: 22px;
  background:
    linear-gradient(135deg, rgba(255,255,255,0.10), rgba(255,255,255,0.04)),
    rgba(15,23,42,0.70);
  transition: transform 0.16s ease, border-color 0.16s ease, box-shadow 0.16s ease;
}

.map-card-v2:hover {
  transform: translateY(-3px);
  border-color: rgba(125,211,252,0.45);
  box-shadow: 0 18px 46px rgba(0,0,0,0.28);
}

.map-card-v2:active {
  transform: scale(0.98);
}

.thumb-wrap-v2 {
  border-bottom: 1px solid rgba(148,163,184,0.16);
}

.map-name-v2 {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 11px 12px 5px;
}

.map-index {
  flex: 0 0 auto;
  min-width: 34px;
  height: 26px;
  display: inline-grid;
  place-items: center;
  border-radius: 999px;
  background: rgba(56,189,248,0.16);
  border: 1px solid rgba(56,189,248,0.28);
  color: #bae6fd;
  font-size: 12px;
  font-weight: 1000;
}

.map-title-text {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
}

.map-foot {
  display: flex;
  justify-content: space-between;
  gap: 8px;
  padding: 0 12px 12px;
  color: #94a3b8;
  font-size: 12px;
  font-weight: 800;
}

.viewer-toolbar {
  background: rgba(15,23,42,0.92);
  backdrop-filter: blur(14px);
}

.viewer-title {
  color: #ffffff;
}

@media (max-width: 760px) {
  .hero-card {
    padding: 18px;
    border-radius: 22px;
  }

  .hero-title-row {
    grid-template-columns: 1fr;
  }

  .hero-badge {
    width: auto;
    height: auto;
    justify-self: start;
    padding: 8px 14px;
    border-radius: 999px;
    transform: none;
  }

  .home-grid {
    grid-template-columns: 1fr 1fr;
  }

  .direction-card-v2 {
    min-height: 162px;
    padding: 16px;
  }

  .direction-emoji {
    width: 44px;
    height: 44px;
    font-size: 24px;
  }

  .category-summary {
    grid-template-columns: 1fr;
  }

  .category-hint {
    justify-self: stretch;
    white-space: normal;
    line-height: 1.5;
  }

  .map-grid-v2 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 420px) {
  .home-grid {
    grid-template-columns: 1fr;
  }

  .map-grid-v2 {
    grid-template-columns: 1fr;
  }

  .hero-title-row h2 {
    font-size: 30px;
  }
}
'''

def patch_app_js():
    if not APP_JS.exists():
        raise RuntimeError("没有找到 app.js，请确认脚本放在 game-map-web 根目录。")

    text = APP_JS.read_text(encoding="utf-8")

    backup = ROOT / "app.backup.before_ui_v2.js"
    if not backup.exists():
        shutil.copy2(APP_JS, backup)

    home_pattern = r'function renderHome\(\)\s*\{.*?\n\}\n\nfunction renderCategory'
    text, home_count = re.subn(home_pattern, NEW_RENDER_HOME + "\n\nfunction renderCategory", text, count=1, flags=re.S)

    cat_pattern = r'function renderCategory\(dirKey,\s*label\)\s*\{.*?\n\}\n\nfunction openViewer'
    text, cat_count = re.subn(cat_pattern, NEW_RENDER_CATEGORY + "\n\nfunction openViewer", text, count=1, flags=re.S)

    if home_count == 0:
        raise RuntimeError("没有成功定位 renderHome 函数。")
    if cat_count == 0:
        raise RuntimeError("没有成功定位 renderCategory 函数。")

    APP_JS.write_text(text, encoding="utf-8")
    return "[OK] app.js 首页与分类页已升级"

def patch_style_css():
    if not STYLE_CSS.exists():
        raise RuntimeError("没有找到 style.css。")

    text = STYLE_CSS.read_text(encoding="utf-8")

    backup = ROOT / "style.backup.before_ui_v2.css"
    if not backup.exists():
        shutil.copy2(STYLE_CSS, backup)

    marker = "/* ===== UI beautify v2 ===== */"
    if marker not in text:
        STYLE_CSS.write_text(text.rstrip() + "\n\n" + EXTRA_CSS + "\n", encoding="utf-8")
        return "[OK] style.css 已追加 UI v2 美化样式"
    return "[SKIP] style.css 已存在 UI v2 样式，未重复追加"

def patch_index():
    if not INDEX_HTML.exists():
        return "[SKIP] 没有找到 index.html"

    text = INDEX_HTML.read_text(encoding="utf-8")

    backup = ROOT / "index.backup.before_ui_v2.html"
    if not backup.exists():
        shutil.copy2(INDEX_HTML, backup)

    text = text.replace("<title>游戏地图助手</title>", "<title>第五人格地图助手</title>")
    text = text.replace('content="游戏固定地图快速查看工具"', 'content="第五人格固定地图路线速查工具，仅供个人自用与学习交流"')

    text = re.sub(
        r'<script\s+src="\./app\.js(?:\?[^"]*)?"></script>',
        '<script src="./app.js?v=ui-beautify-v2"></script>',
        text
    )

    INDEX_HTML.write_text(text, encoding="utf-8")
    return "[OK] index.html 标题与 app.js 版本号已更新"

def main():
    logs = [
        "Beautify UI v2",
        "time: " + str(datetime.datetime.now()),
        "root: " + str(ROOT),
        "",
        patch_app_js(),
        patch_style_css(),
        patch_index(),
    ]
    output = "\n".join(logs)
    print(output)
    (ROOT / "beautify_ui_v2_log.txt").write_text(output, encoding="utf-8")

    print("")
    print("完成。下一步：")
    print("1. python -m http.server 8004")
    print("2. 打开 http://localhost:8004/index.html?v=ui2")
    print("3. 确认没问题后：git add . && git commit -m \"beautify ui\" && git push")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("[ERROR]", e)
        input("按回车退出...")
