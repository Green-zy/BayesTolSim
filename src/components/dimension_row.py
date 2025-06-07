# src/components/dimension_row.py

from dash import html, dcc
import dash_bootstrap_components as dbc
from src.utils.constants import DISTRIBUTION_OPTIONS

def generate_dimension_row(i):
    return html.Div([
        dbc.Row([
            dbc.Col(
                dcc.Input(
                    id={"type": "dim-name", "index": i},
                    placeholder="Name", type="text", className="form-control"
                ),
                width=2, style={"padding": "2px"}
            ),
            dbc.Col(
                dcc.Dropdown(
                    id={"type": "dim-dir", "index": i},
                    options=[{"label": "+", "value": "+"}, {"label": "-", "value": "-"}],
                    placeholder="Dir"
                ),
                width=1, style={"padding": "2px"}
            ),
            dbc.Col(
                dcc.Input(
                    id={"type": "dim-nominal", "index": i},
                    placeholder="Nominal", type="number",
                    className="form-control", style={"width": "90%"}
                ),
                width=2, style={"padding": "2px"}
            ),
            dbc.Col(
                dcc.Input(
                    id={"type": "dim-tol", "index": i},
                    placeholder="Tolerance", type="number",
                    className="form-control", style={"width": "90%"}
                ),
                width=2, style={"padding": "2px"}
            ),
            dbc.Col(
                dcc.Dropdown(
                    id={"type": "dim-dist", "index": i},
                    options=DISTRIBUTION_OPTIONS, placeholder="Distribution"
                ),
                width=2, style={"padding": "2px"}
            ),
            dbc.Col(
                html.Div(id={"type": "dim-params", "index": i}),
                width=2, style={"padding": "2px"}
            ),
            dbc.Col(
                html.Div([
                    dcc.Upload(
                        id={"type": "dim-mle", "index": i},
                        children=html.Div("MLE Data"),
                        style={"border": "1px dashed gray", "padding": "2px", "textAlign": "center"},
                        multiple=False
                    )
                ]),
                width=1, style={"padding": "2px"}
            ),
            dbc.Col(
                html.Div([
                    dcc.Upload(
                        id={"type": "dim-bayes", "index": i},
                        children=html.Div("Bayes Data"),
                        style={"border": "1px dashed gray", "padding": "2px", "textAlign": "center"},
                        multiple=False
                    )
                ]),
                width=1, style={"padding": "2px"}
            )
        ], className="mb-1")
    ])




