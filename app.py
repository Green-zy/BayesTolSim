# app.py

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

from src.layout import layout
from src.callbacks.dimension_rows import register_dim_row_callbacks
from src.callbacks.param_display import register_param_display_callback
from src.callbacks.parse_parameters import register_param_parse_callback
from src.callbacks.param_placeholder import register_param_placeholder_callback
from src.callbacks.tolerance_to_params import register_tolerance_to_params_callback
from src.callbacks.mle_estimation import register_mle_callback
from src.callbacks.mle_visual_feedback import register_mle_visual_feedback_callback
from src.callbacks.bayesian_estimation import register_bayesian_callback  # New import
from src.callbacks.bayesian_visual_feedback import register_bayesian_visual_feedback_callback  # New import
from src.callbacks.chain_summary import register_chain_summary_callback
from src.callbacks.view_dim_distribution import register_view_dim_distribution_callback
from src.callbacks.final_dimension_simulation import register_final_dimension_simulation_callback  # New import


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "BayesTolSim"
app.layout = layout


register_dim_row_callbacks(app)
register_param_display_callback(app)
register_param_parse_callback(app)
register_param_placeholder_callback(app)
register_tolerance_to_params_callback(app)
register_mle_callback(app)
register_mle_visual_feedback_callback(app)
register_bayesian_callback(app)  # Register Bayesian callback
register_bayesian_visual_feedback_callback(app)  # Register Bayesian visual feedback
register_chain_summary_callback(app)
register_view_dim_distribution_callback(app)
register_final_dimension_simulation_callback(app)  # Register final dimension simulation

if __name__ == '__main__':
    app.run(debug=True)