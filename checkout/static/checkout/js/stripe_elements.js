/*
  Mount Stripe Card Element.
  Works even if client_secret is null (you’ll still see the card input).
*/
(function () {
  // Safely read JSON-script tag values
  function getJson(id) {
    var el = document.getElementById(id);
    if (!el) return null;
    var t = (el.textContent || '').trim();
    if (!t || t === 'null') return null;
    try { return JSON.parse(t); } catch (e) {
      // fallback if the value is a quoted string
      return t.replace(/^"|"$/g, '');
    }
  }

  function init() {
    var pubKey = getJson('id_stripe_public_key');
    if (!pubKey) {
      console.error('Stripe public key missing.');
      return;
    }
    if (!window.Stripe) {
      console.error('Stripe.js failed to load.');
      return;
    }

    var stripe = Stripe(pubKey);
    var elements = stripe.elements();

    var style = {
      base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': { color: '#aab7c4' },
      },
      invalid: { color: '#dc3545', iconColor: '#dc3545' },
    };

    var card = elements.create('card', { style: style });

    var container = document.getElementById('card-element');
    if (!container) {
      console.error('#card-element not found.');
      return;
    }

    // Mount the Stripe iframe
    card.mount('#card-element');


// Handle realtime validation errors on the card element
card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';        
    }
});