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
    Output(component_id='my-div0', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)
def stop_name(input_value):
    return 'The stop you searched is: ' + get_stop_name(str(input_value))


@app.callback(
    Output(component_id='my-div1', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)
def arrival_information(input_value):
    return get_arrival_information_for_stop(str(input_value))

@app.callback(
    Output(component_id='my-div2', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)
def nearby_stops(input_value):
    temp = find_nearby_stops(str(input_value))
    # add stop name to the stop id
    for i in range(len(temp)):
        temp[i] += ' ' + get_stop_name(temp[i])
    
    
    info = ''
    if len(temp) == 0:
        info = 'No nearby stops!'
    elif len(temp) == 1:
        info = 'The nearby stop is: ' + temp[0]
    else:
        info = 'The nearby stops are: ' + '+++'.join(temp)
    return info

@app.callback(
    Output(component_id='my-div3', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)
def nearby_information(input_value):
    return combine_nearby_stop_information(str(input_value))
    
if __name__ == '__main__':
    app.run_server(debug=True, host= '0.0.0.0')
