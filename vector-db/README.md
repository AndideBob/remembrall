# vector-db

Vector database — **Chroma**, run as its own container in server mode.

**Image:** official `chromadb/chroma` (no custom code needed to start).

**Responsibilities**
- Stores document embeddings; queried by the ingestion and api services over the
  internal Docker network (`http://vector-db:8000`).
- Data persisted to a named Docker volume so it survives `docker compose down`.

This folder holds any Chroma-specific config or init scripts; the service itself
is configured in the root `docker-compose.yml`.

## Inspecting the database (local development)

The database is **not exposed to the host**. To browse collections and stored
embeddings, a `chroma-admin` service (the `chromadb-admin` web UI) runs on the
internal network alongside the stack and is the only part published to the host.

1. Start the stack:

   ```bash
   docker compose up -d
   ```

2. Open the admin UI at <http://localhost:3001>.

3. When prompted for the Chroma connection string, enter:

   ```
   http://vector-db:8000
   ```

   This resolves via Docker's internal DNS from inside the admin container, so
   the database stays unreachable from the host.

> **Note:** the `chromadb-admin` image is published for ARM64 only, so on an
> amd64 host it runs under emulation — expect slower startup, and rebuild it
> from source if it misbehaves. It is a development tool and is not part of a
> production deployment.
