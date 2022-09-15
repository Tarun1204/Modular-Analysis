# Import required libraries
from dash import html, dcc
from callbacks import df_raw

colors = {
    # For black background
    # 'background': 'rgb(50, 50, 50)',
    # 'text':  'white'      # '#7FDBFF'
    'background': 'white',
    'text':  'black'      # '#7FDBFF'

}
# Create an app layout instead of app.layout we are using layout for multiple pages
layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.Div([html.Div([
        # html.Img(src = app.get_asset_url('logo.png'),style = {'height': '50px'},className = 'title_image'),
              html.H1('Module Level Analysis', style={'color': colors['text']},
                      className='title'), ], className='logo_title'),
              html.Div([
                  html.P('Select Product',
                         style={'color': colors['text']},
                         className='drop_down_list_title'),
                  dcc.Dropdown(id='Products',
                               options=[{'label': i, 'value': i}
                                        for i in df_raw['PRODUCT_NAME'].unique()],
                               clearable=True,
                               value=None,
                               placeholder='Select a product here',
                               searchable=True,
                               className='drop_down_list'),
              ], className='title_drop_down_list'),
              html.Div([
                  html.P('Select Month',
                         style={'color': colors['text']},
                         className='drop_down_month_title'),
                  dcc.Dropdown(id='Month',
                               options=[{'label': i, 'value': i}for i in df_raw['MONTH'].unique()],
                               clearable=True,
                               value=None,
                               placeholder='Select a month here',
                               searchable=True,
                               className='drop_down_month'),
              ], className='month_drop_down_list'), ], className='title_and_drop_down_list'), html.Br(),
    html.Div([
        html.Div([html.H6(children='Tested',
                          style={'textAlign': 'center', 'color': 'white', 'fontSize': 20}),
                  html.P(id='tested_value',
                         style={
                             'textAlign': 'center', 'color': 'orange', 'fontSize': 40,
                             'margin-top': '-18px'})], className="card_container three columns",),
        html.Div([
            html.H6(children='Pass',
                    style={
                        'textAlign': 'center',
                        'color': 'white', 'fontSize': 20}
                    ),

            html.P(id='pass_value',
                   style={
                       'textAlign': 'center',
                       'color': 'green', 'margin-top': '-18px',
                       'fontSize': 40}
                   )], className="card_container three columns",),
        html.Div([
            html.H6(children='Fail',
                    style={
                        'textAlign': 'center',
                        'color': 'white', 'fontSize': 20}
                    ),

            html.P(id='fail_value',
                   style={
                       'textAlign': 'center',
                       'color': '#dd1e35', 'margin-top': '-18px',
                       'fontSize': 40}
                   )], className="card_container three columns",),
        html.Div([
            html.H6(children='FTY',
                    style={
                        'textAlign': 'center',
                        'color': 'white', 'fontSize': 20}
                    ),

            html.P(id='fty_value',
                   style={
                       'textAlign': 'center',
                       'color': '#e55467', 'margin-top': '-18px',
                       'fontSize': 40}
                   )], className="card_container three columns")

    ], className="row flex-display"),
    html.Div([dcc.Graph(id='Faults')],),
    html.Br(),
    html.Br(),

    html.Div([
        html.Div([dcc.Graph(id='Bar')], style={'width': '50%'}),
        html.Div([dcc.Graph(id='Sunburst')], style={'width': '50%'})
                                 ], style={'display': 'flex'}),
    html.Br(),
    html.Br(),
                                ])
