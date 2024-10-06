import requests
import reflex as rx

def make_api_request(method: str, url: str, **kwargs) -> requests.Response:
    """
    Make an API request.

    Args:
        method (str): The HTTP method (e.g., 'GET', 'POST', 'PUT', 'DELETE').
        url (str): The URL for the request.
        **kwargs: Additional arguments to pass to the request (e.g., headers, data, params).

    Returns:
        requests.Response: The response from the API request.
    """
    method = method.upper()
    if method not in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD']:
        raise ValueError(f"Unsupported HTTP method: {method}")

    response = requests.request(method, url, **kwargs)
    return response
