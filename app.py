import dash
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px

# Load the processed data
df = pd.read_csv("data/processed_data.csv")

# Convert date column to datetime and sort
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# Build the Dash app
app = dash.Dash(__name__)

app.layout = html.Div(children=[

    # Header Banner
    html.Div(children=[
        html.H1("🍬 Pink Morsel Sales Visualiser",
                style={
                    "textAlign": "center",
                    "color": "white",
                    "fontFamily": "Arial, sans-serif",
                    "fontSize": "36px",
                    "margin": "0",
                    "padding": "20px 0 5px 0"
                }),
        html.P("Analysing the impact of the Pink Morsel price increase — 15th January 2021",
               style={
                   "textAlign": "center",
                   "color": "#f0c0d0",
                   "fontFamily": "Arial, sans-serif",
                   "fontSize": "15px",
                   "margin": "0",
                   "paddingBottom": "20px"
               })
    ], style={
        "background": "linear-gradient(135deg, #c0392b, #e91e8c)",
        "borderRadius": "12px",
        "marginBottom": "25px",
        "boxShadow": "0 4px 15px rgba(200, 0, 100, 0.3)"
    }),

    # Radio Button Filter
    html.Div(children=[
        html.Label("Filter by Region:",
                   style={
                       "fontFamily": "Arial, sans-serif",
                       "fontWeight": "bold",
                       "fontSize": "15px",
                       "color": "#444",
                       "marginBottom": "10px",
                       "display": "block"
                   }),
        dcc.RadioItems(
            id="region-filter",
            options=[
                {"label": " All",   "value": "all"},
                {"label": " North", "value": "north"},
                {"label": " East",  "value": "east"},
                {"label": " South", "value": "south"},
                {"label": " West",  "value": "west"},
            ],
            value="all",
            inline=True,
            style={
                "fontFamily": "Arial, sans-serif",
                "fontSize": "15px",
                "color": "#333"
            },
            inputStyle={"marginRight": "6px", "accentColor": "#e91e8c"},
            labelStyle={"marginRight": "25px", "cursor": "pointer"}
        )
    ], style={
        "backgroundColor": "white",
        "padding": "20px 25px",
        "borderRadius": "10px",
        "marginBottom": "20px",
        "boxShadow": "0 2px 8px rgba(0,0,0,0.08)",
        "borderLeft": "5px solid #e91e8c"
    }),

    # Line Chart
    dcc.Graph(id="sales-line-chart",
              style={"borderRadius": "10px",
                     "boxShadow": "0 2px 8px rgba(0,0,0,0.08)"}),

    # Footer
    html.Div("© 2024 Soul Foods · Pink Morsel Analytics Dashboard",
             style={
                 "textAlign": "center",
                 "color": "#aaa",
                 "fontFamily": "Arial, sans-serif",
                 "fontSize": "12px",
                 "marginTop": "20px",
                 "paddingBottom": "10px"
             })

], style={
    "maxWidth": "1100px",
    "margin": "30px auto",
    "padding": "25px",
    "backgroundColor": "#f9f0f3",
    "borderRadius": "15px",
    "boxShadow": "0 6px 25px rgba(0,0,0,0.1)"
})


# Callback to update chart based on region selection
@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-filter", "value")
)
def update_chart(selected_region):

    # Filter by region
    if selected_region == "all":
        filtered_df = df.groupby("date")["sales"].sum().reset_index()
    else:
        filtered_df = df[df["region"] == selected_region].groupby("date")["sales"].sum().reset_index()

    # Create line chart
    fig = px.line(
        filtered_df,
        x="date",
        y="sales",
        labels={"date": "Date", "sales": "Total Sales ($)"},
        color_discrete_sequence=["#e91e8c"]
    )

    # Add vertical line for price increase
    fig.add_vline(
        x=pd.Timestamp("2021-01-15").timestamp() * 1000,
        line_dash="dash",
        line_color="#c0392b",
        line_width=2,
        annotation_text="📍 Price Increase",
        annotation_position="top left",
        annotation_font_color="#c0392b"
    )

    # Style the chart
    fig.update_layout(
        title=dict(
            text=f"Sales Over Time — Region: {selected_region.capitalize()}",
            x=0.5,
            xanchor="center",
            font=dict(size=18, family="Arial, sans-serif", color="#333")
        ),
        xaxis_title="Date",
        yaxis_title="Total Sales ($)",
        hovermode="x unified",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial, sans-serif", size=13),
        margin=dict(l=50, r=30, t=60, b=50)
    )

    fig.update_xaxes(showgrid=True, gridcolor="#f0f0f0")
    fig.update_yaxes(showgrid=True, gridcolor="#f0f0f0")

    return fig


if __name__ == "__main__":
    app.run(debug=True)