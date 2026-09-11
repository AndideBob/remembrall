import pytest

from app.loaders import DocumentLoader, LoaderRegistry, UnsupportedFileTypeError
from app.loaders import registry as registry_module


class StubLoader(DocumentLoader):
    supported_mime_types = frozenset({"text/plain"})

    def load(self, path):
        return ["stub:" + path.name]


class OtherPlainLoader(DocumentLoader):
    supported_mime_types = frozenset({"text/plain"})

    def load(self, path):
        return []


class NoTypesLoader(DocumentLoader):
    def load(self, path):
        return []


def test_register_and_get_loader():
    registry = LoaderRegistry()
    loader = StubLoader()
    registry.register(loader)
    assert registry.get_loader("text/plain") is loader
    assert registry.supported_mime_types() == {"text/plain"}


def test_unknown_type_raises():
    registry = LoaderRegistry()
    with pytest.raises(UnsupportedFileTypeError):
        registry.get_loader("application/zip")


def test_conflicting_registration_raises():
    registry = LoaderRegistry()
    registry.register(StubLoader())
    with pytest.raises(ValueError):
        registry.register(OtherPlainLoader())


def test_loader_without_declared_types_rejected():
    registry = LoaderRegistry()
    with pytest.raises(ValueError):
        registry.register(NoTypesLoader())


def test_load_dispatches_by_detected_type(tmp_path, monkeypatch):
    registry = LoaderRegistry()
    registry.register(StubLoader())
    # Bypass libmagic: force the detected type so this runs anywhere.
    monkeypatch.setattr(registry_module, "detect_mime_type", lambda p: "text/plain")
    f = tmp_path / "x.dat"
    f.write_text("whatever")
    assert registry.load(f) == ["stub:x.dat"]


def test_load_unsupported_reports_file_name(tmp_path, monkeypatch):
    registry = LoaderRegistry()
    monkeypatch.setattr(
        registry_module, "detect_mime_type", lambda p: "application/x-tar"
    )
    f = tmp_path / "archive.tar"
    f.write_text("x")
    with pytest.raises(UnsupportedFileTypeError) as exc_info:
        registry.load(f)
    assert "archive.tar" in str(exc_info.value)
