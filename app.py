# app.py

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

from src.layout import layout
from src.callbacks.dimension_rows import register_dim_row_callbacks
from src.callbacks.param_display import register_param_display_callback
from src.callbacks.chain_summary import register_chain_summary_callback
from src.callbacks.view_dim_distribution import register_view_dim_distribution_callback


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "BayesTolSim"
app.layout = layout


register_dim_row_callbacks(app)
register_param_display_callback(app)
register_chain_summary_callback(app)
register_view_dim_distribution_callback(app)

if __name__ == '__main__':
    app.run(debug=True)
