import pytest

from app.loaders import CsvLoader, LoaderError


def test_each_row_becomes_a_segment(tmp_path):
    f = tmp_path / "people.csv"
    f.write_text("name,role\nAda,Engineer\nGrace,Admiral\n")
    assert CsvLoader().load(f) == [
        "name: Ada; role: Engineer",
        "name: Grace; role: Admiral",
    ]


def test_blank_cells_are_dropped(tmp_path):
    f = tmp_path / "gaps.csv"
    f.write_text("name,role,city\nAda,,London\n")
    assert CsvLoader().load(f) == ["name: Ada; city: London"]


def test_header_only_raises(tmp_path):
    f = tmp_path / "headeronly.csv"
    f.write_text("name,role\n")
    with pytest.raises(LoaderError):
        CsvLoader().load(f)


def test_empty_file_raises(tmp_path):
    f = tmp_path / "empty.csv"
    f.write_text("")
    with pytest.raises(LoaderError):
        CsvLoader().load(f)
