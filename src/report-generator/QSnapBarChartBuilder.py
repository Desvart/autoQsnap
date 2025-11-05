import pandas as pd
import plotly.graph_objects as go
from typing import List, Dict, Optional, Union
from dataclasses import dataclass

# Todo: add checks to validate that metadata trigram list has the same size as the original data

# Fixme: Fix the callout distance to last column - The distance between the callouts and the right side of the plot should be the shortest possible to avoid reducing the plot functional size
# Fixme: Fix the callout arrow distance - This distance between the arrow head and the callout should be the lowest possible, without colliding the callout together
# Fixme: Fix the callout arrow height - It should be the highest value between the middle of the callout and the middle of the corresponding category

@dataclass
class ChartMetadata:
    img_name: str
    y_label: str
    trigrams: Optional[Dict[str, Dict[str, List[str]]]] = None

    def __post_init__(self):
        if self.trigrams is None:
            self.trigrams = {}


class QSnapBarChartBuilder:
    """
    Builder class for creating QSnap stacked bar charts with trend visualization.

    Usage:
        builder = QSnapBarChartBuilder()
        fig = builder.set_data(df).set_metadata(metadata).set_image_size(800, 800).build()
        builder.export_to_png('output_chart')
    """

    # ========== CONSTANTS - Easy to maintain and tweak ==========

    # Color scheme for categories
    CATEGORY_COLORS = {
        'Full':    '#4ADE80',   # Medium green
        'Good':    '#86EFAC',   # Light green
        'Average': '#D1D5DB',   # Light grey
        'Low':     '#FDE047',   # Light yellow
        'Bad':     '#FCA5A5',   # Light red
        'None':    '#FCA5A5',   # Light red
        'Unknown': '#FFFFFF'    # White
    }

    # Chart styling constants
    BAR_BORDER_COLOR = '#9CA3AF'
    BAR_BORDER_WIDTH = 2
    CONNECTING_LINE_COLOR = '#9CA3AF'
    CONNECTING_LINE_WIDTH = 1.5
    AXIS_LINE_COLOR = 'black'
    AXIS_LINE_WIDTH = 2
    BAR_WIDTH = 0.4

    # Layout constants
    TITLE_Y_POSITION = 0.99
    LEGEND_Y_POSITION = -0.08
    TOP_MARGIN = 10
    COLUMN_TOTAL_Y_OFFSET = 1.02

    # Font styling
    FONT_SIZE = 12
    TITLE_FONT_SIZE = 14
    BAR_LABEL_FONT_SIZE = 14
    CALLOUT_FONT_SIZE = 11

    # Callout styling
    UNKNOWN_CALLOUT_BG = '#F3F4F6'
    UNKNOWN_CALLOUT_BORDER = '#6B7280'
    UNKNOWN_ARROW_COLOR = '#6B7280'
    UNKNOWN_CALLOUT_X_OFFSET = 120
    UNKNOWN_ARROW_X_OFFSET = 0.75

    BAD_NONE_CALLOUT_BG = '#FEE2E2'
    BAD_NONE_CALLOUT_BORDER = '#DC2626'
    BAD_NONE_ARROW_COLOR = '#DC2626'
    BAD_NONE_CALLOUT_X_OFFSET = 70
    BAD_NONE_ARROW_X_OFFSET = 0.25

    CALLOUT_BORDER_WIDTH = 2
    CALLOUT_BORDER_PAD = 8
    ARROW_HEAD_SIZE = 2
    ARROW_SIZE = 1
    ARROW_WIDTH = 2

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

    # ========== PUBLIC API - Fluent Interface ==========

    def set_data(self, data: Union[pd.DataFrame, Dict]) -> 'QSnapBarChartBuilder':
        """
        Set the data for the chart.

        Args:
            data: Either a pandas DataFrame or a dictionary that can be converted to DataFrame.
                  Must contain a 'Category' column and year columns.

        Returns:
            Self for method chaining

        Raises:
            ValueError: If data format is invalid
        """
        if isinstance(data, dict):
            df = pd.DataFrame(data)
        elif isinstance(data, pd.DataFrame):
            df = data.copy()
        else:
            raise ValueError("Data must be either a pandas DataFrame or a dictionary")

        self._validate_data_frame(df)
        self._original_data_frame = df.copy()
        self._data_frame = self._compute_relative_values(df)

        return self

    def set_metadata(self, metadata: Union[ChartMetadata, Dict]) -> 'QSnapBarChartBuilder':
        """
        Set the metadata for the chart.

        Args:
            metadata: Either a ChartMetadata object or a dictionary with metadata fields

        Returns:
            Self for method chaining

        Raises:
            ValueError: If metadata format is invalid
        """
        if isinstance(metadata, dict):
            self._metadata = ChartMetadata(**metadata)
        elif isinstance(metadata, ChartMetadata):
            self._metadata = metadata
        else:
            raise ValueError("Metadata must be either a ChartMetadata object or a dictionary")

        self._validate_metadata()

        return self

    def set_image_size(self, width: int = None, height: int = None, scale: int = None) -> 'QSnapBarChartBuilder':
        """
        Set the image export dimensions.

        Args:
            width: Image width in pixels (default: 600)
            height: Image height in pixels (default: 600)
            scale: Image scale factor (default: 2)

        Returns:
            Self for method chaining
        """
        if width is not None:
            self._image_width = width
        if height is not None:
            self._image_height = height
        if scale is not None:
            self._image_scale = scale

        return self

    def build(self) -> go.Figure:
        """
        Build the chart with current data and metadata.

        Returns:
            Plotly Figure object

        Raises:
            ValueError: If data or metadata is not set
        """
        if self._data_frame is None:
            raise ValueError("Data must be set before building. Call set_data() first.")
        if self._metadata is None:
            raise ValueError("Metadata must be set before building. Call set_metadata() first.")

        self._figure = self._create_chart()
        return self._figure

    def export_to_png(self, filename: Optional[str] = None) -> None:
        """
        Export the chart to PNG file.

        Args:
            filename: Output filename (without extension). If None, uses metadata img_name.

        Raises:
            ValueError: If chart hasn't been built yet
        """
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
        """
        Get the current figure object.

        Returns:
            The plotly Figure object or None if not built yet
        """
        return self._figure

    # ========== VALIDATION METHODS ==========

    def _validate_data_frame(self, df: pd.DataFrame) -> None:
        """Validate that the DataFrame has the required structure"""
        if 'Category' not in df.columns:
            raise ValueError("DataFrame must contain a 'Category' column")

        if len(df.columns) < 2:
            raise ValueError("DataFrame must contain at least one year column besides 'Category'")

        year_columns = [col for col in df.columns if col != 'Category']
        for col in year_columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                raise ValueError(f"Year column '{col}' must contain numeric values")

    def _validate_metadata(self) -> None:
        """Validate that metadata has required fields"""
        if not self._metadata.img_name:
            raise ValueError("Metadata must include 'img_name'")
        if not self._metadata.y_label:
            raise ValueError("Metadata must include 'y_label'")

    # ========== CHART CREATION METHODS ==========

    def _create_chart(self) -> go.Figure:
        """Main method to create the complete chart"""
        x_axis = self._get_x_axis()
        y_axis = self._get_y_axis()
        labels = self._create_labels()

        # Create base figure with bars
        fig = self._add_bars(x_axis, y_axis, labels)

        # Add connecting lines between bars
        shapes = self._create_connecting_lines(x_axis)

        # Apply layout
        fig = self._apply_layout(fig, shapes)

        # Add column totals
        fig = self._add_column_totals(fig, x_axis)

        # Add callout annotations
        line_coords = self._compute_line_coordinates(x_axis)
        fig = self._add_callout_annotations(fig, x_axis, line_coords)

        return fig

    def _add_bars(self, x_axis: List[str], y_axis: List[str], labels: Dict[str, List[str]]) -> go.Figure:
        """Create the base figure with stacked bars"""
        fig = go.Figure()

        for category in y_axis:
            values = self._data_frame[self._data_frame['Category'] == category][x_axis].values[0]
            category_labels = labels[category]

            fig.add_trace(go.Bar(
                name=category,
                x=x_axis,
                y=values,
                marker={
                    'color': self.CATEGORY_COLORS.get(category, '#CCCCCC'),
                    'line': {
                        'color': self.BAR_BORDER_COLOR,
                        'width': self.BAR_BORDER_WIDTH
                    }
                },
                text=category_labels,
                textposition='inside',
                insidetextanchor='middle',
                textfont={
                    'size': self.BAR_LABEL_FONT_SIZE,
                    'color': 'black'
                },
                legendgroup=category
            ))

        return fig

    def _apply_layout(self, fig: go.Figure, shapes: List[Dict]) -> go.Figure:
        """Apply layout configuration to the figure"""
        fig.update_layout(
            title={
                'text': self._metadata.img_name,
                'x': 0.5,
                'xanchor': 'center',
                'y': self.TITLE_Y_POSITION,
                'yanchor': 'top'
            },
            margin={'t': self.TOP_MARGIN},
            xaxis_title={
                'text': 'Year',
                'font': {'weight': 'bold'}
            },
            xaxis={'tickfont': {'weight': 'bold'}},
            yaxis_title={
                'text': self._metadata.y_label,
                'font': {'weight': 'bold'}
            },
            yaxis={
                'tickformat': '.0%',
                'tickvals': [0, 0.25, 0.5, 0.75, 1],
                'ticktext': ['0%', '25%', '50%', '75%', '100%'],
                'tickfont': {'weight': 'bold'}
            },
            barmode='stack',
            legend={
                'orientation': 'h',
                'yanchor': 'top',
                'y': self.LEGEND_Y_POSITION,
                'xanchor': 'center',
                'x': 0.5,
                'traceorder': 'normal',
            },
            font={'size': self.FONT_SIZE},
            plot_bgcolor='white',
            hovermode=False,
            shapes=shapes
        )

        return fig

    def _add_column_totals(self, fig: go.Figure, x_axis: List[str]) -> go.Figure:
        """Add total count annotations at the top of each column"""
        for i, year in enumerate(x_axis):
            total = int(self._original_data_frame[year].sum())
            fig.add_annotation(
                x=i,
                y=self.COLUMN_TOTAL_Y_OFFSET,
                text=f"({total})",
                showarrow=False,
                font={'size': self.TITLE_FONT_SIZE, 'color': 'black'},
                yref='y'
            )

        return fig

    def _create_connecting_lines(self, x_axis: List[str]) -> List[Dict]:
        """Create connecting lines between consecutive bars"""
        bar_positions = {year: i for i, year in enumerate(x_axis)}
        line_coords = self._compute_line_coordinates(x_axis)
        shapes = []

        # Add lines connecting consecutive bars
        for i in range(len(x_axis) - 1):
            year_from = x_axis[i]
            year_to = x_axis[i + 1]

            for category in self._data_frame['Category'].tolist():
                for edge in ['top', 'bottom']:
                    shapes.append({
                        'type': 'line',
                        'x0': bar_positions[year_from] + self.BAR_WIDTH,
                        'y0': line_coords[year_from][category][edge],
                        'x1': bar_positions[year_to] - self.BAR_WIDTH,
                        'y1': line_coords[year_to][category][edge],
                        'line': {
                            'color': self.CONNECTING_LINE_COLOR,
                            'width': self.CONNECTING_LINE_WIDTH
                        }
                    })

        # Add axis lines
        shapes.extend(self._create_axis_lines(len(x_axis)))

        return shapes

    def _create_axis_lines(self, num_years: int) -> List[Dict]:
        """Create left Y-axis and bottom X-axis lines"""
        return [
            {
                'type': 'line',
                'x0': -0.5, 'y0': 0,
                'x1': -0.5, 'y1': 1,
                'xref': 'x', 'yref': 'y',
                'line': {'color': self.AXIS_LINE_COLOR, 'width': self.AXIS_LINE_WIDTH}
            },
            {
                'type': 'line',
                'x0': -0.5, 'y0': 0,
                'x1': num_years - 0.5, 'y1': 0,
                'xref': 'x', 'yref': 'y',
                'line': {'color': self.AXIS_LINE_COLOR, 'width': self.AXIS_LINE_WIDTH}
            }
        ]

    def _add_callout_annotations(self, fig: go.Figure, x_axis: List[str], line_coords: Dict) -> go.Figure:
        """Add callout boxes for Unknown and None/Bad categories on the last column"""
        last_year = x_axis[-1]
        categories = self._data_frame['Category'].tolist()
        trigrams_data = self._metadata.trigrams.get(last_year, {})

        # Add Unknown callout
        if 'Unknown' in categories:
            self._add_category_callout(
                fig, 'Unknown', last_year, len(x_axis), line_coords,
                trigrams_data, self.UNKNOWN_CALLOUT_BG, self.UNKNOWN_CALLOUT_BORDER,
                self.UNKNOWN_ARROW_COLOR, self.UNKNOWN_CALLOUT_X_OFFSET,
                self.UNKNOWN_ARROW_X_OFFSET
            )

        # Add None or Bad callout
        target_category = 'None' if 'None' in categories else ('Bad' if 'Bad' in categories else None)
        if target_category:
            self._add_category_callout(
                fig, target_category, last_year, len(x_axis), line_coords,
                trigrams_data, self.BAD_NONE_CALLOUT_BG, self.BAD_NONE_CALLOUT_BORDER,
                self.BAD_NONE_ARROW_COLOR, self.BAD_NONE_CALLOUT_X_OFFSET,
                self.BAD_NONE_ARROW_X_OFFSET
            )

        return fig

    def _add_category_callout(self, fig: go.Figure, category: str, year: str,
                              num_years: int, line_coords: Dict, trigrams_data: Dict,
                              bg_color: str, border_color: str, arrow_color: str,
                              callout_x_offset: int, arrow_x_offset: float) -> None:
        """Add a single callout annotation for a category"""
        value = self._data_frame[self._data_frame['Category'] == category][year].values[0]
        if value <= 0:
            return

        top = line_coords[year][category]['top']
        mid = (line_coords[year][category]['bottom'] + top) / 2
        trigrams = trigrams_data.get(category, [])
        trigram_text = '<br>'.join(trigrams) if trigrams else category

        # Add arrow
        fig.add_annotation(
            x=num_years - 1 + 0.45,
            y=mid,
            ax=num_years - 1 + 0.45 + arrow_x_offset,
            ay=mid,
            xref='x', yref='y',
            axref='x', ayref='y',
            showarrow=True,
            arrowhead=self.ARROW_HEAD_SIZE,
            arrowsize=self.ARROW_SIZE,
            arrowwidth=self.ARROW_WIDTH,
            arrowcolor=arrow_color,
            text=''
        )

        # Add callout box
        fig.add_annotation(
            x=num_years - 1,
            y=top,
            text=trigram_text,
            showarrow=False,
            xshift=callout_x_offset,
            bgcolor=bg_color,
            bordercolor=border_color,
            borderwidth=self.CALLOUT_BORDER_WIDTH,
            borderpad=self.CALLOUT_BORDER_PAD,
            font={
                'size': self.CALLOUT_FONT_SIZE,
                'color': 'black',
                'family': 'monospace'
            },
            align='left',
            yanchor='top',
            xanchor='left'
        )

    # ========== DATA PROCESSING METHODS ==========

    def _compute_relative_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert absolute values to relative percentages"""
        df_relative = df.copy()
        x_axis = self._get_x_axis_from_df(df)

        for year in x_axis:
            total = df[year].sum()
            df_relative[year] = (df[year] / total).round(4)

        return df_relative

    def _create_labels(self) -> Dict[str, List[str]]:
        """Create labels showing percentage and absolute values for each bar segment"""
        x_axis = self._get_x_axis()
        labels_dict = {}

        for year in x_axis:
            original_vals = self._original_data_frame[year].values
            relative_vals = self._data_frame[year].values
            categories = self._data_frame['Category'].tolist()

            # Calculate exact percentages and rounded versions
            exact_percentages = [rel * 100 for rel in relative_vals]
            percentages = [round(p) for p in exact_percentages]

            # Adjust to ensure sum is exactly 100%
            total = sum(percentages)
            if total != 100:
                errors = [abs(exact - rounded) for exact, rounded in zip(exact_percentages, percentages)]
                max_error_idx = errors.index(max(errors))
                percentages[max_error_idx] += (100 - total)

            # Store labels for each category
            for i, category in enumerate(categories):
                if category not in labels_dict:
                    labels_dict[category] = []
                labels_dict[category].append(f"{percentages[i]}% ({int(original_vals[i])})")

        return labels_dict

    def _compute_line_coordinates(self, x_axis: List[str]) -> Dict[str, Dict[str, Dict[str, float]]]:
        """Calculate the top and bottom coordinates for each category segment"""
        cumulative_heights = {}

        for year in x_axis:
            cumulative_heights[year] = {}
            cumsum = 0

            for category in self._data_frame['Category'].tolist():
                value = self._data_frame[self._data_frame['Category'] == category][year].values[0]
                cumulative_heights[year][category] = {
                    'bottom': cumsum,
                    'top': cumsum + value
                }
                cumsum += value

        return cumulative_heights

    # ========== HELPER METHODS ==========

    def _get_x_axis(self) -> List[str]:
        return self._data_frame.columns.drop('Category').tolist()

    def _get_x_axis_from_df(self, df: pd.DataFrame) -> List[str]:
        return df.columns.drop('Category').tolist()

    def _get_y_axis(self) -> List[str]:
        return self._data_frame['Category'].tolist()




# ========== EXAMPLE USAGE ==========

if __name__ == "__main__":

    data = {
        'Category': ['Full', 'Good', 'Low', 'None', 'Unknown'],
        '2022': [12, 12, 2, 10, 3],
        '2023': [22, 18, 9, 5, 3],
        '2024': [34, 12, 5, 1, 3],
        '2025': [35, 11, 3, 2, 4]
    }

    metadata = {
        'img_name': 'Coverage Score Trend',
        'y_label': 'Coverage score',
        'trigrams': {
            '2025': {
                'Unknown': ['XXX', 'SDF', 'YEW', 'IOP'],
                'None': ['TRD', 'ABC']
            }
        }
    }

    # Create and build chart
    builder = QSnapBarChartBuilder()
    fig = builder.set_data(data).set_metadata(metadata).set_image_size(600, 600).build()
    fig.show()
    builder.export_to_png()

    # Reuse builder with new data
    new_data = {
        'Category': ['Good', 'Average', 'Bad', 'Unknown'],
        '2022': [12, 12, 2, 10],
        '2023': [22, 18, 9, 5],
        '2024': [34, 12, 5, 0]
    }

    new_metadata = {
        'img_name': 'Quality Trend',
        'y_label': 'Quality score'
    }

    fig2 = builder.set_data(new_data).set_metadata(new_metadata).build()
    fig2.show()