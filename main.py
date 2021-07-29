import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output

#importamos las apps
from app import app
from apps import app_municipio, app_provincia
from apps import app_comparativo_municipios,app_comparativo_provincias,app_departamento

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url','pathname')])
def display_layout(pathname):
    if pathname == '/apps/app_municipio':
        return app_municipio.layout
    elif pathname == '/apps/app_provincia':
        return app_provincia.layout
    elif pathname =='/apps/app_comparativo_municipios':
        return app_comparativo_municipios.layout
    elif pathname == '/apps/app_comparativo_provincias':
        return app_comparativo_provincias.layout
    elif pathname =='/apps/app_departamento':
        return app_departamento.layout
    else:
        return '404'

if __name__ =='__main__':
    app.run_server(debug=False,port=8888)