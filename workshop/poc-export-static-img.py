# import plotly.express as px
#
# df = px.data.medals_long()
#
# data = {
#     'Date': [2022, 2023, 2024, 2025],
#     ''
# }
#
# fig = px.bar(df, x="medal", y="count", color="nation", text="nation")
# fig.show()
import pandas as pd
import plotly.graph_objects as go

# Create the DataFrame
data = {
    'Category': ['Good', 'Average', 'Bad'],
    '2022': [12, 12, 2],
    '2023': [22, 18, 9],
    '2024': [34, 12, 5]
}

df = pd.DataFrame(data)

# Define modern, web-friendly colors
colors = {
    'Good': '#86EFAC',      # Light green (modern, soft)
    'Average': '#D1D5DB',   # Light grey (neutral, clean)
    'Bad': '#FCA5A5'        # Light red (soft warning color)
}

# Darker colors for the trend lines
line_colors = {
    'Good': '#22C55E',      # Darker green
    'Average': '#6B7280',   # Darker grey
    'Bad': '#EF4444'        # Darker red
}

# Create the figure
fig = go.Figure()

# Years for x-axis
years = ['2022', '2023', '2024']
categories_order = ['Bad', 'Average', 'Good']

# Calculate cumulative heights for each category
cumulative_heights = {}
for year in years:
    cumulative_heights[year] = {}
    cumsum = 0
    for category in categories_order:
        value = df[df['Category'] == category][year].values[0]
        cumulative_heights[year][category] = {'bottom': cumsum, 'top': cumsum + value}
        cumsum += value

# Add bar traces for each category (in order: Good, Average, Bad for legend)
for category in ['Good', 'Average', 'Bad']:
    values = df[df['Category'] == category][years].values[0]

    fig.add_trace(go.Bar(
        name=category,
        x=years,
        y=values,
        marker_color=colors[category],
        text=values,
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(size=14, color='black'),
        hovertemplate='<extra></extra>',
        legendgroup=category
    ))

# Prepare shapes for connecting lines
shapes = []

# Bar positions (0, 1, 2 for categorical x-axis)
bar_positions = {year: i for i, year in enumerate(years)}
bar_width = 0.4  # Half of the actual bar width for edge alignment

for category in categories_order:
    # Connect 2022 to 2023
    # Upper edge line
    shapes.append(dict(
        type='line',
        x0=bar_positions['2022'] + bar_width,
        y0=cumulative_heights['2022'][category]['top'],
        x1=bar_positions['2023'] - bar_width,
        y1=cumulative_heights['2023'][category]['top'],
        line=dict(color=line_colors[category], width=1.5)
    ))

    # Lower edge line
    shapes.append(dict(
        type='line',
        x0=bar_positions['2022'] + bar_width,
        y0=cumulative_heights['2022'][category]['bottom'],
        x1=bar_positions['2023'] - bar_width,
        y1=cumulative_heights['2023'][category]['bottom'],
        line=dict(color=line_colors[category], width=1.5)
    ))

    # Connect 2023 to 2024
    # Upper edge line
    shapes.append(dict(
        type='line',
        x0=bar_positions['2023'] + bar_width,
        y0=cumulative_heights['2023'][category]['top'],
        x1=bar_positions['2024'] - bar_width,
        y1=cumulative_heights['2024'][category]['top'],
        line=dict(color=line_colors[category], width=1.5)
    ))

    # Lower edge line
    shapes.append(dict(
        type='line',
        x0=bar_positions['2023'] + bar_width,
        y0=cumulative_heights['2023'][category]['bottom'],
        x1=bar_positions['2024'] - bar_width,
        y1=cumulative_heights['2024'][category]['bottom'],
        line=dict(color=line_colors[category], width=1.5)
    ))

# Update layout
fig.update_layout(
    title='Coverage score trend',
    xaxis_title='Year',
    yaxis_title='Coverage score',
    barmode='stack',
    legend=dict(
        traceorder='normal'
    ),
    font=dict(size=12),
    plot_bgcolor='white',
    hovermode=False,
    shapes=shapes
)

# Show the figure
fig.show()

# Save as PNG with white background and 600x600 size
fig.write_image("coverage_score_trend.png",
                width=600,
                height=600,
                scale=2,  # Higher scale for better quality (2x resolution)
                format="png")