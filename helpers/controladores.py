import dash
from datetime import date
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input,Output

class Controlador:
    def __init__(self,label_,id_):
        self.label = label_
        self.id = id_

class RangoFechasCalendario(Controlador):
    def __init__(self,id):
        rango_fechas_label = 'Escoja un rango de Fechas'
        super().__init__(rango_fechas_label,id)
    
    def crear_calendario(self):
        print(self.id)
        calendario = dcc.DatePickerRange(id=self.id,
                                         min_date_allowed=date(2010, 1, 1),
                                         max_date_allowed=date(2019, 12, 31),
                                         initial_visible_month=date(2012, 6, 6),
                                         end_date=date(2019, 12, 31))
        nombre_calendario = dbc.Label(self.label,id='letrero-'+self.id)
        return dbc.FormGroup([nombre_calendario, calendario])

class TickBoxes(Controlador):
    def __init__(self,label_,id_):
        super().__init__(label_,id_)
        self.options =[]

    def set_opciones(self):
        self.options = [{"label":"Opción "+str(i),"value": str(i)} for i in range(5)]

    def crear_tickboxes(self):
        print(self.id)
        checks = dcc.Checklist(id=self.id,
                               options=self.options)
        nom_checkboxes = dbc.Label(self.label,id='letrero-'+self.id)
        return dbc.FormGroup([nom_checkboxes, checks])

class Slider(Controlador):
    def __init__(self,slider_label,id):
        super().__init__(slider_label,id)

    def set_rango(self,min_value,max_value,step,step_ticks):
        self.min = min_value
        self.max = max_value
        self.step = step
        num_marcas = round((max_value-min_value)/step)
        self.ticks = {i*step:str(i*step) for i in range(num_marcas) if i%step_ticks ==0 }
        
    def crear_slider(self,min_,max_,step_,step_ticks_,val_defecto):
        print(self.id)
        self.set_rango(min_,max_,step_,step_ticks_)
        nombre_slider = dbc.Label(self.label,id='letrero-'+self.id)
        slider = dcc.Slider(id=self.id, 
                            min=self.min, 
                            max=self.max, 
                            step=self.step,
                            marks = self.ticks,
                            value=val_defecto)
        return dbc.FormGroup([nombre_slider, slider])

class Dropdown(Controlador):
    def __init__(self,drop_label,id):
        super().__init__(drop_label,id)
        self.options = []
        
    def set_opciones(self):
        self.options = [{"label":str(i),"value":i} for i in range(5)]
        
    def crear_dropdown(self,val_defecto):
        print(self.id)
        letrero = dbc.Label(self.label,id='letrero-'+self.id)
        drop = dcc.Dropdown(id=self.id,
                            options = self.options,
                            placeholder ="Escoja una opción"
                           )
        return dbc.FormGroup([letrero,drop])