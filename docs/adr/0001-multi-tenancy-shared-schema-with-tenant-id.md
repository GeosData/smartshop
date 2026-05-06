# ADR-001: Multi-tenancy via shared schema with `tenant_id` column

- **Status:** Accepted
- **Date:** 2026-04-14
- **Deciders:** jotive

## Context

SmartShop targets small businesses (retailers, restaurants, salons) with a **freemium → paid** model. Many of those businesses will share one production instance. Tenant counts could grow into the hundreds or thousands; per-tenant data volume stays small (most shops handle 100–10k products and a few hundred sales per week).

The platform needs:

- Strong logical isolation (tenant A never sees tenant B's data).
- Cheap onboarding (creating a tenant = inserting a row, not provisioning a schema or a DB).
- Backups and migrations that scale with tenant count without becoming an operational burden.
- Acceptable cost at small scale (the first 100 tenants might generate < $50/mo combined).

Three realistic options:

1. **Database per tenant** — each tenant has its own PostgreSQL DB.
2. **Schema per tenant** — one DB, one schema per tenant.
3. **Shared schema with `tenant_id` column** — one DB, one schema, every row carries a `tenant_id`.

## Options compared

| Dimension | DB per tenant | Schema per tenant | Shared schema + `tenant_id` |
|---|---|---|---|
| Onboarding cost | High — provision DB, run migrations, manage credentials | Medium — run migrations on new schema | Trivial — `INSERT INTO tenants` |
| Migration ops | Run N times (or run a fan-out tool) | Run N times across schemas | Run once |
| Backup ops | One backup per tenant. Granular but expensive. | One DB backup covers all tenants but per-tenant restore is awkward. | Single backup. Per-tenant restore needs row-level export. |
| Hard isolation (tenant A binary cannot reach tenant B data) | Strongest | Strong (with role per schema) | Weakest — depends on application correctness |
| Cost at 1k tenants | High (1k DBs, 1k connection pools) | Medium-high (1k schemas, shared pool but planner overhead) | Low (1 schema, 1 pool) |
| Noisy-neighbor risk | None | Low | Higher — one tenant's burst can affect others |
| Per-tenant export | Native | Native (`pg_dump --schema`) | Custom export logic |
| Compliance fit (PII residency, regulated industries) | Best | Good | Weakest |

## Decision

**Shared schema with `tenant_id` column on every domain row.**

The driver is **onboarding cost at the target scale**. SmartShop's economic model is small businesses with low ACV; tenants need to be created in seconds for a freemium signup, not provisioned over minutes. Database-per-tenant breaks that flow and adds operational debt that does not pay back at this ACV.

The secondary driver is **migration sanity**. Schema-per-tenant means every Alembic migration ships across N schemas; tooling exists but adds complexity for no functional gain at this customer profile. Shared schema is a single migration target.

We accept the **hard isolation trade-off** by enforcing `tenant_id` filtering at the framework boundary:

- Every model under `app/models/` carries a `tenant_id: str` indexed column.
- Composite indexes are tenant-scoped: `ix_products_tenant_sku UNIQUE (tenant_id, sku)`, not just `(sku)`.
- Repository / service layer takes `tenant_id` as the first parameter and never accepts it from request body — only from the authenticated principal claims.
- Tests verify cross-tenant queries return empty (no leak path).

We accept **noisy-neighbor risk** as a problem to solve later via Postgres-level rate limits (`pg_stat_activity` + connection caps per tenant) and Redis-level rate limits, not via architecture change.

## Consequences

**Positive:**

- Tenants onboard in milliseconds.
- Single migration target across the whole platform.
- Connection pool shared, lower memory footprint at scale.
- Cross-tenant aggregations (admin reports, platform metrics) are trivial SQL.

**Negative:**

- Application correctness owns isolation. A buggy query without `tenant_id` filter is a leak. We mitigate with: tenant context middleware, repository pattern that injects the filter, and tests that assert isolation.
- A noisy tenant can degrade others. Mitigate later with rate limits, not architecture.
- Per-tenant restore needs custom logic.

## Revisit when

- A regulated tenant (healthcare, finance) needs **schema-level isolation** for compliance — moves to schema-per-tenant for that subset.
- A single tenant generates > 10x platform-wide load → consider promoting to its own DB instance.
- Cross-tenant query performance degrades despite indexes → consider partitioning on `tenant_id`.

## References

- [Microsoft — Multi-tenant SaaS database tenancy patterns](https://learn.microsoft.com/azure/azure-sql/database/saas-tenancy-app-design-patterns)
- [Stripe Platform Engineering on multi-tenancy trade-offs](https://stripe.com/blog/online-migrations) (related: online migration patterns)
- [PostgreSQL row-level security as a complement to `tenant_id` filtering](https://www.postgresql.org/docs/current/ddl-rowsecurity.html) — possible defense-in-depth upgrade path.
