import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import argparse
import os

#To run the code, enter in your terminal: python3 restaurants_dashboard.py --file_path '/path/to/WorldsBestRestaurants.csv' and add in the path to the 'WorldsBestRestaurants.csv' file on your local machine.

# Set up argparse to get file path from the user
parser = argparse.ArgumentParser(description="Analyze the World's Best Restaurants dataset")
parser.add_argument(
    '--file_path', 
    type=str, 
    help="Path to the 'WorldsBestRestaurants.csv' file",
    required=True
)

args = parser.parse_args()
file_path = args.file_path

# Check if the file exists
if not os.path.exists(file_path):
    print(f"File not found at {file_path}.")
    print("Please download the 'WorldsBestRestaurants.csv' file as directed in the README.")
    exit(1)  # Exit if file is missing
data = pd.read_csv(file_path)

# Grouping by 'restaurant' to aggregate appearances and details
restaurant_data = data.groupby('restaurant').agg({
    'year': lambda x: list(x),  # List of years of appearance
    'country': 'first',          # Assuming the country doesn't change
    'restaurant': 'count'        # Count of appearances
}).rename(columns={'restaurant': 'Appearances'})

# Filter restaurants with more than 10 appearances
most_popular = restaurant_data[restaurant_data['Appearances'] > 10].reset_index()
most_popular = most_popular.sort_values('Appearances', ascending=False)

# Create a mapping of countries to their restaurants
country_to_restaurants = most_popular.groupby('country')['restaurant'].apply(list).to_dict()

# Initial Bar Chart Creation
def create_initial_figure():
    fig = px.bar(
        most_popular, 
        x='restaurant', 
        y='Appearances', 
        title='Restaurants with More Than 10 Appearances'
    )
    
    fig.update_traces(
        hovertemplate=(
            'Restaurant: %{x}<br>'
            'Appearances: %{y}<br>'
            'Country: %{customdata[0]}<br>'
            '<extra></extra>'
        ),
        customdata=most_popular[['country']].values
    )
    fig.update_layout(
        xaxis_title='Restaurant',
        yaxis_title='Appearances'
    )
    
    return fig

# Define the layout for the app (SRS compliant structure)
app = dash.Dash(__name__)

app.layout = html.Div([
    # Top menu section
    html.Div(
        children=[
            html.H1("World's Best Restaurants '02-'23", style={'text-align': 'center'}),
            html.Div("An analysis of the most frequent restaurants from 2002 to 2023."),
        ], 
        style={'padding': '20px', 'background-color': '#f4f4f4'}
    ),

    # Flex container to hold left menu and main graph
    html.Div(
        children=[
            # Left interaction menu
            html.Div(
                children=[
                    html.Label('Select X-Axis:'),
                    dcc.Dropdown(
                        options=[
                            {'label': 'Restaurant', 'value': 'restaurant'},
                            {'label': 'Country', 'value': 'country'}
                        ],
                        value='restaurant',  # Default value
                        id='x-axis-dropdown',
                        style={'margin-bottom': '20px'}
                    ),
                    html.Label('Select Y-Axis:'),
                    dcc.Dropdown(
                        options=[
                            {'label': 'Appearances', 'value': 'Appearances'}
                        ],
                        value='Appearances',  # Default value
                        id='y-axis-dropdown',
                    ),
                ],
                style={
                    'min-width': '250px',  # Minimum width for the side menu
                    'padding': '20px',
                    'background-color': '#f9f9f9',
                    'border-right': '1px solid #ddd',
                    'flex-shrink': '0'  # Prevent shrinking below min-width
                }
            ),
            # Main graph display
            html.Div(
                children=[
                    dcc.Graph(id='main-graph', figure=create_initial_figure())
                ],
                style={
                    'flex-grow': '1',  # Allows this section to grow and shrink
                    'padding': '20px'
                }
            )
        ],
        style={
            'display': 'flex',  # Use flexbox for layout
            'flex-direction': 'row',
            'height': '100vh'  # Set the container to fill the viewport height
        }
    )
], style={  # Overall page styling
    'font-family': 'Arial',
    'padding': '20px',  
    'margin': '20px',
    'box-shadow': '5px 5px 10px rgba(0, 0, 0, 0.2)',
    'background-color': '#fff'
})

# Callback to update the graph dynamically based on dropdown input
@app.callback(
    dash.dependencies.Output('main-graph', 'figure'),
    [
        dash.dependencies.Input('x-axis-dropdown', 'value'),
        dash.dependencies.Input('y-axis-dropdown', 'value')
    ]
)
def update_graph(x_axis, y_axis):
    if x_axis == 'country':
        # Create a new DataFrame for stacked bars
        stacked_data = most_popular[['restaurant', 'country', 'Appearances']]

        # Create a stacked bar chart
        updated_fig = px.bar(
            stacked_data, 
            x='country', 
            y='Appearances', 
            color='restaurant',  # Color by restaurant
            title='Restaurants per Country',
            barmode='stack',
        )

        # Remove the text labels from bars but keep for hover
        updated_fig.update_traces(
            hovertemplate=(
                'Country: %{x}<br>'
                'Restaurant: %{customdata[0]}<br>'  # Display restaurant names in hover
                'Appearances: %{y}<br>'
                '<extra></extra>'
            ),
            customdata=stacked_data[['restaurant']].values,  # Pass restaurant names to hover
            text=None,  # Remove the text labels from bars
            showlegend=False  # Remove legend
        )
    else:
        # Create a bar chart by restaurant
        updated_fig = px.bar(
            most_popular, 
            x='restaurant', 
            y=y_axis, 
            title='Updated Visualization'
        )

        updated_fig.update_traces(
            hovertemplate=(
                'Restaurant: %{x}<br>'
                'Appearances: %{y}<br>'
                'Country: %{customdata[0]}<br>'
                '<extra></extra>'
            ),
            customdata=most_popular[['country']].values,  # Ensure customdata includes country
            text=None,  # Remove the text labels from bars
            showlegend=False  # Remove legend
        )

    updated_fig.update_layout(
        xaxis_title=x_axis.capitalize(),
        yaxis_title=y_axis.capitalize()
    )
    return updated_fig



if __name__ == '__main__':
    app.run_server(debug=True)
