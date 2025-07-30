# Aoide - Spotify API Client

A Python application for interacting with the Spotify Web API and Track Analysis API via RapidAPI (https://rapidapi.com/soundnet-soundnet-default/api/track-analysis). Aoide provides a command-line interface for importing playlists and analyzing tracks.

## Setup

1. Make sure you have Python 3.7+ installed
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` file with your actual API credentials (subscription required for access to Track Analysis API).

## Environment Variables

- `CLIENT_ID`: Your Spotify API client ID (from Spotify Developer Dashboard)
- `CLIENT_SECRET`: Your Spotify API client secret (from Spotify Developer Dashboard)
- `API_AUTH_URL`: Spotify token endpoint (default: https://accounts.spotify.com/api/token)
- `API_BASE_URL`: Spotify API base URL (default: https://api.spotify.com/v1)
- `AUDIOANALYSIS_KEY`: API key for Track Analysis API
- `AUDIOANALYSIS_HOST`: Host for Track Analysis API
- `API_TIMEOUT`: Request timeout in seconds (default: 30)
- `DEBUG`: Enable debug logging (default: false)

Instructions on obtaining Spotify API client ID and client secret can be found here: https://developer.spotify.com/documentation/web-api/tutorials/getting-started#request-an-access-token

## Running the Application

### Basic usage:
```bash
python main.py                           # Run interactive CLI mode
```

### Available CLI Commands:
```bash
--help                                   # Show help information
--import <playlist_id>                   # Import a Spotify playlist by ID
--print
--exit                                   # Exit the application
```

### Example Usage:
```bash
# Import a playlist from Spotify
python main.py --import 37i9dQZF1DXcBWIGoYBM5M
```
Aoide can also extract playlist ID directly from a link to the playlist.
