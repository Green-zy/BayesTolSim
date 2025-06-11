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
            html.Div([
                html.Div([
                    html.Label("Tolerance for final dimension:", style={"fontWeight": "bold", "marginRight": "15px", "alignSelf": "center"}),
                    dcc.Input(
                        id="final-dim-tol-upper",
                        placeholder="Upper Tolerance", 
                        type="number", 
                        className="form-control",
                        style={"width": "165px", "marginRight": "10px"}
                    ),
                    dcc.Input(
                        id="final-dim-tol-lower",
                        placeholder="Lower Tolerance", 
                        type="number", 
                        className="form-control",
                        style={"width": "165px"}
                    )
                ], style={"display": "flex", "alignItems": "center", "marginBottom": "15px"})
            ]),
            html.Div(id="chain-summary-table"),
            dcc.Graph(id="chain-plot")
        ])
    ], className="mb-4"),

    # Cards 4 & 5: Dimension Distribution Viewer and Final Dimension Distribution - Same row
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("View Distribution of a Dimension"),
                    dcc.Dropdown(
                        id="select-dim-to-view", 
                        placeholder="Select a Dimension", 
                        style={"width": "220px", "marginBottom": "15px"}
                    ),
                    dcc.Graph(
                        id="dimension-distribution-plot",
                        style={"height": "400px"}  # Set explicit height
                    ),
                    html.Pre(
                        id="dimension-statistics", 
                        style={"whiteSpace": "pre-wrap", "fontSize": "0.9rem"}
                    )
                ])
            ], style={"height": "100%"})  # Ensure full height
        ], width=6, style={"paddingRight": "15px"}),  # Card 4 - 6/12 width with more right padding
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Final Dimension Distribution"),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Label("Number of Samples:", style={"marginRight": "10px", "fontWeight": "bold", "alignSelf": "center"}),
                                dcc.Input(
                                    id="num-samples-input",
                                    type="number",
                                    placeholder="Enter samples",
                                    min=1,
                                    step=1,
                                    value=1000,
                                    style={"width": "140px", "marginRight": "10px"}  # Reduced width by ~30%
                                ),
                                dbc.Button(
                                    "Run Simulation", 
                                    id="run-simulation-btn",
                                    color="primary",
                                    style={
                                        "height": "33px",
                                        "display": "flex",
                                        "alignItems": "center",
                                        "justifyContent": "center"
                                    }  # Center text vertically and horizontally
                                )
                            ], style={"display": "flex", "alignItems": "center", "marginBottom": "15px"})
                        ])
                    ]),
                    html.Div(id="final-dimension-content", children=[
                        # Default state - similar to other cards
                        html.Div(
                            "Please set dimension chain first.",
                            style={
                                "textAlign": "center",
                                "color": "gray",
                                "fontSize": "14px",
                                "padding": "100px 20px",
                                "height": "300px",
                                "display": "flex",
                                "alignItems": "center",
                                "justifyContent": "center"
                            }
                        )
                    ])
                ])
            ], style={"height": "100%"})  # Ensure full height
        ], width=6, style={"paddingLeft": "15px"})  # Card 5 - 6/12 width with more left padding
    ], className="mb-4", style={"minHeight": "600px"}),  # Set minimum height for the row
    
    # Author information - Below Card 4 & 5
    html.Div([
        html.P([
            html.Strong("BayesTolSim: "),
            "A Bayesian Monte Carlo tolerance analysis tool for engineering design. ",
            html.Br(),
            html.Strong("Author: "),
            "Yun Zhou | ",
            html.Strong("Email: "),
            html.A("robbiezhou1@gmail.com", href="mailto:robbiezhou1@gmail.com", style={"color": "#007bff", "textDecoration": "none"}),
            " | ",
            html.Strong("Github: "),
            html.A("https://github.com/Green-zy", href="https://github.com/Green-zy", target="_blank", style={"color": "#007bff", "textDecoration": "none"}),
            " | ",
            html.Strong("LinkedIn: "),
            html.A("www.linkedin.com/in/yun-zhou-robbie-172966187", href="https://www.linkedin.com/in/yun-zhou-robbie-172966187", target="_blank", style={"color": "#007bff", "textDecoration": "none"})
        ], style={
            "fontSize": "0.85rem",
            "color": "#6c757d",
            "textAlign": "center",
            "marginTop": "10px",
            "marginBottom": "20px",
            "lineHeight": "1.4"
        })
    ])
], fluid=True)