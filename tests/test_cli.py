"""
Tests for the CLI class.
"""
import pytest
import sys
import os
from unittest.mock import MagicMock, patch
from io import StringIO

# Add the src directory to the path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.cli import CLI
from src.spotify_api_client import SpotifyAPIClient
from src.trackanalysis_api_client import TrackAnalysisApiClient

class TestCLI:
    """Test cases for CLI class."""

    def setup_method(self):
        """Set up test fixtures."""
        # Mock the API clients
        self.mock_spotify_client = MagicMock(spec=SpotifyAPIClient)
        self.mock_trackanalysis_client = MagicMock(spec=TrackAnalysisApiClient)
        
        self.cli = CLI(self.mock_spotify_client, self.mock_trackanalysis_client)

    def test_init(self):
        """Test CLI initialization."""
        assert self.cli.spotify_api_client == self.mock_spotify_client
        assert self.cli.trackanalysis_api_client == self.mock_trackanalysis_client

    @patch('builtins.input', return_value='--exit')
    @patch('sys.stdout', new_callable=StringIO)
    def test_run_quit_immediately(self, mock_stdout, mock_input):
        """Test CLI run method with immediate exit."""
        self.cli.run()
        
        output = mock_stdout.getvalue()
        assert "Welcome to Aoide Audio Analysis Tool!" in output
        assert "Goodbye!" in output

    @patch('builtins.input', side_effect=['--help', '--exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_run_help_command(self, mock_stdout, mock_input):
        """Test CLI run method with help command."""
        self.cli.run()
        
        output = mock_stdout.getvalue()
        assert "Available Commands:" in output
        assert "--help" in output
        assert "--exit" in output

    @patch('builtins.input', side_effect=['invalid_command', '--exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_run_invalid_command(self, mock_stdout, mock_input):
        """Test CLI run method with invalid command."""
        self.cli.run()
        
        output = mock_stdout.getvalue()
        assert "Unknown command" in output

    def test_show_help(self):
        """Test show_help method."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result = self.cli.show_help([])
            
            assert result is True
            output = mock_stdout.getvalue()
            assert "Available Commands:" in output
            assert "--help" in output
            assert "--exit" in output

    def test_parse_command(self):
        """Test parse_command method."""
        command, args = self.cli.parse_command("--help")
        assert command == "--help"
        assert args == []
        
        command, args = self.cli.parse_command("command arg1 arg2")
        assert command == "command"
        assert args == ["arg1", "arg2"]
        
        command, args = self.cli.parse_command("")
        assert command == ""
        assert args == []

    def test_execute_command_help(self):
        """Test execute_command method with help."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result = self.cli.execute_command('--help', [])
            
            assert result is True
            output = mock_stdout.getvalue()
            assert "Available Commands:" in output

    def test_execute_command_exit(self):
        """Test execute_command method with exit."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result = self.cli.execute_command('--exit', [])
            
            assert result is False
            output = mock_stdout.getvalue()
            assert "Goodbye!" in output

    def test_execute_command_unknown(self):
        """Test execute_command method with unknown command."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result = self.cli.execute_command('unknown', [])
            
            assert result is True
            output = mock_stdout.getvalue()
            assert "Unknown command" in output

    def test_exit_app(self):
        """Test exit_app method."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result = self.cli.exit_app([])
            
            assert result is False
            output = mock_stdout.getvalue()
            assert "Thank you for using Aoide!" in output
