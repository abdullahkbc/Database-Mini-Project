import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import psycopg2
import pandas.io.sql as sqlio

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

##### Database queryleri ve sonuclari

## Dashboard:  Ed Chase number of movies
con=psycopg2.connect("dbname=dvdrental user=postgres password=1234")
cur=con.cursor()
cur.execute("select count(film_id) from film_actor where actor_id = (select actor_id from actor where first_name='Ed' and last_name='Chase')")
a=cur.fetchall()
con.close()

## Dashboard:  active customer number
con=psycopg2.connect("dbname=dvdrental user=postgres password=1234")
cur=con.cursor()
cur.execute("select count(*) from customer where active=1")
b=cur.fetchall()
con.close()

## Dashboard: movies in english
con=psycopg2.connect("dbname=dvdrental user=postgres password=1234")
cur=con.cursor()
cur.execute("select count(*) from film where language_id=1")
c=cur.fetchall()
con.close()

## movies longer than 120 minutes
con=psycopg2.connect("dbname=dvdrental user=postgres password=1234")
cur=con.cursor()
cur.execute("select count(*) from film where length>120")
d=cur.fetchall()
con.close()

## table language and number of movies corresponding to them
# con=psycopg2.connect("dbname=dvdrental user=postgres password=1234")
# cur=con.cursor()
# cur.execute("select name from language")
# e=cur.fetchall()
# con.close()


con=psycopg2.connect("dbname=dvdrental user=postgres password=1234")
cur=con.cursor()
cur.execute("select count(*), language.name from film inner join language on language.language_id = film.language_id group by name")
e1=cur.fetchall()
con.close()
#k=[]
# for i in range(6):
#     con = psycopg2.connect("dbname=dvdrental user=postgres password=1234")
#     cur = con.cursor()
#     cur.execute("select count(*) from film where language_id={}".format(i))
#     h = cur.fetchall()
#     k.append(h[0][0])
#     con.close()

## Donut type chart: Percentage of movies action and other types
con=psycopg2.connect("dbname=dvdrental user=postgres password=1234")
cur=con.cursor()
cur.execute("select count(*) from film where film_id in (select film_id from film_category where category_id=1)")
l=cur.fetchall()
con.close()

con=psycopg2.connect("dbname=dvdrental user=postgres password=1234")
cur=con.cursor()
cur.execute("select count(*) from film where film_id in (select film_id from film_category where category_id!=1)")
n=cur.fetchall()
con.close()

perc_actions=(l[0][0]/(l[0][0]+n[0][0]))
perc_others=(n[0][0]/(l[0][0]+n[0][0]))

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Use the hovertext kw argument for hover text
fig = go.Figure(data=[go.Bar( x= [e1[0][1], e1[1][1],e1[2][1],e1[3][1],e1[4][1],e1[5][1]], y=[e1[0][0],e1[1][0],e1[2][0],e1[3][0],e1[4][0],e1[5][0]]  )])
# Customize aspect
fig.update_traces(marker_color='rgb(97, 185, 231)', marker_line_color='rgb(97, 185, 231)')
fig.update_layout(title_text='Num of movies for diff languages',
                  height= 350,
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor ='rgba(0,0,0,0)',
                  bargap=0.45,
                  font_color="white",
                  yaxis = dict(
                        tickfont_size=12,
                    ),
                  xaxis = dict(
                        tickfont_size=12,
                    ),
                  margin=dict(l=50, r=0, b=100, t=100)
                  )
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='DarkBlue')

# Use `hole` to create a donut-like pie chart
fig2 = go.Figure(data=[go.Pie(labels=['Action Movies','Other Movies'], values=[perc_actions,perc_others], hole=.8)])
fig2.update_traces(marker=dict(colors=['rgb(221, 81, 121)','rgb(114, 221, 193)']))
fig2.update_layout(title_text='Percentage of Action Movies',
                  height= 350,
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor ='rgba(0,0,0,0)',
                  font_color="white",
                  # margin=dict(l=50, r=50, b=100, t=100)
                  )

app.layout = html.Div([
                dbc.Row(
                    dbc.Col([
                        dbc.Row(
                            dbc.Col([
                                dbc.NavbarSimple(
                                    children=[
                                        dbc.NavItem(dbc.NavLink("ACTOR", href="/actor")),
                                        dbc.NavItem(dbc.NavLink("ADDRESS", href="/address")),
                                        dbc.NavItem(dbc.NavLink("CATEGORY", href="/category")),
                                        dbc.NavItem(dbc.NavLink("COUNTRY", href="/city")),
                                        dbc.NavItem(dbc.NavLink("CUSTOMER", href="/customer")),
                                        dbc.NavItem(dbc.NavLink("INVENTORY", href="/inventory")),
                                        dbc.NavItem(dbc.NavLink("LANGUAGE", href="/language")),
                                        dbc.NavItem(dbc.NavLink("PAYMENT", href="/payment")),
                                        dbc.NavItem(dbc.NavLink("RENTAL", href="/rental")),
                                    ],
                                    brand="Rental Co.",
                                    brand_href="/home",
                                    id='nav',
                                ),
                                html.P("Abdullah's Dashboard", id='name'),
                            ]),
                        ),

                        dbc.Row([
                            dbc.Col([
                                dbc.Row([
                                    dbc.Col([
                                        html.P('Num.of Movies (Ed Chase)'),
                                        html.H3(a[0][0])
                                    ], width=4),
                                    dbc.Col([
                                        html.P('Customer Number'),
                                        html.H3(b[0][0])
                                    ], width=4)
                                ],id='first', justify='center'),
                                dbc.Row([
                                    dbc.Col([
                                        html.P('Movies in English'),
                                        html.H3(c[0][0])
                                    ], width=4),
                                    dbc.Col([
                                        html.P('Movies longer than 120 min'),
                                        html.H3(d[0][0])
                                    ], width=4)
                                ],id='second',justify='center')
                            ],id='first-middle', width=4),
                            dbc.Col(
                                dcc.Graph(
                                    id ='graph',
                                    figure = fig
                                ),width=4, id='second-middle'
                            ),
                            dbc.Col(
                                dcc.Graph(
                                    id='graph2',
                                    figure= fig2,
                                ), width=4, id='third-middle')
                        ],id='graphs'),

                        # dbc.Row([
                        #     dbc.Col(dbc.Input(id="input-1", placeholder="id", type="number")),
                        #     dbc.Col(dbc.Input(id="input-2", placeholder="Name", type="text")),
                        #     dbc.Col(dbc.Input(id="input-3", placeholder="Surname", type="text")),
                        #     dbc.Col(dbc.Input(id="input-4", placeholder="Profession", type="text")),
                        #     ], className="mt-3", justify='center'),

                        dbc.Row(
                            dbc.Col(id='table', width=12
                            ), className="mt-3", justify='center'
                        ),

                        dbc.Row(
                            dbc.Col([
                                dcc.Input(id='film_id', type='number'),
                                dcc.Input(id='title', type='text'),
                                dcc.Input(id='description', type='text'),
                                dcc.Input(id='length', type='number'),
                                html.Button("Show",  id='show', n_clicks=0),
                                html.Button("Add", id='add', n_clicks=0),
                                html.Button("Update", id='update', n_clicks=0),
                                html.Button("Delete", id='delete', n_clicks=0),
                                html.Div(id='place')
                            ]), className="mt-3", justify='center'
                        ),

                    ]), id='middle'
                ),
            ], id='main-page')

## Callback fonksiyonu
@app.callback(
    Output(component_id='place', component_property='children'),
    [Input(component_id='show', component_property='n_clicks'),
    Input(component_id='add', component_property='n_clicks'),
    Input(component_id='delete', component_property='n_clicks'),
    Input(component_id='update', component_property='n_clicks')],
    [State(component_id='film_id', component_property='value'),
    State(component_id='title', component_property='value'),
    State(component_id='description', component_property='value'),
    State(component_id='length', component_property='value')],
)
def save (n_clicks1,n_clicks2, n_clicks3, n_clicks4,value1, value2, value3, value4):
    ctx=dash.callback_context
    pie=ctx.triggered[0]['prop_id'].split('.')[0]
    if pie=='show':
        con = psycopg2.connect("dbname=dvdrental user=postgres password=1234")
        # con.execute("select film_id, title, description, length from film")
        dat = sqlio.read_sql_query("select film_id, title, description, length from film order by title",con)
        con.close()
        return dash_table.DataTable(
            id='table_ratio',
            data=dat.to_dict('records'),
            columns=[{'id':c,'name':c} for c in dat.columns],
            style_cell={'textAlign':'center','width':'100px','minWidth':'100px','maxWidth':'100px'},
            fixed_rows={'headers':True, 'data':0},
            style_header={'fontWeight':'bold'},
            style_table={'overflowX':'auto'},
            editable=True
        )
    elif pie=='add':
        con = psycopg2.connect("dbname=dvdrental user=postgres password=1234")
        cur=con.cursor()
        cur.execute("insert into film(film_id, title, description, length) values(%s,%s,%s,%s)", (value1, value2, value3, value4))
        sql='select film_id, title, description, length from film'
        dat=sqlio.read_sql_query(sql,con)
        cur.close()
        con.commit()
        con.close()
        return dash_table.DataTable(
            id='table_ratio',
            data=dat.to_dict('records'),
            columns=[{'id':c,'name':c} for c in dat.columns],
            style_cell={'textAlign':'center','width':'100px','minWidth':'100px','maxWidth':'100px'},
            fixed_rows={'headers':True, 'data':0},
            style_header={'fontWeight':'bold'},
            style_table={'overflowX':'auto'},
            editable=True
        )
    elif pie=='delete':
        con = psycopg2.connect("dbname=dvdrental user=postgres password=1234")
        cur=con.cursor()
        cur.execute("delete from film where film_id=%s",(value1) )
        sql='select film_id, title, description, length from film'
        dat=sqlio.read_sql_query(sql,con)
        cur.close()
        con.commit()
        con.close()
        return dash_table.DataTable(
            id='table_ratio',
            data=dat.to_dict('records'),
            columns=[{'id':c,'name':c} for c in dat.columns],
            style_cell={'textAlign':'center','width':'100px','minWidth':'100px','maxWidth':'100px'},
            fixed_rows={'headers':True, 'data':0},
            style_header={'fontWeight':'bold'},
            style_table={'overflowX':'auto'},
            editable=True
        )
    elif pie=='update':
        con = psycopg2.connect("dbname=dvdrental user=postgres password=1234")
        cur=con.cursor()
        cur.execute("update film set length=%s where film_id=%s",(value4, value1) )
        sql='select film_id, title, description, length from film'
        dat=sqlio.read_sql_query(sql,con)
        cur.close()
        con.commit()
        con.close()
        return dash_table.DataTable(
            id='table_ratio',
            data=dat.to_dict('records'),
            columns=[{'id':c,'name':c} for c in dat.columns],
            style_cell={'textAlign':'center','width':'100px','minWidth':'100px','maxWidth':'100px'},
            fixed_rows={'headers':True, 'data':0},
            style_header={'fontWeight':'bold'},
            style_table={'overflowX':'auto'},
            editable=True
        )

if __name__ == '__main__':
    app.run_server(debug=True)