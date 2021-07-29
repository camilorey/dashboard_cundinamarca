import psycopg2
import pandas as pd

#parametros del orquestador
params_orquestador={'hostname':'suleiman.db.elephantsql.com',
                    'username':'bcdcpmha',
                    'database':'bcdcpmha',
                    'password':'fVFa5dcR2zO9-hTJrV8DAj_gKrLKe3Sk'}

#diccionarios de uso
diccionario_armas = {'SIN EMPLEO DE ARMAS':['SIN EMPLEO DE ARMAS', 'NO APLICA'],
                     'NO HAY INFORMACIÓN':['NO HAY INFORMACION', 'NO REPORTADO'],
                      'ARMA DE USO PRIVATIVO':['ARMA DE FUEGO', 'GRANADA DE MANO',
                                               'MINA ANTIPERSONA'],
                       'ARMA BLANCA':['ARMA BLANCA / CORTOPUNZANTE', 'CORTANTES',
                                      'PUNZANTES','ARMA BLANCA','CORTOPUNZANTES',
                                      'CUCHILLA', 'ARMAS BLANCAS'],
                       'HERRAMIENTAS DE ROBO': ['PALANCAS','LLAVE MAESTRA','DIRECTA'],
                       'CONTUNDENTES':['CONTUNDENTES'],
                       'EXPLOSIVOS':['ARTEFACTO EXPLOSIVO/CARGA DINAMITA',
                                     'ARTEFACTO INCENDIARIO', 'CARRO BOMBA'],
                       'OBJETOS CASEROS': ['CINTAS/CINTURON','PRENDAS DE VESTIR',
                                           'ALMOHADA', 'AGUA CALIENTE','BOLSA PLASTICA',
                                           'CUERDA/SOGA/CADENA'],
                       'EXPLOSIVO CASERO': ['POLVORA(FUEGOS PIROTECNICOS)','PAPA EXPLOSIVA'],
                       'COMBUSTIBLE': ['COMBUSTIBLE'],
                       'ANIMALES':['PERRO'],
                       'ÁCIDO': ['ACIDO'],
                       'VEHÍCULO': ['TREN', 'MOTO', 'VEHICULO', 'BICICLETA'],
                       'SUSTANCIAS TÓXICAS': ['SUSTANCIAS TOXICAS', 'VENENO','GASES',
                                              'QUIMICOS','JERINGA'],
                       'SUSTANCIA PSICOACTIVA':['ALUCINOGENOS','LICOR ADULTERADO',
                                                'ESCOPOLAMINA','MEDICAMENTOS']}

def hacer_query(query,db_params,mensaje_exito):
    conexionDB = None
    resultado = None
    try:
        conexionDB = psycopg2.connect(host=db_params['hostname'],
                                      user=db_params['username'],
                                      password=db_params['password'],
                                      dbname=db_params['database'])
        resultado = pd.read_sql_query(query, conexionDB)
        conexionDB.close()
        return resultado
    except (Exception, psycopg2.DatabaseError) as Error:
        print(Error)
    finally:
        if conexionDB is not None:
            conexionDB.close()
            print("DB Connection closed", mensaje_exito)


class BackEnd:

    def __init__(self):
        self.params_orquestador = params_orquestador
        print("Conectándose a la principal para traer parámetros")
        self.params_bases = self.get_parametros_provinciales()
        print("abriendo archivo para traer población actualizada")
        self.poblacion_municipios = self.indicadores_poblacion()
        print("Trayendo reporte de los municipios")
        self.indicadores_municipios_globales = self.reporte_incidentes_municipios()
        print("Trayento reporte de armas y zonas")
        self.indicadores_armas_zonas = self.reporte_zonas_armas_municipios()


    def query_en_orquestador(self,query):
        return hacer_query(query,
                           self.params_orquestador,
                           "Orquestador Reached")

    def query_en_provincia(self,nom_provincia,query):
        db_params = self.params_bases[nom_provincia]
        return hacer_query(query,
                           db_params,
                           "Provincia "+nom_provincia+" reached")

    def get_parametros_provinciales(self):
        query = """SELECT provincia.provincia,
                          parametros_bases_provincias.host,
                          parametros_bases_provincias.username,
                          parametros_bases_provincias.password 
                   FROM parametros_bases_provincias JOIN provincia ON provincia.provincia_id = parametros_bases_provincias.provincia_id;"""
        params_bases_provinciales = self.query_en_orquestador(query)
        params_provincias = {}
        for idx, prov_db in params_bases_provinciales.iterrows():
            prov = prov_db['provincia']
            params_prov = {'hostname': prov_db['host'],
                           'username': prov_db['username'],
                           'database': prov_db['username'],
                           'password': prov_db['password']}
            params_provincias[prov] = params_prov
        return params_provincias

    def get_nombres_provincias(self):
        nom_provincias = list(self.params_bases.keys())
        return nom_provincias

    def cambiar_a_100mil_hab(self,nom_muni,valor):
        poblacion = self.get_poblacion_municipio(nom_muni)
        estadistco = 1
        if poblacion == 0:
            estadistico = valor
        else:
            estadistico = 100000*(valor/poblacion)
        return estadistico

    def corregir_delito(self,original):
        if 'ARTÍCULO' in original or 'SEX' in original:
            return 'DELITOS SEXUALES'
        elif 'HOMICIDIO EN ACCIDENTES DE TRANSITO' in original:
            return 'HOMICIDIO TRÁNSITO'
        elif 'LESIONES EN ACCIDENTES DE TRANSITO' in original:
            return 'LESIONES TRÁNSITO'
        else:
            return original

    def corregir_arma(self,original):
        nom_arma = ''
        for arma in diccionario_armas.keys():
            if original in diccionario_armas[arma]:
                nom_arma = arma
        return nom_arma

    def reporte_zonas_armas_municipios(self):
        query = """SELECT municipio.municipio,
                   EXTRACT(YEAR FROM incidente.FechaYHora) as "ano",
                   delito.delito,
                   zona.zona,
                   armaUsada.armaUsada as "arma",
                   count(incidente.incidente_id) AS "num_incidentes"
                   FROM incidente JOIN municipio ON incidente.municipio_id = municipio.municipio_id
                                   JOIN delito ON incidente.delito_id = delito.delito_id
                                   JOIN zona ON incidente.zona_id = zona.zona_id
                                   JOIN armaUsada ON incidente.armausada_id = armaUsada.armausada_id
                   GROUP BY municipio.municipio,delito.delito,EXTRACT(YEAR FROM incidente.FechaYHora),zona.zona,armaUsada.armaUsada"""
        dfs = []
        for prov in self.params_bases.keys():
            repo_prov = self.query_en_provincia(prov,query)
            # corregimos nombre de los delitos
            repo_prov['delito'] = repo_prov['delito'].apply(lambda d: self.corregir_delito(d))
            repo_prov['arma'] = repo_prov['arma'].apply(lambda a: self.corregir_arma(a))
            # corregimos el año a entero
            repo_prov['ano'] = repo_prov['ano'].apply(lambda a: int(a))
            repo_prov['provincia'] = prov
            #agregamos el dataframe a la lista
            dfs.append(repo_prov)
        general = pd.concat(dfs)
        reporte_pivote = pd.pivot_table(general,
                                        index=['provincia','municipio', 'ano', 'delito', 'zona','arma'],
                                        values='num_incidentes',
                                        aggfunc='sum').reset_index()
        reporte_pivote['num_incidentes_100mil'] = reporte_pivote.apply(lambda f: self.cambiar_a_100mil_hab(f['municipio'],f['num_incidentes']),axis=1)
        return reporte_pivote


    def reporte_incidentes_municipios(self):
        query = """ SELECT municipio.municipio,
                           EXTRACT(YEAR FROM incidente.FechaYHora) as "ano",
                           delito.delito,
                           count(incidente.incidente_id) AS "num_incidentes"
                           FROM incidente JOIN municipio ON incidente.municipio_id = municipio.municipio_id
                           JOIN delito ON incidente.delito_id = delito.delito_id
                           GROUP BY municipio.municipio,delito.delito,EXTRACT(YEAR FROM incidente.FechaYHora)"""
        dfs = []
        for prov in self.params_bases.keys():
            repo_prov = self.query_en_provincia(prov,query)
            # corregimos nombre de los delitos
            repo_prov['delito'] = repo_prov['delito'].apply(lambda d: self.corregir_delito(d))
            #corregimos el año a entero
            repo_prov['ano'] = repo_prov['ano'].apply(lambda a: int(a))
            repo_prov['provincia'] = prov
            dfs.append(repo_prov)
        general = pd.concat(dfs)
        general = pd.concat(dfs)
        reporte_pivote = pd.pivot_table(general,
                                        index=['provincia','municipio', 'ano', 'delito'],
                                        values='num_incidentes',
                                        aggfunc='sum').reset_index()
        reporte_pivote['num_incidentes_100mil'] = reporte_pivote.apply(lambda f: self.cambiar_a_100mil_hab(f['municipio'],f['num_incidentes']),axis=1)
        return reporte_pivote

    def reporte_general(self):
        query = """ SELECT delito.delito, 
                           count(incidente.incidente_id) AS "num_incidentes"
                    FROM incidente JOIN delito ON incidente.delito_id = delito.delito_id
                    GROUP BY delito.delito"""
        reportes_provinciales = []
        for prov in self.params_bases.keys():
            rep_prov = self.query_en_provincia(prov,query)
            # corregimos nombre de los delitos
            rep_prov['delito'] = rep_prov['delito'].apply(lambda d: self.corregir_delito(d))
            # calculamos el número de delitos sexuales a mano
            num_delitos_sexuales = rep_prov.loc[rep_prov['delito'] == 'DELITOS SEXUALES']['num_incidentes'].sum()
            # quitamos los delitos sexuales del DataFrame original
            rep_prov.drop(rep_prov[rep_prov['delito'] == 'DELITOS SEXUALES'].index, inplace=True)
            #agregamos los reportes resumidos
            rep_prov = rep_prov.append({'delito': 'DELITOS SEXUALES',
                                    'num_incidentes': num_delitos_sexuales},
                                   ignore_index=True)
            # agregamos la columna de la provincia
            rep_prov['provincia'] = prov
            #agregamos al listado de reportes provinciales
            reportes_provinciales.append(rep_prov)
        #retornamos todos los reportes unidos
        return pd.concat(reportes_provinciales)

    def get_promedio_departamento(self,nom_delito):
        media_tabla = self.indicadores_crimenes_globales[nom_delito].mean()
        media_delito = round(media_tabla)
        return media_delito

    def get_poblacion_municipio(self,nom_municipio):
        info_muni = self.poblacion_municipios.loc[self.poblacion_municipios['municipio']==nom_municipio]
        if len(info_muni) == 0:
            return 0
        else:
            poblacion = info_muni['habitantes']
            return poblacion.values[0]

    def info_victimas_provincia(self, nom_provincia):
        query = """SELECT incidente.incidente_id,
                        DATE(incidente.fechaYHora) AS "fecha",
                        municipio.municipio,
                        delito.delito,
                        sexo.sexo,
                        incidentePersonal.edad
                   FROM incidente JOIN incidentePersonal ON incidente.incidente_id = incidentePersonal.incidente_id
                                  JOIN sexo ON incidentePersonal.sexo_id = sexo.sexo_id
                                  JOIN delito ON delito.delito_id = incidente.delito_id
                                  JOIN municipio ON incidente.municipio_id = municipio.municipio_id"""
        result = self.query_en_provincia(nom_provincia, query)
        # corregimos nombre de delitos sexuales
        corregir_delito = lambda x: 'DELITOS SEXUALES' if 'ARTÍCULO' in x else x
        result['delito'] = result['delito'].apply(lambda delito: corregir_delito(delito))
        return result

    def indicadores_poblacion(self):
        url='https://opendata.arcgis.com/datasets/289cb188a45c48a08826bf28350b0bca_0.csv'
        info_poblacion = pd.read_csv(url,sep=',')
        info_poblacion = info_poblacion.rename(columns={'f2':'municipio','f3':'habitantes'})

        solo_info = pd.DataFrame(columns=['municipio','habitantes'])
        solo_info['municipio'] = info_poblacion['municipio'].str.upper()
        solo_info['habitantes'] = info_poblacion['habitantes']
        return solo_info
