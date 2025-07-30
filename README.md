# Spectra Python Application

A Python application project for learning and development with API integration capabilities.

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

- `CLIENT_ID`: Your API client ID
- `CLIENT_SECRET`: Your API client secret  
- `API_BASE_URL`: Base URL for your API (optional)
- `API_TIMEOUT`: Request timeout in seconds (optional)
- `DEBUG`: Enable debug logging (optional)

**Important**: Never commit the `.env` file to version control. Use `.env.example` as a template.

## Running the Application

### Basic usage:
```bash
python main.py --demo                    # Run API demo
python main.py --auth-demo               # Run authenticated API demo
python main.py --interactive             # Interactive API client
```

### Make specific API calls:
```bash
# Public API call
python main.py --url https://api.github.com/users/octocat

# Authenticated API call (requires .env setup)
python main.py --url https://your-api.com/endpoint --auth

# POST request with data
python main.py --url https://api.example.com/posts --method POST --data '{"title":"Test"}'
```

## Development

- Main application entry point: `main.py`
- Add your modules in the `src/` directory
- Tests should go in the `tests/` directory
- Store sensitive config in `.env` file

## Project Structure

```
Spectra/
├── main.py              # Main application entry point
├── .env                 # Environment variables (create from .env.example)
├── .env.example         # Environment variables template
├── requirements.txt     # Python dependencies
├── src/                 # Source code modules
├── tests/              # Unit tests
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Features

- ✅ HTTP API client with requests library
- ✅ Environment variable management with python-dotenv
- ✅ Authentication support (Basic Auth)
- ✅ Interactive API testing mode
- ✅ Command-line interface with argparse
- ✅ JSON request/response handling
- ✅ Error handling and timeout management
