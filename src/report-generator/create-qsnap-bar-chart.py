import pandas as pd
import plotly.graph_objects as go
from typing import List, Dict


def determine_x_axis(df: pd.DataFrame) -> List[str]:
    return df.columns.drop('Category').tolist()

def determine_y_axis(df: pd.DataFrame) -> List[str]:
    return df['Category'].tolist()

def add_bars(df: pd.DataFrame, x_axis: List[str], y_axis: List[str], colours: Dict[str, str]) -> go.Figure:

    fig = go.Figure()

    for category in y_axis:
        values = df[df['Category'] == category][x_axis].values[0]
        fig.add_trace(go.Bar(
            name=category,
            x=x_axis,
            y=values,
            marker={
                'color': colours[category]
            },
            text=values,
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


def compute_line_coords() -> List[Dict[str, int]]:
    cumulative_heights = {}
    for year in years:
        cumulative_heights[year] = {}
        cumsum = 0
        for category in categories_order:
            value = df[df['Category'] == category][year].values[0]
            cumulative_heights[year][category] = {'bottom': cumsum, 'top': cumsum + value}
            cumsum += value

    return cumulative_heights


def add_connecting_lines(df: pd.DataFrame, x_axis: List[str]) -> List[Dict[str, str|int]]:
    bar_positions = {year: i for i, year in enumerate(x_axis)}
    bar_width = 0.4  # Half of the actual bar width for edge alignment

    line_coords: List[Dict[str, int]] = compute_line_coords()

    shapes = []
    shapes.append({
        'type':'line',
        'x0':bar_positions['2022'] + bar_width,
        'y0':cumulative_heights['2022'][category]['top'],
        'x1':bar_positions['2023'] - bar_width,
        'y1':cumulative_heights['2023'][category]['top'],
        'line': {
            'color':line_colors[category],
            'width':1.5
        }
    })
    
    return shapes


def qsnap_create_bar_chart(df: pd.DataFrame, metadata: Dict[str, str]) -> go.Figure:

    colours: Dict[str, str] = {
        'Good':    '#86EFAC',   # Light green
        'Average': '#D1D5DB',   # Light grey
        'Bad':     '#FCA5A5'    # Light red
    }

    x_axis: List[str] = determine_x_axis(df)
    y_axis: List[str] = determine_y_axis(df)

    fig: go.Figure = add_bars(df, x_axis, y_axis, colours)
    shapes = add_connecting_lines(df, x_axis)
    fig: go.Figure = define_layout(fig, metadata['img_name'], metadata['y_label'], shapes)
    return fig


def qsnap_export_to_png_web(fig: go.Figure, image_name: str) -> None:
    filename = image_name.strip().lower().replace(' ', '_') + ".png"
    fig.write_image(filename, width=600, height=600, scale=2, format="png")


if __name__ == "__main__":

    data = {
        'Category': ['Good', 'Average', 'Bad'],
        '2022': [12, 12, 2],
        '2023': [22, 18, 9],
        '2024': [34, 12, 5]
    }
    metaData = {
        'img_name': 'Coverage Score Trend',
        'y_label': 'Coverage score'
    }
    df = pd.DataFrame(data)

    fig = qsnap_create_bar_chart(df, metaData)
    fig.show()
    qsnap_export_to_png_web(fig, metaData['img_name'])
