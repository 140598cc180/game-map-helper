const MAPS = [
  {
    "dir": "北",
    "name": "北-1门",
    "thumb": "北门/t1-北-1门.jpg",
    "detail": "北门/1-北-1门.jpg"
  },
  {
    "dir": "北",
    "name": "北-1沙发门",
    "thumb": "北门/t2-北-1沙发门.png",
    "detail": "北门/2-北-1沙发门.png"
  },
  {
    "dir": "北",
    "name": "北-4安全门",
    "thumb": "北门/t3-北-4安全门.png",
    "detail": "北门/3-北-4安全门.png"
  },
  {
    "dir": "北",
    "name": "北-4门",
    "thumb": "北门/t4-北-4门.jpg",
    "detail": "北门/4-北-4门.jpg"
  },
  {
    "dir": "北",
    "name": "北-T门",
    "thumb": "北门/t5-北-T门.jpg",
    "detail": "北门/5-北-T门.jpg"
  },
  {
    "dir": "北",
    "name": "北-凹门",
    "thumb": "北门/t6-北-凹门.jpg",
    "detail": "北门/6-北-凹门.jpg"
  },
  {
    "dir": "北",
    "name": "北-红对角门",
    "thumb": "北门/t7-北-红对角门.jpg",
    "detail": "北门/7-北-红对角门.jpg"
  },
  {
    "dir": "北",
    "name": "北-红门",
    "thumb": "北门/t8-北-红门.jpg",
    "detail": "北门/8-北-红门.jpg"
  },
  {
    "dir": "南",
    "name": "南-十字门",
    "thumb": "南门/t9-南-十字门.jpg",
    "detail": "南门/9-南-十字门.jpg"
  },
  {
    "dir": "南",
    "name": "南-三缺一门",
    "thumb": "南门/t10-南-三缺一门.jpg",
    "detail": "南门/10-南-三缺一门.jpg"
  },
  {
    "dir": "南",
    "name": "南-L门",
    "thumb": "南门/t11-南-L门.png",
    "detail": "南门/11-南-L门.png"
  },
  {
    "dir": "南",
    "name": "南-红门",
    "thumb": "南门/t12-南-红门.png",
    "detail": "南门/12-南-红门.png"
  },
  {
    "dir": "南",
    "name": "南-orz门",
    "thumb": "南门/t13-南-orz门.png",
    "detail": "南门/13-南-orz门.png"
  },
  {
    "dir": "左",
    "name": "左-锤子门",
    "thumb": "左门/t14-左-锤子门.png",
    "detail": "左门/14-左-锤子门.png"
  },
  {
    "dir": "左",
    "name": "左-倒T门",
    "thumb": "左门/t15-左-倒T门.jpg",
    "detail": "左门/15-左-倒T门.jpg"
  },
  {
    "dir": "左",
    "name": "左-对T门",
    "thumb": "左门/t16-左-对T门.png",
    "detail": "左门/16-左-对T门.png"
  },
  {
    "dir": "左",
    "name": "左-Y青蛙房",
    "thumb": "左门/t17-左-Y青蛙房.png",
    "detail": "左门/17-左-Y青蛙房.png"
  },
  {
    "dir": "左",
    "name": "左-对角门",
    "thumb": "左门/t18-左-对角门.png",
    "detail": "左门/18-左-对角门.png"
  },
  {
    "dir": "左",
    "name": "左-Y门",
    "thumb": "左门/t19-左-Y门.jpg",
    "detail": "左门/19-左-Y门.jpg"
  },
  {
    "dir": "左",
    "name": "左-锤灯笼门",
    "thumb": "左门/t20-左-锤灯笼门.png",
    "detail": "左门/20-左-锤灯笼门.png"
  },
  {
    "dir": "左",
    "name": "左-罐子门",
    "thumb": "左门/t21-左-罐子门.png",
    "detail": "左门/21-左-罐子门.png"
  },
  {
    "dir": "左",
    "name": "左-音叉门",
    "thumb": "左门/22-左-音叉门.jpg",
    "detail": "左门/22-左-音叉门.jpg"
  },
  {
    "dir": "右",
    "name": "右-左上右下门",
    "thumb": "右门/t23-右-左上右下门.jpg",
    "detail": "右门/23-右-左上右下门.jpg"
  },
  {
    "dir": "右",
    "name": "右-L门",
    "thumb": "右门/t24-右-L门.png",
    "detail": "右门/24-右-L门.png"
  },
  {
    "dir": "右",
    "name": "右-锤子门",
    "thumb": "右门/t25-右-锤子门.jpg",
    "detail": "右门/25-右-锤子门.jpg"
  },
  {
    "dir": "右",
    "name": "右-骑士门",
    "thumb": "右门/t26-右-骑士门.png",
    "detail": "右门/26-右-骑士门.png"
  },
  {
    "dir": "右",
    "name": "右-三L门",
    "thumb": "右门/t27-右-三L门.png",
    "detail": "右门/27-右-三L门.png"
  },
  {
    "dir": "右",
    "name": "右-双L门",
    "thumb": "右门/t28-右-双L门.jpg",
    "detail": "右门/28-右-双L门.jpg"
  }
];

const DIRS = [
  { key: "北", label: "北门" },
  { key: "右", label: "右门" },
  { key: "左", label: "左门" },
  { key: "南", label: "南门" },
];

const els = {
  main: document.getElementById("main"),
  title: document.getElementById("pageTitle"),
  subtitle: document.getElementById("pageSubtitle"),
  back: document.getElementById("backBtn"),
  install: document.getElementById("installBtn"),
  viewer: document.getElementById("viewer"),
  viewerClose: document.getElementById("viewerClose"),
  viewerTitle: document.getElementById("viewerTitle"),
  viewerStage: document.getElementById("viewerStage"),
  viewerImg: document.getElementById("viewerImg"),
  viewerReset: document.getElementById("viewerReset"),
};

let currentDir = null;

function thumbSrc(item) {
  return "./assets/thumbnails/" + item.thumb;
}

function detailSrc(item) {
  return "./assets/details/" + item.detail;
}

function renderHome() {
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
}

function renderCategory(dirKey, label) {
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
}

function openViewer(item) {
  els.viewerTitle.textContent = item.name;
  els.viewerImg.alt = item.name;
  els.viewerImg.onerror = function () {
    alert("详细图未找到：" + item.detail);
  };
  els.viewerImg.src = detailSrc(item);
  els.viewer.classList.remove("hidden");
  els.viewerStage.classList.remove("zoomed");
  document.body.style.overflow = "hidden";
}

function closeViewer() {
  els.viewer.classList.add("hidden");
  els.viewerImg.onerror = null;
  els.viewerImg.src = "";
  document.body.style.overflow = "";
}

function resetViewer() {
  els.viewerStage.classList.remove("zoomed");
  els.viewerStage.scrollTop = 0;
  els.viewerStage.scrollLeft = 0;
}

function toggleZoom() {
  els.viewerStage.classList.toggle("zoomed");
  if (!els.viewerStage.classList.contains("zoomed")) {
    resetViewer();
  }
}

els.back.addEventListener("click", renderHome);
els.viewerClose.addEventListener("click", closeViewer);
els.viewerReset.addEventListener("click", resetViewer);
els.viewerImg.addEventListener("dblclick", toggleZoom);

document.addEventListener("keydown", function (e) {
  if (e.key === "Escape" && !els.viewer.classList.contains("hidden")) {
    closeViewer();
  }
  if (e.key === "Backspace" && currentDir && els.viewer.classList.contains("hidden")) {
    renderHome();
  }
});

renderHome();
