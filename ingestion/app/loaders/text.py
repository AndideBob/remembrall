from pathlib import Path

from app.loaders.base import DocumentLoader, LoaderError


class TextLoader(DocumentLoader):
    """Loads plain-text and Markdown files.

    The content is returned unchanged as a single segment. Markdown is kept
    as-is rather than stripped — its headings and structure are useful context
    for retrieval.
    """

    supported_mime_types = frozenset({"text/plain", "text/markdown"})

    def load(self, path: Path) -> list[str]:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            raise LoaderError(f"Could not read {path.name}: {exc}") from exc
        if not text.strip():
            raise LoaderError(f"{path.name} contains no text")
        return [text]
