# src/layout.py

import dash_bootstrap_components as dbc
from dash import html, dcc

layout = dbc.Container([
    dcc.Store(id="dim-count", data=0),

    # Card 1: Header
    dbc.Card([
        dbc.CardBody([
            html.H2("Bayesian Monte Carlo Tolerance Analysis", className="card-title")
        ])
    ], className="mb-4"),

    # Card 2: Dimension Setup
    dbc.Card([
        dbc.CardBody([
            html.H4("Dimension Chain Setup"),
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
], className="mb-4")

    # Other cards can be added here as needed
], fluid=True)
