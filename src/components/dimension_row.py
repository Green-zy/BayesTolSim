# src/components/dimension_row.py

from dash import html, dcc
import dash_bootstrap_components as dbc
from src.utils.constants import DISTRIBUTION_OPTIONS

def generate_dimension_row(i):
    return html.Div([
        # Hidden stores for MLE and Bayesian status
        dcc.Store(id={"type": "dim-mle-status", "index": i}, data=False),
        dcc.Store(id={"type": "dim-bayes-status", "index": i}, data=False),
        dcc.Store(id={"type": "dim-bayes-error", "index": i}, data=""),
        
        html.Div([
            html.Div(dcc.Input(
                id={"type": "dim-name", "index": i},
                placeholder="Name", type="text", className="form-control"
            ), style={"width": "160px", "padding": "5px"}),

            html.Div(dcc.Dropdown(
                id={"type": "dim-dir", "index": i},
                options=[{"label": "+", "value": "+"}, {"label": "-", "value": "-"}],
                placeholder="Dir"
            ), style={"width": "80px", "padding": "5px"}),

            html.Div(dcc.Input(
                id={"type": "dim-nominal", "index": i},
                placeholder="Nominal (mm)", type="number", className="form-control"
            ), style={"width": "160px", "padding": "5px"}),

            html.Div([
                dcc.Input(
                    id={"type": "dim-tol-upper", "index": i},
                    placeholder="Upper Tolerance", type="number", className="form-control",
                    style={"width": "165px", "marginRight": "10px"}
                ),
                dcc.Input(
                    id={"type": "dim-tol-lower", "index": i},
                    placeholder="Lower Tolerance", type="number", className="form-control",
                    style={"width": "165px"}
                )
            ], style={"display": "flex", "alignItems": "center", "padding": "5px", "width": "350px"}),

            html.Div(dcc.Dropdown(
                id={"type": "dim-dist", "index": i},
                options=DISTRIBUTION_OPTIONS, placeholder="Distribution"
            ), style={"width": "150px", "padding": "5px"}),

            html.Div([
                dcc.Input(
                    id={"type": "dim-para1", "index": i},
                    placeholder="Para1", type="text", className="form-control",
                    style={"width": "100px", "marginRight": "5px"},
                    debounce=False,  # needed for n_submit to work well
                ),
                dcc.Input(
                    id={"type": "dim-para2", "index": i},
                    placeholder="Para2", type="text", className="form-control",
                    style={"width": "100px"},
                    debounce=False,
                )
            ], style={"display": "flex", "alignItems": "center", "gap": "5px", "padding": "5px", "width": "220px"}),

            html.Div([
                dcc.Upload(
                    id={"type": "dim-mle", "index": i},
                    children=html.Div(
                        id={"type": "dim-mle-display", "index": i},
                        children="MLE Data"
                    ),
                    style={
                        "border": "1px dashed gray", 
                        "padding": "5px", 
                        "textAlign": "center",
                        "transition": "all 0.3s ease"
                    }
                )
            ], style={"width": "120px", "padding": "5px"}),

            html.Div([
                dcc.Upload(
                    id={"type": "dim-bayes", "index": i},
                    children=html.Div(
                        id={"type": "dim-bayes-display", "index": i},
                        children="Bayes Data"
                    ),
                    style={
                        "border": "1px dashed gray", 
                        "padding": "5px", 
                        "textAlign": "center",
                        "transition": "all 0.3s ease"
                    }
                )
            ], style={"width": "120px", "padding": "5px"}),

        ],
        style={"display": "flex", "flexWrap": "nowrap", "alignItems": "center"})
    ])