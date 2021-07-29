import numpy as np
from helpers.controladores import Dropdown,Slider, TickBoxes
from helpers.cajas_controladores import CajaControladores
from dash.dependencies import Input,Output

class DataFrame_Factory(CajaControladores):
    def __init__(self,label,id,dataframe,tipos_):
        super().__init__(label,id)
        self.dataframe = dataframe
        self.tipos_componentes = tipos_

    def crear_slider(self,nom_columna,step,step_ticks):
        min_value = self.dataframe[nom_columna].min()
        max_value = self.dataframe[nom_columna].max()
        val_defecto = min_value
        slider = Slider(nom_columna,self.id+"-"+nom_columna+"_id")
        return slider.crear_slider(min_value,max_value,step,step_ticks,val_defecto)

    def crear_dropdown(self,nom_columna):
        valores = np.sort(list(self.dataframe[nom_columna].unique()))
        #creamos las opciones para el DropDown
        dropdown = Dropdown(nom_columna,self.id+"-"+nom_columna+"_id")
        dropdown.options = [{"label": str(val), "value": val} for val in valores]
        return dropdown.crear_dropdown(valores[0])

    def crear_tickboxes(self,nom_columna):
        valores = np.sort(list(self.dataframe[nom_columna].unique()))
        ticks = TickBoxes(nom_columna, self.id+"-"+nom_columna+"_id")
        ticks.options = [{"label": str(val), "value": str(val)} for val in valores]
        return ticks.crear_tickboxes()
    """
     Aquí necesitamos un diccionario que diga qué columnas y qué tipo quiere hacer
    """
    def crear_componentes(self):
        for campo in self.tipos_componentes.keys():
            params_campo = self.tipos_componentes[campo]
            componente = None
            if params_campo[0] == 'DROPDOWN':
                componente = self.crear_dropdown(campo)
            elif params_campo[0] == 'SLIDER':
                componente = self.crear_slider(campo,params_campo[1], params_campo[2])
            elif params_campo[0] == 'TICKS':
                componente = self.crear_tickboxes(campo)
            #agregamos el componente a la lista de componentes
            self.add_componente(componente)

    def crear_actualizacion_campo(self,nom_campo):
        def actualizar_anotacion(valor):
            if valor is not None:
                return nom_campo + ': ' + str(valor)
            else:
                return nom_campo

        return actualizar_anotacion

    def crear_callbacks_basicos(self,app):
        for campo in self.tipos_componentes.keys():
            app.callback(Output(component_id='letrero-' + campo + "_id", component_property='children'),
                         [Input(component_id=campo + '_id', component_property='value')]
                         )(self.crear_actualizacion_campo(campo))






