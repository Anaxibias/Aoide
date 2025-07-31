#!/usr/bin/env python3
"""
CLI module for the Aoide Python application.
Provides command-line interface functionality.
"""

import sys
from typing import List
from src.playlist import Playlist
from src.radar_plot import RadarPlot
from src.cache import Cache

class CLI:
    """Command-line interface class for command-based operations."""

    def __init__(self, spotify_api_client=None, trackanalysis_api_client=None, cache=None):
        """
        Initialize the CLI with available commands and API clients.
        
        Args:
            spotify_api_client: Instance of SpotifyAPIClient for Spotify API operations
            trackanalysis_api_client: Instance of TrackAnalysisApiClient for track analysis
        """
        self.spotify_api_client = spotify_api_client
        self.trackanalysis_api_client = trackanalysis_api_client
        self.cache = cache

        self.current_playlist = None
    
        self.commands = {
            "--help": {"function": self.show_help, "description": "Show help information"},
            "--import": {"function": self.import_playlist, "description": "Import a Spotify playlist by ID"},
            "--load": {"function": self.load_playlist, "description": "Load cached playlist from a previous session"},
            "--print": {"function": self.print_playlist, "description": "Print a list of songs in an imported playlist"},
            "--vector": {"function": self.display_vector, "description": "Print the vectors for the songs in the playlist"},
            "--display": {"function": self.display_radar_plot, "description": "Create a radar plot visualization using track data from the imported playlist"},
            "--exit": {"function": self.exit_app, "description": "Exit the application"}
        }

    def display_prompt(self) -> None:
        """Display the command prompt."""
        print("aoide> ", end="")

    def parse_command(self, user_input: str) -> tuple[str, List[str]]:
        """Parse user input into command and arguments."""
        parts = user_input.strip().split()
        if not parts:
            return "", []
        return parts[0], parts[1:]

    def execute_command(self, command: str, args: List[str]) -> bool:
        """Execute a command. Returns True to continue, False to exit."""
        if command in self.commands:
            try:
                return self.commands[command]["function"](args)
            except Exception as e:
                print(f"❌ Error executing command: {e}")
                return True
        else:
            print(f"❌ Unknown command: {command}")
            print("Type --help for available commands.")
            return True

    def run(self) -> None:
        """Run the main CLI loop."""
        print("Welcome to Aoide Audio Analysis Tool!")
        print("Type --help for available commands or --exit to quit.")
        print()

        while True:
            try:
                self.display_prompt()
                user_input = input().strip()

                if not user_input:
                    continue

                command, args = self.parse_command(user_input)

                # Execute command and check if we should continue
                if not self.execute_command(command, args):
                    break
  
            except KeyboardInterrupt:
                print("\n\n� Goodbye!")
                break
            except EOFError:
                print("\n\n👋 Goodbye!")
                break

    def show_help(self, args: List[str]) -> bool:
        """Display help information."""
        print("\n❓ AOIDE - HELP & INFORMATION")
        print("=" * 40)
        print()
        print("Available Commands:")
        print("-" * 20)

        for command, info in self.commands.items():
            print(f"  {command:<12} - {info['description']}")

        print()
        print("💡 Tips:")
        print("  • Commands are case-sensitive")
        print("  • Use --exit or Ctrl+C to quit")
        print("  • Additional commands will be added in future versions")
        print()

        return True

    def import_playlist(self, args: List[str]) -> bool:
        """Import a Spotify playlist."""
        if not args:
            print("❌ Please provide a link to a Spotify playlist or a playlist ID .")
            print("Usage: --import <playlist_id>")
            print("Example: --import 37i9dQZF1DXcBWIGoYBM5M")
            return True

        playlist_id = args[0]

        if len(playlist_id) != 22:
            if playlist_id[:34] == "https://open.spotify.com/playlist/":
                playlist_id = playlist_id[34:57]

        if not self.spotify_api_client or not self.trackanalysis_api_client:
            print("❌ API clients not configured. Please check your setup.")
            return True

        try:
            print(f"🔄 Importing playlist: {playlist_id}")            

            # Create and load the playlist
            self.current_playlist = Playlist(
                self.spotify_api_client,
                self.trackanalysis_api_client,
                playlist_id,
                self.cache
            )



            track_count = len(self.current_playlist.playlist) if self.current_playlist.playlist else 0
            print(f"✅ Successfully imported playlist with {track_count} tracks!")
            print("Playlist data loaded and ready for analysis.")

        except Exception as e:
            print(f"❌ Failed to import playlist: {e}")
            self.current_playlist = None

        return True

    def load_playlist(self, args: List[str]) -> bool:
        """Load cached playlist from a previous session."""
        if not self.cache:
            print("❌ Cache not configured. Please check your setup.")
            return True

        try:
            print("🔄 Loading cached playlist...")
            
            # Create playlist from cache
            cached_playlist = Playlist.from_cache(self.cache)
            playlist_tracks = cached_playlist.get_playlist()
            
            # Check if there are any cached tracks
            if len(playlist_tracks) == 0:
                print("❌ No cached playlist found. Use --import <playlist_id> to import a playlist first.")
                return True
            
            self.current_playlist = cached_playlist
            track_count = len(playlist_tracks)
            print(f"✅ Successfully loaded cached playlist with {track_count} tracks!")
            print("Playlist data loaded and ready for analysis.")

        except Exception as e:
            print(f"❌ Failed to load cached playlist: {e}")
            self.current_playlist = None

        return True

    def print_playlist(self, args: List[str]) -> bool:
        """Print the tracks in the current playlist."""
        if not self.current_playlist:
            print("❌ No playlist imported. Use --import <playlist_id> to import a playlist first.")
            return True

        song_list = self.current_playlist.get_song_list()
        if not song_list:
            print("❌ No tracks found in the current playlist.")
            return True

        print(f"\nPlaylist Tracks ({len(song_list)} tracks):")
        print("-" * 40)
        for index, song_name in enumerate(song_list, 1):
            print(f"{index:2d}. {song_name}")
        print()

        return True

    def display_vector(self, args: List[str]) -> bool:
        """
        Display the audio feature vectors for all tracks in the current playlist.
        
        Shows a numbered list of tracks with their corresponding audio analysis vectors,
        which contain numerical representations of audio features like tempo, energy,
        danceability, and valence.
        
        Args:
            args (List[str]): Command arguments (not used for this command)
            
        Returns:
            bool: True to continue CLI execution, False to exit
        """
        if not self.current_playlist:
            print("❌ No playlist imported. Use --import <playlist_id> to import a playlist first.")
            return True

        vectors = self.current_playlist.get_vectors()
        if not vectors:
            print("❌ No tracks found in the current playlist.")
            return True

        print("\nTrack Vectors:")
        print("-" * 40)
        for index, vector in enumerate(vectors, 1):
            print(f"{index:2d}. {vector}")
        print()

        return True

    def display_radar_plot(self, args: List[str]) -> bool:
        """Create a radar plot visualization using track data from the imported playlist."""
        if not self.current_playlist:
            print("❌ No playlist imported. Use --import <playlist_id> to import a playlist first.")
            return True

        vectors = self.current_playlist.get_vectors()
        song_titles = self.current_playlist.get_song_list()

        if not vectors or not song_titles:
            print("❌ No tracks found in the current playlist.")
            return True

        # Create RadarPlot object using vectors and song_titles
        radar_plot = RadarPlot(title="Playlist Audio Features", vectors=vectors, names=song_titles)
        radar_plot.create_figure(['BPM', 'Energy', 'Danceability', 'Valence'])
        radar_plot.show()

        return True

    def exit_app(self, args: List[str]) -> bool:
        """Exit the application."""
        print("\nThank you for using Aoide!")
        return False

def main():
    """Main function to run the CLI."""
    try:
        cli = CLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
