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
  els.subtitle.textContent = "固定地图路线速查｜选择方向进入";
  els.back.classList.add("hidden");

  const grid = document.createElement("div");
  grid.className = "home-grid";

  for (const dir of DIRS) {
    const count = MAPS.filter(item => item.dir === dir.key).length;
    const btn = document.createElement("button");
    btn.className = "direction-card";
    btn.innerHTML =
      '<span class="direction-title">' + dir.label + '</span>' +
      '<span class="direction-count">' + count + ' 张地图路线</span>';
    btn.addEventListener("click", function () {
      renderCategory(dir.key, dir.label);
    });
    grid.appendChild(btn);
  }

  const info = document.createElement("section");
  info.className = "home-info-card";
  info.innerHTML =
    '<div class="home-info-title">主要信息</div>' +
    '<div class="home-info-text">选择门的方向后，点击地图缩略图查看完整路线图。绿色三角为入口，红线为主要路线，蓝色数字为推荐检查顺序。</div>' +
    '<div class="home-meta-grid">' +
      '<div><span>作者</span><strong>cici吃饱饱</strong></div>' +
      '<div><span>第五人格 ID</span><strong>nku守门员</strong></div>' +
      '<div><span>问题联系</span><strong>jayceja817@gmail.com</strong></div>' +
    '</div>' +
    '<div class="home-notice">' +
      '声明：本工具仅供个人自用与学习交流，不用于任何商业用途。地图资料借鉴了 B 站 UP 主“凉哈皮”的相关图片内容，并在此基础上进行个人整理与路线标注。自制整理不易，请勿肆意传播或用于商业转载；如有不妥，请通过上方邮箱联系处理。' +
    '</div>';

  els.main.replaceChildren(grid, info);
}'''

EXTRA_CSS = r'''
/* ===== Homepage beautify by beautify_homepage_v1.py ===== */

.home-info-card {
  margin-top: 18px;
  border: 1px solid rgba(148, 163, 184, 0.24);
  border-radius: 24px;
  background:
    linear-gradient(135deg, rgba(15, 23, 42, 0.92), rgba(30, 41, 59, 0.78)),
    rgba(255, 255, 255, 0.06);
  box-shadow: 0 18px 45px rgba(0, 0, 0, 0.26);
  padding: 20px;
  overflow: hidden;
}

.home-info-title {
  display: inline-flex;
  align-items: center;
  min-height: 34px;
  padding: 5px 14px;
  border-radius: 999px;
  background: linear-gradient(135deg, rgba(56, 189, 248, 0.22), rgba(129, 140, 248, 0.18));
  border: 1px solid rgba(125, 211, 252, 0.32);
  color: #e0f2fe;
  font-weight: 900;
  font-size: 16px;
  letter-spacing: 0.02em;
}

.home-info-text {
  margin-top: 14px;
  color: #e5e7eb;
  font-size: 15px;
  line-height: 1.75;
}

.home-meta-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  margin-top: 16px;
}

.home-meta-grid > div {
  min-height: 72px;
  border: 1px solid rgba(148, 163, 184, 0.20);
  border-radius: 18px;
  padding: 12px 14px;
  background: rgba(15, 23, 42, 0.58);
}

.home-meta-grid span {
  display: block;
  color: #94a3b8;
  font-size: 12px;
  margin-bottom: 7px;
}

.home-meta-grid strong {
  display: block;
  color: #ffffff;
  font-size: 16px;
  line-height: 1.35;
  word-break: break-all;
}

.home-notice {
  margin-top: 14px;
  border-left: 4px solid #fbbf24;
  border-radius: 14px;
  background: rgba(251, 191, 36, 0.10);
  padding: 12px 14px;
  color: #fde68a;
  font-size: 13px;
  line-height: 1.75;
}

.direction-card {
  transition: transform 0.16s ease, border-color 0.16s ease, background 0.16s ease;
}

.direction-card:active {
  transform: scale(0.98);
}

.direction-card:hover {
  border-color: rgba(125, 211, 252, 0.55);
  background:
    linear-gradient(135deg, rgba(56, 189, 248, 0.20), rgba(129, 140, 248, 0.10)),
    var(--panel);
}

@media (max-width: 720px) {
  .home-meta-grid {
    grid-template-columns: 1fr;
  }

  .home-info-card {
    padding: 16px;
    border-radius: 20px;
  }

  .home-info-text {
    font-size: 14px;
  }

  .home-notice {
    font-size: 12px;
  }
}
'''

def patch_app_js():
    if not APP_JS.exists():
        raise RuntimeError("没有找到 app.js，请确认脚本放在 game-map-web 根目录。")

    text = APP_JS.read_text(encoding="utf-8")

    backup = ROOT / "app.backup.before_beautify.js"
    if not backup.exists():
        shutil.copy2(APP_JS, backup)

    pattern = r'function renderHome\(\)\s*\{.*?\n\}\n\nfunction renderCategory'
    replacement = NEW_RENDER_HOME + "\n\nfunction renderCategory"
    new_text, count = re.subn(pattern, replacement, text, count=1, flags=re.S)

    if count == 0:
        raise RuntimeError("没有成功定位 renderHome 函数。请把 app.js 发给我，我帮你手动改。")

    APP_JS.write_text(new_text, encoding="utf-8")
    return "[OK] app.js 首页内容已美化"

def patch_style_css():
    if not STYLE_CSS.exists():
        raise RuntimeError("没有找到 style.css。")

    text = STYLE_CSS.read_text(encoding="utf-8")

    backup = ROOT / "style.backup.before_beautify.css"
    if not backup.exists():
        shutil.copy2(STYLE_CSS, backup)

    marker = "/* ===== Homepage beautify by beautify_homepage_v1.py ===== */"
    if marker not in text:
        STYLE_CSS.write_text(text.rstrip() + "\n\n" + EXTRA_CSS + "\n", encoding="utf-8")
        return "[OK] style.css 已追加首页美化样式"
    return "[SKIP] style.css 已存在美化样式，未重复追加"

def patch_index():
    if not INDEX_HTML.exists():
        return "[SKIP] 没有找到 index.html"

    text = INDEX_HTML.read_text(encoding="utf-8")

    backup = ROOT / "index.backup.before_beautify.html"
    if not backup.exists():
        shutil.copy2(INDEX_HTML, backup)

    text = text.replace("<title>游戏地图助手</title>", "<title>第五人格地图助手</title>")
    text = text.replace('content="游戏固定地图快速查看工具"', 'content="第五人格固定地图路线速查工具，仅供个人自用与学习交流"')

    text = re.sub(
        r'<script\s+src="\./app\.js(?:\?[^"]*)?"></script>',
        '<script src="./app.js?v=beautify-homepage-v1"></script>',
        text
    )

    INDEX_HTML.write_text(text, encoding="utf-8")
    return "[OK] index.html 标题与 app.js 版本号已更新"

def main():
    logs = [
        "Beautify homepage",
        "time: " + str(datetime.datetime.now()),
        "root: " + str(ROOT),
        "",
        patch_app_js(),
        patch_style_css(),
        patch_index(),
    ]
    output = "\n".join(logs)
    print(output)
    (ROOT / "beautify_homepage_log.txt").write_text(output, encoding="utf-8")

    print("")
    print("完成。下一步：")
    print("1. python -m http.server 8003")
    print("2. 打开 http://localhost:8003/index.html?v=beautify1")
    print("3. 确认没问题后：git add . && git commit -m \"beautify homepage\" && git push")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("[ERROR]", e)
        input("按回车退出...")
