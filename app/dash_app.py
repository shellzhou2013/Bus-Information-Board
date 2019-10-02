# dash_app
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import bus_arrival_processing

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Input(id='my-id', value='6 digits:', type='text'),
    html.Div(id='my-div')
])


@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)


def update_output_div(input_value):
    return '"{}"'.format(combine_output(str(input_value)))


if __name__ == '__main__':
    app.run_server(debug=True, host= '0.0.0.0')
