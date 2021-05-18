import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import pickle
import plotly.graph_objs as go
from collections import deque

X = pickle.load(open("x_live.pkl", "rb"))

Y = pickle.load(open("movement_live.pkl", "rb"))

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Graph(id = 'live-graph'),
        dcc.Interval(
            id = 'graph-update',
            interval = 1000,
            n_intervals = 0
        ),
    ]
)

@app.callback(
    Output('live-graph', 'figure'),
    [ Input('graph-update', 'n_intervals') ]
)

def update_graph_scatter(n):
    X = pickle.load(open("x_live.pkl", "rb"))
    Y = pickle.load(open("movement_live.pkl", "rb"))

    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'markers'
    )

    return {'data': [data],
            'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),yaxis = dict(range = [min(Y),max(Y)]),)}

if __name__ == '__main__':
    app.run_server()
