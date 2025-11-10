/* jshint esversion: 11, jquery: true */
/* globals document, window, Stripe */
'use strict';

/**
 * Adds a subtle hover animation effect to the newsletter CTA button.
 */
document.addEventListener('DOMContentLoaded', function () {
  const ctaButton = document.querySelector('.cta a');

  if (ctaButton) {
    ctaButton.addEventListener('mouseenter', function () {
      this.style.transform = 'scale(1.05)';
      this.style.transition = 'transform 0.2s ease-in-out';
    });

    ctaButton.addEventListener('mouseleave', function () {
      this.style.transform = 'scale(1)';
    });
  }
});
