# Aoide - Spotify API Client

A Python application for interacting with the Spotify Web API and audio analysis services. Aoide provides a command-line interface for importing playlists, analyzing tracks, and managing music data.

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
   Then edit `.env` file with your actual API credentials.

## Environment Variables

The application uses a `.env` file to store sensitive configuration:

- `CLIENT_ID`: Your Spotify API client ID (from Spotify Developer Dashboard)
- `CLIENT_SECRET`: Your Spotify API client secret (from Spotify Developer Dashboard)
- `API_AUTH_URL`: Spotify token endpoint (default: https://accounts.spotify.com/api/token)
- `API_BASE_URL`: Spotify API base URL (default: https://api.spotify.com/v1)
- `AUDIOANALYSIS_KEY`: API key for audio analysis service
- `AUDIOANALYSIS_HOST`: Host for audio analysis service
- `API_TIMEOUT`: Request timeout in seconds (default: 30)
- `DEBUG`: Enable debug logging (default: false)

**Important**: Never commit the `.env` file to version control. Use `.env.example` as a template.

### Getting Spotify API Credentials

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Copy the Client ID and Client Secret to your `.env` file

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

## Development

- Main application entry point: `main.py`
- Add your modules in the `src/` directory
- Tests should go in the `tests/` directory
- Store sensitive config in `.env` file

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_spotify_api_client.py
```

### Code Style

This project follows PEP 8 Python style guidelines:

```bash
# Check code style
flake8 src/

# Format code
black src/
```

## Project Structure

```
Aoide/
├── main.py                  # Main application entry point
├── .env                     # Environment variables (create from .env.example)
├── .env.example             # Environment variables template
├── requirements.txt         # Python dependencies
├── src/                     # Source code modules
│   ├── __init__.py         # Package initialization
│   ├── cli.py              # Command-line interface
│   ├── constants.py        # Application constants
│   ├── playlist.py         # Playlist data model
│   ├── track.py            # Track data model
│   ├── spotify_api_client.py      # Spotify API client
│   └── trackanalysis_api_client.py # Track analysis API client
├── tests/                   # Unit tests
│   ├── test_cli.py         # CLI tests
│   ├── test_main.py        # Main module tests
│   ├── test_playlist.py    # Playlist tests
│   ├── test_track.py       # Track tests
│   ├── test_spotify_api_client.py # Spotify client tests
│   └── test_trackanalysis_api_client.py # Analysis client tests
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Features

- ✅ Spotify Web API integration with OAuth 2.0 Client Credentials flow
- ✅ Interactive command-line interface
- ✅ Environment variable management with python-dotenv
- ✅ Error handling and timeout management
- ✅ Comprehensive unit test suite
