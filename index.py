
# Import necessary libraries 
from dash import html, dcc
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app

# Connect to your app pages
from pages import page1, table, page2

# Connect the navbar to the index
from components import navbar

server = app.server

# Define the navbar
nav = navbar.navbar_input()

# Define the index page layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav,
    html.Div(id='page-content', children=[]),
])


# Create the callback to handle pages input
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page1':
        return page1.layout
    if pathname == '/table':
        return table.layout
    if pathname == '/page2':
        return page2.layout
    else:  # if redirected to unknown link
        return "404 Page Error! Please choose a link"


# Run the app on localhost:8050
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8049)
