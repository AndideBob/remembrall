# Remembrall

A self-hosted, modular personal knowledge vault. Upload documents of any type,
then ask questions and get answers with citations back to the source — powered
by retrieval-augmented generation over your own private data.

## Status

**Early development — scaffolding stage.** The service layout and container
orchestration are in place; the individual services are not yet implemented.

- ✅ Repository structure and `docker-compose.yml` skeleton
- ✅ Vector database (Chroma) wired into the stack
- 🚧 Ingestion, API, LLM gateway, and frontend services — in progress

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
