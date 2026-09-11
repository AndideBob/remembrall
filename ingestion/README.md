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
