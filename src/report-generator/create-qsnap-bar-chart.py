import pandas as pd
import plotly.graph_objects as go
from typing import List, Dict

# Todo: Add the total number of product at the top of each column
# Todo: Adapt the Y-axis labels to only show 0 - 0.25 - 0.5 - 0.75 - 1
# Todo: Adapt the Y-axis labels to display % values and not decimal
# Todo: Add axis in black for better visibility
# Todo: Set the axis labels and values in bold for better visibility
# Todo: Refactor the code to make it more readable and maintainable
# Todo: Encapsulate the code to make it usable: function + data + metadata and let's go
# Todo: On the last year, add a static tooltip listing the trigrams for None/Bad and Unknow categories


def determine_x_axis(df: pd.DataFrame) -> List[str]:
    return df.columns.drop('Category').tolist()

def determine_y_axis(df: pd.DataFrame) -> List[str]:
    return df['Category'].tolist()

def add_bars(df: pd.DataFrame, x_axis: List[str], y_axis: List[str], colours: Dict[str, str], labels: Dict[str, List[str]]) -> go.Figure:

    fig = go.Figure()

    for category in y_axis:
        values = df[df['Category'] == category][x_axis].values[0]
        category_labels = labels[category]

        fig.add_trace(go.Bar(
            name=category,
            x=x_axis,
            y=values,
            marker={
                'color': colours[category],
                'line': {
                    'color': '#9CA3AF',
                    'width': 2
                }
            },
            text=category_labels,
            textposition='inside',
            insidetextanchor='middle',
            textfont={
                'size':14,
                'color':'black'
            },
            legendgroup=category
        ))

    return fig

def define_layout(fig: go.Figure, title: str, y_label: str, shapes: List[Dict[str, str]]) -> go.Figure:

    fig.update_layout(
        title={
            'text': title,
            'x':0.5,                # Center horizontally (0.5 = 50% from left)
            'xanchor':'center',
            'y': 0.99,              # Lower the title position (default is ~0.98)
            'yanchor': 'top'
        },
        margin={
            't': 10
        },
        xaxis_title='Year',
        yaxis_title=y_label,
        barmode='stack',
        legend={
            'orientation':'h',      # Horizontal orientation
            'yanchor':'top',        # Anchor to top of legend box
            'y':-0.08,              # Position below graph (negative = below)
            'xanchor': 'center',    # Anchor to center of legend box
            'x':0.5,                # Center horizontally (0.5 = 50% from left)
            'traceorder': 'normal',
        },
        font={'size': 12},
        plot_bgcolor='white',
        hovermode=False,
        shapes=shapes
    )

    return fig


def compute_line_coords(df: pd.DataFrame, x_axis: List[str]) -> List[Dict[str, int]]:
    cumulative_heights = {}
    for year in x_axis:
        cumulative_heights[year] = {}
        cumsum = 0
        for category in df['Category'].to_list():
            value = df[df['Category'] == category][year].values[0]
            cumulative_heights[year][category] = {'bottom': cumsum, 'top': cumsum + value}
            cumsum += value

    return cumulative_heights


def add_connecting_lines(df: pd.DataFrame, x_axis: List[str]) -> List[Dict[str, str|int]]:
    bar_positions = {year: i for i, year in enumerate(x_axis)}
    bar_width = 0.4  # Half of the actual bar width for edge alignment

    line_coords: List[Dict[str, int]] = compute_line_coords(df, x_axis)

    shapes = []

    for i in range(len(x_axis) - 1):
        year_from = x_axis[i]
        year_to = x_axis[i + 1]

        for category in df['Category'].to_list():
            for edge in ['top', 'bottom']:
                shapes.append({
                    'type':'line',
                    'x0':bar_positions[year_from] + bar_width,
                    'y0':line_coords[year_from][category][edge],
                    'x1':bar_positions[year_to] - bar_width,
                    'y1':line_coords[year_to][category][edge],
                    'line': {
                        'color':'#9CA3AF',
                        'width':1.5
                    }
                })

    return shapes


def qsnap_create_bar_chart(df: pd.DataFrame, metadata: Dict[str, str], labels: Dict[str, List[str]]) -> go.Figure:

    colours: Dict[str, str] = {
        'Full':    '#4ADE80',   # Medium green (lighter than Good)
        'Good':    '#86EFAC',   # Light green
        'Average': '#D1D5DB',   # Light grey
        'Low':     '#FDE047',   # Light yellow (warning color)
        'Bad':     '#FCA5A5',   # Light red
        'None':    '#FCA5A5',   # Light red
        'Unknown': '#FFFFFF'    # White
    }

    x_axis: List[str] = determine_x_axis(df)
    y_axis: List[str] = determine_y_axis(df)

    fig: go.Figure = add_bars(df, x_axis, y_axis, colours, labels)
    shapes = add_connecting_lines(df, x_axis)
    fig: go.Figure = define_layout(fig, metadata['img_name'], metadata['y_label'], shapes)
    return fig


def qsnap_export_to_png_web(fig: go.Figure, image_name: str) -> None:
    filename = image_name.strip().lower().replace(' ', '_') + ".png"
    fig.write_image(filename, width=600, height=600, scale=2, format="png")



def compute_relative_values(df: pd.DataFrame) -> pd.DataFrame:
    df_relative: pd.DataFrame = df.copy()
    x_axis: List[str] = determine_x_axis(df)
    for year in x_axis:
        total: int = df[year].sum()
        df_relative[year] = (df[year] / total).round(4)

    return df_relative

def create_labels(df_original: pd.DataFrame, df_relative: pd.DataFrame) -> dict[str, List[str]]:
    x_axis: List[str] = determine_x_axis(df_original)
    labels_dict = {}
    for category in df_original['Category'].tolist():
        original_values = df_original[df_original['Category'] == category][x_axis].values[0]
        relative_values = df_relative[df_relative['Category'] == category][x_axis].values[0]
        labels_dict[category] = [f"{rel * 100:.0f}% ({int(orig)})" for orig, rel in zip(original_values, relative_values)]

    return labels_dict

def create_labels2(df_original: pd.DataFrame, df_relative: pd.DataFrame) -> dict[str, List[str]]:
    x_axis: List[str] = determine_x_axis(df_original)
    labels_dict = {}

    for year in x_axis:
        original_vals = df_original[year].values
        relative_vals = df_relative[year].values
        categories = df_original['Category'].tolist()

        # Calculate exact percentages and rounded versions
        exact_percentages = [rel * 100 for rel in relative_vals]
        percentages = [round(p) for p in exact_percentages]

        # Adjust to ensure sum is exactly 100%
        total = sum(percentages)
        if total != 100:
            # Find value with largest rounding error
            errors = [abs(exact - rounded) for exact, rounded in zip(exact_percentages, percentages)]
            max_error_idx = errors.index(max(errors))
            percentages[max_error_idx] += (100 - total)

        # Store labels for each category
        for i, category in enumerate(categories):
            if category not in labels_dict:
                labels_dict[category] = []
            labels_dict[category].append(f"{percentages[i]}% ({int(original_vals[i])})")

    return labels_dict


if __name__ == "__main__":

    data = {
        'Category': ['Good', 'Average', 'Bad', 'Unknown'],
        '2022': [12, 12, 2, 10],
        '2023': [22, 18, 9, 5],
        '2024': [34, 12, 5, 0]
    }

    data = {
        'Category': ['Full', 'Good', 'Low', 'None', 'Unknown'],
        '2022': [12, 12, 2, 10, 3],
        '2023': [22, 18, 9, 5, 3],
        '2024': [34, 12, 5, 0, 3]
    }
    metaData = {
        'img_name': 'Coverage Score Trend',
        'y_label': 'Coverage score'
    }
    df = pd.DataFrame(data)
    df_rel = compute_relative_values(df)
    labels: Dict[str, List[str]] = create_labels2(df, df_rel)

    fig = qsnap_create_bar_chart(df_rel, metaData, labels)
    fig.show()
    qsnap_export_to_png_web(fig, metaData['img_name'])
