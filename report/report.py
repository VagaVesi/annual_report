"""Convert dataset data to Annual Report elements."""

REPORT_COMPONENTS_LIST = []
REPORT_ELEMENTS_LIST = []


class Report():
    """Report holds its all components"""

    def __init__(self, dataset: dict) -> None:
        """Init report with components based on dataset"""
        self.source_data = dataset
        self.report_components = []


class ReportComponent():
    """Report holds its elements"""

    def __init__(self) -> None:
        """Init component with elements based on dataset"""
        self. report_elements = []


class ReportElement():
    """Report elements holds report data."""
    gl_source_data = []


def find_accountMain_based_pattern(pattern: str) -> list:
    """Rerurn list of MainAcoounts matching pattern"""
    pass
