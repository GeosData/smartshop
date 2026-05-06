# ADR-002: JWT bearer tokens over server-side session cookies

- **Status:** Accepted
- **Date:** 2026-04-14
- **Deciders:** jotive

## Context

SmartShop has a web frontend (Next.js / SPA on Vercel) and an API (FastAPI on Railway) on different origins. It will likely have a mobile client later (Flutter, native, or a PWA). Owners and staff log in once and use the system for full work shifts. The user count per tenant is small (typically 1–10), so identity infra cost is dominated by simplicity and operational cost, not throughput.

We need an auth scheme that:

- Works across origins (frontend ≠ API domain) without CORS-cookie pain.
- Does not require sticky sessions or shared session storage between API replicas.
- Survives a mobile client without a second auth flow.
- Has clear, documented logout / rotation semantics.

Realistic options:

1. **JWT bearer tokens** — stateless, signed, sent in `Authorization: Bearer`.
2. **Server-side session cookies** — opaque ID, server keeps the state in Redis/DB.
3. **Hybrid** — short-lived JWT access + opaque refresh token in cookie.

## Options compared

| Dimension | JWT bearer | Session cookies | Hybrid |
|---|---|---|---|
| Cross-origin ergonomics | Simple — `Authorization` header. | CORS + `SameSite=None` + `Secure`, fights with browsers. | Same as cookies for refresh, simple for access. |
| Stateless API | Yes — verify signature, no DB read. | No — every request hits session store. | Mostly stateless on hot path. |
| Scaling | Scales horizontally without shared state. | Needs shared session store (Redis). | Needs Redis only on refresh. |
| Logout semantics | Hard — token valid until expiry unless we keep a denylist. | Easy — delete session. | Medium — short access expiry mitigates, refresh denylist on logout. |
| Mobile client | Native fit. | Cookie-based mobile is awkward. | Native fit. |
| Token theft blast radius | Large (until expiry). | Small (server can revoke). | Medium — short-lived access bounds the blast. |
| Implementation cost | Low (`python-jose`). | Medium (session store, CSRF). | Higher (two artifacts, refresh flow, denylist). |
| Operational cost | Lowest. | Adds a Redis dependency just for sessions. | Adds Redis. |

## Decision

**JWT bearer tokens for the v1 of SmartShop.**

The driver is **stateless API + cross-origin simplicity**. Frontend on Vercel + API on Railway is the default deployment; cookies across those domains require `SameSite=None; Secure`, which is fragile across browsers and adds CORS complexity for no product benefit at this scale.

The secondary driver is **mobile readiness**. JWT in `Authorization` works identically for web and a future Flutter client. No second auth flow.

We accept the **logout blast-radius trade-off**:

- Access tokens are short-lived (default 60 min, configurable per environment).
- We do not implement a denylist in v1 — the cost (Redis lookup on every request) is not justified at our user count and threat model.
- "Force logout" for a compromised account is solved by **rotating the user's password**, which invalidates future logins; existing tokens expire within the access TTL.
- A future v2 may add hybrid (short access + opaque refresh with denylist) when account-takeover risk grows.

We do **not** put a refresh token in v1. The complexity of refresh flow + theft-detection (rotation, family reuse) is overkill for shifts-of-the-day usage where re-login once a shift is acceptable UX.

## Consequences

**Positive:**

- Hot-path auth is a signature verify, no Redis call.
- One auth flow for web and mobile.
- API horizontal scaling has no shared-state requirement for auth.
- `python-jose` + `bcrypt` is well-trodden, low custom code.

**Negative:**

- Cannot revoke a single token before expiry without adding a denylist (deferred).
- Token in `localStorage` is XSS-exposed on the frontend; mitigated by CSP, no third-party JS, and HttpOnly is unavailable for non-cookie storage. Acceptable at current threat model; revisit when we onboard a tenant that handles regulated data.
- Tokens carry claims; growth in claim payload affects every request. We keep claims minimal (`sub`, `tenant_id`, `role`, `exp`).

## Revisit when

- Account-takeover incidents occur or tenant compliance demands per-token revocation → add hybrid (short access + opaque refresh with rotation + denylist).
- A tenant with regulated data joins → consider HttpOnly cookie + CSRF token for that tenant subset.
- Token claims grow beyond ~512 bytes routinely → move heavy data out of the token, fetch on demand.

## References

- [Auth0 — When to use JWTs vs sessions](https://auth0.com/blog/cookies-vs-tokens-definitive-guide/)
- [OWASP — JWT cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)
- [PortSwigger — JWT attacks](https://portswigger.net/web-security/jwt) — informs claim minimization and validation rules.
