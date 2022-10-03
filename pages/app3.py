import dash
from dash import html, dcc, no_update, ctx
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH, ALL
from .side_bar import sidebar
import geopandas as gpd
import pandas as pd
import numpy as np
import plotly.io as pio
import json
from datetime import datetime
import numpy as np
import base64
import io
import ast
import sys
import plotly.express as px
import plotly.graph_objects as go


# import df
pc_sales_df = gpd.read_file('assets/pc_sales_df.geojson')

# join ship from locations
delivery_loc = pd.read_csv('assets/pc_shipfrom_loc.csv')
delivery_loc['Row Labels'] = delivery_loc['Row Labels'].astype('str')
delivery_loc['Row Labels'] = delivery_loc['Row Labels'].apply(lambda x: '0' + x if x.startswith('8') else x)
delivery_loc.replace(0, False, inplace = True)
delivery_loc.replace(1, True, inplace = True)
pc_sales_df = pc_sales_df.merge(delivery_loc, left_on = 'poa_code21', right_on = 'Row Labels', how = 'left')


# ready geometries
pc_sales_df['geometry'] = pc_sales_df.to_crs(pc_sales_df.estimate_utm_crs()).simplify(2000).to_crs(pc_sales_df.crs) # simplify boundaries to 1km
pc_sales_df = pc_sales_df.to_crs( epsg = 4326) # change to lat/long
pc_sales_df.set_index('poa_code21', inplace = True)

df = pc_sales_df
df['terr_colour'] = np.NaN

# state_df = pc_sales_df[pc_sales_df.codestte == state]
state_coords = {'NT' : [-19.491411, 132.550964],
                'NSW' : [-33.872762037132375, 147.22963557432993],
                'VIC' : [-37.020100, 144.964600],
                'QLD' : [-20.917574, 142.702789],
                'SA' : [-30.000233, 136.209152],
                'WA' : [-25.953512, 117.857048],
                'TAS' : [-41.640079, 146.315918]
                }

# initialise variables
df_state = df[df.codestte == 'NSW']

postcode_colour_d = dict()

fig = px.choropleth_mapbox(df_state,
                           geojson = df_state.geometry,
                           locations = df_state.index,
                           opacity = 0.2,
                           center = {'lat' : -33.872762037132375, 'lon' : 147.22963557432993},
                           zoom = 4.5,
                           height = 1200,
                           width = 1600,
                           mapbox_style="carto-positron",
                           # uirevision = 'Retain user zoom preferences'
)


dash.register_page(__name__)

def layout():
    return html.Div([
        dbc.Row(
            [
                dbc.Col(
                    [
                        sidebar()
                    ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),

                dbc.Col(
                    [
                        html.H3('App 3 - build your own app here and let me know if you have questions', style={'textAlign':'center'}),
                    ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10)
            ]
        )
    ])
