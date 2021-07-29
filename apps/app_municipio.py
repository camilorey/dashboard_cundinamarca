import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

#from helpers.barra_navegacion_factory import crear_barra_navegacion
#Vamos a usar clases que yo he construido para hacer controladores
from helpers.controladores_factory import DataFrame_Factory
#importamos la app base para tener todo en el mismo ambiente
from app import app,crear_barra_navegacion

#vamos a crear una caja de control desde un archivo
df = pd.read_excel("https://github.com/camilorey/datasets_ficti/blob/main/informacionClientes.xlsx?raw=true")
cols_dict = {'estrato':['DROPDOWN'],
             'sexo':['TICKS'],
             'edad':['SLIDER',5,4],
             'saldo':['SLIDER',1000000,6]}
otra_caja = DataFrame_Factory("Controladores de Archivo",
                              "controladores-archivo-id",
                              df,
                              cols_dict)
otra_caja.crear_componentes()
#otra_caja.crear_callbacks_basicos(app)

#vamos a crear la barra de navegación
barra_nav = crear_barra_navegacion("Vista Municipios")

#ahora ponemos el contenedor donde va a ir el resto de las cosas
dashboardContainer = html.Div([html.H1("Aquí va a ir el dashboard"),
                               dbc.Container([
                                    dbc.Row([dbc.Col(dcc.Graph(id='figura-11'),width=8),
                                             dbc.Col(dcc.Graph(id='figura-12'),width=4)],
                                            no_gutters=True),

                                    dbc.Row([dbc.Col(dcc.Graph(id='figura-21'),width=4),
                                             dbc.Col(dcc.Graph(id='figura-22'),width=4),
                                             dbc.Col(dcc.Graph(id='figura-23'),width=4)],
                                            no_gutters=True),

                                    dbc.Row([dbc.Col(dcc.Graph(id='figura-31'),width=3),
                                             dbc.Col(dcc.Graph(id='figura-32'),width=3),
                                             dbc.Col(dcc.Graph(id='figura-33'),width=3),
                                             dbc.Col(dcc.Graph(id='figura-34'),width=3)],
                                            no_gutters=True)
                               ],fluid=True)
                              ],
                     style={"background-color":"red",
                            "padding-left": "0px"})

layout = dbc.Container([barra_nav,
                            dbc.Row([dbc.Col(otra_caja.crear_caja(),width=2),
                                     dbc.Col(dashboardContainer,width=10)])
                            ],
                    fluid=True)