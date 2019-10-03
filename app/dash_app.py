# dash_app
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from bus_arrival_processing import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Input(id='my-id', value='6 digits:', type='text'),
    html.Hr(),
    html.Div(id='my-div0'),
    html.Hr(),
    html.Div(id='my-div1'),
    html.Hr(),
    html.Div(id='my-div2'),
    html.Hr(),
    html.Div(id='my-div3')
])

@app.callback(
    [Output(component_id='my-div0', component_property='children'),
     Output(component_id='my-div1', component_property='children'),
     Output(component_id='my-div2', component_property='children'),
     Output(component_id='my-div3', component_property='children')
    ],
    [Input(component_id='my-id', component_property='value')]
)
def stop_name(input_value):
    res1 = 'The stop you searched is: ' + get_stop_name(str(input_value))
    res2 = get_arrival_information_for_stop(str(input_value))
    res3 = 'Nearby Stop(s): ' + ' '.join(find_nearby_stops(str(input_value)))
    res4 = combine_nearby_stop_information(str(input_value))
    return res1, res2, res3, res4


if __name__ == '__main__':
    app.run_server(debug=True, host= '0.0.0.0')
