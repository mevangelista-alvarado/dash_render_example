import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)
server = app.server

app.title = "Calculadora de Indice de Masa Corporal"
# Agregar el favicon manualmente si no se llama favicon.ico
# El archivo debe estar en la carpeta assets
app._favicon = "example.ico"  

# Lista para almacenar los valores de IMC calculados
bmi_values = []

# Diseno de la app
app.layout = html.Div([
    html.H1("Calculadora de IMC"),
    
    # Inputs de altura y peso
    html.Div([
        html.Label("Altura (m):"),
        dcc.Input(id="height", type="number", placeholder="Ingresa tu altura", min=0.1, step=0.01),
        
        html.Br(),
        html.Label("Peso (kg):"),
        dcc.Input(id="weight", type="number", placeholder="Ingresa tu peso", min=0.1, step=0.1),
        
        html.Br(),
        html.Button("Calcular IMC", id="calculate-btn", n_clicks=0)
    ]),
    
    # Resultado del IMC
    html.Div(id="bmi-output", style={"margin-top": "20px"}),
    
    # Gráfico de barras de frecuencias de IMC
    html.H3("Frecuencia de valores de IMC por rangos"),
    dcc.Graph(id="bmi-bar")
])

# Callback para calcular el IMC y actualizar el grafico de barras
@app.callback(
    [Output("bmi-output", "children"),
     Output("bmi-bar", "figure")],
    [Input("calculate-btn", "n_clicks")],
    [State("height", "value"),
     State("weight", "value")]
)
def calculate_bmi(n_clicks, height, weight):
    if n_clicks > 0 and height and weight:
        # Calcular el IMC
        bmi = weight / (height ** 2)
        bmi_values.append(bmi)
        
        # Crear el mensaje de resultado
        bmi_message = f"Tu IMC es: {bmi:.2f}"
        
        # Definir los rangos de IMC
        bins = [0, 18.5, 20, 21, 24, 27, 30, 35, 40, 50]
        labels = ["<18.5", "18.5-20", "20-21", "21-24", "24-27", "27-30", "30-35", "35-40", "40+"]
        
        # Crear DataFrame y clasificar los valores de IMC en rangos
        df = pd.DataFrame({"IMC": bmi_values})
        df["Rango_IMC"] = pd.cut(df["IMC"], bins=bins, labels=labels, right=False)
        
        # Contar la frecuencia de cada rango
        freq_df = df["Rango_IMC"].value_counts().sort_index().reset_index()
        freq_df.columns = ["Rango_IMC", "Frecuencia"]
        
        # Crear el grafico de barras
        fig = px.bar(freq_df, x="Rango_IMC", y="Frecuencia", title="Frecuencia de IMC por Rango")
        
        return bmi_message, fig
    else:
        # Grafico vacio si no hay datos
        return "Introduce valores válidos para calcular el IMC.", px.bar(pd.DataFrame({"Rango_IMC": [], "Frecuencia": []}), x="Rango_IMC", y="Frecuencia")

if __name__ == "__main__":
    app.run_server(debug=True)
