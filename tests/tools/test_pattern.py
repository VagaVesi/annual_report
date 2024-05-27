from annual_report.report_data.pattern import Pattern, make_pattern, return_pattern_and_elements_from_string


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

    def test_return_pattern_and_elements_from_string_only_elements(self):
        elements_string = "107011, 107021"
        result = return_pattern_and_elements_from_string(elements_string)

        assert result[0] == ""
        assert result[1] == ["107011", "107021"]

    def test_return_pattern_and_elements_from_string_pattern_and_element(self):
        elements_string = "107011, 10**31"
        result = return_pattern_and_elements_from_string(elements_string)

        assert result[0] == "^10\\d{2}31$"
        assert result[1] == ["107011"]

    def test_return_pattern_and_elements_from_complex_pattern(self):
        elements_string = "3****1, 4****2, 5****2, 6****2"
        result = return_pattern_and_elements_from_string(elements_string)

        assert result[0] == "^[3456]\\d{4}[12]$"

    def test_init_pattern_generate_combinations(self):
        """Generate combinations from xls"""
        pattern_v1 = Pattern()
        pattern_v1.generate_combinations()

        assert pattern_v1.patterns["created"] != ""
        assert len(pattern_v1.patterns["Report element pattern"]) > 1
