#!/usr/bin/env python3
"""
Main application entry point for the Aoide Python application.
"""

import os
import requests
from dotenv import load_dotenv
from src.spotify_api_client import SpotifyAPIClient
from src.trackanalysis_api_client import TrackAnalysisApiClient
from src.cache import Cache
from src.cli import CLI

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
AUDIOANALYSIS_KEY = os.getenv('AUDIOANALYSIS_KEY')
AUDIOANALYSIS_HOST = os.getenv('AUDIOANALYSIS_HOST')
API_AUTH_URL = os.getenv('API_AUTH_URL', 'https://accounts.spotify.com/api/token')
API_BASE_URL = os.getenv('API_BASE_URL', 'https://api.example.com')
API_TIMEOUT = int(os.getenv('API_TIMEOUT', '30'))
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'

def check_credentials():
    """Check if required credentials are available."""
    if not SPOTIFY_CLIENT_ID:
        print("⚠️  CLIENT_ID not set")
        return False
    if not SPOTIFY_CLIENT_SECRET:
        print("⚠️  CLIENT_SECRET not set")
        return False
    return True

def get_spotify_access_token():
    """Get Spotify access token using Client Credentials flow."""
    if not check_credentials():
        return None

    auth_data = {
        'grant_type': 'client_credentials'
    }

    # Spotify uses Basic Auth for token endpoint
    import base64
    credentials = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        response = requests.post(API_AUTH_URL, data=auth_data, headers=headers, timeout=API_TIMEOUT)

        if response.status_code == 200:
            token_data = response.json()
            return token_data.get('access_token')
        else:
            print(f"❌ Failed to get access token: {response.status_code}")
            print(f"Response: {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Network error getting access token: {e}")
        return None
    except ValueError as e:
        print(f"❌ Invalid JSON response: {e}")
        return None

def get_auth_headers():
    """Get authentication headers with Spotify Bearer token."""
    if not check_credentials():
        return {}

    # Get Spotify access token
    access_token = get_spotify_access_token()
    if not access_token:
        print("❌ Could not obtain access token")
        return {}

    return {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "Aoide-Python-App/1.0",
        "Accept": "application/json"
    }

def main():
    """Main function to run the application."""
    print("Welcome to Aoide - Spotify API Client!")
    print("========================================\n")

    # Basic functionality test
    if check_credentials():
        print("✅ Credentials are configured")
        token = get_spotify_access_token()
        if token:
            print("✅ Successfully obtained access token")
        else:
            print("❌ Failed to obtain access token")
    else:
        print("⚠️  Credentials not configured")

    print("\nSetup complete. Ready for API integration.")
    cache = Cache()
    spotify_api_client = SpotifyAPIClient(token)
    trackanalysis_api_client = TrackAnalysisApiClient(AUDIOANALYSIS_KEY, AUDIOANALYSIS_HOST, cache)
    cli = CLI(spotify_api_client, trackanalysis_api_client, cache)
    cli.run()
    return 0

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
