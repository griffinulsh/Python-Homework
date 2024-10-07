import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import requests
from bs4 import BeautifulSoup
import os
import csv

file_path = "/Users/griffinulsh/Desktop/python_homework/datasets/WorldsBestRestaurants.csv"
data = pd.read_csv(file_path)

all_restaurants = data["restaurant"].tolist()

restaurant_counts = pd.Series(all_restaurants).value_counts()

most_popular = restaurant_counts[restaurant_counts > 10]

fig = px.bar(most_popular, x=most_popular.index, y=most_popular.values)

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children="World's Best Restaurants '02-'24"),
    html.Div(children='Analysis of the most frequent restaurants from 2002 to 2022.'),
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)