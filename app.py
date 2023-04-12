import pandas as pd
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output, State


# Crear DAshboard
app = dash.Dash(external_stylesheets=[dbc.themes.SKETCHY])


#Cálculos definidos
df_contientes= pd.read_csv("continents-according-to-our-world-in-data.csv")

df= pd.read_csv("ghg-emissions-by-sector.csv")

df= df[df["Year"]==2019]
df_datosContientes= df.merge(df_contientes, on='Entity')
df_datosContientesMelt= pd.melt(df_datosContientes, id_vars=["Entity","Continent"], value_vars=['Agricultura', 'Uso de tierras y bosques',
       'Desechos', 'Industria', 'Manufactura y Construccion', 'Transporte',
       'Electricidad y Calor', 'Construcciones', 'Emisiones Residuales',
       'Otros Combustibles', 'Aviacion y Envio'])
df_datosContientesMelt[df_datosContientesMelt["value"]<=0]=0
df_datosContientesMelt= df_datosContientesMelt[df_datosContientesMelt["Entity"]!=0]
df_sectores= (df_datosContientesMelt.groupby("variable").sum()).iloc[1:].reset_index()

dfpc= pd.read_csv("per-capita-ghg-sector.csv")
dfpc= dfpc[dfpc["Year"]==2019]
df_datosContientespc= dfpc.merge(df_contientes, on='Entity')
df_datosContientesMeltpc= pd.melt(df_datosContientespc, id_vars=["Entity","Continent"], value_vars=['Aviacion y Envio (per capita)',
       'Uso de tierras y bosques (per capita)',
       'Manufactura y Construccion (per capita)',
       'Emisiones Residuales (per capita)', 'Agricultura (per capita)',
       'Construcciones (per capita)', 'Electricidad y Calor (per capita)',
       'Industria (per capita)', 'Transporte (per capita)',
       'Desechos (per capita)'])
df_datosContientesMeltpc[df_datosContientesMeltpc["value"]<=0]=0.0001

df_sectorPaispc= df_datosContientesMeltpc.groupby(["variable","Entity"]).sum().reset_index()
df_sectorPaispc[df_sectorPaispc["value"]<=0]=0.1

df_paisConsulta= pd.read_csv("consultaPaises.csv")
df_paisConsultapc= pd.read_csv("consultaPaisesPerCapita.csv")

def getRanks(sector, pais):
  df_temp= df_paisConsulta[df_paisConsulta["variable"]==sector]
  print(df_temp)
  df_tempSect= df_temp.sort_values(by="Porcentaje Sector", ascending=False).reset_index()
  rankMundial= (df_tempSect[df_tempSect["Entity"]==pais].index+1)[0]
  df_tempCont= df_temp.sort_values(by="Porcentaje Sector Continenete", ascending=False).reset_index()
  rankCont= (df_tempCont[df_tempCont["Entity"]=="United States"].index+1)[0]
  porcentajeMundial= df_temp[df_paisConsulta["Entity"]==pais]["Porcentaje Sector"].iloc[0]
  porcentajeCont= df_temp[df_paisConsulta["Entity"]==pais]["Porcentaje Sector Continenete"].iloc[0]
  print(rankMundial, round(porcentajeMundial,2))
  print(rankCont, round(porcentajeCont,2))

  df_temppc= df_paisConsultapc[df_paisConsultapc["variable"]==(sector+ " (per capita)")]
  df_tempSectpc= df_temppc.sort_values(by="Porcentaje Sector", ascending=False).reset_index()
  rankMundialpc= (df_tempSectpc[df_tempSectpc["Entity"]==pais].index+1)[0]
  df_tempContpc= df_temppc.sort_values(by="Porcentaje Sector Continenete", ascending=False).reset_index()
  rankContpc= (df_tempContpc[df_tempContpc["Entity"]=="United States"].index+1)[0]
  porcentajeMundialpc= df_temppc[df_paisConsultapc["Entity"]==pais]["Porcentaje Sector"].iloc[0]
  porcentajeContpc= df_temppc[df_paisConsultapc["Entity"]==pais]["Porcentaje Sector Continenete"].iloc[0]
  print(rankMundialpc, round(porcentajeMundialpc,2))
  print(rankContpc, round(porcentajeContpc,2))
  return(rankMundial, round(porcentajeMundial,2),rankCont, round(porcentajeCont,2),rankMundialpc, round(porcentajeMundialpc,2), rankContpc, round(porcentajeContpc,2))

df_sectorPais= df_datosContientesMelt.groupby(["variable","Entity"]).sum().reset_index()
df_sectorPais[df_sectorPais["value"]<=0]=0.1

listaPaises= df_datosContientes.sort_values(by="Entity")["Entity"]
sectores= ['Agricultura', 'Uso de tierras y bosques',
       'Desechos', 'Industria', 'Manufactura y Construccion', 'Transporte',
       'Electricidad y Calor', 'Construcciones', 'Emisiones Residuales',
       'Otros Combustibles', 'Aviacion y Envio']

#Gráficos definidos
figSectores = px.treemap(df_sectores, path=[px.Constant("Sectores"),"variable"], values='value',
                  color='value',color_continuous_scale='YlOrRd', height=600,
                  title="Emisiones de Gases efecto Invernadero por sectores (toneladas de C02)")
figSectores.update_layout(margin = dict(t=50, l=25, r=25, b=25))

figContinente = px.treemap(df_datosContientesMelt.groupby(["variable","Continent"]).sum().reset_index(), 
                 path=[px.Constant("Sectores"),"variable", "Continent"], values='value',
                 color='value',color_continuous_scale='YlOrRd', height=600,
                 title="Emisiones de Gases efecto Invernadero por sectores en cada continente (toneladas de C02)")
figContinente.update_layout(margin = dict(t=50, l=25, r=25, b=25))

figSectoresPais = px.treemap(df_sectorPais, 
                 path=[px.Constant("Sectores"),"variable", "Entity"], values='value',
                 color='value',color_continuous_scale='YlOrRd',height=700, 
                 title="Emisiones de Gases efecto Invernadero por sectores de cada país (toneladas de C02)")
figSectoresPais.update_layout(margin = dict(t=50, l=25, r=25, b=25))

figSectoresPaispc = px.treemap(df_sectorPaispc, 
                 path=[px.Constant("Sectores"),"variable", "Entity"], values='value',
                 color='value',color_continuous_scale='YlOrRd',height=700, 
                 title="Emisiones de Gases efecto Invernadero por sectores de cada país per cápita (toneladas de C02)")
figSectoresPaispc.update_layout(margin = dict(t=50, l=25, r=25, b=25))

#Dashboard
app.layout = html.Div(children=[
    dbc.NavbarSimple(
    children=[
            dbc.NavItem(dbc.NavLink("SAIDM CEM", href="https://www.instagram.com/saidm.cem/?igshid=YmMyMTA2M2Y=")),
            dbc.NavItem(dbc.NavLink("Calculadora Huella Ecológica", href="https://www.footprintcalculator.org/home/es")),
            ],
        brand="Detectives Medioambientales",
        brand_href="#",
        color="primary",
        dark=True,
        fluid=True),

    html.Br(),
        
    dbc.Col([
        
        dbc.Tabs([
            dbc.Tab([
                
                html.Br(),  

                html.H1("Sectores que generan emisiones de gases de efecto invernadero"),

                html.H2("Ingrese el procentaje que cree le corresponde a cada sector"),

                html.Br(),

                dbc.Row([
                    dbc.Col([
    
                        dbc.Row([
                            

                            dbc.Col([
                                html.H5("Agricultura")
                            ], width=3),

                            dbc.Col([
                                dcc.Slider(id="sliderAgricultura", min=0, max=50, step=1, value=10,
                                           tooltip={"placement": "bottom", "always_visible": True},
                                           marks={0:0, 10:10, 20:20, 30:30, 40:40, 50:50})
                            ], width=4), 

                            dbc.Col([
                                html.Div(id="RespuestaAgricultura",children=[html.P("Tienes un error del __%")])
                            ], width=5)
                        ]),
                        dbc.Row([
                            

                            dbc.Col([
                                html.H5("Aviación y Envío")
                            ], width=3),

                            dbc.Col([
                                dcc.Slider(id="sliderAvicionEnvio", min=0, max=50, step=1, value=10,
                                           tooltip={"placement": "bottom", "always_visible": True},
                                           marks={0:0, 10:10, 20:20, 30:30, 40:40, 50:50})
                            ], width=4), 

                            dbc.Col([
                                html.Div(id="RespuestaAviación",children=[html.P("Tienes un error del __%")])
                            ], width=5)
                        ]),

                        dbc.Row([
                            dbc.Col([
                                html.H5("Construcciones")
                            ], width=3),

                            dbc.Col([
                                dcc.Slider(id="sliderConstrucciones", min=0, max=50, step=1, value=10,
                                           tooltip={"placement": "bottom", "always_visible": True},
                                           marks={0:0, 10:10, 20:20, 30:30, 40:40, 50:50})
                            ], width=4),

                            dbc.Col([
                                html.Div(id="RespuestaConstrucciones",children=[html.P("Tienes un error del __%")])
                            ], width=5)
                        ]),

                        dbc.Row([
                            dbc.Col([
                                html.H5("Electricicdad y calor")
                            ], width=3),

                            dbc.Col([
                                dcc.Slider(id="sliderElectricidad", min=0, max=50, step=1, value=10,
                                           tooltip={"placement": "bottom", "always_visible": True},
                                           marks={0:0, 10:10, 20:20, 30:30, 40:40, 50:50})
                            ], width=4),

                            dbc.Col([
                                html.Div(id="RespuestaElectricidad",children=[html.P("Tienes un error del __%")])
                            ], width=5)
                        ]),


                        dbc.Row([
                            dbc.Col([
                                html.H5("Emisiones residuales")
                            ], width=3),

                            dbc.Col([
                                dcc.Slider(id="sliderEmisiones", min=0, max=50, step=1, value=10,
                                           tooltip={"placement": "bottom", "always_visible": True},
                                           marks={0:0, 10:10, 20:20, 30:30, 40:40, 50:50})
                            ], width=4),

                            dbc.Col([
                                html.Div(id="RespuestaEmisiones",children=[html.P("Tienes un error del __%")])
                            ], width=5)
                        ]),

                        dbc.Row([
                            dbc.Col([
                                html.H5("Industria")
                            ], width=3),

                            dbc.Col([
                                dcc.Slider(id="sliderIndustria", min=0, max=50, step=1, value=10,
                                           tooltip={"placement": "bottom", "always_visible": True},
                                           marks={0:0, 10:10, 20:20, 30:30, 40:40, 50:50})
                            ], width=4),

                            dbc.Col([
                                html.Div(id="RespuestaIndustria",children=[html.P("Tienes un error del __%")])
                            ], width=5)
                        ]),

                        dbc.Row([
                            dbc.Col([
                                html.H5("Uso de tierras y bosques")
                            ], width=3),

                            dbc.Col([
                                dcc.Slider(id="sliderTierras", min=0, max=50, step=1, value=10,
                                           tooltip={"placement": "bottom", "always_visible": True},
                                           marks={0:0, 10:10, 20:20, 30:30, 40:40, 50:50})
                            ], width=4),

                            dbc.Col([
                                html.Div(id="RespuestaTierras",children=[html.P("Tienes un error del __%")])
                            ], width=5)
                        ]),

                        dbc.Row([
                            dbc.Col([
                                html.H5("Manufactura y Construcción")
                            ], width=3),

                            dbc.Col([
                                dcc.Slider(id="sliderManufactura", min=0, max=50, step=1, value=10,
                                           tooltip={"placement": "bottom", "always_visible": True},
                                           marks={0:0, 10:10, 20:20, 30:30, 40:40, 50:50})
                            ], width=4),

                            dbc.Col([
                                html.Div(id="RespuestaManufactura",children=[html.P("Tienes un error del __%")])
                            ], width=5)
                        ]),

                        dbc.Row([
                            dbc.Col([
                                html.H5("Transporte")
                            ], width=3),

                            dbc.Col([
                                dcc.Slider(id="sliderTransporte", min=0, max=50, step=1, value=10,
                                           tooltip={"placement": "bottom", "always_visible": True},
                                           marks={0:0, 10:10, 20:20, 30:30, 40:40, 50:50})
                            ], width=4),

                            dbc.Col([
                                html.Div(id="RespuestaTransporte",children=[html.P("Tienes un error del __%")])
                            ], width=5)
                        ]),

                        dbc.Row([
                            dbc.Col([
                                html.H5("Desechos")
                            ], width=3),

                            dbc.Col([
                                dcc.Slider(id="sliderDesechos", min=0, max=50, step=1, value=10,
                                           tooltip={"placement": "bottom", "always_visible": True},
                                           marks={0:0, 10:10, 20:20, 30:30, 40:40, 50:50})
                            ], width=4),

                            dbc.Col([
                                html.Div(id="RespuestaDesecho",children=[html.P("Tienes un error del __%")])
                            ], width=5)
                        ]),

                        dbc.Row([
                            dbc.Col([
                                html.H5("Otros Combustibles")
                            ], width=3),

                            dbc.Col([
                                dcc.Slider(id="sliderOtros", min=0, max=50, step=1, value=10,
                                           tooltip={"placement": "bottom", "always_visible": True},
                                           marks={0:0, 10:10, 20:20, 30:30, 40:40, 50:50})
                            ], width=4),

                            dbc.Col([
                                html.Div(id="RespuestaOtros",children=[html.P("Tienes un error del __%")])
                            ], width=5)
                        ]),

                        dbc.Button("Comprobar Respuestas", color="primary", id="VerSectores"),

                        html.Br(),

                        html.Br(),

                        html.H1("Gráfico de las emisiones de gases por sectores"),

                        dcc.Graph(figure=figSectores)
                        
                        
                        ], width=12),

                ])



            ],label="Sectores",
            
            style={'margin-right': '5px', 'margin-left': '5px'}),

            # CONTIENTES -----------------------------------------------------------------

            dbc.Tab([
                dbc.Col([

                    html.Br(),

                    html.H1("Emisiones de Gases de Efecto Invernadero en cada sector por Continente"),

                    dbc.Row([
                        dbc.Col([
                            html.H4("Electricidad y Calor", style={'textAlign': 'center'}),
                            dbc.Select(id="Electricidad1",
                            options=[
                                {"label": "Africa", "value": "Africa"},
                                {"label": "Asia", "value": "Asia"},
                                {"label": "Europa", "value": "Europe"},
                                {"label":"Norte América", "value":"North America"},
                                {"label":"Sudamérica", "value":"South America"},
                                {"label":"Oceania", "value":"Oceania"}
                            ], placeholder="Continente 1"),

                            html.Br(),

                            dbc.Select(id="Electricidad2",
                            options=[
                                {"label": "Africa", "value": "Africa"},
                                {"label": "Asia", "value": "Asia"},
                                {"label": "Europa", "value": "Europe"},
                                {"label":"Norte América", "value":"North America"},
                                {"label":"Sudamérica", "value":"South America"},
                                {"label":"Oceania", "value":"Oceania"}
                            ], placeholder="Continente 2"),

                            html.Br(),

                            dbc.Select(id="Electricidad3",
                            options=[
                                {"label": "Africa", "value": "Africa"},
                                {"label": "Asia", "value": "Asia"},
                                {"label": "Europa", "value": "Europe"},
                                {"label":"Norte América", "value":"North America"},
                                {"label":"Sudamérica", "value":"South America"},
                                {"label":"Oceania", "value":"Oceania"}
                            ], placeholder="Continente 3"),

                            html.Br(),

                            dbc.Select(id="Electricidad4",
                            options=[
                                {"label": "Africa", "value": "Africa"},
                                {"label": "Asia", "value": "Asia"},
                                {"label": "Europa", "value": "Europe"},
                                {"label":"Norte América", "value":"North America"},
                                {"label":"Sudamérica", "value":"South America"},
                                {"label":"Oceania", "value":"Oceania"}
                            ], placeholder="Continente 4"),

                            html.Br(),

                            dbc.Select(id="Electricidad5",
                            options=[
                                {"label": "Africa", "value": "Africa"},
                                {"label": "Asia", "value": "Asia"},
                                {"label": "Europa", "value": "Europe"},
                                {"label":"Norte América", "value":"North America"},
                                {"label":"Sudamérica", "value":"South America"},
                                {"label":"Oceania", "value":"Oceania"}
                            ], placeholder="Continente 5"),

                            html.Br(),

                            dbc.Select(id="Electricidad6",
                            options=[
                                {"label": "Africa", "value": "Africa"},
                                {"label": "Asia", "value": "Asia"},
                                {"label": "Europa", "value": "Europe"},
                                {"label":"Norte América", "value":"North America"},
                                {"label":"Sudamérica", "value":"South America"},
                                {"label":"Oceania", "value":"Oceania"}
                            ], placeholder="Continente 6"),

                            html.Br(),

                            dbc.Button("Comprobar Respuestas", color="primary", id="VerContinente1"),

                            html.Br(),

                            html.Div(id="RespuestaCont1",children=[html.P("Tienes _ errores")])

                        ], width=3),

                        dbc.Col([
                            html.H4("Transporte", style={'textAlign': 'center'}),
                            dbc.Select(id="Transporte1",
                            options=[
                                {"label": "Africa", "value": "Africa"},
                                {"label": "Asia", "value": "Asia"},
                                {"label": "Europa", "value": "Europe"},
                                {"label":"Norte América", "value":"North America"},
                                {"label":"Sudamérica", "value":"South America"},
                                {"label":"Oceania", "value":"Oceania"}
                            ], placeholder="Continente 1"),

                            html.Br(),

                            dbc.Select(id="Transporte2",
                            options=[
                                {"label": "Africa", "value": "Africa"},
                                {"label": "Asia", "value": "Asia"},
                                {"label": "Europa", "value": "Europe"},
                                {"label":"Norte América", "value":"North America"},
                                {"label":"Sudamérica", "value":"South America"},
                                {"label":"Oceania", "value":"Oceania"}
                            ], placeholder="Continente 2"),

                            html.Br(),

                            dbc.Select(id="Transporte3",
                            options=[
                                {"label": "Africa", "value": "Africa"},
                                {"label": "Asia", "value": "Asia"},
                                {"label": "Europa", "value": "Europe"},
                                {"label":"Norte América", "value":"North America"},
                                {"label":"Sudamérica", "value":"South America"},
                                {"label":"Oceania", "value":"Oceania"}
                            ], placeholder="Continente 3"),

                            html.Br(),

                            dbc.Select(id="Transporte4",
                            options=[
                                {"label": "Africa", "value": "Africa"},
                                {"label": "Asia", "value": "Asia"},
                                {"label": "Europa", "value": "Europe"},
                                {"label":"Norte América", "value":"North America"},
                                {"label":"Sudamérica", "value":"South America"},
                                {"label":"Oceania", "value":"Oceania"}
                            ], placeholder="Continente 4"),

                            html.Br(),

                            dbc.Select(id="Transporte5",
                            options=[
                                {"label": "Africa", "value": "Africa"},
                                {"label": "Asia", "value": "Asia"},
                                {"label": "Europa", "value": "Europe"},
                                {"label":"Norte América", "value":"North America"},
                                {"label":"Sudamérica", "value":"South America"},
                                {"label":"Oceania", "value":"Oceania"}
                            ], placeholder="Continente 5"),

                            html.Br(),

                            dbc.Select(id="Transporte6",
                            options=[
                                {"label": "Africa", "value": "Africa"},
                                {"label": "Asia", "value": "Asia"},
                                {"label": "Europa", "value": "Europe"},
                                {"label":"Norte América", "value":"North America"},
                                {"label":"Sudamérica", "value":"South America"},
                                {"label":"Oceania", "value":"Oceania"}
                            ], placeholder="Continente 6"),

                            html.Br(),

                            dbc.Button("Comprobar Respuestas", color="primary", id="VerContinente2"),

                            html.Br(),

                            html.Div(id="RespuestaCont2",children=[html.P("Tienes _ errores")])

                        ], width=3),

                        dbc.Col([
                            html.H4("Manufactura y Construcción", style={'textAlign': 'center'}),
                            dbc.Select(id="Manufactura1",
                            options=[
                                {"label": "Africa", "value": "Africa"},
                                {"label": "Asia", "value": "Asia"},
                                {"label": "Europa", "value": "Europe"},
                                {"label":"Norte América", "value":"North America"},
                                {"label":"Sudamérica", "value":"South America"},
                                {"label":"Oceania", "value":"Oceania"}
                            ], placeholder="Continente 1"),

                            html.Br(),

                            dbc.Select(id="Manufactura2",
                            options=[
                                {"label": "Africa", "value": "Africa"},
                                {"label": "Asia", "value": "Asia"},
                                {"label": "Europa", "value": "Europe"},
                                {"label":"Norte América", "value":"North America"},
                                {"label":"Sudamérica", "value":"South America"},
                                {"label":"Oceania", "value":"Oceania"}
                            ], placeholder="Continente 2"),

                            html.Br(),

                            dbc.Select(id="Manufactura3",
                            options=[
                                {"label": "Africa", "value": "Africa"},
                                {"label": "Asia", "value": "Asia"},
                                {"label": "Europa", "value": "Europe"},
                                {"label":"Norte América", "value":"North America"},
                                {"label":"Sudamérica", "value":"South America"},
                                {"label":"Oceania", "value":"Oceania"}
                            ], placeholder="Continente 3"),

                            html.Br(),

                            dbc.Select(id="Manufactura4",
                            options=[
                                {"label": "Africa", "value": "Africa"},
                                {"label": "Asia", "value": "Asia"},
                                {"label": "Europa", "value": "Europe"},
                                {"label":"Norte América", "value":"North America"},
                                {"label":"Sudamérica", "value":"South America"},
                                {"label":"Oceania", "value":"Oceania"}
                            ], placeholder="Continente 4"),

                            html.Br(),

                            dbc.Select(id="Manufactura5",
                            options=[
                                {"label": "Africa", "value": "Africa"},
                                {"label": "Asia", "value": "Asia"},
                                {"label": "Europa", "value": "Europe"},
                                {"label":"Norte América", "value":"North America"},
                                {"label":"Sudamérica", "value":"South America"},
                                {"label":"Oceania", "value":"Oceania"}
                            ], placeholder="Continente 5"),

                            html.Br(),

                            dbc.Select(id="Manufactura6",
                            options=[
                                {"label": "Africa", "value": "Africa"},
                                {"label": "Asia", "value": "Asia"},
                                {"label": "Europa", "value": "Europe"},
                                {"label":"Norte América", "value":"North America"},
                                {"label":"Sudamérica", "value":"South America"},
                                {"label":"Oceania", "value":"Oceania"}
                            ], placeholder="Continente 6"),

                            html.Br(),

                            dbc.Button("Comprobar Respuestas", color="primary", id="VerContinente3"),

                            html.Br(),

                            html.Div(id="RespuestaCont3",children=[html.P("Tienes _ errores")])

                        ], width=3),

                        dbc.Col([
                            html.H4("Agricultura", style={'textAlign': 'center'}),
                            dbc.Select(id="Agricultura1",
                            options=[
                                {"label": "Africa", "value": "Africa"},
                                {"label": "Asia", "value": "Asia"},
                                {"label": "Europa", "value": "Europe"},
                                {"label":"Norte América", "value":"North America"},
                                {"label":"Sudamérica", "value":"South America"},
                                {"label":"Oceania", "value":"Oceania"}
                            ], placeholder="Continente 1"),

                            html.Br(),

                            dbc.Select(id="Agricultura2",
                            options=[
                                {"label": "Africa", "value": "Africa"},
                                {"label": "Asia", "value": "Asia"},
                                {"label": "Europa", "value": "Europe"},
                                {"label":"Norte América", "value":"North America"},
                                {"label":"Sudamérica", "value":"South America"},
                                {"label":"Oceania", "value":"Oceania"}
                            ], placeholder="Continente 2"),

                            html.Br(),

                            dbc.Select(id="Agricultura3",
                            options=[
                                {"label": "Africa", "value": "Africa"},
                                {"label": "Asia", "value": "Asia"},
                                {"label": "Europa", "value": "Europe"},
                                {"label":"Norte América", "value":"North America"},
                                {"label":"Sudamérica", "value":"South America"},
                                {"label":"Oceania", "value":"Oceania"}
                            ], placeholder="Continente 3"),

                            html.Br(),

                            dbc.Select(id="Agricultura4",
                            options=[
                                {"label": "Africa", "value": "Africa"},
                                {"label": "Asia", "value": "Asia"},
                                {"label": "Europa", "value": "Europe"},
                                {"label":"Norte América", "value":"North America"},
                                {"label":"Sudamérica", "value":"South America"},
                                {"label":"Oceania", "value":"Oceania"}
                            ], placeholder="Continente 4"),

                            html.Br(),

                            dbc.Select(id="Agricultura5",
                            options=[
                                {"label": "Africa", "value": "Africa"},
                                {"label": "Asia", "value": "Asia"},
                                {"label": "Europa", "value": "Europe"},
                                {"label":"Norte América", "value":"North America"},
                                {"label":"Sudamérica", "value":"South America"},
                                {"label":"Oceania", "value":"Oceania"}
                            ], placeholder="Continente 5"),

                            html.Br(),

                            dbc.Select(id="Agricultura6",
                            options=[
                                {"label": "Africa", "value": "Africa"},
                                {"label": "Asia", "value": "Asia"},
                                {"label": "Europa", "value": "Europe"},
                                {"label":"Norte América", "value":"North America"},
                                {"label":"Sudamérica", "value":"South America"},
                                {"label":"Oceania", "value":"Oceania"}
                            ], placeholder="Continente 6"),

                            html.Br(),

                            dbc.Button("Comprobar Respuestas", color="primary", id="VerContinente4"),

                            html.Br(),

                            html.Div(id="RespuestaCont4",children=[html.P("Tienes _ errores")])

                        ], width=3)
                    ]),

                    html.H1("Gráfico de las emisiones de gases por sector en cada contienente"),

                    dcc.Graph(figure=figContinente)
                ])
            ],label="Continentes", style={'margin-right': '5px', 'margin-left': '5px'}),

            dbc.Tab([
                
                html.Br(),

                html.H1("Emisiones de gases en cada sector por país"),

                dbc.Row([
    
                    dbc.Col([
                        dbc.Select(id="Sector",
                            options=sectores, placeholder="Seleccione un sector")
                    ], width=3),

                    dbc.Col([
                        dbc.Select(id="Pais",
                            options=listaPaises, placeholder="Seleccione un país")
                    ], width=3),

                    dbc.Col([
                        dbc.Button("Comprobar Respuestas", color="primary", id="VerPais")
                    ])
                ]),

                html.Br(),

                dbc.Row([
                    dbc.Col([
                        dbc.Card(
                            dbc.CardBody([
                                    html.H2("???", id= "rankMundial", style={"color":"white"}),
                                    html.P("Ranking mundial de emisiones del país en el sector", style={"color":"white"})]
                            ), color="primary"
                        )
                    ], width=3),

                    dbc.Col([
                        dbc.Card(
                            dbc.CardBody([
                                    html.H2("???", id= "porcMundial", style={"color":"white"}),
                                    html.P("Porcentaje mundial de emisiones del país en el sector", style={"color":"white"})]
                            ), color="primary"
                        )
                    ], width=3),

                    dbc.Col([
                        dbc.Card(
                            dbc.CardBody([
                                    html.H2("???", id= "rankContinente", style={"color":"white"}),
                                    html.P("Ranking del continente de emisiones del país en el sector", style={"color":"white"})]
                            ), color="primary"
                        )
                    ], width=3),

                    dbc.Col([
                        dbc.Card(
                            dbc.CardBody([
                                    html.H2("???", id= "porcContinente", style={"color":"white"}),
                                    html.P("Porcentaje del continente de emisiones del país en el sector", style={"color":"white"})]
                            ), color="primary"
                        )
                    ], width=3)
                ]),

                html.Br(),

                dbc.Row([
                    dbc.Col([dbc.Input(placeholder="", size="lg")], width=3),

                    dbc.Col([dbc.Input(placeholder="", size="lg")], width=3),

                    dbc.Col([dbc.Input(placeholder="", size="lg")], width=3),

                    dbc.Col([dbc.Input(placeholder="", size="lg")], width=3)
                ]),

                html.Br(),

                dbc.Row([
                    dbc.Col([
                        dbc.Card(
                            dbc.CardBody([
                                    html.H2("???", id= "rankMundialpc", style={"color":"white"}),
                                    html.P("Ranking mundial de emisiones per capita del país en el sector", style={"color":"white"})]
                            ), color="primary"
                        )
                    ], width=3),

                    dbc.Col([
                        dbc.Card(
                            dbc.CardBody([
                                    html.H2("???", id= "porcMundialpc", style={"color":"white"}),
                                    html.P("Porcentaje mundial de emisiones per capita del país en el sector", style={"color":"white"})]
                            ), color="primary"
                        )
                    ], width=3),

                    dbc.Col([
                        dbc.Card(
                            dbc.CardBody([
                                    html.H2("???", id= "rankContinentepc", style={"color":"white"}),
                                    html.P("Ranking del continente de emisiones per capita del país en el sector", style={"color":"white"})]
                            ), color="primary"
                        )
                    ], width=3),

                    dbc.Col([
                        dbc.Card(
                            dbc.CardBody([
                                    html.H2("???", id= "porcContinentepc", style={"color":"white"}),
                                    html.P("Porcentaje del continente de emisiones per capita del país en el sector", style={"color":"white"})]
                            ), color="primary"
                        )
                    ], width=3)
                ]),

                html.Br(),

                dbc.Row([
                    dbc.Col([dbc.Input(placeholder="", size="lg")], width=3),

                    dbc.Col([dbc.Input(placeholder="", size="lg")], width=3),

                    dbc.Col([dbc.Input(placeholder="", size="lg")], width=3),

                    dbc.Col([dbc.Input(placeholder="", size="lg")], width=3)
                ]),

                html.Br(),

                dcc.Graph(figure=figSectoresPais),

                dcc.Graph(figure=figSectoresPaispc),
                
            ],label="Países", style={'margin-right': '5px', 'margin-left': '5px'})

        ])

    ],style={'margin-right': '20px', 'margin-left': '20px'})  
 
        ])

@app.callback(Output('RespuestaAgricultura', 'children'),
              [Input('VerSectores', 'n_clicks')],
              [State('sliderAgricultura', 'value')])
def update_output(n_clicks, sliderAgricultura):
    if n_clicks > 0:
        valor=abs(round(sliderAgricultura-11))
        return("Te equivocaste por "+str(valor)+"%")
    else:
        return ''
    
@app.callback(Output('RespuestaAviación', 'children'),
              [Input('VerSectores', 'n_clicks')],
              [State('sliderAvicionEnvio', 'value')])
def update_output(n_clicks, sliderAgricultura):
    if n_clicks > 0:
        valor=abs(round(sliderAgricultura-3))
        return("Te equivocaste por "+str(valor)+"%")
    else:
        return ''
    
@app.callback(Output('RespuestaConstrucciones', 'children'),
              [Input('VerSectores', 'n_clicks')],
              [State('sliderConstrucciones', 'value')])
def update_output(n_clicks, sliderAgricultura):
    if n_clicks > 0:
        valor=abs(round(sliderAgricultura-6))
        return("Te equivocaste por "+str(valor)+"%")
    else:
        return ''
    
@app.callback(Output('RespuestaElectricidad', 'children'),
              [Input('VerSectores', 'n_clicks')],
              [State('sliderElectricidad', 'value')])
def update_output(n_clicks, sliderAgricultura):
    if n_clicks > 0:
        valor=abs(round(sliderAgricultura-31))
        return("Te equivocaste por "+str(valor)+"%")
    else:
        return ''
    
@app.callback(Output('RespuestaEmisiones', 'children'),
              [Input('VerSectores', 'n_clicks')],
              [State('sliderEmisiones', 'value')])
def update_output(n_clicks, sliderAgricultura):
    if n_clicks > 0:
        valor=abs(round(sliderAgricultura-7))
        return("Te equivocaste por "+str(valor)+"%")
    else:
        return ''
    
@app.callback(Output('RespuestaIndustria', 'children'),
              [Input('VerSectores', 'n_clicks')],
              [State('sliderIndustria', 'value')])
def update_output(n_clicks, sliderAgricultura):
    if n_clicks > 0:
        valor=abs(round(sliderAgricultura-6))
        return("Te equivocaste por "+str(valor)+"%")
    else:
        return ''
    
@app.callback(Output('RespuestaTierras', 'children'),
              [Input('VerSectores', 'n_clicks')],
              [State('sliderTierras', 'value')])
def update_output(n_clicks, sliderAgricultura):
    if n_clicks > 0:
        valor=abs(round(sliderAgricultura-7))
        return("Te equivocaste por "+str(valor)+"%")
    else:
        return ''
    
@app.callback(Output('RespuestaManufactura', 'children'),
              [Input('VerSectores', 'n_clicks')],
              [State('sliderManufactura', 'value')])
def update_output(n_clicks, sliderAgricultura):
    if n_clicks > 0:
        valor=abs(round(sliderAgricultura-12))
        return("Te equivocaste por "+str(valor)+"%")
    else:
        return ''
    
@app.callback(Output('RespuestaTransporte', 'children'),
              [Input('VerSectores', 'n_clicks')],
              [State('sliderTransporte', 'value')])
def update_output(n_clicks, sliderAgricultura):
    if n_clicks > 0:
        valor=abs(round(sliderAgricultura-13))
        return("Te equivocaste por "+str(valor)+"%")
    else:
        return ''
    
@app.callback(Output('RespuestaDesecho', 'children'),
              [Input('VerSectores', 'n_clicks')],
              [State('sliderDesechos', 'value')])
def update_output(n_clicks, sliderAgricultura):
    if n_clicks > 0:
        valor=abs(round(sliderAgricultura-3))
        return("Te equivocaste por "+str(valor)+"%")
    else:
        return ''
    
@app.callback(Output('RespuestaOtros', 'children'),
              [Input('VerSectores', 'n_clicks')],
              [State('sliderOtros', 'value')])
def update_output(n_clicks, sliderAgricultura):
    if n_clicks > 0:
        valor=abs(round(sliderAgricultura-1))
        return("Te equivocaste por "+str(valor)+"%")
    else:
        return ''
    

@app.callback(Output('RespuestaCont1', 'children'),
              [Input('VerContinente1', 'n_clicks')],
              [State('Electricidad1', 'value'),
               State('Electricidad2', 'value'),
               State('Electricidad3', 'value'),
               State('Electricidad4', 'value'),
               State('Electricidad5', 'value'),
               State('Electricidad6', 'value')])
def update_output(n_clicks, valor1, valor2, valor3, valor4, valor5, valor6):
    if n_clicks > 0:
        errores=0
        if(valor1!="Asia"): errores+=1
        if(valor2!="North America"): errores+=1
        if(valor3!="Europe"): errores+=1
        if(valor4!="Africa"): errores+=1
        if(valor5!="South America"): errores+=1
        if(valor6!="Oceania"): errores+=1

        return ("Tienes "+str(errores)+" errores")
    else:
        return ''
    
@app.callback(Output('RespuestaCont2', 'children'),
              [Input('VerContinente2', 'n_clicks')],
              [State('Transporte1', 'value'),
               State('Transporte2', 'value'),
               State('Transporte3', 'value'),
               State('Transporte4', 'value'),
               State('Transporte5', 'value'),
               State('Transporte6', 'value')])
def update_output(n_clicks, valor1, valor2, valor3, valor4, valor5, valor6):
    if n_clicks > 0:
        errores=0
        if(valor1!="Asia"): errores+=1
        if(valor2!="North America"): errores+=1
        if(valor3!="Europe"): errores+=1
        if(valor4!="South America"): errores+=1
        if(valor5!="Africa"): errores+=1
        if(valor6!="Oceania"): errores+=1

        return ("Tienes "+str(errores)+" errores")
    else:
        return ''
    
@app.callback(Output('RespuestaCont3', 'children'),
              [Input('VerContinente3', 'n_clicks')],
              [State('Manufactura1', 'value'),
               State('Manufactura2', 'value'),
               State('Manufactura3', 'value'),
               State('Manufactura4', 'value'),
               State('Manufactura5', 'value'),
               State('Manufactura6', 'value')])
def update_output(n_clicks, valor1, valor2, valor3, valor4, valor5, valor6):
    if n_clicks > 0:
        errores=0
        if(valor1!="Asia"): errores+=1
        if(valor2!="Europe"): errores+=1
        if(valor3!="North America"): errores+=1
        if(valor4!="South America"): errores+=1
        if(valor5!="Africa"): errores+=1
        if(valor6!="Oceania"): errores+=1

        return ("Tienes "+str(errores)+" errores")
    else:
        return ''

@app.callback(Output('RespuestaCont4', 'children'),
              [Input('VerContinente4', 'n_clicks')],
              [State('Agricultura1', 'value'),
               State('Agricultura2', 'value'),
               State('Agricultura3', 'value'),
               State('Agricultura4', 'value'),
               State('Agricultura5', 'value'),
               State('Agricultura6', 'value')])
def update_output(n_clicks, valor1, valor2, valor3, valor4, valor5, valor6):
    if n_clicks > 0:
        errores=0
        if(valor1!="Asia"): errores+=1
        if(valor2!="Africa"): errores+=1
        if(valor3!="South America"): errores+=1
        if(valor4!="Europe"): errores+=1
        if(valor5!="North America"): errores+=1
        if(valor6!="Oceania"): errores+=1

        return ("Tienes "+str(errores)+" errores")
    else:
        return ''
    
@app.callback(Output('rankMundial', 'children'),
              [Input('VerPais', 'n_clicks')],
              [State('Pais', 'value'),
               State('Sector', 'value')])
def update_output(n_clicks, pais, sector):
    if n_clicks > 0:
        
        rankMundial, procMundial, rankContinente, procContinente, rankMundialpc, procMundialpc, rankContinentepc, procContinentepc= getRanks(sector, pais)
        return("# "+str(rankMundial))
    else:
        return ''
    
@app.callback(Output('porcMundial', 'children'),
              [Input('VerPais', 'n_clicks')],
              [State('Pais', 'value'),
               State('Sector', 'value')])
def update_output(n_clicks, pais, sector):
    if n_clicks > 0:
        
        rankMundial, procMundial, rankContinente, procContinente, rankMundialpc, procMundialpc, rankContinentepc, procContinentepc= getRanks(sector, pais)
        return(str(procMundial)+" %")
    else:
        return ''
    
@app.callback(Output('rankContinente', 'children'),
              [Input('VerPais', 'n_clicks')],
              [State('Pais', 'value'),
               State('Sector', 'value')])
def update_output(n_clicks, pais, sector):
    if n_clicks > 0:
        
        rankMundial, procMundial, rankContinente, procContinente, rankMundialpc, procMundialpc, rankContinentepc, procContinentepc= getRanks(sector, pais)
        return("# "+str(rankContinente))
    else:
        return ''
    
@app.callback(Output('porcContinente', 'children'),
              [Input('VerPais', 'n_clicks')],
              [State('Pais', 'value'),
               State('Sector', 'value')])
def update_output(n_clicks, pais, sector):
    if n_clicks > 0:
        
        rankMundial, procMundial, rankContinente, procContinente, rankMundialpc, procMundialpc, rankContinentepc, procContinentepc= getRanks(sector, pais)
        return(str(procContinente)+" %")
    else:
        return ''
    
@app.callback(Output('rankMundialpc', 'children'),
              [Input('VerPais', 'n_clicks')],
              [State('Pais', 'value'),
               State('Sector', 'value')])
def update_output(n_clicks, pais, sector):
    if n_clicks > 0:
        
        rankMundial, procMundial, rankContinente, procContinente, rankMundialpc, procMundialpc, rankContinentepc, procContinentepc= getRanks(sector, pais)
        return("# "+str(rankMundialpc))
    else:
        return ''
    
@app.callback(Output('porcMundialpc', 'children'),
              [Input('VerPais', 'n_clicks')],
              [State('Pais', 'value'),
               State('Sector', 'value')])
def update_output(n_clicks, pais, sector):
    if n_clicks > 0:
        
        rankMundial, procMundial, rankContinente, procContinente, rankMundialpc, procMundialpc, rankContinentepc, procContinentepc= getRanks(sector, pais)
        return(str(procMundialpc)+" %")
    else:
        return ''
    
@app.callback(Output('rankContinentepc', 'children'),
              [Input('VerPais', 'n_clicks')],
              [State('Pais', 'value'),
               State('Sector', 'value')])
def update_output(n_clicks, pais, sector):
    if n_clicks > 0:
        
        rankMundial, procMundial, rankContinente, procContinente, rankMundialpc, procMundialpc, rankContinentepc, procContinentepc= getRanks(sector, pais)
        return("# "+str(rankContinentepc))
    else:
        return ''
    
@app.callback(Output('porcContinentepc', 'children'),
              [Input('VerPais', 'n_clicks')],
              [State('Pais', 'value'),
               State('Sector', 'value')])
def update_output(n_clicks, pais, sector):
    if n_clicks > 0:
        rankMundial, procMundial, rankContinente, procContinente, rankMundialpc, procMundialpc, rankContinentepc, procContinentepc= getRanks(sector, pais)
        return(str(procContinentepc)+" %")
    else:
        return ''

server= app.server
if __name__ == '__main__':
    app.run_server()