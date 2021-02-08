import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input

data = pd.read_csv("waterdata.csv")
data["Time"] = pd.to_datetime(data["Time"], format="%Y-%m-%d")


external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Sensor Analytics: Understanding Your Metrics!"

app.layout = html.Div( 
    children=[
        html.Div(
            children=[
                html.P(children="", className="header-emoji"),
                html.H1(
                    children="Sensor Analytics", className="header-title"
                ),
                html.P(
                    children="Visualization analysis of sensor readings "
                    ,
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Metrics", className="menu-title"),
                        dcc.Dropdown(
                            id="metrics-filter",
                            options=[
                                {"label": col, "value": col}
                                for col in data.columns
                            ],
                            value="Tp",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Event", className="menu-title"),
                        dcc.Dropdown(
                            id="event-filter",
                            options=[
                                {"label": 'False', "value":'False'},
                                {"label": 'True', "value":'True'}
                            ],
                            value="False",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range", className="menu-title"
                        ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data.Time.min().date(),
                            max_date_allowed=data.Time.max().date(),
                            start_date=data.Time.min().date(),
                            end_date=data.Time.max().date(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="series1",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                
            ],
            className="wrapper",
        ),
    ]
)

@app.callback(
    Output("series1", "figure"),
    [
        Input("metrics-filter", "value"),
        Input("event-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),    
    ],
)
def update_charts(metrics,event,start_date, end_date):
    df = data
    
    mask =((df.Time >= start_date) & (df.Time <= end_date))
    df_selected = df.loc[mask,:]
    
    #df_selected = df_selected [df_selected ['EVENT']==True]
    
    if (event == 'True') :
        df_selected = df_selected [df_selected ['EVENT']==True]
    
    else:
        df_selected = df_selected [df_selected ['EVENT']==True]
    
        
    chart_figure = {
        "data": [
            {
                "x": df_selected["Time"],
                "y": df_selected[metrics],
                "type": "lines",
                "hovertemplate": "%{y:.2f}<extra></extra>",
            },
        ],
       "layout": {
            "title": {
                "text": "Sensor readings",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }
    return chart_figure


    
    
    
    

  


if __name__ == "__main__":
    app.run_server(debug=True)
