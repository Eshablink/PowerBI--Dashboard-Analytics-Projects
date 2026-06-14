# 📞 Truecaller Sentiment Analysis Dashboard

> **B.Tech CS Final-Year Portfolio Project** — built to demonstrate real-world Data Analyst skills in Python, NLP, and interactive dashboarding.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B?style=flat-square&logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-5.x-3F4F75?style=flat-square&logo=plotly)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 🎯 Project Overview

An end-to-end interactive data analytics dashboard that analyzes **1,000 Truecaller app reviews** to surface insights on:

- User sentiment (Positive / Negative / Neutral)
- Spam-call mention trends over the years
- Star rating distributions
- Country-level breakdown
- Word frequency from review text
- App-version performance

The dark-themed dashboard is built with **Streamlit + Plotly** and is ready to deploy on **Streamlit Cloud** in one click.

---

## 🗂️ Folder Structure

```
truecaller-sentiment-dashboard/
│
├── app.py                    # Main Streamlit application
├── truecaller_reviews.csv    # Sample dataset (1 000 rows)
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

---

## ✨ Features

| Feature | Details |
|---|---|
| 🎨 Dark UI | Professional dark-theme with CSS overrides |
| 📊 KPI Cards | Total reviews · Positive · Negative · Avg rating |
| 🥧 Sentiment Pie | Donut chart with percentage labels |
| ⭐ Rating Bar | Colour-coded per star level |
| 📈 Yearly Trend | Multi-line chart by sentiment |
| 📉 Spam Area Chart | Spam-mention volume over years |
| ☁️ Word Cloud | Top keywords from review text |
| 🌍 Country Donut | Geographic distribution |
| 🔥 Monthly Heatmap | Review volume by month × year |
| 📦 Version Analysis | Avg rating per app version |
| 🔍 Sidebar Filters | Year · Sentiment · Rating · Country · Text search |
| 📋 Dataset Preview | Sortable, styled, downloadable table |

---

## 🚀 Run Locally

### 1 — Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/truecaller-sentiment-dashboard.git
cd truecaller-sentiment-dashboard
```

### 2 — Create a virtual environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### 4 — Launch the dashboard

```bash
streamlit run app.py
```

The app opens at **http://localhost:8501** in your browser.

---

## ☁️ Deploy to Streamlit Cloud (Free)

1. Push this repository to **GitHub** (public repo).
2. Visit [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app** → choose your repo → set **Main file path** to `app.py`.
4. Click **Deploy** — your live URL is ready in ~2 minutes!

> No extra configuration needed. All dependencies are in `requirements.txt`.

---

## 📦 Dataset Schema

`truecaller_reviews.csv` — 1 000 rows, 12 columns

| Column | Type | Description |
|---|---|---|
| `review_id` | string | Unique review identifier |
| `date` | date | Review submission date |
| `year` | int | Review year (2019–2024) |
| `month` | int | Review month (1–12) |
| `review_text` | string | Full review content |
| `rating` | int | Star rating (1–5) |
| `sentiment` | string | Positive / Negative / Neutral |
| `spam_mentioned` | string | Yes / No |
| `country` | string | Reviewer's country |
| `app_version` | string | Truecaller version at review time |
| `helpful_count` | int | Thumbs-up count |
| `review_length` | int | Character count of review |

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Streamlit** — web dashboard framework
- **Pandas** — data manipulation
- **Plotly** — interactive charts
- **WordCloud + Matplotlib** — word frequency visualisation
- **Scikit-learn** (listed in requirements for future ML extensions)
- **NumPy** — numerical operations

---

## 💡 Potential Extensions

- [ ] Live Google Play review scraper integration
- [ ] ML-based sentiment classifier (Logistic Regression / BERT)
- [ ] SQL database backend (SQLite / PostgreSQL)
- [ ] Export charts as PNG / PDF report
- [ ] Email alert for sudden rating drops

---

## 👤 About

Built by a **Final-Year B.Tech Computer Science** student targeting Data Analyst roles.

Skills demonstrated: `Python` · `Pandas` · `Data Visualisation` · `NLP Basics` · `Streamlit` · `Dashboard Design` · `Git/GitHub`

---

## 📄 License

MIT — free to use, modify, and share.
