第五人格地图小助手——手机版网页 APK
=================================

这次是手机版，不是平板左右分栏版。

核心方式
--------

APK 内部直接加载你现有的网站：

- index.html
- app.js
- style.css
- manifest.json
- assets 目录

所以手机 APK 的页面结构、门方向选择、地图缩略图、详情大图和缩放逻辑，
都以你当前网页为准。

Android 工程只做三件事：

1. 用 WebView 打开本地网页；
2. 隐藏网页里的“安装应用”按钮，因为 APK 已经安装；
3. 处理安卓返回键和外部链接。

系统兼容
--------

- 最低 Android：Android 9
- minSdk：28
- 手机竖屏和横屏都可以使用
- 不再使用平板左右分栏界面
- 导入网页后，地图图片包含在 APK 内，可离线使用

第一步：备份并导入现有网页
------------------------

双击：

scripts\1_BACKUP_AND_IMPORT_WEBSITE.cmd

脚本会先把：

D:\副业\game-map-web

备份到：

D:\副业\game-map-web-backups

然后把现有网页复制到 APK 工程。

注意：

- 原网页不会被修改；
- APK 使用的是复制出来的网页副本；
- 每次网页更新后，可以重新运行导入脚本再生成 APK。

第二步：生成 APK
---------------

方式一：Android Studio

1. 使用 Android Studio 打开本工程根目录；
2. 等待 Gradle 同步；
3. 选择：

Build
→ Build App Bundle(s) / APK(s)
→ Build APK(s)

APK 通常位于：

app\build\outputs\apk\debug\app-debug.apk

方式二：GitHub Actions 自动打包

双击：

scripts\2_UPLOAD_AND_BUILD_APK.cmd

脚本会把工程放入现有网页仓库的：

android-phone

并添加自动构建流程。

推送成功后进入 GitHub：

Actions
→ Build Phone Web APK
→ 最新构建
→ Artifacts
→ IdentityV-Map-Helper-Phone-Android9

下载并解压后得到：

第五人格地图小助手-手机版-Android9.apk

安装
----

将 APK 发送到安卓手机，在系统设置中允许文件管理器或浏览器安装未知应用，
然后点击 APK 安装。

说明
----

这个压缩包是 APK 工程和自动打包工具，不是已经编译好的 APK。

实际 APK 必须通过 Android SDK 或 GitHub Actions 编译后生成。
