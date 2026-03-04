# 📚 Second Hand Book Store

Welcome to **Second Hand Book Store** — a Django-based assessment project providing a full e-commerce flow for browsing, cart management, checkout (with Stripe), and user order history.

🔗 **Live Site:** [https://second-hand-book-57a183b732b9.herokuapp.com/](https://second-hand-book-57a183b732b9.herokuapp.com/)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Intended Users](#-intended-users)
- [User Stories](#-user-stories)
- [Features](#-features)
- [Folder Structure](#-folder-structure)
- [Pages Breakdown](#-pages-breakdown)
- [Screenshots](#-screenshots)
- [Technologies Used](#-technologies-used)
- [Getting Started](#-getting-started)
- [Stripe Testing](#-stripe-testing)
- [Database Schema](#-database-schema)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Contact](#-contact)
- [Acknowledgements](#-acknowledgements)

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

## 📖 User Stories

The main demographic for the site is budget-conscious book lovers and environmentally aware individuals seeking affordable, pre-owned books while supporting sustainable shopping practices.

### Visitors

As a visitor, I would like to see what the second-hand book store offers so I can decide if it's right for me.

As a visitor, I would like to browse the available book collection (by title, author, genre, or language) so I can find books that interest me.

As a visitor, I would like to view detailed book information (cover, description, author, publication date, ISBN, price, language, genre) so I can make informed purchase decisions.

As a visitor, I would like to filter books by language or genre so I can easily find books matching my preferences.

As a visitor, I would like to search for books by title, author, or ISBN so I can quickly locate specific books.

As a visitor, I would like to see book pricing clearly displayed so I can understand the cost before adding to my cart.

As a visitor, I would like the site to be responsive so I can browse comfortably on my phone, tablet, or desktop.

As a visitor, I would like to register an account so I can make purchases and track my order history.

### Registered Users / Book Buyers

As a registered user, I would like to sign in to my account so I can access my shopping cart and order history.

As a registered user, I would like to add books to my shopping cart so I can purchase multiple items at once.

As a registered user, I would like to view my shopping cart with item quantities and prices so I can review my purchase before checkout.

As a registered user, I would like to update quantities in my cart so I can adjust my order before purchasing.

As a registered user, I would like to remove items from my cart so I can change my purchase selection.

As a registered user, I would like to proceed to checkout securely so I can complete my book purchase with confidence.

As a registered user, I would like to make payments via Stripe so I can pay safely using my credit or debit card.

As a registered user, I would like to receive a confirmation message after purchase so I know my order was successfully completed.

As a registered user, I would like to view my order history with past purchases so I can track what I've bought.

As a registered user, I would like to mark orders as received so I can confirm when items arrive.

As a registered user, I would like to delete orders from my history so I can manage my account records.

As a registered user, I would like to sign out of my account so my information stays secure on shared devices.

### Admin / Site Owner

As an admin, I would like to manage all books, orders, and users via the Django admin panel so I can oversee the application.

As an admin, I would like to add, edit, and delete books from the catalog so I can keep the inventory current.

As an admin, I would like to view order details and customer information so I can process and ship orders efficiently.

As an admin, I would like the site to be visually appealing and professional so it attracts customers and builds trust.

As an admin, I would like checkout to be restricted to signed-in users so I can ensure only registered customers make purchases.

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

## 📸 Screenshots

![Screenshot 1](docs/screenshots/Screenshot%202026-03-04%20at%2021.04.41.png)

![Screenshot 3](docs/screenshots/Screenshot%202026-03-04%20at%2021.04.52.png)

![Screenshot 4](docs/screenshots/Screenshot%202026-03-04%20at%2021.05.21.png)

![Screenshot 5](docs/screenshots/Screenshot%202026-03-04%20at%2021.05.46.png)

![Screenshot 6](docs/screenshots/Screenshot%202026-03-04%20at%2021.06.39.png)

![Screenshot 7](docs/screenshots/Screenshot%202026-03-04%20at%2021.07.00.png)

![Screenshot 8](docs/screenshots/Screenshot%202026-03-04%20at%2021.07.12.png)

![Screenshot 9](docs/screenshots/Screenshot%202026-03-04%20at%2021.07.28.png)

![Screenshot 10](docs/screenshots/Screenshot%202026-03-04%20at%2021.07.32.png)

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

## � Database Schema

The complete database schema for this project is documented in [SCHEMA.md](SCHEMA.md). This file contains detailed information about all models, their fields, relationships, and constraints.

---

## 🧪 Testing

All testing and validation evidence for this project is documented in [TESTING.md](TESTING.md). This includes:

- HTML, CSS, JavaScript, and Python validation results
- Lighthouse audit scores
- Manual testing scenarios and outcomes
- Bug tracker with known and resolved issues

Please review [TESTING.md](TESTING.md) for full details.

---

## 🚀 Deployment

### Local Setup

The getting started section above covers the basic local setup. To ensure everything is configured correctly for local development:

1. Verify your `.env` file is set to `DJANGO_DEBUG=true`
2. Use SQLite (default) for local development, or configure PostgreSQL if preferred
3. Run migrations: `python manage.py migrate`
4. Load sample data (optional): `python manage.py loaddata fixtures/my_books.json fixtures/new_books_multilang.json`
5. Start the development server: `python manage.py runserver`

### Heroku Deployment

This project is configured for deployment on Heroku. Follow these steps to deploy:

#### Prerequisites
- Heroku CLI installed and logged in
- Git repository initialized
- All code committed to git

#### Deployment Steps

1. **Create a Heroku app** (if not already created):
   ```sh
   heroku create your-app-name
   ```

2. **Add a PostgreSQL database**:
   ```sh
   heroku addons:create heroku-postgresql:essential-0
   ```
   Heroku automatically sets the `DATABASE_URL` environment variable.

3. **Set environment variables** on Heroku:
   ```sh
   heroku config:set DJANGO_SECRET_KEY=your-secret-key
   heroku config:set DJANGO_DEBUG=false
   heroku config:set STRIPE_PUBLIC_KEY=pk_live_...
   heroku config:set STRIPE_SECRET_KEY=sk_live_...
   ```

4. **Deploy to Heroku**:
   ```sh
   git push heroku main
   ```
   The `Procfile` automatically runs:
   - Release phase: `python manage.py migrate` (runs migrations before app starts)
   - Web dyno: `gunicorn second_hand_book.wsgi --log-file -`

5. **Collect static files**:
   - Static files are automatically collected during deployment via the `Procfile` release phase.
   - The project uses WhiteNoise middleware for serving static files in production.

6. **Create a superuser** (for admin access on Heroku):
   ```sh
   heroku run python manage.py createsuperuser
   ```

7. **Open your app**:
   ```sh
   heroku open
   ```

#### Environment Configuration

Heroku uses the following configuration:
- **Python version**: 3.12 (specified in `runtime.txt`)
- **WSGI server**: Gunicorn
- **Database**: PostgreSQL (Heroku Postgres)
- **Static files**: WhiteNoise middleware with S3 or local serving options

#### Important Notes

- Always use `DJANGO_DEBUG=false` in production
- Use Heroku's environment variable system (never commit `.env` files)
- Keep your Stripe keys separate for development (pk_test_, sk_test_) and production (pk_live_, sk_live_)
- Monitor logs with: `heroku logs --tail`
- Scale dynos if needed with: `heroku ps:scale web=2`

---

## �📬 Contact

Built with care by Christopher Quinones.

For feedback or issues, contact: `517996@waes.ac.uk`.

---

## 🙌 Acknowledgements

- Bootstrap 5
- Stripe API
- Django & Django Allauth
- Unsplash for placeholder images
- Code Institute Guided Walkthrough Projects