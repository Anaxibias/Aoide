#!/usr/bin/env python3
"""
API Client for the Aoide Python application.
Handles API requests and authentication for Spotify API.
"""

from typing import Optional, Dict, Any
import requests

class SpotifyAPIClient:
    """API Client for making authenticated requests to Spotify API."""

    def __init__(self, auth_token: str):
        """
        Initialize the API client with authentication token.
        
        Args:
            auth_token (str): The authentication token for API requests
        """
        self.auth_token = auth_token
        self.headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def get(self, endpoint: str, fields: Optional[list[str]] = None) -> Optional[Dict[str, Any]]:
        """
        Make a GET request to the specified endpoint.
        
        Args:
            endpoint (str): The API endpoint to request
            fields (Optional[list[str]]): Optional list of fields to include
            
        Returns:
            Optional[Dict[str, Any]]: The JSON response data or None if request failed
        """
        try:
            params = {}
            if fields:
                params['fields'] = ','.join(fields)

            response = requests.get(endpoint, headers=self.headers, params=params, timeout=30)

            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ GET request failed: {response.status_code}")
                print(f"Response: {response.text}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"❌ Network error making GET request: {e}")
            return None
        except ValueError as e:
            print(f"❌ JSON parsing error: {e}")
            return None
