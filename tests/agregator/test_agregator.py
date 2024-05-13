from annual_report.agregator.agregator import AgregatorEntries


class TestAgregator():
    """Tests for entries agregator class."""

    def test_init_agregator_entries(self):
        ag = AgregatorEntries(
            "annual_report/tests/entry/modified_entries_list.json")

        assert len(ag.entries) > 0