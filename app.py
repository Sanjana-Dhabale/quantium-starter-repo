import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px

# Load the processed data
df = pd.read_csv("data/processed_data.csv")

# Convert date column to datetime and sort
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# Group by date and sum sales across all regions
df_grouped = df.groupby("date")["sales"].sum().reset_index()

# Create the line chart
fig = px.line(
    df_grouped,
    x="date",
    y="sales",
    title="Pink Morsel Sales Over Time",
    labels={"date": "Date", "sales": "Total Sales ($)"}
)

# Add a vertical line for the price increase on 15th Jan 2021
fig.add_vline(
    x=pd.Timestamp("2021-01-15").timestamp() * 1000,
    line_dash="dash",
    line_color="red",
    annotation_text="Price Increase",
    annotation_position="top left"
)

# Build the Dash app
app = dash.Dash(__name__)

app.layout = html.Div(children=[

    # Header
    html.H1(
        "Pink Morsel Sales Visualiser",
        style={
            "textAlign": "center",
            "color": "#333",
            "fontFamily": "Arial, sans-serif",
            "padding": "20px"
        }
    ),

    html.P(
        "Visualising the impact of the Pink Morsel price increase on 15th January 2021",
        style={
            "textAlign": "center",
            "color": "#666",
            "fontFamily": "Arial, sans-serif",
            "marginBottom": "30px"
        }
    ),

    # Line Chart
    dcc.Graph(
        id="sales-line-chart",
        figure=fig
    )

], style={"maxWidth": "1200px", "margin": "0 auto"})

if __name__ == "__main__":
    app.run(debug=True)