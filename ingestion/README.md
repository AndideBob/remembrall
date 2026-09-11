# ingestion

File parsing, chunking, and embedding — the pluggable "any file type" layer.

**Language:** Python

**Responsibilities**
- **Loader registry:** a base `DocumentLoader` interface with one implementation
  per file type (PDF, DOCX, text/Markdown, CSV, images via OCR), selected by a
  MIME-type dispatcher. Unknown types return a clear "unsupported" error.
- Every loader outputs plain text; chunking + embedding are a **shared library**
  applied uniformly downstream (single source of truth).
- Embeds via local `sentence-transformers` (`all-MiniLM-L6-v2`) by default, then
  writes vectors to the Chroma service.

## Tests

Test and dev dependencies live in `requirements-dev.txt` and are **not**
installed in the production image. They are baked into the image's `dev` build
stage instead, which the `ingestion-tests` compose service uses. Run the suite
with one command (from anywhere in the repo, on any OS):

```bash
docker compose run --rm ingestion-tests
```

That builds the `dev` stage (pytest + the test suite + libmagic) and runs
`pytest`. Pass extra pytest arguments after the service name, e.g.
`docker compose run --rm ingestion-tests pytest -k csv -v`.

The `ingestion-tests` service is behind the `test` profile, so it never starts
with a normal `docker compose up`. Tests that depend on libmagic skip
automatically where it is absent, so the suite can also be run directly with
`pytest` on a host that has the dev requirements installed.
