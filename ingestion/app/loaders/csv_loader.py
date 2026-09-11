import csv
from pathlib import Path

from app.loaders.base import DocumentLoader, LoaderError


class CsvLoader(DocumentLoader):
    """Loads CSV files, rendering each row as a self-describing text segment.

    Each data row becomes one segment of ``field: value`` pairs (using the
    header names), so a retrieved row is understandable on its own and can be
    cited individually. The first row is treated as the header.
    """

    supported_mime_types = frozenset({"text/csv"})

    def load(self, path: Path) -> list[str]:
        segments: list[str] = []
        try:
            with path.open(encoding="utf-8", errors="replace", newline="") as handle:
                reader = csv.DictReader(handle)
                if reader.fieldnames is None:
                    raise LoaderError(f"{path.name} has no header row")
                for row in reader:
                    pairs = [
                        f"{(name or '').strip()}: {(value or '').strip()}"
                        for name, value in row.items()
                        if (value or "").strip()
                    ]
                    if pairs:
                        segments.append("; ".join(pairs))
        except OSError as exc:
            raise LoaderError(f"Could not read {path.name}: {exc}") from exc
        if not segments:
            raise LoaderError(f"{path.name} contains no data rows")
        return segments
