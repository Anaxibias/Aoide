#!/usr/bin/env python3
"""
Radar plot implementation for the Audio Visualizer Python application.
Subclass of Figure for creating radar/spider charts.
"""

from typing import List
import plotly.graph_objects as go
from src.figure import Figure

class RadarPlot(Figure):
    """
    Radar plot visualization class for displaying multi-dimensional data.
    
    Inherits from Figure superclass and implements radar/spider chart functionality.
    """

    def __init__(self, title: str = "Radar Plot", width: int = 800, height: int = 600, vectors: list = None, names: list = None):
        """
        Initialize the RadarPlot.
        
        Args:
            title (str): The title of the radar plot
            width (int): Width of the plot in pixels
            height (int): Height of the plot in pixels
            vectors (list): List of vectors for the radar plot
            names (list): List of song titles
        """
        super().__init__(title, width, height, vectors, names)

    def create_figure(self, categories: List = None) -> None:
        """
        Create the radar plot figure.
        
        Args:
            data (List[Any]): The data to visualize
            categories (List): The categories for the radar plot
            
        Returns:
            go.Figure: The created plotly figure
        """
        fig = go.Figure()

        traces = self.get_traces(categories)

        for trace in traces:
            fig.add_trace(trace)

        self.set_layout(fig)

        self.fig = fig

    def set_layout(self, fig, **kwargs) -> None:
        """
        Configure the layout of the radar plot.
        
        Args:
            **kwargs: Layout configuration options
        """
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 200]  # Adjusted range for the data values
                )
            ),
            showlegend=True,
            title=self.title
        )

    def get_traces(self, categories: List = None) -> List[go.Scatterpolar]:
        """
        Get traces for the radar plot.
        
        Returns:
            List: List of plotly traces for the radar plot
        """
        traces = []

        for song_name, vector in zip(self.names, self.vectors):
            trace = go.Scatterpolar(
                r = vector,
                theta = categories,
                fill = 'toself',
                name = song_name,
            )

            traces.append(trace)

        return traces
