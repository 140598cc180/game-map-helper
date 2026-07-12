# -*- coding: utf-8 -*-
"""
把索引页缩略图改成正方形图标版。

作用：
1. 进入北门/南门/左门/右门后，缩略图统一变成正方形。
2. 图片在正方形里等比例自适应显示，不强行拉伸。
3. 手机端索引页改成 3 列，减少上下滑动。
4. 自动刷新 app.js 版本号，减少手机缓存影响。

使用：
cd D:\副业\game-map-web
python square_thumbnails_v1.py

预览：
python -m http.server 8007
http://localhost:8007/index.html?v=square1

上传：
git add .
git commit -m "make thumbnails square"
git push
"""

from pathlib import Path
import re
import shutil
import datetime

ROOT = Path(__file__).resolve().parent
CSS = ROOT / "style.css"
HTML = ROOT / "index.html"

STYLE = r"""
/* ===== Square thumbnails v1 ===== */

/* 索引页：缩略图统一正方形 */
.battle-thumb,
.compact-thumb,
.thumb-wrap-v2,
.thumb-wrap {
  aspect-ratio: 1 / 1 !important;
  width: 100%;
  border-radius: 12px 12px 0 0;
  background:
    radial-gradient(circle at center, rgba(56,189,248,0.08), transparent 70%),
    rgba(15, 23, 42, 0.72);
}

/* 图片保持比例，自适应放进正方形，不拉伸 */
.battle-thumb img,
.compact-thumb img,
.thumb-wrap-v2 img,
.thumb-wrap img {
  width: 100% !important;
  height: 100% !important;
  object-fit: contain !important;
  object-position: center center !important;
  background: rgba(15, 23, 42, 0.38);
}

/* 索引页卡片更像方形图标 */
.battle-map-card,
.compact-map-card,
.map-card-v2,
.map-card {
  border-radius: 14px !important;
}

/* 手机端默认 3 列，尽量一屏看完整 */
.battle-map-grid,
.compact-map-grid {
  grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
  gap: 7px !important;
}

/* 名字压缩，避免卡片被文字撑高 */
.battle-map-name,
.compact-map-name,
.map-name-v2,
.map-name {
  min-height: 34px;
  padding: 5px 6px 6px !important;
  font-size: 11px !important;
  line-height: 1.15 !important;
}

.battle-map-no,
.compact-map-index,
.map-index {
  min-width: 24px !important;
  height: 19px !important;
  font-size: 10px !important;
}

.battle-map-title,
.map-title-text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 大屏幕可以显示更多列 */
@media (min-width: 700px) {
  .battle-map-grid,
  .compact-map-grid {
    grid-template-columns: repeat(auto-fit, minmax(118px, 1fr)) !important;
  }
}

/* 特别小的手机仍保持 3 列，但进一步收紧间距 */
@media (max-width: 390px) {
  .battle-map-grid,
  .compact-map-grid {
    gap: 5px !important;
  }

  .battle-map-name,
  .compact-map-name,
  .map-name-v2,
  .map-name {
    font-size: 10px !important;
    min-height: 31px;
  }
}
"""


def patch_css():
    if not CSS.exists():
        raise RuntimeError("没有找到 style.css，请确认脚本放在 game-map-web 根目录。")

    text = CSS.read_text(encoding="utf-8")
    backup = ROOT / ("style.backup.before_square_thumbs_%s.css" % datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    shutil.copy2(CSS, backup)

    marker = "/* ===== Square thumbnails v1 ===== */"
    if marker not in text:
        CSS.write_text(text.rstrip() + "\n\n" + STYLE + "\n", encoding="utf-8")
        return "[OK] style.css 已追加正方形缩略图样式"
    return "[SKIP] style.css 已存在正方形缩略图样式"


def patch_html():
    if not HTML.exists():
        return "[SKIP] 没有找到 index.html"

    text = HTML.read_text(encoding="utf-8")
    backup = ROOT / ("index.backup.before_square_thumbs_%s.html" % datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    shutil.copy2(HTML, backup)

    text = re.sub(
        r'<script\s+src="\./app\.js(?:\?[^"]*)?"></script>',
        '<script src="./app.js?v=square-thumbnails-v1"></script>',
        text
    )
    HTML.write_text(text, encoding="utf-8")
    return "[OK] index.html 已刷新版本号"


def main():
    logs = [
        "Square thumbnails v1",
        "time: " + str(datetime.datetime.now()),
        "root: " + str(ROOT),
        "",
        patch_css(),
        patch_html(),
    ]
    out = "\n".join(logs)
    print(out)
    (ROOT / "square_thumbnails_v1_log.txt").write_text(out, encoding="utf-8")

    print("")
    print("完成。请预览：")
    print("python -m http.server 8007")
    print("http://localhost:8007/index.html?v=square1")
    print("")
    print("确认后上传：")
    print("git status")
    print("git add .")
    print('git commit -m "make thumbnails square"')
    print("git push")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("[ERROR]", e)
        input("按回车退出...")
