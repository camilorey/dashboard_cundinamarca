import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

class AdministradorGraficos:
    def __init__(self,id_prefix):
        self.id_prefix_ = id_prefix

    def crear_id(self,id):
        return self.id_prefix_+"-"+id

    def crear_class_name(self,tipo):
        return self.id_prefix_+"-figura-"+tipo

    def crear_tag(self,tag_id):
        tag = html.Div(id=self.crear_id(tag_id),
                       children=['Respuesta'])
        return tag

    def crear_figura(self,titulo,id):
        figura_id = self.crear_id('figura-'+id)
        figura = dcc.Graph(id=figura_id)
        figura_div = html.Div(className=self.crear_class_name(id),
                              children=[html.H4(titulo),
                                        figura],
                              style={'text-align': 'center'})
        return figura_div,figura_id

    def top_incidentes(self, dataset,nom_columna):
        pivote_col = pd.pivot_table(dataset,
                                    index=nom_columna,
                                    values='num_incidentes',
                                    aggfunc='sum').reset_index()
        #Ordenamos el pivote
        pivote_col = pivote_col.sort_values(by='num_incidentes',ascending=False)
        figura = go.Figure()
        for i in range(2):
            for j in range(5):
                indice = i + 2 * j
                if indice <pivote_col.shape[0]:
                    delito = pivote_col.iloc[indice][nom_columna]
                    valor = pivote_col.iloc[indice]['num_incidentes']
                    indicador = go.Indicator(value=valor,
                                             mode='number',
                                             delta={'reference': valor},
                                             gauge={'axis': {'visible': False}},
                                             title={'text': delito},
                                             domain={'row': i, 'column': j})
                    figura.add_trace(indicador)
        figura.update_layout(grid={'rows': 2, 'columns': 5})
        return figura

    def barras_incidentes(self,datos,nom_columna='provincia',nom_grupo=None):
        categorias = datos[nom_columna].unique()
        valores = []
        for cat in categorias:
            num_incidentes = datos.loc[datos[nom_columna]==cat]['num_incidentes'].sum()
            valores.append(num_incidentes)
        if nom_grupo is not None:
            return go.Bar(x=categorias,y=valores,name=nom_grupo)
        else:
            return go.Bar(x=categorias,y=valores)

    def generar_tabla_top(self,data,nom_columna,nom_conteo='num_incidentes',tipo='SUP',tam_top=10):
        pivote = pd.pivot_table(data,
                                index = [nom_columna],
                                values=[nom_conteo],
                                aggfunc='mean').reset_index()
        if tipo=='SUP':
            pivote = pivote.sort_values(by=nom_conteo,ascending=False)
        else:
            pivote = pivote.sort_values(by=nom_conteo, ascending=True)
        #sacamos el top del tamaño que queremos
        top = pivote.head(tam_top)

        if tipo != 'SUP':
            top = top.sort_values(by=nom_conteo,ascending=True)
        campo = list(top[nom_columna])
        incidentes = ["{:.2f}".format(x) for x in list(top[nom_conteo])]
        tabla = go.Table(header=dict(values=[nom_columna, nom_conteo]),
                         cells=dict(values=[campo, incidentes]))
        return tabla




