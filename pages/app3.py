import dash
from dash import html, dcc, no_update, ctx
import dash_bootstrap_components as dbc
from .side_bar import sidebar
import geopandas as gpd
import pandas as pd

# import df
pc_sales_df = gpd.read_file('assets/pc_sales_df.geojson')

# join ship from locations
delivery_loc = pd.read_csv('pc_shipfrom_loc.csv')
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
