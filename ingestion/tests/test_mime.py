import pytest

from app.loaders import detect_mime_type


def _magic_available() -> bool:
    try:
        import magic

        magic.from_buffer(b"probe", mime=True)
        return True
    except Exception:
        return False


# Content-based detection needs libmagic, which is present in the container but
# not on a bare host. These tests skip automatically when it is unavailable.
magic_required = pytest.mark.skipif(
    not _magic_available(),
    reason="libmagic/python-magic not available (run inside the container)",
)


@magic_required
def test_plain_text_detected(tmp_path):
    f = tmp_path / "note.txt"
    f.write_text("just some text")
    assert detect_mime_type(f) == "text/plain"


@magic_required
@pytest.mark.parametrize(
    "name,expected",
    [
        ("data.csv", "text/csv"),
        ("readme.md", "text/markdown"),
        ("readme.markdown", "text/markdown"),
    ],
)
def test_text_subtype_refined_by_extension(tmp_path, name, expected):
    f = tmp_path / name
    f.write_text("a,b\n1,2\n")
    assert detect_mime_type(f) == expected


@magic_required
def test_content_beats_misleading_extension(tmp_path):
    # PDF bytes with a .txt name must be detected as a PDF.
    f = tmp_path / "mislabeled.txt"
    f.write_bytes(b"%PDF-1.4\n1 0 obj")
    assert detect_mime_type(f) == "application/pdf"
