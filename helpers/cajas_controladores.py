import dash_bootstrap_components as dbc
import dash_html_components as html
from helpers.elementos_interfaz_fijos import CardAutoria
from helpers.controladores import Controlador,Dropdown,Slider,RangoFechasCalendario,TickBoxes

class CajaControladores(Controlador):
    def __init__(self,label,id):
        super().__init__(label,id)
        # vamos a crear la Card con los autores
        self.card_autores = CardAutoria().crear_card()
        self.componentes = []
        letrero = dbc.FormGroup([html.H2("Escoja los parámetros")])
        self.add_componente(letrero)

    def crear_componentes(self):
        miDrop = Dropdown("Dropdown De Prueba 1", "prueba_1").crear_dropdown(2)
        miDrop2 = Dropdown("Dropdown de prueba 2", "prueba-2").crear_dropdown(2)
        # agregamos los dropdowns
        self.add_componente(miDrop)
        self.add_componente(miDrop2)
        # ahora vamos a crear un slider
        miSlider = Slider("Slider de prueba", "slider-1").crear_slider(0, 20, 2, 4, 3)
        miSlider2 = Slider("Slider de prueba 2", "slider-2").crear_slider(0, 50, 1, 5, 15)
        miSlider3 = Slider("slider de prueba 3", "slider-3").crear_slider(0, 100, 10, 4, 20)
        self.add_componente(miSlider)
        self.add_componente(miSlider2)
        self.add_componente(miSlider3)
        # vamos  a crear una caja con Ticks
        check_div = TickBoxes('Escoja la opción', 'ticks-1').crear_tickboxes()
        self.add_componente(check_div)
        # vamos a crear un calendario
        calendario_div = RangoFechasCalendario('rango-fechas1').crear_calendario()
        self.add_componente(calendario_div)

    def add_componente(self, componente):
        self.componentes.append(componente)

    def crear_caja(self):
        control_div = html.Div([dbc.Card(self.componentes),
                                html.Hr(),
                                self.card_autores],
                                style={"padding-left": "0px"})
        return control_div


