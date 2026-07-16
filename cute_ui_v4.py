# -*- coding: utf-8 -*-
from pathlib import Path
import re, shutil, datetime

ROOT = Path(__file__).resolve().parent
APP = ROOT / 'app.js'
CSS = ROOT / 'style.css'
HTML = ROOT / 'index.html'
MANIFEST = ROOT / 'manifest.json'

HOME = r'''function renderHome() {
  currentDir = null;
  els.title.textContent = "地图小助手";
  els.subtitle.textContent = "选一个方向出发吧 ✨";
  els.back.classList.add("hidden");

  const meta = {
    "北": ["🧭", "pink"],
    "右": ["➡️", "purple"],
    "左": ["⬅️", "mint"],
    "南": ["🔻", "peach"]
  };

  const page = document.createElement("section");
  page.className = "cute-home";

  const hero = document.createElement("section");
  hero.className = "cute-hero";
  hero.innerHTML =
    '<div class="cute-kicker">🎮 Identity V Map Helper</div>' +
    '<h2>第五人格地图路线速查</h2>' +
    '<p>选择门的方向，快速查看入口、路线与检查顺序。</p>' +
    '<div class="cute-tips"><span>🟢 入口</span><span>🔴 路线</span><span>🔵 顺序</span></div>';

  const grid = document.createElement("div");
  grid.className = "cute-dir-grid";
  for (const dir of DIRS) {
    const count = MAPS.filter(item => item.dir === dir.key).length;
    const m = meta[dir.key] || ["📍", "pink"];
    const btn = document.createElement("button");
    btn.className = "cute-dir-card cute-" + m[1];
    btn.innerHTML =
      '<span class="cute-dir-icon">' + m[0] + '</span>' +
      '<span class="cute-dir-name">' + dir.label + '</span>' +
      '<span class="cute-dir-count">' + count + ' 张地图</span>' +
      '<span class="cute-dir-go">进入 →</span>';
    btn.addEventListener("click", function () { renderCategory(dir.key, dir.label); });
    grid.appendChild(btn);
  }

  const author = document.createElement("section");
  author.className = "cute-author";
  author.innerHTML =
    '<div class="cute-avatar-box">' +
      '<img class="cute-avatar" src="./assets/avatar.png" alt="作者头像">' +
      '<div class="cute-avatar-fallback">🍚</div>' +
    '</div>' +
    '<div class="cute-author-copy">' +
      '<div class="cute-author-label">🌷 关于作者</div>' +
      '<div class="cute-author-name">cici吃饱饱</div>' +
      '<div class="cute-author-id">第五人格 ID：nku守门员</div>' +
      '<div class="cute-author-tags"><span>🗺️ 原创地图整理</span><span>✏️ 原创路线标注</span><span>✨ AI 辅助增强</span></div>' +
      '<a href="mailto:jayceja817@gmail.com" class="cute-mail">📮 jayceja817@gmail.com</a>' +
    '</div>' +
    '<div class="cute-note"><strong>原创说明</strong><p>本工具中的地图整理、路线规划、界面设计与标注内容均为原创制作，部分图片与视觉效果使用 AI 辅助增强。仅供个人自用与学习交流，不用于商业用途。未经允许，请勿搬运、转载或用于商业传播。</p></div>';

  const avatar = author.querySelector(".cute-avatar");
  const fallback = author.querySelector(".cute-avatar-fallback");
  avatar.addEventListener("load", () => fallback.style.display = "none");
  avatar.addEventListener("error", () => { avatar.style.display = "none"; fallback.style.display = "grid"; });

  page.append(hero, grid, author);
  els.main.replaceChildren(page);
}'''

CATEGORY = r'''function renderCategory(dirKey, label) {
  currentDir = dirKey;
  const meta = {
    "北": ["🧭", "pink"],
    "右": ["➡️", "purple"],
    "左": ["⬅️", "mint"],
    "南": ["🔻", "peach"]
  };
  const m = meta[dirKey] || ["📍", "pink"];
  const list = MAPS.filter(item => item.dir === dirKey);

  els.title.textContent = m[0] + " " + label;
  els.subtitle.textContent = "点击缩略图查看完整路线";
  els.back.classList.remove("hidden");

  const page = document.createElement("section");
  page.className = "cute-category";

  const head = document.createElement("section");
  head.className = "cute-cat-head cute-" + m[1];
  head.innerHTML =
    '<div class="cute-cat-icon">' + m[0] + '</div>' +
    '<div><div class="cute-cat-title">' + label + '</div><div class="cute-cat-sub">共 ' + list.length + ' 张地图</div></div>' +
    '<div class="cute-cat-legend">🟢入口　🔴路线　🔵顺序</div>';

  const grid = document.createElement("div");
  grid.className = "cute-map-grid";
  list.forEach(function (item, i) {
    const card = document.createElement("button");
    card.className = "cute-map-card";
    const thumb = document.createElement("div");
    thumb.className = "cute-thumb";
    const img = document.createElement("img");
    img.loading = "lazy";
    img.alt = item.name;
    img.src = thumbSrc(item);
    img.onerror = function () { thumb.innerHTML = '<div class="missing-img">图片未找到</div>'; };
    thumb.appendChild(img);
    const info = document.createElement("div");
    info.className = "cute-map-info";
    info.innerHTML = '<span class="cute-map-no">' + String(i + 1).padStart(2, "0") + '</span><span class="cute-map-title">' + item.name + '</span><span>↗</span>';
    card.append(thumb, info);
    card.addEventListener("click", function () { openViewer(item); });
    grid.appendChild(card);
  });

  page.append(head, grid);
  els.main.replaceChildren(page);
}'''

STYLE = r'''
/* ===== Cute UI v4 ===== */
:root {
  --cute-ink:#5d5368; --cute-muted:#8e8398;
  --cute-pink:#ffe2ef; --cute-purple:#ece6ff;
  --cute-mint:#dff8ef; --cute-peach:#ffeadc;
}
body {
  color:var(--cute-ink) !important;
  background:
    radial-gradient(circle at 8% 8%,rgba(255,159,199,.25),transparent 24rem),
    radial-gradient(circle at 92% 14%,rgba(184,160,255,.22),transparent 22rem),
    radial-gradient(circle at 50% 100%,rgba(141,223,200,.19),transparent 25rem),
    linear-gradient(180deg,#fff8fb,#f8f5ff) !important;
}
.topbar { background:rgba(255,250,253,.76)!important; border-bottom:1px solid rgba(194,173,207,.28)!important; backdrop-filter:blur(16px); }
#pageTitle{color:#5d5368!important;text-shadow:none!important}.icon-btn,.install-btn{color:#6e6379!important;background:#fff!important;border-color:rgba(185,165,201,.35)!important}
.cute-home,.cute-category{display:grid;gap:13px}
.cute-hero{padding:18px;border:2px solid rgba(255,159,199,.32);border-radius:26px;background:linear-gradient(135deg,rgba(255,226,239,.97),rgba(236,230,255,.93));box-shadow:0 18px 42px rgba(108,80,112,.13)}
.cute-kicker{display:inline-flex;padding:5px 10px;border-radius:999px;background:rgba(255,255,255,.72);color:#98748c;font-size:11px;font-weight:900}
.cute-hero h2{margin:11px 0 0;font-size:clamp(25px,6vw,40px);line-height:1.08;letter-spacing:-.05em}.cute-hero p{margin:7px 0 0;color:#786e82;font-size:13px}.cute-tips{display:flex;flex-wrap:wrap;gap:6px;margin-top:11px}.cute-tips span{padding:5px 8px;border-radius:999px;background:rgba(255,255,255,.72);font-size:10px;font-weight:800}
.cute-dir-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px}.cute-dir-card{position:relative;min-height:128px;padding:12px;border:2px solid transparent;border-radius:23px;color:#5d5368;text-align:left;box-shadow:0 13px 29px rgba(108,80,112,.11)}.cute-dir-card:active{transform:scale(.98)}
.cute-pink{background:linear-gradient(145deg,#fff8fb,var(--cute-pink))!important;border-color:rgba(255,159,199,.45)!important}.cute-purple{background:linear-gradient(145deg,#fcfaff,var(--cute-purple))!important;border-color:rgba(184,160,255,.45)!important}.cute-mint{background:linear-gradient(145deg,#f9fffd,var(--cute-mint))!important;border-color:rgba(141,223,200,.48)!important}.cute-peach{background:linear-gradient(145deg,#fffaf6,var(--cute-peach))!important;border-color:rgba(255,189,143,.5)!important}
.cute-dir-icon{display:grid;place-items:center;width:38px;height:38px;border-radius:14px;background:rgba(255,255,255,.76);font-size:21px}.cute-dir-name{display:block;margin-top:8px;font-size:30px;font-weight:1000;line-height:1}.cute-dir-count{display:inline-flex;margin-top:7px;padding:4px 8px;border-radius:999px;background:rgba(255,255,255,.72);font-size:10px;font-weight:900}.cute-dir-go{position:absolute;right:10px;bottom:9px;font-size:10px;font-weight:900;color:#8d8097}
.cute-author{display:grid;grid-template-columns:82px 1fr;gap:12px;padding:14px;border:2px solid rgba(184,160,255,.3);border-radius:24px;background:rgba(255,255,255,.84);box-shadow:0 15px 36px rgba(104,79,112,.1)}.cute-avatar-box,.cute-avatar,.cute-avatar-fallback{width:82px;height:82px}.cute-avatar,.cute-avatar-fallback{border:4px solid #fff;border-radius:25px;box-shadow:0 9px 22px rgba(103,77,112,.15)}.cute-avatar{display:block;object-fit:cover}.cute-avatar-fallback{display:none;place-items:center;background:linear-gradient(145deg,#ffe2ef,#ece6ff);font-size:34px}.cute-author-label{font-size:11px;font-weight:900;color:#a16e8d}.cute-author-name{margin-top:2px;font-size:20px;font-weight:1000}.cute-author-id{margin-top:2px;font-size:11px;color:#85798d;font-weight:700}.cute-author-tags{display:flex;flex-wrap:wrap;gap:5px;margin-top:7px}.cute-author-tags span{padding:4px 7px;border-radius:999px;background:#faf3ff;font-size:9px;font-weight:800}.cute-mail{display:inline-flex;margin-top:7px;color:#a46184;font-size:10px;font-weight:900;text-decoration:none;word-break:break-all}.cute-note{grid-column:1/-1;border-top:1px dashed rgba(166,137,177,.28);padding-top:9px}.cute-note strong{font-size:10px;color:#8f6782}.cute-note p{margin:3px 0 0;font-size:9px;line-height:1.55;color:#887d90}
.cute-cat-head{display:grid;grid-template-columns:46px 1fr;gap:9px;align-items:center;padding:10px;border:2px solid rgba(255,159,199,.28);border-radius:21px;box-shadow:0 12px 26px rgba(105,80,112,.1)}.cute-cat-icon{display:grid;place-items:center;width:46px;height:46px;border-radius:16px;background:rgba(255,255,255,.73);font-size:25px}.cute-cat-title{font-size:22px;font-weight:1000}.cute-cat-sub{margin-top:2px;font-size:10px;color:#83778b}.cute-cat-legend{grid-column:1/-1;padding:5px 8px;border-radius:999px;background:rgba(255,255,255,.65);font-size:9px;font-weight:800;text-align:center}
.cute-map-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px}.cute-map-card{overflow:hidden;padding:0;border:2px solid rgba(201,181,215,.27);border-radius:16px;color:#5d5368;background:rgba(255,255,255,.85);box-shadow:0 9px 21px rgba(104,79,112,.09)}.cute-map-card:active{transform:scale(.98)}.cute-thumb{width:100%;aspect-ratio:1/1;overflow:hidden;background:#fffafd}.cute-thumb img{width:100%;height:100%;object-fit:contain;object-position:center}.cute-map-info{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:4px;align-items:center;padding:4px 5px 5px}.cute-map-no{min-width:21px;height:18px;display:inline-grid;place-items:center;border-radius:999px;background:#ffe9f2;color:#8e6b84;font-size:8px;font-weight:1000}.cute-map-title{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:9px;font-weight:900}
.viewer{background:rgba(75,59,80,.88)!important}.viewer-toolbar{background:rgba(255,247,251,.94)!important}.viewer-title{color:#5d5368!important}.viewer-btn{color:#6e6379!important;background:#fff!important;border-color:rgba(185,165,201,.38)!important}
.battle-home,.battle-category,.compact-home,.compact-category,.hero-card,.home-info-card-v2,.category-summary,.map-grid-v2{display:none!important}
@media(min-width:760px){.cute-dir-grid{grid-template-columns:repeat(4,minmax(0,1fr))}.cute-map-grid{grid-template-columns:repeat(auto-fit,minmax(120px,1fr))}}
@media(max-width:430px){.cute-hero{padding:14px;border-radius:22px}.cute-dir-card{min-height:118px;border-radius:20px;padding:10px}.cute-dir-name{font-size:27px}.cute-author{grid-template-columns:68px 1fr;padding:11px;gap:9px}.cute-avatar-box,.cute-avatar,.cute-avatar-fallback{width:68px;height:68px;border-radius:21px}.cute-author-name{font-size:17px}.cute-map-title{font-size:8px}}
@media(max-height:680px){.cute-hero p{display:none}.cute-dir-card{min-height:104px}.cute-note{display:none}}
'''

def backup(path, tag):
    if path.exists():
        dst = ROOT / f'{path.stem}.backup.before_{tag}_{datetime.datetime.now():%Y%m%d_%H%M%S}{path.suffix}'
        shutil.copy2(path, dst)

def patch_app():
    if not APP.exists(): raise RuntimeError('没有找到 app.js')
    text = APP.read_text(encoding='utf-8')
    backup(APP, 'cute_ui')
    text, n1 = re.subn(r'function renderHome\(\)\s*\{.*?\n\}\n\nfunction renderCategory', HOME+'\n\nfunction renderCategory', text, count=1, flags=re.S)
    text, n2 = re.subn(r'function renderCategory\(dirKey,\s*label\)\s*\{.*?\n\}\n\nfunction openViewer', CATEGORY+'\n\nfunction openViewer', text, count=1, flags=re.S)
    if not n1 or not n2: raise RuntimeError('没有定位到 renderHome / renderCategory')
    APP.write_text(text, encoding='utf-8')

def patch_css():
    if not CSS.exists(): raise RuntimeError('没有找到 style.css')
    text = CSS.read_text(encoding='utf-8')
    backup(CSS, 'cute_ui')
    if '/* ===== Cute UI v4 ===== */' not in text:
        CSS.write_text(text.rstrip()+'\n\n'+STYLE+'\n', encoding='utf-8')

def patch_html():
    if not HTML.exists(): return
    text = HTML.read_text(encoding='utf-8')
    backup(HTML, 'cute_ui')
    text = text.replace('<title>游戏地图助手</title>', '<title>第五人格地图小助手</title>').replace('<title>第五人格地图助手</title>', '<title>第五人格地图小助手</title>')
    text = re.sub(r'<meta\s+name="theme-color"\s+content="[^"]*"\s*/?>', '<meta name="theme-color" content="#fff1f7">', text)
    text = re.sub(r'<script\s+src="\./app\.js(?:\?[^"]*)?"></script>', '<script src="./app.js?v=cute-ui-v4"></script>', text)
    HTML.write_text(text, encoding='utf-8')

def patch_manifest():
    if not MANIFEST.exists(): return
    text = MANIFEST.read_text(encoding='utf-8')
    backup(MANIFEST, 'cute_ui')
    text = re.sub(r'"theme_color"\s*:\s*"[^"]*"', '"theme_color": "#fff1f7"', text)
    text = re.sub(r'"background_color"\s*:\s*"[^"]*"', '"background_color": "#fff8fb"', text)
    MANIFEST.write_text(text, encoding='utf-8')

def main():
    patch_app(); patch_css(); patch_html(); patch_manifest()
    avatar = ROOT / 'assets' / 'avatar.png'
    print('[OK] 可爱风界面已更新')
    print('[INFO] 头像路径：assets/avatar.png')
    print('[INFO] 当前头像：' + ('已找到' if avatar.exists() else '尚未放入，将显示 🍚 占位图'))
    print('预览：python -m http.server 8008')
    print('打开：http://localhost:8008/index.html?v=cute4')
    print('上传：git add . && git commit -m "update cute ui and author profile" && git push')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('[ERROR]', e)
        input('按回车退出...')
