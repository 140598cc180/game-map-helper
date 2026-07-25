(() => {
  document.documentElement.classList.add("android-apk");

  document.addEventListener(
    "contextmenu",
    (event) => {
      if (event.target instanceof HTMLImageElement) {
        event.preventDefault();
      }
    },
    { passive: false }
  );
})();
