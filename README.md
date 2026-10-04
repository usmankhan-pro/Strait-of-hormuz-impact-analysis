# Strait of Hormuz Closure Impact Dashboard

Interactive analysis of country exposure to a potential Strait of Hormuz disruption, with regional filters, risk rankings, a global map, correlation analysis, scenario simulation, and CSV export.

[![Deploy to Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy?repository=usmankhan-pro/Strait-of-hormuz-impact-analysis&branch=main&mainModule=app.py)

## Deploy online

1. Push the repository to GitHub.
2. Select **Deploy to Streamlit** above and sign in to Streamlit Community Cloud with GitHub.
3. Confirm `main` as the branch and `app.py` as the entry point, then deploy.
4. Streamlit Community Cloud will provide a public URL for the dashboard.

The app and cleaned CSV are included in this repository. Dependencies are defined in `requirements.txt` and the dashboard theme is in `.streamlit/config.toml`.

## Run locally

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Hosting note

This project uses Streamlit's persistent app server and WebSocket session model. Vercel Functions/Pages do not host Streamlit directly; use Streamlit Community Cloud for this app. To host on Vercel, the dashboard would need to be rebuilt as a static or serverless web application.
