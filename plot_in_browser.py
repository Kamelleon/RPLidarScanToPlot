import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import pickle
import traceback
import os
import plotly.graph_objs as go
import plotly.express as px

X = pickle.load(open("x_live.pkl", "rb"))

Y = pickle.load(open("movement_live.pkl", "rb"))

distance = pickle.load(open('distance_live.pkl', 'rb'))

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Graph(id='live-graph', style={'width': '100%', 'height': '49vw'}),
        # dcc.RangeSlider(
        #     id='range-slider',
        #     min=50, max=500, step=1,
        #     marks={0: '50', 500: '500'},
        #     value=[348, 368]
        # ),
        dcc.Interval(
            id='graph-update',
            interval=1000,
            n_intervals=0
        ),
    ]
)


@app.callback(
    Output('live-graph', 'figure'),
    [Input('graph-update', 'n_intervals')])
def update_graph_scatter(n):
    try:
        X = pickle.load(open("x_live.pkl", "rb"))
        Y = pickle.load(open("movement_live.pkl", "rb"))
        distance = pickle.load(open('distance_live.pkl', 'rb'))
    except Exception:
        X = pickle.load(open("x_live.pkl", "rb"))
        Y = pickle.load(open("movement_live.pkl", "rb"))
        distance = pickle.load(open('distance_live.pkl', 'rb'))
    fig = px.scatter(
        x=X,
        y=Y,
        color=distance,
        color_continuous_scale='rdbu',
        range_color=[340,360],
    )
    return fig


if __name__ == '__main__':
    app.run_server()
