import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input,Output

class ListaComponentes:
    def __init__(self):
        self.lista_componentes = []

    def add_componentes(self,comp):
        self.lista_componentes.append(comp)

class BarraNavegacion(ListaComponentes):
    def __init__(self):
        super().__init__()
        #nombre = html.H1("Dashboard Cundinamarca")


    def crear_links(self,links_dict):
        links = []
        for nom_link in links_dict.keys():
            url_link = links_dict[nom_link]
            if url_link == "divider":
                links.append(dbc.DropdownMenuItem(divider=True))
            else:
                links.append(dbc.DropdownMenuItem(nom_link,
                                                  href=url_link,
                                                  external_link=True))
        return links

    def crear_menu_links(self, nom_dropmenu, links_dict):
        dropdown_items = self.crear_links(links_dict)
        menu = dbc.DropdownMenu(id='drop-barra',
                                children=dropdown_items,
                                nav=True,
                                in_navbar=True,
                                label=nom_dropmenu)
        self.add_componentes(menu)

    def crear_barra(self,nom_barra,nom_drop_menu,links_dict):
        self.crear_menu_links(nom_drop_menu, links_dict)
        navbar = dbc.NavbarSimple(self.lista_componentes,
                                  brand=nom_barra,
                                  brand_href="#",
                                  color="dark",
                                  dark=True,
                                  fluid=True
                                  )
        return navbar

class CardAutoria(ListaComponentes):
    def __init__(self):
        super().__init__()
        self.icono_src = "../static/Logo_Poli_tiny.png"
        self.nombre_dashboard = "Dashboard de Cundinamarca"
        self.autores = "E.Mora, J.S. Martinez & C.Rey"
        self.info = "Este es un dashboard con información de Cundinamarca"

    def crear_imagen(self):
        return dbc.CardImg(src = self.icono_src,bottom=True)

    def crear_titulo(self):
        return html.H4(self.nombre_dashboard,className='card-title')
    def crear_info(self):
        return html.P(self.info,className='card-text')
    def crear_autores(self):
        return html.H6(self.autores,className='card-subtitle')

    def crear_cuerpo(self):
        self.lista_componentes.append(self.crear_titulo())
        self.lista_componentes.append(self.crear_autores())
        self.lista_componentes.append(self.crear_info())

    def crear_card(self):
        self.crear_cuerpo()
        card = dbc.Card([dbc.CardBody(self.lista_componentes),
                        self.crear_imagen()]
                        )
        return card




