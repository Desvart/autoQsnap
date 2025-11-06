import pandas as pd
import plotly.graph_objects as go
from dataclasses import dataclass
from typing import Optional, Union, Dict, List


@dataclass
class ChartMetadata:
    img_name: str
    y_label: str

class QSnapRadarPlotBuilder:

    # Default image size
    DEFAULT_IMAGE_WIDTH = 600
    DEFAULT_IMAGE_HEIGHT = 600
    DEFAULT_IMAGE_SCALE = 2

    def __init__(self):
        self._data_frame: Optional[pd.DataFrame] = None
        self._original_data_frame: Optional[pd.DataFrame] = None
        self._metadata: Optional[ChartMetadata] = None
        self._figure: Optional[go.Figure] = None
        self._image_width: int = self.DEFAULT_IMAGE_WIDTH
        self._image_height: int = self.DEFAULT_IMAGE_HEIGHT
        self._image_scale: int = self.DEFAULT_IMAGE_SCALE


    def set_data(self, data: Union[pd.DataFrame, Dict]) -> 'QSnapRadarPlotBuilder':
        if isinstance(data, dict):
            df = pd.DataFrame(data)
        elif isinstance(data, pd.DataFrame):
            df = data.copy()
        else:
            raise ValueError("Data must be either a pandas DataFrame or a dictionary")

        self._validate_data_frame(df)
        self._original_data_frame = df.copy()
        self._data_frame = df.copy()

        return self


    def set_metadata(self, metadata: Union[ChartMetadata, Dict]) -> 'QSnapRadarPlotBuilder':
        if isinstance(metadata, dict):
            self._metadata = ChartMetadata(**metadata)
        elif isinstance(metadata, ChartMetadata):
            self._metadata = metadata
        else:
            raise ValueError("Metadata must be either a ChartMetadata object or a dictionary")

        self._validate_metadata()

        return self


    def set_image_size(self, width: int = None, height: int = None, scale: int = None) -> 'QSnapRadarPlotBuilder':
        if width is not None:
            self._image_width = width
        if height is not None:
            self._image_height = height
        if scale is not None:
            self._image_scale = scale

        return self


    def build(self) -> go.Figure:
        if self._data_frame is None:
            raise ValueError("Data must be set before building. Call set_data() first.")
        if self._metadata is None:
            raise ValueError("Metadata must be set before building. Call set_metadata() first.")

        self._figure = self._create_chart()
        return self._figure


    def export_to_png(self, filename: Optional[str] = None) -> None:
        if self._figure is None:
            raise ValueError("Chart must be built before exporting. Call build() first.")

        if filename is None:
            filename = self._metadata.img_name

        clean_filename = filename.strip().lower().replace(' ', '_') + ".png"

        self._figure.write_image(
            clean_filename,
            width=self._image_width,
            height=self._image_height,
            scale=self._image_scale,
            format="png"
        )

    def get_figure(self) -> Optional[go.Figure]:
        return self._figure


    # ========== VALIDATION METHODS ==========

    def _validate_data_frame(self, df: pd.DataFrame) -> None:
        if 'Category' not in df.columns:
            raise ValueError("DataFrame must contain a 'Category' column")

        # Todo: check for 10 categories

        if len(df.columns) < 2:
            raise ValueError("DataFrame must contain at least one year column besides 'Category'")

        year_columns = [col for col in df.columns if col != 'Category']
        for col in year_columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                raise ValueError(f"Year column '{col}' must contain numeric values")


    def _validate_metadata(self) -> None:
        if not self._metadata.img_name:
            raise ValueError("Metadata must include 'img_name'")
        if not self._metadata.y_label:
            raise ValueError("Metadata must include 'y_label'")


    # ========== CHART CREATION METHODS ==========

    def _create_chart(self) -> go.Figure:
        years = self._get_x_axis()
        categories = self._get_y_axis()

        fig = self._add_radars(years, categories)
        fig = self._apply_layout(fig)

        return fig


    def _add_radars(self, years: List[str], categories: List[str]) -> go.Figure:
        fig = go.Figure()

        for i in years[2::1]:
            value = self._data_frame[i].tolist()
            fig.add_trace(go.Scatterpolar(
                r=value,
                theta=categories,
                fill='toself',
                name=i
            ))
        return fig


    def _apply_layout(self, fig: go.Figure) -> go.Figure:
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                ),
                angularaxis = dict(
                    rotation=90, # start position of angular axis
                    direction="clockwise"
                )
            ),
            showlegend=True,
            plot_bgcolor='white',
            hovermode=False,
        )

        return fig


    # ========== HELPER METHODS ==========

    def _get_x_axis(self) -> List[str]:
        return self._data_frame.columns.drop('Category').tolist()

    def _get_y_axis(self) -> List[str]:
        return self._data_frame['Category'].tolist()

# ========== EXAMPLE USAGE ==========

if __name__ == "__main__":

    data = {
        'Category': ['User satisfaction', 'Product stability', 'Fix reactivity', 'Documentation',
                     'Policy adherence', 'FAT practices', 'UAT practices', 'Static quality',
                     'Unit coverage', 'Automation practices'],
        '2022': [0.68, 0.48, 0.79, 0.98, 1.00, 0.57, 0.00, 0.62, 0.37, 0.97],
        '2023': [0.48, 0.58, 0.89, 0.88, 0.60, 0.77, 0.40, 0.82, 0.17, 0.07],
        '2024': [0.18, 0.58, 0.79, 0.78, 0.80, 0.67, 0.20, 0.42, 0.77, 0.47],
        '2025': [0.28, 0.68, 0.84, 0.90, 0.70, 0.47, 0.10, 0.62, 0.37, 0.97]
    }

    metadata = {
        'img_name': 'Coverage Score Trend',
        'y_label': 'Coverage score'
    }

    # Create and build chart
    builder = QSnapRadarPlotBuilder()
    fig = builder.set_data(data).set_metadata(metadata).set_image_size(600, 600).build()
    fig.show()
    # builder.export_to_png()
