#!/usr/bin/env python3
"""
Figure superclass for the Aoide Python application.
Provides base functionality for data visualization and plotting.
"""

from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
import plotly.graph_objects as go
import plotly.express as px

class Figure(ABC):
    """
    Abstract base class for creating data visualizations in Aoide.
    
    This superclass provides common functionality for all figure types
    and defines the interface that subclasses must implement.
    """

    def __init__(self, title: str = "Aoide Visualization", width: int = 800, height: int = 600, vectors: list = None, names: list = None):
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
        self.data = vectors if vectors is not None else []
        self.names = names if names is not None else []
        
        # Default styling configuration
        self.theme = "plotly_dark"
        self.color_palette = px.colors.qualitative.Set3
        self.font_family = "Arial, sans-serif"
        self.font_size = 12

    @abstractmethod
    def create_figure(self, data: List[Any], categories: List = None) -> go.Figure:
        """
        Abstract method to create the specific figure type.
        
        Args:
            data (List[Any]): The data to visualize
            categories (List): Optional categories for the figure
            
        Returns:
            go.Figure: The created plotly figure
        """
        raise NotImplementedError("Subclasses must implement create_figure method")

    def set_layout(self, **kwargs) -> None:
        """
        Configure the layout of the figure.
        
        Args:
            **kwargs: Layout configuration options
        """
        if not self.fig:
            raise ValueError("Figure must be created before setting layout")
            
        layout_config = {
            'title': {
                'text': self.title,
                'x': 0.5,
                'font': {'size': 16, 'family': self.font_family}
            },
            'width': self.width,
            'height': self.height,
            'template': self.theme,
            'font': {'family': self.font_family, 'size': self.font_size}
        }
        
        # Update with any additional layout options
        layout_config.update(kwargs)
        
        self.fig.update_layout(**layout_config)

    def set_theme(self, theme: str) -> None:
        """
        Set the visual theme for the figure.
        
        Args:
            theme (str): Plotly theme name (e.g., 'plotly_dark', 'plotly_white', 'ggplot2')
        """
        self.theme = theme
        if self.fig:
            self.fig.update_layout(template=theme)

    def set_colors(self, color_palette: List[str]) -> None:
        """
        Set the color palette for the figure.
        
        Args:
            color_palette (List[str]): List of color codes or names
        """
        self.color_palette = color_palette

    def add_annotation(self, text: str, x: float, y: float, **kwargs) -> None:
        """
        Add a text annotation to the figure.
        
        Args:
            text (str): The annotation text
            x (float): X coordinate for the annotation
            y (float): Y coordinate for the annotation
            **kwargs: Additional annotation options
        """
        if not self.fig:
            raise ValueError("Figure must be created before adding annotations")
            
        annotation_config = {
            'text': text,
            'x': x,
            'y': y,
            'showarrow': True,
            'arrowhead': 2,
            'arrowsize': 1,
            'arrowwidth': 2,
            'arrowcolor': "#636363",
            'font': {'family': self.font_family, 'size': self.font_size}
        }
        
        annotation_config.update(kwargs)
        self.fig.add_annotation(**annotation_config)

    def show(self) -> None:
        """Display the figure in the browser."""
        if not self.fig:
            raise ValueError("Figure must be created before showing")
        self.fig.show()

    def save(self, filename: str, file_format: str = "html") -> None:
        """
        Save the figure to a file.
        
        Args:
            filename (str): The filename to save to
            file_format (str): The file format ('html', 'png', 'svg', 'pdf')
        """
        if not self.fig:
            raise ValueError("Figure must be created before saving")
            
        if file_format.lower() == "html":
            self.fig.write_html(filename)
        elif file_format.lower() == "png":
            self.fig.write_image(filename)
        elif file_format.lower() == "svg":
            self.fig.write_image(filename)
        elif file_format.lower() == "pdf":
            self.fig.write_image(filename)
        else:
            raise ValueError(f"Unsupported format: {file_format}")

    def get_figure(self) -> Optional[go.Figure]:
        """
        Get the plotly figure object.
        
        Returns:
            Optional[go.Figure]: The plotly figure object, or None if not created
        """
        return self.fig

    def update_data(self, data: List[Any]) -> None:
        """
        Update the figure with new data.
        
        Args:
            data (List[Any]): New data to visualize
        """
        self.data = data
        self.fig = self.create_figure(data)
        self.set_layout()

    def get_config(self) -> Dict[str, Any]:
        """
        Get the current figure configuration.
        
        Returns:
            Dict[str, Any]: Configuration dictionary
        """
        return {
            'title': self.title,
            'width': self.width,
            'height': self.height,
            'theme': self.theme,
            'color_palette': self.color_palette,
            'font_family': self.font_family,
            'font_size': self.font_size
        }

    def set_config(self, config: Dict[str, Any]) -> None:
        """
        Set figure configuration from a dictionary.
        
        Args:
            config (Dict[str, Any]): Configuration dictionary
        """
        for key, value in config.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        # Refresh the figure if it exists
        if self.fig and self.data:
            self.fig = self.create_figure(self.data)
            self.set_layout()

    def __str__(self) -> str:
        """String representation of the figure."""
        return f"Figure(title='{self.title}', size={self.width}x{self.height}, theme='{self.theme}')"

    def __repr__(self) -> str:
        """Detailed string representation of the figure."""
        return (f"Figure(title='{self.title}', width={self.width}, height={self.height}, "
                f"theme='{self.theme}', data_points={len(self.data)})")
