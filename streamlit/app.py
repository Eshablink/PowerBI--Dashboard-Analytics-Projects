# ============================================================
#  Spotify Analytics Dashboard
#  Author  : Dabbara Esha
#  Stack   : Python · Streamlit · Plotly · Pandas
#  Purpose : Portfolio project – Data Analyst / Python Developer
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page Config ─────────────────────────────────────────────
st.set_page_config(
    page_title="Spotify Analytics Dashboard",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS (dark theme + card styling) ───────────────────
st.markdown("""
<style>
/* ---- Global background ---- */
[data-testid="stAppViewContainer"] {
    background-color: #0d0d0d;
    color: #ffffff;
}
[data-testid="stSidebar"] {
    background-color: #121212;
    border-right: 1px solid #1db954;
}

/* ---- KPI Cards ---- */
.kpi-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border: 1px solid #1db954;
    border-radius: 12px;
    padding: 20px 24px;
    text-align: center;
    margin: 4px 0;
    box-shadow: 0 4px 15px rgba(29,185,84,0.15);
}
.kpi-title {
    font-size: 13px;
    color: #b3b3b3;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.kpi-value {
    font-size: 30px;
    font-weight: 700;
    color: #1db954;
    margin: 0;
}
.kpi-sub {
    font-size: 12px;
    color: #666;
    margin-top: 4px;
}

/* ---- Section headers ---- */
.section-header {
    font-size: 20px;
    font-weight: 700;
    color: #1db954;
    border-left: 4px solid #1db954;
    padding-left: 12px;
    margin: 28px 0 16px 0;
}

/* ---- Plotly chart background ---- */
.js-plotly-plot .plotly .bg {fill: transparent !important;}

/* ---- Sidebar text ---- */
.css-1d391kg {color: #ffffff !important;}
</style>
""", unsafe_allow_html=True)


# ── Load Data ────────────────────────────────────────────────
@st.cache_data
def load_data():
    """Load and return the Spotify dataset. Cached for performance."""
    df = pd.read_csv("spotify_data.csv")
    df["streams_billions"] = (df["streams"] / 1_000_000_000).round(2)
    df["explicit"] = df["explicit"].astype(str)
    return df

df = load_data()

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎵 Spotify Analytics")
    st.markdown("---")

    # Genre filter
    all_genres = sorted(df["genre"].unique().tolist())
    selected_genres = st.multiselect(
        "🎸 Genre",
        options=all_genres,
        default=all_genres
    )

    # Year range filter
    min_year = int(df["release_year"].min())
    max_year = int(df["release_year"].max())
    year_range = st.slider(
        "📅 Release Year",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )

    # Popularity filter
    min_pop = st.slider(
        "⭐ Min Popularity Score",
        min_value=0, max_value=100, value=85
    )

    # Explicit filter
    explicit_filter = st.radio(
        "🔞 Explicit Content",
        options=["All", "True", "False"],
        index=0
    )

    st.markdown("---")
    st.markdown("**📊 Dashboard by**")
    st.markdown("**Dabbara Esha**")
    st.markdown("*Data Analyst · Python Developer*")

# ── Apply Filters ────────────────────────────────────────────
filtered = df[
    (df["genre"].isin(selected_genres)) &
    (df["release_year"] >= year_range[0]) &
    (df["release_year"] <= year_range[1]) &
    (df["popularity"] >= min_pop)
]
if explicit_filter != "All":
    filtered = filtered[filtered["explicit"] == explicit_filter]

# ── Header ───────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding: 10px 0 20px 0;'>
    <h1 style='color:#1db954; font-size:42px; margin:0;'>🎵 Spotify Analytics Dashboard</h1>
    <p style='color:#b3b3b3; font-size:16px; margin:4px 0 0 0;'>
        Interactive music data analysis · Portfolio project by Dabbara Esha
    </p>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ─────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)

total_tracks   = len(filtered)
total_streams  = filtered["streams"].sum()
avg_popularity = filtered["popularity"].mean()
top_artist     = filtered.groupby("artist_name")["streams"].sum().idxmax() if total_tracks else "—"
top_genre      = filtered["genre"].value_counts().idxmax() if total_tracks else "—"

def kpi(col, title, value, sub=""):
    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>""", unsafe_allow_html=True)

kpi(k1, "🎵 Tracks", f"{total_tracks:,}", "in selection")
kpi(k2, "▶️ Total Streams", f"{total_streams/1e9:.1f}B", "billion plays")
kpi(k3, "⭐ Avg Popularity", f"{avg_popularity:.1f}", "out of 100")
kpi(k4, "🏆 Top Artist", top_artist, "by streams")
kpi(k5, "🎸 Top Genre", top_genre, "most tracks")

st.markdown("<br>", unsafe_allow_html=True)

# ── Chart helpers ────────────────────────────────────────────
CHART_BG    = "rgba(0,0,0,0)"
PAPER_BG    = "rgba(0,0,0,0)"
FONT_COLOR  = "#e0e0e0"
GRID_COLOR  = "#2a2a2a"
GREEN       = "#1db954"

def base_layout(title=""):
    return dict(
        title=dict(text=title, font=dict(color=FONT_COLOR, size=16)),
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=CHART_BG,
        font=dict(color=FONT_COLOR, family="Inter, sans-serif"),
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(bgcolor="rgba(0,0,0,0.3)", bordercolor="#333")
    )

# ── Row 1 : Top Artists | Genre Distribution ─────────────────
st.markdown('<div class="section-header">Top Artists & Genre Breakdown</div>', unsafe_allow_html=True)
col1, col2 = st.columns([3, 2])

with col1:
    top_artists = (
        filtered.groupby("artist_name")["streams"]
        .sum()
        .sort_values(ascending=True)
        .tail(10)
        .reset_index()
    )
    top_artists["streams_b"] = (top_artists["streams"] / 1e9).round(2)

    fig_artists = go.Figure(go.Bar(
        x=top_artists["streams_b"],
        y=top_artists["artist_name"],
        orientation="h",
        marker=dict(
            color=top_artists["streams_b"],
            colorscale=[[0, "#1a5c2a"], [1, "#1db954"]],
            showscale=False
        ),
        text=top_artists["streams_b"].apply(lambda x: f"{x}B"),
        textposition="outside",
        textfont=dict(color=FONT_COLOR, size=11)
    ))
    fig_artists.update_layout(**base_layout("🏆 Top 10 Artists by Total Streams"))
    fig_artists.update_xaxes(
        showgrid=True, gridcolor=GRID_COLOR, zeroline=False,
        title_text="Streams (Billions)", title_font=dict(color="#aaa")
    )
    fig_artists.update_yaxes(showgrid=False)
    st.plotly_chart(fig_artists, use_container_width=True)

with col2:
    genre_dist = filtered["genre"].value_counts().reset_index()
    genre_dist.columns = ["genre", "count"]

    fig_pie = go.Figure(go.Pie(
        labels=genre_dist["genre"],
        values=genre_dist["count"],
        hole=0.55,
        marker=dict(colors=px.colors.sequential.Greens_r[:len(genre_dist)]),
        textinfo="label+percent",
        textfont=dict(color=FONT_COLOR, size=12),
        hovertemplate="<b>%{label}</b><br>Tracks: %{value}<br>Share: %{percent}<extra></extra>"
    ))
    fig_pie.update_layout(**base_layout("🎸 Genre Distribution"))
    fig_pie.add_annotation(
        text=f"<b>{total_tracks}</b><br>Tracks",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=16, color=GREEN)
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ── Row 2 : Yearly Trends ────────────────────────────────────
st.markdown('<div class="section-header">Yearly Streaming Trends</div>', unsafe_allow_html=True)
col3, col4 = st.columns(2)

with col3:
    yearly = (
        filtered.groupby("release_year")
        .agg(total_streams=("streams", "sum"), track_count=("track_name", "count"))
        .reset_index()
    )
    yearly["streams_b"] = (yearly["total_streams"] / 1e9).round(2)

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=yearly["release_year"], y=yearly["streams_b"],
        mode="lines+markers",
        name="Streams (B)",
        line=dict(color=GREEN, width=3),
        marker=dict(size=8, color=GREEN, symbol="circle"),
        fill="tozeroy",
        fillcolor="rgba(29,185,84,0.08)",
        hovertemplate="Year: %{x}<br>Streams: %{y}B<extra></extra>"
    ))
    fig_trend.add_trace(go.Bar(
        x=yearly["release_year"], y=yearly["track_count"],
        name="Track Count",
        yaxis="y2",
        marker=dict(color="rgba(29,185,84,0.25)", line=dict(color=GREEN, width=1)),
        hovertemplate="Year: %{x}<br>Tracks: %{y}<extra></extra>"
    ))
    fig_trend.update_layout(
        **base_layout("📈 Streams & Track Count by Year"),
        yaxis=dict(title="Streams (Billions)", showgrid=True, gridcolor=GRID_COLOR, color=FONT_COLOR),
        yaxis2=dict(title="Track Count", overlaying="y", side="right", showgrid=False, color=FONT_COLOR),
        xaxis=dict(showgrid=False, color=FONT_COLOR),
        hovermode="x unified"
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with col4:
    genre_year = (
        filtered.groupby(["release_year", "genre"])["streams"]
        .sum()
        .reset_index()
    )
    genre_year["streams_b"] = (genre_year["streams"] / 1e9).round(2)

    fig_area = px.area(
        genre_year, x="release_year", y="streams_b", color="genre",
        color_discrete_sequence=px.colors.qualitative.G10,
        labels={"streams_b": "Streams (B)", "release_year": "Year", "genre": "Genre"},
        title="📊 Streams by Genre Over Time"
    )
    fig_area.update_layout(**base_layout("📊 Streams by Genre Over Time"))
    fig_area.update_xaxes(showgrid=False, color=FONT_COLOR)
    fig_area.update_yaxes(showgrid=True, gridcolor=GRID_COLOR, color=FONT_COLOR)
    st.plotly_chart(fig_area, use_container_width=True)

# ── Row 3 : Audio Features | Popularity vs Streams ───────────
st.markdown('<div class="section-header">Audio Features & Popularity Analysis</div>', unsafe_allow_html=True)
col5, col6 = st.columns(2)

with col5:
    # Radar chart – avg audio features per genre
    features = ["danceability", "energy", "valence", "tempo"]
    radar_df = filtered.groupby("genre")[features].mean().reset_index()

    fig_radar = go.Figure()
    colors = ["#1db954", "#ff6384", "#36a2eb", "#ffce56", "#9b59b6", "#e67e22"]
    for i, row in radar_df.iterrows():
        # Normalise tempo to 0-100 for display
        vals = [row["danceability"], row["energy"], row["valence"], min(row["tempo"] / 2, 100)]
        vals_closed = vals + [vals[0]]
        labels_closed = features + [features[0]]
        fig_radar.add_trace(go.Scatterpolar(
            r=vals_closed,
            theta=labels_closed,
            fill="toself",
            name=row["genre"],
            line=dict(color=colors[i % len(colors)], width=2),
            opacity=0.7
        ))
    fig_radar.update_layout(
        **base_layout("🎛️ Avg Audio Features by Genre"),
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100], color=FONT_COLOR, gridcolor=GRID_COLOR),
            angularaxis=dict(color=FONT_COLOR, gridcolor=GRID_COLOR)
        )
    )
    st.plotly_chart(fig_radar, use_container_width=True)

with col6:
    fig_scatter = px.scatter(
        filtered,
        x="popularity", y="streams_billions",
        color="genre",
        size="duration_min",
        hover_name="track_name",
        hover_data={"artist_name": True, "release_year": True},
        color_discrete_sequence=px.colors.qualitative.G10,
        labels={"popularity": "Popularity Score", "streams_billions": "Streams (Billions)"},
        title="🔵 Popularity vs Streams (bubble = duration)"
    )
    fig_scatter.update_layout(**base_layout("🔵 Popularity vs Streams"))
    fig_scatter.update_xaxes(showgrid=True, gridcolor=GRID_COLOR, color=FONT_COLOR)
    fig_scatter.update_yaxes(showgrid=True, gridcolor=GRID_COLOR, color=FONT_COLOR)
    st.plotly_chart(fig_scatter, use_container_width=True)

# ── Row 4 : Top Tracks Table ──────────────────────────────────
st.markdown('<div class="section-header">🏅 Top 10 Tracks by Streams</div>', unsafe_allow_html=True)

top_tracks = (
    filtered[["track_name", "artist_name", "genre", "release_year", "streams_billions", "popularity"]]
    .sort_values("streams_billions", ascending=False)
    .head(10)
    .reset_index(drop=True)
)
top_tracks.index = top_tracks.index + 1
top_tracks.columns = ["Track", "Artist", "Genre", "Year", "Streams (B)", "Popularity"]

st.dataframe(
    top_tracks.style
    .background_gradient(subset=["Streams (B)"], cmap="Greens")
    .background_gradient(subset=["Popularity"], cmap="Blues")
    .format({"Streams (B)": "{:.2f}"}),
    use_container_width=True,
    height=380
)

# ── Row 5 : Dataset Preview ───────────────────────────────────
st.markdown('<div class="section-header">📂 Dataset Preview</div>', unsafe_allow_html=True)

with st.expander("🔍 Click to explore the full dataset"):
    search = st.text_input("🔎 Search by track or artist name", placeholder="e.g. Taylor Swift")
    display_df = filtered.copy()
    if search:
        mask = (
            display_df["track_name"].str.contains(search, case=False, na=False) |
            display_df["artist_name"].str.contains(search, case=False, na=False)
        )
        display_df = display_df[mask]

    st.dataframe(
        display_df[["track_name", "artist_name", "genre", "release_year",
                     "streams_billions", "popularity", "danceability",
                     "energy", "valence", "explicit"]]
        .rename(columns={
            "track_name": "Track", "artist_name": "Artist",
            "genre": "Genre", "release_year": "Year",
            "streams_billions": "Streams (B)", "popularity": "Popularity",
            "danceability": "Dance", "energy": "Energy",
            "valence": "Valence", "explicit": "Explicit"
        })
        .reset_index(drop=True),
        use_container_width=True,
        height=350
    )
    st.caption(f"Showing {len(display_df)} of {len(filtered)} filtered tracks")

# ── Footer ────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#555; font-size:13px; padding:10px 0;'>
    Built with ❤️ by <b style='color:#1db954;'>Dabbara Esha</b> ·
    Data Analyst | Python Developer | SQL &nbsp;·&nbsp;
    <a href='https://github.com' style='color:#1db954;'>GitHub</a> ·
    <a href='https://linkedin.com' style='color:#1db954;'>LinkedIn</a>
</div>
""", unsafe_allow_html=True)
