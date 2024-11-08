# Software Requirements Specification (SRS)

#Start here to download the data set: https://www.kaggle.com/datasets/thomasfranois/worlds-best-restaurants

## 1. Introduction

### 1.1 Purpose
The purpose of this document is to outline the requirements for the interactive data visualization web application that analyzes the World's Best Restaurants dataset. The application will enable users to explore restaurant data dynamically, allowing them to visualize the frequency of restaurant appearances over multiple years, categorized by country or restaurant name.

### 1.2 Scope
This application will provide a user-friendly interface for displaying and analyzing data on the world's best restaurants from 2002 to 2023. Users will be able to filter the data by country or restaurant, view appearances in a bar chart format, and gain insights through interactive features.

### 1.3 Definitions, Acronyms, and Abbreviations
- **SRS**: Software Requirements Specification
- **UI**: User Interface
- **API**: Application Programming Interface

### 1.4 Overview
This document describes the overall functionality of the application, including user interface requirements, system features, and the technical architecture needed to achieve the intended outcomes.

## 2. Overall Description

### 2.1 Product Perspective
The application will be a standalone web application developed using the Dash framework and Plotly for data visualization. It will utilize a CSV dataset containing information about the world's best restaurants.

### 2.2 Product Functions
The main functions of the application include:
- Loading and processing the restaurant dataset.
- Allowing users to upload a file path for the dataset.
- Displaying a bar chart of restaurants by appearance frequency.
- Allowing users to select the x-axis and y-axis to dynamically update the graph.
- Showing restaurant names directly on the bars for clarity when viewing data by country.

### 2.3 User Classes and Characteristics
- **Data Analysts**: Users who wish to analyze the data in-depth and extract insights.
- **General Users**: Users interested in viewing the trends in the world's best restaurants without needing extensive data analysis skills.

### 2.4 Operating Environment
The application will run in a web browser and will be accessible from any device with an internet connection. It will require:
- A modern web browser (Chrome, Firefox, Safari, etc.)
- Internet access to view the application hosted on a server.

### 2.5 Design and Implementation Constraints
- The application must be responsive to ensure usability across different screen sizes.
- It should adhere to accessibility standards for inclusive design.

### 2.6 Assumptions and Dependencies
- The application assumes that users have a basic understanding of data visualization concepts.
- It relies on the availability of the Plotly and Dash libraries for data visualization and interaction.

## 3. Specific Requirements

### 3.1 Functional Requirements

#### 3.1.1 Data Loading
- The application shall load the dataset from a specified CSV file.
- The application shall process the data to aggregate restaurant appearances and details.

#### 3.1.2 File Upload
- The application shall provide an interface for users to upload a file path for the dataset.
- The application shall validate the uploaded file to ensure it is in the correct CSV format.

#### 3.1.3 Graph Display
- The application shall display a bar chart representing restaurant appearances.
- Users shall have the option to select the x-axis as either "Country" or "Restaurant".
- The y-axis shall display the count of appearances.
- The application shall display restaurant names directly on the stacked bars when the x-axis is set to "Country".

#### 3.1.4 Interactivity
- Users shall be able to dynamically update the graph based on their selection of x-axis and y-axis.
- The application shall provide hover information showing detailed data about each bar segment.

### 3.2 Non-Functional Requirements

#### 3.2.1 Usability
- The UI shall be intuitive and user-friendly, with clear labeling and instructions.
- Users shall be able to navigate the application without extensive training.

#### 3.2.2 Performance
- The application shall load the dataset and render the initial graph within 2 seconds.
- Dynamic updates to the graph based on user input shall occur within 1 second.

#### 3.2.3 Reliability
- The application shall handle errors gracefully, providing user-friendly messages in case of failures (e.g., file not found, data processing errors).

#### 3.2.4 Security
- User data and interactions with the application shall be protected against unauthorized access.

### 3.3 User Interface Requirements

#### 3.3.1 Layout
- The application shall have a clear layout divided into three main sections: 
  1. Top menu with the title and description.
  2. Left interaction menu for dropdown selections.
  3. Main graph display area.

#### 3.3.2 Components
- The application shall include:
  - An upload component for users to specify the file path.
  - Dropdowns for selecting x-axis and y-axis.
  - A graph display area that updates based on user selections.

#### 3.3.3 Styling
- The application shall utilize a clean and modern design with appropriate spacing and font choices.

## 4. External Interface Requirements

### 4.1 User Interfaces
- The application will provide a web-based UI accessible through standard web browsers.

### 4.2 Hardware Interfaces
- The application will run on server-side hardware capable of hosting a Dash application.

### 4.3 Software Interfaces
- The application will depend on:
  - Dash framework for building the web application.
  - Plotly library for data visualization.
  - Pandas library for data manipulation.

## 5. Appendices
### 5.1 Code Snippet
```python
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

    # Left interaction menu
    html.Div(
        children=[
            html.Label('Upload CSV File:'),
            dcc.Upload(
                id='upload-data',
                children=html.Button('Upload File'),
                multiple=False
            ),
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
        style={'width': '20%', 'float': 'left', 'padding': '20px'}
    ),

    # Main graph display
    html.Div(
        children=[
            dcc.Graph(id='main-graph', figure=create_initial_figure())
        ],
        style={'width': '75%', 'float': 'right', 'padding': '20px'}
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
    fig = px.bar(
        most_popular, 
        x=x_axis, 
        y=y_axis,
        title=f"{x_axis.capitalize()} vs {y_axis.capitalize()}"
    )
    fig.update_layout(
        xaxis_title=x_axis.capitalize(),
        yaxis_title=y_axis.capitalize()
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
