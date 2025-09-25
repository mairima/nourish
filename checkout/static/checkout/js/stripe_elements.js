/*
    Accept a card payment with a confirm step

    Based on Stripe’s accept-a-payment guide:
    https://stripe.com/docs/payments/accept-a-payment
*/

(function () {
  // --- Read keys the same way as the walkthrough ---
  var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
  var clientSecret    = $('#id_client_secret').text().slice(1, -1);
  var stripe          = Stripe(stripePublicKey);
  var elements        = stripe.elements();

  var style = {
    base: {
      color: '#000',
      fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
      fontSmoothing: 'antialiased',
      fontSize: '16px',
      '::placeholder': { color: '#aab7c4' }
    },
    invalid: { color: '#dc3545', iconColor: '#dc3545' }
  };

  var card = elements.create('card', { style: style });
  card.mount('#card-element');

  // --- Utilities ---
  function showFieldError(msg) {
    var $div = $('#card-errors');
    var html = `
      <span class="icon" role="alert">
        <i class="fas fa-times"></i>
      </span>
      <span>${msg}</span>
    `;
    $div.html(html);
  }
  function clearFieldError() {
    $('#card-errors').text('');
  }

  function getOverlay() {
    return $('#loading-overlay');
  }

  // Scrape the amount shown near the submit button (fallback if not found)
  function getChargeAmountText() {
    var txt = $('.submit-button p.small strong').first().text(); // e.g. "$19.99"
    return txt || '$' + (window.__grand_total || '');
  }

  // Render a confirm question inside the overlay
  function renderConfirm() {
    var amountText = getChargeAmountText();
    var html = `
      <div class="bg-white rounded shadow p-4 text-center" role="dialog" aria-modal="true" style="max-width:420px; width:92%;">
        <h5 class="mb-2">Confirm payment</h5>
        <p class="mb-0">Charge <strong>${amountText}</strong> to your card?</p>
        <div class="mt-3 d-flex justify-content-center">
          <button type="button" id="pay-confirm" class="btn btn-primary mr-2">Yes, pay now</button>
          <button type="button" id="pay-cancel"  class="btn btn-outline-secondary">Cancel</button>
        </div>
      </div>
    `;
    getOverlay().addClass('show').html(html);
  }

  // Render a spinner while processing
  function renderSpinner() {
    var html = `
      <h1 class="text-light logo-font loading-spinner" role="status" aria-live="polite">
        <span class="icon"><i class="fas fa-3x fa-sync-alt fa-spin" aria-hidden="true"></i></span>
        <span class="sr-only">Processing payment…</span>
      </h1>
    `;
    getOverlay().addClass('show').html(html);
  }

  function hideOverlay() {
    getOverlay().removeClass('show').empty();
  }

  function lockUI(lock) {
    try { card.update({ disabled: !!lock }); } catch (_) {}
    $('#submit-button').prop('disabled', !!lock);
    // Pointer-events guard in case overlay is hidden on error
    $('#payment-form').css('pointer-events', lock ? 'none' : '');
  }

  // --- Realtime validation errors on the card element ---
  card.addEventListener('change', function (event) {
    if (event.error) showFieldError(event.error.message);
    else clearFieldError();
  });

  // --- Two-step submit: confirm first, then pay ---
  var $form = $('#payment-form');

  $form.on('submit', function (ev) {
    ev.preventDefault();
    clearFieldError();
    // Step 1: Ask for confirmation in the overlay
    renderConfirm();
  });

  // Overlay button handlers (delegated since we inject the markup)
  $(document).on('click', '#pay-cancel', function () {
    hideOverlay(); // simply close; nothing else happens
  });

  $(document).on('click', '#pay-confirm', function () {
    // Step 2: proceed with payment
    renderSpinner();
    lockUI(true);

    // (Optional) supply billing_details from the form
    var billingDetails = {
      name:        $('[name="full_name"]').val() || undefined,
      email:       $('[name="email"]').val() || undefined,
      phone:       $('[name="phone_number"]').val() || undefined,
      address: {
        line1:      $('[name="street_address1"]').val() || undefined,
        line2:      $('[name="street_address2"]').val() || undefined,
        city:       $('[name="town_or_city"]').val() || undefined,
        country:    $('[name="country"]').val() || undefined,
        postal_code:$('[name="postcode"]').val() || undefined
      }
    };

    stripe.confirmCardPayment(clientSecret, {
      payment_method: { card: card, billing_details: billingDetails }
    }).then(function (result) {
      if (result.error) {
        // Show Stripe error, re-enable UI, close overlay
        showFieldError(result.error.message);
        lockUI(false);
        hideOverlay();
      } else if (result.paymentIntent && result.paymentIntent.status === 'succeeded') {
        // Let Django finish the order
        $form.off('submit'); // avoid recursion
        $form.trigger('submit');
      } else {
        showFieldError('Unexpected payment status. Please try again.');
        lockUI(false);
        hideOverlay();
      }
    });
  });
})();
