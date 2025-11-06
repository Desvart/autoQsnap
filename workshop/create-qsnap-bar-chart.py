import pandas as pd
import plotly.graph_objects as go
from typing import List, Dict

# Fixme: Fix the callout distance to last column
# Fixme: Fix the callout arrow distance between column and callout

# Todo: Refactor the code to make it more readable and maintainable
# Todo: Encapsulate the code to make it usable: Object => function + data + metadata and let's go


def add_column_totals(fig: go.Figure, df_original: pd.DataFrame, x_axis: List[str]) -> go.Figure:
    """Add total count annotations at the top of each column"""
    i = 0
    for year in x_axis:
        total = int(df_original[year].sum())
        fig.add_annotation(
            x=i,
            y=1.02,  # Slightly above the top of the chart
            text=f"({total})",
            showarrow=False,
            font={'size': 14, 'color': 'black'},
            yref='y'
        )
        i = i+1
    return fig

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
        xaxis_title={
            'text': 'Year',
            'font': {'weight': 'bold'}
        },
        xaxis={
            'tickfont': {'weight': 'bold'}
        },
        yaxis_title={
            'text': y_label,
            'font': {'weight': 'bold'}
        },
        yaxis={
            'tickformat': '.0%',              # Format as percentage with 0 decimals
            'tickvals': [0, 0.25, 0.5, 0.75, 1],  # Only show these values
            'ticktext': ['0%', '25%', '50%', '75%', '100%'],  # Custom labels
            'tickfont': {'weight': 'bold'}
        },
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


def compute_line_coords(df: pd.DataFrame, x_axis: List[str]) -> Dict[str, int]:
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

    line_coords: Dict[str, int] = compute_line_coords(df, x_axis)

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

    # Left Y-axis line
    shapes.append({
        'type': 'line',
        'x0': -0.5,
        'y0': 0,
        'x1': -0.5,
        'y1': 1,
        'xref': 'x',
        'yref': 'y',
        'line': {
            'color': 'black',
            'width': 2
        }
    })

    # Bottom X-axis line
    shapes.append({
        'type': 'line',
        'x0': -0.5,
        'y0': 0,
        'x1': len(x_axis) - 0.5,
        'y1': 0,
        'xref': 'x',
        'yref': 'y',
        'line': {
            'color': 'black',
            'width': 2
        }
    })

    return shapes

def add_callout_annotations(fig: go.Figure, df: pd.DataFrame, x_axis: List[str], line_coords: Dict, metadata: Dict) -> go.Figure:
    """Add styled callout boxes with trigram lists pointing to Unknown and None/Bad categories on the last column"""
    last_year = x_axis[-1]
    categories = df['Category'].tolist()

    # Get trigrams from metadata if available
    trigrams_data = metadata.get('trigrams', {}).get(last_year, {})

    # Check if Unknown category exists and has value > 0
    if 'Unknown' in categories:
        unknown_value = df[df['Category'] == 'Unknown'][last_year].values[0]
        if unknown_value > 0:
            # Get top and middle position of Unknown section
            unknown_top = line_coords[last_year]['Unknown']['top']
            unknown_mid = (line_coords[last_year]['Unknown']['bottom'] +
                           line_coords[last_year]['Unknown']['top']) / 2

            # Get trigrams for Unknown category
            unknown_trigrams = trigrams_data.get('Unknown', [])
            trigram_text = '<br>'.join(unknown_trigrams) if unknown_trigrams else 'Unknown'

            # Add a separate horizontal arrow from bar to callout at middle height
            fig.add_annotation(
                x=len(x_axis) - 1 + 0.45,  # Start just after the bar
                y=unknown_mid,
                ax=len(x_axis) - 1 + 0.45 + 0.75,  # End just before the callout
                ay=unknown_mid,
                xref='x',
                yref='y',
                axref='x',
                ayref='y',
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor='#6B7280',
                text=''
            )

            # Add the callout box without arrow
            fig.add_annotation(
                x=len(x_axis) - 1,
                y=unknown_top,
                text=trigram_text,
                showarrow=False,
                xshift=120,  # Horizontal offset to the right (extreme right)
                bgcolor='#F3F4F6',
                bordercolor='#6B7280',
                borderwidth=2,
                borderpad=8,
                font={
                    'size': 11,
                    'color': 'black',
                    'family': 'monospace'
                },
                align='left',
                yanchor='top',
                xanchor='left'
            )



    # Check for None or Bad category (only one should exist)
    target_category = None
    if 'None' in categories:
        none_value = df[df['Category'] == 'None'][last_year].values[0]
        if none_value > 0:
            target_category = 'None'
    elif 'Bad' in categories:
        bad_value = df[df['Category'] == 'Bad'][last_year].values[0]
        if bad_value > 0:
            target_category = 'Bad'

    if target_category:
        # Get top and middle position of None/Bad section
        target_top = line_coords[last_year][target_category]['top']
        target_mid = (line_coords[last_year][target_category]['bottom'] +
                      line_coords[last_year][target_category]['top']) / 2

        # Get trigrams for None/Bad category
        target_trigrams = trigrams_data.get(target_category, [])
        trigram_text = '<br>'.join(target_trigrams) if target_trigrams else 'TBC'

        # Add a separate horizontal arrow from bar to callout at middle height
        fig.add_annotation(
            x=len(x_axis) - 1 + 0.45,  # Start just after the bar
            y=target_mid,
            ax=len(x_axis) - 1 + 0.45+0.25,  # End just before the callout
            ay=target_mid,
            xref='x',
            yref='y',
            axref='x',
            ayref='y',
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor='#DC2626',
            text=''
        )

        # Add the callout box without arrow
        fig.add_annotation(
            x=len(x_axis) - 1,
            y=target_top,
            text=trigram_text,
            showarrow=False,
            xshift=70,  # Horizontal offset to the right (between column and Unknown)
            bgcolor='#FEE2E2',
            bordercolor='#DC2626',
            borderwidth=2,
            borderpad=8,
            font={
                'size': 11,
                'color': 'black',
                'family': 'monospace'
            },
            align='left',
            yanchor='top',
            xanchor='left'
        )



    return fig



def qsnap_create_bar_chart(df: pd.DataFrame, df_original: pd.DataFrame, metadata: Dict[str, str], labels: Dict[str, List[str]]) -> go.Figure:

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

    fig = add_column_totals(fig, df_original, x_axis)
    line_coords = compute_line_coords(df, x_axis)
    fig = add_callout_annotations(fig, df, x_axis, line_coords, metadata)

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

    # data = {
    #     'Category': ['Good', 'Average', 'Bad', 'Unknown'],
    #     '2022': [12, 12, 2, 10],
    #     '2023': [22, 18, 9, 5],
    #     '2024': [34, 12, 5, 0]
    # }

    data = {
        'Category': ['Full', 'Good', 'Low', 'None', 'Unknown'],
        '2022': [12, 12, 2, 10, 3],
        '2023': [22, 18, 9, 5, 3],
        '2024': [34, 12, 5, 1, 3],
        '2025': [35, 11, 3, 2, 4]
    }
    metaData = {
        'img_name': 'Coverage Score Trend',
        'y_label': 'Coverage score',
        'trigrams': {
            '2025': {
                'Unknown': ['XXX', 'SDF', 'YEW', 'IOP'],
                'None': ['TRD', 'ABC']
            }
        }
    }
    df = pd.DataFrame(data)
    df_rel = compute_relative_values(df)
    labels: Dict[str, List[str]] = create_labels(df, df_rel)

    fig = qsnap_create_bar_chart(df_rel, df, metaData, labels)
    fig.show()
    qsnap_export_to_png_web(fig, f'../../dist/{metaData['img_name']}')
