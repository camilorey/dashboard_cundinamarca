import pandas as pd
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
#Vamos a usar clases que he construido para hacer controladores
from helpers.controladores_factory import DataFrame_Factory
from helpers.administrador_graficos import AdministradorGraficos
#importamos la app base para tener todo en el mismo ambiente
from app import app,crear_barra_navegacion,backend

#-------------------------------------------------------------------------------------
#Los datasets que usaremos
#-------------------------------------------------------------------------------------
reporte_municipios = backend.indicadores_municipios_globales


#Creamos un administrador de Gráficos para esta vista
admon_graficos = AdministradorGraficos('vista-depto')

#vamos a crear una caja de control desde un archivo
cols_dict = {'provincia':['DROPDOWN'],
             'municipio':['DROPDOWN'],
             'ano':['TICKS'],
             'delito':['TICKS']}
controles_depto = DataFrame_Factory("Controladores Indicadores",
                                    "controladores-indicadores",
                                    reporte_municipios,
                                    cols_dict)
controles_depto.crear_componentes()

#vamos a crear la barra de navegación
barra_nav = crear_barra_navegacion("Vista Indicadores Globales")

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


#-------------------------------------------------------------------------------------
#vamos a crear el top 10 de delitos
#-------------------------------------------------------------------------------------
top_10 =html.Div([html.H4('Top 10 de Delitos',id='top-10-titulo'),
                  dcc.Graph(id='top-10-plot')],
                 style={"text-align":"center"})

@app.callback(Output('top-10-titulo','children'),
              Input('controladores-indicadores-provincia_id','value'),
              Input('controladores-indicadores-municipio_id','value'))
def update_top_10_titulo(nom_provincia,nom_muni):
    info = "Top 10 de Delitos en el Departamento"
    if nom_muni is not None:
        info = "Top 10 de Delitos en "+nom_muni
    else:
        if nom_provincia is not None:
            info =  "Top 10 de delitos en "+nom_provincia
        else:
            info = "Top 10 de delitos en Cundinamarca"
    return info

@app.callback(Output('top-10-plot','figure'),
              Input('controladores-indicadores-provincia_id','value'),
              Input('controladores-indicadores-municipio_id','value'),
              Input('controladores-indicadores-ano_id','value'))
def update_top_10(nom_provincia,nom_muni,anos):
    datos = filtrar_por_anos(reporte_municipios,anos)
    if nom_muni is not None:
        datos = datos.loc[datos['municipio']==nom_muni]
    elif nom_provincia is not None:
        datos = datos.loc[datos['provincia']==nom_provincia]

    return admon_graficos.top_incidentes(datos,'delito')

#-------------------------------------------------------------------------------------
#vamos a poner las barras con el número de incidentes
#-------------------------------------------------------------------------------------
barras_incidentes =html.Div([html.H4('Incidentes por Provincia',id='incidentes-prov-titulo'),
                            dcc.Graph(id='incidentes-barras-plot')],
                            style={"text-align":"center"})

@app.callback(Output('incidentes-prov-titulo','children'),
              Input('controladores-indicadores-delito_id','value'))
def update_barras_letrero(filtros):
    if filtros is None or len(filtros)==0:
        return "Acumulado de Incidentes por Provincia"
    elif len(filtros)== 1:
        return "Acumulado de Incidentes por Provincia ("+filtros[0]+")"
    else:
        return "Acumulado de Incidentes por Provincia (Filtros Múltiples)"

@app.callback(Output('incidentes-barras-plot','figure'),
              Input('controladores-indicadores-delito_id','value'),
              Input('controladores-indicadores-ano_id','value'))
def update_barras(filtros,anos):
    datos = filtrar_por_anos(reporte_municipios,anos)
    if filtros is None or len(filtros)==0:
        return go.Figure(admon_graficos.barras_incidentes(datos, 'provincia'))
    elif len(filtros)==1:
        sub_datos = datos.loc[datos['delito'] == filtros[0]]
        return go.Figure(admon_graficos.barras_incidentes(sub_datos,'provincia'))
    else:
        sub_barras = []
        for valor in filtros:
            sub_datos = datos.loc[datos['delito'] == valor]
            barras = admon_graficos.barras_incidentes(sub_datos,'provincia',valor)
            sub_barras.append(barras)
        figura = go.Figure(data=sub_barras,
                           layout=go.Layout(barmode='stack'))
        return figura

#-------------------------------------------------------------------------------------
#vamos a poner una tabla con el top de los municipios
#-------------------------------------------------------------------------------------
tabla_top_mas = html.Div([html.H4('Top 10 Municipios Más x 100mil Habs',
                                  id='top-munis-mas-letrero'),
                          dcc.Graph(id='tabla-top-10-mas-munis')],
                      style={"text-align":"center"})
tabla_top_menos = html.Div([html.H4('Top 10 Municipios Menos x 100mil Habs',
                                    id='top-munis-menos-letrero'),
                      dcc.Graph(id='tabla-top-10-menos-munis')],
                      style={"text-align":"center"})

@app.callback(Output('tabla-top-10-mas-munis','figure'),
              Input('controladores-indicadores-delito_id','value'),
              Input('controladores-indicadores-ano_id','value'))
def actualizar_tabla_top_mas_munis(filtros,anos):
    data = filtrar_por_anos(reporte_municipios,anos)
    if filtros is not None and len(filtros)>1:
        data = data.loc[data['delito'].isin(filtros)]
    elif filtros is not None and len(filtros) == 1:
        data = data.loc[data['delito'] == filtros[0]]

    tabla_mas = admon_graficos.generar_tabla_top(data,
                                                 nom_columna='municipio',
                                                 nom_conteo='num_incidentes_100mil')
    return go.Figure(tabla_mas)

@app.callback(Output('tabla-top-10-menos-munis','figure'),
              Input('controladores-indicadores-delito_id','value'),
              Input('controladores-indicadores-ano_id','value'))
def actualizar_tabla_top_menos_munis(filtros,anos):
    data = filtrar_por_anos(reporte_municipios,anos)
    if filtros is not None and len(filtros) > 1:
        data = data.loc[data['delito'].isin(filtros)]
    elif filtros is not None and len(filtros) == 1:
        data = data.loc[data['delito'] == filtros[0]]

    tabla_menos = admon_graficos.generar_tabla_top(data,
                                                   nom_columna='municipio',
                                                   nom_conteo='num_incidentes_100mil',
                                                   tipo='MIN')
    return go.Figure(tabla_menos)

@app.callback(Output('top-munis-mas-letrero','children'),
              Input('controladores-indicadores-delito_id','value'))
def actualizar_letrero_top_mas_munis(filtros):
    if filtros is None or len(filtros) == 0:
        return "Top 10 Incidente Más x 100mil Habs"
    elif len(filtros) == 1:
        return "Top 10 Municipios Más x 100mil Habs (" + filtros[0] + ")"
    else:
        return "Top 10 Municipios Más x 100mil Habs (Filtros Múltiples)"

@app.callback(Output('top-munis-menos-letrero','children'),
              Input('controladores-indicadores-delito_id','value'))
def actualizar_letrero_top_menos_munis(filtros):
    if filtros is None or len(filtros) == 0:
        return "Top 10 Municipios Menos x 100mil Habs"
    elif len(filtros) == 1:
        return "Top 10 Municipios Menos x 100mil Habs (" + filtros[0] + ")"
    else:
        return "Top 10 Municipios Menos x 100mil Habs (Filtros Múltiples)"

#-------------------------------------------------------------------------------------
#Vamos a hacer unas cajas de bigotes
#-------------------------------------------------------------------------------------
bigotes_anuales = html.Div([html.H4('Bigotes anuales Incidentes x 100 mil habitantes ',
                                  id='bigotes-anuales-letrero'),
                          dcc.Graph(id='bigotes-anuales')],
                      style={"text-align":"center"})

@app.callback(Output('bigotes-anuales-letrero','children'),
              Input('controladores-indicadores-delito_id','value'))
def actualizar_letrero_bigotes_anuales(filtros):
    if filtros is None or len(filtros) == 0:
        return "Bigotes Anuales Incidentes x 100mil Habs"
    elif len(filtros) == 1:
        return "Bigotes Anuales Incidentes x 100mil Habs (" + filtros[0] + ")"
    else:
        return "Bigotes Anuales Incidentes x 100mil Habs (Filtros Múltiples)"

@app.callback(Output('bigotes-anuales','figure'),
              Input('controladores-indicadores-delito_id','value'),
              Input('controladores-indicadores-provincia_id','value'),
              Input('controladores-indicadores-municipio_id','value'))
def crear_bigotes_anuales(delitos,provincia,municipio):
    anos = list(reporte_municipios['ano'].unique())
    anos.sort()
    datos = reporte_municipios
    if municipio is not None:
        if delitos is None:
            datos = datos.loc[datos['municipio']==municipio]
        elif len(delitos)>2:
            datos = datos.loc[datos['municipio'] == municipio]
    else:
        if provincia is not None:
            datos = datos.loc[datos['provincia']==provincia]

    if delitos is not None:
        if len(delitos)>=1:
            datos = datos.loc[datos['delito'].isin(delitos)]

    fig = go.Figure()
    for ano in anos:
        sub_datos = datos.loc[datos['ano']==ano]
        if sub_datos.shape[0]>5:
            fig.add_trace(go.Box(y=sub_datos['num_incidentes_100mil'],
                                 name=str(ano)))
    return fig
#-------------------------------------------------------------------------------------
#Vamos a hacer unas barras por incidentes por año
#-------------------------------------------------------------------------------------
barras_anuales = html.Div([html.H4('Barras anuales Incidentes ',
                                  id='barras-anuales-letrero'),
                          dcc.Graph(id='barras-anuales')],
                      style={"text-align":"center"})
@app.callback(Output('barras-anuales-letrero','children'),
              Input('controladores-indicadores-delito_id','value'))
def actualizar_letrero_barras_anuales(filtros):
    if filtros is None or len(filtros) == 0:
        return "Barras Anuales Incidentes "
    elif len(filtros) == 1:
        return "Barras Anuales Incidentes  (" + filtros[0] + ")"
    else:
        return "Barras Anuales Incidentes  (Filtros Múltiples)"

@app.callback(Output('barras-anuales','figure'),
              Input('controladores-indicadores-delito_id','value'),
              Input('controladores-indicadores-provincia_id','value'),
              Input('controladores-indicadores-municipio_id','value'))
def actualizar_barras_anuales(delitos,provincia,municipio):
    datos = reporte_municipios
    if municipio is not None:
        datos = datos.loc[datos['municipio']==municipio]
    elif provincia is not None:
        datos = datos.loc[datos['provincia']==provincia]
    figura = None
    # noinspection PyUnreachableCode
    if delitos is None:
        figura = go.Figure(admon_graficos.barras_incidentes(datos, 'ano'))

    elif len(delitos) == 0:
        figura = go.Figure(admon_graficos.barras_incidentes(datos, 'ano'))

    elif len(delitos)==1:
        datos = datos.loc[datos['delito']==delitos[0]]
        figura = go.Figure(admon_graficos.barras_incidentes(datos, 'ano'))
    else:
        sub_barras = []
        for delito in delitos:
            sub_datos = datos.loc[datos['delito'] == delito]
            barras = admon_graficos.barras_incidentes(sub_datos, 'ano', delito)
            sub_barras.append(barras)
        figura = go.Figure(data=sub_barras,
                           layout=go.Layout(barmode='stack'))
    return figura
#-------------------------------------------------------------------------------------
#ahora ponemos el contenedor donde va a ir el resto de las cosas
#-------------------------------------------------------------------------------------
dashboardContainer = html.Div([dbc.Container([
                                    dbc.Row([dbc.Col(top_10,width=12)],
                                            no_gutters=True),
                                    dbc.Row([dbc.Col(barras_incidentes,width=4),
                                             dbc.Col(tabla_top_mas,width=4),
                                             dbc.Col(tabla_top_menos,width=4)],
                                            no_gutters=True),
                                    dbc.Row([dbc.Col(bigotes_anuales,width=6),
                                             dbc.Col(barras_anuales,width=6)],
                                            no_gutters=True)
                               ],fluid=True)
                              ],
                     style={"padding-left": "0px"})

layout = dbc.Container([dcc.Store(id='dataset-store'),
                        barra_nav,
                        dbc.Row([dbc.Col(controles_depto.crear_caja(), width=2),
                                 dbc.Col(dashboardContainer,width=10)])
                        ],
                    fluid=True)