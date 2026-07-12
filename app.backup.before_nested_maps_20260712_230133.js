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
  els.title.textContent = "地图速查";
  els.subtitle.textContent = "选择方向";
  els.back.classList.add("hidden");

  const meta = {
    "北": ["🧭", "北门"],
    "右": ["➡️", "右门"],
    "左": ["⬅️", "左门"],
    "南": ["🔻", "南门"]
  };

  const wrap = document.createElement("section");
  wrap.className = "battle-home";

  const title = document.createElement("div");
  title.className = "battle-title";
  title.innerHTML =
    '<div class="battle-title-main">🎮 第五人格地图助手</div>' +
    '<div class="battle-title-sub">🟢入口　🔴路线　🔵顺序</div>';

  const grid = document.createElement("div");
  grid.className = "battle-dir-grid";

  for (const dir of DIRS) {
    const count = MAPS.filter(item => item.dir === dir.key).length;
    const m = meta[dir.key] || ["📍", dir.label];
    const btn = document.createElement("button");
    btn.className = "battle-dir-btn";
    btn.innerHTML =
      '<span class="battle-dir-emoji">' + m[0] + '</span>' +
      '<span class="battle-dir-name">' + dir.label + '</span>' +
      '<span class="battle-dir-count">' + count + ' 张</span>';
    btn.addEventListener("click", function () {
      renderCategory(dir.key, dir.label);
    });
    grid.appendChild(btn);
  }

  const info = document.createElement("div");
  info.className = "battle-info";
  info.innerHTML =
    '<div>作者：cici吃饱饱｜第五人格ID：nku守门员</div>' +
    '<div>仅个人自用，非商业用途；借鉴 B 站 UP 主“凉哈皮”的图，自制不易请勿肆意传播。</div>' +
    '<div>联系：jayceja817@gmail.com</div>';

  wrap.append(title, grid, info);
  els.main.replaceChildren(wrap);
}

function renderCategory(dirKey, label) {
  currentDir = dirKey;
  const emoji = { "北": "🧭", "右": "➡️", "左": "⬅️", "南": "🔻" }[dirKey] || "📍";

  els.title.textContent = emoji + " " + label;
  els.subtitle.textContent = "点图打开";
  els.back.classList.remove("hidden");

  const list = MAPS.filter(item => item.dir === dirKey);
  const wrap = document.createElement("section");
  wrap.className = "battle-category";

  const head = document.createElement("div");
  head.className = "battle-cat-head";
  head.innerHTML =
    '<div class="battle-cat-title">' + emoji + ' ' + label + '</div>' +
    '<div class="battle-cat-rule">🟢入口 🔴路线 🔵顺序</div>' +
    '<div class="battle-cat-count">' + list.length + '张</div>';

  const grid = document.createElement("div");
  grid.className = "battle-map-grid";

  for (let i = 0; i < list.length; i++) {
    const item = list[i];
    const card = document.createElement("button");
    card.className = "battle-map-card";
    card.setAttribute("aria-label", "查看" + item.name);

    const imgBox = document.createElement("div");
    imgBox.className = "battle-thumb";

    const img = document.createElement("img");
    img.loading = "lazy";
    img.alt = item.name;
    img.src = thumbSrc(item);
    img.onerror = function () {
      imgBox.innerHTML = '<div class="missing-img">图未找到<br>' + item.thumb + '</div>';
    };
    imgBox.appendChild(img);

    const name = document.createElement("div");
    name.className = "battle-map-name";
    name.innerHTML =
      '<span class="battle-map-no">' + String(i + 1).padStart(2, "0") + '</span>' +
      '<span class="battle-map-title">' + item.name + '</span>';

    card.append(imgBox, name);
    card.addEventListener("click", function () {
      openViewer(item);
    });
    grid.appendChild(card);
  }

  wrap.append(head, grid);
  els.main.replaceChildren(wrap);
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
