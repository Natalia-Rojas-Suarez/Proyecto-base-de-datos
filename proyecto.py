import psycopg2
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import requests as rq
from Conexion import Connection
import querySQL as sql
#se usan git ccon el mapa de los departamentos de colombia para luego visiaulizarlo en la funcion delitos por departamento
external_stylesheets = ["https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css"]
geojsondepartamentosURL = "https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json"
colombia_departamentos = rq.get(geojsondepartamentosURL).json()


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#Se abre la conexion
con = Connection()
con.openConnection()
conexion = con.cursor()
#se crean las consultas
query = pd.read_sql_query(sql.delitosSexPorDepartamento(), con.connection)
query2 = pd.read_sql_query(sql.Grupo_Etario(), con.connection)
query3 = pd.read_sql_query(sql.genero(), con.connection)
query4 = pd.read_sql_query(sql.delitosSexPorMunicipio(), con.connection)

#se cierra la conexion
con.closeConnection()
#se pasan las consultas de sql a un dataframe de pandas
datosSexsporDepartamento = pd.DataFrame(query, columns=["departamento", "numero_de_delitos"])
datosGrupo_Etario = pd.DataFrame(query2, columns=["grupo_etario", "numeros_casos"])
datosGenero = pd.DataFrame(query3, columns=["genero", "numeros_casos"])
datosdelitosSexPorMunicipio = pd.DataFrame(query4, columns=["municipio", "numero_de_delitos"])

# se usa el dataframe para crear los diagrama barra y torta

hDepartamentosB = px.bar(datosSexsporDepartamento.head(32), x="departamento", y="numero_de_delitos")
hDepartamentosP = px.pie(datosSexsporDepartamento.head(32), names="departamento", values="numero_de_delitos")
hDepartamentosMapa = px.choropleth(datosSexsporDepartamento.head(32), 
                            geojson = colombia_departamentos,
                            locations="departamento",
                            featureidkey="properties.NOMBRE_DPT", 
                            color = "numero_de_delitos"
                            )






hetario = px.pie(datosGrupo_Etario.head(5), names="grupo_etario", values="numeros_casos")


hgeneroP = px.pie(datosGenero.head(5), names="genero", values="numeros_casos")
hgeneroB = px.bar(datosGenero.head(5), x="genero", y="numeros_casos")

hmunicipiosP=px.bar(datosdelitosSexPorMunicipio.head(5), x="municipio", y="numero_de_delitos")

#se muestran los dash en un localhost de html

app.layout = html.Div(children=[
    html.H1(children='Analisis Delitos Sexuales Colombia'),
    html.H2(children='Delitos por departamento'),
    dcc.Graph(
        id='Delitos por departamento Barra',
        figure=hDepartamentosB
    ),
    dcc.Graph(
        id='Delitos por departamento Pie',
        figure=hDepartamentosP
    ),
     dcc.Graph(
        id='Homicidios por departamento Mapa',
        figure=hDepartamentosMapa
    ),


    html.H2(children='Grupos estarios'),
    dcc.Graph(
        id='Grupos estarios',
        figure=hetario
    ),


    html.H2(children='Genero Victimarios'),
    dcc.Graph(
        id='Genero Victimarios Pie',
        figure=hgeneroP
    ),
    dcc.Graph(
        id='Genero  Barras',
        figure=hgeneroB
    ),
    html.H2(children='Municipios'),
    dcc.Graph(
        id='Municipios menos afectados',
        figure=hmunicipiosP
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)