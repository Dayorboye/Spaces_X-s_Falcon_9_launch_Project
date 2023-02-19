

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px


spaceX_dataF = pd.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
)
max_payload = spaceX_dataF['Payload Mass (kg)'].max()
min_payload = spaceX_dataF['Payload Mass (kg)'].min()
launchsites_options = spaceX_dataF["Launch Site"].unique()

options_sites = []
options_sites.append({'label': 'All Sites', 'value': 'All Sites'})
for i in launchsites_options:
 options_sites.append({'label': i, 'value': i}),

app = dash.Dash()

# app.layout = html.Div(html.Div([html.Div("a"),html.Div("b"),html.Div("c"),html.Div("d")],style={"display":"grid","grid-template-columns": "auto auto"}))
app.layout = html.Div(children=[html.Div(dcc.Dropdown(
                id="Launch_sites", placeholder='Select a Launch Site here', searchable = True ,
                options=options_sites,
                value='All Sites',),
                                                  style={"background-color": "#161A1D","text-align": "center",
                                                    "padding": "10px 0", "font-size": "12px","color":"black"},),
                                html.Div(dcc.RangeSlider(
                                    id='payload_slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    marks = {0: '0 kg',
                                            1000: '1000 kg',
                                            2000: '2000 kg',
                                            3000: '3000 kg',
                                            4000: '4000 kg',
                                            5000: '5000 kg',
                                            6000: '6000 kg',
                                            7000: '7000 kg',
                                            8000: '8000 kg',
                                            9000: '9000 kg',
                                            10000: '10000 kg'
                                    },

                                    value=[min_payload,max_payload]
                                ),
                                                   style={"background-color": "#161A1D","text-align": "center",
                                                    "padding": "20px 0", "font-size": "30px","color":"white"}),
                                html.Div(dcc.Graph(id='funnel-graph', 
                                                   style={"background-color": "#161A1D","text-align": "center",
                                                     "height":"70vh", "width":"100%"}),),
                                html.Div(dcc.Graph(id='success-payload-scatter-chart',
                                                   style={"background-color": "#161A1D","text-align": "center",
                                                     "height":"70vh", "width":"100%"}),),],
                                style={"display":"grid","grid-template-columns": "auto auto",
                                "grid-gap": "10px","background-color": "#0e1012","padding": "60px"})

@app.callback(
    dash.dependencies.Output('funnel-graph', 'figure'),
    [dash.dependencies.Input('Launch_sites', 'value')])

def update_graph(Launch_sites):
    if (Launch_sites == 'All Sites'):
        df  = spaceX_dataF[spaceX_dataF['class'] == 1 ]
        figure = px.pie(df, names = 'Launch Site',hole=.3,title = 'Total Success Launches By all sites')
    else:
        df  = spaceX_dataF.loc[spaceX_dataF['Launch Site'] == Launch_sites]
        figure = px.pie(df, names = 'class',hole=.3,title = 'Total Success Launches for site '+Launch_sites)
    return figure


@app.callback(
     dash.dependencies.Output('success-payload-scatter-chart','figure'),
     [dash.dependencies.Input('Launch_sites','value'), dash.dependencies.Input('payload_slider','value')])

def update_scattergraph(site_dropdown,payload_slider):
    if site_dropdown == 'All Sites':
        low, high = payload_slider
        df  = spaceX_dataF
        mask = (df['Payload Mass (kg)'] > low) & (df['Payload Mass (kg)'] < high)
        figure = px.scatter(
            df[mask], x="Payload Mass (kg)", y="class",
            color="Booster Version",
            size='Payload Mass (kg)',
            title = 'Payload Mass Against Class',
            hover_data=['Payload Mass (kg)'],
            )
    else:
        low, high = payload_slider
        df  = spaceX_dataF.loc[spaceX_dataF['Launch Site'] == site_dropdown]
        mask = (df['Payload Mass (kg)'] > low) & (df['Payload Mass (kg)'] < high)
        figure = px.scatter(
            df[mask], x="Payload Mass (kg)", y="class",
            color="Booster Version",
            size='Payload Mass (kg)',
            title = 'Payload Mass Against Class',
            hover_data=['Payload Mass (kg)'])
    return figure                                             


if __name__=='__main__':
    app.run_server(debug=True) 
    
       