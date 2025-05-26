# Save this as app.py and run using: `python app.py`
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

df = pd.read_csv("enhanced_crop_yield_dataset.csv")  # Update path if needed

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Interactive Crop Yield Dashboard"),

    html.Label("Select Subcounty:"),
    dcc.Dropdown(
        options=[{"label": s, "value": s} for s in df["SUBCOUNTY"].unique()],
        value=df["SUBCOUNTY"].unique()[0],
        id='subcounty-dropdown'
    ),

    html.Label("Select Feature:"),
    dcc.Dropdown(
        options=[{"label": col, "value": col} for col in [
            "Rainfall", "Temperature", "NDVI", "EVI", "LST", 
            "Water_stress", "Heat_index", "Yield_per_EVI"
        ]],
        value="Rainfall",
        id='xaxis-dropdown'
    ),

    dcc.Graph(id='scatter-plot')
])

@app.callback(
    dash.dependencies.Output('scatter-plot', 'figure'),
    [
        dash.dependencies.Input('subcounty-dropdown', 'value'),
        dash.dependencies.Input('xaxis-dropdown', 'value')
    ]
)
def update_graph(subcounty, xaxis):
    filtered_df = df[df["SUBCOUNTY"] == subcounty]
    fig = px.scatter(filtered_df, x=xaxis, y="Quantity", color="YEAR",
                     title=f"{xaxis} vs Yield for {subcounty}", hover_name="YEAR")
    return fig

if __name__ == '__main__':
    app.run(debug=True)
