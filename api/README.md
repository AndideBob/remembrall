# api

FastAPI service — orchestration, auth, and public HTTP endpoints.

**Language:** Python (FastAPI)

**Responsibilities**
- Public endpoints: `/upload`, `/documents`, `/chat`, `/documents/{id}` (delete).
- Single-user authentication as swappable middleware (hashed password).
- Orchestrates the ingestion, vector-db, and llm-gateway services over the
  internal Docker network — it does not import them as libraries.
