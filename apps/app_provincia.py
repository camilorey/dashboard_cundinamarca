import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

#Vamos a usar clases que yo he construido para hacer controladores
from helpers.controladores_factory import DataFrame_Factory
from helpers.administrador_graficos import AdministradorGraficos
from helpers.generador_mapas import GeneradorMapas
#traemos la app principal
from app import app,crear_barra_navegacion,backend

#-------------------------------------------------------------------------------------
#Los datasets que usaremos
#-------------------------------------------------------------------------------------
reporte_municipios = backend.indicadores_municipios_globales
reporte_armas = backend.indicadores_armas_zonas


#Creamos un administrador de Gráficos para esta vista
admon_graficos = AdministradorGraficos('vista-mapas')

#Creamos el Generador mapas
mapas = GeneradorMapas()

#vamos a crear una caja de control desde un archivo
cols_dict = { 'ano':['SLIDER',1,2],
              'zona':['TICKS'],
              'delito':['TICKS'],
              'arma':['DROPDOWN']}
controles_depto = DataFrame_Factory("Controladores Mapas",
                                    "controladores-mapas",
                                    reporte_armas,
                                    cols_dict)
controles_depto.crear_componentes()

@app.callback(Output('letrero-controladores-mapas-ano_id','children'),
              Input('controladores-mapas-ano_id','value'))
def mostrar_ano_slider(ano):
    return "Año: "+str(ano)

#vamos a crear la barra de navegación
barra_nav = crear_barra_navegacion("Mapas de Crimen en el Departamento")

#una función auxiliar para filtrar por anos
def filtrar_por_anos(datos,lista_anos):
    if lista_anos is None:
        return datos
    elif len(lista_anos)==0:
        return datos
    else:
        anos = [int(a) for a in lista_anos]
        if len(anos) == 1:
            return datos.loc[datos['ano']==anos[0]]
        else:
            return datos.loc[datos['ano'].isin(anos)]

def filtrar_por_categorias(dataset,nom_columna,filtros):
    datos = dataset
    if filtros is not None:
        if len(filtros) == 1:
            datos = datos.loc[datos[nom_columna]==filtros[0]]
        elif len(filtros)> 1:
            datos = datos.loc[datos[nom_columna].isin(filtros)]
    return datos
#-------------------------------------------------------------------------------------
#vamos a crear el mapa por número de incidentes
#-------------------------------------------------------------------------------------
mapa_incidentes =html.Div([html.H4('Número de incidentes',id='mapa-num-incidentes-letrero'),
                  dcc.Graph(id='mapa-num-incidentes')],
                 style={"text-align":"left"})
@app.callback(Output('mapa-num-incidentes-letrero','children'),
              Input('controladores-mapas-delito_id','value'))
def actualizar_letrero_mapa_incidentes(delitos):
    info = "Incidentes de delitos Departamento"
    if delitos is not None:
        if len(delitos) == 1:
            info = "Incidentes de delitos Departamento ("+delitos[0]+")"
        elif len(delitos)>1:
            info = "Incidentes de delitos Departamento (Múltiples Filtros)"
    return info

@app.callback(Output('mapa-num-incidentes','figure'),
              Input('controladores-mapas-delito_id','value'),
              Input('controladores-mapas-ano_id','value'),
              Input('controladores-mapas-zona_id','value'))
def crear_mapa_incidentes(delitos,anos,zonas):
    datos = filtrar_por_categorias(reporte_armas,'ano',[anos])
    datos = filtrar_por_categorias(datos, 'delito', delitos)
    datos = filtrar_por_categorias(datos, 'zona', zonas)
    pivote = pd.pivot_table(datos,
                            index='municipio',
                            values='num_incidentes',
                            aggfunc='sum').reset_index()
    mapa_plot = mapas.crear_mapa_figura(pivote, 'num_incidentes',colores='magma')
    return mapa_plot

#-------------------------------------------------------------------------------------
#vamos a crear el mapa de densidad (incidencias por 100mil  incidentes
#-------------------------------------------------------------------------------------
mapa_densidades =html.Div([html.H4('Incidentes x 100 mil habitantes',
                                   id='mapa-densidad-incidentes-letrero'),
                           dcc.Graph(id='mapa-densidad-incidentes')],
                           style={"text-align":"left"})
@app.callback(Output('mapa-densidad-incidentes-letrero','children'),
              Input('controladores-mapas-delito_id','value'))
def actualizar_letrero_mapa_densidad(delitos):
    info = "Incidentes x 100 mil habitantes"
    if delitos is not None:
        if len(delitos) == 1:
            info = "Incidentes x 100 mil habitantes ("+delitos[0]+")"
        elif len(delitos)>1:
            info = "Incidentes x 100 mil habitantes (Múltiples Filtros)"
    return info

@app.callback(Output('mapa-densidad-incidentes','figure'),
              Input('controladores-mapas-delito_id','value'),
              Input('controladores-mapas-ano_id','value'),
              Input('controladores-mapas-zona_id','value'))
def crear_mapa_densidad(delitos,anos,zonas):
    datos = filtrar_por_categorias(reporte_armas,'ano',[anos])
    datos = filtrar_por_categorias(datos,'delito',delitos)
    datos = filtrar_por_categorias(datos,'zona',zonas)
    pivote = pd.pivot_table(datos,
                            index='municipio',
                            values='num_incidentes_100mil',
                            aggfunc='mean').reset_index()
    mapa_plot = mapas.crear_mapa_figura(pivote, 'num_incidentes_100mil')
    return mapa_plot

#-------------------------------------------------------------------------------------
#vamos a crear el mapa de armas
#-------------------------------------------------------------------------------------
mapa_armas = html.Div([html.H4('Armas usadas en Cundinamarca',
                                   id='mapa-armas-letrero'),
                           dcc.Graph(id='mapa-armas-incidentes')],
                           style={"text-align":"left"})

@app.callback(Output('mapa-armas-letrero','children'),
              Input('controladores-mapas-delito_id','value'),
              Input('controladores-mapas-ano_id','value'),
              Input('controladores-mapas-zona_id','value'),
              Input('controladores-mapas-arma_id','value'))
def actualizar_letrero_mapa_armas(delitos,anos,zonas,arma):
    letrero = "Mapa de Armas en Cundinamarca "
    if arma is not None:
        letrero += " ("+arma+")"
    if delitos is not None or anos is not None or zonas is not None:
        letrero += " (Múltiples Filtros)"
    return "Mapa de Armas"

@app.callback(Output('mapa-armas-incidentes','figure'),
              Input('controladores-mapas-delito_id','value'),
              Input('controladores-mapas-ano_id','value'),
              Input('controladores-mapas-zona_id','value'),
              Input('controladores-mapas-arma_id','value'))
def crear_mapa_armas(delitos,anos,zonas,arma):
    datos = filtrar_por_categorias(reporte_armas,'arma',[arma])
    datos = filtrar_por_categorias(datos,'ano',[anos])
    datos = filtrar_por_categorias(datos,'delito',delitos)
    datos = filtrar_por_categorias(datos,'zona',zonas)
    pivote = None
    if len(datos)==0:
        pivote = pd.DataFrame()
        pivote['municipio'] = reporte_armas['municipio'].unique()
        pivote['num_incidentes_100mil'] = 1
    else:
        pivote = pd.pivot_table(datos,
                                index='municipio',
                                values='num_incidentes_100mil',
                                aggfunc='mean').reset_index()
    mapa_plot = mapas.crear_mapa_figura(pivote,'num_incidentes_100mil')
    return mapa_plot
#-------------------------------------------------------------------------------------
#ahora ponemos el contenedor donde va a ir el resto de las cosas
#-------------------------------------------------------------------------------------

dashboardContainer = html.Div([dbc.Container([html.Div(html.H1("Mapas de Cantidad de Incidentes por Municipio")),
                                    dbc.Row([dbc.Col(mapa_incidentes,width=6),
                                             dbc.Col(mapa_densidades,width=6)],
                                            no_gutters=True),
                                    html.Div(html.H1("Mapas de armas en el Departamento")),
                                    dbc.Row([dbc.Col(mapa_armas,width=6),
                                             dbc.Col(dcc.Graph(id='figura-22'),width=6)],
                                            no_gutters=True),

                                    dbc.Row([dbc.Col(dcc.Graph(id='figura-31'),width=3),
                                             dbc.Col(dcc.Graph(id='figura-32'),width=3),
                                             dbc.Col(dcc.Graph(id='figura-33'),width=3),
                                             dbc.Col(dcc.Graph(id='figura-34'),width=3)],
                                            no_gutters=True)
                               ],fluid=True)
                              ],
                     style={"padding-left": "0px"})

layout = dbc.Container([barra_nav,
                        dbc.Row([dbc.Col(controles_depto.crear_caja(),width=2),
                        dbc.Col(dashboardContainer,width=10)])
                            ],
                    fluid=True)