import plotly.express as px
import cv2 as cv
from dash import Dash, html, dcc, Input, Output, ctx, callback
from data_loader import DataLoader

subjects = DataLoader('data').load_data()

app = Dash(__name__, external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'])

default_subject = 'E1'
fig = px.imshow(cv.cvtColor(subjects[default_subject].get_image(), cv.COLOR_BGR2RGB))
fig.update_layout(width=911, height=512, margin=dict(l=10, r=10, b=10, t=10))
fig.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)

default_slider_max = len(subjects[default_subject].screen_images)-1
default_slider_marks = {0: "0"}
default_slider_marks[default_slider_max] = str(default_slider_max)

current_subject = default_subject

app.layout = html.Div(children=[
    html.H3(children='User Visual Attention x Saliency Model Comparison'),

    html.Div(children='''
        Developed by Julia Melgaré and Guido Mainardi for the Data Visualization class.
    '''),

    html.Div(
        [
            html.Div(dcc.Graph(figure=fig, id='image-graph'), style={'display': 'inline-block'}),
            html.Div(
                [
                    html.Div(['Select Video:', dcc.Dropdown(list(subjects.keys()), default_subject, id='subject-dropdown')]),
                    html.Br(),
                    html.Div(['Show Maps:', dcc.Checklist(['User', 'Saliency Model'], [], id='maps-checklist')])
                ],
                style={'display': 'inline-block', 'verticalAlign': 'top'}
            )
        ], 
        style={'width': '100%', 'display': 'flex', 'align-items':'top', 'justify-content':'center'}
    ),

    html.Div(
        [
            html.Button('<', n_clicks=0, id='prev-btn', style={'display': 'inline-block', 'verticalAlign': 'top'}),
            html.Div(dcc.Slider(0, default_slider_max, 1, value=0, marks=default_slider_marks, id='frame-slider'), style={'display': 'inline-block', 'width': '50%'}),
            html.Button('>', n_clicks=0, id='next-btn', style={'display': 'inline-block', 'verticalAlign': 'top'})
        ],
        style={'align-items':'center', 'justify-content':'center', 'marginLeft' : '460px'}
    )  
])

@callback(
    Output('image-graph', 'figure'),
    Input('frame-slider', 'value'),
    Input('subject-dropdown', 'value'),
    Input('maps-checklist', 'value')
)
def update_image(frame, subject, checklist):
    current_subject = subject
    subjects[subject].index = frame
    subjects[subject].heatmap_on if 'User' in checklist else subjects[subject].heatmap_off
    subjects[subject].saliency_on if 'Saliency Model' in checklist else subjects[subject].saliency_off
    fig = px.imshow(cv.cvtColor(subjects[subject].get_image(), cv.COLOR_BGR2RGB))
    fig.update_layout(width=911, height=512, margin=dict(l=10, r=10, b=10, t=10))
    fig.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)
    return fig

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