#!/usr/bin/env python
"""
Setup script for Gmail API integration.

This script handles the OAuth flow for Gmail API access by:
1. Creating a .secrets directory if it doesn't exist
2. Using credentials from .secrets/secrets.json to authenticate
3. Opening a browser window for user authentication
4. Storing the access token in .secrets/token.json
"""

import os
import sys
import json
from pathlib import Path

# Add project root to sys.path for imports to work correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))

# Import required Google libraries
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

def main():
    """Run Gmail authentication setup."""
    # Create .secrets directory
    secrets_dir = Path(__file__).parent.absolute() / ".secrets"
    secrets_dir.mkdir(parents=True, exist_ok=True)
    
    # Check for secrets.json
    secrets_path = secrets_dir / "secrets.json"
    if not secrets_path.exists():
        print(f"Error: Client secrets file not found at {secrets_path}")
        print("Please download your OAuth client ID JSON from Google Cloud Console")
        print("and save it as .secrets/secrets.json")
        return 1
    
    print("Starting Gmail API authentication flow...")
    print("A browser window will open for you to authorize access.")
    
    # This will trigger the OAuth flow and create token.json
    try:
        # Define the scopes we need
        SCOPES = [
            'https://www.googleapis.com/auth/gmail.modify',
            'https://www.googleapis.com/auth/calendar'
        ]
        
        # Load client secrets
        with open(secrets_path, 'r') as f:
            client_config = json.load(f)
        
        # Create the flow using the client_secrets.json format
        flow = InstalledAppFlow.from_client_secrets_file(
            str(secrets_path),
            SCOPES
        )
        
        # Run the OAuth flow
        credentials = flow.run_local_server(port=0)
        
        # Save the credentials to token.json
        token_path = secrets_dir / "token.json"
        token_data = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes,
            'universe_domain': 'googleapis.com',
            'account': '',
            'expiry': credentials.expiry.isoformat() + "Z"
        }
        
        with open(token_path, 'w') as token_file:
            json.dump(token_data, token_file)
            
        print("\nAuthentication successful!")
        print(f"Access token stored at {token_path}")
        return 0
    except Exception as e:
        print(f"Authentication failed: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())