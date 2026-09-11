import pytest

from app.loaders import LoaderError, TextLoader


def test_plain_text_returned_as_single_segment(tmp_path):
    f = tmp_path / "note.txt"
    f.write_text("hello world")
    assert TextLoader().load(f) == ["hello world"]


def test_markdown_kept_as_is(tmp_path):
    f = tmp_path / "doc.md"
    content = "# Heading\n\nSome *body* text."
    f.write_text(content)
    assert TextLoader().load(f) == [content]


def test_empty_or_whitespace_file_raises(tmp_path):
    f = tmp_path / "empty.txt"
    f.write_text("   \n  ")
    with pytest.raises(LoaderError):
        TextLoader().load(f)


def test_declares_supported_types():
    assert TextLoader().supported_mime_types == frozenset(
        {"text/plain", "text/markdown"}
    )
