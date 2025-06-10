# src/layout.py

import dash_bootstrap_components as dbc
from dash import html, dcc

layout = dbc.Container([
    dcc.Store(id="dim-count", data=0),
    html.Div(id="dummy-output", style={"display": "none"}),  # Add dummy output

    # Card 1: Header
    dbc.Card([
        dbc.CardBody([
            html.H2("Bayesian Monte Carlo Tolerance Analysis", className="card-title")
        ])
    ], className="mb-4", style={"marginTop": "10px"}),

    # Card 2: Dimension Setup
    dbc.Card([
        dbc.CardBody([
            html.H4("Dimension Chain Setup"),
            html.P("Enter expressions and press Enter to calculate results", style={"color": "gray", "fontSize": "0.9rem"}),
            dbc.ButtonGroup([
                dbc.Button("+ Add Dimension", id="add-dim", color="success", className="me-2"),
                dbc.Button("- Remove Dimension", id="remove-dim", color="danger")
            ]),
            html.Br(), html.Br(),
            html.Div(id="dimension-form-container")
        ])
    ], className="mb-4"),

    # Card 3: Chain Viewer
    dbc.Card([
        dbc.CardBody([
            html.H4("Current Dimension Chain"),
            html.Div(id="chain-summary-table"),
            dcc.Graph(id="chain-plot")
        ])
    ], className="mb-4"),

    # Card 4: Dimension Distribution Viewer - Reduced width
    dbc.Card([
        dbc.CardBody([
            html.H4("Distribution of Dimension"),
            dcc.Dropdown(
                id="select-dim-to-view", 
                placeholder="Select a Dimension", 
                style={"width": "350px", "marginBottom": "15px"}
            ),
            dcc.Graph(id="dimension-distribution-plot"),
            html.Pre(
                id="dimension-statistics", 
                style={"whiteSpace": "pre-wrap", "fontSize": "0.9rem"}
            )
        ])
    ], className="mb-4", style={"maxWidth": "700px"})  # Constrained width, left aligned
], fluid=True)