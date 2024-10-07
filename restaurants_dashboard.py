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
    app.run_server(debug=True)# Import necessary libraries for building the dashboard
    import dash
    from dash import dcc, html
    import pandas as pd
    import plotly.express as px
    import requests
    from bs4 import BeautifulSoup
    import os
    import csv
    
    # Specify the file path to the dataset
    file_path = "/Users/griffinulsh/Desktop/python_homework/datasets/WorldsBestRestaurants.csv"
    
    # Load the dataset into a pandas DataFrame
    data = pd.read_csv(file_path)
    
    # Extract the list of restaurants from the DataFrame
    all_restaurants = data["restaurant"].tolist()
    
    # Create a pandas Series to count the occurrences of each restaurant
    restaurant_counts = pd.Series(all_restaurants).value_counts()
    
    # Filter the Series to include only restaurants with more than 10 occurrences
    most_popular = restaurant_counts[restaurant_counts > 10]
    
    # Create a bar chart using plotly express to visualize the most popular restaurants
    fig = px.bar(most_popular, x=most_popular.index, y=most_popular.values)
    
    # Initialize the Dash app
    app = dash.Dash(__name__)
    
    # Define the layout of the app
    app.layout = html.Div(children=[
        # Add a title to the app
        html.H1(children="World's Best Restaurants '02-'24"),
        
        # Add a brief description of the app
        html.Div(children='Analysis of the most frequent restaurants from 2002 to 2022.'),
        
        # Add the bar chart to the app
        dcc.Graph(figure=fig)
    ])
    
    # Run the app if this script is executed directly (i.e., not imported as a module)
    if __name__ == '__main__':
        app.run_server()