"""Request, load and save data from API."""
from requests import get


def request_data(api_path: str) -> str:
    """Reguest data list from API 

    parameters:
    api_path (str) : API path.
    return (list): Response from API in JSON format
    """
    with get(api_path) as response:
        return response.json()
