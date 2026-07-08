# -*- coding: utf-8 -*-
from pathlib import Path
import re
import shutil
import datetime

ROOT = Path(__file__).resolve().parent
APP = ROOT / "app.js"
CSS = ROOT / "style.css"
HTML = ROOT / "index.html"

HOME = r"""function renderHome() {
  currentDir = null;
  els.title.textContent = "地图速查";
  els.subtitle.textContent = "选择方向";
  els.back.classList.add("hidden");

  const meta = {
    "北": ["🧭", "北门"],
    "右": ["➡️", "右门"],
    "左": ["⬅️", "左门"],
    "南": ["🔻", "南门"]
  };

  const wrap = document.createElement("section");
  wrap.className = "battle-home";

  const title = document.createElement("div");
  title.className = "battle-title";
  title.innerHTML =
    '<div class="battle-title-main">🎮 第五人格地图助手</div>' +
    '<div class="battle-title-sub">🟢入口　🔴路线　🔵顺序</div>';

  const grid = document.createElement("div");
  grid.className = "battle-dir-grid";

  for (const dir of DIRS) {
    const count = MAPS.filter(item => item.dir === dir.key).length;
    const m = meta[dir.key] || ["📍", dir.label];
    const btn = document.createElement("button");
    btn.className = "battle-dir-btn";
    btn.innerHTML =
      '<span class="battle-dir-emoji">' + m[0] + '</span>' +
      '<span class="battle-dir-name">' + dir.label + '</span>' +
      '<span class="battle-dir-count">' + count + ' 张</span>';
    btn.addEventListener("click", function () {
      renderCategory(dir.key, dir.label);
    });
    grid.appendChild(btn);
  }

  const info = document.createElement("div");
  info.className = "battle-info";
  info.innerHTML =
    '<div>作者：cici吃饱饱｜第五人格ID：nku守门员</div>' +
    '<div>仅个人自用，非商业用途；借鉴 B 站 UP 主“凉哈皮”的图，自制不易请勿肆意传播。</div>' +
    '<div>联系：jayceja817@gmail.com</div>';

  wrap.append(title, grid, info);
  els.main.replaceChildren(wrap);
}"""

CATEGORY = r"""function renderCategory(dirKey, label) {
  currentDir = dirKey;
  const emoji = { "北": "🧭", "右": "➡️", "左": "⬅️", "南": "🔻" }[dirKey] || "📍";

  els.title.textContent = emoji + " " + label;
  els.subtitle.textContent = "点图打开";
  els.back.classList.remove("hidden");

  const list = MAPS.filter(item => item.dir === dirKey);
  const wrap = document.createElement("section");
  wrap.className = "battle-category";

  const head = document.createElement("div");
  head.className = "battle-cat-head";
  head.innerHTML =
    '<div class="battle-cat-title">' + emoji + ' ' + label + '</div>' +
    '<div class="battle-cat-rule">🟢入口 🔴路线 🔵顺序</div>' +
    '<div class="battle-cat-count">' + list.length + '张</div>';

  const grid = document.createElement("div");
  grid.className = "battle-map-grid";

  for (let i = 0; i < list.length; i++) {
    const item = list[i];
    const card = document.createElement("button");
    card.className = "battle-map-card";
    card.setAttribute("aria-label", "查看" + item.name);

    const imgBox = document.createElement("div");
    imgBox.className = "battle-thumb";

    const img = document.createElement("img");
    img.loading = "lazy";
    img.alt = item.name;
    img.src = thumbSrc(item);
    img.onerror = function () {
      imgBox.innerHTML = '<div class="missing-img">图未找到<br>' + item.thumb + '</div>';
    };
    imgBox.appendChild(img);

    const name = document.createElement("div");
    name.className = "battle-map-name";
    name.innerHTML =
      '<span class="battle-map-no">' + String(i + 1).padStart(2, "0") + '</span>' +
      '<span class="battle-map-title">' + item.name + '</span>';

    card.append(imgBox, name);
    card.addEventListener("click", function () {
      openViewer(item);
    });
    grid.appendChild(card);
  }

  wrap.append(head, grid);
  els.main.replaceChildren(wrap);
}"""

STYLE = r"""
/* ===== Battle Compact UI v3 ===== */

.app-shell {
  width: min(960px, 100%);
  padding: calc(8px + env(safe-area-inset-top)) 8px calc(8px + env(safe-area-inset-bottom));
}

.topbar {
  padding: 5px 0 7px;
  gap: 8px;
}

#pageTitle {
  font-size: clamp(20px, 5vw, 30px);
  line-height: 1.05;
}

#pageSubtitle {
  margin-top: 2px;
  font-size: 12px;
}

.icon-btn, .install-btn, .viewer-btn {
  min-width: 38px;
  height: 38px;
  padding: 0 12px;
}

.main {
  min-height: auto;
}

.battle-home {
  display: grid;
  gap: 9px;
}

.battle-title {
  border: 1px solid rgba(148, 163, 184, 0.22);
  border-radius: 18px;
  padding: 11px 13px;
  background:
    radial-gradient(circle at top right, rgba(56,189,248,0.18), transparent 18rem),
    linear-gradient(135deg, rgba(15,23,42,0.94), rgba(30,41,59,0.76));
  box-shadow: 0 14px 34px rgba(0,0,0,0.22);
}

.battle-title-main {
  font-size: clamp(22px, 6vw, 34px);
  font-weight: 1000;
  letter-spacing: -0.05em;
}

.battle-title-sub {
  margin-top: 4px;
  color: #cbd5e1;
  font-size: 13px;
  font-weight: 800;
}

.battle-dir-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 9px;
}

.battle-dir-btn {
  min-height: clamp(112px, 22vh, 166px);
  border: 1px solid rgba(148, 163, 184, 0.22);
  border-radius: 22px;
  color: #fff;
  text-align: left;
  padding: 13px;
  background:
    linear-gradient(135deg, rgba(255,255,255,0.14), rgba(255,255,255,0.04)),
    rgba(15,23,42,0.78);
  box-shadow: 0 14px 32px rgba(0,0,0,0.22);
}

.battle-dir-btn:active {
  transform: scale(0.98);
}

.battle-dir-emoji {
  display: grid;
  place-items: center;
  width: 40px;
  height: 40px;
  border-radius: 15px;
  background: rgba(255,255,255,0.13);
  font-size: 23px;
}

.battle-dir-name {
  display: block;
  margin-top: 8px;
  font-size: clamp(30px, 9vw, 46px);
  font-weight: 1000;
  letter-spacing: -0.06em;
  line-height: 1;
}

.battle-dir-count {
  display: inline-flex;
  margin-top: 7px;
  padding: 5px 9px;
  border-radius: 999px;
  background: rgba(226,232,240,0.92);
  color: #07111f;
  font-size: 12px;
  font-weight: 1000;
}

.battle-info {
  border: 1px solid rgba(251,191,36,0.22);
  border-radius: 15px;
  padding: 8px 10px;
  background: rgba(251,191,36,0.08);
  color: #fde68a;
  font-size: 11px;
  line-height: 1.5;
}

.battle-category {
  display: grid;
  gap: 8px;
}

.battle-cat-head {
  display: grid;
  grid-template-columns: 1fr auto;
  grid-template-areas:
    "title count"
    "rule count";
  align-items: center;
  gap: 2px 10px;
  border: 1px solid rgba(148, 163, 184, 0.22);
  border-radius: 17px;
  padding: 9px 11px;
  background: linear-gradient(135deg, rgba(15,23,42,0.88), rgba(30,41,59,0.72));
}

.battle-cat-title {
  grid-area: title;
  font-size: 22px;
  font-weight: 1000;
  line-height: 1.05;
}

.battle-cat-rule {
  grid-area: rule;
  color: #cbd5e1;
  font-size: 12px;
  font-weight: 800;
}

.battle-cat-count {
  grid-area: count;
  border-radius: 999px;
  padding: 6px 10px;
  background: rgba(226,232,240,0.92);
  color: #07111f;
  font-size: 12px;
  font-weight: 1000;
}

.battle-map-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 7px;
}

.battle-map-card {
  overflow: hidden;
  border: 1px solid rgba(148, 163, 184, 0.20);
  border-radius: 15px;
  background: rgba(15,23,42,0.72);
  color: #fff;
  padding: 0;
  box-shadow: 0 9px 22px rgba(0,0,0,0.18);
}

.battle-map-card:active {
  transform: scale(0.985);
}

.battle-thumb {
  width: 100%;
  aspect-ratio: 18 / 9;
  background: rgba(15, 23, 42, 0.75);
  overflow: hidden;
}

.battle-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.battle-map-name {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 7px 7px;
  font-size: 12px;
  font-weight: 1000;
  white-space: nowrap;
  overflow: hidden;
}

.battle-map-no {
  flex: 0 0 auto;
  min-width: 27px;
  height: 21px;
  display: inline-grid;
  place-items: center;
  border-radius: 999px;
  background: rgba(56,189,248,0.16);
  border: 1px solid rgba(56,189,248,0.28);
  color: #bae6fd;
  font-size: 11px;
}

.battle-map-title {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 隐藏旧版冗余大卡片 */
.hero-card,
.home-info-card-v2,
.category-summary,
.map-grid-v2 {
  display: none !important;
}

@media (min-width: 760px) {
  .battle-dir-grid {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
  .battle-map-grid {
    grid-template-columns: repeat(auto-fit, minmax(145px, 1fr));
  }
}

@media (max-height: 680px) {
  .topbar {
    padding-top: 3px;
    padding-bottom: 4px;
  }
  .battle-title {
    padding: 8px 11px;
  }
  .battle-title-main {
    font-size: 22px;
  }
  .battle-dir-btn {
    min-height: 104px;
  }
  .battle-info {
    display: none;
  }
  .battle-cat-head {
    padding: 7px 10px;
  }
  .battle-thumb {
    aspect-ratio: 20 / 9;
  }
}

@media (max-width: 390px) {
  .app-shell {
    padding-left: 7px;
    padding-right: 7px;
  }
  .battle-dir-grid,
  .battle-map-grid {
    gap: 6px;
  }
  .battle-dir-name {
    font-size: 30px;
  }
  .battle-map-name {
    font-size: 11px;
  }
}
"""

def patch_js():
    if not APP.exists():
        raise RuntimeError("没有找到 app.js")
    text = APP.read_text(encoding="utf-8")
    backup = ROOT / "app.backup.before_battle_compact_v3.js"
    if not backup.exists():
        shutil.copy2(APP, backup)

    text, n1 = re.subn(
        r"function renderHome\(\)\s*\{.*?\n\}\n\nfunction renderCategory",
        HOME + "\n\nfunction renderCategory",
        text,
        count=1,
        flags=re.S,
    )
    text, n2 = re.subn(
        r"function renderCategory\(dirKey,\s*label\)\s*\{.*?\n\}\n\nfunction openViewer",
        CATEGORY + "\n\nfunction openViewer",
        text,
        count=1,
        flags=re.S,
    )
    if n1 == 0:
        raise RuntimeError("没有定位到 renderHome")
    if n2 == 0:
        raise RuntimeError("没有定位到 renderCategory")
    APP.write_text(text, encoding="utf-8")
    return "[OK] app.js 已改成实战紧凑版"

def patch_css():
    if not CSS.exists():
        raise RuntimeError("没有找到 style.css")
    text = CSS.read_text(encoding="utf-8")
    backup = ROOT / "style.backup.before_battle_compact_v3.css"
    if not backup.exists():
        shutil.copy2(CSS, backup)
    if "/* ===== Battle Compact UI v3 ===== */" not in text:
        CSS.write_text(text.rstrip() + "\n\n" + STYLE + "\n", encoding="utf-8")
        return "[OK] style.css 已追加实战紧凑版样式"
    return "[SKIP] style.css 已有实战紧凑版样式"

def patch_html():
    if not HTML.exists():
        return "[SKIP] 没有找到 index.html"
    text = HTML.read_text(encoding="utf-8")
    backup = ROOT / "index.backup.before_battle_compact_v3.html"
    if not backup.exists():
        shutil.copy2(HTML, backup)
    text = text.replace("<title>游戏地图助手</title>", "<title>第五人格地图助手</title>")
    text = re.sub(
        r'<script\s+src="\./app\.js(?:\?[^"]*)?"></script>',
        '<script src="./app.js?v=battle-compact-v3"></script>',
        text,
    )
    HTML.write_text(text, encoding="utf-8")
    return "[OK] index.html 已更新缓存版本号"

def main():
    logs = [
        "Battle Compact UI v3",
        "time: " + str(datetime.datetime.now()),
        "root: " + str(ROOT),
        "",
        patch_js(),
        patch_css(),
        patch_html(),
    ]
    out = "\n".join(logs)
    print(out)
    (ROOT / "battle_compact_v3_log.txt").write_text(out, encoding="utf-8")
    print("")
    print("完成。请预览：")
    print("python -m http.server 8005")
    print("http://localhost:8005/index.html?v=compact3")
    print("")
    print("确认后上传：")
    print("git add .")
    print('git commit -m "compact ui and update images"')
    print("git push")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("[ERROR]", e)
        input("按回车退出...")
