import plotly.express as px
from dash import Dash, html, dcc, Input, Output, callback
import cv2 as cv
import os
from data_loader import DataLoader


subjects = DataLoader('data').load_data()

app = Dash(__name__)

default_fig = subjects['E1'].get_image()
fig = px.imshow(default_fig)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),
    html.Div(
        [
            dcc.Dropdown(['E1', 'E2', 'E3'], 'E1', id='demo-dropdown')
        ],
        style={"width": "30%"},
    )
])

@callback(
    Output('example-graph', 'figure'),
    Input('demo-dropdown', 'value')
)
def update_output(value):
    return px.imshow(subjects[value].get_image())

if __name__ == '__main__':
    app.run(debug=False)