from app.loaders.csv_loader import CsvLoader
from app.loaders.registry import LoaderRegistry
from app.loaders.text import TextLoader


def build_default_registry() -> LoaderRegistry:
    """Return a registry with every built-in loader registered."""
    registry = LoaderRegistry()
    registry.register(TextLoader())
    registry.register(CsvLoader())
    return registry
