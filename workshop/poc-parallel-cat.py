import pandas as pd
import plotly.graph_objects as go

# Create the DataFrame
data = {
    'Category': ['Good', 'Average', 'Bad'],
    '2022': [5, 12, 2],
    '2023': [42, 50, 84],
    '2024': [34, 12, 5]
}

df = pd.DataFrame(data)

# Define modern, web-friendly colors
color_map = {
    'Good': '#86EFAC',      # Light green
    'Average': '#D1D5DB',   # Light grey
    'Bad': '#FCA5A5'        # Light red
}

# Calculate cumulative heights for positioning text
years = ['2022', '2023', '2024']
cumulative_heights = {}
for year in years:
    cumulative_heights[year] = {}
    cumsum = 0
    for category in ['Bad', 'Average', 'Good']:
        value = df[df['Category'] == category][year].values[0]
        cumulative_heights[year][category] = {'bottom': cumsum, 'top': cumsum + value, 'center': cumsum + value/2}
        cumsum += value

# Create the parallel categories diagram
fig = go.Figure(data=[go.Parcats(
    dimensions=[
        {
            'label': '2022',
            'values': ['Good'] * 5 + ['Average'] * 12 + ['Bad'] * 2,
            'categoryorder': 'array',
            'categoryarray': ['Good', 'Average', 'Bad']
        },
        {
            'label': '2023',
            'values': ['Good'] * 42 + ['Average'] * 50 + ['Bad'] * 84,
            'categoryorder': 'array',
            'categoryarray': ['Good', 'Average', 'Bad']
        },
        {
            'label': '2024',
            'values': ['Good'] * 34 + ['Average'] * 12 + ['Bad'] * 5,
            'categoryorder': 'array',
            'categoryarray': ['Good', 'Average', 'Bad']
        }
    ],
    line={
        'color': [color_map['Good']] * 5 + [color_map['Average']] * 12 + [color_map['Bad']] * 2,
        'colorscale': [[0, color_map['Good']], [0.5, color_map['Average']], [1, color_map['Bad']]]
    },
    labelfont={'size': 14, 'family': 'Arial'},
    tickfont={'size': 12, 'family': 'Arial'},
    arrangement='freeform',
    hoverinfo='none',
    bundlecolors=False
)])

# Add annotations for values in the center of each stack
year_positions = {'2022': 0.15, '2023': 0.5, '2024': 0.85}  # x positions for each year column
total_height = sum(df['2022'])  # Total height for normalization

annotations = []
for year in years:
    for category in ['Good', 'Average', 'Bad']:
        value = df[df['Category'] == category][year].values[0]
        # Calculate y position (normalized between 0 and 1)
        y_pos = cumulative_heights[year][category]['center'] / total_height

        annotations.append(dict(
            x=year_positions[year],
            y=y_pos,
            text=str(value),
            showarrow=False,
            font=dict(size=14, color='black'),
            xref='paper',
            yref='paper'
        ))

# Update layout with larger categories and y-axis
fig.update_layout(
    title='Coverage score trend',
    font=dict(size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=100, r=100, t=80, b=50),
    annotations=annotations,
    yaxis=dict(
        title='Coverage score',
        showticklabels=True,
        showgrid=True,
        gridcolor='lightgray',
        range=[0, total_height],
        side='left'
    ),
    width=800,
    height=600
)

# Show the figure
fig.show()

# Save as PNG with white background and 600x600 size
fig.write_image("coverage_score_parallel_categories.png",
                width=600,
                height=600,
                scale=2,
                format="png")