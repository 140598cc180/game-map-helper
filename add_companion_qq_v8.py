# -*- coding: utf-8 -*-
# 在作者简介中增加陪玩说明和 QQ 联系方式。
#
# 修改效果：
# 第五人格 ID：nku守门员 · 欢迎找我陪玩
# 📮 jayceja817@gmail.com　QQ：1405985556
#
# 使用：
# cd D:\副业\game-map-web
# python add_companion_qq_v8.py
#
# 预览：
# python -m http.server 8013
# http://localhost:8013/index.html?v=contact8
#
# 上传：
# git add .
# git commit -m "add companion and qq contact"
# git push

from pathlib import Path
import re
import shutil
import datetime

ROOT = Path(__file__).resolve().parent
APP_JS = ROOT / "app.js"
STYLE_CSS = ROOT / "style.css"
INDEX_HTML = ROOT / "index.html"

EXTRA_CSS = r'''
/* ===== Companion and QQ contact v8 ===== */

.cute-author-id {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 4px 7px;
}

.cute-play-note {
  display: inline-flex;
  align-items: center;
  padding: 3px 7px;
  border-radius: 999px;
  background: rgba(255, 225, 238, 0.88);
  color: #9a617f;
  font-size: 9px;
  font-weight: 900;
  line-height: 1.2;
  white-space: nowrap;
}

.cute-contact-v7,
.cute-contact {
  display: flex !important;
  flex-wrap: wrap;
  align-items: center;
  gap: 5px 10px;
}

.cute-email-text,
.cute-qq-text {
  min-width: 0;
  overflow-wrap: anywhere;
}

.cute-qq-text {
  color: #86657a;
  font-weight: 900;
}

@media (max-width: 430px) {
  .cute-author-id {
    gap: 4px 5px;
  }

  .cute-play-note {
    padding: 3px 6px;
    font-size: 8px;
  }

  .cute-contact-v7,
  .cute-contact {
    gap: 4px 8px;
  }
}
'''


def patch_app_js():
    if not APP_JS.exists():
        raise RuntimeError("没有找到 app.js，请确认脚本位于项目根目录。")

    text = APP_JS.read_text(encoding="utf-8")
    backup = ROOT / (
        "app.backup.before_contact_v8_%s.js"
        % datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    )
    shutil.copy2(APP_JS, backup)

    id_pattern = (
        r"'<div class=\"cute-author-id\">"
        r"第五人格 ID：nku守门员"
        r"(?:.*?)"
        r"</div>'"
    )
    id_replacement = (
        '\'<div class="cute-author-id">\' +\n'
        '          \'<span>第五人格 ID：nku守门员</span>\' +\n'
        '          \'<span class="cute-play-note">🎮 欢迎找我陪玩</span>\' +\n'
        '        \'</div>\''
    )

    text, id_count = re.subn(
        id_pattern,
        lambda _: id_replacement,
        text,
        count=1,
        flags=re.S
    )

    contact_pattern = (
        r"'<a class=\"cute-contact(?: cute-contact-v7)?\" "
        r"href=\"mailto:jayceja817@gmail\.com\">"
        r".*?"
        r"</a>'"
    )
    contact_replacement = (
        '\'<a class="cute-contact cute-contact-v7" '
        'href="mailto:jayceja817@gmail.com">\' +\n'
        '      \'<span class="cute-email-text">📮 jayceja817@gmail.com</span>\' +\n'
        '      \'<span class="cute-qq-text">🐧 QQ：1405985556</span>\' +\n'
        '    \'</a>\''
    )

    text, contact_count = re.subn(
        contact_pattern,
        lambda _: contact_replacement,
        text,
        count=1,
        flags=re.S
    )

    if id_count == 0:
        raise RuntimeError("没有找到作者 ID 区域。")
    if contact_count == 0:
        raise RuntimeError("没有找到邮箱联系方式区域。")

    APP_JS.write_text(text, encoding="utf-8")
    return "[OK] app.js 已加入陪玩说明和 QQ 联系方式"


def patch_css():
    if not STYLE_CSS.exists():
        raise RuntimeError("没有找到 style.css。")

    text = STYLE_CSS.read_text(encoding="utf-8")
    backup = ROOT / (
        "style.backup.before_contact_v8_%s.css"
        % datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    )
    shutil.copy2(STYLE_CSS, backup)

    marker = "/* ===== Companion and QQ contact v8 ===== */"
    if marker not in text:
        STYLE_CSS.write_text(
            text.rstrip() + "\n\n" + EXTRA_CSS + "\n",
            encoding="utf-8"
        )
        return "[OK] style.css 已追加陪玩和 QQ 样式"

    return "[SKIP] style.css 已存在 v8 样式"


def patch_html():
    if not INDEX_HTML.exists():
        return "[SKIP] 没有找到 index.html"

    text = INDEX_HTML.read_text(encoding="utf-8")
    backup = ROOT / (
        "index.backup.before_contact_v8_%s.html"
        % datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    )
    shutil.copy2(INDEX_HTML, backup)

    text = re.sub(
        r'<script\s+src="\./app\.js(?:\?[^"]*)?"></script>',
        '<script src="./app.js?v=contact-v8"></script>',
        text
    )

    INDEX_HTML.write_text(text, encoding="utf-8")
    return "[OK] index.html 已刷新缓存版本号"


def main():
    logs = [
        "Companion and QQ contact v8",
        "time: " + str(datetime.datetime.now()),
        "root: " + str(ROOT),
        "",
        patch_app_js(),
        patch_css(),
        patch_html(),
    ]

    output = "\n".join(logs)
    print(output)
    (ROOT / "contact_v8_log.txt").write_text(output, encoding="utf-8")

    print("")
    print("本地预览：")
    print("python -m http.server 8013")
    print("http://localhost:8013/index.html?v=contact8")
    print("")
    print("确认后上传：")
    print("git add .")
    print('git commit -m "add companion and qq contact"')
    print("git push")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("[ERROR]", exc)
        input("按回车退出...")
