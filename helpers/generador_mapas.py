import geojson
import pandas as pd
import numpy as np

import plotly.graph_objects as go

archivo_mapa_municipios = 'assets/municipios_cundinamarca.geojson'

class GeneradorMapas:
    def __init__(self):
        self.set_archivos()

    def set_archivos(self):
        with open(archivo_mapa_municipios,encoding='utf-8') as archivo:
            geojson_colombia = geojson.load(archivo)

        features_cundi = []
        num_municipios = len(geojson_colombia['features'])
        munis_df = pd.DataFrame()
        for i in range(num_municipios):
            feature = geojson_colombia['features'][i]
            cod_dane = str(feature['properties']['cod_DANE'])
            nom_muni = feature['properties']['MUNICIPIO']
            if cod_dane.startswith('25'):
                features_cundi.append(feature)
                munis_df = munis_df.append({'cod_DANE':cod_dane,
                                            'municipio':nom_muni},
                                           ignore_index=True)

        self.geojson = {"type":"FeatureCollection",
                         "features": features_cundi}
        self.municipios = munis_df

    def adaptar_dataframe(self,dataframe):
        return self.municipios.join(dataframe.set_index('municipio'),
                                    on='municipio')
    def crear_mapa_figura(self,dataframe,nom_columna,colores='viridis'):
        #hacemos el join de los municipios
        data = self.adaptar_dataframe(dataframe)
        mapa_plot = go.Choroplethmapbox(geojson=self.geojson,
                                        colorscale=colores,
                                        z=list(data[nom_columna]),
                                        ids=list(data['cod_DANE']),
                                        text=list(data['municipio']),
                                        locations=list(data['cod_DANE']),
                                        marker={'opacity': 0.6})
        mapa_figura = go.Figure(mapa_plot)
        mapa_figura.update_layout(mapbox_center={'lat': 4.60971, 'lon': -74.08175},
                                  mapbox_style='carto-positron',
                                  mapbox_zoom=7,
                                  width=800,
                                  height=800)
        mapa_figura.update_geos(fitbounds='geojson')
        return mapa_figura

    def crear_dataframe(self):
        mapa_df = pd.DataFrame()
        num_munis = len(self.geojson['features'])
        for i in range(num_munis):
            cod_dane = self.geojson['features'][i]['properties']['cod_DANE']
            nom_muni = self.geojson['features'][i]['properties']['MUNICIPIO']
            reg_df = {}
            reg_df['municipio'] = nom_muni
            reg_df['valor_1'] = np.random.randint(100)
            reg_df['valor_2'] = np.random.randint(200)
            reg_df['valor_3'] = np.random.randint(200)

            mapa_df = mapa_df.append(reg_df, ignore_index=True)
        return mapa_df

