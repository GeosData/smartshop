# SmartShop

Backend for local businesses: inventory, sales, WhatsApp alerts, and demand forecasting.

Built with **FastAPI**, **PostgreSQL**, **Redis**, and **Docker**. Designed for small retailers, restaurants, salons, and service shops that currently run on spreadsheets or paper.

## Features

- **Product management** — CRUD with categories, SKU tracking, soft delete
- **Inventory control** — Real-time stock tracking with low-stock detection
- **Sales processing** — Multi-item transactions with automatic stock deduction and validation
- **Multi-tenant** — Tenant isolation for multiple businesses on one instance
- **Multi-role auth** — Owner and staff roles with JWT authentication
- **WhatsApp alerts** — Low-stock notifications via WhatsApp Business API *(planned)*
- **Demand forecasting** — Weekly reorder recommendations based on sales history *(planned)*
- **Real-time dashboard** — WebSocket-powered inventory updates *(planned)*

## Tech Stack

| Layer | Technology |
|---|---|
| **API** | FastAPI, Pydantic v2 |
| **Database** | PostgreSQL 16, SQLAlchemy 2 (async), Alembic |
| **Cache/Queue** | Redis 7 |
| **Auth** | JWT (python-jose), bcrypt |
| **Logging** | structlog (JSON) |
| **Infra** | Docker, Docker Compose, GitHub Actions CI |
| **Testing** | pytest, pytest-asyncio, httpx, coverage |
| **Linting** | Ruff, mypy |

## Quick Start

```bash
git clone https://github.com/GeosData/smartshop.git
cd smartshop
cp .env.example .env
make dev
# API docs at http://localhost:8000/docs
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/api/v1/products/` | Create product |
| `GET` | `/api/v1/products/` | List products (paginated, filterable) |
| `GET` | `/api/v1/products/{id}` | Get product |
| `PATCH` | `/api/v1/products/{id}` | Update product |
| `DELETE` | `/api/v1/products/{id}` | Soft delete product |
| `POST` | `/api/v1/sales/` | Create sale (multi-item, stock validation) |
| `GET` | `/api/v1/sales/{id}` | Get sale with items |

## Project Structure

```
smartshop/
├── app/
│   ├── main.py          # FastAPI application
│   ├── config.py        # Settings (Pydantic)
│   ├── database.py      # SQLAlchemy async engine
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── api/             # Route handlers
│   └── services/        # Business logic
├── tests/
├── alembic/             # Database migrations
├── docker-compose.yml
├── Dockerfile
├── Makefile
└── pyproject.toml
```

## Development

```bash
make lint          # Check code style
make format        # Auto-format
make type-check    # mypy strict mode
make test          # Run tests with coverage
make migration msg="add orders table"
make migrate       # Apply migrations
```

## Roadmap

- [x] Project scaffolding + Docker setup
- [x] Product CRUD with pagination and filters
- [x] Sales with multi-item transactions and stock validation
- [ ] JWT authentication with owner/staff roles
- [ ] Alembic initial migration
- [ ] Integration tests with real database
- [ ] WhatsApp alerts for low-stock (Twilio)
- [ ] Weekly sales reports endpoint
- [ ] Demand forecasting with Pandas
- [ ] WebSocket real-time inventory dashboard
- [ ] GitHub Actions CI pipeline

---

*Built by [jotive](https://github.com/jotive) | [dev.jotive.com.co](https://dev.jotive.com.co) | [GeosData](https://geosdata.com)*
