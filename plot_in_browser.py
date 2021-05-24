import dash
import dash_core_components as dcc
import dash_daq as daq
from dash.dependencies import Output, Input, State
import dash_html_components as html
from math import floor
import pickle
import plotly.express as px


X = pickle.load(open("x_live.pkl", "rb"))
movement = pickle.load(open("movement_live.pkl", "rb"))
distance = pickle.load(open('distance_live.pkl', 'rb'))

app = dash.Dash(__name__)

# Website title
app.title = 'LiDAR - wykres na żywo'

app.layout = \
    html.Div(
        [
            html.P("LiDAR - wykres na żywo",
                   style={"text-align": "center",
                          "font-size": "30px",
                          "font-family": "Arial",
                          "margin-top": "2vw"}),


            html.P(id='average-distance-attention',
                   style={"color": "orange"}),


            dcc.Graph(id='plot',
                      style={"text-align": "center",
                             "display": "inline-block"}),


            html.Div(children=[
                html.P("Aktualizacja wykresu:",
                       style={"text-align": "center"}),
                html.P("WŁĄCZONA",
                       id='plot-update-status',
                       style={"color": "green",
                              "text-align": "center",
                              "font-size": "30px"}),
                html.Div(children=[html.Button("Przełącz aktualizację wykresu",
                                               id='start-stop-plot-updates-button')],
                         style={"text-align": "center"}),


                html.P("Prawidłowa wartość dystansu i tolerancja:"),
                html.Div(children=[
                    dcc.Input(id="correct-distance-value",
                              type="number",
                              placeholder="Wartość prawidłowa",
                              style={"width": "10vw"}),
                    dcc.Input(id='tolerance-value',
                              type='number',
                              placeholder="Tolerancja",
                              style={"width": "3.9vw"})],
                    style={'text-align': 'center'}),


                html.P("Schemat koloru punktów wykresu"),
                dcc.Dropdown
                (
                    id='color-theme',
                    value='rdbu',
                    options=[{"value": x, "label": x}
                             for x in px.colors.named_colorscales()]
                ),


                html.Br(),


                daq.ColorPicker
                (
                    label='Kolor tła wykresu:',
                    id='background-plot-color-picker',
                    value=dict(hex='#DFE2E2')
                ),


                html.P("Zakres koloru punktów dla wykresu:"),
                dcc.RangeSlider
                (
                    id='color-range-slider',
                    min=0,
                    max=500,
                    step=0.5,
                    marks={0: '0',
                           50: '50',
                           100: '100',
                           150: '150',
                           200: '200',
                           250: '250',
                           300: '300',
                           350: '350',
                           400: '400',
                           450: '450',
                           500: '500'},
                    value=[250, 350],
                    allowCross=False
                ),
                html.Div(id='color-range-slider-output-text',
                         style={'text-align': 'center'}),


                html.Br(),


                html.P("Szerokość osi X:"),
                dcc.RangeSlider
                (
                    id='x-axis-range-slider',
                    min=-300,
                    max=300,
                    step=0.5,
                    marks={-300: '-300',
                           -250: '-250',
                           -200: '-200',
                           -150: "-150",
                           -100: "-100",
                           -50: "-50",
                           0: '0',
                           50: '50',
                           100: '100',
                           150: '150',
                           200: '200',
                           250: '250',
                           300: '300'},
                    value=[-60, 60],
                    allowCross=False
                ),


                html.P("Rozmiar punktów wykresu:"),
                dcc.Slider
                (
                    id='point-size-slider',
                    min=1,
                    max=40,
                    step=1,
                    marks={1: '1',
                           5: '5',
                           10: '10',
                           15: '15',
                           20: '20',
                           25: '25',
                           30: '30',
                           35: '35',
                           40: '40'},
                    value=10,
                ),


                html.P("Kształt punktów wykresu:"),
                dcc.RadioItems
                (
                    id='point-shape-radio',
                    options=
                    [
                        {'label': 'Koło', 'value': 'circle'},
                        {'label': 'Okrąg', 'value': 'circle-open'},
                        {'label': 'Kwadrat', 'value': 'square'},
                        {'label': 'Pusty kwadrat', 'value': 'square-open'},
                    ],
                    value='circle'
                ),


                html.P("Wysokość wykresu:"),
                dcc.Slider
                (
                    id='plot-height-slider',
                    min=1,
                    max=100,
                    step=0.5,
                    marks={1: '1',
                           10: '10',
                           20: '20',
                           30: '30',
                           40: "40",
                           50: "50",
                           60: "60",
                           70: "70",
                           80: "80",
                           90: "90",
                           100: "100"},
                    value=45,
                ),


                html.P("Szerokość wykresu:"),
                dcc.Slider
                (
                    id='plot-width-slider',
                    min=1,
                    max=100,
                    step=0.5,
                    marks={1: '1',
                           10: '10',
                           20: '20',
                           30: '30',
                           40: "40",
                           50: "50",
                           60: "60",
                           70: "70",
                           80: "80",
                           90: "90",
                           100: "100"},
                    value=65,
                ), ], style={"float": "right",
                             "width": "25vw",
                             "height": "20vw",
                             "margin-right": "120px"}),


            dcc.Interval
            (
                id='update-interval',
                interval=1000,
                n_intervals=0,
                disabled=False
            ),


            html.Br(), html.Br(), html.Br(), html.Br(), html.Br(),


            html.P(id="average-distance"),
            html.Div(id='left-bottom'),
            html.Div(id='right-bottom'),
            html.Div(id='left-upper'),
            html.Div(id='right-upper'),
        ], style={"font-family": "Bahnschrift"}
    )




@app.callback(
    Output('plot-update-status', 'children'),
    Output('plot-update-status', 'style'),

    Input('start-stop-plot-updates-button', 'n_clicks')
)
def change_plot_updates_status_text(number_of_clicks):
    if type(number_of_clicks) == int:
        if number_of_clicks % 2 == 0:
            return "WŁĄCZONA",\
                   {"color": "green",
                    "text-align": "center",
                    "font-size": "30px"}
        else:
            return "WYŁĄCZONA",\
                   {"color": "red",
                    "text-align": "center",
                    "font-size": "30px"}




@app.callback(
    Output('update-interval', 'disabled'),

    Input('start-stop-plot-updates-button', 'n_clicks'),

    State('update-interval', 'disabled'),
)
def enable_disable_plot_updates(number_of_clicks, disabled_state):
    if number_of_clicks is not None and number_of_clicks > 0:
        return not disabled_state
    else:
        return disabled_state




@app.callback(
    Output('average-distance-attention', 'children'),

    Input('correct-distance-value', 'value')
)
def average_distance_alert(correct_distance_value):
    if type(correct_distance_value) == int:
        if correct_distance_value > 0:
            if round(sum(distance) / len(distance)) > correct_distance_value:
                return "UWAGA: Średnia z dystansu (" + str(
                    round(sum(distance) / len(distance))) + ") jest wyższa niż podana " \
                                                            "prawidłowa wartość dystansu!"
            elif round(sum(distance) / len(distance)) < correct_distance_value:
                return "UWAGA: Średnia z dystansu (" + str(
                    round(sum(distance) / len(distance))) + ") jest niższa niż podana " \
                                                            "prawidłowa wartość dystansu!"
            else:
                return ""
        else:
            return ""




@app.callback(
    Output('plot', 'figure'),
    Output('plot', 'style'),
    Output('average-distance', 'children'),
    Output('left-bottom', 'children'),
    Output('right-bottom', 'children'),
    Output('left-upper', 'children'),
    Output('right-upper', 'children'),

    Input('update-interval', 'n_intervals'),
    Input('color-range-slider', 'value'),
    Input("color-theme", "value"),
    Input('point-size-slider', 'value'),
    Input('point-shape-radio', 'value'),
    Input("background-plot-color-picker", "value"),
    Input("plot-height-slider", "value"),
    Input('plot-width-slider', "value"),
    Input('x-axis-range-slider', 'value'),
    Input('correct-distance-value', 'value'),
    Input('tolerance-value', 'value'))
def update_graph_scatter(n, color_range, color_theme, point_size, point_shape, bg_plot_color, height_slider,
                         width_slider, x_axis_range_slider, correct_distance_value, tolerance):
    try:
        X = pickle.load(open("x_live.pkl", "rb"))
        movement = pickle.load(open("movement_live.pkl", "rb"))
        distance = pickle.load(open('distance_live.pkl', 'rb'))
    except Exception:
        X = pickle.load(open("x_live.pkl", "rb"))
        movement = pickle.load(open("movement_live.pkl", "rb"))
        distance = pickle.load(open('distance_live.pkl', 'rb'))

    fig = px.scatter(
        x=X,
        y=movement,
        color=distance,
        color_continuous_scale=color_theme,
        range_color=[color_range[0], color_range[1]],
        labels=dict(x="X", y="Rząd", color="Dystans")
    )

    fig.update_traces(marker=dict(size=point_size, symbol=point_shape),
                      selector=dict(mode='markers'),
                      )

    if type(correct_distance_value) == int and type(tolerance) == int:

        if correct_distance_value > 0:

            if floor(distance[movement.index(1) - 1]) == correct_distance_value \
                    or (correct_distance_value - tolerance <= floor(distance[movement.index(1) - 1]) <= correct_distance_value) \
                    or (correct_distance_value + tolerance >= floor(distance[movement.index(1) - 1]) >= correct_distance_value):
                fig.add_annotation(x=X[movement.index(1) - 1],
                                   y=movement[movement.index(1) - 1],
                                   text=round(distance[movement.index(1) - 1], 2),
                                   showarrow=True,
                                   arrowhead=3,
                                   font=dict
                                       (
                                           family="Arial",
                                           size=18,
                                           color="black"
                                       ),
                                   )
            else:
                fig.add_annotation(x=X[movement.index(1) - 1],
                                   y=movement[movement.index(1) - 1],
                                   text=round(distance[movement.index(1) - 1], 2),
                                   showarrow=True,
                                   arrowhead=3,
                                   font=dict
                                       (
                                           family="Arial",
                                           size=18,
                                           color="red"
                                       ),
                                   )

            if floor(distance[0]) == correct_distance_value \
                    or (correct_distance_value - tolerance <= floor(distance[0]) <= correct_distance_value) \
                    or (correct_distance_value + tolerance >= floor(distance[0]) >= correct_distance_value):
                fig.add_annotation(x=X[0],
                                   y=movement[0],
                                   text=round(distance[0], 2),
                                   arrowhead=3,
                                   showarrow=True,
                                   font=dict
                                       (
                                           family="Arial",
                                           size=18,
                                           color="black"
                                       ),
                                   )
            else:
                fig.add_annotation(x=X[0],
                                   y=movement[0],
                                   text=round(distance[0], 2),
                                   arrowhead=3,
                                   showarrow=True,
                                   font=dict
                                       (
                                           family="Arial",
                                           size=18,
                                           color="red"
                                       ),
                                   )

            if floor(distance[movement.index(movement[-1])]) == correct_distance_value \
                    or (correct_distance_value - tolerance <= floor(distance[movement.index(movement[-1])]) <= correct_distance_value) \
                    or (correct_distance_value + tolerance >= floor(distance[movement.index(movement[-1])]) >= correct_distance_value):
                fig.add_annotation(x=X[movement.index(movement[-1])],
                                   y=movement[-1],
                                   text=round(distance[movement.index(movement[-1])], 2),
                                   showarrow=True,
                                   arrowhead=3,
                                   font=dict
                                       (
                                           family="Arial",
                                           size=18,
                                           color="black"
                                       ),
                                   )
            else:
                fig.add_annotation(x=X[movement.index(movement[-1])],
                                   y=movement[-1],
                                   text=round(distance[movement.index(movement[-1])], 2),
                                   showarrow=True,
                                   arrowhead=3,
                                   font=dict
                                       (
                                           family="Arial",
                                           size=18,
                                           color="red"
                                       ),
                                   )

            if floor(distance[-1]) == correct_distance_value \
                    or (correct_distance_value - tolerance <= floor(distance[-1]) <= correct_distance_value) \
                    or (correct_distance_value + tolerance >= floor(distance[-1]) >= correct_distance_value):
                fig.add_annotation(x=X[-1],
                                   y=movement[-1],
                                   text=round(distance[-1], 2),
                                   showarrow=True,
                                   arrowhead=3,
                                   font=dict
                                       (
                                           family="Arial",
                                           size=18,
                                           color="black"
                                       ),
                                   )
            else:
                fig.add_annotation(x=X[-1],
                                   y=movement[-1],
                                   text=round(distance[-1], 2),
                                   showarrow=True,
                                   arrowhead=3,
                                   font=dict
                                       (
                                           family="Arial",
                                           size=18,
                                           color="red"
                                       ),
                                   )

    fig.update_layout(plot_bgcolor=bg_plot_color['hex'],
                      xaxis_title="Oś X",
                      yaxis_title="Rząd",
                      legend_title="Legenda")

    fig.update_xaxes(range=[x_axis_range_slider[0], x_axis_range_slider[1]])

    return fig, \
           {'height': str(height_slider) + "vw",
            'width': str(width_slider) + "%",
            "display": "inline-block"}, \
           "Średnia z dystansu: " + str(round(sum(distance) / len(distance))), \
           "Wartość w prawym dolnym rogu wykresu: " + str(distance[0]), \
           "Wartość w lewym dolnym rogu wykresu: " + str(distance[movement.index(1) - 1]), \
           "Wartość w prawym górnym rogu wykresu: " + str(distance[movement.index(movement[-1])]), \
           "Wartość w lewym górnym rogu wykresu: " + str(distance[-1])




@app.callback(Output('color-range-slider-output-text', 'children'),
              Input('color-range-slider', 'value'))
def display_color_range_slider_value(color_range_slider_value):
    slider_min_val = float(color_range_slider_value[0])
    slider_max_val = float(color_range_slider_value[1])
    slider_avg_val = (slider_min_val + slider_max_val) / 2

    return 'Wartość najniższa, środkowa, najwyższa: {} | {} | {}'.format(slider_min_val, slider_avg_val, slider_max_val)


if __name__ == '__main__':
    print("[~] Starting server")
    app.run_server()
