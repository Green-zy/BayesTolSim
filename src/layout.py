# src/layout.py

import dash_bootstrap_components as dbc
from dash import html, dcc

layout = dbc.Container([
    dcc.Store(id="dim-count", data=0),
    html.Div(id="dummy-output", style={"display": "none"}),  # Add dummy output

# Card 1: Header with Professional Design and User Guide Link
    dbc.Card([
        dbc.CardBody([
            html.Div([
                # Left side - Title and subtitle
                html.Div([
                    html.H2("Bayesian Monte Carlo Tolerance Analysis", 
                           className="card-title",
                           style={
                               "color": "#2c3e50",
                               "fontWeight": "bold",
                               "marginBottom": "8px",
                               "fontSize": "2.2rem"
                           }),
                    html.P("Advanced Statistical Analysis for Engineering Design",
                          style={
                              "color": "#7f8c8d",
                              "fontSize": "1.1rem",
                              "fontStyle": "italic",
                              "marginBottom": "0px",
                              "fontWeight": "300"
                          })
                ], style={
                    "flex": "1",
                    "display": "flex",
                    "flexDirection": "column",
                    "justifyContent": "center"
                }),
                
                # Right side - User Guide Link
                html.Div([
                    html.A(
                        dbc.Button([
                            html.I(className="fas fa-book-open me-2"),  # Font Awesome book icon
                            "User Guide"
                        ], 
                        color="primary", 
                        size="lg",
                        style={
                            "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                            "border": "none",
                            "borderRadius": "25px",
                            "padding": "12px 24px",
                            "fontSize": "1.1rem",
                            "fontWeight": "600",
                            "boxShadow": "0 4px 15px rgba(102, 126, 234, 0.3)",
                            "transition": "all 0.3s ease"
                        }),
                        href="https://green-zy.github.io/BayesTolSim/",
                        target="_blank",
                        style={"textDecoration": "none"},
                        # Add hover effect via CSS
                        className="user-guide-btn"
                    )
                ], style={
                    "display": "flex",
                    "alignItems": "center"
                })
                
            ], style={
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "space-between"
            })
        ])
    ], className="mb-4", style={
        "marginTop": "10px",
        "background": "linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)",
        "border": "none",
        "boxShadow": "0 4px 12px rgba(0,0,0,0.1)"
    }),

    # Card 2: Dimension Setup
    dbc.Card([
        dbc.CardBody([
            html.H4("Dimension Chain Setup", style={"color": "#2c3e50", "fontWeight": "600"}),
            html.P("Enter expressions and press Enter to calculate results", 
                   style={"color": "gray", "fontSize": "0.9rem"}),
            dbc.ButtonGroup([
                dbc.Button("+ Add Dimension", id="add-dim", color="success", className="me-2"),
                dbc.Button("- Remove Dimension", id="remove-dim", color="danger")
            ]),
            html.Br(), html.Br(),
            html.Div(id="dimension-form-container")
        ])
    ], className="mb-4", style={"boxShadow": "0 2px 8px rgba(0,0,0,0.08)"}),

    # Card 3: Chain Viewer
    dbc.Card([
        dbc.CardBody([
            html.H4("Current Dimension Chain", style={"color": "#2c3e50", "fontWeight": "600"}),
            html.Div([
                html.Div([
                    html.Label("Tolerance for final dimension:", 
                              style={"fontWeight": "bold", "marginRight": "15px", "alignSelf": "center"}),
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
    ], className="mb-4", style={"boxShadow": "0 2px 8px rgba(0,0,0,0.08)"}),

    # Cards 4 & 5: Dimension Distribution Viewer and Final Dimension Distribution - Same row
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("View Distribution of a Dimension", 
                           style={"color": "#2c3e50", "fontWeight": "600"}),
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
            ], style={"height": "100%", "boxShadow": "0 2px 8px rgba(0,0,0,0.08)"})  # Ensure full height
        ], width=6, style={"paddingRight": "15px"}),  # Card 4 - 6/12 width with more right padding
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Final Dimension Distribution", 
                           style={"color": "#2c3e50", "fontWeight": "600"}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Label("Number of Samples:", 
                                          style={"marginRight": "10px", "fontWeight": "bold", "alignSelf": "center"}),
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
            ], style={"height": "100%", "boxShadow": "0 2px 8px rgba(0,0,0,0.08)"})  # Ensure full height
        ], width=6, style={"paddingLeft": "15px"})  # Card 5 - 6/12 width with more left padding
    ], className="mb-4", style={"minHeight": "600px"}),  # Set minimum height for the row
    
    # Author information - Below Card 4 & 5 with enhanced styling
    html.Div([
        html.Hr(style={"margin": "40px 0 20px 0", "border": "none", "height": "1px", "background": "linear-gradient(90deg, transparent, #dee2e6, transparent)"}),
        html.P([
            html.Strong("BayesTolSim: "),
            "A Bayesian Monte Carlo tolerance analysis tool for engineering design. ",
            html.Br(),
            html.Strong("Author: "),
            "Yun Zhou | ",
            html.Strong("Email: "),
            html.A("robbiezhou1@gmail.com", 
                   href="mailto:robbiezhou1@gmail.com", 
                   style={"color": "#007bff", "textDecoration": "none"}),
            " | ",
            html.Strong("Github: "),
            html.A("https://github.com/Green-zy", 
                   href="https://github.com/Green-zy", 
                   target="_blank", 
                   style={"color": "#007bff", "textDecoration": "none"}),
            " | ",
            html.Strong("LinkedIn: "),
            html.A("www.linkedin.com/in/yun-zhou-robbie-172966187", 
                   href="https://www.linkedin.com/in/yun-zhou-robbie-172966187", 
                   target="_blank", 
                   style={"color": "#007bff", "textDecoration": "none"})
        ], style={
            "fontSize": "0.85rem",
            "color": "#6c757d",
            "textAlign": "center",
            "marginTop": "10px",
            "marginBottom": "30px",
            "lineHeight": "1.4",
            "padding": "20px",
            "background": "#f8f9fa",
            "borderRadius": "8px",
            "border": "1px solid #e9ecef"
        })
    ])
], fluid=True)