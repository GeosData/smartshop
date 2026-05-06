# TRACE — SmartShop

Append-only structured log. Cross-project decisions, locks, kills, pivots. Newest at top.

> Decisions in detail: [`docs/adr/`](docs/adr/) · Future plan: [`ROADMAP.md`](ROADMAP.md)

Types: `DECISION` | `EVENT` | `MILESTONE` | `KILL` | `PIVOT` | `LOCK` | `BLOCKER`

---

## 2026-05-05 — MILESTONE — Open-sourced + ADR-001 + ADR-002 + project hygiene

Repo flipped from private to public on GeosData org.

Pre-flip additions:

- `docs/adr/0001-multi-tenancy-shared-schema-with-tenant-id.md` — documents the shared-schema choice with explicit trade-offs (DB-per-tenant vs schema-per-tenant vs shared) and revisit conditions.
- `docs/adr/0002-jwt-auth-over-session-cookies.md` — documents JWT bearer over cookies / hybrid for v1, with the logout blast-radius accepted and bounded by short-lived tokens.
- `ROADMAP.md` — Now / Next / Later / Won't do, with revisit conditions.
- This `TRACE.md`.

Test coverage at flip: minimal (`test_health.py` only). Acknowledged in `ROADMAP.md` as the top priority for the next 30 days. Shipped honest rather than waiting for full coverage.

Reasons for ship-now:
- The architecture is in place; the ADRs encode the thinking behind it.
- Visible trajectory of next commits is more valuable than perfect first impression.
- Counter-action to the "5 aspirational repos" anti-pattern (3 of which were vapor).

## 2026-04-14 — EVENT — Initial scaffold pushed

Stack laid out: FastAPI 0.115 + SQLAlchemy 2 async + Alembic + Redis + JWT auth + Docker Compose. Multi-tenant data model with `tenant_id` indexed on every domain row. Composite unique index `(tenant_id, sku)` on products. Owner / staff role split on users.

Frontend (Next.js / Vercel) and backend (Railway) deployed at:
- `https://smartshop-jotivegmailcoms-projects.vercel.app`
- `https://smartshop-api-production-24de.up.railway.app/docs`

## 2026-04-14 — DECISION — Multi-tenancy: shared schema with `tenant_id`

Chosen for onboarding cost and migration sanity at the target customer profile (small businesses, low ACV, fast freemium signup). Hard isolation trade-off accepted, mitigated by tenant-scoped indexes, repository-layer filter injection, and isolation tests planned.

Documented later as ADR-001 (2026-05-05). See `docs/adr/0001-multi-tenancy-shared-schema-with-tenant-id.md`.

## 2026-04-14 — DECISION — Auth: JWT bearer over session cookies

Chosen for cross-origin simplicity (Vercel frontend ≠ Railway API) and mobile readiness (one auth flow). Logout blast-radius accepted, bounded by short access TTL. No refresh token in v1.

Documented later as ADR-002 (2026-05-05). See `docs/adr/0002-jwt-auth-over-session-cookies.md`.

## 2026-04-14 — DECISION — Domain rows are tenant-scoped at the index level, not just the column

`ix_products_tenant_sku UNIQUE (tenant_id, sku)`, `ix_products_tenant_category (tenant_id, category)`. SKUs collide globally across tenants but are unique within a tenant. This is also a defense-in-depth signal: a query that forgets `tenant_id` cannot accidentally hit the unique-constraint path that exists.
