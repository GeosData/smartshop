# SmartShop

Backend for local businesses: inventory, sales, WhatsApp alerts, and demand forecasting.

Built with **FastAPI**, **PostgreSQL**, **Redis**, and **Docker**. Designed for small retailers, restaurants, salons, and service shops that currently run on spreadsheets or paper.

## Live Demo

- **Frontend:** [smartshop-jotivegmailcoms-projects.vercel.app](https://smartshop-jotivegmailcoms-projects.vercel.app)
- **API Docs:** [smartshop-api-production-24de.up.railway.app/docs](https://smartshop-api-production-24de.up.railway.app/docs)

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

## Architecture decisions

The non-obvious calls are documented as ADRs under [`docs/adr/`](docs/adr/):

- [ADR-001: Multi-tenancy via shared schema with `tenant_id`](docs/adr/0001-multi-tenancy-shared-schema-with-tenant-id.md) — why we accept the application-level isolation trade-off instead of database-per-tenant.
- [ADR-002: JWT bearer tokens over session cookies](docs/adr/0002-jwt-auth-over-session-cookies.md) — why stateless tokens for v1, with the logout trade-off bounded by short access TTL.

## Roadmap

Full plan, milestones, and revisit conditions in [`ROADMAP.md`](ROADMAP.md). Structured event log in [`TRACE.md`](TRACE.md).

---

*Built by [jotive](https://github.com/jotive) | [dev.jotive.com.co](https://dev.jotive.com.co) | [GeosData](https://geosdata.com)*
