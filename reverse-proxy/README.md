# reverse-proxy

Entry point for the stack — **Caddy** for automatic HTTPS and a single,
controlled access gate in front of the frontend and api.

**Image:** official `caddy` (configured via a `Caddyfile`).

**Responsibilities**
- Terminates TLS (automatic HTTPS via Caddy).
- Forwards traffic to the frontend and api instead of exposing every service
  port to the host.
