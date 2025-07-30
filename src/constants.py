#!/usr/bin/env python3
"""
Constants and mappings for the Aoide Python application.
"""

# Camelot wheel mapping to numerical values
# Based on the Camelot wheel system used in DJ mixing
CAMELOT_TO_NUMERIC = {
    "1A": 1, "1B": 2, "2A": 3, "2B": 4, "3A": 5, "3B": 6,
    "4A": 7, "4B": 8, "5A": 9, "5B": 10, "6A": 11, "6B": 12,
    "7A": 13, "7B": 14, "8A": 15, "8B": 16, "9A": 17, "9B": 18,
    "10A": 19, "10B": 20, "11A": 21, "11B": 22, "12A": 23, "12B": 24
}

MODE_TO_NUMERIC = {"major": 1, "minor": 0}

# Reverse mapping for converting back from numeric to Camelot
NUMERIC_TO_CAMELOT = {v: k for k, v in CAMELOT_TO_NUMERIC.items()}

NUMERIC_TO_MODE = {v: k for k, v in MODE_TO_NUMERIC.items()}
