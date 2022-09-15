from dash import html, dcc
from callbacks import df_raw
colors = {
    # For black backgroung
    # 'background': 'rgb(50, 50, 50)',
    # 'text':  'white'      # '#7FDBFF'
    'background': 'white',
    'text':  'black'      # '#7FDBFF'

}
layout = html.Div(style={'backgroundColor': colors['background']},children=[
    html.Div([html.Div([
        # html.Img(src = app.get_asset_url('logo.png'),style = {'height': '50px'},className = 'title_image'),
        # html.Div([dcc.Link('Go to Summary', href='/page1'),
              html.H1('Module Level Analysis',style={'color': colors['text']},
                      className = 'title'),],className = 'logo_title'),
    html.Div([
            html.P('Select Product',
                   style = {'color': colors['text']},
                   className = 'drop_down_list_title'
                   ),
                                dcc.Dropdown(id='Products',
                                             options=[{'label': i, 'value': i}
                                                      for i in df_raw['PRODUCT_NAME'].unique()],
                                             clearable = True,
                                             value= None,
                                             placeholder='Select a product here',
                                             searchable=True,
                                             className = 'drop_down_list'),
    ], className = 'title_drop_down_list'),
        html.Div([
            html.P('Select Month',
                   style = {'color': colors['text']},
                   className = 'drop_down_month_title'
                   ),
                                dcc.Dropdown(id='Month',
                                             options=[{'label': i, 'value': i}
                                                      for i in df_raw['MONTH'].unique()],
                                             clearable = True,
                                             value= None,
                                             placeholder='Select a month here',
                                             searchable=True,
                                             className = 'drop_down_month'),
        ], className = 'month_drop_down_list'),], className = 'title_and_drop_down_list'),
    html.H3('Faults Data'),
    dcc.Dropdown(id='List of Faults',
                 value=None,
                 placeholder='Select a Fault here',
                 searchable=True),
    html.Br(),
    html.Div(id='Faults_list')
])