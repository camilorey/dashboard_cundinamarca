from dash import Dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from backend.back_end import BackEnd
from dash.dependencies import Input,Output

#aquí creamos la app principal que va a manejar todo
app = Dash(__name__,
           suppress_callback_exceptions=True,
           external_stylesheets=[dbc.themes.BOOTSTRAP])

#creamos el servidor
server = app.server

#ahora vamos a crear los ítems del menú que nos permitirán ir a todas las vistas
vistas_dict ={"Vista de Datos Municipio":["municipio",'/apps/app_municipio'],
              "Vista de Datos Provincia":["provincia",'/apps/app_provincia'],
              "Vista de Datos Departamento":["departamento",'/apps/app_departamento'],
              "Comparativo entre Municipios":["comparativo-municipios",'/apps/app_comparativo_municipios'],
              "comparativo entre Provincias":["comparativo-provincias",'/apps/app_comparativo_provincias']}

#Vamos a crear cada uno de los ítems dentro del menú de la Barra de Navegación
dropdown_items = []
#agregamos los items para cada vista
opciones_drop = []
for nom_drop in vistas_dict.keys():
    comp_id = vistas_dict[nom_drop][0]+"-vista-id"
    link_interno = vistas_dict[nom_drop][1]
    opciones_drop.append({'label':nom_drop,'value':link_interno})

drop_vistas = dcc.Dropdown(id='dropdown-vistas-barra',
                           options=opciones_drop,
                           value='/apps/app_departamento')


#agregamos los links a documentos internos
links = []
links.append(dbc.NavItem(dbc.NavLink("Manual Técnico",external_link=True,
                                     href="/assets/manual_tecnico.html")))
links.append(dbc.NavItem(dbc.NavLink("Ejemplos",external_link=True,
                                     href="/assets/ejemplos.html")))


#Método para crear la barra de navegación en cada vista
def crear_barra_navegacion(nom_vista):
    nom_barra = "Dashboard de Seguridad de Cundinamarca: "+nom_vista
    contenido = links + [drop_vistas]
    navbar = dbc.NavbarSimple(contenido,
                              brand=nom_barra,
                              brand_href="#",
                              color="dark",
                              dark=True,
                              fluid=True)
    barra_nav = html.Div(navbar,
                     style={"width":"100%"})
    return barra_nav


#vamos a crear el BackEnd de la aplicación
backend = BackEnd()

