import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Load the dataset
file_path = "/Users/griffinulsh/Desktop/python_homework/datasets/WorldsBestRestaurants.csv"
data = pd.read_csv(file_path)

# Grouping by 'restaurant' to aggregate appearances and details
restaurant_data = data.groupby('restaurant').agg({
    'year': lambda x: list(x),  # List of years of appearance
    'country': 'first',         # Assuming the country doesn't change
    'restaurant': 'count'       # Count of appearances
}).rename(columns={'restaurant': 'Appearances'})

# Filter restaurants with more than 10 appearances
most_popular = restaurant_data[restaurant_data['Appearances'] > 10]

# Reset index to make 'restaurant' a regular column
most_popular = most_popular.reset_index()

# Sort by appearance count in descending order
most_popular = most_popular.sort_values('Appearances', ascending=False)

# Create the bar chart
fig = px.bar(
    most_popular, 
    x='restaurant',          # Use lowercase 'restaurant' for the x-axis
    y='Appearances', 
    title='Restaurants with More Than 10 Appearances'
)

# Update hover template to format the labels correctly
fig.update_traces(
    hovertemplate=(
        'Restaurant: %{x}<br>'        # %{x} refers to the restaurant name
        'Appearances: %{y}<br>'       # %{y} refers to the appearances
        'Country: %{customdata[0]}<br>'  # customdata[0] refers to the country
        'Years: %{customdata[1]}<br>'     # customdata[1] refers to the years
        '<extra></extra>'              # Remove extra hover information
    ),
    customdata=most_popular[['country', 'year']].values  # Add country and years as custom data
)

# Update the axis labels to be capitalized
fig.update_layout(
    xaxis_title='Restaurant',  # Capitalize the x-axis label
    yaxis_title='Appearances'   # Capitalize the y-axis label
)

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children="World's Best Restaurants '02-'23"),
    html.Div(children='Analysis of the most frequent restaurants from 2002 to 2023.'),
    dcc.Graph(figure=fig)
], style={  # Inline CSS to apply the border
        'border': '2px solid black',  # You can change the color and width
        'padding': '20px',  # Adds padding between the content and border
        'margin': '20px',   # Adds space outside the border
        'box-shadow': '5px 5px 10px rgba(0, 0, 0, 0.2)'  # Optional: adds a shadow for better visibility
    }
)



if __name__ == '__main__':
    app.run_server(debug=True)
