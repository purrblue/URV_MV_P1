import os
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# INICIALITZACIÓ

# Carregar datasets
base_dir = os.path.dirname(os.path.abspath(__file__))
dataset_dir = os.path.join(base_dir, "..", "01_dades", "processat")

df_sem_prom = pd.read_csv(os.path.join(dataset_dir, "homicidio_doloso_semestral_promedio_diario.csv"), index_col="Año")
df_sem_abs = pd.read_csv(os.path.join(dataset_dir, "homicidio_doloso_semestral_frecuencia_absoluta.csv"), index_col="Año")
df_jul_prom = pd.read_csv(os.path.join(dataset_dir, "homicidio_doloso_Julio_promedio_diario.csv"), index_col="Año")
df_jul_abs = pd.read_csv(os.path.join(dataset_dir, "homicidio_doloso_Julio_frecuencia_absoluta.csv"), index_col="Año")

# Inicialitzar app
app = Dash(__name__)

# LAYOUT
app.layout = html.Div([
    html.H1("Registro de Homicidio Doloso a Nivel Nacional (2015-2025)"),
    
    # Primer semestre
    html.H2("Enero a julio de cada año"),
    dcc.RadioItems(
        id="sem_select_type",
        options=[
            {"label": "Promedio diario", "value": "promig"},
            {"label": "Conteo absoluto", "value": "absolut"}
        ],
        value="promig"
    ),
    dcc.Graph(id="sem_grafic"),
    
    # Juliol
    html.H2("Julio de cada año"),
    dcc.RadioItems(
        id="jul_select_type",
        options=[
            {"label": "Promedio diario", "value": "promig"},
            {"label": "Conteo absoluto", "value": "absolut"}
        ],
        value="promig"
    ),
    dcc.Graph(id="jul_grafic")
])

# INTERACTIVITAT

# Callback pel primer semestre
@app.callback(
    Output(component_id="sem_grafic", component_property="figure"),
    Input(component_id="sem_select_type", component_property="value")
)
def actualitzar_semestre(tipus):
    if tipus == "promig":
        fig = px.bar(
                    df_sem_prom.mean(axis=1).rename("Víctimas homicidio doloso"),
                    title="Promedio diario de homicidio doloso a nivel nacional (2015-2025)",
                    labels={"value": "Promedio diario"}
                )
    else:
        fig = px.bar(
                    df_sem_abs.sum(axis=1).rename("Víctimas homicidio doloso"),
                    title="Conteo de homicidio doloso a nivel nacional (2015-2025)",
                    labels={"value": "Valor absoluto"}
                )
    fig.update_traces(showlegend=False)
    return fig


# Callback per juliol
@app.callback(
    Output(component_id="jul_grafic", component_property="figure"),
    Input(component_id="jul_select_type", component_property="value")
)
def actualizar_juliol(tipus):
    if tipus == "promig":
        fig = px.bar(
                    df_jul_prom.mean(axis=1).rename("Víctimas homicidio doloso"),
                    title="Promedio diario de homicidio doloso a nivel nacional (2015-2025)",
                    labels={"value": "Promedio diario"}
                )
    else:
        fig = px.bar(
                    df_jul_abs.sum(axis=1).rename("Víctimas homicidio doloso"),
                    title="Conteo de homicidio doloso a nivel nacional (2015-2025)",
                    labels={"value": "Valor absoluto"}
                )
        
    fig.update_traces(showlegend=False)
    return fig


if __name__ == "__main__":
    app.run(debug=True)