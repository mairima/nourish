/* jshint esversion: 11 */
/* globals document, window */
'use strict';

/**
 * Handles navigation actions like going back to the previous page.
 */
document.addEventListener('DOMContentLoaded', () => {
  const backButtons = document.querySelectorAll('.btn-back');

  backButtons.forEach((button) => {
    button.addEventListener('click', () => {
      if (window.history.length > 1) {
        window.history.back();
      } else {
        // Fallback if no history available
        window.location.href = '/';
      }
    });
  });
});
