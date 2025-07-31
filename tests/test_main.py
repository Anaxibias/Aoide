"""
Tests for the Audio Visualizer application.
"""
import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the src directory to the path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_main_import():
    """Test that main module can be imported."""
    try:
        import main
        assert True
    except ImportError:
        pytest.fail("Could not import main module")

def test_check_credentials():
    """Test the check_credentials function."""
    import main
    
    # Test with missing credentials - need to patch the module-level variables
    with patch.object(main, 'SPOTIFY_CLIENT_ID', None), \
         patch.object(main, 'SPOTIFY_CLIENT_SECRET', None):
        assert main.check_credentials() == False
    
    # Test with valid credentials
    with patch.object(main, 'SPOTIFY_CLIENT_ID', 'test_id'), \
         patch.object(main, 'SPOTIFY_CLIENT_SECRET', 'test_secret'):
        assert main.check_credentials() == True

@patch('main.requests.post')
def test_get_spotify_access_token_success(mock_post):
    """Test successful access token retrieval."""
    import main
    
    # Mock successful response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'access_token': 'test_token'}
    mock_post.return_value = mock_response
    
    with patch.dict(os.environ, {
        'SPOTIFY_CLIENT_ID': 'test_id',
        'SPOTIFY_CLIENT_SECRET': 'test_secret'
    }):
        token = main.get_spotify_access_token()
        assert token == 'test_token'

@patch('main.requests.post')
def test_get_spotify_access_token_failure(mock_post):
    """Test failed access token retrieval."""
    import main
    
    # Mock failed response
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.text = 'Bad Request'
    mock_post.return_value = mock_response
    
    with patch.dict(os.environ, {
        'SPOTIFY_CLIENT_ID': 'test_id',
        'SPOTIFY_CLIENT_SECRET': 'test_secret'
    }):
        token = main.get_spotify_access_token()
        assert token is None
