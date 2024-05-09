"""Class holding entry validation error info"""
from enum import Enum


class ValidationErrorType (Enum):
    """Validation error descriptions."""
    NOT_EXCISTING_CODE = "The code of the element is not in the classification."
    DEBIT_NOT_EQUALS_CREDIT = "The total debit of an entry does not equal the credit of an entry."


class EntryValidationError:
    """Entry validation error."""
    NOT_MATERIAL_DIFFERENCE = 0.5

    def __init__(self, error_type: ValidationErrorType, entry_number: str, line_number="") -> None:
        self.entry_number = entry_number
        self.line_number = line_number
        self.error_type = error_type

    def __str__(self) -> str:
        error_message = "Error in entry " + self.entry_number
        if self.line_number != "":
            error_message = error_message + " line " + self.line_number
        error_message = error_message + ". Validation error: " + self.error_type.value
        return error_message
