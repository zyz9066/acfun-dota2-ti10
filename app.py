import dash
import plotly.graph_objs as go
import dash_core_components as dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd

app = dash.Dash(__name__)
server = app.server

df = pd.read_csv("https://raw.githubusercontent.com/zyz9066/acfun-dota2-ti10/master/assets/acfun_dota2_ti10.csv")
df = df.sort_values('match_id')

app.layout = html.Div([
    html.Div([

        html.Div([
            html.Label(['Date:'], style={'font-weight': 'bold'}),
            dcc.Dropdown(
                id='date',
                options=[{'label': i, 'value': i} for i in sorted(set(df['date'].tolist() + ['all']))],
                value='all'
            ),
            html.Label(['Radiant:'], style={'font-weight': 'bold'}),
            dcc.Dropdown(
                id='radiant',
                options=[{'label': i, 'value': i} for i in sorted(set(df['Team'].tolist() + ['all']))],
                value='all'
            )], style={'width': '48%', 'display': 'inline-block'}),
        html.Div([
            html.Label(['Time:'], style={'font-weight': 'bold'}),
            dcc.Dropdown(
                id='time',
                options=[{'label': i, 'value': i} for i in sorted(set(df['time'].tolist() + ['all']))],
                value='all'
            ),
            html.Label(['Dire:'], style={'font-weight': 'bold'}),
            dcc.Dropdown(
                id='dire',
                options=[{'label': i, 'value': i} for i in sorted(set(df['Team.1'].tolist() + ['all']))],
                value='all'
            )], style={'width': '48%', 'display': 'inline-block'}),
    dcc.RadioItems(
                id='display-type',
                options=[{'label': i, 'value': i} for i in ['gold', 'exp']],
                value='gold'
            ),
    dcc.Graph(id='acfun-graphic')
    ])
])

@app.callback(
    Output('acfun-graphic', 'figure'),
    Output('radiant', 'options'),
    Output('dire', 'options'),
    Output('time', 'options'),
    Input('date', 'value'),
    Input('radiant', 'value'),
    Input('dire', 'value'),
    Input('time', 'value'),
    Input('display-type', 'value'))
def update_graph(date, radiant, dire, time, display_type):
    dff = df
    if date != 'all':
        dff = dff[dff['date'] == date].reset_index()
    if radiant != 'all':
        dff = dff[dff['Team'] == radiant].reset_index()
    if dire != 'all':
        dff = dff[dff['Team.1'] == dire].reset_index()
    if time != 'all':
        dff = dff[dff['time'] == time].reset_index()

    fig = go.Figure()
    for i in range(len(dff.index)):
        if display_type == 'gold':
            fig.add_trace(go.Scatter(y=[int(s) for s in dff['radiant_gold_adv'][i].split(',')], name='{} vs {} {}'.format(dff['Team'][i], dff['Team.1'][i], dff['time'][i]), mode='lines'))
        elif display_type == 'exp':
            fig.add_trace(go.Scatter(y=[int(s) for s in dff['radiant_exp_adv'][i].split(',')], name='{} vs {} {}'.format(dff['Team'][i], dff['Team.1'][i], dff['time'][i]), mode='lines'))
    fig.update_layout(title='AcFun Dota2 TI10 Statistics',
                   xaxis_title='Duration',
                   yaxis_title='radiant_gold_adv' if display_type == 'gold' else 'radiant_exp_adv')
    return fig, [{'label': i, 'value': i} for i in sorted(set(dff['Team'].tolist() + ['all']))], [{'label': i, 'value': i} for i in sorted(set(dff['Team.1'].tolist() + ['all']))], [{'label': i, 'value': i} for i in sorted(set(dff['time'].tolist() + ['all']))]


if __name__ == '__main__':
    app.run_server()
