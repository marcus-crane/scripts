"""
A handy script for validating Azure AD OAuth credentials by trying
to acquire authentication credentials.

You'll only receive the credentials if client id/secret etc are correct.

Handy if you feel like a client id is matched to a wrong secret I guess.

Dependencies:
    > pip install msal

Usage:
    > python3 azure_oauth.py
    Login via the following auth url: https://example.com
    Paste the response URL here: > https://response.example.com?abc=123
    { ...creds here }
"""

from pprint import pprint
import urllib.parse as urlparse

import msal

SCOPES = ["https://graph.microsoft.com/.default"]

CLIENT_ID = "abc123"
CLIENT_SECRET = "bcd234"
TENANT_ID = "https://login.microsoftonline.com/abc123"

client = msal.ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET,
        authority=TENANT_ID
    )
auth_url = client.get_authorization_request_url(scopes=SCOPES)

print(f"Login via the following auth url: {auth_url}")

response_url = input("Paste the response URL here: > ")
parsed_url = urlparse.urlparse(response_url)
code = urlparse.parse_qs(parsed_url.query).get('code')

auth_creds = client.acquire_token_by_authorization_code(code, scopes=SCOPES)

pprint(auth_creds)
