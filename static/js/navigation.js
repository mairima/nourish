// static/js/navigation.js
// Handles navigation actions like going back to the previous page

document.addEventListener("DOMContentLoaded", () => {
  const backButtons = document.querySelectorAll(".btn-back");

  backButtons.forEach((button) => {
    button.addEventListener("click", () => {
      if (window.history.length > 1) {
        window.history.back();
      } else {
        // fallback if no history
        window.location.href = "/";
      }
    });
  });
});
