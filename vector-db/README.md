# vector-db

Vector database — **Chroma**, run as its own container in server mode.

**Image:** official `chromadb/chroma` (no custom code needed to start).

**Responsibilities**
- Stores document embeddings; queried by the ingestion and api services over the
  internal Docker network (`http://vector-db:8000`).
- Data persisted to a named Docker volume so it survives `docker compose down`.

This folder holds any Chroma-specific config or init scripts; the service itself
is configured in the root `docker-compose.yml`.
