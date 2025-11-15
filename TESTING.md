# Testing

> [!NOTE]  
> Return back to the [README.md](README.md) file.

The following testing documentation outlines all validation, manual, and functional tests performed on the Nourish Bakery eCommerce project, including HTML, CSS, JavaScript, Python validation, responsiveness, browser compatibility, Lighthouse audits, and user story verification.

## Code Validation

All validation was completed successfully using the official W3C, Jigsaw, JSHint, and PEP8 CI tools. Minor warnings were identified only in third-party template files (Allauth and Stripe integration), which are considered acceptable.

### HTML

All deployed templates were validated via W3C HTML Validator
.
Authenticated pages were checked using “View Page Source” to remove Jinja syntax.

Result summary: All templates passed validation with no critical errors. Minor warnings in Allauth templates were ignored as they stem from external library markup.

I have used the recommended [HTML W3C Validator](https://validator.w3.org) to validate all of my HTML files.

All html files positively validated like this picture bellow:

![screenshot](documentation/validation/html-passed.png)

Find bellow the directories and file names:


| Directory | File Urls | Notes |
| --- | --- | --- |
| bag | [bag.html](https://github.com/mairima/nourish/blob/main/bag/templates/bag/bag.html) |  |
| bag | [bag_total.html](https://github.com/mairima/nourish/blob/main/bag/templates/bag/bag_total.html) |  |
| bag | [checkout-buttons.html](https://github.com/mairima/nourish/blob/main/bag/templates/bag/checkout-buttons.html) |  |
| bag | [product-image.html](https://github.com/mairima/nourish/blob/main/bag/templates/bag/product-image.html) |  |
| bag | [product-info.html](https://github.com/mairima/nourish/blob/main/bag/templates/bag/product-info.html) |  |
| bag | [quantity-form.html](https://github.com/mairima/nourish/blob/main/bag/templates/bag/quantity-form.html) |  |
| checkout | [checkout.html](https://github.com/mairima/nourish/blob/main/checkout/templates/checkout/checkout.html) |  |
| checkout | [checkout_success.html](https://github.com/mairima/nourish/blob/main/checkout/templates/checkout/checkout_success.html) |  |
| contact | [contact.html](https://github.com/mairima/nourish/blob/main/contact/templates/contact/contact.html) |  |
| faqs | [add_faq.html](https://github.com/mairima/nourish/blob/main/faqs/templates/faqs/add_faq.html) |  |
| faqs | [faqs.html](https://github.com/mairima/nourish/blob/main/faqs/templates/faqs/faqs.html) |  |
| faqs | [update_faq.html](https://github.com/mairima/nourish/blob/main/faqs/templates/faqs/update_faq.html) |  |
| home | [index.html](https://github.com/mairima/nourish/blob/main/home/templates/home/index.html) |  |
| newsletter | [newsletter.html](https://github.com/mairima/nourish/blob/main/newsletter/templates/newsletter/newsletter.html) |  |
| products | [add_product.html](https://github.com/mairima/nourish/blob/main/products/templates/products/add_product.html) |  |
| products | [custom_clearable_file_input.html](https://github.com/mairima/nourish/blob/main/products/templates/products/custom_widget_templates%20copy/custom_clearable_file_input.html) |  |
| products | [product_detail.html](https://github.com/mairima/nourish/blob/main/products/templates/products/product_detail.html) |  |
| products | [products.html](https://github.com/mairima/nourish/blob/main/products/templates/products/products.html) |  |
| profiles | [profile.html](https://github.com/mairima/nourish/blob/main/profiles/templates/profiles/profile.html) |  |
| profiles | [profile_edit.html](https://github.com/mairima/nourish/blob/main/profiles/templates/profiles/profile_edit.html) |  |
| templates | [email_confirm.html](https://github.com/mairima/nourish/blob/main/templates/account/email_confirm.html) |  |
| templates | [login.html](https://github.com/mairima/nourish/blob/main/templates/account/login.html) |  |
| templates | [logout.html](https://github.com/mairima/nourish/blob/main/templates/account/logout.html) |  |
| templates | [password_reset.html](https://github.com/mairima/nourish/blob/main/templates/account/password_reset.html) |  |
| templates | [password_reset_done.html](https://github.com/mairima/nourish/blob/main/templates/account/password_reset_done.html) |  |
| templates | [password_reset_from_key.html](https://github.com/mairima/nourish/blob/main/templates/account/password_reset_from_key.html) |  |
| templates | [password_reset_from_key_done.html](https://github.com/mairima/nourish/blob/main/templates/account/password_reset_from_key_done.html) |  |
| templates | [signup.html](https://github.com/mairima/nourish/blob/main/templates/account/signup.html) |  |
| templates | [verification_sent.html](https://github.com/mairima/nourish/blob/main/templates/account/verification_sent.html) |  |
| templates | [terms_and_conditions.html](https://github.com/mairima/nourish/blob/main/templates/terms/terms_conditions.html) |  |
| templates | [privacy_policy.html](https://github.com/mairima/nourish/blob/main/templates/terms/privacy_policy.html) |  |


### CSS

All custom CSS files were validated using the Jigsaw CSS Validator
Bootstrap and Font Awesome were excluded.

Result summary: All CSS files passed validation after fixing extra semicolons and color format consistency.

I have used the recommended [CSS Jigsaw Validator](https://jigsaw.w3.org/css-validator) to validate all of my CSS files.

**Validation Link:**  
[CSS Jigsaw Validator](https://jigsaw.w3.org/css-validator/validator?uri=https://nourish1-cc6378c356ae.herokuapp.com/static/css/base.css)


All css files positively validated like this picture bellow:

![screenshot](documentation/validation/cssvalidated.png)

Find bellow the directories and file Urls:

| Directory | File Urls | Notes |
| --- | --- | --- |
| checkout | [checkout.css](https://github.com/mairima/nourish/blob/main/checkout/static/checkout/css/checkout.css) |  |
| profiles | [profile.css](https://github.com/mairima/nourish/blob/main/profiles/static/profiles/css/profile.css) |  |
| static | [base.css](https://github.com/mairima/nourish/blob/main/static/css/base.css) |  |


**Result:** No errors found — document validates as **CSS Level 3 + SVG**.

The main stylesheet (`base.css`) was tested with the [W3C CSS Validator](https://jigsaw.w3.org/css-validator/).  
The validator confirmed that the file meets all modern web standards and best practices.


### JavaScript

Validated via JSHint
.
All modern ES6 features were marked with /* jshint esversion: 11, jquery: true */.

Result summary: No syntax errors. Acceptable “Stripe undefined variable” warning in checkout JS.

I have used the recommended [JShint Validator](https://jshint.com) to validate all of my JS files.

| Directory | File | URL | Screenshot | Notes |
| --- | --- | --- | --- | --- |
| checkout | [stripe_elements.js](https://github.com/mairima/nourish/blob/main/checkout/static/checkout/js/stripe_elements.js) |  | ![screenshot](documentation/validation/stripeelement-val-pass.png) |  |
| profiles | [countryfield.js](https://github.com/mairima/nourish/blob/main/profiles/static/profiles/js/countryfield.js) |  | ![screenshot](documentation/validation/countryfieldjs-val-pass.png) |  |
| static | [base.js](https://github.com/mairima/nourish/blob/main/static/js/base.js) |  | ![screenshot](documentation/validation/basejs-val-pass.png) |  |


### Python

Validated via PEP8 CI Linter
.
All files passed with no PEP8 violations after applying line breaks, spacing fixes, and # noqa for Django default validator lines.

I have used the recommended [PEP8 CI Python Linter](https://pep8ci.herokuapp.com) to validate all of my Python files.

All python files positively validated like this picture bellow:

![screenshot](documentation/validation/pylinter-val-pass.png)


| Directory | File | Linter URL | Notes |
| --- | --- | --- | --- |
| bag | [admin.py](https://github.com/mairima/nourish/blob/main/bag/admin.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/mairima/nourish/main/bag/admin.py) |  |
| bag | [contexts.py](https://github.com/mairima/nourish/blob/main/bag/contexts.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/mairima/nourish/main/bag/contexts.py) |  |
| bag | [models.py](https://github.com/mairima/nourish/blob/main/bag/models.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/mairima/nourish/main/bag/models.py) |  |
| bag | [bag_tools.py](https://github.com/mairima/nourish/blob/main/bag/templatetags/bag_tools.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/mairima/nourish/main/bag/templatetags/bag_tools.py) |  |
| bag | [tests.py](https://github.com/mairima/nourish/blob/main/bag/tests.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/mairima/nourish/main/bag/tests.py) |  |
| bag | [urls.py](https://github.com/mairima/nourish/blob/main/bag/urls.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/mairima/nourish/main/bag/urls.py) |  |
| bag | [views.py](https://github.com/mairima/nourish/blob/main/bag/views.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/mairima/nourish/main/bag/views.py) |  |
| checkout | [admin.py](https://github.com/mairima/nourish/blob/main/checkout/admin.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/mairima/nourish/main/checkout/admin.py) |  |
| checkout | [forms.py](https://github.com/mairima/nourish/blob/main/checkout/forms.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/mairima/nourish/main/checkout/forms.py) |  |
| checkout | [models.py](https://github.com/mairima/nourish/blob/main/checkout/models.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/mairima/nourish/main/checkout/models.py) |  |
| checkout | [signals.py](https://github.com/mairima/nourish/blob/main/checkout/signals.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/mairima/nourish/main/checkout/signals.py) |  |
| checkout | [tests.py](https://github.com/mairima/nourish/blob/main/checkout/tests.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/mairima/nourish/main/checkout/tests.py) |  |
| checkout | [urls.py](https://github.com/mairima/nourish/blob/main/checkout/urls.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/mairima/nourish/main/checkout/urls.py) |  |
| checkout | [views.py](https://github.com/mairima/nourish/blob/main/checkout/views.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/mairima/nourish/main/checkout/views.py) |  |
| checkout | [webhook_handler.py](https://github.com/mairima/nourish/blob/main/checkout/webhook_handler.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/mairima/nourish/main/checkout/webhook_handler.py) |  |
| checkout | [webhooks.py](https://github.com/mairima/nourish/blob/main/checkout/webhooks.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/mairima/nourish/main/checkout/webhooks.py) |  |
| checkout | [widgets.py](https://github.com/mairima/nourish/blob/main/checkout/widgets.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/mairima/nourish/main/checkout/widgets.py) |  |
| contact | [admin.py](https://github.com/mairima/nourish/blob/main/contact/admin.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/mairima/nourish/main/contact/admin.py) |  |
| contact | [forms.py](https://github.com/mairima/nourish/blob/main/contact/forms.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/mairima/nourish/main/contact/forms.py) |  |
| contact | [models.py](https://github.com/mairima/nourish/blob/main/contact/models.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/mairima/nourish/main/contact/models.py) |  |
| contact | [tests.py](https://github.com/mairima/nourish/blob/main/contact/tests.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/mairima/nourish/main/contact/tests.py) |  |
| contact | [urls.py](https://github.com/mairima/nourish/blob/main/contact/urls.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/mairima/nourish/main/contact/urls.py) |  |
| contact | [views.py](https://github.com/mairima/nourish/blob/main/contact/views.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/mairima/nourish/main/contact/views.py) |  |



## Responsiveness

Tested using Chrome DevTools on Mobile (375px), Tablet (768px), and Desktop (1920px) breakpoints.
Additionally verified on a physical ios phone.

Result summary: All pages displayed consistently. Navbar collapses correctly, hero sections and grids remain responsive.

I've tested my deployed project to check for responsiveness issues.

| Page | Mobile | Tablet | Desktop | Notes |
| --- | --- | --- | --- | --- |
| Register | ![screenshot](documentation/responsiveness/mobile-register.png) | ![screenshot](documentation/responsiveness//tablet-register.png) | ![screenshot](documentation/responsiveness/desktop-register.png) | Works as expected |
| Login | ![screenshot](documentation/responsiveness/mobile-login.png) | ![screenshot](documentation/responsiveness/tablet-login.png) | ![screenshot](documentation/responsiveness/desktop-login.png) | Works as expected |
| Profile | ![screenshot](documentation/responsiveness/mobile-profile.png) | ![screenshot](documentation/responsiveness/tablet-profile.png) | ![screenshot](documentation/responsiveness/desktop-profile.png) | Works as expected |
| Home | ![screenshot](documentation/responsiveness/mobile-home.png) | ![screenshot](documentation/responsiveness/tablet-home.png) | ![screenshot](documentation/responsiveness/desktop-home.png) | Works as expected |
| Products | ![screenshot](documentation/responsiveness/mobile-products.png) | ![screenshot](documentation/responsiveness/tablet-products.png) | ![screenshot](documentation/responsiveness/desktop-products.png) | Works as expected |
| Product Details | ![screenshot](documentation/responsiveness/mobile-product-details.png) | ![screenshot](documentation/responsiveness/tablet-product-details.png) | ![screenshot](documentation/responsiveness/desktop-product-details.png) | Works as expected |
| Bag | ![screenshot](documentation/responsiveness/mobile-bag.png) | ![screenshot](documentation/responsiveness/tablet-bag.png) | ![screenshot](documentation/responsiveness/desktop-bag.png) | Works as expected |
| Checkout | ![screenshot](documentation/responsiveness/mobile-checkout.png) | ![screenshot](documentation/responsiveness/tablet-checkout.png) | ![screenshot](documentation/responsiveness/desktop-checkout.png) | Works as expected |
| Checkout Success | ![screenshot](documentation/responsiveness/mobile-checkout-success.png) | ![screenshot](documentation/responsiveness/tablet-checkout-success.png) | ![screenshot](documentation/responsiveness/desktop-checkout-success.png) | Works as expected |
| Add Product | ![screenshot](documentation/responsiveness/mobile-add-product.png) | ![screenshot](documentation/responsiveness/tablet-add-product.png) | ![screenshot](documentation/responsiveness/desktop-add-product.png) | Works as expected |
| Edit Product | ![screenshot](documentation/responsiveness/mobile-edit-product.png) | ![screenshot](documentation/responsiveness/tablet-edit-product.png) | ![screenshot](documentation/responsiveness/desktop-edit-product.png) | Works as expected |
| Newsletter | ![screenshot](documentation/responsiveness/mobile-newsletter.png) | ![screenshot](documentation/responsiveness/tablet-newsletter.png) | ![screenshot](documentation/responsiveness/desktop-newsletter.png) | Works as expected |
| Contact | ![screenshot](documentation/responsiveness/mobile-contact.png) | ![screenshot](documentation/responsiveness/tablet-contact.png) | ![screenshot](documentation/responsiveness/desktop-contact.png) | Works as expected |
| Admin Page | ![screenshot](documentation/responsiveness/mobile-admin.png) | ![screenshot](documentation/responsiveness/tablet-admin.png) | ![screenshot](documentation/responsiveness/desktop-admin.png) | Works as expected |
| 404 | ![screenshot](documentation/responsiveness/mobile-404.png) | ![screenshot](documentation/responsiveness/tablet-404.png) | ![screenshot](documentation/responsiveness/desktop-404.png) | Works as expected |
| Terms & Conditions | ![screenshot](documentation/responsiveness//mobile-termsandconditions.png) | ![screenshot](documentation/responsiveness/tablet-termsandconditions.png) | ![screenshot](documentation/responsiveness/desktop-termsandconditions.png) | Works as expected |
| Privacy Policy | ![screenshot](documentation/responsiveness/mobile-privacy.png) | ![screenshot](documentation/responsiveness/tablet-privacy.png) | ![screenshot](documentation/responsiveness/desktop-privacy.png) | Works as expected |


## Browser Compatibility

Tested on:

Chrome (Windows)

Edge (Windows)

Safari (macOS test via iphone)

Result summary: No rendering or functionality issues found. Stripe and Cloudinary integrations worked across all browsers.

- [Chrome](https://www.google.com/chrome)
- [Edge](https://www.microsoft.com/edge)
- [Safari](https://support.apple.com/downloads/safari)


I've tested my deployed project on multiple browsers to check for compatibility issues.

### Browser Compatibility Table

| Page | Chrome | Edge | Safari | Notes |
| --- | --- | --- | --- | --- |
| Register | See **Responsiveness section** | ![screenshot](documentation/browsers/edge-register.png) | ![screenshot](documentation/browsers/safari-register.jpeg) | Works as expected |
| Login | See **Responsiveness section** | ![screenshot](documentation/browsers/edge-login.png) | ![screenshot](documentation/browsers/safari-login.jpeg) | Works as expected |
| Profile | See **Responsiveness section** | ![screenshot](documentation/browsers/edge-profile.png) | ![screenshot](documentation/browsers/safari-profile.jpeg) | Works as expected |
| Home | See **Responsiveness section** | ![screenshot](documentation/browsers/edge-home.png) | ![screenshot](documentation/browsers/safari-home.jpeg) | Works as expected |
| Products | See **Responsiveness section** | ![screenshot](documentation/browsers/edge-products.png) | ![screenshot](documentation/browsers/safari-products.jpeg) | Works as expected |
| Product Details | See **Responsiveness section** | ![screenshot](documentation/browsers/edge-product-details.png) | ![screenshot](documentation/browsers/safari-product-details.jpeg) | Works as expected |
| Bag | See **Responsiveness section** | ![screenshot](documentation/browsers/edge-bag.png) | ![screenshot](documentation/browsers/safari-bag.jpeg) | Works as expected |
| Checkout | See **Responsiveness section** | ![screenshot](documentation/browsers/edge-checkout.png) | ![screenshot](documentation/browsers/safari-checkout.jpeg) | Works as expected |
| Checkout Success | See **Responsiveness section** | ![screenshot](documentation/browsers/edge-checkout-success.png) | ![screenshot](documentation/browsers/safari-checkout-success.jpeg) | Works as expected |
| Add Product | See **Responsiveness section** | ![screenshot](documentation/browsers/edge-add-product.png) | ![screenshot](documentation/browsers/safari-add-product.jpeg) | Works as expected |
| Edit Product | See **Responsiveness section** | ![screenshot](documentation/browsers/edge-edit-product.png) | ![screenshot](documentation/browsers/safari-edit-product.jpeg) | Works as expected |
| Newsletter | See **Responsiveness section** | ![screenshot](documentation/browsers/edge-newsletter.png) | ![screenshot](documentation/browsers/safari-newsletter.jpeg) | Works as expected |
| Contact | See **Responsiveness section** | ![screenshot](documentation/browsers/edge-contact.png) | ![screenshot](documentation/browsers/safari-contact.jpeg) | Works as expected |
| 404 | See **Responsiveness section** | ![screenshot](documentation/browsers/edge-404.png) | ![screenshot](documentation/browsers/safari-404.jpeg) | Works as expected |
| Terms & Conditions | See **Responsiveness section** | ![screenshot](documentation/browsers/edge-terms.png) | ![screenshot](documentation/browsers/safari-terms.jpeg) | Works as expected |
| Privacy Policy | See **Responsiveness section** | ![screenshot](documentation/browsers/edge-privacy.png) | ![screenshot](documentation/browsers/safari-policy.jpeg) | Works as expected |


## Lighthouse Audit

I've tested my deployed project using the Lighthouse Audit tool to check for any major issues. Some warnings are outside of my control, and mobile results tend to be lower than desktop.

| Page | Desktop |
| --- | --- |
| Register | ![screenshot](documentation/lighthouse/desktop-register.png) |
| Login | ![screenshot](documentation/lighthouse/desktop-login.png) |
| Profile | ![screenshot](documentation/lighthouse/desktop-profile.png) |
| Home | ![screenshot](documentation/lighthouse/desktop-home.png) |
| Products | ![screenshot](documentation/lighthouse/desktop-products.png) |
| Product Details | ![screenshot](documentation/lighthouse/desktop-product-details.png) |
| Bag | ![screenshot](documentation/lighthouse/desktop-bag.png) |
| Checkout | ![screenshot](documentation/lighthouse/desktop-checkout.png) |
| Checkout Success | ![screenshot](documentation/lighthouse/desktop-checkout-success.png) |
| Add Product | ![screenshot](documentation/lighthouse/desktop-add-product.png) |
| Edit Product | ![screenshot](documentation/lighthouse/desktop-edit-product.png) |
| Newsletter | ![screenshot](documentation/lighthouse/desktop-newsletter.png) |
| Contact | ![screenshot](documentation/lighthouse/desktop-contact.png) |
| 404 | ![screenshot](documentation/lighthouse/desktop-404.png) |
| Terms & Conditions | ![screenshot](documentation/lighthouse/desktop-terms.png) |
| Privacy Policy | ![screenshot](documentation/lighthouse/desktop-policy.png) |

## Defensive Programming

Defensive checks were implemented for all form submissions and page restrictions.

Key findings:

All user inputs are validated via Django forms with required attributes.

Non-authenticated users cannot access checkout success or profile pages.

Admin-only CRUD actions protected with @login_required and @user_passes_test.


Defensive programming was manually tested with the below user acceptance testing:

## 🛡️ Defensive Programming – User Acceptance Testing

| Page | Expectation | Test | Result | Screenshot |
| --- | --- | --- | --- | --- |
| Products | Users should be able to browse products (Cakes, Snacks, Drinks, etc.) without needing to log in. | Opened all product categories as a guest user on the deployed site. | Products displayed correctly with images and descriptions pulled from Cloudinary, no login required. |Refer to **products** validation image |
|  |  Category: Products should sort correctly by price and name. | Tested sorting “Price (low–high)”, “Price (high–low)”, and “Name (A–Z)” on the product list page. | Sorting options worked perfectly and displayed updated order instantly. |![screenshot](documentation/defensive/product-sort.png)  |
|  | Category filters should show only relevant items. | Applied filters for Cakes, Snacks, and Drinks. | Filter results correctly showed only the selected category’s products. | ![screenshot](documentation/defensive/productcategory-filter.png)|
|  | Product details should show correct data. | Clicked on products like *Pistachio Cake with Chocolate Ganache* and *Orange Drink*. | Each product displayed accurate description, price, Cloudinary image, and “Add to Bag” button. | Refer to **products** validation image |
| Shopping Cart | Customers should add and update product quantities easily. | Added items to bag and used “+ / –” buttons to adjust quantities. | Quantities updated dynamically; bag total recalculated correctly. | Refer to **bag** validation image|
|  | Customers should manage their cart content. | Opened bag page and removed an item. | Bag updated instantly; totals and delivery charge recalculated. | Refer to **bag** validation image |
| Checkout | Checkout should display all items, grand total, and secure form. | Proceeded to checkout with multiple items in the bag. | Checkout summary matched the bag contents; form fields loaded as expected. |Refer to **checkout** validation image |
|  | Payment must be securely processed via Stripe. | Entered valid test card details (`4242 4242 4242 4242`). | Stripe processed payment securely; redirected to checkout success page. |Refer to **checkout** validation image|
|  | Confirmation email should be sent automatically. | Completed an order and checked email inbox. | Order confirmation email received successfully with correct order summary. |![screenshot](documentation/defensive/emailconfirm.png)|
|  | Confirmation page should display a valid order number. | Completed checkout flow. | Checkout success page displayed order number and order summary correctly. | Refer to **checkout** validation image |
| Account Management | Logged-in users should access their profiles and past orders. | Logged in using test user and navigated to “My Profile”. | Order history, address, and contact details displayed accurately. |Refer to **profiles** validation image|
|  | Returning users’ shipping info should prefill automatically. | Completed second order with same account. | Address, phone, and email pre-populated correctly in the checkout form. | Refer to **profiles** validation image |
| Admin Features | Admin users can create new products. | Logged in as superuser and added new Cake item via Admin panel. | New product appeared immediately in product list and category view. | Refer to **admin** validation image|
|  | Admin users can update product information. | Edited price and description of an existing Snack item. | Product updated successfully and reflected on the live site. | Refer to **admin** validation image |
|  | Admin users can delete outdated or duplicate products. | Deleted an old test product through Admin dashboard. | Product removed successfully after confirmation prompt. | Refer to **admin** validation image |
| Orders | Admin users can review all placed orders. | Accessed “Orders” in Admin → Checkout Orders. | Orders listed with correct customer, total, and status. | Refer to **Admin** validation image |
| Newsletter | Users can subscribe with valid emails. | Entered valid emails into newsletter form. | Subscriptions stored in database; success message displayed. |![screenshot](documentation/defensive/subscribtiontoast.png)|
| 404 Error Page | Invalid URLs should show custom error page. | Navigated to `/xyz404test/` path. | Custom 404 page displayed with bakery theme and “Back to Home” link. |  Refer to **404** validation image |
| Discount Code Application | Invalid, manipulated discount codes must be safely rejected server-side. | Entered expired code, blank input, and edited discount value in HTML (DevTools). | Only valid codes accepted; other codes rejected| ![screenshot](documentation/defensive/discounttoast.png) |
| Unsubscribe Functionality | Unsubscribe token must be validated securely | Used correct unsubscribe link, expired/tampered token, and repeated unsubscribe attempts. | Valid token successfully removed subscription; invalid/tampered links returned safe error. | ![screenshot](documentation/defensive/unsubscribetedtoast.png)|


## User Story Testing

All user stories from the README were tested and satisfied.

| Target | Expectation | Outcome | Screenshot Reference |
| --- | --- | --- | --- |
| As a guest user | I would like to browse the bakery’s products (cakes, snacks, and drinks) without needing to register | so that I can freely explore the available treats before creating an account. | Refer to **Products** responsiveness image |
| As a guest user | I would like to be prompted to sign up or log in when I proceed to checkout | so that I can complete my order securely and have it recorded under my account. | Refer to **Login** responsiveness image |
| As a user | I would like to subscribe to the Nourish newsletter | so that I can stay updated about new bakery items, discounts, and promotions. | Refer to **Newsletter** responsiveness image |
| As a customer | I would like to browse multiple product categories such as Cakes, Snacks, and Drinks | so that I can easily find my preferred type of bakery item. | Refer to **Products** responsiveness image |
| As a customer | I would like to sort products by price (low–high / high–low) and by name (A–Z) | so that I can organize the product list to suit my preferences. | Refer to **Products** responsiveness image |
| As a customer | I would like to filter products by category | so that I can focus on the products that interest me most. | Refer to **Products** responsiveness image |
| As a customer | I would like to click on a product to view its detailed page showing name, description, price, and image | so that I can read more about the item before purchasing. | Refer to **Product Details** responsiveness image |
| As a customer | I would like to add products to my shopping bag and adjust quantities with + / – buttons | so that I can easily select the exact quantity I want before checkout. | Refer to **Bag** responsiveness image |
| As a customer | I would like to view my shopping bag and manage its contents | so that I can review, edit, or remove items before paying. | Refer to **Bag** responsiveness image |
| As a customer | I would like to change product quantities directly in the bag page | so that I can quickly correct or update my order. | Refer to **Bag** responsiveness image |
| As a customer | I would like to remove any product from my bag | so that I can keep only the items I want to buy. | Refer to **Bag** responsiveness image |
| As a customer | I would like to proceed to a checkout page showing my bag items, total cost, and a secure form to enter my details | so that I can complete my purchase easily and confidently. | Refer to **Checkout** responsiveness image |
| As a customer | I would like to receive an order confirmation email after checkout | so that I have proof of my purchase and delivery details. | Refer to **Checkout Success** responsiveness image |
| As a customer | I would like to see an order confirmation page showing an order number after completing my payment | so that I know my transaction has been successful. | Refer to **Checkout Success** responsiveness image |
| As a customer | I would like to pay securely using Stripe | so that my card details are safely processed with encrypted checkout fields. | Refer to **Checkout** validation image |
| As a returning customer | I would like to log into my Nourish account and view my previous orders | so that I can track my past purchases and reorder items I liked. | Refer to **Profile** responsiveness image |
| As a returning customer | I would like my checkout form to remember my saved address and contact information | so that I can make future purchases more quickly. | Refer to **Profile** responsiveness image |
| As a site owner | I would like to add new products with names, prices, descriptions, and images | so that I can expand my online store’s menu whenever new bakery items are introduced. | Refer to **Add Product** responsiveness image |
| As a site owner | I would like to update product details (price, name, description, or image) | so that I can keep all product information current and accurate. | Refer to **Edit Product** responsiveness image |
| As a site owner | I would like to delete products that are outdated or no longer available | so that my site always displays relevant and available items. | Refer to **Admin Page** responsiveness image |
| As a site owner | I would like to view all customer orders from the admin dashboard | so that I can manage sales and fulfill orders efficiently. | Refer to **Admin Page** responsiveness image |
| As a site owner | I would like to manage categories (Cakes, Snacks, Drinks) | so that I can ensure all products are well-organized for easy browsing. | Refer to **Products** responsiveness image |
| As a user | I would like to see a friendly 404 error page when I visit an invalid link | so that I know I’ve reached a missing page and can return to the homepage easily. | Refer to **404** responsiveness image |
| As a user | I want to apply a valid discount code during checkout | so that I can receive a promotional price reduction on my order. | Refer to Discount Code testing image in the defemsive section above|
| As a user | I want to unsubscribe easily from the newsletter using a secure one-click link | so that I can stop receiving emails whenever I choose. | Refer to Unsubscribe testing image in the defemsive section above|

## Bugs

### Fixed Bugs

Tracked using GitHub Issues.

[![GitHub issue custom search](https://img.shields.io/github/issues-search/mairima/nourish?query=is%3Aissue%20is%3Aclosed%20label%3Abug&label=Fixed%20Bugs&color=green)](https://www.github.com/mairima/nourish/issues?q=is%3Aissue+is%3Aclosed+label%3Abug)

I've used [GitHub Issues](https://www.github.com/mairima/nourish/issues) to track and manage bugs and issues during the development stages of my project.

All previously closed/fixed bugs can be tracked [here](https://www.github.com/mairima/nourish/issues?q=is%3Aissue+is%3Aclosed+label%3Abug).


| Issue                              | Fix Applied / How It Was Fixed                         | Status   |
|-----------------------------------|----------------------------------------------------------|----------|
| Heroku site static files issue, now fixed       | the "django.contrib.staticfiles" was placed before "cloudinary_storage","cloudinary", on the list and the static files where then properly loaded on heroku.|  Fixed |

### Unfixed Bugs

[![GitHub issue custom search](https://img.shields.io/github/issues-search/mairima/nourish?query=is%3Aissue%2Bis%3Aopen%2Blabel%3Abug&label=Unfixed%20Bugs&color=red)](https://www.github.com/mairima/nourish/issues?q=is%3Aissue+is%3Aopen+label%3Abug)

Any remaining open issues can be tracked [here](https://www.github.com/mairima/nourish/issues?q=is%3Aissue+is%3Aopen+label%3Abug).


### Known Issues

| Issue |
| --- |
| The project is designed to be responsive from `375px` and upwards, in line with the material taught on the course LMS. Minor layout inconsistencies may occur on extra-wide (e.g. 4k/8k monitors) or smart-display devices (e.g. Nest Hub, Smart Watches, Gameboy Color), as these resolutions are outside the project’s scope, as taught by Code Institute. |

> [!IMPORTANT]  
> There are no remaining bugs that I am aware of, though, even after thorough testing, I cannot rule out the possibility.

## Summary

- All **HTML**, **CSS**, **JavaScript**, and **Python** files validated successfully.  
- The site is **responsive**, **accessible**, and functions correctly on all major browsers.  
- **Stripe**, **Cloudinary**, and **Allauth** integrations perform as expected.  
- **Lighthouse** scores exceed **Code Institute** benchmarks.  
- **Defensive programming** ensures safe, secure operations for both users and admins.  