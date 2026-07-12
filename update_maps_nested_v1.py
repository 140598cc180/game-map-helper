# -*- coding: utf-8 -*-
from pathlib import Path
import re
import shutil
import datetime
import json

ROOT = Path(__file__).resolve().parent
APP_JS = ROOT / "app.js"
INDEX_HTML = ROOT / "index.html"

MAPS = [
    {"dir": "北", "name": "北-1门", "thumb": "北门/t1-北-1门.jpg", "detail": "北门/1-北-1门.jpg"},
    {"dir": "北", "name": "北-1沙发门", "thumb": "北门/t2-北-1沙发门.png", "detail": "北门/2-北-1沙发门.png"},
    {"dir": "北", "name": "北-4安全门", "thumb": "北门/t3-北-4安全门.png", "detail": "北门/3-北-4安全门.png"},
    {"dir": "北", "name": "北-4门", "thumb": "北门/t4-北-4门.jpg", "detail": "北门/4-北-4门.jpg"},
    {"dir": "北", "name": "北-T门", "thumb": "北门/t5-北-T门.jpg", "detail": "北门/5-北-T门.jpg"},
    {"dir": "北", "name": "北-凹门", "thumb": "北门/t6-北-凹门.jpg", "detail": "北门/6-北-凹门.jpg"},
    {"dir": "北", "name": "北-红对角门", "thumb": "北门/t7-北-红对角门.jpg", "detail": "北门/7-北-红对角门.jpg"},
    {"dir": "北", "name": "北-红门", "thumb": "北门/t8-北-红门.jpg", "detail": "北门/8-北-红门.jpg"},

    {"dir": "南", "name": "南-十字门", "thumb": "南门/t9-南-十字门.jpg", "detail": "南门/9-南-十字门.jpg"},
    {"dir": "南", "name": "南-三缺一门", "thumb": "南门/t10-南-三缺一门.jpg", "detail": "南门/10-南-三缺一门.jpg"},
    {"dir": "南", "name": "南-L门", "thumb": "南门/t11-南-L门.png", "detail": "南门/11-南-L门.png"},
    {"dir": "南", "name": "南-红门", "thumb": "南门/t12-南-红门.png", "detail": "南门/12-南-红门.png"},
    {"dir": "南", "name": "南-orz门", "thumb": "南门/t13-南-orz门.png", "detail": "南门/13-南-orz门.png"},

    {"dir": "左", "name": "左-锤子门", "thumb": "左门/t14-左-锤子门.png", "detail": "左门/14-左-锤子门.png"},
    {"dir": "左", "name": "左-倒T门", "thumb": "左门/t15-左-倒T门.jpg", "detail": "左门/15-左-倒T门.jpg"},
    {"dir": "左", "name": "左-对T门", "thumb": "左门/t16-左-对T门.png", "detail": "左门/16-左-对T门.png"},
    {"dir": "左", "name": "左-Y青蛙房", "thumb": "左门/t17-左-Y青蛙房.png", "detail": "左门/17-左-Y青蛙房.png"},
    {"dir": "左", "name": "左-对角门", "thumb": "左门/t18-左-对角门.png", "detail": "左门/18-左-对角门.png"},
    {"dir": "左", "name": "左-Y门", "thumb": "左门/t19-左-Y门.jpg", "detail": "左门/19-左-Y门.jpg"},
    {"dir": "左", "name": "左-锤灯笼门", "thumb": "左门/t20-左-锤灯笼门.png", "detail": "左门/20-左-锤灯笼门.png"},
    {"dir": "左", "name": "左-罐子门", "thumb": "左门/t21-左-罐子门.png", "detail": "左门/21-左-罐子门.png"},
    {"dir": "左", "name": "左-音叉门", "thumb": "左门/22-左-音叉门.jpg", "detail": "左门/22-左-音叉门.jpg"},

    {"dir": "右", "name": "右-左上右下门", "thumb": "右门/t23-右-左上右下门.jpg", "detail": "右门/23-右-左上右下门.jpg"},
    {"dir": "右", "name": "右-L门", "thumb": "右门/t24-右-L门.png", "detail": "右门/24-右-L门.png"},
    {"dir": "右", "name": "右-锤子门", "thumb": "右门/t25-右-锤子门.jpg", "detail": "右门/25-右-锤子门.jpg"},
    {"dir": "右", "name": "右-骑士门", "thumb": "右门/t26-右-骑士门.png", "detail": "右门/26-右-骑士门.png"},
    {"dir": "右", "name": "右-三L门", "thumb": "右门/t27-右-三L门.png", "detail": "右门/27-右-三L门.png"},
    {"dir": "右", "name": "右-双L门", "thumb": "右门/t28-右-双L门.jpg", "detail": "右门/28-右-双L门.jpg"},
]


def check_files():
    if not APP_JS.exists():
        raise RuntimeError("没有找到 app.js，请确认脚本放在 game-map-web 根目录。")
    missing = []
    for item in MAPS:
        thumb = ROOT / "assets" / "thumbnails" / item["thumb"]
        detail = ROOT / "assets" / "details" / item["detail"]
        if not thumb.exists():
            missing.append("缩略图缺失：" + str(thumb.relative_to(ROOT)))
        if not detail.exists():
            missing.append("详细图缺失：" + str(detail.relative_to(ROOT)))
    if missing:
        print("发现文件缺失：")
        for m in missing:
            print(" - " + m)
        raise RuntimeError("文件缺失，已停止写入 app.js。")


def patch_app_js():
    text = APP_JS.read_text(encoding="utf-8")
    backup = ROOT / ("app.backup.before_nested_maps_%s.js" % datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    shutil.copy2(APP_JS, backup)

    maps_js = "const MAPS = " + json.dumps(MAPS, ensure_ascii=False, indent=2) + ";"
    text, count = re.subn(r"const\s+MAPS\s*=\s*\[.*?\];", maps_js, text, count=1, flags=re.S)
    if count == 0:
        raise RuntimeError("没有在 app.js 中找到 const MAPS = [...]。")

    text = re.sub(
        r"function\s+thumbSrc\s*\(\s*item\s*\)\s*\{.*?\}",
        'function thumbSrc(item) {\n  return "./assets/thumbnails/" + item.thumb;\n}',
        text,
        count=1,
        flags=re.S
    )
    text = re.sub(
        r"function\s+detailSrc\s*\(\s*item\s*\)\s*\{.*?\}",
        'function detailSrc(item) {\n  return "./assets/details/" + item.detail;\n}',
        text,
        count=1,
        flags=re.S
    )

    APP_JS.write_text(text, encoding="utf-8")
    return "[OK] app.js 已更新为新版 28 张地图和子文件夹路径"


def patch_index_html():
    if not INDEX_HTML.exists():
        return "[SKIP] 没有找到 index.html"
    text = INDEX_HTML.read_text(encoding="utf-8")
    backup = ROOT / ("index.backup.before_nested_maps_%s.html" % datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    shutil.copy2(INDEX_HTML, backup)
    text = re.sub(
        r'<script\s+src="\./app\.js(?:\?[^"]*)?"></script>',
        '<script src="./app.js?v=nested-maps-20260712"></script>',
        text
    )
    INDEX_HTML.write_text(text, encoding="utf-8")
    return "[OK] index.html 已刷新 app.js 版本号"


def main():
    print("正在检查新版地图文件是否完整...")
    check_files()
    logs = [
        "Update nested maps",
        "time: " + str(datetime.datetime.now()),
        "root: " + str(ROOT),
        "",
        patch_app_js(),
        patch_index_html(),
        "",
        "地图数量：%d" % len(MAPS),
        "北门：%d" % len([x for x in MAPS if x["dir"] == "北"]),
        "南门：%d" % len([x for x in MAPS if x["dir"] == "南"]),
        "左门：%d" % len([x for x in MAPS if x["dir"] == "左"]),
        "右门：%d" % len([x for x in MAPS if x["dir"] == "右"]),
    ]
    out = "\n".join(logs)
    print(out)
    (ROOT / "update_nested_maps_log.txt").write_text(out, encoding="utf-8")
    print("")
    print("完成。请本地预览：")
    print("python -m http.server 8006")
    print("http://localhost:8006/index.html?v=nested1")
    print("")
    print("确认没问题后上传：")
    print("git status")
    print("git add .")
    print('git commit -m "update nested map assets"')
    print("git push")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("[ERROR]", e)
        input("按回车退出...")
