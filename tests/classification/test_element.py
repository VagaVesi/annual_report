"""Test Element class and its properties."""
from datetime import date
from classifications.classification import Element, make_elements_list


class TestElement():
    """Tests for Element class."""

    def test_init_element(self):
        lang = {"en": "Cash - Cash in hand", "et": "Raha - Sularaha"}
        test_element = Element("101010", lang, "2024-01-01")

        assert test_element.code == "101010"
        assert test_element.valid_until_date == None

    def test_get_element_name(self):
        lang = {"en": "Cash - Cash in hand", "et": "Raha - Sularaha"}
        test_element = Element("101010", lang, "2024-01-01")

        assert test_element.get_name() == {"et": "Raha - Sularaha"}
        assert test_element.get_name(["en"]) == {"en": "Cash - Cash in hand"}
        assert test_element.get_name(["en", "et"]) == lang

    def test_make_elements_list(self):
        source = [
            {
                "code": "101010",
                "name": {"en": "Cash - Cash in hand", "et": "Raha - Sularaha"},
                "valid_from_date": "2024-01-01"
            },
            {
                "code": "101020",
                "name": {"en": "Cash - Bank accounts", "et": "Raha - Arvelduskontod"},
                "valid_from_date": "2024-01-01",
                "valid_until_date": "2025-01-01"
            },]
        element_list = make_elements_list(source)

        assert len(element_list) == 2
        assert element_list[0].code == "101010"
        assert element_list[0].valid_until_date == None
        assert element_list[1].valid_until_date == date(2025, 1, 1)
