# Import required libraries
from dash import html, dcc
from callbacks import df_raw

filtered_df = df_raw.loc[df_raw['STAGE'] == 'ATE']

colors = {
    # For black background
    # 'background': 'rgb(50, 50, 50)',
    # 'text':  'white'      # '#7FDBFF'
    'background': 'white',
    'text':  'black'      # '#7FDBFF'
}
# Create an app layout instead of app.layout we are using layout for multiple pages
layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.Div([
        html.Div([
              html.H1('Module Level Analysis', style={'color': colors['text']},
                      className='title'), ], className='logo_title'),
        html.Div([
            html.P('Select Product',
                   style={'color': colors['text']},
                   className='drop_down_list_title'
                   ),
            dcc.Dropdown(id='Product_f2',
                         # options=[{'label': i, 'value': i}for i in filtered_df['PRODUCT_NAME'].unique()],
                         clearable=True,
                         value=None,
                         placeholder='Select a product here',
                         searchable=True,
                         className='drop_down_list'),
        ], className='title_drop_down_list'),
        html.Div([
            html.P('Select Month',
                   style={'color': colors['text']},
                   className='drop_down_month_title'
                   ),
            dcc.Dropdown(id='Month',
                         options=[{'label': i, 'value': i}for i in df_raw['MONTH'].unique()],
                         clearable=True,
                         value=None,
                         placeholder='Select a month here',
                         searchable=True,
                         className='drop_down_month'),
        ], className='month_drop_down_list'), ], className='title_and_drop_down_list'),
    html.Div([
        html.Div([html.H6(children='Tested',
                          style={'textAlign': 'center', 'color': 'white', 'fontSize': 20}),
                  html.P(id='tested_value_f2',
                         style={
                             'textAlign': 'center', 'color': 'orange', 'fontSize': 40,
                             'margin-top': '-18px'})], className="card_container three columns",),
        html.Div([
            html.H6(children='Pass',
                    style={
                        'textAlign': 'center',
                        'color': 'white', 'fontSize': 20}
                    ),
            html.P(id='pass_value_f2',
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
            html.P(id='fail_value_f2',  # f"{covid_data_1['recovered'].iloc[-1]:,.0f}"
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
            html.P(id='fty_value_f2',  # f"{covid_data_1['active'].iloc[-1]:,.0f}"
                   style={
                       'textAlign': 'center',
                       'color': '#e55467', 'margin-top': '-18px',
                       'fontSize': 40}
                   )], className="card_container three columns")
    ], className="row flex-display"),
    html.Div([
        html.Div([html.P('Select Stage:', className='fix_label',  style={'color': 'white'}),
                  dcc.Dropdown(id='stages',
                                  multi=False,
                                  clearable=True,
                                  placeholder='Select Stage',
                                  className='drop_down_stage'),
                  dcc.Graph(id='Tested', config={'displayModeBar': False}, className='dcc_compon',
                            style={'margin-top': '20px'},
                            ),

                  dcc.Graph(id='Pass1', config={'displayModeBar': False}, className='dcc_compon',
                            style={'margin-top': '20px'},
                            ),

                  dcc.Graph(id='Fail', config={'displayModeBar': False}, className='dcc_compon',
                            style={'margin-top': '20px'},
                            ),

                  dcc.Graph(id='%Fail', config={'displayModeBar': False}, className='dcc_compon',
                            style={'margin-top': '20px'},
                            ),
                  ], className="create_container two columns", id="cross-filter-options"),
        html.Div([
                      dcc.Graph(id='pie_chart1',
                                config={'displayModeBar': 'hover'}),
                              ], className="create_container four columns"),
        html.Div([
            dcc.Graph(id="Bar1")
                    ], className="create_container five columns"),
        ], className="row flex-display"),
                                ])
