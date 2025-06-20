# Import required libraries
# python3.11 -m pip install pandas dash
# wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
# python3.11 spacex-dash-app.py

import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children= [
                html.H1('SpaceX Launch Records Dashboard', 
                style={'textAlign': 'center', 'color': '#503D36','font-size': 40}),
                
                # TASK 1: Add a dropdown list to enable Launch Site selection
                # The default select value is for ALL sites
                # dcc.Dropdown(id='site-dropdown',...)    
                dcc.Dropdown(id='site-dropdown',
                    options=[{'label': 'All Sites', 'value': 'ALL'},] +[{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
                    placeholder='Select a Launch Site here',
                    value='ALL',
                    searchable=True
                ),
                html.Br(),

                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                # Function decorator to specify function input and output
                
                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                html.Div(dcc.Graph(id='success-pie-chart')),
                html.Br(),

                html.P("Payload range (Kg):"),
                # TASK 3: Add a slider to select payload range
                #dcc.RangeSlider(id='payload-slider',...)
                dcc.RangeSlider(id='payload-slider',
                    min=0,
                    max=int(max_payload),
                    step=1000,
                    marks={i: f'{i} kg' for i in range(int(min_payload), int(max_payload)+1, 1000)},
                    value=[int(min_payload), int(max_payload)]
                ),
                # dcc.RangeSlider(id='id',
                # min=0, max=10000, step=1000,
                # marks={0: '0',
                #     100: '100'},
                # value=[min_value, max_value])

                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
# def update_pie_chart(selected_site):
#     if selected_site == 'ALL':
#         fig = px.pie(spacex_df, names='Launch Site', values='Class',
#                      title='Total Success Launches by Site')
#     else:
#         filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
#         fig = px.pie(filtered_df, names='Outcome', title=f'Launch Outcome for {selected_site}')
#     return fig
def update_pie(launch_site):
    if(launch_site=='ALL'):
        fig=px.pie(spacex_df,values='class',names='Launch Site',title='Total Success launches By each Site')
    else:
        f_df=spacex_df[spacex_df['Launch Site']==launch_site]
        fig=px.pie(f_df,names='class',title=f"total succesful launches for {launch_site}",color_discrete_map={0:'red',1:'green'},color='class')
    return fig

# def generate_chart(names):
#     df = px.data.tips() # replace with your own data source
#     fig = px.pie(df, values=values, names=names, hole=.3)
#     return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output("success-payload-scatter-chart", "figure"),
    [Input("site-dropdown", "value"),
    Input("payload-slider", "value")]
)
def update_scatter(selected_site, payload_range):
    low, high = payload_range
    df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
    entered_site = "All"

    if selected_site != 'ALL':
        df = df[df['Launch Site'] == selected_site]
        entered_site = selected_site
    
    fig=px.scatter(
        df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title=f"Correlation between Payload and Success for {entered_site}"

    )
    # fig = px.scatter(
    #     df, x='Payload Mass (kg)', y='Class',
    #     color='Booster Version',
    #     hover_data=['Launch Site'],
    #     title='Correlation between Payload Mass and Launch Outcome',
    #     labels={'Class': 'Launch Outcome', 'Payload Mass (kg)': 'Payload Mass (kg)'},
    #     category_orders={"Class": [0, 1]},
    #     range_y=[-0.5, 1.5]
    # )
    return fig
# Run the app
if __name__ == '__main__':
    app.run(port=8088)
