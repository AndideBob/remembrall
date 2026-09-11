from pathlib import Path

from app.loaders.base import DocumentLoader
from app.loaders.mime import detect_mime_type


class UnsupportedFileTypeError(Exception):
    """Raised when no registered loader handles a file's MIME type.

    Distinct from :class:`~app.loaders.base.LoaderError`: here no loader exists
    for the type at all, rather than a loader failing to read the file.
    """

    def __init__(self, mime_type: str, path: Path | None = None) -> None:
        self.mime_type = mime_type
        self.path = path
        where = f" ({path.name})" if path is not None else ""
        super().__init__(f"No loader registered for MIME type '{mime_type}'{where}")


class LoaderRegistry:
    """Maps MIME types to the loader responsible for them.

    Loaders self-declare the types they handle via
    :attr:`DocumentLoader.supported_mime_types`; :meth:`register` wires each of
    those types into the lookup. :meth:`load` dispatches a file by detecting its
    MIME type and delegating to the matching loader.
    """

    def __init__(self) -> None:
        self._loaders: dict[str, DocumentLoader] = {}

    def register(self, loader: DocumentLoader) -> None:
        """Register a loader for each MIME type it declares.

        Raises ``ValueError`` if the loader declares no types, or if one of its
        types is already handled by a different loader.
        """
        if not loader.supported_mime_types:
            raise ValueError(f"{type(loader).__name__} declares no supported_mime_types")
        for mime_type in loader.supported_mime_types:
            existing = self._loaders.get(mime_type)
            if existing is not None and type(existing) is not type(loader):
                raise ValueError(
                    f"MIME type '{mime_type}' is already handled by "
                    f"{type(existing).__name__}"
                )
            self._loaders[mime_type] = loader

    def get_loader(self, mime_type: str) -> DocumentLoader:
        """Return the loader for ``mime_type`` or raise ``UnsupportedFileTypeError``."""
        loader = self._loaders.get(mime_type)
        if loader is None:
            raise UnsupportedFileTypeError(mime_type)
        return loader

    def supported_mime_types(self) -> set[str]:
        """Return the set of MIME types with a registered loader."""
        return set(self._loaders)

    def load(self, path: Path) -> list[str]:
        """Detect ``path``'s MIME type and extract its text via the right loader.

        Raises ``UnsupportedFileTypeError`` if no loader handles the detected
        type.
        """
        mime_type = detect_mime_type(path)
        loader = self._loaders.get(mime_type)
        if loader is None:
            raise UnsupportedFileTypeError(mime_type, path)
        return loader.load(path)
