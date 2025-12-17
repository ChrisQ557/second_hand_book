# 📚 Second Hand Book Store

Welcome to **Second Hand Book Store** — a Django-based assessment project providing a full e-commerce flow for browsing, cart management, checkout (with Stripe), and user order history.

---

## 🌟 Overview

Users can:

- Browse a curated collection of second-hand books (by language, genre).
- Add books to a shopping cart and manage quantities.
- Securely sign up, sign in, and sign out via Django Allauth.
- Checkout with Stripe (PaymentIntent API) and persist orders.
- View order history, mark orders as received, or delete past orders.
- Receive toast notifications for important actions.

---

## 🎯 Intended Users

- **Book Enthusiasts** — who want a streamlined way to shop used books.
- **Bargain Hunters** — searching for affordable reads.
- **Collectors** — tracking past purchases and order statuses.
- **Django Learners** — studying a full-stack assessment with auth, payments, and relational models.
- **Accessibility-focused Users** — benefit from ARIA-labeled modals, semantic HTML, and responsive design.

---

## 🧱 Features

- 🎨 Responsive design with Bootstrap 5.
- 📚 Browse books by list or detail view, with language/genre filters.
- 🛒 Cart service in session, with quantity management and total calculation.
- 🔒 Django Allauth for signup/login/logout flows.
- 💳 Stripe PaymentIntent integration for secure payments.
- 📦 Order & OrderItem Django models with foreign-key relations.
- 📜 Order history page with `Mark as Received` and `Delete` actions (Bootstrap modal confirmation).
- 🔔 Global toast notifications for user feedback.
- 📂 Clean project structure with reusable services and DRY code.

---

## 📁 Folder Structure

```text
second_hand_book/
├── books/              # Book catalog app (models, views, templates)
├── cart/               # Cart service and views
├── checkout/           # Checkout, orders models, views, services
│   ├── migrations/
│   ├── models.py
│   ├── services.py
│   ├── views.py
│   └── urls.py
├── templates/          # Global and account templates
│   ├── account/        # login, signup, order_history
│   └── base.html       # site-wide layout
├── static/css/base.css # Core styles with Bootstrap overrides
├── second_hand_book/   # Django project settings, urls, wsgi/asgi
├── manage.py
└── README.md           # Project documentation
```

---

## 💡 Pages Breakdown

### Home (`/`)
- Featured book list

### Books List (`/books/`)
- Paginated grid of books

### Book Detail (`/books/<slug>/`)
- Cover, description, author, price, language
- "Add to Bag" button

### Cart (`/cart/`)
- View items, update quantities, remove items
- Proceed to Checkout

### Checkout (`/checkout/`)
- Payment form powered by Stripe

### Checkout Success (`/checkout/success/`)
- Order summary and confirmation toast

### Order History (`/checkout/history/`)
- List past orders in semantic `<section>`
- Mark as received or delete (with Bootstrap modal)

### Account Flows
- Sign in, Sign up, Sign out pages styled uniformly

---

## 🧰 Technologies Used
- Python 3 & Django 4.2
- Django Allauth for authentication
- Stripe PaymentIntent API for payments
- Bootstrap 5 for responsive UI
- django-summernote for rich-text in admin
- WhiteNoise for static file serving in production
- PostgreSQL (via dj-database-url)

---

## 🚀 Getting Started

1. **Clone the repository**:
   ```sh
   git clone <your-repo-url>
   cd second_hand_book
   ```

2. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (create `.env`):
   ```env
   DJANGO_SECRET_KEY=your-secret-key
   DJANGO_DEBUG=true
   DATABASE_URL=postgres://user:pass@localhost:5432/second_hand_book
   STRIPE_PUBLIC_KEY=pk_test_...
   STRIPE_SECRET_KEY=sk_test_...
   ```

4. **Run migrations**:
   ```sh
   python manage.py migrate
   ```

5. **Create a superuser** (for admin access):
   ```sh
   python manage.py createsuperuser
   ```

6. **Collect static files (for production)**:
   ```sh
   python manage.py collectstatic
   ```

7. **Run the development server**:
   ```sh
   python manage.py runserver
   ```

Open http://localhost:8000 in your browser.

---

## 💳 Stripe Testing

During development, you can test payments using Stripe's test mode with the following details:

- Card number: 4242 4242 4242 4242
- Expiry date: Any valid future date (e.g., 12/34)
- CVC: Any three digits (e.g., 123)
- ZIP: Any five digits (e.g., 12345)

For additional test card numbers and scenarios, see: https://stripe.com/docs/testing

---

## 📬 Contact

Built with care by Christopher Quinones.

For feedback or issues, contact: `517996@waes.ac.uk`.

---

## 🙌 Acknowledgements

- Bootstrap 5
- Stripe API
- Django & Django Allauth
- Unsplash for placeholder images
- Code Institute Guided Walkthrough Projects