# Import required libraries
import pandas as pd
import numpy as np
import dash_html_components as html
from dash import html, callback, Input, Output
import plotly.express as px
from dash import dash_table
import plotly.graph_objs as go

xls = pd.ExcelFile("MCM.xlsx", engine='openpyxl')
# to read all sheets to a map

sheet_to_df_map = {}
for sheet_name in xls.sheet_names:
    sheet_to_df_map[sheet_name] = xls.parse(sheet_name)
# sheet_to_df_map
# print(sheet_to_df_map.get("RAW"))
sheet_name_list = list(sheet_to_df_map.keys())
# print(sheet_name_list)
df_raw = sheet_to_df_map.get("RAW")
df_raw["REPAIRING_DATE"] = df_raw["REPAIRING_DATE"].replace(np.nan, 'Pending', regex=True)
for i in range(len(df_raw)):
    # print(df_raw.loc[i]["Repaired Date "])
    if df_raw.loc[i]["REPAIRING_DATE"] == "Pending":
        df_raw.at[i, "FAULT_CATEGORY"] = "Pending"
        df_raw.at[i, "REPAIRING_ACTION"] = "Pending"
        df_raw.at[i, "KEY_COMPONENT"] = "Pending"
        df_raw.at[i, "POSSIBLE_REASON"] = "Pending"

df_raw['TOTAL'] = 'TOTAL'
df = df_raw[['PRODUCT_NAME', 'PART_CODE', 'DATE', 'MONTH', 'STAGE', 'FAULT_OBSERVED', 'FAULT_CATEGORY',
             'REPAIRING_ACTION', 'KEY_COMPONENT', 'POSSIBLE_REASON']]

df_card = sheet_to_df_map.get("Card")
df_card.rename(columns=df_card.iloc[0], inplace=True)
df_card.drop(df_card.index[0], inplace=True)

# group by product for card
card_product_total = df_card.groupby(['PRODUCT'])[['TEST QUANTITY', 'PASS QUANTITY', 'REJECT QUANTITY', 'FTY(%)']].sum()

# group by product for part code and month
card_part_code_month = df_card.groupby(['PRODUCT', 'PART CODE', 'MONTH'])[['TEST QUANTITY', 'PASS QUANTITY',
                                                                           'REJECT QUANTITY', 'FTY(%)']].sum()

# group by product for month
card_month = df_card.groupby(['PRODUCT', 'MONTH'])[['TEST QUANTITY', 'PASS QUANTITY', 'REJECT QUANTITY', 'FTY(%)']]\
    .sum().reset_index().set_index('PRODUCT')

df_smr = sheet_to_df_map.get("SMR")
df_smr_filter = df_smr.groupby('PRODUCT').sum()
df_mcm = sheet_to_df_map.get("MCM")
df_mcm_filter = df_mcm.groupby('PRODUCT').sum()


def generate_table(dataframe, max_rows=100):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[j][col]) for col in dataframe.columns
        ]) for j in range(min(len(dataframe), max_rows))]
    )


colors = {
    # For black backgroung
    # 'background': 'rgb(50, 50, 50)',
    # 'text':  'white'      # '#7FDBFF'
    'background': 'white',
    'text':  'black'      # '#7FDBFF'
}

# TASK 2:
# Add a callback function for `Products` as input, `Faults` as output


@callback(
    Output(component_id='tested_value', component_property='children'),
    [Input(component_id='Products', component_property='value'),
     Input(component_id='Month', component_property='value')])
def test_count(product, month):
    total = card_product_total  # for total
    month_wise = card_month  # month vise card
    # part_code_wise = card_part_code_month  # for part code data
    # tested, pass_v, fail = compute_info(Total, product)
    if product is None:
        if month is None:
            return f"{total['TEST QUANTITY'].loc['TOTAL']:,.0f}"
        else:
            # need to add month column
            a = month_wise.loc[month_wise['MONTH'] == month]['TEST QUANTITY'].sum()
            return a
    else:
        if month is None:
            return f"{total['TEST QUANTITY'].loc[product]:,.0f}"
        else:
            # need to add month column
            a = month_wise.loc[month_wise['MONTH'] == month]
            return f"{a['TEST QUANTITY'].loc[product]:,.0f}"


@callback(
    Output(component_id='pass_value', component_property='children'),
    [Input(component_id='Products', component_property='value'),
     Input(component_id='Month', component_property='value')])
def pass_count(product, month):
    total = card_product_total  # for total
    month_wise = card_month  # month vise card
    # part_code_wise = card_part_code_month  # for part code data
    if product is None:
        if month is None:
            return f"{total['PASS QUANTITY'].loc['TOTAL']:,.0f}"
        else:
            # need to add month column
            a = month_wise.loc[month_wise['MONTH'] == month]['PASS QUANTITY'].sum()
            return a
    else:
        if month is None:
            return f"{total['PASS QUANTITY'].loc[product]:,.0f}"
        else:
            # need to add month column
            a = month_wise.loc[month_wise['MONTH'] == month]
            return f"{a['PASS QUANTITY'].loc[product]:,.0f}"


@callback(
    Output(component_id='fail_value', component_property='children'),
    [Input(component_id='Products', component_property='value'),
     Input(component_id='Month', component_property='value')])
def fail_count(product, month):
    total = card_product_total  # for total
    month_wise = card_month  # month vise card
    # part_code_wise = card_part_code_month  # for part code data
    if product is None:
        if month is None:
            return f"{total['REJECT QUANTITY'].loc['TOTAL']:,.0f}"
        else:
            # need to add month column
            a = month_wise.loc[month_wise['MONTH'] == month]['REJECT QUANTITY'].sum()
            return a
    else:
        if month is None:
            return f"{total['REJECT QUANTITY'].loc[product]:,.0f}"
        else:
            # need to add month column
            a = month_wise.loc[month_wise['MONTH'] == month]
            return f"{a['REJECT QUANTITY'].loc[product]:,.0f}"


@callback(
    Output(component_id='fty_value', component_property='children'),
    [Input(component_id='Products', component_property='value'),
     Input(component_id='Month', component_property='value')])
def fty_count(product, month):
    total = card_product_total  # for total
    month_wise = card_month  # month vise card
    # part_code_wise = card_part_code_month  # for part code data
    if product is None:
        if month is None:
            # a = str(round(((month_wise['PASS QUANTITY'].sum() / Total['TEST QUANTITY'].sum()) * 100), 1)) + '%'
            a = str(round((total['FTY(%)'].loc['TOTAL']*100), 1)) + '%'
            return a
        else:
            # need to add month column
            a = month_wise.loc[month_wise['MONTH'] == month]['TEST QUANTITY'].sum()
            b = month_wise.loc[month_wise['MONTH'] == month]['PASS QUANTITY'].sum()
            c = str(round(((b/a)*100), 1)) + '%'
            return c
    else:
        if month is None:
            a = str(round(((total['PASS QUANTITY'].loc[product] / total['TEST QUANTITY'].loc[product])*100), 1)) + '%'
            return a
        else:
            # need to add month column
            d = month_wise.loc[month_wise['MONTH'] == month]
            a = str(round((((d['PASS QUANTITY'].loc[product]) / (d['TEST QUANTITY'].loc[product]))*100), 1)) + '%'
            return a


@callback(Output(component_id='Faults', component_property='figure'),
          [Input(component_id='Products', component_property='value'),
           Input(component_id='Month', component_property='value')])
def pie_chart(product, month):
    filtered_df = df_raw
    if product is None:
        if month is None:
            pie_df = filtered_df
            a = str(pie_df["FAULT_OBSERVED"].count())
            b = 'Modules Faults Data'
            fig = px.pie(pie_df, names='PRODUCT_NAME', title=b, labels='PRODUCT_NAME', hole=0.3)
            # fig.update_layout(margin=dict(b=10))
            fig.update_traces(hovertemplate="Product:%{label} <br>Fault_Count:%{value} <br>Percentage: %{percent}}")
            # fig.update_traces(textinfo='percent+value', insidetextfont_color='black')
            fig.add_annotation(x=0.5, y=0.5, text=a, font=dict(size=14, family='Verdana', color='black'),
                               showarrow=False)
            fig.update_layout(margin=dict(b=10), plot_bgcolor=colors['background'], paper_bgcolor=colors['background'],
                              font_color=colors['text'])
            return fig
        else:
            pie_df = filtered_df.loc[filtered_df['MONTH'] == month]
            a = str(pie_df["FAULT_OBSERVED"].count())
            b = 'Modules Faults Data for ' + month
            fig = px.pie(pie_df, names='PRODUCT_NAME', title=b, labels='PRODUCT_NAME', hole=0.3)
            # fig.update_layout(margin=dict(b=10))
            fig.update_traces(hovertemplate="Product:%{label} <br>Fault_Count:%{value} <br>Percentage: %{percent}}")
            # fig.update_traces(textinfo='percent+value', insidetextfont_color='black')
            fig.add_annotation(x=0.5, y=0.5, text=a, font=dict(size=14, family='Verdana', color='black'),
                               showarrow=False)
            fig.update_layout(margin=dict(b=10), plot_bgcolor=colors['background'], paper_bgcolor=colors['background'],
                              font_color=colors['text'])
            return fig
    else:
        specific_df = filtered_df.loc[filtered_df['PRODUCT_NAME'] == product]
        if month is None:
            pie_df = specific_df
            a = str(pie_df["FAULT_OBSERVED"].count())
            b = 'Total Failure for ' + product
        else:
            pie_df = specific_df.loc[specific_df['MONTH'] == month]
            # return the outcomes piechart for a selected month
            a = str(pie_df["FAULT_OBSERVED"].count())
            b = product + ' Failure for ' + month

    fig = px.pie(pie_df, names='FAULT_OBSERVED', title=b, labels='FAULT_OBSERVED', hole=0.3)
    # fig.update_layout(margin=dict(b=10))
    # fig.update_traces(textinfo='percent+value', textfont_size=12, insidetextfont_color='black',
    #                   hovertemplate="Fault:%{label} <br>Count:%{value} <br>Percentage: %{percent}}")
    fig.update_traces(hovertemplate="Fault:%{label} <br>Count:%{value} <br>Percentage: %{percent}}")
    fig.add_annotation(x=0.5, y=0.5, text=a, font=dict(size=14, family='Verdana', color='black'),
                       showarrow=False)
    fig.update_layout(margin=dict(b=10), plot_bgcolor=colors['background'], paper_bgcolor=colors['background'],
                      font_color=colors['text'])
    return fig


@callback(Output(component_id='pie_chart1', component_property='figure'),
          [Input(component_id='Product_f2', component_property='value'),
           Input(component_id='Month', component_property='value')])
def pie_chart1(product, month):
    filtered_df = df_raw
    if product is None:
        if month is None:
            pie_df = filtered_df
            a = str(pie_df["FAULT_OBSERVED"].count())
            b = 'Modules Faults Data'
            fig = px.pie(pie_df, names='PRODUCT_NAME', title=b, hole=0.3)
            # fig.update_layout(margin=dict(b=0))
            fig.update_layout(title_font_size=20, title_pad_b=0, title_y=0.96)
            fig.update_traces(hovertemplate="Product:%{label} <br>Fault_Count:%{value} <br>Percentage: %{percent}}",
                              insidetextfont_color='white')
            # fig.update_traces(textinfo='percent+value', insidetextfont_color='black')
            fig.add_annotation(x=0.5, y=0.5, text=a, font=dict(size=14, family='Verdana', color='white'),
                               showarrow=False)
            fig.update_layout(margin=dict(b=10), plot_bgcolor='#1f2c56', paper_bgcolor='#1f2c56',
                              font_color='white', showlegend=False)
            return fig
        else:
            pie_df = filtered_df.loc[filtered_df['MONTH'] == month]
            a = str(pie_df["FAULT_OBSERVED"].count())
            b = 'Modules Faults Data for ' + month
            fig = px.pie(pie_df, names='PRODUCT_NAME', title=b, hole=0.3)
            fig.update_layout(title_font_size=20, title_pad_b=0, title_y=0.96)
            fig.update_traces(hovertemplate="Product:%{label} <br>Fault_Count:%{value} <br>Percentage: %{percent}}",
                              insidetextfont_color='white')
            fig.add_annotation(x=0.5, y=0.5, text=a, font=dict(size=14, family='Verdana', color='white'),
                               showarrow=False)
            fig.update_layout(margin=dict(b=10), plot_bgcolor='#1f2c56', paper_bgcolor='#1f2c56',
                              font_color='white', showlegend=False)
            return fig
    else:
        specific_df = filtered_df.loc[filtered_df['PRODUCT_NAME'] == product]
        if month is None:
            pie_df = specific_df
            a = str(pie_df["FAULT_OBSERVED"].count())
            b = 'Total Failure for ' + product
        else:
            pie_df = specific_df.loc[specific_df['MONTH'] == month]
            # return the outcomes piechart for a selected month
            a = str(pie_df["FAULT_OBSERVED"].count())
            b = product + ' Failure for ' + month

    fig = px.pie(pie_df, names='FAULT_OBSERVED', title=b, hole=0.3)
    fig.update_layout(title_font_size=20, title_pad_b=0, title_y=0.96)
    fig.update_traces(hovertemplate="Fault:%{label} <br>Count:%{value} <br>Percentage: %{percent}}",
                      insidetextfont_color='white')
    fig.add_annotation(x=0.5, y=0.5, text=a, font=dict(size=14, family='Verdana', color='white'),
                       showarrow=False)
    fig.update_layout(margin=dict(b=10), plot_bgcolor='#1f2c56', paper_bgcolor='#1f2c56',
                      font_color='white', showlegend=False)
    return fig


@callback(Output(component_id='Sunburst', component_property='figure'),
          [Input(component_id='Products', component_property='value'),
           Input(component_id='Month', component_property='value')])
def sunburst_chart(product, month):
    filtered_df = df_raw
    map_1 = {'(?)': 'rgb(128, 177, 211)', 'ATS': '#00CC96', 'Initial': 'cornflowerblue', 'Burn In': 'red',
             'Testing': '#A000ff', 'Pre Initial': '#00ff4f', 'Rack testing': '#Ffe200', 'ATE': '#00CC96',
             'TESTING': '#A000ff'}
    if product is None:
        if month is None:
            d = filtered_df
        else:
            d = filtered_df.loc[filtered_df['MONTH'] == month]

    else:
        specific_df = filtered_df.loc[filtered_df['PRODUCT_NAME'] == product]
        if month is None:
            d = specific_df
        else:
            d = specific_df.loc[specific_df['MONTH'] == month]

    fig = px.sunburst(d, path=['TOTAL', 'STAGE', 'FAULT_OBSERVED', 'FAULT_CATEGORY', 'KEY_COMPONENT'],
                      maxdepth=2, title='Stage wise Fault', color='STAGE', custom_data=['STAGE'],
                      color_discrete_map=map_1)
    fig.update_traces(textinfo='label+value', textfont_size=14, insidetextfont_color='black')
    fig.update_layout(margin=dict(b=10), plot_bgcolor=colors['background'], paper_bgcolor=colors['background'],
                      font_color=colors['text'])
    fig.update_traces(hovertemplate="Stage:%{customdata} <br>label:%{label} <br>Count:%{value}<br>Parent:%{parent}")
    return fig


@callback(Output(component_id='Bar', component_property='figure'),
          [Input(component_id='Products', component_property='value'),
           Input(component_id='Month', component_property='value')])
def bar_chart(product, month):
    filtered_df = df_raw
    map_1 = {'(?)': 'rgb(128, 177, 211)', 'ATS': '#00CC96', 'Initial': 'cornflowerblue', 'Burn In': 'red',
             'Testing': '#A000ff', 'Pre Initial': '#00ff4f', 'Rack testing': '#Ffe200', 'ATE': '#00CC96',
             'TESTING': '#A000ff'}
    if product is None:
        if month is None:
            d = filtered_df
        else:
            d = filtered_df.loc[filtered_df['MONTH'] == month]
    else:
        specific_df = filtered_df.loc[filtered_df['PRODUCT_NAME'] == product]
        if month is None:
            d = specific_df
        else:
            d = specific_df.loc[specific_df['MONTH'] == month]

    bar = d.groupby(['FAULT_OBSERVED', 'STAGE'])['TOTAL'].size().reset_index()
    fig = px.bar(bar, x='TOTAL', y='FAULT_OBSERVED', title="Faults Type", color='STAGE', text='TOTAL',
                 color_discrete_map=map_1)
    fig.update_traces(textfont_size=20, textangle=0, textposition="inside", cliponaxis=False,
                      insidetextfont_color='black')
    fig.update_layout(margin=dict(b=10), plot_bgcolor=colors['background'], paper_bgcolor=colors['background'],
                      font_color=colors['text'])
    return fig


@callback(Output(component_id='Bar1', component_property='figure'),
          [Input(component_id='Product_f2', component_property='value'),
           Input(component_id='Month', component_property='value')])
def bar_chart1(product, month):
    filtered_df = df_raw
    map_1 = {'(?)': 'rgb(128, 177, 211)', 'ATS': '#00CC96', 'Initial': 'cornflowerblue', 'Burn In': 'red',
             'Testing': '#A000ff', 'Pre Initial': '#00ff4f', 'Rack testing': '#Ffe200', 'ATE': '#00CC96',
             'TESTING': '#A000ff'}
    if product is None:
        if month is None:
            d = filtered_df
        else:
            d = filtered_df.loc[filtered_df['MONTH'] == month]
    else:
        specific_df = filtered_df.loc[filtered_df['PRODUCT_NAME'] == product]
        if month is None:
            d = specific_df
        else:
            d = specific_df.loc[specific_df['MONTH'] == month]

    bar = d.groupby(['FAULT_OBSERVED', 'STAGE'])['TOTAL'].size().reset_index()
    fig = px.bar(bar, x='TOTAL', y='FAULT_OBSERVED', title="Faults Type", color='STAGE', text='TOTAL',
                 color_discrete_map=map_1)
    fig.update_layout(title_font_size=20, title_pad_b=0, title_y=0.96)
    fig.update_traces(textfont_size=14, textangle=0, textposition="inside", cliponaxis=False,
                      insidetextfont_color='white')
    fig.update_layout(margin=dict(b=10), plot_bgcolor='#1f2c56', paper_bgcolor='#1f2c56',
                      font_color='white')
    return fig


@callback(Output(component_id='List of Faults', component_property='options'),
          [Input(component_id='List of Faults', component_property='search_value'),
           Input(component_id='Products', component_property='value'),
           Input(component_id='Month', component_property='value')])
def dropdown_faults(product, month):
    filtered_df = df_raw
    if product is None:
        if month is None:
            d = filtered_df
        else:
            d = filtered_df.loc[filtered_df['MONTH'] == month]
            # return [{"label": i, "value": i} for i in fault[month]]
    else:
        specific_df = filtered_df.loc[filtered_df['PRODUCT_NAME'] == product]
        if month is None:
            d = specific_df
        else:
            d = specific_df.loc[specific_df['MONTH'] == month]

    return [{"label": j, "value": j} for j in d['FAULT_OBSERVED'].unique()]


@callback(Output(component_id='Faults_list', component_property='children'),
          [Input(component_id='List of Faults', component_property='value'),
           Input(component_id='Products', component_property='value'),
           Input(component_id='Month', component_property='value')])
def display_table(dropdown_value, product, month):
    filtered = df
    if product is None:
        if dropdown_value is None:
            if month is None:
                a = filtered
            else:
                a = filtered.loc[filtered['MONTH'] == month]
        else:
            specific = filtered.loc[filtered['FAULT_OBSERVED'] == dropdown_value]
            if month is None:
                a = specific
            else:
                a = specific.loc[specific['MONTH'] == month]

    else:
        specific_df = filtered.loc[filtered['PRODUCT_NAME'] == product]
        if dropdown_value is None:
            if month is None:
                a = specific_df
            else:
                a = specific_df.loc[specific_df['MONTH'] == month]
        else:
            specific = specific_df.loc[specific_df['FAULT_OBSERVED'] == dropdown_value]
            if month is None:
                a = specific
            else:
                a = specific.loc[specific['MONTH'] == month]

    return html.Div([dash_table.DataTable(data=a.to_dict('records'),
                                          columns=[{'name': j, 'id': j} for j in a.columns],
                                          editable=True,
                                          filter_action="native",
                                          sort_action="native",
                                          sort_mode='multi',
                                          fixed_rows={'headers': True},
                                          style_header={'backgroundColor': "rgb(50, 50, 50)",
                                                        'color': 'white',
                                                        'fontWeight': 'bold',
                                                        'textAlign': 'center', },
                                          # style_header={'backgroundColor': "#FFD700",
                                          #               'fontWeight': 'bold',
                                          #               'textAlign': 'center', },
                                          style_table={'height': 420, 'overflowX': 'scroll'},
                                          style_cell={'minWidth': '130px', 'width': '140px',
                                                      'maxWidth': '130px', 'whiteSpace': 'normal',
                                                      'textAlign': 'center',
                                                      'backgroundColor': 'white', 'color': 'black'}, ),
                     html.Hr()
                     ])


@callback(Output(component_id='Product_f2', component_property='options'),
          [Input(component_id='Product_f2', component_property='search_value'),
           Input(component_id='Month', component_property='value')])
def dropdown_faults_f2(search_value, month):
    modules = ['SMR', 'CHARGER', 'M1000', 'M2000', 'WCBMS']
    filtered_df = df_raw.loc[df_raw['PRODUCT_NAME'].isin(modules)]
    # filtered_df = df_raw
    if month is None:
        d = filtered_df
    else:
        d = filtered_df.loc[filtered_df['MONTH'] == month]
    return [{"label": j, "value": j}for j in d['PRODUCT_NAME'].unique()]


@callback(Output(component_id='stages', component_property='options'),
          [Input(component_id='stages', component_property='search_value'),
           Input(component_id='Product_f2', component_property='value')])
def dropdown_stages(search_value, product):
    filtered_df = df_raw.sort_values(by=['STAGE'], ascending=False)
    if product is None:
        d = filtered_df
    else:
        d = filtered_df.loc[filtered_df['PRODUCT_NAME'] == product]

    return [{"label": j, "value": j} for j in d['STAGE'].unique()]


@callback(
    Output('stages', 'value'),
    [Input('stages', 'options'),
     Input('Product_f2', 'value')])
def set_stages_value(available_options, product):
    if product is None:
        return None
    else:
        return available_options[0]['value']
# def logo():
#     return html.Img(src=app.get_asset_url('logo.png'))


@callback(
    Output('Tested', 'figure'),
    [Input('stages', 'value'),
     Input('Product_f2', 'value')])
def update_confirmed(stages, product):
    smr = df_smr_filter
    mcm = df_mcm_filter
    if stages is not None:
        a = stages.upper().replace(" ", "-")
        b = a + '_TEST_QUANTITY'
        if (product == 'SMR') or (product == 'CHARGER'):
            value = smr[b].loc[product]
        else:
            value = mcm[b].loc[product]

        value_confirmed = value
    else:
        value_confirmed = 0

    return {
        'data': [go.Indicator(
            mode='number',
            value=value_confirmed,
            # delta={'reference': delta_confirmed,
            #        'position': 'right',
            #        'valueformat': ',g',
            #        'relative': False,
            #
            #        'font': {'size': 15}},
            number={'font': {'size': 20}, },
            domain={'y': [0, 1], 'x': [0, 1]})],
        'layout': go.Layout(
                title={'text': 'Tested',
                       'y': 1,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'},
                font=dict(color='orange'),
                paper_bgcolor='#1f2c56',
                plot_bgcolor='#1f2c56',
                height=50
                ), }


@callback(
    Output('Pass1', 'figure'),
    [Input('stages', 'value'),
     Input('Product_f2', 'value')])
def update_confirmed(stages, product):
    smr = df_smr_filter
    mcm = df_mcm_filter
    if stages is not None:
        a = stages.upper().replace(" ", "-")
        b = a + '_PASS_QUANTITY'
        if (product == 'SMR') or (product == 'CHARGER'):
            value = smr[b].loc[product]
        else:
            value = mcm[b].loc[product]

        value_confirmed = value
    else:
        value_confirmed = 0

    return {
        'data': [go.Indicator(
            mode='number',
            value=value_confirmed,
            # delta={'reference': delta_confirmed,
            #        'position': 'right',
            #        'valueformat': ',g',
            #        'relative': False,
            #
            #        'font': {'size': 15}},
            number={'font': {'size': 20}, },
            domain={'y': [0, 1], 'x': [0, 1]})],
        'layout': go.Layout(
                title={'text': 'Pass',
                       'y': 1,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'},
                font=dict(color='green'),
                paper_bgcolor='#1f2c56',
                plot_bgcolor='#1f2c56',
                height=50
                ), }


@callback(
    Output('Fail', 'figure'),
    [Input('stages', 'value'),
     Input('Product_f2', 'value')])
def update_confirmed(stages, product):
    smr = df_smr_filter
    mcm = df_mcm_filter
    if stages is not None:
        a = stages.upper().replace(" ", "-")
        b = a + '_FAIL_QUANTITY'
        if (product == 'SMR') or (product == 'CHARGER'):
            value = smr[b].loc[product]
        else:
            value = mcm[b].loc[product]

        value_confirmed = value
    else:
        value_confirmed = 0
    return {
        'data': [go.Indicator(
            mode='number',
            value=value_confirmed,
            # delta={'reference': delta_confirmed,
            #        'position': 'right',
            #        'valueformat': ',g',
            #        'relative': False,
            #
            #        'font': {'size': 15}},
            number={'font': {'size': 20}, },
            domain={'y': [0, 1], 'x': [0, 1]})],
        'layout': go.Layout(
                title={'text': 'Fail',
                       'y': 1,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'},
                font=dict(color='#dd1e35'),
                paper_bgcolor='#1f2c56',
                plot_bgcolor='#1f2c56',
                height=50
                ), }


@callback(
    Output('%Fail', 'figure'),
    [Input('stages', 'value'),
     Input('Product_f2', 'value')])
def update_confirmed(stages, product):
    smr = df_smr_filter
    mcm = df_mcm_filter
    if stages is not None:
        a = stages.upper().replace(" ", "-")
        b = a + '_FAIL_QUANTITY'
        c = a + '_TEST_QUANTITY'
        if (product == 'SMR') or (product == 'CHARGER'):
            fail = smr[b].loc[product]
            tested = smr[c].loc[product]
        else:
            fail = mcm[b].loc[product]
            tested = mcm[c].loc[product]

        value_confirmed = (round((fail/tested)*100, 1))
    else:
        value_confirmed = 0
    return {
        'data': [go.Indicator(
            mode='number',
            value=value_confirmed,
            # delta={'reference': delta_confirmed,
            #        'position': 'right',
            #        'valueformat': ',g',
            #        'relative': False,
            #
            #        'font': {'size': 15}},
            number={'font': {'size': 20}, },
            domain={'y': [0, 1], 'x': [0, 1]})],
        'layout': go.Layout(
                title={'text': '%Fail',
                       'y': 1,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'},
                font=dict(color='#e55467'),
                paper_bgcolor='#1f2c56',
                plot_bgcolor='#1f2c56',
                height=50
                ), }


@callback(
    Output(component_id='tested_value_f2', component_property='children'),
    [Input(component_id='Product_f2', component_property='value'),
     Input(component_id='Month', component_property='value')])
def test_count1(product, month):
    total = card_product_total  # for total
    month_wise = card_month  # month vise card
    # part_code_wise = card_part_code_month  # for part code data
    # tested, pass_v, fail = compute_info(Total, product)
    if product is None:
        if month is None:
            return f"{total['TEST QUANTITY'].loc['TOTAL']:,.0f}"
        else:
            # need to add month column
            a = month_wise.loc[month_wise['MONTH'] == month]['TEST QUANTITY'].sum()
            return a
    else:
        if month is None:
            return f"{total['TEST QUANTITY'].loc[product]:,.0f}"
        else:
            # need to add month column
            a = month_wise.loc[month_wise['MONTH'] == month]
            return f"{a['TEST QUANTITY'].loc[product]:,.0f}"


@callback(
    Output(component_id='pass_value_f2', component_property='children'),
    [Input(component_id='Product_f2', component_property='value'),
     Input(component_id='Month', component_property='value')])
def pass_count1(product, month):
    total = card_product_total  # for total
    month_wise = card_month  # month vise card
    # part_code_wise = card_part_code_month  # for part code data
    if product is None:
        if month is None:
            return f"{total['PASS QUANTITY'].loc['TOTAL']:,.0f}"
        else:
            # need to add month column
            a = month_wise.loc[month_wise['MONTH'] == month]['PASS QUANTITY'].sum()
            return a
    else:
        if month is None:
            return f"{total['PASS QUANTITY'].loc[product]:,.0f}"
        else:
            # need to add month column
            a = month_wise.loc[month_wise['MONTH'] == month]
            return f"{a['PASS QUANTITY'].loc[product]:,.0f}"


@callback(
    Output(component_id='fail_value_f2', component_property='children'),
    [Input(component_id='Product_f2', component_property='value'),
     Input(component_id='Month', component_property='value')])
def fail_count1(product, month):
    total = card_product_total  # for total
    month_wise = card_month  # month vise card
    # part_code_wise = card_part_code_month  # for part code data
    if product is None:
        if month is None:
            return f"{total['REJECT QUANTITY'].loc['TOTAL']:,.0f}"
        else:
            # need to add month column
            a = month_wise.loc[month_wise['MONTH'] == month]['REJECT QUANTITY'].sum()
            return a
    else:
        if month is None:
            return f"{total['REJECT QUANTITY'].loc[product]:,.0f}"
        else:
            # need to add month column
            a = month_wise.loc[month_wise['MONTH'] == month]
            return f"{a['REJECT QUANTITY'].loc[product]:,.0f}"


@callback(
    Output(component_id='fty_value_f2', component_property='children'),
    [Input(component_id='Product_f2', component_property='value'),
     Input(component_id='Month', component_property='value')])
def fty_count1(product, month):
    total = card_product_total  # for total
    month_wise = card_month  # month vise card
    # part_code_wise = card_part_code_month  # for part code data
    if product is None:
        if month is None:
            # a = str(round(((month_wise['PASS QUANTITY'].sum() / Total['TEST QUANTITY'].sum()) * 100), 1)) + '%'
            a = str(round((total['FTY(%)'].loc['TOTAL']*100), 1)) + '%'
            return a
        else:
            # need to add month column
            a = month_wise.loc[month_wise['MONTH'] == month]['TEST QUANTITY'].sum()
            b = month_wise.loc[month_wise['MONTH'] == month]['PASS QUANTITY'].sum()
            c = str(round(((b/a)*100), 1)) + '%'
            return c
    else:
        if month is None:
            a = str(round(((total['PASS QUANTITY'].loc[product] / total['TEST QUANTITY'].loc[product])*100), 1)) + '%'
            return a
        else:
            # need to add month column
            d = month_wise.loc[month_wise['MONTH'] == month]
            a = str(round((((d['PASS QUANTITY'].loc[product]) / (d['TEST QUANTITY'].loc[product]))*100), 1)) + '%'
            return a
