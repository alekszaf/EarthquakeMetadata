"""
This module provides functions for token retrieval from a token endpoint.
"""

import requests

CLIENT_ID = 'dfbe495e-3b17-40e7-b9e1-7022bfbce640'
CLIENT_SECRET = '47f8Q~hLwk-fPTEOlJF~WyZFHgiQW6cAx20GHa4t'
TENANT_ID = '9c5012c9-b616-44c2-a917-66814fbe3e87'
SCOPE = 'https://graph.microsoft.com/.default'
TOKEN_URL = f'https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token'

data = {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'scope': SCOPE,
}


def token_request(timeout=None):
    """
    Sends a POST request to obtain an access token from a token endpoint.

    Args:
        timeout (float, optional): Maximum time allowed for the request
        to complete, in seconds. Defaults to None.

    Returns:
        str: Access token obtained from the token endpoint.

    Usage:
        access_token = token_request()
    """

    try:
        response = requests.post(TOKEN_URL, data=data, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:  # pylint: disable=[invalid-name]
        print(f"Request failed: {e}")
        raise SystemExit(e)  # pylint: disable=[raise-missing-from]

    access_token = response.json()['access_token']
    print(f"Access Token: {access_token}")
    return access_token


token_request()
