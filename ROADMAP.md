# Roadmap — SmartShop

Plan público. Items concretos, no ideas. Si no está acá, no está commited.

> Decisions: [`docs/adr/`](docs/adr/) · Event log: [`TRACE.md`](TRACE.md)

## Now (alpha — 2026-05)

- [x] Multi-tenant data model (Product, Sale, SaleItem, User scoped by `tenant_id`)
- [x] JWT auth (owner / staff roles, bcrypt password hashing)
- [x] Product CRUD with low-stock detection (`is_low_stock` derived from `stock <= min_stock`)
- [x] Sales processing with multi-item transactions and atomic stock deduction
- [x] PostgreSQL 16 + SQLAlchemy 2 async + Alembic migrations
- [x] Redis dependency wired (session/cache/rate-limit ready)
- [x] FastAPI app with lifespan + structured config
- [x] Live demo deployed (Vercel frontend + Railway API)
- [x] ADR-001: multi-tenancy strategy
- [x] ADR-002: JWT auth strategy

## Next (next 30 days)

- [ ] **Test coverage push to 70%** — current `tests/` covers health only. Priority targets: products CRUD with multi-tenant isolation assertions, sales pipeline (stock deduction + transaction rollback on insufficient stock), auth (JWT issuance + claim validation + role gates).
- [ ] **ADR-003**: rate limiting strategy (token bucket via Redis Lua, fail-open vs fail-closed).
- [ ] **Rate limiting middleware** — tenant-scoped, sliding window, configurable per endpoint class.
- [ ] **Stock movement audit log** — every change (sale, manual adjustment, reorder) recorded immutably.
- [ ] **Soft delete consistency** — confirm cascading behavior across products with sale history.
- [ ] **Improve error model** — RFC 7807 problem+json across all error responses.

## Later (60–90 days)

- [ ] **WhatsApp alerts** — low-stock notifications via WhatsApp Business API. Requires onboarding flow for tenant phone number + opt-in audit.
- [ ] **Demand forecasting v0** — weekly reorder recommendations from sales history (start with simple moving average + seasonality, defer ML until justified by data).
- [ ] **Real-time dashboard** — WebSocket-powered inventory updates per tenant.
- [ ] **OpenTelemetry tracing** — spans across auth → handler → repo → DB / Redis.
- [ ] **Cost dashboard** — per-tenant request count, latency, and storage to inform pricing tiers.
- [ ] **Export per tenant** — CSV / Excel export of products + sales history.

## Won't do (yet)

- **Multi-currency** — single currency per tenant is enough for the target market.
- **Marketplace / e-commerce frontend** — out of scope; SmartShop is the back-of-house tool, not the storefront.
- **Native mobile apps** — PWA on the existing frontend covers in-store use cases until usage data justifies native.
- **Marketplace payments / split payments** — until a tenant requires it.
- **Built-in BI** — exports + warehouse integration are enough; dashboards are not the product.

## Revisit conditions

- If multi-tenant isolation tests find a leak → ADR-001 may add row-level security as defense-in-depth.
- If account-takeover incidents occur → ADR-002 evolves to hybrid auth (short access + refresh with rotation).
- If a real customer asks for WhatsApp alerts before the demand forecasting work → swap order in Later.
- If test coverage stalls below 70% for > 14 days → reduce scope of "Next" until coverage gap is closed; tests block new features.

---

*Tracked alongside [`TRACE.md`](TRACE.md) (structured events) and decisions under [`docs/adr/`](docs/adr/).*
