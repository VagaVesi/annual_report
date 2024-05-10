"""Class validates JSON data."""
from jsonschema import validate
from json import loads
from path import Path


def validate(input: str, schema_location: str) -> list:
    """Validate input with JSONschema.

    params:
    input (str): data to validate
    schema_location (str): file path

    return: List of errors if any else empty list 
    """
    if Path(schema_location).exists():
        shcema = loads(Path(schema_location).read_text())
        try:
            validate(input, shcema)
            return []
        except Exception as e:
            return [e, e.context]

    else:
        return [f"{schema_location} not found"]
