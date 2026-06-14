"""
Truecaller Sentiment Analysis Dashboard
Author: Portfolio Project | B.Tech Computer Science
Description: Interactive dashboard for analyzing Truecaller app reviews,
             sentiment trends, spam mentions, and rating distributions.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import io
import base64
from collections import Counter
import re

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Truecaller Sentiment Dashboard",
    page_icon="📞",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ---- Global ---- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #0a0d14;
    color: #e2e8f0;
}

/* ---- Sidebar ---- */
[data-testid="stSidebar"] {
    background: #0f1320 !important;
    border-right: 1px solid #1e2535;
}
[data-testid="stSidebar"] .block-container {
    padding-top: 2rem;
}

/* ---- KPI Cards ---- */
.kpi-card {
    background: linear-gradient(135deg, #141927 0%, #1a2234 100%);
    border: 1px solid #1e2d4a;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    height: 100%;
}
.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(0,180,255,0.12);
}
.kpi-icon   { font-size: 1.8rem; margin-bottom: 0.4rem; }
.kpi-value  { font-size: 2.2rem; font-weight: 700; letter-spacing: -0.02em; }
.kpi-label  { font-size: 0.78rem; color: #64748b; font-weight: 500;
               text-transform: uppercase; letter-spacing: 0.08em; margin-top: 0.2rem; }
.kpi-delta  { font-size: 0.82rem; margin-top: 0.3rem; font-weight: 500; }

/* ── Colour accents per KPI ── */
.kpi-total  .kpi-value { color: #60a5fa; }
.kpi-pos    .kpi-value { color: #34d399; }
.kpi-neg    .kpi-value { color: #f87171; }
.kpi-rating .kpi-value { color: #fbbf24; }

/* ---- Section headers ---- */
.section-header {
    font-size: 1.05rem;
    font-weight: 600;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin: 1.8rem 0 0.8rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1e2535;
}

/* ---- Chart cards ---- */
.chart-card {
    background: #141927;
    border: 1px solid #1e2535;
    border-radius: 14px;
    padding: 1.2rem;
}

/* ---- Badge pill ---- */
.badge {
    display: inline-block;
    padding: 0.15rem 0.6rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.badge-positive { background: rgba(52,211,153,0.15); color: #34d399; }
.badge-negative { background: rgba(248,113,113,0.15); color: #f87171; }
.badge-neutral  { background: rgba(148,163,184,0.12); color: #94a3b8; }

/* ---- Brand header ---- */
.brand-header {
    background: linear-gradient(135deg, #0f1a2e 0%, #0f1320 100%);
    border: 1px solid #1e2d4a;
    border-radius: 16px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.4rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.brand-title {
    font-size: 1.7rem;
    font-weight: 700;
    background: linear-gradient(90deg, #60a5fa, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
}
.brand-subtitle {
    color: #475569;
    font-size: 0.85rem;
    margin: 0.2rem 0 0;
}

/* ---- Streamlit overrides ---- */
.stSelectbox label, .stMultiSelect label,
.stSlider label, .stRadio label          { color: #94a3b8 !important; font-size: 0.82rem !important; }
div[data-baseweb="select"] > div         { background: #0f1320 !important; border-color: #1e2535 !important; }
.stDataFrame                             { background: #141927 !important; border-radius: 10px; }
div[data-testid="metric-container"]      { background: transparent !important; }
</style>
""", unsafe_allow_html=True)


# ── Data loading ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("truecaller_reviews.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

df_raw = load_data()


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📞 Dashboard Filters")
    st.markdown("---")

    years_available = sorted(df_raw["year"].unique())
    selected_years = st.multiselect(
        "📅 Year", years_available, default=years_available,
    )

    sentiments_available = df_raw["sentiment"].unique().tolist()
    selected_sentiments = st.multiselect(
        "💬 Sentiment", sentiments_available, default=sentiments_available,
    )

    ratings_available = sorted(df_raw["rating"].unique())
    selected_ratings = st.multiselect(
        "⭐ Rating", ratings_available, default=ratings_available,
    )

    countries_available = df_raw["country"].unique().tolist()
    selected_countries = st.multiselect(
        "🌍 Country", countries_available, default=countries_available,
    )

    st.markdown("---")
    search_term = st.text_input("🔍 Search reviews", placeholder="e.g. spam, battery...")

    st.markdown("---")
    st.markdown(
        "<small style='color:#475569'>Built for B.Tech CS Portfolio<br>"
        "Data Analyst | Python | SQL</small>",
        unsafe_allow_html=True,
    )


# ── Filter data ──────────────────────────────────────────────────────────────
df = df_raw.copy()
if selected_years:
    df = df[df["year"].isin(selected_years)]
if selected_sentiments:
    df = df[df["sentiment"].isin(selected_sentiments)]
if selected_ratings:
    df = df[df["rating"].isin(selected_ratings)]
if selected_countries:
    df = df[df["country"].isin(selected_countries)]
if search_term.strip():
    df = df[df["review_text"].str.contains(search_term.strip(), case=False, na=False)]


# ── Plotly dark theme helper ──────────────────────────────────────────────────
CHART_BG   = "#141927"
GRID_COLOR = "#1e2535"
TEXT_COLOR = "#94a3b8"
ACCENT     = ["#60a5fa", "#34d399", "#f87171", "#fbbf24", "#a78bfa", "#fb923c"]

def apply_dark_theme(fig, height=360):
    fig.update_layout(
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_BG,
        font=dict(color=TEXT_COLOR, family="Inter"),
        height=height,
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor=GRID_COLOR,
            font=dict(color=TEXT_COLOR),
        ),
        xaxis=dict(
            gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR,
            tickfont=dict(color=TEXT_COLOR),
        ),
        yaxis=dict(
            gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR,
            tickfont=dict(color=TEXT_COLOR),
        ),
    )
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="brand-header">
  <span style="font-size:2.4rem">📞</span>
  <div>
    <p class="brand-title">Truecaller Sentiment Analysis Dashboard</p>
    <p class="brand-subtitle">
      Interactive review analytics · Spam trend analysis · NLP-powered insights
    </p>
  </div>
</div>
""", unsafe_allow_html=True)

if len(df) == 0:
    st.warning("⚠️ No records match the current filters. Try adjusting the sidebar selections.")
    st.stop()


# ═══════════════════════════════════════════════════════════════════════════════
# KPI CARDS
# ═══════════════════════════════════════════════════════════════════════════════
total        = len(df)
positive_cnt = len(df[df["sentiment"] == "Positive"])
negative_cnt = len(df[df["sentiment"] == "Negative"])
avg_rating   = df["rating"].mean()
pos_pct      = (positive_cnt / total * 100) if total else 0
neg_pct      = (negative_cnt / total * 100) if total else 0

k1, k2, k3, k4 = st.columns(4)

def kpi(col, css_class, icon, value, label, delta_html=""):
    col.markdown(
        f"""<div class="kpi-card {css_class}">
              <div class="kpi-icon">{icon}</div>
              <div class="kpi-value">{value}</div>
              <div class="kpi-label">{label}</div>
              {f'<div class="kpi-delta">{delta_html}</div>' if delta_html else ''}
            </div>""",
        unsafe_allow_html=True,
    )

kpi(k1, "kpi-total",  "📊", f"{total:,}",      "Total Reviews")
kpi(k2, "kpi-pos",    "😊", f"{positive_cnt:,}","Positive Reviews",
    f"<span style='color:#34d399'>▲ {pos_pct:.1f}%</span> of total")
kpi(k3, "kpi-neg",    "😞", f"{negative_cnt:,}","Negative Reviews",
    f"<span style='color:#f87171'>▼ {neg_pct:.1f}%</span> of total")
kpi(k4, "kpi-rating", "⭐", f"{avg_rating:.2f}","Avg Rating",
    "out of 5.0 stars")

st.markdown("<br>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# ROW 1  –  Sentiment pie  +  Rating bar
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="section-header">Sentiment & Rating Distribution</p>', unsafe_allow_html=True)

col_pie, col_bar = st.columns(2)

with col_pie:
    sent_counts = df["sentiment"].value_counts().reset_index()
    sent_counts.columns = ["Sentiment", "Count"]
    colours_sent = {"Positive": "#34d399", "Negative": "#f87171", "Neutral": "#94a3b8"}
    fig_pie = px.pie(
        sent_counts, names="Sentiment", values="Count",
        title="Sentiment Distribution",
        color="Sentiment",
        color_discrete_map=colours_sent,
        hole=0.45,
    )
    fig_pie.update_traces(
        textinfo="percent+label",
        textfont_color="#e2e8f0",
        marker=dict(line=dict(color=CHART_BG, width=3)),
    )
    fig_pie = apply_dark_theme(fig_pie)
    fig_pie.update_layout(showlegend=True, title_font_color="#cbd5e1")
    st.plotly_chart(fig_pie, use_container_width=True)

with col_bar:
    rating_counts = df["rating"].value_counts().sort_index().reset_index()
    rating_counts.columns = ["Rating", "Count"]
    rating_counts["Star"] = rating_counts["Rating"].apply(lambda x: "⭐" * int(x))
    colour_map = {1: "#ef4444", 2: "#f97316", 3: "#eab308", 4: "#22c55e", 5: "#34d399"}
    fig_bar = px.bar(
        rating_counts, x="Rating", y="Count",
        title="Rating Distribution",
        color="Rating",
        color_discrete_map=colour_map,
        text="Count",
    )
    fig_bar.update_traces(textposition="outside", textfont_color="#e2e8f0")
    fig_bar = apply_dark_theme(fig_bar)
    fig_bar.update_layout(
        showlegend=False, title_font_color="#cbd5e1",
        xaxis_title="Star Rating", yaxis_title="Number of Reviews",
        bargap=0.25,
    )
    st.plotly_chart(fig_bar, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# ROW 2  –  Yearly trend line  +  Spam trend
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="section-header">Trend Analysis</p>', unsafe_allow_html=True)

col_trend, col_spam = st.columns(2)

with col_trend:
    yearly = (
        df.groupby(["year", "sentiment"])
        .size()
        .reset_index(name="count")
    )
    colour_line = {"Positive": "#34d399", "Negative": "#f87171", "Neutral": "#94a3b8"}
    fig_line = px.line(
        yearly, x="year", y="count", color="sentiment",
        title="Year-wise Review Trends",
        color_discrete_map=colour_line,
        markers=True,
    )
    fig_line.update_traces(line_width=2.5, marker_size=7)
    fig_line = apply_dark_theme(fig_line)
    fig_line.update_layout(
        title_font_color="#cbd5e1",
        xaxis_title="Year", yaxis_title="Review Count",
        xaxis=dict(tickmode="linear", gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR),
    )
    st.plotly_chart(fig_line, use_container_width=True)

with col_spam:
    spam_year = (
        df[df["spam_mentioned"] == "Yes"]
        .groupby("year")
        .size()
        .reset_index(name="spam_reviews")
    )
    fig_spam = px.area(
        spam_year, x="year", y="spam_reviews",
        title="Spam-Mention Trend by Year",
        color_discrete_sequence=["#818cf8"],
    )
    fig_spam.update_traces(
        fill="tozeroy",
        fillcolor="rgba(129,140,248,0.18)",
        line_color="#818cf8",
        line_width=2.5,
    )
    fig_spam = apply_dark_theme(fig_spam)
    fig_spam.update_layout(
        title_font_color="#cbd5e1",
        xaxis_title="Year", yaxis_title="Reviews Mentioning Spam",
        xaxis=dict(tickmode="linear", gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR),
    )
    st.plotly_chart(fig_spam, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# ROW 3  –  Word Cloud  +  Country donut
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="section-header">Text Insights & Geography</p>', unsafe_allow_html=True)

col_wc, col_country = st.columns([1.3, 1])

with col_wc:
    st.markdown("**☁️ Word Cloud — Review Text**")
    text_blob = " ".join(df["review_text"].dropna().tolist())
    # Remove common stop-words inline (no nltk dependency)
    stop = {
        "the","a","an","and","or","but","in","on","at","to","for","of","with",
        "this","that","it","is","was","are","be","been","have","has","will",
        "not","no","my","your","i","me","we","you","they","he","she","its",
        "can","do","did","from","by","as","so","if","up","out","about","very",
        "just","also","more","some","all","there","then","than","been","their",
    }
    filtered = " ".join(
        w.lower() for w in re.findall(r"\b[a-zA-Z]{3,}\b", text_blob)
        if w.lower() not in stop
    )
    wc = WordCloud(
        width=700, height=350,
        background_color="#141927",
        colormap="cool",
        max_words=120,
        prefer_horizontal=0.85,
        min_font_size=10,
    ).generate(filtered)

    fig_wc, ax = plt.subplots(figsize=(8, 4))
    fig_wc.patch.set_facecolor("#141927")
    ax.set_facecolor("#141927")
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight",
                facecolor="#141927", dpi=140)
    buf.seek(0)
    plt.close(fig_wc)
    st.image(buf, use_container_width=True)

with col_country:
    country_cnt = df["country"].value_counts().reset_index()
    country_cnt.columns = ["Country", "Reviews"]
    fig_country = px.pie(
        country_cnt, names="Country", values="Reviews",
        title="Reviews by Country",
        color_discrete_sequence=ACCENT,
        hole=0.45,
    )
    fig_country.update_traces(
        textinfo="percent+label",
        textfont_color="#e2e8f0",
        marker=dict(line=dict(color=CHART_BG, width=2)),
    )
    fig_country = apply_dark_theme(fig_country, height=380)
    fig_country.update_layout(title_font_color="#cbd5e1", showlegend=True)
    st.plotly_chart(fig_country, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# ROW 4  –  Monthly heatmap  +  Rating boxplot per sentiment
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="section-header">Deep-Dive Analytics</p>', unsafe_allow_html=True)

col_heat, col_box = st.columns(2)

with col_heat:
    heatmap_data = (
        df.groupby(["year", "month"])
        .size()
        .reset_index(name="count")
    )
    pivot = heatmap_data.pivot(index="month", columns="year", values="count").fillna(0)
    month_names = ["Jan","Feb","Mar","Apr","May","Jun",
                   "Jul","Aug","Sep","Oct","Nov","Dec"]
    pivot.index = [month_names[m-1] for m in pivot.index]

    fig_heat = go.Figure(go.Heatmap(
        z=pivot.values,
        x=[str(c) for c in pivot.columns],
        y=pivot.index.tolist(),
        colorscale="Blues",
        showscale=True,
        hovertemplate="Year: %{x}<br>Month: %{y}<br>Reviews: %{z}<extra></extra>",
    ))
    fig_heat.update_layout(
        title="Monthly Review Heatmap",
        title_font_color="#cbd5e1",
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_BG,
        font=dict(color=TEXT_COLOR),
        height=360,
        margin=dict(l=20, r=20, t=40, b=20),
    )
    st.plotly_chart(fig_heat, use_container_width=True)

with col_box:
    colour_sent = {"Positive": "#34d399", "Negative": "#f87171", "Neutral": "#94a3b8"}
    fig_box = px.box(
        df, x="sentiment", y="rating",
        title="Rating Distribution by Sentiment",
        color="sentiment",
        color_discrete_map=colour_sent,
        points="outliers",
    )
    fig_box.update_traces(marker_size=4)
    fig_box = apply_dark_theme(fig_box)
    fig_box.update_layout(
        title_font_color="#cbd5e1", showlegend=False,
        xaxis_title="Sentiment", yaxis_title="Rating",
    )
    st.plotly_chart(fig_box, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# ROW 5  –  App version bar + Spam vs sentiment stacked
# ═══════════════════════════════════════════════════════════════════════════════
col_ver, col_stack = st.columns(2)

with col_ver:
    ver_data = (
        df.groupby("app_version")["rating"]
        .mean()
        .reset_index()
        .rename(columns={"rating": "avg_rating"})
        .sort_values("app_version")
    )
    fig_ver = px.bar(
        ver_data, x="app_version", y="avg_rating",
        title="Avg Rating by App Version",
        color="avg_rating",
        color_continuous_scale=["#ef4444","#eab308","#34d399"],
        text=ver_data["avg_rating"].round(2),
    )
    fig_ver.update_traces(textposition="outside", textfont_color="#e2e8f0")
    fig_ver = apply_dark_theme(fig_ver)
    fig_ver.update_layout(
        title_font_color="#cbd5e1",
        coloraxis_showscale=False,
        xaxis_title="App Version", yaxis_title="Avg Star Rating",
    )
    st.plotly_chart(fig_ver, use_container_width=True)

with col_stack:
    spam_sent = (
        df.groupby(["sentiment", "spam_mentioned"])
        .size()
        .reset_index(name="count")
    )
    colour_spam = {"Yes": "#f87171", "No": "#60a5fa"}
    fig_stack = px.bar(
        spam_sent, x="sentiment", y="count", color="spam_mentioned",
        title="Spam Mentions by Sentiment",
        color_discrete_map=colour_spam,
        barmode="stack",
    )
    fig_stack = apply_dark_theme(fig_stack)
    fig_stack.update_layout(
        title_font_color="#cbd5e1",
        xaxis_title="Sentiment", yaxis_title="Review Count",
        legend_title="Spam Mentioned",
    )
    st.plotly_chart(fig_stack, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# DATASET PREVIEW
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="section-header">📋 Dataset Preview</p>', unsafe_allow_html=True)

preview_cols = st.columns([1, 1, 1])
with preview_cols[0]:
    n_rows = st.slider("Rows to display", 5, 50, 10)
with preview_cols[1]:
    sort_col = st.selectbox("Sort by", ["date", "rating", "sentiment", "year"])
with preview_cols[2]:
    sort_asc = st.radio("Order", ["Descending", "Ascending"], horizontal=True) == "Ascending"

display_df = (
    df[["review_id","date","year","review_text","rating","sentiment",
        "spam_mentioned","country","app_version","helpful_count"]]
    .sort_values(sort_col, ascending=sort_asc)
    .head(n_rows)
    .reset_index(drop=True)
)

# Colour-code sentiment column
def colour_sentiment(val):
    colours = {
        "Positive": "background-color:#0f2a1e; color:#34d399",
        "Negative": "background-color:#2a0f0f; color:#f87171",
        "Neutral":  "background-color:#1a1f2e; color:#94a3b8",
    }
    return colours.get(val, "")

styled = display_df.style.map(colour_sentiment, subset=["sentiment"])
st.dataframe(styled, use_container_width=True, height=min(40 + n_rows * 36, 520))

# Download button
csv_bytes = df.to_csv(index=False).encode()
st.download_button(
    label="⬇️ Download Filtered Data as CSV",
    data=csv_bytes,
    file_name="truecaller_reviews_filtered.csv",
    mime="text/csv",
)


# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(
    "<center style='color:#334155; font-size:0.78rem'>"
    "📞 Truecaller Sentiment Analysis Dashboard &nbsp;·&nbsp; "
    "Built with Streamlit + Plotly &nbsp;·&nbsp; "
    "B.Tech CS Portfolio Project &nbsp;·&nbsp; "
    "Data Analyst | Python | SQL"
    "</center>",
    unsafe_allow_html=True,
)
