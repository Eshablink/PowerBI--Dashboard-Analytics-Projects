# 🎵 Spotify Analytics Dashboard

> **A modern, interactive data analytics dashboard built with Python · Streamlit · Plotly · Pandas**
> 
> Portfolio project by **Dabbara Esha** — Data Analyst | Python Developer | SQL

---

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.22-3F4F75?logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.2-150458?logo=pandas&logoColor=white)

---

## 📸 Dashboard Preview

![Dashboard Preview](https://via.placeholder.com/900x500/0d0d0d/1db954?text=Spotify+Analytics+Dashboard)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎛️ **Sidebar Filters** | Filter by genre, release year range, popularity score, explicit content |
| 📊 **KPI Cards** | Total tracks, streams (billions), avg popularity, top artist, top genre |
| 🏆 **Top Artists Chart** | Horizontal bar chart — top 10 artists by total streams |
| 🍩 **Genre Donut Chart** | Genre distribution with track count in centre |
| 📈 **Yearly Trends** | Dual-axis chart: streams + track count over years |
| 🌊 **Area Chart** | Streams breakdown by genre over time |
| 🕸️ **Radar Chart** | Average audio features (danceability, energy, valence, tempo) per genre |
| 🔵 **Scatter Plot** | Popularity vs streams, bubble size = track duration |
| 🏅 **Top 10 Table** | Gradient-highlighted top tracks table |
| 🔍 **Dataset Explorer** | Searchable, filterable full dataset preview |

---

## 🗂️ Folder Structure

```
spotify-analytics-dashboard/
│
├── app.py                  ← Main Streamlit application
├── spotify_data.csv        ← Sample dataset (75 tracks)
├── requirements.txt        ← Python dependencies
└── README.md               ← This file
```

---

## 🚀 Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/spotify-analytics-dashboard.git
cd spotify-analytics-dashboard
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```

The app opens at **http://localhost:8501** in your browser.

---

## ☁️ Deploy on Streamlit Cloud (Free)

1. Push this repo to your **GitHub** account
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **"New app"**
4. Select your repo → branch: `main` → Main file: `app.py`
5. Click **"Deploy"** — live in ~2 minutes! 🎉

> **Streamlit Cloud auto-reads `requirements.txt`** — no extra config needed.

---

## 📦 Tech Stack

```
Python 3.10+
├── streamlit      → Web app framework
├── plotly         → Interactive charts
└── pandas         → Data manipulation
```

---

## 📊 Dataset

The `spotify_data.csv` contains **75 sample tracks** with the following columns:

| Column | Description |
|---|---|
| `track_name` | Name of the song |
| `artist_name` | Performing artist |
| `album_name` | Album the track belongs to |
| `genre` | Music genre (Pop, Hip-Hop, Rock, etc.) |
| `release_year` | Year of release (2000–2022) |
| `streams` | Total Spotify streams |
| `duration_min` | Track duration in minutes |
| `popularity` | Spotify popularity score (0–100) |
| `danceability` | How suitable for dancing (0–100) |
| `energy` | Intensity & activity level (0–100) |
| `valence` | Musical positivity (0–100) |
| `tempo` | Beats per minute |
| `explicit` | Whether the track has explicit content |

---

## 🎯 Skills Demonstrated

- ✅ **Python** — data processing, filtering, aggregation
- ✅ **Pandas** — groupby, sort, merge, column creation
- ✅ **Plotly** — bar, pie, scatter, area, radar, dual-axis charts
- ✅ **Streamlit** — layout, sidebar, caching, expander, dataframe styling
- ✅ **Data Visualisation** — dashboard design, colour theory, UX
- ✅ **Deployment** — Streamlit Cloud ready, clean project structure

---

## 👩‍💻 About Me

**Dabbara Esha**  
B.Tech Computer Science Engineering · Mohan Babu University (CGPA 9.4)  
Data Analyst | Python Developer | SQL

- 📧 eshascs@gmail.com  
- 💼 [LinkedIn](https://linkedin.com)  
- 🐙 [GitHub](https://github.com)

---

## 📄 License

This project is open source under the [MIT License](LICENSE).

---

<div align="center">
  <b>⭐ If you found this useful, please star the repo! ⭐</b>
</div>
