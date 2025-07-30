"""
Tests for the Track class.
"""
import pytest
import sys
import os

# Add the src directory to the path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.track import Track

class TestTrack:
    """Test cases for Track class."""

    def setup_method(self):
        """Set up test fixtures."""
        # Sample track data
        self.sample_track_data = {
            "name": "Test Song",
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
        }
        
        self.track = Track(self.sample_track_data)

    def test_init(self):
        """Test track initialization."""
        assert self.track.data == self.sample_track_data
        
        # Check that attributes are properly set after initialization
        assert self.track.name == "Test Song"
        assert self.track.key == "C"

    def test_track_attributes(self):
        """Test that track attributes are properly set."""
        assert self.track.name == "Test Song"
        assert self.track.key == "C"
        assert self.track.mode == "major"
        assert self.track.camelot == "8B"
        assert self.track.loudness == "-5.5"
        assert self.track.tempo == 120.0
        assert self.track.energy == 0.8
        assert self.track.danceability == 0.7
        assert self.track.happiness == 0.6
        assert self.track.acousticness == 0.2
        assert self.track.liveness == 0.1
        assert self.track.speechiness == 0.05

    def test_get_track(self):
        """Test get_track method."""
        result = self.track.get_track()
        assert result == self.sample_track_data

    def test_get_name(self):
        """Test get_name method."""
        result = self.track.get_name()
        assert result == "Test Song"

    def test_get_audio_features(self):
        """Test get_audio_features method."""
        result = self.track.get_audio_features()
        
        expected_features = {
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
        }
        
        assert result == expected_features

    def test_empty_initialization(self):
        """Test track with empty data."""
        # Test with None data
        track_with_none = Track(None)
        
        # Should have empty/None values for all attributes
        assert track_with_none.data is None
        assert track_with_none.name == ""
        assert track_with_none.tempo is None
        
        # Test with empty dict
        track_with_empty = Track({})
        assert track_with_empty.data == {}
        assert track_with_empty.name == ""
        assert track_with_empty.tempo is None

    def test_load_track_method(self):
        """Test load_track method directly."""
        # Create a track with different data
        new_data = {
            "name": "New Song",
            "key": "G",
            "mode": "minor",
            "camelot": "6A",
            "loudness": "-3.2",
            "tempo": 140.0,
            "energy": 0.9,
            "danceability": 0.8,
            "happiness": 0.4,
            "acousticness": 0.1,
            "liveness": 0.2,
            "speechiness": 0.1
        }
        
        # Update the track's data and reload
        self.track.data = new_data
        self.track.load_track()
        
        # Check that attributes were updated
        assert self.track.name == "New Song"
        assert self.track.key == "G"
        assert self.track.mode == "minor"
        assert self.track.tempo == 140.0
