# 📊 Database Schema

This document outlines the database schema for the Second Hand Book Store project. The database uses Django's ORM with PostgreSQL as the primary database.

---

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                          User (Django Auth)                     │
│  ─────────────────────────────────────────────────────────────  │
│  id (PK)              | AutoField                               │
│  username             | CharField(150)                          │
│  email                | EmailField                              │
│  password             | CharField                               │
│  first_name           | CharField(150, blank)                   │
│  last_name            | CharField(150, blank)                   │
└──────────┬────────────────────────────────────────────────────────┘
           │
           │ 1:N (ForeignKey, CASCADE)
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│                           Order                                 │
│  ─────────────────────────────────────────────────────────────  │
│  id (PK)              | AutoField                               │
│  user (FK)            | ForeignKey → User (CASCADE)             │
│  order_date           | DateTimeField (auto_now_add)            │
│  total_amount         | DecimalField(10, 2)                     │
│  status               | CharField(50, default="Processing")     │
│  received             | BooleanField(default=False)             │
└──────────┬────────────────────────────────────────────────────────┘
           │
           │ 1:N (ForeignKey, CASCADE via "items")
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│                         OrderItem                               │
│  ─────────────────────────────────────────────────────────────  │
│  id (PK)              | AutoField                               │
│  order (FK)           | ForeignKey → Order (CASCADE)            │
│  book (FK)            | ForeignKey → Book (PROTECT)             │
│  quantity             | PositiveIntegerField                    │
│  price_at_purchase    | DecimalField(10, 2)                     │
└──────────┬────────────────────────────────────────────────────────┘
           │
           │ N:1 (ForeignKey, PROTECT)
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│                          Book                                   │
│  ─────────────────────────────────────────────────────────────  │
│  id (PK)              | AutoField                               │
│  title                | CharField(200)                          │
│  author               | CharField(200)                          │
│  slug                 | SlugField(200, unique)                  │
│  isbn                 | CharField(13, unique)                   │
│  description          | TextField(blank)                        │
│  price                | DecimalField(8, 2, default=0)           │
│  published_date       | DateField(null, blank)                  │
│  genre                | CharField(50, choices)                  │
│  language             | CharField(5, choices)                   │
│  cover                | ImageField(upload_to, null, blank)      │
│  cover_path           | CharField(255, null, blank)             │
│  created_at           | DateTimeField(auto_now_add)             │
│  updated_at           | DateTimeField(auto_now_add)             │
└─────────────────────────────────────────────────────────────────┘
```

---

## Model Details

### 1. User (Django Built-in)

**Location:** `django.contrib.auth.models`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | AutoField | Primary Key | Unique user identifier |
| `username` | CharField(150) | Unique | Login username |
| `email` | EmailField | Unique | User email address |
| `password` | CharField | Hashed | Encrypted password |
| `first_name` | CharField(150) | Optional | User's first name |
| `last_name` | CharField(150) | Optional | User's last name |
| `is_active` | BooleanField | default=True | Account activation status |
| `is_staff` | BooleanField | default=False | Staff member status |

**Relationships:**
- `orders` (Reverse): One User → Many Orders (CASCADE delete)

---

### 2. Book

**Location:** `books/models.py`

**Purpose:** Represents a book in the catalog with pricing, metadata, and cover information.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| `id` | AutoField | Primary Key | Unique book identifier |
| `title` | CharField(200) | Required | Book title |
| `author` | CharField(200) | Required | Author name |
| `slug` | SlugField(200) | Unique | URL-friendly identifier (auto-generated) |
| `isbn` | CharField(13) | Unique | International Standard Book Number |
| `description` | TextField | Blank=True | Full book description |
| `price` | DecimalField(8,2) | default=0 | Price in USD (max: $999,999.99) |
| `published_date` | DateField | null, blank | Date of publication |
| `genre` | CharField(50) | choices | One of 11 genres (Fiction, Fantasy, etc.) |
| `language` | CharField(5) | choices | One of 5 languages (en, es, de, it, sv) |
| `cover` | ImageField | null, blank | Book cover image upload |
| `cover_path` | CharField(255) | null, blank | Static path for WhiteNoise serving |
| `created_at` | DateTimeField | auto_now_add | Timestamp when book added to catalog |
| `updated_at` | DateTimeField | auto_now_add | Timestamp when book last modified |

**Genre Choices:**
```python
("fiction", "Fiction")
("non_fiction", "Non-Fiction")
("fantasy", "Fantasy")
("sci_fi", "Sci-Fi")
("mystery", "Mystery")
("biography", "Biography")
("history", "History")
("children", "Children")
("romance", "Romance")
("classics", "Classics")
("other", "Other")
```

**Language Choices:**
```python
("en", "English")
("es", "Spanish")
("de", "German")
("it", "Italian")
("sv", "Swedish")
```

**Methods:**
- `__str__()`: Returns `"[title] by [author]"`
- `save()`: Auto-generates slug from title if not provided

**Relationships:**
- `orderitem_set` (Reverse): One Book → Many OrderItems (PROTECT delete)

---

### 3. Order

**Location:** `checkout/models.py`

**Purpose:** Represents a customer purchase transaction with order details and status tracking.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| `id` | AutoField | Primary Key | Unique order identifier |
| `user` | ForeignKey(User) | CASCADE | Reference to the customer |
| `order_date` | DateTimeField | auto_now_add | Timestamp of purchase |
| `total_amount` | DecimalField(10,2) | Required | Total order value (max: $99,999,999.99) |
| `status` | CharField(50) | default="Processing" | Order status (Processing, Completed, etc.) |
| `received` | BooleanField | default=False | Customer confirmation of receipt |

**Methods:**
- `__str__()`: Returns `"Order #[id] by [email] – [status]"`

**Relationships:**
- `user` (Foreign Key): Many Orders → One User (CASCADE delete)
- `items` (Reverse): One Order → Many OrderItems (CASCADE delete via related_name)

---

### 4. OrderItem

**Location:** `checkout/models.py`

**Purpose:** Represents individual line items (book + quantity) in an order. Acts as a junction table between Order and Book.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| `id` | AutoField | Primary Key | Unique order item identifier |
| `order` | ForeignKey(Order) | CASCADE | Reference to parent order |
| `book` | ForeignKey(Book) | PROTECT | Reference to purchased book |
| `quantity` | PositiveIntegerField | Required | Number of copies ordered |
| `price_at_purchase` | DecimalField(10,2) | Required | Price of book at time of purchase |

**Methods:**
- `__str__()`: Returns `"[qty]×[title] (Order [order_id])"`

**Relationships:**
- `order` (Foreign Key): Many OrderItems → One Order (CASCADE delete)
- `book` (Foreign Key): Many OrderItems → One Book (PROTECT delete)

**Notes:**
- Uses PROTECT on Book deletion to preserve order history
- `price_at_purchase` captures the book price at time of order (accounts for price changes)

---

## Key Design Decisions

### 1. **Cascade vs. Protect Relationships**
- **Order → User**: CASCADE
  - Rationale: If a user is deleted, their orders should also be deleted (clear audit trail)
- **OrderItem → Order**: CASCADE
  - Rationale: Order items are meaningless without their parent order
- **OrderItem → Book**: PROTECT
  - Rationale: Books should never be deleted if they appear in order history (data integrity)

### 2. **Price Storage**
- `Book.price`: Current catalog price
- `OrderItem.price_at_purchase`: Historical price at purchase time
- Rationale: Allows books to change price without affecting historical order data

### 3. **Slug Field**
- Auto-generated from title in `Book.save()`
- Used for clean URLs (`/books/[slug]/`)
- Unique constraint ensures one URL per book

### 4. **Cover Images**
- `cover`: ImageField for uploads
- `cover_path`: CharField for static files (WhiteNoise serving)
- Rationale: Supports both upload and pre-generated cover paths

### 5. **Stateless Cart**
- Cart stored in session (not in database)
- No Cart model needed
- Simpler for single-user per session

---

## Indexes

Django automatically creates indexes on:
- Primary keys (`id`)
- Foreign keys (`user`, `order`, `book`)
- Fields with `unique=True` (`slug`, `isbn`)

**Recommended additional indexes for performance:**
- `Order.order_date` (filtering by date range)
- `Book.genre` and `Book.language` (filtering operations)

---

## Migration History

Run `python manage.py showmigrations` to view all applied migrations:
- `0001_initial.py` — Initial Book model
- `0002_book_description.py` — Add description field
- `0003_book_cover.py` — Add cover image support
- `0004_...` — Add genre, language, price fields
- `0005_...` — Update datetime fields

Checkout migrations:
- `0001_initial.py` — Initial Order and OrderItem models
- `0002_order_received.py` — Add received field to Order

---

## Database Constraints

| Constraint | Type | Purpose |
|-----------|------|---------|
| `Book.slug` | UNIQUE | Ensure clean, unique URLs |
| `Book.isbn` | UNIQUE | ISBN standard compliance |
| `User.username` | UNIQUE | Django auth requirement |
| `User.email` | UNIQUE | Email uniqueness for auth |
| `OrderItem.quantity` | POSITIVE | Cannot order negative quantities |
| `Order.total_amount` | DECIMAL(10,2) | Accurate monetary calculations |

---

*Database schema documented for assessment purposes — March 2026*
