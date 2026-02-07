# Hotel Admin Platform - Backend API

A FastAPI-based REST API for managing hotels, room types, and rate adjustments.

## Tech Stack

- **Framework:** FastAPI
- **Database:** SQLite (default) / PostgreSQL
- **ORM:** SQLAlchemy 2.x
- **Migrations:** Alembic
- **Auth:** JWT (python-jose) + bcrypt

## Setup

### 1. Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Environment variables (optional)

Create a `.env` file in the project root:

```env
DATABASE_URL=sqlite:///./hotel.db
SECRET_KEY=your-secret-key-change-in-production-min-32-chars
```

### 4. Seed the database

```bash
python seed.py
```

Default credentials:

- **Email:** admin@hotel.com
- **Password:** password123

### 5. Run the server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

## API Endpoints

### Auth

| Method | Endpoint      | Description |
| ------ | ------------- | ----------- |
| POST   | `/auth/login` | Login       |

### Hotels

| Method | Endpoint       | Description     |
| ------ | -------------- | --------------- |
| GET    | `/hotels`      | List all hotels |
| GET    | `/hotels/{id}` | Get hotel by ID |
| POST   | `/hotels`      | Create hotel    |
| PUT    | `/hotels/{id}` | Update hotel    |
| DELETE | `/hotels/{id}` | Delete hotel    |

### Room Types

| Method | Endpoint                       | Description            |
| ------ | ------------------------------ | ---------------------- |
| GET    | `/room-types`                  | List room types        |
| GET    | `/room-types/{id}`             | Get room type details  |
| POST   | `/room-types`                  | Create room type       |
| PUT    | `/room-types/{id}`             | Update room type       |
| DELETE | `/room-types/{id}`             | Delete room type       |
| POST   | `/room-types/{id}/adjustments` | Create rate adjustment |
| GET    | `/room-types/{id}/adjustments` | List rate adjustments  |

> All endpoints except `/auth/login`, `/health`, and `/` require a Bearer token.

## Database & Migrations

This project uses **SQLAlchemy** as ORM and **Alembic** for database migrations. Tables are auto-created on app startup via `Base.metadata.create_all()`.

### Database Schema

```
users
├── id          (PK)
├── email       (unique)
├── hashed_password
├── full_name
└── is_active

hotels
├── id          (PK)
├── name
├── address
├── city
├── country
├── description
└── status      ("active" / "inactive")

room_types
├── id          (PK)
├── hotel_id    (FK → hotels.id)
├── name
├── description
├── base_rate
└── capacity

rate_adjustments
├── id              (PK)
├── room_type_id    (FK → room_types.id)
├── adjustment_amount
├── effective_date
├── reason
└── created_at
```

### Alembic Migrations

```bash
# Run all migrations
alembic -c alembic/alembic.ini upgrade head

# Rollback one migration
alembic -c alembic/alembic.ini downgrade -1

# Generate a new migration (after model changes)
alembic -c alembic/alembic.ini revision --autogenerate -m "description"

# View current migration status
alembic -c alembic/alembic.ini current

# View migration history
alembic -c alembic/alembic.ini history
```

### Existing Migrations

| Migration        | Description                                                        |
| ---------------- | ------------------------------------------------------------------ |
| `001_initial`    | Creates `users`, `hotels`, `room_types`, `rate_adjustments` tables |
| `002_add_status` | Adds `status` column to `hotels` table                             |

### Reset Database

```bash
# Delete the SQLite database and re-seed
rm -f hotel.db
python seed.py
```

### Switch to PostgreSQL

Update `.env`:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/hotel_admin
```

## Project Structure

```
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── api/
│   │   ├── auth.py          # Auth routes
│   │   ├── hotels.py        # Hotel CRUD routes
│   │   └── room_types.py    # Room type & rate adjustment routes
│   ├── core/
│   │   ├── config.py        # App settings
│   │   └── security.py      # JWT & password hashing
│   ├── db/
│   │   └── session.py       # Database engine & session
│   ├── models/
│   │   ├── hotel.py         # Hotel model
│   │   ├── room_type.py     # RoomType model
│   │   ├── rate_adjustment.py # RateAdjustment model
│   │   └── user.py          # User model
│   └── schemas/
│       ├── auth.py          # Auth schemas
│       ├── hotel.py         # Hotel schemas
│       └── room_type.py     # RoomType & RateAdjustment schemas
├── alembic/                 # Database migrations
├── seed.py                  # Database seeder
└── requirements.txt
```
# hotel_admin_platform_backend
