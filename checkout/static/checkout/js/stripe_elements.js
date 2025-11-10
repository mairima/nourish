/* jshint esversion: 11 */
/* globals $, Stripe, document, window */
'use strict';

/**
 * Stripe payment flow logic
 * Source: https://stripe.com/docs/payments/accept-a-payment
 * CSS reference: https://stripe.com/docs/stripe-js
 */

(function () {
  const stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
  const clientSecret = $('#id_client_secret').text().slice(1, -1);
  const stripe = Stripe(stripePublicKey);
  const elements = stripe.elements();

  const style = {
    base: {
      color: '#000',
      fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
      fontSmoothing: 'antialiased',
      fontSize: '16px',
      '::placeholder': {
        color: '#aab7c4'
      }
    },
    invalid: {
      color: '#dc3545',
      iconColor: '#dc3545'
    }
  };

  const card = elements.create('card', { style: style });
  card.mount('#card-element');

  // Handle real-time validation errors on the card element
  card.addEventListener('change', function (event) {
    const errorDiv = document.getElementById('card-errors');
    if (!errorDiv) return;

    if (event.error) {
      const html =
        '<span class="icon" role="alert">' +
        '<i class="fas fa-times"></i>' +
        '</span>' +
        '<span>' + event.error.message + '</span>';
      $(errorDiv).html(html);
    } else {
      errorDiv.textContent = '';
    }
  });

  // Handle form submission
  const form = document.getElementById('payment-form');
  if (!form) return;

  form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    card.update({ disabled: true });
    $('#submit-button').attr('disabled', true);
    $('#payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);
    
    // safer for checkbox
    const saveInfo = $('#id-save-info').prop('checked');
    const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    const postData = {
      csrfmiddlewaretoken: csrfToken,
      client_secret: clientSecret,
      save_info: saveInfo
    };
    const url = '/checkout/cache_checkout_data/';

    $.post(url, postData)
      .done(function () {
        stripe.confirmCardPayment(clientSecret, {
          payment_method: {
            card: card,
            billing_details: {
              name: $.trim(form.full_name.value),
              phone: $.trim(form.phone_number.value),
              email: $.trim(form.email.value),
              address: {
                line1: $.trim(form.street_address1.value),
                line2: $.trim(form.street_address2.value),
                city: $.trim(form.town_or_city.value),
                country: $.trim(form.country.value),
                state: $.trim(form.county.value)
              }
            }
          },
          shipping: {
            name: $.trim(form.full_name.value),
            phone: $.trim(form.phone_number.value),
            address: {
              line1: $.trim(form.street_address1.value),
              line2: $.trim(form.street_address2.value),
              city: $.trim(form.town_or_city.value),
              country: $.trim(form.country.value),
              postal_code: $.trim(form.postcode.value),
              state: $.trim(form.county.value)
            }
          }
        }).then(function (result) {
          const errorDiv = document.getElementById('card-errors');
          if (!errorDiv) return;

          if (result.error) {
            const html =
              '<span class="icon" role="alert">' +
              '<i class="fas fa-times"></i>' +
              '</span>' +
              '<span>' + result.error.message + '</span>';
            $(errorDiv).html(html);
            $('#payment-form').fadeToggle(100);
            $('#loading-overlay').fadeToggle(100);
            card.update({ disabled: false });
            $('#submit-button').attr('disabled', false);
          } else if (
            result.paymentIntent &&
            result.paymentIntent.status === 'succeeded'
          ) {
            form.submit();
          }
        });
      })
      .fail(function () {
        // Reload the page; Django will display the error message
        window.location.reload();
      });
  });
})();
