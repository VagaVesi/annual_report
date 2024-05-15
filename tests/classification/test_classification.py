"""Test Element class and its properties."""
from annual_report.classifications.classification import Classification


class TestClassification():
    """Tests for Classification class."""

    def test_init_classification(self):
        cls_presentation = Classification("ANDMETEESITLUSVIIS2024ap")

        assert cls_presentation.code == "ANDMETEESITLUSVIIS2024ap"
        assert len(cls_presentation.elements) == 15

    def test_is_code_correct(self):
        cls_presentation = Classification("ANDMETEESITLUSVIIS2024ap")
        assert cls_presentation.is_code_correct("AE_15") == True
        assert cls_presentation.is_code_correct("AX_15") == False
