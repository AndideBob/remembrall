from pathlib import Path

# Text formats that libmagic reports generically as "text/plain" by content,
# but which we want to route to more specific loaders. libmagic inspects bytes,
# and a Markdown or CSV file has no distinguishing signature, so we refine these
# by extension.
_TEXT_EXTENSION_OVERRIDES = {
    ".md": "text/markdown",
    ".markdown": "text/markdown",
    ".csv": "text/csv",
}


def detect_mime_type(path: Path) -> str:
    """Detect a file's MIME type from its content, refined by extension.

    Content-based detection (via libmagic) guards against mislabeled files: a
    ``.txt`` that is actually a PDF is reported as ``application/pdf``. Because
    libmagic cannot tell text subtypes apart (Markdown and CSV both read as
    ``text/plain``), a generic text result is refined using the file extension.

    ``magic`` is imported lazily so this module stays importable where libmagic
    is not installed; the runtime container provides it.
    """
    import magic

    mime_type = magic.from_file(str(path), mime=True)
    if mime_type == "text/plain":
        return _TEXT_EXTENSION_OVERRIDES.get(path.suffix.lower(), mime_type)
    return mime_type
