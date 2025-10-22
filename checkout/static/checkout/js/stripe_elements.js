/*
  Stripe Elements – merged:
  - Confirm overlay (v2)
  - cache_checkout_data + save_info + billing/shipping (v1)
*/

(function () {
  var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
  var clientSecret    = $('#id_client_secret').text().slice(1, -1);
  if (!stripePublicKey || !clientSecret) {
    console.error('Stripe keys missing on page'); return;
  }

  var stripe   = Stripe(stripePublicKey);
  var elements = stripe.elements();

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

  function showFieldError(msg) {
    var $div = $('#card-errors');
    var html = `
      <span class="icon" role="alert"><i class="fas fa-times"></i></span>
      <span>${msg}</span>`;
    $div.html(html);
  }
  function clearFieldError() { $('#card-errors').text(''); }

  function overlay() { return $('#loading-overlay'); }
  function renderConfirm() {
    var amountText = $('.submit-button .small strong').first().text() || '';
    var html = `
      <div class="bg-white rounded shadow p-4 text-center" role="dialog" aria-modal="true" style="max-width:420px; width:92%;">
        <h5 class="mb-2">Confirm payment</h5>
        <p class="mb-0">Charge <strong>${amountText}</strong> to your card?</p>
        <div class="mt-3 d-flex justify-content-center">
          <button type="button" id="pay-confirm" class="btn btn-primary mr-2">Yes, pay now</button>
          <button type="button" id="pay-cancel"  class="btn btn-outline-secondary">Cancel</button>
        </div>
      </div>`;
    overlay().addClass('show').html(html);
  }
  function renderSpinner() {
    var html = `
      <h1 class="text-light logo-font loading-spinner" role="status" aria-live="polite">
        <span class="icon"><i class="fas fa-3x fa-sync-alt fa-spin" aria-hidden="true"></i></span>
        <span class="sr-only">Processing payment…</span>
      </h1>`;
    overlay().addClass('show').html(html);
  }
  function hideOverlay() { overlay().removeClass('show').empty(); }

  function lockUI(lock) {
    try { card.update({ disabled: !!lock }); } catch (_) {}
    $('#submit-button').prop('disabled', !!lock);
    $('#payment-form').css('pointer-events', lock ? 'none' : '');
  }

  // Live validation
  card.addEventListener('change', function (ev) {
    if (ev.error) showFieldError(ev.error.message);
    else clearFieldError();
  });

  var $form = $('#payment-form');

  $form.on('submit', function (ev) {
    ev.preventDefault();
    clearFieldError();
    renderConfirm();
  });

  // Cancel confirmation
  $(document).on('click', '#pay-cancel', function () {
    hideOverlay();
  });

  // Confirm and pay
  $(document).on('click', '#pay-confirm', function () {
    renderSpinner();
    lockUI(true);

    // Save-info & CSRF
    var saveInfo  = Boolean($('#id-save-info').prop('checked'));
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

    // Allow overriding the cache URL via data-attr if desired
    var cacheUrl = $('#payment-form').data('cache-url') || '/checkout/cache_checkout_data/';

    // Post metadata to our cache endpoint so webhook gets bag/username/save_info
    $.post(cacheUrl, {
      'csrfmiddlewaretoken': csrfToken,
      'client_secret': clientSecret,
      'save_info': saveInfo
    })
    .done(function () {
      // Build billing + shipping from form (as in v1)
      var billingDetails = {
        name:  $.trim($('[name="full_name"]').val()),
        phone: $.trim($('[name="phone_number"]').val()),
        email: $.trim($('[name="email"]').val()),
        address: {
          line1: $.trim($('[name="street_address1"]').val()),
          line2: $.trim($('[name="street_address2"]').val()),
          city:  $.trim($('[name="town_or_city"]').val()),
          country: $.trim($('[name="country"]').val()),
          state: $.trim($('[name="county"]').val())
        }
      };
      var shipping = {
        name: $.trim($('[name="full_name"]').val()),
        phone: $.trim($('[name="phone_number"]').val()),
        address: {
          line1: $.trim($('[name="street_address1"]').val()),
          line2: $.trim($('[name="street_address2"]').val()),
          city: $.trim($('[name="town_or_city"]').val()),
          country: $.trim($('[name="country"]').val()),
          postal_code: $.trim($('[name="postcode"]').val()),
          state: $.trim($('[name="county"]').val())
        }
      };

      return stripe.confirmCardPayment(clientSecret, {
        payment_method: { card: card, billing_details: billingDetails },
        shipping: shipping
      });
    })
    .then(function (result) {
      if (!result) return; // already handled by .fail
      if (result.error) {
        showFieldError(result.error.message);
        lockUI(false);
        hideOverlay();
      } else if (result.paymentIntent && result.paymentIntent.status === 'succeeded') {
        // Let Django create the Order and redirect
        $form.off('submit'); // prevent loop
        $form.trigger('submit');
      } else {
        showFieldError('Unexpected payment status. Please try again.');
        lockUI(false);
        hideOverlay();
      }
    })
    .fail(function () {
      // Backend will surface a message; reload to show it
      location.reload();
    });
  });
})();
