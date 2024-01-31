import dash
from dash import Dash, html, Input, Output, ctx, callback, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import mysql.connector
import plotly.graph_objects as go
from tkinter import messagebox, ttk
from tkinter import *
from PIL import Image
import intento

external_stylesheets = ['style.css',dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Contenido de la primera página
Flujo_pg = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Flujo de las transacciones del IVR", className="BienvenidaLabel"), width=20),
    ]),
    
    
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='snake-chart',style={'height': '500px'}),
            style={'height': '500px'}  # Establece la altura aquí
        ),
    ])# Container to display result
], className="mt-4")

# Contenido de la segunda página
Estadisticas_pg = dbc.Container([
    html.H1("Pagina principal", className="BienvenidaLabel"),
    # Agrega el contenido específico de la segunda página aquí
], className="mt-4")

Acercade_pg = dbc.Container([
    html.H1("Acerca de - Contenido aquí", className="BienvenidaLabel"),
    # Agrega el contenido específico de la tercera página aquí
], className="mt-4")

Ayuda_pg = dbc.Container([
    html.H1("Ayuda - Contenido aquí", className="BienvenidaLabel"),
    # Agrega el contenido específico de la tercera página aquí
], className="mt-4")

Contacto_pg = dbc.Container([
    html.H1("Contacto - Contenido aquí", className="BienvenidaLabel"),
    # Agrega el contenido específico de la tercera página aquí
], className="mt-4")

# Contenido de la tercera página

# Definición del menú
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Acerca de:", href="/Acercade")),
        dbc.NavItem(dbc.NavLink("Ayuda", href="/Ayuda")),
        dbc.NavItem(dbc.NavLink("Contacto", href="/Contacto")),
        
    ],
    brand="Bienvenid@ a IVRAnalytics Pro by CSS",
    brand_href="/",
    color="#198754",
    dark=True,
    brand_style={'font-size': '25px', 'font-weight': 'bold'}
)

accordion = html.Div(
    dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                dbc.NavItem(dbc.NavLink("Estadisticas", href="/",style={'display': 'block','text-aling':'center','margin':'5px','font-size': '18px',
                'cursor':'pointer',})),
                html.Hr(className='vertical-divider'),
                dbc.NavItem(dbc.NavLink("Flujo", href="/Flujo",style={'display': 'block','text-aling':'center','margin':'5px','font-size': '18px',
                'cursor':'pointer',})),
                html.Hr(className='vertical-divider'),
                    
                ],
                title="Paginas",style={'width':'100%','justify-content':'center'}
    
            ),
            dbc.AccordionItem(
                [
                    html.Label("Seleccione cual IVR desea generar:", className="labelCombo",style={'display': 'block','text-aling':'center','margin':'5px','font-size': '15px'}),
                    dcc.Dropdown(
                        id='combo-dropdown',
                        options=[
                            {'label': '', 'value': ''},
                            {'label': 'Coomeva-CAC', 'value': 'Coomeva-CAC'},
                            {'label': 'Coomeva-SyS', 'value': 'Coomeva-SyS'},
                            {'label': 'MP Validacion Productos', 'value': 'MP Validacion Productos'}
                        ],
                        className="Combo",style={'display': 'block','text-aling':'center','margin':'10px','font-size': '15px'}
                    ),
                    html.Hr(className='vertical-divider'),
                    html.Label("Fecha Inicio: (AAAA-MM-DDD)", className="LFechaInicio",style={'display': 'block'}),
                    dcc.DatePickerSingle(
                        id='fecha-inicio-picker',
                        display_format='YYYY-MM-DD',
                        className="FechaInicio",
                        style={'display': 'block','text-aling':'center','margin':'10px','font-size': '15px','width':'90%',  'justify-content': 'center'}
                    ),
                    html.Hr(className='vertical-divider'),
                    html.Label("Fecha Fin: (AAAA-MM-DD)", className="LFechaFin",style={'display': 'block','text-aling':'center','margin':'10px','font-size': '15px'}),
                    dcc.DatePickerSingle(
                        id='fecha-fin-picker',
                        display_format='YYYY-MM-DD',
                        className="FechaFin",style={'display': 'block','text-aling':'center','margin':'10px','font-size': '15px',  'justify-content': 'center'}
                    ),
                    html.Hr(className='vertical-divider'),
                    html.Button('Generar', id='analyze-button', n_clicks=0, className="AnalyzeButton",style={'display': 'block','justify-content': 'center','text-aling':'center',
                        'margin':'10px','font-size': '15px','background-color': '#557C55',
                'color': '#fff',
                'border': 'none',
                'border-radius': '20px',
                'cursor':'pointer',
                'width':'90%',
                'height':'50px'}),

                ],
                title="Filtros",

          ),
        ],
        start_collapsed=False,style={'width':'100%','justify-content':'center'}
    ),
        style={'width':'80%'})

# Layout principal con el contenido de la página actual
app.layout = html.Div([
    dcc.ConfirmDialog(
        id='confirm-danger',
        message='Danger danger! Are you sure you want to continue?',
    ),
    dcc.Location(id='url', refresh=False),
    navbar,
    dbc.Row([
        dbc.Col(accordion, width=3,style={
  'display': 'flex',
  'justify-content': 'center'}),  # Barra lateral que ocupa 3 columnas
        dbc.Col(html.Div(id='page-content'), width=9),  # Contenido que ocupa 9 columnas
    ]),
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])

def display_page(pathname):
    if pathname == '/Flujo':
        return Flujo_pg

    elif pathname == '/Acercade':
        return Acercade_pg
    elif pathname == '/Ayuda':
        return Ayuda_pg
    elif pathname == '/Contacto':
        return Contacto_pg
    else:
        return Estadisticas_pg


@app.callback(
    [Output('output-container', 'children'),
     Output('confirm-danger', 'displayed'),
     Output('snake-chart', 'figure')],
    [Input('analyze-button', 'n_clicks'),
    Input('combo-dropdown','value'),
    Input('fecha-inicio-picker','date'),
    Input('fecha-fin-picker','date')
    ]
)
def print_hello_world_callback(n_clicks, combo, inicio, fin):
    # Check if the button was clicked
    if (combo==None or inicio==None or fin==None) and 'analyze-button' == ctx.triggered_id:

        return None, True, None   # Puedes mostrar el resultado en tu diseño si es necesario
    if 'analyze-button' == ctx.triggered_id:
        try:
            print("entra")
            #CONEXION MYSQL 
            conexion= mysql.connector.connect(user='repocct',password='r3p0cc7', host='10.32.4.251', 
                database='mydb', port='3306')


            cursor= conexion.cursor()

            #SENTENCIA SQL PARA IVR COOMEVA
            if combo=="Coomeva-CAC":
                sql= f"SELECT * FROM mydb.trackings WHERE start BETWEEN '{inicio} 00:00:00' AND '{fin} 23:59:59'AND detail LIKE '%IVR_OPERATIVO_PILOTO%' AND detail LIKE '%Opc_1%' "
                sql2=f"SELECT * FROM mydb.trackings WHERE start BETWEEN '{inicio} 00:00:00' AND '{fin} 23:59:59'AND detail LIKE '%Menu_Principal_CAC%' AND detail LIKE '%Opcion1_CAC%'"
            elif combo=="MP Validacion Productos":
                sql= f"SELECT * FROM mydb.trackings WHERE start BETWEEN '{inicio} 00:00:00' AND '{fin} 23:59:59'AND detail LIKE '%IVR_Medicina_Prepagada%'"
                sql2=""
                
            else:
                sql= f"SELECT * FROM mydb.trackings WHERE start BETWEEN '{inicio} 00:00:00' AND '{fin} 23:59:59' AND detail LIKE '%Menu_Principal_SyS%'"
                sql2=""
        except:
            print("no pudo")

        figura=intento.transformacion(sql,sql2,conexion, inicio, fin, combo)
        print(figura)
        return f"{conexion} // {sql}", False, figura
    else:     
        return None, False, ""

if __name__ == '__main__':
    app.run_server(debug=False,dev_tools_ui=False,dev_tools_props_check=False)