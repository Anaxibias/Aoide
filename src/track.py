#!/usr/bin/env python3
"""
Track object for the Aoide Python application.
"""

from src.constants import CAMELOT_TO_NUMERIC, MODE_TO_NUMERIC

class Track:
    """Track class for managing Spotify track data and audio analysis."""

    def __init__(self, track_data: dict):
        """
        Initialize the Track with an API client and track reference.
        
        Args:
            trackanalysis_api_client (TrackAnalysisApiClient): The track analysis API client for making requests
            track_ref (str): The Spotify track reference/URL for analysis
        """

        self.data = track_data

        # Initialize empty variables
        self.name = ""
        self.key = ""
        self.mode = ""
        self.camelot = ""
        self.loudness = ""
        self.tempo = None
        self.energy = None
        self.danceability = None
        self.happiness = None
        self.acousticness = None
        self.liveness = None
        self.speechiness = None

        self.load_track()

    def load_track(self):
        """Load track data and audio analysis from the track analysis API."""

        if self.data:
            # Use .get() method with default values to handle missing keys
            self.name = self.data.get("name", "Unknown Track")
            self.key = self.data.get("key", "")
            self.mode = self.data.get("mode", "")
            self.camelot = self.data.get("camelot", "")
            self.loudness = self.data.get("loudness", "")
            self.tempo = self.data.get("tempo", None)
            self.energy = self.data.get("energy", None)
            self.danceability = self.data.get("danceability", None)
            self.happiness = self.data.get("happiness", None)
            self.acousticness = self.data.get("acousticness", None)
            self.liveness = self.data.get("liveness", None)
            self.speechiness = self.data.get("speechiness", None)

    def get_track(self):
        """
        Get the complete track data dictionary.

        Returns:
            dict: The complete track data from the API
        """
        return self.data

    def get_name(self):
        """
        Get the track name.

        Returns:
            str: The track name
        """
        return self.name

    def get_audio_features(self):
        """
        Get the audio features as a dictionary.

        Returns:
            dict: Dictionary containing all audio analysis features
        """
        return {
            "key": self.key,
            "mode": self.mode,
            "camelot": self.camelot,
            "loudness": self.loudness,
            "tempo": self.tempo,
            "energy": self.energy,
            "danceability": self.danceability,
            "happiness": self.happiness,
            "acousticness": self.acousticness,
            "liveness": self.liveness,
            "speechiness": self.speechiness
        }

    def get_vector(self):
        """
        Get the track's audio features as a numerical vector for analysis.

        Returns:
            list: List of numerical audio features
        """
        # Convert Camelot code to numeric value
        mode_numeric = MODE_TO_NUMERIC.get(self.mode, 0)
        camelot_numeric = CAMELOT_TO_NUMERIC.get(self.camelot, 0)

        return [
            mode_numeric,
            camelot_numeric,
            self.tempo,
            self.energy,
            self.danceability,
            self.happiness,
            self.acousticness,
            self.liveness,
            self.speechiness
        ]
