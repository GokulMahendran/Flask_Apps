import pandas as pd
import numpy as np
import pickle
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input,Output,State

loaded_model = pickle.load(open("finalized_model.pkl", 'rb'))
encoder = pickle.load(open("encoder_category.pkl", 'rb'))
dict_of_models = pickle.load(open("dict_models.pkl", 'rb'))
cities = pickle.load(open("cities_list.pkl", 'rb'))


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server=app.server

Brands=list(dict_of_models.keys())
models=dict_of_models["Maruti"]
Transmission_=dict_of_models["Maruti"]["Baleno"][0]
Fuel_Type_=dict_of_models["Maruti"]["Baleno"][1]
Years=np.arange(1980,2021).tolist()

controls_cat = dbc.Card(
    [
        dbc.FormGroup(
            (
                html.P(),
                dbc.Label("Brand"),
                html.P(),
                dcc.Dropdown(
                    id="Brand",
                    options=[
                        {"label": col, "value": col} for col in Brands
                    ],
                    value="Maruti",
                ),
                html.P(),
                dbc.Label("Model"),
                html.P(),
                dcc.Dropdown(
                    id="Model",
                    options=[
                        {"label": col, "value": col} for col in models
                    ],
                    value="Baleno",
                ),
                html.P(),
                dbc.Label("Year"),
                html.P(),
                dcc.Dropdown(
                    id="Year",
                    options=[
                        {"label": col, "value": int(col)} for col in Years
                    ],
                    value=2019,
                ),
                html.P(),
                dbc.Label("Fuel Type"),
                html.P(),
                dcc.Dropdown(
                    id="Fuel Type",
                    options=[
                        {"label": col, "value": col} for col in Fuel_Type_
                    ],
                    value="Petrol",
                ),
                html.P(),
                dbc.Label("Transmission"),
                html.P(),
                dcc.Dropdown(
                    id="Transmission",
                    options=[
                        {"label": col, "value": col} for col in Transmission_
                    ],
                    value="Manual",
                ),
                html.P(),
                dbc.Label("City"),
                html.P(),
                dcc.Dropdown(
                    id="City",
                    options=[
                        {"label": col, "value": col} for col in cities
                    ],
                    value="Chennai",
                ),
                html.P(),
                dbc.Label("Kms Driven"),
                html.P(),
                dbc.Input(id="Kms Driven", placeholder="Type something...", type="number"),
                html.P(),
                dbc.Label("Owner"),
                html.P(),
                dbc.Input(id="Owner", placeholder="Type something...", type="number"),
                html.P(),
                dbc.Button(id="Submit-Button", children="Submit", color="info", className="mr-1", n_clicks=0)
            ))
    ],
    body=True,
)

jumbotron = dbc.Container(
            [
                html.P(id="output")
            ],
            fluid=True,
        )
app.layout = dbc.Container(
    [
        html.H1("Car Project"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls_cat, md=4),
                dbc.Col(jumbotron, md=8),
            ],
            align="center",
        ),
    ],
    fluid=True,
)

@app.callback(Output("Model","options"),
              [Input("Brand","value")])

def update_dropdown(Brand):
    models=[i for i in dict_of_models[Brand]]
    options_=[
        {"label": col, "value": col} for col in models
    ]
    return options_

@app.callback(Output("Fuel Type","options"),
              [Input("Model","value"),
              Input("Brand","value")])

def update_dropdown(Model,Brand):
    Fuel_Type_=dict_of_models[Brand][Model][1]
    options_=[
        {"label": col, "value": col} for col in Fuel_Type_
    ]
    return options_

@app.callback(Output("Transmission","options"),
              [Input("Model","value"),
              Input("Brand","value")])

def update_dropdown(Model,Brand):
    Transmission=dict_of_models[Brand][Model][0]
    options_=[
        {"label": col, "value": col} for col in Transmission
    ]
    return options_


@app.callback(Output("output","children"),
              [Input("Submit-Button","n_clicks")],
             [State("Brand","value"),
              State("Model","value"),
              State("Year","value"),
              State("Fuel Type","value"),
              State("Transmission","value"),
              State("City","value"),
              State("Kms Driven","value"),
              State("Owner","value")
              ])
def update_output(clicks,Brand,model,Year,Fuel_Type,Transmission,City,Kms_Driven,Owner):
    li = [Year, Kms_Driven, Fuel_Type, Owner, Transmission, City, Brand, model]
    if None not  in li:

        arr=np.array(li).reshape(1,8)
        cols=["Year",'Kms Driven', 'Fuel Type', 'Owner', 'Transmission', 'city', 'brand',
       'model']
        data_t=pd.DataFrame(data=arr,columns=cols)
        for i in ["Year","Kms Driven","Owner"]:
            data_t[i]=data_t[i].astype(int)
        data_t["Years_since_car_bought"]=2020-data_t["Year"]
        data_t=data_t.drop(columns=["Year"])
        data=encoder.transform(data_t)
        prediction= loaded_model.predict(data)
        return "The Value of the Car is"+" "+str(round(prediction[0]))+"."

if __name__ == "__main__":
    app.run_server()