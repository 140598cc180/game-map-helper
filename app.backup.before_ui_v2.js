const MAPS = [
  {
    "dir": "北",
    "name": "北-1门",
    "thumb": "thumb_01.jpg",
    "detail": "detail_01.jpg"
  },
  {
    "dir": "北",
    "name": "北-4门",
    "thumb": "thumb_02.jpg",
    "detail": "detail_02.jpg"
  },
  {
    "dir": "北",
    "name": "北-T门",
    "thumb": "thumb_03.jpg",
    "detail": "detail_03.jpg"
  },
  {
    "dir": "北",
    "name": "北-凹门",
    "thumb": "thumb_04.jpg",
    "detail": "detail_04.jpg"
  },
  {
    "dir": "北",
    "name": "北-红对角门",
    "thumb": "thumb_05.jpg",
    "detail": "detail_05.jpg"
  },
  {
    "dir": "北",
    "name": "北-红门",
    "thumb": "thumb_06.jpg",
    "detail": "detail_06.jpg"
  },
  {
    "dir": "南",
    "name": "南-L门",
    "thumb": "thumb_07.jpg",
    "detail": "detail_07.jpg"
  },
  {
    "dir": "南",
    "name": "南-红门",
    "thumb": "thumb_08.png",
    "detail": "detail_08.png"
  },
  {
    "dir": "南",
    "name": "南-三缺一门",
    "thumb": "thumb_09.jpg",
    "detail": "detail_09.jpg"
  },
  {
    "dir": "南",
    "name": "南-十字门",
    "thumb": "thumb_10.jpg",
    "detail": "detail_10.jpg"
  },
  {
    "dir": "右",
    "name": "右-L门",
    "thumb": "thumb_11.png",
    "detail": "detail_11.png"
  },
  {
    "dir": "右",
    "name": "右-锤子门",
    "thumb": "thumb_12.jpg",
    "detail": "detail_12.jpg"
  },
  {
    "dir": "右",
    "name": "右-骑士门",
    "thumb": "thumb_13.png",
    "detail": "detail_13.png"
  },
  {
    "dir": "右",
    "name": "右-双L门",
    "thumb": "thumb_14.jpg",
    "detail": "detail_14.jpg"
  },
  {
    "dir": "右",
    "name": "右-左上右下门",
    "thumb": "thumb_15.jpg",
    "detail": "detail_15.jpg"
  },
  {
    "dir": "左",
    "name": "左-Y门",
    "thumb": "thumb_16.jpg",
    "detail": "detail_16.jpg"
  },
  {
    "dir": "左",
    "name": "左-锤子门",
    "thumb": "thumb_17.jpg",
    "detail": "detail_17.jpg"
  },
  {
    "dir": "左",
    "name": "左-倒T门",
    "thumb": "thumb_18.jpg",
    "detail": "detail_18.jpg"
  },
  {
    "dir": "左",
    "name": "左-对T门",
    "thumb": "thumb_19.png",
    "detail": "detail_19.png"
  },
  {
    "dir": "左",
    "name": "左-对角门",
    "thumb": "thumb_20.png",
    "detail": "detail_20.png"
  },
  {
    "dir": "左",
    "name": "左-罐子门",
    "thumb": "thumb_21.png",
    "detail": "detail_21.png"
  },
  {
    "dir": "左",
    "name": "左-音叉门",
    "thumb": "thumb_22.jpg",
    "detail": "detail_22.jpg"
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
  els.title.textContent = "第五人格地图助手";
  els.subtitle.textContent = "固定地图路线速查｜选择方向进入";
  els.back.classList.add("hidden");

  const grid = document.createElement("div");
  grid.className = "home-grid";

  for (const dir of DIRS) {
    const count = MAPS.filter(item => item.dir === dir.key).length;
    const btn = document.createElement("button");
    btn.className = "direction-card";
    btn.innerHTML =
      '<span class="direction-title">' + dir.label + '</span>' +
      '<span class="direction-count">' + count + ' 张地图路线</span>';
    btn.addEventListener("click", function () {
      renderCategory(dir.key, dir.label);
    });
    grid.appendChild(btn);
  }

  const info = document.createElement("section");
  info.className = "home-info-card";
  info.innerHTML =
    '<div class="home-info-title">主要信息</div>' +
    '<div class="home-info-text">选择门的方向后，点击地图缩略图查看完整路线图。绿色三角为入口，红线为主要路线，蓝色数字为推荐检查顺序。</div>' +
    '<div class="home-meta-grid">' +
      '<div><span>作者</span><strong>cici吃饱饱</strong></div>' +
      '<div><span>第五人格 ID</span><strong>nku守门员</strong></div>' +
      '<div><span>问题联系</span><strong>jayceja817@gmail.com</strong></div>' +
    '</div>' +
    '<div class="home-notice">' +
      '声明：本工具仅供个人自用与学习交流，不用于任何商业用途。地图资料借鉴了 B 站 UP 主“凉哈皮”的相关图片内容，并在此基础上进行个人整理与路线标注。自制整理不易，请勿肆意传播或用于商业转载；如有不妥，请通过上方邮箱联系处理。' +
    '</div>';

  els.main.replaceChildren(grid, info);
}

function renderCategory(dirKey, label) {
  currentDir = dirKey;
  els.title.textContent = label;
  els.subtitle.textContent = "点击缩略图查看完整详细图";
  els.back.classList.remove("hidden");

  const list = MAPS.filter(item => item.dir === dirKey);
  const grid = document.createElement("div");
  grid.className = "map-grid";

  for (const item of list) {
    const card = document.createElement("button");
    card.className = "map-card";
    card.setAttribute("aria-label", "查看" + item.name);

    const wrap = document.createElement("div");
    wrap.className = "thumb-wrap";

    const img = document.createElement("img");
    img.loading = "lazy";
    img.alt = item.name;
    img.src = thumbSrc(item);

    img.onerror = function () {
      wrap.innerHTML = '<div class="missing-img">缩略图未找到<br>' + item.thumb + '</div>';
    };

    wrap.appendChild(img);

    const name = document.createElement("div");
    name.className = "map-name";
    name.textContent = item.name;

    card.append(wrap, name);
    card.addEventListener("click", function () {
      openViewer(item);
    });
    grid.appendChild(card);
  }

  els.main.replaceChildren(grid);
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
