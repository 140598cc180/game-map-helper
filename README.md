# 地图系列小助手

把两套地图小抄放在一个离线软件中：

- 噩梦之女：困难难度，最后更新 7.25，4 类 28 张地图。
- 磷光症：噩梦难度，最后更新 11.8，6 类 15 张地图。

主页先选系列，然后选择类别、地图缩略图并打开详情。详情图支持缩放和拖动。软件运行时只读取随软件附带的 `catalog.js` 和图片，不联网、不搜索目录，也不调用扫描接口。

## Windows 版

双击 `地图系列小助手.exe`，或运行 `启动地图助手.cmd`。Windows 软件和地图图片需放在同一项目目录中。

重新生成软件：双击 `重新生成软件.cmd`。更新地图后重新生成清单和软件；运行中的版本不会自动发现新图。

## 安卓平板版

安装包位于 `release/地图系列小助手-安卓版.apk`。图片已打入 APK，可离线查看；支持横竖屏、分屏、双指缩放和系统返回。安装步骤见[安卓平板安装说明](安卓平板安装说明.md)。

补图后运行 `一键生成安卓安装包.cmd`，再把新 APK 传到平板覆盖安装。请保留 `android-tablet/.signing/maphelper.keystore`，它用于后续覆盖更新。

## 网页版

根目录中的 `index.html`、`catalog.js`、`app.js`、`style.css` 和地图图片构成静态离线网站。部署到 GitHub Pages 时，全部图片以仓库内的相对路径加载，不依赖 API 或远程图片。

## 地图文件

噩梦之女使用固定清单 `series/nightmare-woman/catalog.json`，对应的缩略图与详情图存放在 `series/nightmare-woman/assets/`。原图按原扩展名和内容保存。

磷光症仍按 `classimage/`、`class1/` 至 `class6/` 的命名规则放置。缩略图和类别图标保留 PNG，现有 detail 地图为 JPG。补图后重新生成清单和目标安装包，图片路径才会进入该静态版本。

## 生成与检查

- Windows EXE：运行 `重新生成软件.cmd`。
- Android APK：运行 `一键生成安卓安装包.cmd`。
- 仅准备 Android 离线资源：`powershell -ExecutionPolicy Bypass -File build-tablet.ps1 -PrepareOnly`。
- JavaScript 语法：`node --check app.js`。
- Windows 与浏览器回归：`node tests/smoke.cjs`。
- Android 离线与触控回归：`node tests/tablet-smoke.cjs`。

`android-tablet/app/src/main/assets/www/` 是生成目录，修改根目录文件后再重新打包。
