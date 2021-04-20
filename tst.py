# import dash
# import dash_table
# import pandas as pd
# import dash_core_components as dcc
# from dash.dependencies import Output, Input, State
# import dash_html_components as html
# import dash_bootstrap_components as dbc
#
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
#
# df1 = pd.read_csv('C:\\Users\\kbc\\PycharmProjects\\Last\\DatabaseProject\\data\\BIST 30 Historical Data.csv')
#
# app.layout = html.Div([
#
#                      dcc.RadioItems(
#                                     id='strategy-type',
#                                     options=[
#                                         {'label': 'Price', 'value': 'Price'},
#                                         {'label': 'Open', 'value': 'Open'},
#                                         {'label': 'High', 'value': 'High'},
#                                     ],
#                                     value='Price'
#                                 ),
#                     dcc.Dropdown(
#                         id='strategy',
#                         options=[
#                             {'label': 'BIST 30', 'value': 'BIST 30'},
#                             {'label': 'BIST 100', 'value': 'BIST 100'},
#                             {'label': 'S&P 500', 'value': 'S&P 500'},
#                             {'label': 'Brent', 'value': 'Brent'},
#
#                         ], value='BIST 30', placeholder='Select instrument...'),
#
#                     # dcc.Input(id='commission-input', type='number', placeholder='Commission', min=0, value=2),
#
#                     html.Button('Bring data', id='bring-data-button', n_clicks=0),
#
#                     html.Div(id='place1'),
#                     html.Div(id='place2')
#      ])
# @app.callback(
#     [Output(component_id='place1', component_property='children'),
#     Output(component_id='place2', component_property='children')],
#     Input(component_id='bring-data-button', component_property='n_clicks'),
#     [State(component_id='strategy-type', component_property='value'),
#      State(component_id='strategy', component_property='value')]
# )
#
# def save(n_clicks1, value1, value2):
#     if value2 == 'BIST 30':
#         df = pd.read_csv('C:\\Users\\kbc\\PycharmProjects\\Last\\DatabaseProject\\data\\BIST 30 Historical Data.csv')
#     elif value2 == 'BIST 100':
#         df = pd.read_csv('/Users/hackyourfuture/Desktop/Tez için indirilen veriler/BIST 100 Historical Data.csv')
#     elif value2 == 'S&P 500':
#         df = pd.read_csv('/Users/hackyourfuture/Desktop/Tez için indirilen veriler/S&P 500 Historical Data.csv')
#     elif value2 == 'Brent':
#         df = pd.read_csv(
#             '/Users/hackyourfuture/Desktop/Tez için indirilen veriler/Brent Oil Futures Historical Data.csv')
#
#     if value1 == 'Price':
#         df1 = df.Price
#     elif value1 == 'Open':
#         df1 = df.Open
#     elif value1 == 'High':
#         df1 = df.High
#
#     if n_clicks1 == 0:
#         return [None, dcc.Graph(
#                         id='graph',
#                         figure={
#                             'data': [
#                                 {'x': df.Date, 'y': df1, 'type': 'line', 'color': 'blue'},
#                                 # {'x': df.Date, 'y': df_kkk['MA(19)'], 'type': 'line', 'color':'red', 'name': '19d-MA'}
#                             ],
#                             'layout': {
#                                 # 'title': stock,
#                                 'height': 400,
#                             }
#                         }
#                     )]
#
#     else:
#
#         return [dash_table.DataTable(
#                         id='table_ratio',
#                         data=df.to_dict('records'),
#                         columns=[{'id': c, 'name': c} for c in df.columns],
#                         style_cell={'textAlign': 'center', 'width': '100px', 'minWidth': '100px', 'maxWidth': '100px'},
#                         fixed_rows={'headers': True, 'data': 0},
#                         style_header={'fontWeight': 'bold'},
#                         style_table={'overflowX': 'auto'},
#                         editable=True
#                     ),
#
#                 dcc.Graph(
#                         id='graph',
#                         figure={
#                             'data': [
#                                 {'x': df.Date, 'y': df1, 'type': 'line', 'color': 'blue'},
#                                 # {'x': df.Date, 'y': df_kkk['MA(19)'], 'type': 'line', 'color':'red', 'name': '19d-MA'}
#                             ],
#                             'layout': {
#                                 # 'title': stock,
#                                 'height': 400,
#                             }
#                         }
#                     )]
#
#
# if __name__ == '__main__':
#     app.run_server(debug=True)
import psycopg2
import pandas.io.sql as sqlio
#
con = psycopg2.connect("dbname=dvdrental user=postgres password=1234")
cur = con.cursor()
cur.execute("delete from film where film_id=%s", ('22'))
sql = 'select film_id, title, description, length from film'
dat = sqlio.read_sql_query(sql, con)
cur.close()
con.commit()
con.close()
