# Remembrall

A self-hosted, modular personal knowledge vault. Upload documents of any type,
then ask questions and get answers with citations back to the source — powered
by retrieval-augmented generation over your own private data.

## Status

**Early development.** The full stack builds and runs — every service starts and
passes its health check — but the services are still skeletons without their core
functionality.

- ✅ Repository structure and `docker-compose.yml`
- ✅ Vector database (Chroma) wired into the stack
- ✅ API, ingestion, and LLM gateway services start and report healthy
- 🚧 Document ingestion, retrieval, and chat — not yet implemented
- 🚧 Frontend — not yet started

## Architecture

The system is split into independent services with defined boundaries, so file
types, the vector database, and the LLM provider can each be swapped without
touching the rest. Each service's responsibilities are documented in its own
folder:

| Service | Role | Stack |
|---|---|---|
| [`frontend/`](frontend/) | Upload UI + chat | React + TypeScript |
| [`api/`](api/) | Orchestration, auth, HTTP endpoints | Python (FastAPI) |
| [`ingestion/`](ingestion/) | Parsing, chunking, embedding | Python |
| [`vector-db/`](vector-db/) | Embedding storage | Chroma |
| [`llm-gateway/`](llm-gateway/) | Provider abstraction | Python |
| [`reverse-proxy/`](reverse-proxy/) | HTTPS + access gate | Caddy |

Services communicate over an internal Docker network and persist data to named
volumes.

## Getting started

Prerequisites: Docker and Docker Compose.

```bash
cp .env.example .env   # then edit values as needed
docker compose up
```

See [`.env.example`](.env.example) for all configuration options.

## Running tests

Each service ships its tests as a `<service>-tests` compose service (behind the
`test` profile, so they never start with a normal `up`). Run everything:

```bash
bash scripts/run-tests.sh
```

The script discovers and runs every `*-tests` service. To run a single service's
suite directly:

```bash
docker compose run --rm ingestion-tests
```

Per-service testing notes live in each service's own README.
