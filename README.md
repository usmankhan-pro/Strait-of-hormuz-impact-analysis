# Strait of Hormuz Impact Monitor

A browser-based dashboard for exploring country exposure to a potential Strait of Hormuz disruption. Includes interactive filters, a global exposure map, country rankings, correlation analysis, scenario estimates, and filtered CSV export.

## Deploy on Vercel

1. Push the repository changes to GitHub and wait for Vercel to redeploy the connected project.
2. In Vercel, set **Root Directory** to `.` (the repository root) and **Framework Preset** to **Other**.
3. Leave **Build Command** and **Install Command** blank. Set **Output Directory** to `.` if the project settings require one.
4. Redeploy. Vercel should serve the root `index.html`; the cleaned CSV and frontend assets must remain in the same repository root.

The repository includes `vercel.json` for clean URL behavior. No Python runtime or build step is required for the website. Plotly.js and the display fonts are loaded from public CDNs; all analysis data is bundled in the repository.

## Run the website locally

Serve the repository root with any static file server, for example:

```bash
python -m http.server 4173
```

Then open `http://localhost:4173`.

## Run the original Streamlit analysis

The original Python dashboard remains available as `app.py`:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```
