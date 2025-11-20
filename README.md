# Nourish ([Live site](https://nourish1-cc6378c356ae.herokuapp.com))

Developer: Mairi Aissatou ([mairima](https://www.github.com/mairima))

[![GitHub commit activity](https://img.shields.io/github/commit-activity/t/mairima/nourish)](https://www.github.com/mairima/nourish/commits/main)
[![GitHub last commit](https://img.shields.io/github/last-commit/mairima/nourish)](https://www.github.com/mairima/nourish/commits/main)
[![GitHub repo size](https://img.shields.io/github/repo-size/mairima/nourish)](https://www.github.com/mairima/nourish)
[![badge](https://img.shields.io/badge/deployment-Heroku-purple)](https://nourish1-cc6378c356ae.herokuapp.com)

🥖 Nourish — Project Overview & Rationale

Nourish is an elegant and fully responsive e-commerce web application designed for a modern, health-conscious bakery brand. The project aims to provide users with a seamless online shopping experience for artisanal baked goods, catering to individuals who value convenience, quality, and transparency in what they consume.

The website offers a clean and intuitive interface where users can browse through products, view detailed descriptions, add items to their shopping bag, and complete secure checkouts. Beyond shopping, Nourish integrates features such as newsletter subscriptions, FAQs, and a contact page to help build customer trust and engagement — reflecting the kind of holistic customer experience real businesses need.

🎯 Project Goals

The main goal of Nourish is to demonstrate the design and development of a fully functional, responsive, and user-friendly online store using Django and Bootstrap, with secure authentication, Stripe payment integration, and backend management for products and orders.
It also seeks to model how small local businesses can expand their reach through digital transformation — taking a neighborhood bakery and giving it a professional online presence.

👥 Target Audience

Nourish is aimed at:

Everyday consumers looking for healthy, fresh, and locally made baked goods.

Small business owners or bakers exploring e-commerce as a way to scale their businesses.

Students and developers interested in learning modern web development, UX design, and full-stack architecture through a real-world concept.

💡 Why This Project (Rationale)

I chose to create Nourish because food, particularly artisan baking, connects people on a personal and emotional level. During recent years, more consumers have shifted toward online purchasing — even for traditionally local products like bread and pastries. This inspired me to build a platform that blends the warmth of a neighborhood bakery with the convenience of modern e-commerce.

It combines backend logic (Django), frontend design (HTML, CSS, Bootstrap), third-party integrations (Stripe, email verification), and real-world business logic — making it creatively fulfilling.

Ultimately, Nourish isn’t just an online bakery — it’s a digital experience built to show how thoughtful design and solid engineering can make even the simplest daily pleasures more accessible and enjoyable.


**Site Mockups**
*([amiresponsive](https://ui.dev/amiresponsive?url=https://nourish1-cc6378c356ae.herokuapp.com))*


![screenshot](documentation/mockup.png)

source: [nourish amiresponsive](https://ui.dev/amiresponsive?url=https://nourish1-cc6378c356ae.herokuapp.com)

> [!IMPORTANT]  
> The examples in these templates are strongly influenced by the Code Institute walkthrough project called "Boutique Ado".

## UX

### The 5 Planes of UX

#### 1. Strategy

**Purpose**
- Deliver a seamless and visually appealing e-commerce experience for customers to browse, filter, and purchase baked goods.

- Empower bakery owners to manage their store, products, and orders efficiently through a secure and user-friendly system.

**Primary User Needs**
- Guest Users — browse, view, and purchase products easily without needing an account.

- Registered Users — sign up, log in, view order history, and manage account details effortlessly.

- Store Owners / Admins — maintain product listings, monitor sales, and manage orders in the Django admin interface.

**Business Goals**
- Increase online sales and brand awareness for the bakery.

- Build customer loyalty through accounts, order history, and newsletter engagement.

- Maintain an accurate, scalable inventory management system and secure payment workflow.

#### 2. Scope

**[Features](#features)** (see below)

**Content Requirements**
- Product listings with name, image, price, and description.

- Shopping bag and checkout functionality with quantity updates. Guests can add items to the shopping bag and are prompted to log in when they reach the secure checkout page. After logging in, the items in the bag can remain available, and the logged-in user can proceed to checkout.

- Secure payment processing via Stripe.

- User authentication system with email verification.

- Order confirmation and email notifications.

- Newsletter subscription and contact forms.

- FAQ section and custom 404 error page.

- Fully responsive design optimized for all devices.

#### 3. Structure

**Information Architecture**
- **Navigation Menu**:
  - Links to Home, All Products, Categories, Contact, Newsletter, FAQ, and Account.

  - Visible shopping bag and user account icons on every page for convenience.

- **Hierarchy**:
  - Hero banner on the homepage introducing the brand and call to action.

  - Product categories displayed prominently for intuitive browsing.

  - Checkout and bag pages streamlined for quick navigation and conversion.

**User Flow**
1. Guest user lands on the Homepage → explores Products.
2. Adds desired items to the Shopping Bag.
3. Proceeds to Checkout, where they may sign up or log in.
4. Completes payment securely via Stripe and receives confirmation.
5. Registered users can later log in to view past orders and update account details.
6. Users can subscribe to the newsletter or contact the store for support.
7. Admins manage products, categories, and orders via Django’s backend.

#### 4. Skeleton

**[Wireframes](#wireframes)** (see below)
Homepage: Hero banner, delivery promotion, and navigation links.

Product Listing Page: Product grid with consistent image sizes and prices.

Product Detail Page: Displays detailed product info, price, and add-to-bag option.

Shopping Bag Page: List of items with quantity controls and subtotal updates.

Checkout Page: Form for shipping and billing details with payment summary.

Login / Signup Pages: Centered forms with clear prompts and validation messages.

Contact, Newsletter, FAQ Pages: Simple, mobile-first layouts for clarity and usability.

#### 5. Surface

**Visual Design Elements**
- **[Colours](#colour-scheme)** (see below)
- **[Typography](#typography)** (see below)

### Colour Scheme

### **Primary Colours**

| Role | Colour | Hex | Description |
| --- | --- | --- | --- |
| **Primary Text & Background Contrast** | Black | `#000000` | Used across text, headers, buttons, and hero overlays --- provides a bold and modern contrast. |
| **Primary Background** | White | `#FFFFFF` | Clean white base throughout pages (`body.plain-page`, product sections). |
| **Gold Accent** | Soft Gold | `#FFD700` | Used in footer icons and hover states --- adds a luxurious, elegant tone. |

* * * * *

### **Accent Colours**

| Role | Colour | Hex | Description |
| --- | --- | --- | --- |
| **Action / Success / Highlights** | Green | `#28A745` | Used for primary buttons (`.shop-now-button`, `.navbar-nav .active .nav-link`) and status highlights. |
| **Green Hover State** | Darker Green | `#218838` | Hover tone for `.shop-now-button`. |
| **Info / Link Accent** | Teal Blue | `#17A2B8` | Used for anchor links and text-info color in forms. |
| **Success Alert (Bootstrap tone)** | Light Green | `#28A745` (reused) | Matches brand accent for visual consistency. |

* * * * *

### **Neutral & Supporting Shades**

| Role | Colour | Hex | Description |
| --- | --- | --- | --- |
| **Secondary Text** | Medium Gray | `#6C757D` | For muted text and placeholders (`.allauth-form-inner-content p`). |
| **Light Backgrounds** | Light Gray | `#F8F9FA`, `#E9ECEF`, `#E6E6E6` | Used in FAQ cards, newsletter cards, and neutral sections for structure and readability. |
| **Overlay Tint** | Black (semi-transparent) | `rgba(0, 0, 0, 0.35)` | Adds depth to hero banners. |

Consistent use of dark headers and light body sections to create contrast and focus.
[coolors](https://coolors.co/generate).


I used [coolors.co](https://coolors.co/080708-3772ff-df2935-fdca40-e6e8e6) to generate my color palette.

-   `#000000` -- **Primary text and headers** (black)

    -   `#FFFFFF` -- **Primary background** (white)

    -   `#FFD700` -- **Gold accent** for icons and hover states

    -   `#28A745` -- **Action green** for buttons and highlights

    -   `#218838` -- **Dark green hover** tone

    -   `#17A2B8` -- **Teal info links** and secondary accents

    -   `#6C757D` -- **Muted gray text** (placeholders and secondary content)

    -   `#F8F9FA` -- **Light background gray** for FAQ and card sections

    -   `#E6E6E6` -- **Neutral border and panel color**

![screenshot](documentation/colors.png)

### Typography

Lato — a modern, highly legible sans-serif font.

Uppercase styling used for headings and branding elements for a professional finish.

- [Lato](https://fonts.google.com/specimen/Lato) was used for all other secondary text.
- [Font Awesome](https://fontawesome.com) icons were used throughout the site, such as the social media icons in the footer.

### Imagery

High-quality product images showcasing artisanal baked goods.

Uniform aspect ratios to maintain balance and consistency across product cards.

Visuals emphasize freshness, warmth, and craftsmanship — reflecting the brand ethos.

## Wireframes

I created wireframes for the Nourish website to plan the layout, content structure, and user journey across different screen sizes (mobile, tablet, and desktop). These wireframes helped shape the responsive design and UI decisions made during development.

To follow best practice, wireframes were developed for mobile, tablet, and desktop sizes.
I've used [Balsamiq](https://balsamiq.com/wireframes) and chatgpt to design my site wireframes.

## 🖼️ Wireframes

| Page | Mobile | Desktop/Tablet |  |
| --- | --- | --- | --- |
| **General Wireframe** | ![screenshot](documentation/wireframes/mobilegeneralwireframe.png) | ![screenshot](documentation/wireframes/desktopgeneralwireframe.png) |

## User Stories


| Target | Expectation | Outcome |
| --- | --- | --- |
| As a guest user | I would like to browse all available baked goods without needing to register | so that I can explore the shop before deciding to create an account. |
| As a guest user | I would like to be prompted to create an account or log in at checkout | so that I can complete my purchase and receive an order confirmation. |
| As a guest user | I would like to filter products by category | so that I can quickly narrow down to the type of baked goods I'm looking for. |
| As a guest user | I would like to sort products by price and name | so that I can organize items in a way that suits my browsing preference. |
| As a customer | I would like to view consistent product images, names, prices, and descriptions | so that I can compare items easily and make informed purchasing decisions. |
| As a customer | I would like to click on individual products to view detailed information | so that I can see ingredients, sizes, and prices before adding to my bag. |
| As a customer | I would like to add items to my shopping bag | so that I can save them for checkout. |
| As a customer | I would like to view and manage my shopping bag | so that I can adjust, add, or remove items before proceeding to checkout. |
| As a customer | I would like to adjust the quantity of products in my shopping bag | so that I can modify how many items I wish to purchase. |
| As a customer | I would like to remove products from my shopping bag | so that I can manage what I plan to buy. |
| As a customer | I would like to see an updated subtotal, delivery cost, and total in my bag | so that I can clearly understand the overall cost. |
| As a customer | I would like to securely enter my payment details via Stripe | so that I can confidently complete transactions online. |
| As a customer | I would like to proceed through a simple checkout process | so that I can complete my purchase with minimal friction. |
| As a customer | I would like to be redirected to a checkout success page after payment | so that I know my purchase was successful. |
| As a customer | I would like to receive an email confirmation after purchasing | so that I have a record of my transaction and order details. |
| As a new user | I would like to register an account with email verification | so that I can create a secure and validated profile. |
| As a returning customer | I would like to log in and out easily | so that I can access my saved details and order history from any device. |
| As a returning customer | I would like to view my past orders on my profile | so that I can review previous purchases or reorder favorite items. |
| As a returning customer | I would like my checkout information (name, address) to be remembered | so that I can complete future orders faster. |
| As a user | I would like a responsive navigation bar and footer | so that I can browse comfortably across mobile, tablet, and desktop devices. |
| As a user | I would like the active navbar link to be highlighted | so that I can easily identify which page I am on. |
| As a user | I would like a delivery banner visible across pages | so that I can quickly see promotions or free delivery offers. |
| As a user | I would like to receive clear toast notifications | so that I have immediate feedback after actions like adding to bag or submitting forms. |
| As a user | I would like to subscribe to a newsletter | so that I can stay updated on new products and seasonal promotions. |
| As a user | I would like to contact the shop through a contact form | so that I can ask questions or make special requests. |
| As a user | I would like to read frequently asked questions (FAQs) | so that I can quickly find answers to common queries. |
| As a site owner | I would like to add new products with a name, description, price, and image | so that I can keep the online store stocked and updated. |
| As a site owner | I would like to update existing product details | so that I can make price or description changes at any time. |
| As a site owner | I would like to delete products no longer available | so that I can maintain an accurate and relevant product catalog. |
| As a site owner | I would like to manage categories for baked goods | so that items are organized and easy for customers to navigate. |
| As a site owner | I would like to view and manage all customer orders | so that I can fulfill purchases efficiently. |
| As a user | I would like to see a branded 404 error page | so that I know when I've reached a broken or non-existent link and can return to the homepage. |
| As a user | I would like to receive a welcome/first-time discount code after subscribing | so that I feel rewarded and motivated to make my first purchase. |
| As a user | I would like to receive a confirmation message after subscribing to the newsletter | so that I know my subscription was successful and my email was registered. |
| As a user | I would like the ability to unsubscribe from the newsletter at any time | so that I can manage my communication preferences and stop receiving promotional emails, in case I have less storage. |

## Features

### Existing Features

Refer for most images for this section in the testing document under responsiveness section

| Feature | Notes | Note |
| --- | --- | --- |
| Register | Users can create an account through a custom signup form integrated with Django Allauth. Email verification is required to activate the account for improved security. |  |
| Login | Registered users can securely log in using their email and password. Toast messages confirm successful logins or errors. |  |
| Logout | Users can easily log out of their account with a confirmation message. |  |
| Product Catalog | Displays all available baked goods, including cakes, pastries, and bread. Supports keyword search, sorting by price or name, and filtering by category. |  |
| Product Details | Shows a detailed page for each product, including images, description, price, and ingredients. Users can select quantity before adding items to the bag. |  |
| Add to Bag | Users can add products to their shopping bag directly from the product page. Toast notifications confirm successful additions. |  |
| View Bag | Displays all items currently added to the bag, with options to update quantities or remove items. The bag total, delivery charge, and grand total are shown dynamically. |  |
| Bag Quantity Update | Users can adjust quantities in their bag using increment/decrement buttons. Totals update automatically in real time. |  |
| Checkout | Users can enter shipping and payment details securely through Stripe integration. Guest checkout and logged-in checkout are both supported. |  |
| Checkout Redirect | After a successful payment, users are redirected to a checkout success page summarizing their order. |  |
| Order Confirmation | Once checkout is completed, users receive an on-screen success message and a confirmation email containing their order details. |  |
| Email Verification | Upon registration, users must verify their email address through a confirmation email link to activate their account. |  |
| Profile Management | Logged-in users can manage their profile information, update delivery details, and view order history. |  |
| Order History | Displays a history of all previous purchases, allowing users to view order numbers, items purchased, and total spent. |  |
| Product Management | Admins and superusers can create, update, and delete products through a user-friendly CRUD interface in Django Admin. |  |
| Newsletter | Visitors can sign up for the newsletter to receive updates and promotions. Emails are stored in the database for future campaigns. |  |
| Contact Form | Users can contact the shop through a form that captures name, email, and message. Messages are saved in the database for admin review. |  |
| FAQs | A dynamic FAQ section managed from the admin panel, allowing the site owner to update common questions easily. |  |
| Toast Notifications | Interactive toast messages provide feedback for actions like adding to bag, removing items, or logging in/out. |  |
| Delivery Banner | A responsive promotional banner is displayed at the top of pages to highlight delivery offers |  |
| Navbar Highlight | The active navigation link is highlighted to improve user awareness of the current page. | ![screenshot](documentation/features/navbarhighlight.png) |
| Responsive Navbar & Footer | Fully responsive design ensures easy navigation and consistent layout across all device sizes. |  |
| Footer Design | Includes quick navigation links, contact info, social media icons, and newsletter subscription. |  |
| Heroku Deployment | The site is fully deployed to Heroku, allowing live access for users with database integration. | [Live Site – Nourish](https://nourish1-cc6378c356ae.herokuapp.com/) |
| SEO Optimization | Integrated sitemap.xml, robots.txt, and optimized meta tags improve search visibility. |  |
| Marketing & Social Links | Footer links connect to social media platforms to boost engagement and brand reach. | Refer to Social Media Marketing section below |
| 404 Error Page | A custom 404 page aligns with the site's branding and helps users return to the home page. |  |
| Welcome Discount Code | Users receive an automatic welcome or first-time discount code after subscribing to the newsletter, encouraging initial purchases and improving conversion. | |
| Newsletter Confirmation Message | After subscribing, users receive a clear confirmation message so they know their email has been successfully added to the mailing list. | |
| Unsubscribe Functionality | Users can unsubscribe from the newsletter at any time through a secure link, allowing them full control over their communication preferences. | |

### CRUD Functionality

Nourish includes full Create, Read, Update and Delete (CRUD) functionality across several features of the site. The tables below outline how CRUD is implemented in each relevant area of the project.

---

### Products (Admin Only)

| Operation | Description | Access |
|----------|-------------|--------|
| Create | Admin users can add new products through the Django admin panel. | Admin |
| Read | All users can browse and view all products and their details. | All users |
| Update | Admin users can edit product information, prices and images. | Admin |
| Delete | Admin users can delete products from the catalogue. | Admin |

---

### Shopping Bag

| Operation | Description | Access |
|----------|-------------|--------|
| Create | Users can add products to the shopping bag. Items are stored in session or in the database for logged-in users. | All users |
| Read | Users can view their bag contents at any time. | All users |
| Update | Users can adjust product quantities directly in the bag. | All users |
| Delete | Users can remove items from the shopping bag. | All users |

---

### Checkout and Orders

| Operation | Description | Access |
|----------|-------------|--------|
| Create | Orders are created after successful checkout and payment. | All users |
| Read | Authenticated users can view their order history in their profile. | Registered users |
| Update | Users can update and save delivery details to their profile. | Registered users |
| Delete | Orders are not deleted to preserve transaction integrity. | Not applicable |

---

### User Profiles

| Operation | Description | Access |
|----------|-------------|--------|
| Create | User profiles are automatically generated upon registration. | Registered users |
| Read | Users can view their saved profile details and order history. | Registered users |
| Update | Users can update delivery and profile information. | Registered users |
| Delete | Profile deletion is handled manually (upon request) for GDPR compliance. | Admin |

---

### Newsletter Subscriptions

| Operation | Description | Access |
|----------|-------------|--------|
| Create | Users can subscribe to the newsletter. | All users |
| Read | Admin can view subscriber lists in the Django admin panel. | Admin |
| Update | Not applicable (email addresses cannot be edited). | Not applicable |
| Delete | Users can unsubscribe using a secure tokenised link. | All users |

---

### FAQs (Admin Only)

| Operation | Description | Access |
|----------|-------------|--------|
| Create | Admin users can create new FAQ entries. | Admin |
| Read | Users can view all FAQs on the FAQ page. | All users |
| Update | Admin users can edit existing FAQ entries. | Admin |
| Delete | Admin users can delete FAQs. | Admin |
---




### Future Features

-  **Social Login Integration**: Allow new users to sign in using Google or GitHub, removing the need to create a separate password and making the login process faster and more convenient.

-   **Product Reviews & Ratings**: Allow customers to leave reviews and rate baked goods, helping others make informed choices. Admins will have the ability to approve or remove reviews.

-   **Wishlist Functionality**: Enable registered users to save favorite products to a wishlist for future purchases.

 -   **Discount Codes & Promotions**: Allow admins to create and manage promotional discount codes for marketing campaigns or special events.

-   **Product Recommendations**: Suggest similar or complementary baked goods based on customer browsing and purchase history.

-   **Loyalty Program**: Introduce a reward system where users earn points for purchases that can be redeemed for discounts.

-   **Product Inventory Alerts**: Notify users when out-of-stock items become available again.

 -   **Social Media Integration**: Allow users to share products directly to social platforms such as Instagram or Facebook to boost engagement.

-   **Shipping Tracking Integration**: Include real-time delivery tracking details within order history.

-   **Admin Analytics Dashboard**: Provide the store owner with an overview of sales data, top-performing products, and user engagement metrics.

 -   **Wishlist Reminder Emails**: Send gentle reminders to users when their wishlist items go on sale or are back in stock.

## Tools & Technologies

| Tool / Tech | Use |
| --- | --- |
| [![badge](https://img.shields.io/badge/Markdown_Builder-grey?logo=markdown&logoColor=000000)](https://markdown.2bn.dev) | Generate README and TESTING templates. |
| [![badge](https://img.shields.io/badge/Git-grey?logo=git&logoColor=F05032)](https://git-scm.com) | Version control. (`git add`, `git commit`, `git push`) |
| [![badge](https://img.shields.io/badge/GitHub-grey?logo=github&logoColor=181717)](https://github.com) | Secure online code storage. |
| [![badge](https://img.shields.io/badge/VSCode-grey?logo=htmx&logoColor=007ACC)](https://code.visualstudio.com) | Local IDE for development. |
| [![badge](https://img.shields.io/badge/HTML-grey?logo=html5&logoColor=E34F26)](https://en.wikipedia.org/wiki/HTML) | Main site content and layout. |
| [![badge](https://img.shields.io/badge/CSS-grey?logo=css&logoColor=1572B6)](https://en.wikipedia.org/wiki/CSS) | Design and layout. |
| [![badge](https://img.shields.io/badge/JavaScript-grey?logo=javascript&logoColor=F7DF1E)](https://www.javascript.com) | User interaction on the site. |
| [![badge](https://img.shields.io/badge/Python-grey?logo=python&logoColor=3776AB)](https://www.python.org) | Back-end programming language. |
| [![badge](https://img.shields.io/badge/Heroku-grey?logo=heroku&logoColor=430098)](https://www.heroku.com) | Hosting the deployed back-end site. |
| [![badge](https://img.shields.io/badge/Bootstrap-grey?logo=bootstrap&logoColor=7952B3)](https://getbootstrap.com) | Front-end CSS framework for modern responsiveness and pre-built components. |
| [![badge](https://img.shields.io/badge/Django-grey?logo=django&logoColor=092E20)](https://www.djangoproject.com) | Python framework for the site. |
| [![badge](https://img.shields.io/badge/PostgreSQL-grey?logo=postgresql&logoColor=4169E1)](https://www.postgresql.org) | Relational database management. |
| [![badge](https://img.shields.io/badge/Cloudinary-grey?logo=cloudinary&logoColor=3448C5)](https://cloudinary.com) | Online static file storage. |
| [![badge](https://img.shields.io/badge/WhiteNoise-grey?logo=python&logoColor=FFFFFF)](https://whitenoise.readthedocs.io) | Serving static files with Heroku. |
| [![badge](https://img.shields.io/badge/Stripe-grey?logo=stripe&logoColor=008CDD)](https://stripe.com) | Online secure payments of e-commerce products/services. |
| [![badge](https://img.shields.io/badge/Gmail_API-grey?logo=gmail&logoColor=EA4335)](https://mail.google.com) | Sending emails in my application. |
| [![badge](https://img.shields.io/badge/Font_Awesome-grey?logo=fontawesome&logoColor=528DD7)](https://fontawesome.com) | Icons. |
| [![badge](https://img.shields.io/badge/ChatGPT-grey?logo=openai&logoColor=75A99C)](https://chat.openai.com) | Help debug, troubleshoot, and explain things. |
| [![badge](https://img.shields.io/badge/Mermaid-grey?logo=mermaid&logoColor=FF3670)](https://mermaid.live) | Generate an interactive diagram for the data/schema. |


## Database Design

### Data Model

The data model for Nourish was designed to support a smooth e-commerce workflow — from product browsing and user management to order processing and customer communication.
The Entity Relationship Diagram (ERD) below illustrates how core components such as users, profiles, products, orders, and contact forms interact with each other to ensure an efficient and scalable system structure.

Entity Relationship Diagrams (ERD) help visualize the project’s database architecture, showing how models relate to one another and simplifying both development and maintenance.

I have used `Mermaid` to generate an interactive ERD of my project.

```mermaid
erDiagram
    Category {
        int id PK
        varchar name
        varchar friendly_name
    }

    Product {
        int id PK
        int category FK
        varchar name
        text description
        decimal price
        decimal rating
        varchar image_filename
        varchar image_url
    }

    Order {
        int id PK
        varchar order_number
        varchar full_name
        varchar email
        varchar phone_number
        varchar country
        varchar postcode
        varchar town_or_city
        varchar street_address1
        varchar street_address2
        varchar county
        datetime date
        decimal delivery_cost
        decimal order_total
        decimal grand_total
        int user_profile FK
        int discount_code FK
    }

    OrderLineItem {
        int id PK
        int order FK
        int product FK
        varchar product_size
        int quantity
        decimal lineitem_total
    }

    UserProfile {
        int id PK
        int user FK
        varchar default_phone_number
        varchar default_country
        varchar default_postcode
        varchar default_town_or_city
        varchar default_street_address1
        varchar default_street_address2
        varchar default_county
    }

    Newsletter {
        int id PK
        varchar email
        varchar unsubscribe_token
        boolean is_active
    }

    DiscountCode {
        int id PK
        varchar code
        int discount_percent
        boolean is_welcome_code
        boolean is_active
        datetime expiry_date
        int used_by FK
    }

    Contact {
        int id PK
        varchar name
        varchar email
        text message
        datetime sent
    }

    FAQ {
        int id PK
        varchar question
        text answer
    }

    Order }o--|| UserProfile : "user_profile"
    Order }o--o| DiscountCode : "applied_code"
    OrderLineItem }o--|| Order : "order"
    OrderLineItem }o--|| Product : "product"
    Product }o--|| Category : "category"
    UserProfile }o--|| User : "user"
    DiscountCode }o--o| UserProfile : "used_by"
```

source: [Mermaid](https://mermaid.live/edit#pako:eNqVVcFu2zAM_RVD57RIHLdpfRs6DBg2bB2GXYYAhmIxjlBZcimqqdvk3yfbSVPHceP5kBh8TyRFPtKvLDUCWMwAP0ueIc_nOvDPHwsYvDbv1SM1BVIE998OpieO6Ypj4DxV8xy6CORcqq654NauDYoG2c71IeQ9mqVUMDCygCV3ipJiZTQk2uULwH6WJQSghAuBYO1kKDHsJ5JZ68Rgkkoq-1mpcfojvDCWqiac8YDliXoFm83FxWbTql0crLhNfEX2xDtOkBksB1b1dC-XKEELVSYH-C0TH1m4lAb6tw_uXFCCZ_K3tynKgqTRB2RhjKrvZ-UL2INdQCpzroICZQpdM3KSOuuG9WAGicN3Kq1NzW_PNauam82hrHGwAGV0Zr0g9tyfKAYPkKm4vfJdOqWS_5uvD8ehJabWsV4dfqzzs3N1dp6OJ0T4ypLMoX7pNlOAkk-ApZ8LS124KScZ4qoL-g2nxTFYy82gzKTmKlnw7OQdZAFJIY-3Vt3o71LDV4L8TMMr06Pjmlp13KemvBPpnRxn99afRn618k8lsddlO6NmG-Rcl6fy3R3ZK7tfyTtie890yT9gbRUQDdb-Owm_3ebOaOKD18mg0ag7nHv1daf6y6dfAyM9OrDtbVS75dqu94O2ZSOWA_rgwn9Ta7dzRivwKbLYvwqOD3M21xWPOzK_S52ymNDBiLmikvvuK8ziJVfWWwuuWfzKnlk8jSaXN9ez8HoyHc_C8TiajVjJ4ovp5XUUTqMovLqdXd2Et-FsO2Ivxngfk8vxZBpGkT_m_zxW-_tbY01QNC5b7YJt_wE0ZoQj)


I have used `pygraphviz` and `django-extensions` to auto-generate an ERD.

The steps taken were as follows:
- In the terminal: `sudo apt update`
- then: `sudo apt-get install python3-dev graphviz libgraphviz-dev pkg-config`
- then type `Y` to proceed
- then: `pip3 install django-extensions pygraphviz`
- in my `settings.py` file, I added the following to my `INSTALLED_APPS`:
```python


INSTALLED_APPS = [
    ...
    'django_extensions',
    ...
]
```
- back in the terminal: `python3 manage.py graph_models -a -o erd.png`
- drag the new `erd.png` file into my `documentation/` folder
- removed `'django_extensions',` from my `INSTALLED_APPS`
- finally, in the terminal: `pip3 uninstall django-extensions pygraphviz -y`

![screenshot](documentation/erd/nourish-erd-mermaid.png)

source: [medium.com](https://medium.com/@yathomasi1/1-using-django-extensions-to-visualize-the-database-diagram-in-django-application-c5fa7e710e16)

## Agile Development Process

### GitHub Projects

[GitHub Projects](https://www.github.com/mairima/nourish/projects) served as an Agile tool for this project. Through it, EPICs, User Stories, issues/bugs, and Milestone tasks were planned, then subsequently tracked on a regular basis using the Kanban project board.

![screenshot](documentation/images/gh-projects.png)

### GitHub Issues

[GitHub Issues](https://www.github.com/mairima/nourish/issues) served as an another Agile tool. There, I managed my User Stories and Milestone tasks, and tracked any issues/bugs.

| Link | Screenshot |
| --- | --- |
| [![GitHub issues](https://img.shields.io/github/issues-search/mairima/nourish?query=is%3Aissue%20is%3Aopen%20-label%3Abug&label=Open%20Issues&color=yellow)](https://www.github.com/mairima/nourish/issues?q=is%3Aissue%20is%3Aopen%20-label%3Abug) | ![screenshot](documentation/images/gh-issues-open.png) |
| [![GitHub closed issues](https://img.shields.io/github/issues-search/mairima/nourish?query=is%3Aissue%20is%3Aclosed%20-label%3Abug&label=Closed%20Issues&color=green)](https://www.github.com/mairima/nourish/issues?q=is%3Aissue%20is%3Aclosed%20-label%3Abug) | ![screenshot](documentation/images/gh-issues-closed.png) |

### MoSCoW Prioritization

I've decomposed my Epics into User Stories for prioritizing and implementing them. Using this approach, I was able to apply "MoSCoW" prioritization and labels to my User Stories within the Issues tab.

- **Must Have**: guaranteed to be delivered 
- **Should Have**: adds significant value 
- **Could Have**: has small impact if left out
- **Won't Have**: not a priority for this iteration - future features

## Ecommerce Business Model

This site sells goods to individual customers, and therefore follows a **Business to Customer** model. It is of the simplest **B2C** forms, as it focuses on individual transactions, and doesn't need anything such as monthly/annual subscriptions.

It is still in its early development stages, although it already has a newsletter, and links for social media marketing.

Social media can potentially build a community of users around the business, and boost site visitor numbers, especially when using larger platforms such a Facebook.

A newsletter list can be used by the business to send regular messages to site users. For example, what items are on special offer, new items in stock, updates to business hours, notifications of events, and much more!

## SEO & Marketing

### Keywords

To improve **search engine visibility** and help potential customers discover the **Nourish** website, I identified relevant keywords aligned with my brand, products, and audience. These keywords include both **short-tail** and **long-tail** phrases to target general and specific search intents.

I used tools such as [Word Tracker](https://www.wordtracker.com) to check search frequency and keyword strength (during the free trial period), and also reviewed related trends from Google Search Console and manual competitor analysis.

* * * * *

### **Short-Tail Keywords (Head Terms)**

These help capture high-volume searches for general products and categories:

-   nourish cakes

-   healthy snacks

-   African desserts

-   homemade pastries

-   fresh fruit drinks

-   bakery Berlin

-   online cake shop

-   natural yogurt drink

* * * * *

### **Long-Tail Keywords**

These phrases target more specific and conversion-ready searches:

-   buy pistachio cake online in Berlin

-   best homemade groundnut sweets

-   crunchy chocolate cake near me

-   affordable African snacks delivery

-   order fish pie with home delivery

-   refreshing orange and yogurt drinks

-   handmade cakes and pastries in Germany

-   Nourish bakery healthy dessert shop

* * * * *

### **Example Product Keyword Mapping**

| Product | Category | Example Keywords |
| --- | --- | --- |
| **Pistachio Cake** | Cakes | pistachio cake Berlin, buy nut cake online, premium handmade cakes |
| **Crunchy Chocolate Cake** | Cakes | chocolate cake Germany, crunchy chocolate dessert, artisan cake shop |
| **Groundnut Sweets** | Snacks | groundnut candy Cameroon style, African sweet snacks, peanut brittle Berlin |
| **Fish Pie** | Snacks | African fish pie recipe, homemade pastry Berlin, savory snack delivery |
| **Yogurt Drink** | Drinks | natural yogurt drink, probiotic drink Berlin, healthy milk beverage |
| **Fresh Orange Drink** | Drinks | freshly squeezed orange juice, vitamin C drink, healthy fruit beverage |

### Sitemap

I've used [XML-Sitemaps](https://www.xml-sitemaps.com) to generate a sitemap.xml file. This was generated using my deployed site URL: https://nourish1-cc6378c356ae.herokuapp.com

After it finished crawling the entire site, it created a [sitemap.xml](sitemap.xml), which I've downloaded and included in the repository.

### Robots

I've created the [robots.txt](robots.txt) file at the root-level. Inside, I've included the default settings:

```txt
User-agent: *
Disallow:
Allow: /
Sitemap: https://nourish1-cc6378c356ae.herokuapp.com/sitemap.xml
```

### **Explanation**

-   `User-agent: *` → Applies to all search engine crawlers (Google, Bing, etc.).

-   `Disallow:` → Blank, meaning no pages are blocked from indexing.

-   `Allow: /` → Confirms the entire site is open to crawling.

-   `Sitemap:` → Points to your automatically generated sitemap for structured indexing.

Further links for future implementation:
- [Google search console](https://search.google.com/search-console)
- [Creating and submitting a sitemap](https://developers.google.com/search/docs/advanced/sitemaps/build-sitemap)
- [Managing your sitemaps and using sitemaps reports](https://support.google.com/webmasters/answer/7451001)
- [Testing the robots.txt file](https://support.google.com/webmasters/answer/6062598)

### Social Media Marketing

Creating a strong social base (with participation) and linking that to the business site can help drive sales. Using more popular providers with a wider user base, such as Facebook, typically maximizes site views.

I've created a Facebook business account using Facebook. 

![screenshot](documentation/images/facebookpage-nourish.png)

### Newsletter Marketing

I have incorporated a newsletter sign-up form on my application, to allow users to supply their email address if they are interested in learning more. 

**Custom Django Model Newsletter**

📬 Newsletter Feature Implementation -- Nourish Website
------------------------------------------------------

To fulfill the project requirement of including a **newsletter system** and implementing **at least three custom models**, a dedicated app called `newsletter` was created within the Django project.

### 🔧 Step-by-Step Implementation

#### 1\. **Creating the Newsletter App**

A custom Django app named `newsletter` was generated using:

`python manage.py startapp newsletter`

This separates newsletter-related functionality from other parts of the site and keeps the project modular.

#### 2\. **Defining the Custom Model**

Inside the `models.py` of the `newsletter` app, a `Newsletter` model was created with a single field --- `email`. This is the only field required for users to subscribe.

`# newsletter/models.py

from django.db import models

class Newsletter(models.Model):
    email = models.EmailField(unique=True, null=False, blank=False)

    def __str__(self):
        return self.email`

-   The `email` field is **unique**, ensuring that the same email address cannot subscribe more than once.

-   The `__str__` method allows for a readable display of emails in the admin panel.

This model counts as **one of the three required custom models** for the full-stack milestone project.

#### 3\. **Admin Configuration**

To manage subscriptions via the Django admin:

`# newsletter/admin.py

from django.contrib import admin
from .models import Newsletter

admin.site.register(Newsletter)`

This allows site admins to view, add, or delete newsletter entries from the backend.

#### 4\. **Newsletter Form & Frontend Integration**

A basic form was created using Django's `ModelForm`, allowing users to subscribe by submitting their email from a public-facing newsletter page.

The form was added to a `newsletter.html` template linked in the navigation bar, clearly visible to users.

#### 5\. **Sending Emails (Optional Enhancement)**

The `send_mail()` function --- similar to the one used in `webhook_handler.py` for Stripe confirmations --- can be used to notify all newsletter subscribers whenever a **new product** is added.

This would look something like:

`from django.core.mail import send_mail
from .models import Newsletter

def notify_subscribers(product):
    subscribers = Newsletter.objects.all()
    for subscriber in subscribers:
        send_mail(
            subject=f"New Product: {product.name}",
            message=f"Check out our newest product: {product.name} at {product.get_absolute_url()}",
            from_email="noreply@nourish.com",
            recipient_list=[subscriber.email],
            fail_silently=False,
        )`

> This approach enhances user engagement and builds a customer base over time.



## Testing

> [!NOTE]  
> For all testing, please refer to the [TESTING.md](TESTING.md) file.

## Deployment

The live deployed application can be found deployed on [Heroku](https://nourish1-cc6378c356ae.herokuapp.com).

### Heroku Deployment


To deploy my **Nourish** Django website, I used [**Heroku**](https://www.heroku.com), a **cloud-based Platform as a Service (PaaS)** that simplifies deployment and hosting of web applications. It allows me to run the app entirely in the cloud without managing servers manually.

### 🔧 Step-by-Step Deployment

After creating my Heroku account, here's how I deployed the project:

* * * * *

### 1\. **Create a New Heroku App**

-   I logged into the Heroku Dashboard, clicked **New** (top right), and selected **Create new app**.

-   I gave the app a **unique name** (`nourish1` in my case), chose **Europe (EU)** as the region (since I'm based in Germany), and clicked **Create App**.

* * * * *

### 2\. **Set Environment Variables**

-   In the app dashboard, I navigated to **Settings > Reveal Config Vars**.

-   I manually added the same environment variables from my local `env.py` file, such as:

    -   `SECRET_KEY`

    -   `DEBUG = False`

    -   `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`

    -   `STRIPE_PUBLIC_KEY`, `STRIPE_SECRET_KEY`, etc.

    -   `DATABASE_URL` (automatically added by Heroku Postgres)

* * * * *

### 3\. **Prepare for Deployment**

-   I pushed my code to GitHub, ensuring the `Procfile`, `requirements.txt` were included in the repo.

-   In the **Deploy** tab of the Heroku dashboard, I:

    -   Linked the Heroku app to my GitHub repo.

    -   Enabled **Automatic Deploys** (so each push to main redeploys the app).

    -   Clicked **Deploy Branch** for the first-time manual deploy.

* * * * *

### 4\. **Final Touches**

-   After deployment, I ran the following from the **Heroku CLI** (or manually via the dashboard):

    `heroku run python manage.py migrate
    heroku run python manage.py collectstatic`

-   I also set up **Heroku Postgres** (as the production database) and **Cloudinary** for static/media files.

| Key | Value |
| --- | --- |
| `CLOUDINARY_CLOUD_NAME`     | your-cloudinary-cloud-name                 |
| `CLOUDINARY_API_KEY`        | your-cloudinary-api-key                    |
| `CLOUDINARY_API_SECRET`     | your-cloudinary-api-secret                |
| `DATABASE_URL` | user-inserts-own-postgres-database-url |
| `DISABLE_COLLECTSTATIC` | 1 (*this is temporary, and can be removed for the final deployment*) |
| `EMAIL_HOST_PASS` | user-inserts-own-gmail-api-key |
| `EMAIL_HOST_USER` | user-inserts-own-gmail-email-address |
| `SECRET_KEY` | any-random-secret-key |
| `STRIPE_PUBLIC_KEY` | user-inserts-own-stripe-public-key |
| `STRIPE_SECRET_KEY` | user-inserts-own-stripe-secret-key |
| `STRIPE_WH_SECRET` | user-inserts-own-stripe-webhook-secret |

Heroku needs some additional files in order to deploy properly.

- [requirements.txt](requirements.txt)
- [Procfile](Procfile)
- [.python-version](.python-version)

Requirements & Deployment Configuration (Steps I Took)

To prepare my Nourish project for deployment on Heroku, I followed these steps:

1. ✅ Installed Project Requirements

I used the provided requirements.txt file to install all necessary dependencies locally:

pip3 install -r requirements.txt


If I installed new packages during development, I updated the file using:

pip3 freeze --local > requirements.txt


This ensured Heroku had all the packages needed for a successful build.

2. ✅ Created the Procfile

To tell Heroku how to run the app, I created a Procfile at the root of mRequirements & Deployment Configuration (Steps I Took)
-------------------------------------------------------

To prepare my Nourish project for deployment on **Heroku**, I followed these steps:

* * * * *

### 1\. ✅ Installed Project Requirements

I used the provided `requirements.txt` file to install all necessary dependencies locally:

`pip3 install -r requirements.txt`

If I installed new packages during development, I updated the file using:

`pip3 freeze --local > requirements.txt`

This ensured Heroku had all the packages needed for a successful build.

* * * * *

### 2\. ✅ Created the Procfile

To tell Heroku how to run the app, I created a `Procfile` at the root of my project:

`echo web: gunicorn nourish.wsgi > Procfile`

> In my case, the main Django app is called `nourish`, so I used `nourish.wsgi`.

* * * * *

### 3\. ✅ Specified the Python Version

To ensure Heroku used the correct Python version, I created a file called `.python-version` with the following:

`3.12`

This matches the Python version I used locally and helps avoid compatibility issues.

* * * * *

### 4\. 🚀 Deployed to Heroku

After pushing my code to GitHub, I went to my Heroku app dashboard and:

-   Connected my Heroku app to the GitHub repository.

-   Enabled **Automatic Deployment** from the `main` branch, so every push redeploys the site.

-   Clicked **Deploy Branch** once for the initial deploy.

After deployment, I ran:

`heroku run python manage.py migrate
heroku run python manage.py collectstatic`

This completed the database setup and prepared static files for production.y project:

echo web: gunicorn nourish.wsgi > Procfile


In my case, the main Django app is called nourish, so I used nourish.wsgi.

3. ✅ Specified the Python Version

To ensure Heroku used the correct Python version, I created a file called .python-version with the following:

3.12


This matches the Python version I used locally and helps avoid compatibility issues.

4. 🚀 Deployed to Heroku

After pushing my code to GitHub, I went to my Heroku app dashboard and:

Connected my Heroku app to the GitHub repository.

Enabled Automatic Deployment from the main branch, so every push redeploys the site.

Clicked Deploy Branch once for the initial deploy.

After deployment, I ran:

heroku run python manage.py migrate
heroku run python manage.py collectstatic


This completed the database setup and prepared static files for production.

The project could now be connected and deployed to Heroku!

### Cloudinary API

🖼️ Using Cloudinary to Store Media Files
-----------------------------------------

Since Heroku doesn't persist static or media files (e.g., product images), I integrated [**Cloudinary**](https://cloudinary.com) into my Nourish Django project to handle all **media asset storage and delivery**.

###  How to Set It Up

1.  **I created a free Cloudinary account** and logged into the dashboard.

    -   For "Primary Interest", I selected **Programmable Media for image and video API**.

2.  In my dashboard, I copied my **Cloudinary API Environment Variable**.

    -   It looks like:

        `CLOUDINARY_URL=cloudinary://123456789012345:AbCdEfGhIjKlMnOpQrStuVwXyZa@your-cloud-name`

    -   I removed the leading `CLOUDINARY_URL=` and used the rest as the **value** for the key `CLOUDINARY_URL`.

3.  I added this to my local `env.py` like this:

    `os.environ["CLOUDINARY_URL"] = "cloudinary://123456789012345:AbCdEfGhIjKlMnOpQrStuVwXyZa@your-cloud-name"`

4.  I also added the same key and value to **Heroku Config Vars** in the dashboard:

    -   **Key**: `CLOUDINARY_URL`

    -   **Value**: `cloudinary://...@your-cloud-name`

5.  Finally, I updated the Django settings and installed the necessary packages:

    `pip install cloudinary django-cloudinary-storage`

    In `settings.py`, I added:

    `DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'`

### PostgreSQL

Database – PostgreSQL (Code Institute)

For the Nourish website, I used the Code Institute PostgreSQL Database
 as the relational database, connected through Django.
This database was ideal for development and deployment since it integrates smoothly with Heroku.

How I Set It Up

I visited the CI PostgreSQL Database page
 and submitted my email address.

I received an email with my database credentials and a connection URL similar to this:

postgres://<db_username>:<db_password>@<db_host>/<db_name>


I then copied this full database URL into:

My local env.py file, and

My Heroku Config Vars under the key DATABASE_URL.

This connected my Django application to the hosted PostgreSQL database, allowing all my data — such as users, orders, products, and newsletter subscriptions — to be stored safely online.

Note: Code Institute databases are only for CI students and have a limited lifespan (max 8 per student, up to 18 months).
For future production, I plan to migrate to a personal PostgreSQL instance (e.g., via Render or ElephantSQL).

### Stripe API (Payments Integration)

For processing secure online payments, I integrated Stripe
 into the Nourish website.
Stripe handles all transactions during checkout, ensuring encrypted and verified payment processing.

Steps I Took

I created a Stripe account, logged into the dashboard, and retrieved the test API keys:

STRIPE_PUBLIC_KEY → starts with pk_

STRIPE_SECRET_KEY → starts with sk_

I added both keys to:

My local env.py file

My Heroku Config Vars

I set up Stripe Webhooks to handle order confirmation events (in case users close the payment window early):

From the Stripe dashboard → Developers → Webhooks → Add Endpoint

Added:

https://nourish1-cc6378c356ae.herokuapp.com/checkout/wh/


Selected “Receive all events”

Copied the Signing Secret as:

STRIPE_WH_SECRET


All these keys are stored securely as environment variables. Stripe now automatically handles checkout, payment confirmation, and order success for customers.

### Gmail API (Email Notifications)

To send confirmation emails to customers after successful purchases, I integrated Gmail’s SMTP service
.

How I Configured It

I enabled 2-Step Verification for my Gmail account.

Under Google Account → Security → App Passwords, I generated a 16-character app password.

I used these two environment variables in my project:

EMAIL_HOST_USER = myemail@gmail.com
EMAIL_HOST_PASS = <16-character-app-password>


These were added to both env.py and Heroku Config Vars.

This setup allowed the site to automatically send:

Order confirmation emails

Stripe payment receipts

Future newsletter subscription confirmations

### WhiteNoise Static File Handling

Since Heroku doesn’t persist static files, I used WhiteNoise
 to serve static assets (CSS, JS) efficiently during deployment.

✅ Steps I Followed

Installed WhiteNoise:

pip install whitenoise


Updated the requirements.txt file:

pip freeze --local > requirements.txt


Added WhiteNoise middleware in settings.py:

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # Other middleware below
]


Ran:

python manage.py collectstatic


WhiteNoise ensures my static files (Bootstrap, CSS, JS) load instantly on Heroku even without external storage.

### Local Development

This project can be cloned or forked in order to make a local copy on your own system.

For either method, you will need to install any applicable packages found within the [requirements.txt](requirements.txt) file.

- `pip3 install -r requirements.txt`.

You will need to create a new file called `env.py` at the root-level, and include the same environment variables listed above from the Heroku deployment steps.


I created a file called env.py in the project root to store my environment variables (same as Heroku Config Vars).

Note:
The values in env.py (Stripe keys, Cloudinary URL, Database URL, etc.) are unique to my project and must be replaced with your own if you clone this repository.

✅ Summary of Environment Variables Used

Variable	Description
SECRET_KEY	Django secret key
DATABASE_URL	PostgreSQL connection URL
CLOUDINARY_URL	Cloudinary media storage
STRIPE_PUBLIC_KEY	Stripe publishable key
STRIPE_SECRET_KEY	Stripe secret key
STRIPE_WH_SECRET	Stripe webhook signing secret
EMAIL_HOST_USER	Gmail address
EMAIL_HOST_PASS	Gmail app password


Sample `env.py` file:

```python
import os

os.environ.setdefault("CLOUDINARY_URL", "cloudinary://<your_api_key>:<your_api_secret>@<your_cloud_name>")
os.environ.setdefault("DATABASE_URL", "user-inserts-own-postgres-database-url")
os.environ.setdefault("EMAIL_HOST_PASS", "user-inserts-own-gmail-host-api-key")
os.environ.setdefault("EMAIL_HOST_USER", "user-inserts-own-gmail-email-address")
os.environ.setdefault("SECRET_KEY", "any-random-secret-key")
os.environ.setdefault("STRIPE_PUBLIC_KEY", "user-inserts-own-stripe-public-key")
os.environ.setdefault("STRIPE_SECRET_KEY", "user-inserts-own-stripe-secret-key")
os.environ.setdefault("STRIPE_WH_SECRET", "user-inserts-own-stripe-webhook-secret")  # only if using Stripe Webhooks

# local environment only (not to include these in production/deployment!)
os.environ.setdefault("DEBUG", "True")
os.environ.setdefault("DEVELOPMENT", "True")
```

Once the project is cloned or forked, in order to run it locally, you'll need to follow these steps:

- Start the Django app: `python3 manage.py runserver`
- Stop the app once it's loaded: `CTRL+C` (*Windows/Linux*) or `⌘+C` (*Mac*)
- Make any necessary migrations: `python3 manage.py makemigrations --dry-run` then `python3 manage.py makemigrations`
- Migrate the data to the database: `python3 manage.py migrate --plan` then `python3 manage.py migrate`
- Create a superuser: `python3 manage.py createsuperuser`
- Load fixtures (*if applicable*): `python3 manage.py loaddata file-name.json` (*repeat for each file*)
- Everything should be ready now, so run the Django app again: `python3 manage.py runserver`

If you'd like to backup your database models, use the following command for each model you'd like to create a fixture for:

- `python3 manage.py dumpdata your-model > your-model.json`
- *repeat this action for each model you wish to backup*
- **NOTE**: You should never make a backup of the default *admin* or *users* data with confidential information.

#### Cloning

You can clone the repository by following these steps:

1. Go to the [GitHub repository](https://www.github.com/mairima/nourish).
2. Locate and click on the green "Code" button at the very top, above the commits and files.
3. Select whether you prefer to clone using "HTTPS", "SSH", or "GitHub CLI", and click the "copy" button to copy the URL to your clipboard.
4. Open "Git Bash" or "Terminal".
5. Change the current working directory to the location where you want the cloned directory.
6. In your IDE Terminal, type the following command to clone the repository:
	- `git clone https://www.github.com/mairima/nourish.git`
7. Press "Enter" to create your local clone.

Alternatively, if using Ona (formerly Gitpod), you can click below to create your own workspace using this repository.

[![Open in Ona-Gitpod](https://ona.com/run-in-ona.svg)](https://gitpod.io/#https://www.github.com/mairima/nourish)

**Please Note**: in order to directly open the project in Ona (Gitpod), you should have the browser extension installed. A tutorial on how to do that can be found [here](https://www.gitpod.io/docs/configure/user-settings/browser-extension).

#### Forking

By forking the GitHub Repository, you make a copy of the original repository on our GitHub account to view and/or make changes without affecting the original owner's repository. You can fork this repository by using the following steps:

1. Log in to GitHub and locate the [GitHub Repository](https://www.github.com/mairima/nourish).
2. At the top of the Repository, just below the "Settings" button on the menu, locate and click the "Fork" Button.
3. Once clicked, you should now have a copy of the original repository in your own GitHub account!

### Local VS Deployment

There are no remaining major differences between the local version when compared to the deployed version online.

## Credits

### Project Idea & Design

-   The overall concept for the **Nourish** website --- an online store for cakes, snacks, and drinks --- was **inspired by real-world artisanal bakeries** and food brands, as well as personal interest in African and homemade baked goods.

-   The design and UX structure were informed by the [Code Institute's Boutique Ado](https://github.com/Code-Institute-Solutions/boutique_ado_v1) e-commerce walkthrough project, but heavily customized in visuals, layout, and content.

### Content

This section lists all third-party resources, libraries, tools, and support I used while building the Nourish website. Every effort has been made to ensure correct attribution for code, media, and guidance received throughout the project.

| Source | Notes |
| --- | --- |
| [Markdown Builder](https://markdown.2bn.dev) | Help generating Markdown files |
| [Chris Beams](https://chris.beams.io/posts/git-commit) | "How to Write a Git Commit Message" |
| [Boutique Ado](https://codeinstitute.net) | Code Institute walkthrough project inspiration |
| [Bootstrap](https://getbootstrap.com) | Various components / responsive front-end framework |
| [Cloudinary](https://cloudinary.com) | Cloud-based storage and delivery for static and media files |
| [Whitenoise](https://whitenoise.readthedocs.io) | Static file service |
| [Stripe](https://docs.stripe.com/payments/elements) | Online payment services |
| [Gmail API](https://developers.google.com/gmail/api/guides) | Sending payment confirmation emails |
| [Python Tutor](https://pythontutor.com) | Additional Python help |
| [ChatGPT](https://chatgpt.com) | for AI-assisted content creation, wireframes, and image generation |

### Media

This section lists all third-party resources, libraries, tools, and support I used while building the Nourish website. Every effort has been made to ensure correct attribution for code, media, and guidance received throughout the project

- Images
| [Pexels](https://images.pexels.com/photos/416160/pexels-photo-416160.jpeg) | Hero image |

| Source | Notes |
| --- | --- |
| [favicon.io](https://favicon.io) | Generating the favicon |
| [Boutique Ado](https://codeinstitute.net) | Sample images provided from the walkthrough projects |
| [Font Awesome](https://fontawesome.com) | Icons used throughout the site |
| [Cloudinary](https://cloudinary.com) | Hosts and delivers all uploaded product images and media assets |
| [ChatGPT Image Generator](https://chat.openai.com) | colors |


### Acknowledgements

Throughout the development of the Nourish project, I received support, encouragement, and guidance from various people and platforms — all of which played a valuable role in helping me grow as a developer.

This section is dedicated to recognizing and appreciating that support:

-  I would like to thank Code Institute, for the course structure, walkthrough projects (especially Boutique Ado), mentorship, and Slack community support throughout my Full Stack Software Developer journey.

- I would like to thank my Code Institute mentor, [Tim Nelson](https://www.github.com/TravelTimN) for the support throughout the development of this project.
- I would like to thank the [Code Institute](https://codeinstitute.net) Tutor Team for their assistance with troubleshooting and debugging some project issues.
- I would like to thank the [Code Institute Slack community](https://code-institute-room.slack.com) and [Code Institute Discord community](https://discord-portal.codeinstitute.net) for the moral support.
- I would like to thank my family.

