import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# INICIALITZACIÓ 
# ==========================================

base_dir = os.path.dirname(os.path.abspath(__file__))
dataset_dir = os.path.join(base_dir, "..", "01_dades", "processat")

## Carregar dades d'homicidis i desapareguts
df_sem_prom = pd.read_csv(os.path.join(dataset_dir, "homicidio_doloso_semestral_promedio_diario.csv"), index_col="Año")
df_sem_abs = pd.read_csv(os.path.join(dataset_dir, "homicidio_doloso_semestral_frecuencia_absoluta.csv"), index_col="Año")
df_jul_prom = pd.read_csv(os.path.join(dataset_dir, "homicidio_doloso_Julio_promedio_diario.csv"), index_col="Año")
df_jul_abs = pd.read_csv(os.path.join(dataset_dir, "homicidio_doloso_Julio_frecuencia_absoluta.csv"), index_col="Año")
df_desap_sem = pd.read_csv(os.path.join(dataset_dir, "desaparecidos_semestral.csv"), index_col="Año")

## Inicialitzar l'aplicació de Dash
app = Dash(__name__)

# FUNCIONS HELPER
# ==========================================

def crear_grafic(df_prom, df_abs, tipus, show_desap=False, es_semestre=True):
    fig = go.Figure()
    
    ## Canviar tipus de gràfic
    if tipus == "promig":
        data = df_prom.mean(axis=1)
        fig.add_trace(go.Bar(
            x=data.index, y=data.values,
            name="Homicidios dolosos", marker_color="#3b82f6",
            text=[f"{val:.1f}" for val in data.values], textposition="outside", hoverinfo="skip"
        ))
        titol_eix_y = "Promedio diario de víctimas"
    else:
        data = df_abs.sum(axis=1).fillna(0).astype(int)
        fig.add_trace(go.Bar(
            x=data.index, y=data.values,
            name="Homicidios dolosos", marker_color="#ef4444",
            text=data.values, textposition="outside", hoverinfo="skip"
        ))
        
        ### Afegir desapareguts
        if es_semestre and show_desap and "yes" in show_desap:
            col_name = df_desap_sem.columns[0] if not df_desap_sem.empty else "Desaparecidos"
            desap_values = df_desap_sem[col_name].groupby(level=0).sum().reindex(data.index).fillna(0).astype(int).values
            
            fig.add_trace(go.Scatter(
                x=data.index, y=desap_values,
                name="Desaparecidos", mode="lines+markers+text",
                line=dict(color="#334155", width=3), marker=dict(size=8, color="#334155"),
                text=desap_values, textposition="top center", hoverinfo="skip"
            ))
            
        titol_eix_y = "Número total de víctimas"

    ## Disseny del gràfic
    fig.update_layout(
        height=450, transition_duration=500,
        xaxis_title="", 
        xaxis=dict(tickmode='linear', dtick=1, automargin=False),
        yaxis=dict(title=titol_eix_y, automargin=False),
        showlegend=True, hovermode=False,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        margin=dict(t=60, b=30, l=60, r=20)
    )
    return fig

# LAYOUT 
# ==========================================

app.layout = html.Div([
    ## Títol
    html.Div(className="header-bar", children=[
        html.H1("Homicidio Doloso a Nivel Nacional en México (2015-2025)", className="titol-principal")
    ]),
    
    ## Explicació del dashboard
    html.Div(className="content-wrapper", children=[
        html.P( [
            "En este panel se pueden consultar los datos oficiales del SESNSP y RNPDNO para contrastar la narrativa gubernamental sobre el descenso de homicidios. ",
            "El panel expone las cifras de incidencia, pero se debe considerar también los ajustes metodológicos y correcciones en los datos abiertos, " ,
            "así como otros factores.", 
            ], className="subtitol-context"
        ),
        ## Gràfics
        html.Div(className="contenidor-principal", children=[
            
            ### Gener a Juliol 
            html.Div(className="columna", children=[
                html.H2("Enero a Julio"),
                
                html.Button("Ver/Ocultar gráfico oficial", id="sem_toggle_btn", n_clicks=0, className="boto-toggle"),
                html.Div(className="controls-wrapper", children=[
                    html.Div(className="controls-grafic", children=[
                        dcc.RadioItems(id="sem_select_type", options=[{"label": " Promedio diario", "value": "promig"}, {"label": " Conteo absoluto", "value": "absolut"}], value="promig", inline=True)
                    ]),
                    html.Div(id="sem_desap_container", className="contenidor-desapareguts ocult-vis", children=[
                        dcc.Checklist(id="sem_show_desap", options=[{"label": " Añadir Desaparecidos y No Localizados", "value": "yes"}], value=[], inline=True)
                    ])
                ]),
                html.Div(className="grafic-wrapper", children=[
                    html.Div(id="sem_img_container", className="contenidor-imatge ocult", children=[html.Img(src="/assets/1rSEMESTRE_Promedio_diario_homicidio_doloso_nacional.png", className="imatge-original")]),
                    dcc.Graph(id="sem_grafic")
                ]),
                html.Div(dcc.Markdown("Fuente: [SESNSP](https://www.datos.gob.mx/dataset/incidencia_delictiva)/[RNPDNO](https://versionpublicarnpdno.segob.gob.mx)"), className="text-font")
            ]),
            
            ### Mes de Juliol
            html.Div(className="columna", children=[
                html.H2("Julio"),
                
                html.Button("Ver/Ocultar gráfico original", id="jul_toggle_btn", n_clicks=0, className="boto-toggle"),
                html.Div(className="controls-wrapper", children=[
                    html.Div(className="controls-grafic", children=[
                        dcc.RadioItems(id="jul_select_type", options=[{"label": " Promedio diario", "value": "promig"}, {"label": " Conteo absoluto", "value": "absolut"}], value="promig", inline=True)
                    ]),
                    html.Div(id="jul_desap_container", className="contenidor-desapareguts ocult-vis")
                ]),
                html.Div(className="grafic-wrapper", children=[
                    html.Div(id="jul_img_container", className="contenidor-imatge ocult", children=[html.Img(src="/assets/JULIO_Promedio_diario_homicidio_doloso_nacional.png", className="imatge-original")]),
                    dcc.Graph(id="jul_grafic")
                ]),
                html.Div(dcc.Markdown("Fuente: [SESNSP](https://www.datos.gob.mx/dataset/incidencia_delictiva)"), className="text-font")
            ])
        ])
    ])
])

# CALLBACKS 
# ==========================================

## Mostrar/Ocultar imatge original de gener a juliol
@app.callback(Output("sem_img_container", "className"), Input("sem_toggle_btn", "n_clicks"))
def toggle_sem(n): 
    return "contenidor-imatge actiu" if n % 2 == 1 else "contenidor-imatge ocult"

## Mostrar/Ocultar imatge original del mes de juliol
@app.callback(Output("jul_img_container", "className"), Input("jul_toggle_btn", "n_clicks"))
def toggle_jul(n): 
    return "contenidor-imatge actiu" if n % 2 == 1 else "contenidor-imatge ocult"

## Gestionar la visibilitat del selector de desapareguts
@app.callback(Output("sem_desap_container", "className"), Output("sem_show_desap", "value"), Input("sem_select_type", "value"))
def toggle_desap(tipus): 
    return ("contenidor-desapareguts actiu-vis", []) if tipus == "absolut" else ("contenidor-desapareguts ocult-vis", [])

## Actualitzar  gràfic del primer semestre
@app.callback(Output("sem_grafic", "figure"), Input("sem_select_type", "value"), Input("sem_show_desap", "value"))
def update_sem(tipus, show_desap):
    return crear_grafic(df_sem_prom, df_sem_abs, tipus, show_desap, es_semestre=True)

## Actualitzar gràfic de juliol
@app.callback(Output("jul_grafic", "figure"), Input("jul_select_type", "value"))
def update_jul(tipus):
    return crear_grafic(df_jul_prom, df_jul_abs, tipus, es_semestre=False)

# EXECUCIÓ
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)