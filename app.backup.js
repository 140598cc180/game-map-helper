const MAPS = [
  { dir: "北", name: "北-1门", thumb: "01_北-1门.jpg", detail: "北-1门.jpg" },
  { dir: "北", name: "北-4门", thumb: "02_北-4门.jpg", detail: "北-4门.jpg" },
  { dir: "北", name: "北-T门", thumb: "03_北-T门.jpg", detail: "北-T门.jpg" },
  { dir: "北", name: "北-凹门", thumb: "04_北-凹门.jpg", detail: "北-凹门.jpg" },
  { dir: "北", name: "北-红对角门", thumb: "05_北-红对角门.jpg", detail: "北-红对角门.jpg" },
  { dir: "北", name: "北-红门", thumb: "06_北-红门.jpg", detail: "北-红门.jpg" },

  { dir: "南", name: "南-L门", thumb: "07_南-L门.jpg", detail: "南-L门.jpg" },
  { dir: "南", name: "南-红门", thumb: "08_南-红门.png", detail: "南-红门.png" },
  { dir: "南", name: "南-三缺一门", thumb: "09_南-三缺一门.jpg", detail: "南-三缺一门.jpg" },
  { dir: "南", name: "南-十字门", thumb: "10_南-十字门.jpg", detail: "南-十字门.jpg" },

  { dir: "右", name: "右-L门", thumb: "11_右-L门.png", detail: "右-L门.png" },
  { dir: "右", name: "右-锤子门", thumb: "12_右-锤子门.jpg", detail: "右-锤子门.jpg" },
  { dir: "右", name: "右-骑士门", thumb: "13_右-骑士门.png", detail: "右-骑士门.png" },
  { dir: "右", name: "右-双L门", thumb: "14_右-双L门.jpg", detail: "右-双L门.jpg" },
  { dir: "右", name: "右-左上右下门", thumb: "15_右-左上右下门.jpg", detail: "右-左上右下门.jpg" },

  { dir: "左", name: "左-Y门", thumb: "16_左-Y门.jpg", detail: "左-Y门.jpg" },
  { dir: "左", name: "左-锤子门", thumb: "17_左-锤子门.jpg", detail: "左-锤子门.jpg" },
  { dir: "左", name: "左-倒T门", thumb: "18_左-倒T门.jpg", detail: "左-倒T门.jpg" },
  { dir: "左", name: "左-对T门", thumb: "19_左-对门.png", detail: "左-对T门.png" },
  { dir: "左", name: "左-对角门", thumb: "20_左-对角门.png", detail: "左-对角门.png" },
  { dir: "左", name: "左-罐子门", thumb: "21_左-罐子门.png", detail: "左-罐子门.png" },
  { dir: "左", name: "左-音叉门", thumb: "22_左-音叉门.jpg", detail: "左-音叉门.jpg" },
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
let deferredPrompt = null;

function asset(path) {
  return `./assets/${path}`;
}

function thumbSrc(item) {
  return `./assets/thumbnails/${item.thumb}`;
}

function detailSrc(item) {
  return `./assets/details/${item.detail}`;
}

function renderHome() {
  currentDir = null;
  els.title.textContent = "游戏地图助手";
  els.subtitle.textContent = "选择方向后查看对应地图";
  els.back.classList.add("hidden");

  const grid = document.createElement("div");
  grid.className = "home-grid";

  for (const dir of DIRS) {
    const count = MAPS.filter(item => item.dir === dir.key).length;
    const btn = document.createElement("button");
    btn.className = "direction-card";
    btn.innerHTML = `
      <span class="direction-title">${dir.label}</span>
      <span class="direction-count">${count} 张地图</span>
    `;
    btn.addEventListener("click", () => renderCategory(dir.key, dir.label));
    grid.appendChild(btn);
  }

  const tip = document.createElement("div");
  tip.className = "tip-card";
  tip.innerHTML = `
    苹果手机 Safari 打开 GitHub Pages 地址后，可以点“分享 → 添加到主屏幕”，以后就像 App 一样打开。
    <br />
    部署后如果某张图不显示，通常是文件名或扩展名没有完全对应。
  `;

  els.main.replaceChildren(grid, tip);
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
    card.setAttribute("aria-label", `查看${item.name}`);

    const wrap = document.createElement("div");
    wrap.className = "thumb-wrap";

    const img = document.createElement("img");
    img.loading = "lazy";
    img.alt = item.name;
    img.src = thumbSrc(item);

    img.onerror = () => {
      wrap.innerHTML = `<div class="missing-img">缩略图未找到<br>${item.thumb}</div>`;
    };

    wrap.appendChild(img);

    const name = document.createElement("div");
    name.className = "map-name";
    name.textContent = item.name;

    card.append(wrap, name);
    card.addEventListener("click", () => openViewer(item));
    grid.appendChild(card);
  }

  els.main.replaceChildren(grid);
}

function openViewer(item) {
  els.viewerTitle.textContent = item.name;
  els.viewerImg.alt = item.name;
  els.viewerImg.src = detailSrc(item);
  els.viewer.classList.remove("hidden");
  els.viewerStage.classList.remove("zoomed");
  document.body.style.overflow = "hidden";

  els.viewerImg.onerror = () => {
    alert(`详细图未找到：${item.detail}\n\n请检查 assets/details 文件夹中的文件名是否完全一致。`);
  };
}

function closeViewer() {
  els.viewer.classList.add("hidden");
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

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && !els.viewer.classList.contains("hidden")) {
    closeViewer();
  }
  if (e.key === "Backspace" && currentDir && els.viewer.classList.contains("hidden")) {
    renderHome();
  }
});

window.addEventListener("beforeinstallprompt", (e) => {
  e.preventDefault();
  deferredPrompt = e;
  els.install.classList.remove("hidden");
});

els.install.addEventListener("click", async () => {
  if (!deferredPrompt) return;
  deferredPrompt.prompt();
  await deferredPrompt.userChoice;
  deferredPrompt = null;
  els.install.classList.add("hidden");
});

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("./service-worker.js").catch(() => {});
  });
}

renderHome();
