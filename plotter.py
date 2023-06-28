import plotly.express as px
from dash import Dash, html, dcc, Input, Output, ctx, callback
from data_loader import DataLoader

subjects = DataLoader('data').load_data()

app = Dash(__name__)

default_subject = 'E1'
fig = px.imshow(subjects[default_subject].get_image())
default_slider_max = len(subjects[default_subject].screen_images)-1
default_slider_marks = {0: "0"}
default_slider_marks[default_slider_max] = str(default_slider_max)

current_subject = default_subject

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    html.Div(dcc.Graph(figure=fig, id='image-graph'), style={'width': '100%'}),

    html.Div(
        [
            html.Button('<', n_clicks=0, id='prev-btn', style={'display': 'inline-block', 'verticalAlign': 'top'}),
            html.Div(dcc.Slider(0, default_slider_max, 1, value=0, marks=default_slider_marks, id='frame-slider'), style={'display': 'inline-block', 'width': '80%'}),
            html.Button('>', n_clicks=0, id='next-btn', style={'display': 'inline-block', 'verticalAlign': 'top'})
        ],
        style={'width': '100%', 'display': 'flex', 'align-items':'center', 'justify-content':'center'}
    ),
    
    html.Div(
        [
            dcc.Dropdown(list(subjects.keys()), 'E1', id='subject-dropdown'),
        ],
        style={'width': '30%'},
    )
])

@callback(
    Output('image-graph', 'figure'),
    Input('frame-slider', 'value'),
    Input('subject-dropdown', 'value')
)
def update_image(frame, subject):
    current_subject = subject
    subjects[subject].index = frame
    return px.imshow(subjects[subject].get_image())

@callback(
    Output('frame-slider', 'value'),
    Input('subject-dropdown', 'value'),
    Input('next-btn', 'n_clicks'),
    Input('prev-btn', 'n_clicks'),
)
def update_slider_value(subject, next_btn, prev_btn):
    if 'next-btn' == ctx.triggered_id:
        subjects[subject].next
        return subjects[subject].index
    if 'prev-btn' == ctx.triggered_id:
        subjects[subject].prev
        return subjects[subject].index
    return 0

@callback(
    Output('frame-slider', 'max'),
    Output('frame-slider', 'marks'),
    Input('frame-slider', 'value'),
    Input('subject-dropdown', 'value')
)
def update_slider(frame, subject):
    max = len(subjects[subject].screen_images)-1
    marks = {0:'0'}
    marks[frame] = str(frame)
    marks[max] = str(max)
    return max, marks

@callback(
    Output('next-btn', 'disabled'),
    Output('prev-btn', 'disabled'),
    Input('frame-slider', 'value')
)
def disable_buttons(frame):
    return (frame >= len(subjects[current_subject].screen_images)-1), (frame <= 0)

if __name__ == '__main__':
    app.run(debug=False)