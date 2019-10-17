from collections import OrderedDict
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
from datetime import date, datetime
from dateutils import relativedelta
import plotly.graph_objs as go
import pandas as pd

from graph_layout import date_layout, generic_layout
from html_components import build_header, build_menu, build_graphs
from loading_data import get_df, get_variables_id_name, get_sites_id_name, get_clients_id, get_access_sites
from auxilaries import build_options, get_name


## I - INPUTS:
#variables_lst contains a list of tuples (var_id, var_name)
variables_lst = get_variables_id_name()
#site_lst contains a list of tuples (site_id, site_name)
sites_lst = get_sites_id_name()
#client_lst contains a list of client_id
client_lst = get_clients_id()
#admin id: full access to all sites
admin_id = [0]
#list of sites you have access from the dashaboard
sites_access = []
#Oldest data history date
start_date = date(2019, 9, 25)


## II - CSS LINKS
external_stylesheets = [
                            "https://codepen.io/chriddyp/pen/bWLwgP.css",
                            "/assets/style.css",
                        ]

## III - APP
app = dash.Dash(
                __name__,
                external_stylesheets=external_stylesheets,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1.0"}],
            )

server = app.server

app.layout = html.Div(
                    children=
                        [
                            dcc.Location(id='url', refresh=False),
                            build_header(),
                            html.Div(children=
                                            [
                                            build_menu(start_date, build_options(variables_lst)),
                                            html.Hr(),
                                            build_graphs(),
                                            ],
                                    className="column")
                        ],
                    className="row"
                    )


## IV - CALLBACKS
#       1. Visualization callback
@app.callback(
                [Output("line_graph", "figure"), Output("box_graph", "figure"), Output('line_title', 'children'), Output('box_title', 'children')],
                [Input('submit-visu-button', "n_clicks")],
                [State('site-id', "value"), State('var-id', "value"), State('starting-date', "date"), State('ending-date', "date")],
            )

def update_graph(n_clicks, site_id, var_id, starting_date, ending_date):
    """ Returns a figure.

    Parameters:
        n_clicks (int): 0 | 1
        site_id (list): list of string ["393", "412", "426", "437", "438", "521", "525", "543", "549"]
        starting_date (datetime): the starting date of the timeframe selected
        ending_date (datetime): the ending date of the timeframe selected

    Returns:
        figures (dict): tuple of figure

    """
    var_name = get_name(variables_lst, var_id, "variable")
    site_name = get_name(sites_lst, site_id, "site")
    print("updating the graph... data loading")
    #print("site_id: ", site_id)
    #print("var_id: ", var_id)
    df_sel = get_df(site_id, var_id, starting_date, ending_date)
    #line traces per equipment
    line_traces, box_traces = [], []
    for equi, df_group in df_sel.groupby('equipment'):
        line_traces.append(go.Scatter(x=df_group.datetime, y=df_group.value, name=equi, mode='lines'))
        box_traces.append(go.Box(x=df_group.equipment, y=df_group.value, name=equi))

    print("data agregated")
    line_figure = dict(data=line_traces, layout=date_layout)
    box_figure = dict(data=box_traces, layout=generic_layout)
    #print("traces: ", line_traces, box_traces)
    if line_traces == [] and box_traces == []:
        line_title = "SORRY, we don't have data to display for the couple: (variable: " + var_name + ", site: " + site_name + ") for that timeframe, check another variable."
        box_title = line_title
    else:
        box_title = "Graph2: distribution of " + var_name + " per equipment (on " + site_name + ")"
        line_title = "Graph1: " + var_name + " for the equipment of " + site_name
    return line_figure, box_figure, line_title, box_title


#       2. Access callback
#           Depending on your client_id (client1: 1, client2: 2, admin (full access): 0)
@app.callback(
                Output("site-id", "options"),
                [Input('url', 'pathname')],
            )

def update_dropdown(pathname):
    """ Returns dropdown options.

    Parameters:
        pathname (int): clientid (clientid = 0 if is_admin = 1, meaning access to all sites)

    Returns:
        options (list): list of dict (cf build_options function)
    """
    options = []
    if pathname == None:
        pass
    else:
        try:
            client_id = int(pathname[1:])
            #print("client_lst: ", client_lst)
            #print("client_id: ", client_id)
            if client_id in client_lst + admin_id:
                site_access = get_access_sites(client_id)
                #print("sites_access: ", site_access)
                options = build_options(site_access)
            #print(options)
        except:
            pass
    return list(options)
