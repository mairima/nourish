/*
  Stripe Elements (robust init + full payment flow)

  Expects in template:
    <script src="https://js.stripe.com/v3/"></script>
    {{ stripe_public_key|json_script:"id_stripe_public_key" }}
    {{ client_secret|json_script:"id_client_secret" }}
  And the markup:
    <div id="card-element"></div>
    <div id="card-errors" role="alert"></div>
    <form id="payment-form">...</form>
*/

(function () {
  // ---- helpers ----
  function getJson(id) {
    var el = document.getElementById(id);
    if (!el) return null;
    var t = (el.textContent || '').trim();
    if (!t || t === 'null') return null;
    try { return JSON.parse(t); } catch (e) { return t.replace(/^"|"$/g, ''); }
  }
  function $(sel) { return document.querySelector(sel); }
  function val(name) {
    var el = document.querySelector('[name="' + name + '"]');
    return el ? el.value : '';
  }
  function showError(msg) {
    var errorDiv = $('#card-errors');
    if (!errorDiv) return;
    errorDiv.innerHTML =
      '<span class="icon" role="alert"><i class="fas fa-times"></i></span> ' +
      '<span>' + (msg || 'Payment error') + '</span>';
  }
  function clearError() {
    var errorDiv = $('#card-errors');
    if (errorDiv) errorDiv.textContent = '';
  }
  function setLoading(on) {
    var overlay = document.querySelector('.overlay');
    if (overlay) overlay.style.display = on ? 'block' : 'none';
  }

  function init() {
    var pubKey = getJson('id_stripe_public_key');
    var clientSecret = getJson('id_client_secret');

    if (!window.Stripe) {
      console.error('Stripe.js failed to load.');
      showError('Unable to load payment library. Please refresh the page.');
      return;
    }
    if (!pubKey) {
      console.error('Stripe public key missing.');
      showError('Payment not initialised (missing public key).');
      return;
    }

    var container = document.getElementById('card-element');
    if (!container) {
      console.error('#card-element not found.');
      return;
    }

    var form = document.getElementById('payment-form');
    var submitBtn = document.getElementById('submit-button');

    var stripe = Stripe(pubKey);
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

    // Realtime validation errors
    card.addEventListener('change', function (event) {
      if (event.error) showError(event.error.message);
      else clearError();
    });

    // Full payment flow (only if we have a real client secret)
    if (form) {
      form.addEventListener('submit', function (ev) {
        ev.preventDefault();

        if (!clientSecret) {
          showError('Payment not initialised. Please reload the page.');
          return;
        }

        // Lock UI
        try { card.update({ disabled: true }); } catch (_) {}
        if (submitBtn) submitBtn.disabled = true;
        setLoading(true);

        // Optional: pass billing details from your form
        var billingDetails = {
          name: val('full_name'),
          email: val('email'),
          phone: val('phone_number'),
          address: {
            line1: val('street_address1'),
            line2: val('street_address2'),
            city: val('town_or_city'),
            country: val('country'),
            postal_code: val('postcode')
          }
        };

        stripe.confirmCardPayment(clientSecret, {
          payment_method: {
            card: card,
            billing_details: billingDetails
          }
        }).then(function (result) {
          if (result.error) {
            // Show error and re-enable
            showError(result.error.message);
            try { card.update({ disabled: false }); } catch (_) {}
            if (submitBtn) submitBtn.disabled = false;
            setLoading(false);
          } else {
            // PaymentIntent succeeded → submit form to finish order
            if (result.paymentIntent && result.paymentIntent.status === 'succeeded') {
              form.submit();
            } else {
              // Unexpected status
              showError('Unexpected payment status. Please try again.');
              try { card.update({ disabled: false }); } catch (_) {}
              if (submitBtn) submitBtn.disabled = false;
              setLoading(false);
            }
          }
        });
      });
    } else {
      console.warn('#payment-form not found; skipping submit handler.');
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
