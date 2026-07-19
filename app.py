import pandas as pd
import numpy as np

from dash import Dash, html, dcc, Input, Output
import plotly.express as px

df = pd.read_csv("netflix_titles.csv")

df = df.drop_duplicates()

df["date_added"] = df["date_added"].astype(str).str.strip()
df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
df = df.dropna(subset=["date_added"])

text_columns = ["director", "cast", "country", "rating"]
for col in text_columns:
    df[col] = df[col].fillna("Unknown")

df["year_added"] = df["date_added"].dt.year
df["month_added"] = df["date_added"].dt.month_name()

df["duration_number"] = df["duration"].str.extract(r"(\d+)").astype(float)
df["duration_type"] = df["duration"].str.extract(r"([A-Za-z]+)")
df["duration_type"] = df["duration_type"].replace(
    {"min": "Movie", "Season": "TV Show", "Seasons": "TV Show"}
)

df["main_genre"] = df["listed_in"].str.split(",").str[0].str.strip()
df["main_country"] = df["country"].str.split(",").str[0].str.strip()

app = Dash(__name__)
server = app.server

BACKGROUND = "#141414"
CARD = "#222222"
RED = "#E50914"
TEXT = "white"

type_options = (
    [{"label": "All", "value": "All"}]
    + [{"label": t, "value": t} for t in sorted(df["type"].unique())]
)

country_options = (
    [{"label": "All", "value": "All"}]
    + [{"label": c, "value": c} for c in sorted(df["main_country"].unique())]
)

app.layout = html.Div(
    style={"backgroundColor": BACKGROUND, "padding": "20px", "fontFamily": "Arial"},
    children=[
        html.H1(
            "Netflix Content Dashboard",
            style={"color": RED, "textAlign": "center", "marginBottom": "25px"},
        ),
        html.Div(
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "gap": "20px",
                "marginBottom": "30px",
            },
            children=[
                html.Div(
                    [
                        html.Label("Content Type", style={"color": TEXT}),
                        dcc.Dropdown(
                            id="type-dropdown",
                            options=type_options,
                            value="All",
                            clearable=False,
                        ),
                    ],
                    style={"width": "30%"},
                ),
                html.Div(
                    [
                        html.Label("Country", style={"color": TEXT}),
                        dcc.Dropdown(
                            id="country-dropdown",
                            options=country_options,
                            value="All",
                            clearable=False,
                        ),
                    ],
                    style={"width": "30%"},
                ),
                html.Div(
                    [
                        html.Label("Release Year", style={"color": TEXT}),
                        dcc.RangeSlider(
                            id="year-slider",
                            min=int(df["release_year"].min()),
                            max=int(df["release_year"].max()),
                            value=[
                                int(df["release_year"].min()),
                                int(df["release_year"].max()),
                            ],
                            marks={
                                int(i): str(i)
                                for i in range(
                                    int(df["release_year"].min()),
                                    int(df["release_year"].max()) + 1,
                                    10,
                                )
                            },
                            tooltip={"placement": "bottom"},
                        ),
                    ],
                    style={"width": "40%"},
                ),
            ],
        ),
        html.Div(
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "marginBottom": "30px",
                "gap": "20px",
            },
            children=[
                html.Div(
                    [
                        html.H3("Total Titles", style={"color": RED}),
                        html.H2(id="total-titles", style={"color": TEXT}),
                    ],
                    style={
                        "backgroundColor": CARD,
                        "padding": "20px",
                        "borderRadius": "10px",
                        "width": "24%",
                        "textAlign": "center",
                    },
                ),
                html.Div(
                    [
                        html.H3("Movies", style={"color": RED}),
                        html.H2(id="movie-count", style={"color": TEXT}),
                    ],
                    style={
                        "backgroundColor": CARD,
                        "padding": "20px",
                        "borderRadius": "10px",
                        "width": "24%",
                        "textAlign": "center",
                    },
                ),
                html.Div(
                    [
                        html.H3("TV Shows", style={"color": RED}),
                        html.H2(id="tv-count", style={"color": TEXT}),
                    ],
                    style={
                        "backgroundColor": CARD,
                        "padding": "20px",
                        "borderRadius": "10px",
                        "width": "24%",
                        "textAlign": "center",
                    },
                ),
                html.Div(
                    [
                        html.H3("Average Movie Length", style={"color": RED}),
                        html.H2(id="avg-duration", style={"color": TEXT}),
                    ],
                    style={
                        "backgroundColor": CARD,
                        "padding": "20px",
                        "borderRadius": "10px",
                        "width": "24%",
                        "textAlign": "center",
                    },
                ),
            ],
        ),
        html.Div(
            style={"display": "flex", "gap": "20px", "marginBottom": "20px"},
            children=[
                dcc.Graph(id="line-chart", style={"width": "50%"}),
                dcc.Graph(id="pie-chart", style={"width": "50%"}),
            ],
        ),
        html.Div(
            style={"display": "flex", "gap": "20px"},
            children=[
                dcc.Graph(id="bar-chart", style={"width": "50%"}),
                dcc.Graph(id="scatter-chart", style={"width": "50%"}),
            ],
        ),
    ],
)


def filter_data(content_type, country, year_range):
    filtered = df.copy()

    if content_type != "All":
        filtered = filtered[filtered["type"] == content_type]

    if country != "All":
        filtered = filtered[filtered["main_country"] == country]

    filtered = filtered[
        (filtered["release_year"] >= year_range[0])
        & (filtered["release_year"] <= year_range[1])
    ]

    return filtered


def style_figure(fig):
    fig.update_layout(
        paper_bgcolor=BACKGROUND,
        plot_bgcolor=CARD,
        font=dict(color=TEXT, size=13),
        title_font=dict(color=RED, size=20),
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(bgcolor=CARD),
    )
    return fig


def create_line_chart(filtered):
    yearly = (
        filtered.groupby("release_year").size().reset_index(name="Titles")
    )

    fig = px.line(
        yearly,
        x="release_year",
        y="Titles",
        markers=True,
        title="Titles Released Over Time",
    )

    fig.update_traces(line_color=RED, marker_size=8)

    return style_figure(fig)


def create_bar_chart(filtered):
    genres = filtered["main_genre"].value_counts().head(10).reset_index()
    genres.columns = ["Genre", "Count"]

    fig = px.bar(
        genres,
        x="Genre",
        y="Count",
        color="Count",
        title="Top 10 Genres",
    )

    fig.update_layout(xaxis_tickangle=-35)

    return style_figure(fig)


def create_pie_chart(filtered):
    counts = filtered["type"].value_counts().reset_index()
    counts.columns = ["Type", "Count"]

    fig = px.pie(
        counts,
        names="Type",
        values="Count",
        hole=0.45,
        title="Movies vs TV Shows",
    )

    fig.update_traces(textposition="inside", textinfo="percent+label")

    return style_figure(fig)


def create_scatter_chart(filtered):
    movies = filtered[filtered["duration_type"] == "Movie"]

    fig = px.scatter(
        movies,
        x="release_year",
        y="duration_number",
        color="rating",
        hover_name="title",
        hover_data=["country", "main_genre", "duration"],
        title="Movie Duration vs Release Year",
        labels={
            "release_year": "Release Year",
            "duration_number": "Duration (Minutes)",
        },
    )

    fig.update_traces(marker=dict(size=9))

    return style_figure(fig)


@app.callback(
    Output("line-chart", "figure"),
    Output("bar-chart", "figure"),
    Output("pie-chart", "figure"),
    Output("scatter-chart", "figure"),
    Output("total-titles", "children"),
    Output("movie-count", "children"),
    Output("tv-count", "children"),
    Output("avg-duration", "children"),
    Input("type-dropdown", "value"),
    Input("country-dropdown", "value"),
    Input("year-slider", "value"),
)
def update_dashboard(content_type, country, year_range):
    filtered = filter_data(content_type, country, year_range)

    total = len(filtered)
    movies = len(filtered[filtered["type"] == "Movie"])
    tv = len(filtered[filtered["type"] == "TV Show"])

    avg_dur = filtered.loc[
        filtered["duration_type"] == "Movie", "duration_number"
    ].mean()
    avg_dur_str = f"{avg_dur:.0f} min" if pd.notna(avg_dur) else "N/A"

    return (
        create_line_chart(filtered),
        create_bar_chart(filtered),
        create_pie_chart(filtered),
        create_scatter_chart(filtered),
        f"{total}",
        f"{movies}",
        f"{tv}",
        avg_dur_str,
    )


if __name__ == "__main__":
    app.run(debug=True)