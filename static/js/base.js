// static/js/base.js

/**
 * Handles toast notifications positioning and display
 * Ensures they appear below the fixed navbar
 */
(function () {
  function placeToast() {
    const header = document.querySelector("header.container-fluid.fixed-top");
    const mc = document.querySelector(".message-container");
    if (!header || !mc) return;
    mc.style.top = header.offsetHeight + 10 + "px";
  }

  function showToasts() {
    const toasts = document.querySelectorAll(".toast");
    if (!toasts.length) return;
    try {
      if (window.jQuery && typeof jQuery.fn.toast === "function") {
        jQuery(toasts).toast({ autohide: false }).toast("show");
      } else {
        toasts.forEach((t) => t.classList.add("show"));
      }
    } catch (e) {
      toasts.forEach((t) => t.classList.add("show"));
    }
  }

  function initToasts() {
    placeToast();
    showToasts();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initToasts);
  } else {
    initToasts();
  }

  window.addEventListener("resize", placeToast);
})();

// Set CSS var to header height so pages can offset correctly
window.addEventListener('load', () => {
  const header = document.querySelector('header.container-fluid.fixed-top');
  if (header) {
    document.documentElement.style.setProperty('--header-height', header.offsetHeight + 'px');
  }
});
