"""Test EntryValidationError class."""
from annual_report.entry.entry_validation_error import EntryValidationError, ValidationErrorType


class TestEntryValidationError():
    """Test EntryValidationError class."""

    def test_init_validation_error(self):
        """Create simple EntryDetail"""
        error = EntryValidationError(
            ValidationErrorType.NOT_EXCISTING_CODE, "1", "1")
        assert error.entry_number == "1"
        assert error.error_type == ValidationErrorType.NOT_EXCISTING_CODE

    def test_error_message_name_all_atributes(self):
        """Error message string with 3 attributes"""
        error = EntryValidationError(
            ValidationErrorType.NOT_EXCISTING_CODE, "3003", "2")
        correct_message = "Error in entry 3003 line 2. Validation error: The code of the element is not in the classification."
        error_message = str(error)
        assert error_message == correct_message

    def test_error_message_name_row_number_missing(self):
        """Error message string eith 2 attributes"""
        error = EntryValidationError(
            ValidationErrorType.DEBIT_NOT_EQUALS_CREDIT, "2000")
        correct_message = "Error in entry 2000. Validation error: The total debit of an entry does not equal the credit of an entry."
        error_message = str(error)
        assert error_message == correct_message
