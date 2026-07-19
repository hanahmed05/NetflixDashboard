# Netflix Content Dashboard

An interactive dashboard exploring the Netflix titles dataset, built with [Dash](https://dash.plotly.com/) (Plotly). Filter by content type, country, and release year range to see four linked visualizations — a release trend line chart, a movies-vs-TV-shows pie chart, a top-genres bar chart, and a movie duration scatter plot — update together in real time.

**Live dashboard:** https://netflix-dashboard-6wrp.onrender.com/
**Video walkthrough:** https://drive.google.com/file/d/12cRxAHXj5doZ_FD3-MYgOz4611WcStrU/view?usp=sharing

> Note: this app is hosted on Render's free tier, which spins down after periods of inactivity. The first load after idle time may take 30-50 seconds to wake up — please be patient on the initial visit.

## Features

- **Content Type filter** — All / Movie / TV Show
- **Country filter** — filter by a title's primary listed country
- **Release Year range slider** — narrow to any year span in the dataset
- **KPI cards** — total titles, movie count, TV show count, and average movie length, all recalculated live
- **Four linked charts** — line, pie, bar, and scatter, all responding to the same filter selections simultaneously

## Dataset

Uses `netflix_titles.csv` (Kaggle's Netflix Movies and TV Shows dataset). Cleaning steps applied in `app.py`:
- Duplicate rows removed
- `date_added` parsed to datetime; unparseable rows dropped
- Missing `director`, `cast`, `country`, and `rating` values filled as `"Unknown"`
- `duration` split into a numeric value and a type (`Movie` / `TV Show`)
- `listed_in` reduced to a single primary genre per title
- `country` reduced to a single primary country per title

## Project Structure

```
NetflixDashboard/
│
├── app.py                  # Dash application
├── netflix_titles.csv      # Dataset
├── requirements.txt        # Python dependencies
├── README.md                # This file
```

## Running Locally

**1. Clone the repository**
```bash
git clone https://github.com/hanahmed05/NetflixDashboard.git
cd NetflixDashboard
```

**2. Install dependencies**
```bash
pip3 install -r requirements.txt
```

**3. Run the app**
```bash
python3 app.py
```

**4. Open the dashboard**

Visit the URL printed in the terminal, typically:
```
http://127.0.0.1:8050/
```

## Deployment

This app is deployed on [Render](https://render.com) as a web service, using `gunicorn` to serve the Dash app's underlying Flask server (`app.server`).

- **Build command:** `pip install -r requirements.txt`
- **Start command:** `gunicorn app:server`

## Tech Stack

- [Dash](https://dash.plotly.com/) — reactive web app framework built on Flask, React, and Plotly.js
- [Plotly Express](https://plotly.com/python/plotly-express/) — chart generation
- [pandas](https://pandas.pydata.org/) / [NumPy](https://numpy.org/) — data cleaning and manipulation
- [Gunicorn](https://gunicorn.org/) — production WSGI server for deployment

## Author

Hana Ahmed
