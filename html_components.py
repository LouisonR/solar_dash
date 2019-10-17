import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt

def build_header():
    return html.Div(
                    id="header",
                    children=[
                        html.Div(
                                [
                                    html.H1("SOLAR PLANT DASHBOARD")], className="ten columns"),
                                    html.Img(id="logo_header", src="/assets/sun.png", style={'height':'10%','width':'10%'})
                                ],
                    className="row",
                    )


def build_graphs():
    return html.Div(
                    children =
                            [   html.Span(children=[" "]),
                                html.Div(children=[
                                                html.Span(children=[" "]),
                                                html.H5(html.Div(id='line_title'), className="eight columns"),
                                                html.Div([dcc.Graph(id="line_graph")], className="eight columns"),
                                                html.H5(html.Div(id='box_title'), className="eight columns"),
                                                html.Div([dcc.Graph(id="box_graph")], className="eight columns"),
                                                ],
                                        className = "eight column")
                            ],
                    className="column",
                    )


def build_menu(start_date, options):
    return html.Div(
                    id="header_viz",
                    children=[
                                #html.H3("Visualization Module"),
                                html.Span(children=[" "]),
                                html.Div(id="site_dropdown",
                                        children=[
                                                    html.H5("Select the site you want to display"),
                                                    html.Span(children=[" "]),
                                                    dcc.Dropdown(
                                                                    id='site-id',
                                                                    style={'width': '380px'}
                                                                )
                                                ],
                                        className = "two column"
                                        ),
                                html.Div(id="variable_dropdown",
                                        children=[
                                                    html.H5("Select the variable you want to display"),
                                                    html.Span(children=[" "]),
                                                    dcc.Dropdown(
                                                                    id='var-id',
                                                                    options=options,
                                                                    style={'width': '380px'}
                                                                )
                                                ],
                                        className = "two column"
                                        ),
                                html.Div(id="date_picker",
                                        children=[
                                                    html.H5("Select the timeframe you want to display"),
                                                    html.Span(children=[" "]),
                                                    dcc.DatePickerSingle(
                                                                            id='starting-date',
                                                                            min_date_allowed=start_date,
                                                                            max_date_allowed=dt.today(),
                                                                            initial_visible_month=start_date,
                                                                            date=str(start_date)
                                                                        ),
                                                    html.Span(children=[" "]),
                                                    dcc.DatePickerSingle(
                                                                            id='ending-date',
                                                                            min_date_allowed=start_date,
                                                                            max_date_allowed=dt.today(),
                                                                            initial_visible_month=dt.today(),
                                                                            date=str(dt.today())
                                                                        ),
                                                    html.Span(children=[" "]),
                                                    html.Button(
                                                                    id="submit-visu-button",
                                                                    n_clicks=0,
                                                                    children="Submit"
                                                                ),
                                                ],
                                        className = "two column"
                                        ),
                            ],
                    className="row",
                    )
