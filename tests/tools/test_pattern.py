from tools.pattern import Pattern, make_pattern


class TestPattern():
    """Tests for Pattern generation class."""

    def test_init_pattern_load_data_from_excel(self):
        pattern = Pattern()
        xls = pattern.load_data_from_excel()

        assert len(xls) > 1
        assert pattern.patterns == {"created": "",
                                    "Report element pattern": []}

    def test_load_source_data(self):
        """Data loaded from default xls path and stored to source_data"""
        pattern = Pattern()
        pattern.load_source_data()

        assert len(pattern.source_data) > 1
        assert len(pattern.source_data[0]['MAJANDUSLIKSISU2024ap']) > 1

    def test_make_pattern_1_element_replace_2(self):
        elements = ["103**0"]
        pattern = make_pattern(elements)

        assert pattern == "^103\\d{2}0$"

    def test_make_pattern_1_element_replace_5(self):
        elements = ["1*****"]
        pattern = make_pattern(elements)

        assert pattern == "^1\\d{5}$"

    def test_make_pattern_3_elements_replace_2(self):
        elements = ["103**0", "104**0", "105**0"]
        pattern = make_pattern(elements)

        assert pattern == "^10[345]\\d{2}0$"

    def test_make_pattern_1_element_replace_1(self):
        elements = ["11111*"]
        pattern = make_pattern(elements)

        assert pattern == "^11111\\d{1}$"
