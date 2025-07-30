"""
Tests for the SpotifyAPIClient class.
"""
import pytest
import sys
import os
from unittest.mock import patch, MagicMock
import requests

# Add the src directory to the path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.spotify_api_client import SpotifyAPIClient

class TestSpotifyAPIClient:
    """Test cases for SpotifyAPIClient."""

    def setup_method(self):
        """Set up test fixtures."""
        self.test_token = "test_access_token"
        self.client = SpotifyAPIClient(self.test_token)

    def test_init(self):
        """Test client initialization."""
        assert self.client.auth_token == self.test_token
        assert "Authorization" in self.client.headers
        assert self.client.headers["Authorization"] == f"Bearer {self.test_token}"

    @patch('src.spotify_api_client.requests.get')
    def test_get_success(self, mock_get):
        """Test successful GET request."""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"test": "data"}
        mock_get.return_value = mock_response

        url = "https://api.spotify.com/v1/test"
        result = self.client.get(url)

        assert result == {"test": "data"}
        mock_get.assert_called_once_with(url, headers=self.client.headers, params={}, timeout=30)

    @patch('src.spotify_api_client.requests.get')
    def test_get_with_fields(self, mock_get):
        """Test GET request with fields parameter."""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"test": "data"}
        mock_get.return_value = mock_response

        url = "https://api.spotify.com/v1/test"
        fields = ["field1", "field2"]
        result = self.client.get(url, fields=fields)

        assert result == {"test": "data"}
        expected_params = {"fields": "field1,field2"}
        mock_get.assert_called_once_with(url, headers=self.client.headers, params=expected_params, timeout=30)

    @patch('src.spotify_api_client.requests.get')
    def test_get_request_exception(self, mock_get):
        """Test GET request with RequestException."""
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        url = "https://api.spotify.com/v1/test"
        result = self.client.get(url)

        assert result is None

    @patch('src.spotify_api_client.requests.get')
    def test_get_value_error(self, mock_get):
        """Test GET request with ValueError (invalid JSON)."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response

        url = "https://api.spotify.com/v1/test"
        result = self.client.get(url)

        assert result is None

    @patch('src.spotify_api_client.requests.get')
    def test_get_http_error(self, mock_get):
        """Test GET request with HTTP error status."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_get.return_value = mock_response

        url = "https://api.spotify.com/v1/test"
        result = self.client.get(url)

        assert result is None
