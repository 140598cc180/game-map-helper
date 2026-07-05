# GitHub Pages 部署步骤

## 方式一：网页上传，最简单

1. 打开 GitHub，创建新仓库，例如 `game-map-helper`
2. 进入仓库，点击 `Add file → Upload files`
3. 把本项目里的全部文件拖进去
4. 点击 `Commit changes`
5. 进入 `Settings → Pages`
6. 在 `Build and deployment` 中选择：
   - Source: `Deploy from a branch`
   - Branch: `main`
   - Folder: `/root`
7. 点击 `Save`
8. 等部署完成后，访问：
   `https://你的用户名.github.io/game-map-helper/`

## 方式二：命令行上传

```bash
git init
git add .
git commit -m "init game map helper"
git branch -M main
git remote add origin https://github.com/你的用户名/game-map-helper.git
git push -u origin main
```

然后去 GitHub 仓库的 `Settings → Pages` 开启 Pages。

## 注意

- 文件名必须和 `app.js` 里的 `thumb`、`detail` 完全一致。
- GitHub Pages 默认大小写敏感，`北-1门.jpg` 和 `北-1门.JPG` 不是同一个文件。
- 图片不要太大，否则手机加载会慢。
