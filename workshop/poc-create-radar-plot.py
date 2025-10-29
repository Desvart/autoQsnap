# import plotly.express as px
#
# df = px.data.iris()
# fig = px.scatter(df, x='sepal_width', y='sepal_length', color='species')
# fig.show()
# fig.write_html("./file.html")


# import plotly.graph_objects as go
#
# categories = ['processing cost','mechanical properties','chemical stability',
#               'thermal stability', 'device integration']
#
# fig = go.Figure()
#
# fig.add_trace(go.Scatterpolar(
#     r=[1, 5, 2, 2, 3],
#     theta=categories,
#     fill='toself',
#     name='Product A'
# ))
# fig.add_trace(go.Scatterpolar(
#     r=[4, 3, 2.5, 1, 2],
#     theta=categories,
#     fill='toself',
#     name='Product B'
# ))
#
# fig.update_layout(
#     polar=dict(
#         radialaxis=dict(
#             visible=True,
#             range=[0, 5]
#         )),
#     showlegend=True
# )
#
# fig.show()
# fig.write_html("./file2.html")


# imports
import plotly.graph_objects as go
import numpy as np
import pandas as pd

# categories:
categories = ['processing cost','mechanical properties','chemical stability',
              'thermal stability', 'device integration']

# values:
rVars1=[1, 5, 2, 2, 3]
rVars2=[4, 3, 2.5, 1, 2]

rAllMax = max(rVars1+rVars2)

# colors
values = [3,5]
colors = ['rgba(255, 0, 0, 0.9)', 'rgba(0, 255, 0, 0.9)', ]

# some calcultations to place all elements
slices=len(rVars1)
fields=[max(rVars1)]*slices
circle_split = [360/slices]*(slices)
theta= 0
thetas=[0]
for t in circle_split:
    theta=theta+t
    thetas.append(theta)
thetas

# set up label positions
df_theta=pd.DataFrame({'theta':thetas, 'positions':['middle right', 'middle right',
                                                    'bottom center', 'middle left',
                                                    'middle left', 'middle left']})


# plotly
fig = go.Figure()

# "background"
for t in range(0, len(colors)):
    fig.add_trace(go.Barpolar(
        r=[values[t]],
        width=360,
        marker_color=[colors[t]],
        opacity=0.6,
        # name = 'Range ' + str(t+1),
        name = ' ',
        showlegend=False,
        hovertemplate = 'Zone x',
    ))
    t=t+1

for r, cat in enumerate(categories):
    #print(r, cat)
    fig.add_trace(go.Scatterpolar(
        text = cat,
        r = [rAllMax],
        theta = [thetas[r]],
        mode = 'lines+text+markers',
        fill='toself',
        fillcolor='rgba(255, 255, 255, 0.4)',
        line = dict(color='black'),
        #textposition='bottom center',
        textposition=df_theta[df_theta['theta']==thetas[r]]['positions'].values[0],
        marker = dict(line_color='white', color = 'black'),
        marker_symbol ='circle',
        name = cat,
        showlegend = False))



# trace 1
fig.add_trace(go.Scatterpolar(
    #text = categories,
    r = rVars1,
    mode = 'lines+text+markers',
    fill='toself',
    fillcolor='rgba(0, 0, 255, 0.4)',
    textposition='bottom center',
    marker = dict(color = 'blue'),
    marker_symbol ='square',
    name = 'Product A'))

# trace 2
fig.add_trace(go.Scatterpolar(
    #text = categories,
    r = rVars2,
    mode = 'lines+text+markers',
    fill='toself',
    fillcolor='rgba(0, 255, 0, 0.4)',
    textposition='bottom center',
    marker = dict(color = 'Green'),
    name = 'Product B'))


# adjust layout
fig.update_layout(
    template=None,
    polar = dict(radialaxis = dict(gridwidth=0.5,
                                   range=[0, max(fields)],
                                   showticklabels=True, ticks='', gridcolor = "grey"),
                 angularaxis = dict(showticklabels=False, ticks='',
                                    rotation=45,
                                    direction = "clockwise",
                                    gridcolor = "white")))

fig.update_yaxes(showline=True, linewidth=2, linecolor='white')
fig.show()