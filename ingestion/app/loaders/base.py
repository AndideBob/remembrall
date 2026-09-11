from abc import ABC, abstractmethod
from pathlib import Path


class DocumentLoader(ABC):
    """Common interface implemented by every document loader.

    A loader has one responsibility: extract plain text from a single family of
    file formats. Everything downstream — chunking, embedding, storage — is
    deliberately out of scope, so each loader stays small and independent.

    Concrete loaders declare the MIME types they handle via
    ``supported_mime_types`` and implement :meth:`load`.
    """

    #: MIME types this loader can handle, e.g. ``{"application/pdf"}``.
    #: The registry uses this to dispatch a file to the right loader.
    supported_mime_types: frozenset[str] = frozenset()

    @abstractmethod
    def load(self, path: Path) -> list[str]:
        """Extract text from the file at ``path``.

        Returns a list of text segments. Segments preserve the document's
        natural boundaries — one per page for a PDF, per sheet for a workbook,
        and so on — which keeps source locations available for later citation.
        A format with no meaningful internal divisions returns a single-element
        list.

        Implementations should raise :class:`LoaderError` when a file matches
        this loader's type but cannot be read (corrupt, encrypted, empty).
        """
        raise NotImplementedError


class LoaderError(Exception):
    """Raised when a loader fails to extract text from a file it should handle.

    Distinct from an unsupported file type (no loader exists at all); this means
    the correct loader was found but the file itself could not be read.
    """
