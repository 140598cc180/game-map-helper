# 游戏地图助手网页版

这是一个可以部署到 GitHub Pages 的静态网页版本。

## 功能

- 首页四个方向：北门、右门、左门、南门
- 进入方向后显示对应缩略图
- 点击缩略图查看详细大图
- 手机端自适应
- 支持 iPhone Safari 添加到主屏幕
- 支持 PWA 缓存，打开过的图片再次访问更快

## 文件结构

```text
game-map-web/
├── index.html
├── style.css
├── app.js
├── manifest.json
├── service-worker.js
├── .nojekyll
├── assets/
│   ├── thumbnails/
│   │   └── 把缩略图放这里
│   ├── details/
│   │   └── 把详细图放这里
│   └── icons/
└── copy_images_from_D.bat
```

## 第一步：复制图片

双击运行：

```text
copy_images_from_D.bat
```

它会把：

```text
D:\BaiduNetdiskDownload\缩略图
D:\BaiduNetdiskDownload\详细图
```

复制到网页项目的：

```text
assets\thumbnails
assets\details
```

也可以手动复制。

## 第二步：本地预览

在当前文件夹打开终端，运行：

```bash
python -m http.server 8000
```

浏览器打开：

```text
http://localhost:8000
```

## 第三步：上传到 GitHub

建议仓库名：

```text
game-map-helper
```

把整个文件夹里的文件上传到仓库根目录。

## 第四步：开启 GitHub Pages

进入 GitHub 仓库：

```text
Settings → Pages → Build and deployment → Source: Deploy from a branch
```

然后选择：

```text
Branch: main
Folder: /root
```

保存后等待部署完成。

部署成功后，访问地址一般是：

```text
https://你的GitHub用户名.github.io/game-map-helper/
```

## iPhone 使用

用 Safari 打开部署地址，然后：

```text
分享 → 添加到主屏幕
```

之后桌面上就会出现“地图助手”图标。

## 修改地图列表

地图列表在 `app.js` 顶部的 `MAPS` 数组中。

例如：

```js
{ dir: "北", name: "北-1门", thumb: "01_北-1门.jpg", detail: "北-1门.jpg" }
```

含义：

- `dir`：所属方向
- `name`：界面显示名
- `thumb`：缩略图文件名
- `detail`：详细图文件名
