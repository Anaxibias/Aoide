#!/usr/bin/env python3
"""
Track Analysis API Client for the Aoide Python application.
Handles API requests and authentication for RapidAPI Track Analysis service.
"""

import time
import requests
from src.cache import Cache

class TrackAnalysisApiClient:
    """API Client for making authenticated requests to RapidAPI Track Analysis service."""

    def __init__(self, key: str, host: str, cache: Cache):
        """
        Initialize the Track Analysis API client with authentication credentials.
        
        Args:
            key (str): The RapidAPI key for authentication
            host (str): The RapidAPI host for the track analysis service
            cache: Instance of Cache for persistent data storage
        """
        self.url = "https://track-analysis.p.rapidapi.com/pktx/spotify"
        self.headers = {
            "x-rapidapi-key": key,
            "x-rapidapi-host": host
        }
        self.cache = cache
        self.last_request_time = 0  # Track last request time for rate limiting

    def get(self, track_ref: str):
        """
        Get track analysis data for a Spotify track.
        Rate limited to 1 request per second.
        
        Args:
            track_ref (str): The Spotify track ID to analyze
            
        Returns:
            dict or None: Track analysis data if successful, None if failed
        """
        # Implement rate limiting - ensure at least 1 second between requests
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time

        if time_since_last_request < 1.0:
            sleep_time = 1.0 - time_since_last_request
            time.sleep(sleep_time)

        try:
            while True:
                response = requests.get(f"{self.url}/{track_ref}", headers=self.headers, timeout=30)
                self.cache.update_request_count()
                if response.status_code != 429:
                    break
                else:
                    time.sleep(0.1)

            # Update last request time after receiving response
            self.last_request_time = time.time()

            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ GET request failed: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            # Update last request time even if there's an error
            self.last_request_time = time.time()
            print(f"❌ Network error making GET request: {e}")
            return None
        except ValueError as e:
            print(f"❌ JSON parsing error: {e}")
            return None
