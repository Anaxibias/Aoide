#!/usr/bin/env python3
"""
Figure superclass for the Audio Visualizer Python application.
Provides base functionality for data visualization and plotting.
"""

from typing import List
from abc import ABC, abstractmethod
import plotly.graph_objects as go
import plotly.express as px

class Figure(ABC):
    """
    Abstract base class for creating data visualizations in Audio Visualizer.
    
    This superclass provides common functionality for all figure types
    and defines the interface that subclasses must implement.
    """

    def __init__(self, title: str = "Audio Visualizer Visualization", width: int = 800, height: int = 600, vectors: list = None, names: list = None):
        """
        Initialize the Figure with basic configuration.
        
        Args:
            title (str): The title of the figure
            width (int): Width of the figure in pixels
            height (int): Height of the figure in pixels
            vectors (list): List of vectors for the figure
            names (list): List of song titles
        """
        self.title = title
        self.width = width
        self.height = height
        self.fig = None
        self.vectors = vectors if vectors is not None else []
        self.names = names if names is not None else []

        # Default styling configuration
        self.theme = "plotly_dark"
        self.color_palette = px.colors.qualitative.Set3
        self.font_family = "Arial, sans-serif"
        self.font_size = 12

    @abstractmethod
    def create_figure(self, categories: List = None) -> None:
        """
        Abstract method to create the specific figure type.
        
        Args:
            data (List[Any]): The data to visualize
            categories (List): Optional categories for the figure
            
        Returns:
            go.Figure: The created plotly figure
        """
        raise NotImplementedError("Subclasses must implement create_figure method")

    @abstractmethod
    def set_layout(self, fig, **kwargs) -> None:
        """
        Configure the layout of the figure.
        
        Args:
            **kwargs: Layout configuration options
        """
        raise NotImplementedError("Subclasses must implement set_layout method")

    def show(self) -> None:
        """Display the figure in the browser."""
        if not self.fig:
            raise ValueError("Figure must be created before showing")
        self.fig.show()

    def __str__(self) -> str:
        """String representation of the figure."""
        return f"Figure(title='{self.title}', size={self.width}x{self.height}, theme='{self.theme}')"

    def __repr__(self) -> str:
        """Detailed string representation of the figure."""
        return (f"Figure(title='{self.title}', width={self.width}, height={self.height}, "
                f"theme='{self.theme}', data_points={len(self.vectors)})")
