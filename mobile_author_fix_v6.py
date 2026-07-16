# -*- coding: utf-8 -*-
from pathlib import Path
import re
import shutil
import datetime

ROOT = Path(__file__).resolve().parent
APP_JS = ROOT / "app.js"
STYLE_CSS = ROOT / "style.css"
INDEX_HTML = ROOT / "index.html"

NEW_AUTHOR_NOTE = r'''<details class="cute-original-note cute-original-details">' +
      '<summary>📄 查看原创说明</summary>' +
      '<p>本工具中的地图整理、路线规划、界面设计及标注内容均为原创制作，部分图片与视觉效果使用 AI 辅助增强。仅供个人自用与学习交流，不用于商业用途。自制整理不易，请勿未经允许搬运、转载或用于商业传播。</p>' +
    '</details>'''

EXTRA_CSS = r'''
/* ===== Mobile author fix v6 ===== */

html {
  -webkit-text-size-adjust: 100%;
  text-size-adjust: 100%;
}

body {
  overflow-x: hidden;
}

.app-shell {
  padding-bottom: calc(96px + env(safe-area-inset-bottom)) !important;
}

.cute-author-card {
  width: 100%;
  box-sizing: border-box;
  grid-template-columns: 68px minmax(0, 1fr) !important;
  gap: 11px !important;
  align-items: start;
  padding: 13px !important;
  margin-bottom: 10px;
  overflow: hidden;
  border: 2px solid rgba(184, 160, 255, 0.28) !important;
  border-radius: 22px !important;
  background: rgba(255, 255, 255, 0.88) !important;
  box-shadow: 0 14px 34px rgba(106, 82, 115, 0.10) !important;
}

.cute-avatar-wrap,
.cute-avatar,
.cute-avatar-fallback {
  width: 68px !important;
  height: 68px !important;
  box-sizing: border-box;
}

.cute-avatar,
.cute-avatar-fallback {
  border-radius: 21px !important;
}

.cute-author-main {
  min-width: 0;
  overflow: hidden;
}

.cute-author-heading {
  font-size: 11px !important;
  line-height: 1.3;
}

.cute-author-name {
  margin-top: 2px !important;
  font-size: 19px !important;
  line-height: 1.15 !important;
  word-break: break-word;
}

.cute-author-id {
  margin-top: 3px !important;
  font-size: 11px !important;
  line-height: 1.4 !important;
}

.cute-author-tags {
  display: flex !important;
  flex-wrap: wrap !important;
  gap: 5px !important;
  margin-top: 7px !important;
}

.cute-author-tags span {
  padding: 4px 7px !important;
  font-size: 9px !important;
  line-height: 1.2;
  white-space: nowrap;
}

.cute-contact {
  display: flex !important;
  align-items: center;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
  margin-top: 8px !important;
  padding: 7px 9px;
  border: 1px solid rgba(255, 159, 199, 0.34);
  border-radius: 12px;
  background: rgba(255, 241, 247, 0.88);
  color: #8d5f7a !important;
  font-size: 11px !important;
  line-height: 1.35;
  text-decoration: none !important;
  overflow-wrap: anywhere;
  word-break: break-all;
}

.cute-original-details {
  grid-column: 1 / -1;
  width: 100%;
  box-sizing: border-box;
  margin-top: 1px;
  padding-top: 10px;
  border-top: 1px dashed rgba(166, 137, 177, 0.28);
}

.cute-original-details summary {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 36px;
  padding: 7px 10px;
  border: 1px solid rgba(184, 160, 255, 0.24);
  border-radius: 12px;
  background: rgba(248, 243, 255, 0.90);
  color: #806b88;
  font-size: 11px;
  font-weight: 900;
  cursor: pointer;
  list-style: none;
}

.cute-original-details summary::-webkit-details-marker {
  display: none;
}

.cute-original-details summary::after {
  content: "＋";
  font-size: 15px;
  line-height: 1;
}

.cute-original-details[open] summary::after {
  content: "－";
}

.cute-original-details p {
  margin: 8px 2px 0 !important;
  padding: 9px 10px;
  border-radius: 12px;
  background: rgba(255, 250, 253, 0.82);
  color: #7e7385 !important;
  font-size: 11px !important;
  line-height: 1.65 !important;
  letter-spacing: 0;
  text-align: left;
  overflow-wrap: anywhere;
}

@media (max-width: 430px) {
  .app-shell {
    padding-bottom: calc(104px + env(safe-area-inset-bottom)) !important;
  }

  .cute-author-card {
    grid-template-columns: 60px minmax(0, 1fr) !important;
    gap: 9px !important;
    padding: 11px !important;
    border-radius: 20px !important;
  }

  .cute-avatar-wrap,
  .cute-avatar,
  .cute-avatar-fallback {
    width: 60px !important;
    height: 60px !important;
  }

  .cute-avatar,
  .cute-avatar-fallback {
    border-radius: 19px !important;
  }

  .cute-author-name {
    font-size: 17px !important;
  }

  .cute-author-id {
    font-size: 10px !important;
  }

  .cute-author-tags {
    gap: 4px !important;
  }

  .cute-author-tags span {
    padding: 3px 6px !important;
    font-size: 8px !important;
  }

  .cute-contact {
    padding: 6px 8px;
    font-size: 10px !important;
  }

  .cute-original-details summary {
    font-size: 10px;
  }

  .cute-original-details p {
    font-size: 10px !important;
    line-height: 1.6 !important;
  }
}
'''

def patch_app():
    if not APP_JS.exists():
        raise RuntimeError("没有找到 app.js，请确认脚本位于项目根目录。")

    text = APP_JS.read_text(encoding="utf-8")
    backup = ROOT / (
        "app.backup.before_mobile_author_v6_%s.js"
        % datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    )
    shutil.copy2(APP_JS, backup)

    pattern = (
        r"'<div class=\"cute-original-note\">'\s*\+\s*"
        r"'<strong>原创说明</strong>'\s*\+\s*"
        r"'<p>.*?</p>'\s*\+\s*"
        r"'</div>'"
    )

    text, count = re.subn(
        pattern,
        lambda _: NEW_AUTHOR_NOTE,
        text,
        count=1,
        flags=re.S
    )

    if count == 0:
        raise RuntimeError("没有找到旧版原创说明区块，请确认已经运行 cute_ui_v5.py。")

    APP_JS.write_text(text, encoding="utf-8")
    return "[OK] app.js 已将原创说明改为折叠面板"

def patch_css():
    if not STYLE_CSS.exists():
        raise RuntimeError("没有找到 style.css。")

    text = STYLE_CSS.read_text(encoding="utf-8")
    backup = ROOT / (
        "style.backup.before_mobile_author_v6_%s.css"
        % datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    )
    shutil.copy2(STYLE_CSS, backup)

    marker = "/* ===== Mobile author fix v6 ===== */"
    if marker not in text:
        STYLE_CSS.write_text(
            text.rstrip() + "\n\n" + EXTRA_CSS + "\n",
            encoding="utf-8"
        )
        return "[OK] style.css 已追加手机端作者区修复样式"

    return "[SKIP] style.css 已存在 v6 修复样式"

def patch_html():
    if not INDEX_HTML.exists():
        return "[SKIP] 没有找到 index.html"

    text = INDEX_HTML.read_text(encoding="utf-8")
    backup = ROOT / (
        "index.backup.before_mobile_author_v6_%s.html"
        % datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    )
    shutil.copy2(INDEX_HTML, backup)

    text = re.sub(
        r'<script\s+src="\./app\.js(?:\?[^"]*)?"></script>',
        '<script src="./app.js?v=mobile-author-v6"></script>',
        text
    )

    INDEX_HTML.write_text(text, encoding="utf-8")
    return "[OK] index.html 已刷新缓存版本号"

def main():
    logs = [
        "Mobile author fix v6",
        "time: " + str(datetime.datetime.now()),
        "root: " + str(ROOT),
        "",
        patch_app(),
        patch_css(),
        patch_html(),
    ]

    output = "\n".join(logs)
    print(output)
    (ROOT / "mobile_author_fix_v6_log.txt").write_text(output, encoding="utf-8")

    print("")
    print("本地预览：")
    print("python -m http.server 8010")
    print("http://localhost:8010/index.html?v=mobile6")
    print("")
    print("确认后上传：")
    print("git add .")
    print('git commit -m "fix mobile author layout"')
    print("git push")

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("[ERROR]", exc)
        input("按回车退出...")
