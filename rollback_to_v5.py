# -*- coding: utf-8 -*-
# 回退 mobile_author_fix_v6，恢复到运行 v6 之前的 v5 状态。
#
# 使用方法：
# cd D:\副业\game-map-web
# python rollback_to_v5.py
#
# 本地预览：
# python -m http.server 8011
# http://localhost:8011/index.html?v=rollback-v5
#
# 确认正常后上传：
# git add .
# git commit -m "rollback to cute ui v5"
# git push

from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parent

TARGETS = {
    "app.js": "app.backup.before_mobile_author_v6_*.js",
    "style.css": "style.backup.before_mobile_author_v6_*.css",
    "index.html": "index.backup.before_mobile_author_v6_*.html",
}


def latest_backup(pattern: str) -> Path:
    files = sorted(
        ROOT.glob(pattern),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    if not files:
        raise FileNotFoundError(f"没有找到备份文件：{pattern}")
    return files[0]


def restore_file(target_name: str, pattern: str) -> str:
    src = latest_backup(pattern)
    dst = ROOT / target_name

    if dst.exists():
        broken_backup = ROOT / f"{target_name}.broken_v6_backup"
        shutil.copy2(dst, broken_backup)

    shutil.copy2(src, dst)
    return f"[OK] {target_name} 已从 {src.name} 恢复"


def refresh_cache_version() -> str:
    index = ROOT / "index.html"
    text = index.read_text(encoding="utf-8")

    text = re.sub(
        r'<script\s+src="\./app\.js(?:\?[^"]*)?"></script>',
        '<script src="./app.js?v=cute-ui-v5-rollback"></script>',
        text
    )

    index.write_text(text, encoding="utf-8")
    return "[OK] 已刷新 app.js 缓存版本号"


def main():
    print("正在回退到 v5...")
    logs = []

    for target, pattern in TARGETS.items():
        logs.append(restore_file(target, pattern))

    logs.append(refresh_cache_version())

    print("\n".join(logs))
    print("")
    print("回退完成。请预览：")
    print("python -m http.server 8011")
    print("http://localhost:8011/index.html?v=rollback-v5")
    print("")
    print("确认正常后上传 GitHub：")
    print("git status")
    print("git add .")
    print('git commit -m "rollback to cute ui v5"')
    print("git push")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("[ERROR]", exc)
        print("如果提示找不到备份，请把项目目录下以 backup.before_mobile_author_v6 开头的文件名发给我。")
        input("按回车退出...")
