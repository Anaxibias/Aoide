#!/usr/bin/env python3
"""
Playlist object for the Aoide Python application.
"""
from src.spotify_api_client import SpotifyAPIClient
from src.trackanalysis_api_client import TrackAnalysisApiClient
from src.track import Track
from src.cache import Cache

class Playlist:
    """Playlist class for managing Spotify playlists."""
    
    def __init__(self, spotify_api_client: SpotifyAPIClient, trackanalysis_api_client: TrackAnalysisApiClient, playlist_id: str, cache: Cache):
        """
        Initialize the Playlist with an API client and playlist ID.
        
        Args:
            spotify_api_client: The Spotify API client object for making requests
            playlist_id (str): The Spotify playlist ID
        """
        self.spotify_api_client = spotify_api_client
        self.trackanalysis_api_client = trackanalysis_api_client
        self.playlist_id = playlist_id
        self.cache = cache
        self.data = None
        self.track_data = None
        self.playlist = None
        self.vectors = []
        self.song_list = []

        self.load_playlist()
        self.refs = self.get_track_refs()
        self.track_data = self.get_track_data()
        self.playlist = self.build_playlist()

        for track in self.playlist:
            self.vectors.append(track.get_vector())

        for track in self.playlist:
            self.song_list.append(track.get_name())

    @classmethod
    def from_cache(cls, cache):
        """
        Create a Playlist instance from cached track data.
        
        Args:
            cache: Cache instance containing playlist data
            
        Returns:
            Playlist: A new Playlist instance created from cached data
        """
        # Create a new instance without calling __init__
        instance = cls.__new__(cls)
        
        # Initialize basic attributes
        instance.spotify_api_client = None
        instance.trackanalysis_api_client = None
        instance.playlist_id = None
        instance.cache = cache
        instance.data = None
        
        # Load cached playlist data
        cache_data = cache.get_cached_playlist()
        instance.track_data = cache_data
        instance.vectors = []
        instance.song_list = []
        
        # Build playlist from cached data
        instance.playlist = []
        for data in cache_data:
            if data is not None:
                instance.playlist.append(Track(data))
        
        # Build vectors and song list
        for track in instance.playlist:
            instance.vectors.append(track.get_vector())
            instance.song_list.append(track.get_name())
        
        return instance

    def load_playlist(self):
        """Load playlist data from Spotify API."""
        self.data = self.spotify_api_client.get(f"https://api.spotify.com/v1/playlists/{self.playlist_id}",
                                       fields=["tracks.items(track(href))"])

    def get_track_refs(self):
        """
        Extract track href URLs from the loaded playlist data.
        
        Returns:
            list[str]: A list of Spotify track API href URLs
        """
        track_refs = []
        if self.data and 'tracks' in self.data and 'items' in self.data['tracks']:
            items = self.data['tracks']['items']
            for item in items:
                if 'track' in item and 'href' in item['track']:
                    track_refs.append(item['track']['href'])

        return track_refs

    def get_track_data(self):
        """
        Get track analysis data for all tracks in the playlist.
        Rate limited to 1 request per second due to API constraints.
        
        Returns:
            list: List of track analysis data dictionaries
        """
        track_metadata = []

        if self.refs:
            total_tracks = len(self.refs)
            print(f"🔄 Importing {total_tracks} tracks (rate limited to 1 request/second)...")
            
            for index, ref in enumerate(self.refs, 1):
                print(f"🔄 Importing track {index}/{total_tracks}...")
                # Extract track ID from Spotify href URL
                # URL format: https://api.spotify.com/v1/tracks/{track_id}
                track_id = ref.split('/')[-1] if ref else ""
                track_data = self.trackanalysis_api_client.get(track_id)
                track_metadata.append(track_data)

        return track_metadata

    def build_playlist(self):
        """
        Build a list of Track objects from the track analysis data.
        
        Returns:
            list[Track]: A list of Track objects created from the playlist's track data
        """
        playlist_tracks = []

        for data in self.track_data:
            # Only create Track objects for valid data (skip None values)
            if data is not None:
                playlist_tracks.append(Track(data))

        cache_data = []
        for track in playlist_tracks:
            data = track.get_data()
            cache_data.append(data)

        self.cache.update_playlist(cache_data)
        
        return playlist_tracks
    
    def get_playlist(self):
        return self.playlist
    
    def get_vectors(self):
        return self.vectors
    
    def get_song_list(self):
        return self.song_list
