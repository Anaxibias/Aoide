#!/usr/bin/env python3
"""
Cache module for the Audio Visualizer Python application.
Provides persistent data storage between sessions.
"""

import json
import os
from typing import Any, List

class Cache:
    """Simple file-based cache for storing data between sessions."""

    def __init__(self, cache_file: str = "cache/audiovisualizer_cache.json"):
        """
        Initialize the cache with a specified file path.
        
        Args:
            cache_file (str): Path to the cache file
        """
        self.cache_file = cache_file
        self.data = self._load_cache()

        self.request_count = self.get("request count", 0)
        self.cached_playlist = self.get("cached playlist", [])

    def _load_cache(self) -> dict:
        """Load cache data from file."""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def _save_cache(self) -> None:
        """Save cache data to file."""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2)
        except IOError:
            pass  # Silently fail if can't write

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a value from the cache.
        
        Args:
            key (str): The cache key
            default (Any): Default value if key not found
            
        Returns:
            Any: The cached value or default
        """
        return self.data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Set a value in the cache.
        
        Args:
            key (str): The cache key
            value (Any): The value to cache
        """
        self.data[key] = value
        self._save_cache()

    def delete(self, key: str) -> None:
        """
        Delete a value from the cache.
        
        Args:
            key (str): The cache key to delete
        """
        if key in self.data:
            del self.data[key]
            self._save_cache()

    def clear(self) -> None:
        """Clear all cache data."""
        self.data = {}
        self._save_cache()

    def has(self, key: str) -> bool:
        """
        Check if a key exists in the cache.
        
        Args:
            key (str): The cache key to check
            
        Returns:
            bool: True if key exists, False otherwise
        """
        return key in self.data

    def update_request_count(self) -> None:
        """
        Increment the request count value by 1 and save to cache.
        """
        self.request_count += 1
        self.set("request count", self.request_count)

    def update_playlist(self, playlist: List) -> None:

        self.cached_playlist = playlist
        self.set("cached playlist", self.cached_playlist)

    def get_cached_playlist(self) -> List:
        return self.cached_playlist
