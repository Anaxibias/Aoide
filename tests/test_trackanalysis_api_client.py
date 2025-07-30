"""
Tests for the TrackAnalysisApiClient class.
"""
import pytest
import sys
import os
from unittest.mock import patch, MagicMock
import requests

# Add the src directory to the path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.trackanalysis_api_client import TrackAnalysisApiClient

class TestTrackAnalysisApiClient:
    """Test cases for TrackAnalysisApiClient."""

    def setup_method(self):
        """Set up test fixtures."""
        self.test_key = "test_api_key"
        self.test_host = "test.rapidapi.com"
        self.client = TrackAnalysisApiClient(self.test_key, self.test_host)

    def test_init(self):
        """Test client initialization."""
        assert "x-rapidapi-key" in self.client.headers
        assert "x-rapidapi-host" in self.client.headers
        assert self.client.headers["x-rapidapi-key"] == self.test_key
        assert self.client.headers["x-rapidapi-host"] == self.test_host
        assert hasattr(self.client, 'url')
        assert self.client.url == "https://track-analysis.p.rapidapi.com/pxtx/spotify"

    @patch('src.trackanalysis_api_client.requests.get')
    def test_get_success(self, mock_get):
        """Test successful GET request."""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "name": "Test Track",
            "key": "C",
            "mode": "major",
            "tempo": 120.0
        }
        mock_get.return_value = mock_response

        track_ref = "spotify:track:4iV5W9uYEdYUVa79Axb7Rh"
        result = self.client.get(track_ref)

        expected_data = {
            "name": "Test Track",
            "key": "C",
            "mode": "major",
            "tempo": 120.0
        }
        assert result == expected_data
        expected_url = f"{self.client.url}/{track_ref}"
        mock_get.assert_called_once_with(expected_url, headers=self.client.headers, timeout=30)

    @patch('src.trackanalysis_api_client.requests.get')
    def test_get_request_exception(self, mock_get):
        """Test GET request with RequestException."""
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        track_ref = "spotify:track:4iV5W9uYEdYUVa79Axb7Rh"
        result = self.client.get(track_ref)

        assert result is None

    @patch('src.trackanalysis_api_client.requests.get')
    def test_get_value_error(self, mock_get):
        """Test GET request with ValueError (invalid JSON)."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response

        track_ref = "spotify:track:4iV5W9uYEdYUVa79Axb7Rh"
        result = self.client.get(track_ref)

        assert result is None

    @patch('src.trackanalysis_api_client.requests.get')
    def test_get_http_error(self, mock_get):
        """Test GET request with HTTP error status."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_get.return_value = mock_response

        track_ref = "spotify:track:4iV5W9uYEdYUVa79Axb7Rh"
        result = self.client.get(track_ref)

        assert result is None

    @patch('src.trackanalysis_api_client.requests.get')
    def test_get_timeout(self, mock_get):
        """Test GET request with timeout."""
        mock_get.side_effect = requests.exceptions.Timeout("Request timed out")

        track_ref = "spotify:track:4iV5W9uYEdYUVa79Axb7Rh"
        result = self.client.get(track_ref)

        assert result is None
