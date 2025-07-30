"""
Tests for the Playlist class.
"""
import pytest
import sys
import os
from unittest.mock import MagicMock, patch

# Add the src directory to the path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.playlist import Playlist
from src.spotify_api_client import SpotifyAPIClient
from src.trackanalysis_api_client import TrackAnalysisApiClient

class TestPlaylist:
    """Test cases for Playlist class."""

    def setup_method(self):
        """Set up test fixtures."""
        # Mock the API clients
        self.mock_spotify_client = MagicMock(spec=SpotifyAPIClient)
        self.mock_trackanalysis_client = MagicMock(spec=TrackAnalysisApiClient)
        
        # Sample playlist data from Spotify
        self.sample_playlist_data = {
            "tracks": {
                "items": [
                    {
                        "track": {
                            "href": "https://api.spotify.com/v1/tracks/track1"
                        }
                    },
                    {
                        "track": {
                            "href": "https://api.spotify.com/v1/tracks/track2"
                        }
                    }
                ]
            }
        }
        
        # Sample track analysis data
        self.sample_track_data = [
            {
                "name": "Track 1",
                "key": "C",
                "mode": "major",
                "camelot": "8B",
                "loudness": "-5.5",
                "tempo": 120.0,
                "energy": 0.8,
                "danceability": 0.7,
                "happiness": 0.6,
                "acousticness": 0.2,
                "liveness": 0.1,
                "speechiness": 0.05
            },
            {
                "name": "Track 2",
                "key": "G",
                "mode": "minor",
                "camelot": "6A",
                "loudness": "-4.2",
                "tempo": 128.0,
                "energy": 0.9,
                "danceability": 0.8,
                "happiness": 0.7,
                "acousticness": 0.1,
                "liveness": 0.15,
                "speechiness": 0.03
            }
        ]
        
        # Configure mocks
        self.mock_spotify_client.get.return_value = self.sample_playlist_data
        self.mock_trackanalysis_client.get.side_effect = self.sample_track_data
        
        self.playlist_id = "test_playlist_123"

    @patch('src.playlist.Track')
    def test_init(self, mock_track_class):
        """Test playlist initialization."""
        # Create mock Track instances
        mock_track1 = MagicMock()
        mock_track2 = MagicMock()
        mock_track_class.side_effect = [mock_track1, mock_track2]
        
        playlist = Playlist(
            self.mock_spotify_client,
            self.mock_trackanalysis_client,
            self.playlist_id
        )
        
        assert playlist.spotify_api_client == self.mock_spotify_client
        assert playlist.trackanalysis_api_client == self.mock_trackanalysis_client
        assert playlist.playlist_id == self.playlist_id
        assert playlist.data == self.sample_playlist_data
        
        # Check that Spotify API was called for playlist data
        self.mock_spotify_client.get.assert_called_once()

    def test_load_playlist(self):
        """Test load_playlist method."""
        playlist = Playlist.__new__(Playlist)  # Create without calling __init__
        playlist.spotify_api_client = self.mock_spotify_client
        playlist.playlist_id = self.playlist_id
        
        playlist.load_playlist()
        
        expected_url = f"https://api.spotify.com/v1/playlists/{self.playlist_id}"
        self.mock_spotify_client.get.assert_called_with(
            expected_url,
            fields=["tracks.items(track(href))"]
        )
        assert playlist.data == self.sample_playlist_data

    def test_get_track_refs(self):
        """Test get_track_refs method."""
        playlist = Playlist.__new__(Playlist)  # Create without calling __init__
        playlist.data = self.sample_playlist_data
        
        refs = playlist.get_track_refs()
        
        expected_refs = [
            "https://api.spotify.com/v1/tracks/track1",
            "https://api.spotify.com/v1/tracks/track2"
        ]
        assert refs == expected_refs

    def test_get_track_refs_empty_data(self):
        """Test get_track_refs with empty data."""
        playlist = Playlist.__new__(Playlist)  # Create without calling __init__
        playlist.data = None
        
        refs = playlist.get_track_refs()
        assert refs == []

    def test_get_track_refs_malformed_data(self):
        """Test get_track_refs with malformed data."""
        playlist = Playlist.__new__(Playlist)  # Create without calling __init__
        playlist.data = {"tracks": {"items": []}}
        
        refs = playlist.get_track_refs()
        assert refs == []

    def test_get_track_data(self):
        """Test get_track_data method."""
        playlist = Playlist.__new__(Playlist)  # Create without calling __init__
        playlist.trackanalysis_api_client = self.mock_trackanalysis_client
        playlist.refs = [
            "https://api.spotify.com/v1/tracks/track1",
            "https://api.spotify.com/v1/tracks/track2"
        ]
        
        track_data = playlist.get_track_data()
        
        assert len(track_data) == 2
        assert track_data == self.sample_track_data
        
        # Check that track analysis API was called for each track
        assert self.mock_trackanalysis_client.get.call_count == 2

    def test_get_track_data_empty_refs(self):
        """Test get_track_data with empty refs."""
        playlist = Playlist.__new__(Playlist)  # Create without calling __init__
        playlist.trackanalysis_api_client = self.mock_trackanalysis_client
        playlist.refs = []
        
        track_data = playlist.get_track_data()
        assert track_data == []

    @patch('src.playlist.Track')
    def test_build_playlist(self, mock_track_class):
        """Test build_playlist method."""
        # Create mock Track instances
        mock_track1 = MagicMock()
        mock_track2 = MagicMock()
        mock_track_class.side_effect = [mock_track1, mock_track2]
        
        playlist = Playlist.__new__(Playlist)  # Create without calling __init__
        playlist.trackanalysis_api_client = self.mock_trackanalysis_client
        playlist.track_data = self.sample_track_data
        
        playlist_tracks = playlist.build_playlist()
        
        assert len(playlist_tracks) == 2
        assert playlist_tracks[0] == mock_track1
        assert playlist_tracks[1] == mock_track2
        
        # Check that Track was instantiated with correct data
        assert mock_track_class.call_count == 2
