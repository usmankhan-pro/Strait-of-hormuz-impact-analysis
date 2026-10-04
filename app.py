"""
=============================================================================
STRAIT OF HORMUZ CLOSURE IMPACT ANALYSIS - INTERACTIVE STREAMLIT DASHBOARD
=============================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & THEME STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Strait of Hormuz Closure Impact Analysis",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
    }
    .metric-title {
        font-size: 0.85rem;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.05em;
        color: #64748b;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #0f172a;
        margin-top: 4px;
    }
    .metric-delta {
        font-size: 0.82rem;
        font-weight: 600;
    }
    .badge-critical { background-color: #fee2e2; color: #991b1b; padding: 3px 8px; border-radius: 6px; font-weight: 600; }
    .badge-high { background-color: #ffedd5; color: #9a3412; padding: 3px 8px; border-radius: 6px; font-weight: 600; }
    .badge-severe { background-color: #fef3c7; color: #92400e; padding: 3px 8px; border-radius: 6px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. LOAD DATASET WITH LAT/LON COORDINATES
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv('strait_of_hormuz_closure_impacts_cleaned.csv')
    
    # Coordinate dictionary for geospatial mapping
    coords = {
        'Saudi Arabia': {'lat': 23.8859, 'lon': 45.0792, 'iso': 'SAU'},
        'Iraq': {'lat': 33.2232, 'lon': 43.6793, 'iso': 'IRQ'},
        'United Arab Emirates': {'lat': 23.4241, 'lon': 53.8478, 'iso': 'ARE'},
        'Kuwait': {'lat': 29.3117, 'lon': 47.4818, 'iso': 'KWT'},
        'Qatar': {'lat': 25.3548, 'lon': 51.1839, 'iso': 'QAT'},
        'Iran': {'lat': 32.4279, 'lon': 53.6880, 'iso': 'IRN'},
        'China': {'lat': 35.8617, 'lon': 104.1954, 'iso': 'CHN'},
        'India': {'lat': 20.5937, 'lon': 78.9629, 'iso': 'IND'},
        'Japan': {'lat': 36.2048, 'lon': 138.2529, 'iso': 'JPN'},
        'South Korea': {'lat': 35.9078, 'lon': 127.7669, 'iso': 'KOR'},
        'Singapore': {'lat': 1.3521, 'lon': 103.8198, 'iso': 'SGP'},
        'Thailand': {'lat': 15.8700, 'lon': 100.9925, 'iso': 'THA'},
        'Pakistan': {'lat': 30.3753, 'lon': 69.3451, 'iso': 'PAK'},
        'Germany': {'lat': 51.1657, 'lon': 10.4515, 'iso': 'DEU'},
        'United States': {'lat': 37.0902, 'lon': -95.7129, 'iso': 'USA'}
    }
    
    df['lat'] = df['Country'].map(lambda x: coords.get(x, {}).get('lat', 0.0))
    df['lon'] = df['Country'].map(lambda x: coords.get(x, {}).get('lon', 0.0))
    df['iso_alpha'] = df['Country'].map(lambda x: coords.get(x, {}).get('iso', ''))
    return df

df_full = load_data()

# -----------------------------------------------------------------------------
# 3. SIDEBAR CONTROLS & FILTERS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/oil-pump.png", width=70)
    st.markdown("### 🎛️ Analysis Controls")
    
    # Region Multi-select
    regions = ['All'] + sorted(df_full['Region'].unique().tolist())
    selected_region = st.selectbox("Select Region", regions, index=0)
    
    # Role Multi-select
    roles = ['All'] + sorted(df_full['Role'].unique().tolist())
    selected_role = st.selectbox("Select Economic Role", roles, index=0)
    
    # Risk Level Multi-select
    risk_options = df_full['Economic_Impact_Risk'].unique().tolist()
    selected_risks = st.multiselect("Filter Risk Levels", risk_options, default=risk_options)
    
    # Transit Dependency Range Slider
    dep_range = st.slider(
        "Hormuz Transit Dependency Range (%)",
        min_value=0,
        max_value=100,
        value=(0, 100),
        step=5
    )
    
    st.markdown("---")
    st.markdown("### ⚡ Scenario Simulation")
    sim_days = st.slider("Disruption Duration (Days)", 7, 180, 30, step=7)
    oil_price = st.slider("Crude Oil Benchmark ($/bbl)", 60, 160, 85, step=5)
    
    st.markdown("---")
    st.markdown("<small>Data: Strait of Hormuz Closure Risk Dataset</small>", unsafe_allow_html=True)

# Apply Filters
df_filtered = df_full.copy()
if selected_region != 'All':
    df_filtered = df_filtered[df_filtered['Region'] == selected_region]
if selected_role != 'All':
    df_filtered = df_filtered[df_filtered['Role'] == selected_role]
if selected_risks:
    df_filtered = df_filtered[df_filtered['Economic_Impact_Risk'].isin(selected_risks)]
df_filtered = df_filtered[
    (df_filtered['Hormuz_Transit_Dependency_Pct'] >= dep_range[0]) &
    (df_filtered['Hormuz_Transit_Dependency_Pct'] <= dep_range[1])
]

# -----------------------------------------------------------------------------
# 4. MAIN DASHBOARD HEADER & KPI CARDS
# -----------------------------------------------------------------------------
st.markdown('<div class="main-title">⚓ Strait of Hormuz Closure Impact Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Interactive Geospatial, Volumetric & Macroeconomic Risk Simulator</div>', unsafe_allow_html=True)

if df_filtered.empty:
    st.warning("⚠️ No countries match the current filter selection. Please broaden your sidebar filters.")
    st.stop()

# Key Performance Indicators
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_vol = df_filtered['Daily_Volume_Affected_Mbd'].sum()
avg_dep = df_filtered['Hormuz_Transit_Dependency_Pct'].mean()
avg_gdp = df_filtered['Estimated_GDP_Impact_Pct'].mean()
crit_count = (df_filtered['Economic_Impact_Risk'] == 'Critical').sum()

with kpi1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Nations Analyzed</div>
        <div class="metric-value">{len(df_filtered)} <span style="font-size:1rem;color:#64748b">/ 15</span></div>
        <div class="metric-delta" style="color:#0284c7">Active Filter Selection</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Daily Disrupted Volume</div>
        <div class="metric-value">{total_vol:.1f} <span style="font-size:1rem;color:#64748b">Mbd</span></div>
        <div class="metric-delta" style="color:#ea580c">{(total_vol/26.3)*100:.1f}% of Global Sample</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Mean Transit Dependency</div>
        <div class="metric-value">{avg_dep:.1f}<span style="font-size:1rem;color:#64748b">%</span></div>
        <div class="metric-delta" style="color:#6366f1">Peak: {df_filtered['Hormuz_Transit_Dependency_Pct'].max():.0f}%</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Mean Estimated GDP Impact</div>
        <div class="metric-value" style="color:#dc2626">{avg_gdp:.1f}<span style="font-size:1rem;color:#dc2626">%</span></div>
        <div class="metric-delta" style="color:#dc2626">{crit_count} Nations in Critical Tier</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. TABS FOR MULTI-DIMENSIONAL ANALYSIS
# -----------------------------------------------------------------------------
tab_geo, tab_rank, tab_corr, tab_scenario, tab_data = st.tabs([
    "🌍 Interactive Global Map",
    "📊 Exposure & Rankings",
    "📈 Correlation & Statistical Analysis",
    "⚡ Scenario Simulator",
    "📋 Data Explorer"
])

# -----------------------------------------------------------------------------
# TAB 1: GEOSPATIAL MAP
# -----------------------------------------------------------------------------
with tab_geo:
    st.subheader("Global Chokepoint Exposure Map")
    st.caption("Bubble size indicates daily hydrocarbon volume affected (Mbd). Color intensity indicates estimated GDP contraction (%).")
    
    fig_map = px.scatter_geo(
        df_filtered,
        lat='lat',
        lon='lon',
        hover_name='Country',
        size='Daily_Volume_Affected_Mbd',
        color='Estimated_GDP_Impact_Pct',
        color_continuous_scale='Reds_r',
        size_max=38,
        projection='natural earth',
        hover_data={
            'lat': False,
            'lon': False,
            'Region': True,
            'Role': True,
            'Hormuz_Transit_Dependency_Pct': ':.1f',
            'Daily_Volume_Affected_Mbd': ':.2f',
            'Estimated_GDP_Impact_Pct': ':.1f',
            'Alternative_Route_Availability': True,
            'Primary_Energy_Risk': True
        }
    )
    fig_map.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        height=520,
        geo=dict(
            showcoastlines=True,
            coastlinecolor="#cbd5e1",
            showland=True,
            landcolor="#f1f5f9",
            showocean=True,
            oceancolor="#e0f2fe",
            showlakes=True,
            lakecolor="#e0f2fe"
        )
    )
    st.plotly_chart(fig_map, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 2: RANKINGS & DISTRIBUTIONS
# -----------------------------------------------------------------------------
with tab_rank:
    col_r1, col_r2 = st.columns(2)
    
    with col_r1:
        st.subheader("Hormuz Dependency by Country")
        sorted_dep = df_filtered.sort_values('Hormuz_Transit_Dependency_Pct', ascending=True)
        fig_dep = px.bar(
            sorted_dep,
            x='Hormuz_Transit_Dependency_Pct',
            y='Country',
            orientation='h',
            color='Role',
            color_discrete_map={'Exporter': '#ef4444', 'Importer': '#0ea5e9'},
            text='Hormuz_Transit_Dependency_Pct',
            labels={'Hormuz_Transit_Dependency_Pct': 'Dependency (%)', 'Country': ''}
        )
        fig_dep.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_dep.update_layout(height=480, margin=dict(l=0, r=30, t=20, b=20))
        st.plotly_chart(fig_dep, use_container_width=True)

    with col_r2:
        st.subheader("Daily Affected Volume (Mbd)")
        sorted_vol = df_filtered.sort_values('Daily_Volume_Affected_Mbd', ascending=True)
        fig_vol = px.bar(
            sorted_vol,
            x='Daily_Volume_Affected_Mbd',
            y='Country',
            orientation='h',
            color='Economic_Impact_Risk',
            color_discrete_map={
                'Critical': '#b91c1c',
                'Severe': '#ea580c',
                'High': '#f59e0b',
                'Moderate': '#3b82f6',
                'Low': '#10b981'
            },
            text='Daily_Volume_Affected_Mbd',
            labels={'Daily_Volume_Affected_Mbd': 'Volume (Mbd)', 'Country': ''}
        )
        fig_vol.update_traces(texttemplate='%{text:.2f} Mbd', textposition='outside')
        fig_vol.update_layout(height=480, margin=dict(l=0, r=40, t=20, b=20))
        st.plotly_chart(fig_vol, use_container_width=True)

    st.markdown("---")
    
    col_r3, col_r4 = st.columns(2)
    with col_r3:
        st.subheader("Estimated GDP Impact Distribution by Role")
        fig_box = px.box(
            df_filtered,
            x='Role',
            y='Estimated_GDP_Impact_Pct',
            color='Role',
            points='all',
            color_discrete_map={'Exporter': '#ef4444', 'Importer': '#0ea5e9'},
            labels={'Estimated_GDP_Impact_Pct': 'GDP Impact (%)', 'Role': 'Economic Role'}
        )
        fig_box.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)

    with col_r4:
        st.subheader("Regional Volume & Country Breakdown")
        fig_sun = px.sunburst(
            df_filtered,
            path=['Region', 'Role', 'Country'],
            values='Daily_Volume_Affected_Mbd',
            color='Estimated_GDP_Impact_Pct',
            color_continuous_scale='Reds_r'
        )
        fig_sun.update_layout(height=400, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_sun, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 3: CORRELATION & STATISTICAL ANALYSIS
# -----------------------------------------------------------------------------
with tab_corr:
    st.subheader("Multi-Variable Relationship Analysis")
    
    col_c1, col_c2 = st.columns([1.8, 1.2])
    
    with col_c1:
        fig_scatter = px.scatter(
            df_filtered,
            x='Hormuz_Transit_Dependency_Pct',
            y='Estimated_GDP_Impact_Pct',
            size='Daily_Volume_Affected_Mbd',
            color='Role',
            hover_name='Country',
            trendline='ols',
            color_discrete_map={'Exporter': '#ef4444', 'Importer': '#0ea5e9'},
            labels={
                'Hormuz_Transit_Dependency_Pct': 'Hormuz Transit Dependency (%)',
                'Estimated_GDP_Impact_Pct': 'Estimated GDP Impact (%)',
                'Daily_Volume_Affected_Mbd': 'Volume (Mbd)'
            }
        )
        fig_scatter.update_layout(height=480)
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    with col_c2:
        st.markdown("#### Correlation Matrix")
        corr_subset = df_filtered[['Hormuz_Transit_Dependency_Pct', 'Daily_Volume_Affected_Mbd', 'Estimated_GDP_Impact_Pct']].corr()
        fig_heat = px.imshow(
            corr_subset,
            text_auto='.2f',
            color_continuous_scale='RdBu_r',
            zmin=-1,
            zmax=1
        )
        fig_heat.update_layout(height=380, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_heat, use_container_width=True)
        
        st.info("""
        **Statistical Note**:
        Dependency shows a moderate-to-strong negative association with GDP impact ($r = -0.64$).
        Exporters experience much steeper declines due to direct fiscal reliance on oil sales.
        """)

# -----------------------------------------------------------------------------
# TAB 4: SCENARIO SIMULATOR
# -----------------------------------------------------------------------------
with tab_scenario:
    st.subheader("⚡ Closure Scenario Impact Simulator")
    st.caption(f"Simulating a **{sim_days}-day** full physical closure at **${oil_price}/barrel** benchmark price.")
    
    # Calculate simulated losses
    df_sim = df_filtered.copy()
    # Total barrels disrupted = Daily Volume (Mbd) * 1,000,000 * Days
    df_sim['Disrupted_Barrels_M'] = df_sim['Daily_Volume_Affected_Mbd'] * sim_days
    df_sim['Estimated_Dollar_Value_B'] = (df_sim['Disrupted_Barrels_M'] * oil_price) / 1000.0  # In Billion USD
    
    tot_disrupted_bbl = df_sim['Disrupted_Barrels_M'].sum()
    tot_dollar_value = df_sim['Estimated_Dollar_Value_B'].sum()
    
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        st.metric("Total Cumulative Disrupted Barrels", f"{tot_disrupted_bbl:.1f} Million Bbls")
    with sc2:
        st.metric("Total Gross Flow Value Disrupted", f"${tot_dollar_value:.1f} Billion USD")
    with sc3:
        st.metric("Estimated Daily Financial Shock", f"${(tot_dollar_value/sim_days)*1000:.1f} Million/Day")
        
    fig_sim = px.bar(
        df_sim.sort_values('Estimated_Dollar_Value_B', ascending=False),
        x='Country',
        y='Estimated_Dollar_Value_B',
        color='Role',
        color_discrete_map={'Exporter': '#ef4444', 'Importer': '#0ea5e9'},
        text='Estimated_Dollar_Value_B',
        labels={'Estimated_Dollar_Value_B': f'Disrupted Trade Value ($ Billion over {sim_days} Days)'}
    )
    fig_sim.update_traces(texttemplate='$%{text:.1f}B', textposition='outside')
    fig_sim.update_layout(height=450)
    st.plotly_chart(fig_sim, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 5: DATA EXPLORER & EXPORT
# -----------------------------------------------------------------------------
with tab_data:
    st.subheader("Filtered Dataset Explorer")
    
    st.dataframe(
        df_filtered[[
            'Country', 'Region', 'Role', 'Hormuz_Transit_Dependency_Pct',
            'Daily_Volume_Affected_Mbd', 'Estimated_GDP_Impact_Pct',
            'Economic_Impact_Risk', 'Alternative_Route_Availability', 'Primary_Energy_Risk'
        ]],
        use_container_width=True,
        hide_index=True
    )
    
    csv_download = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Current Filtered View (CSV)",
        data=csv_download,
        file_name="strait_of_hormuz_filtered_data.csv",
        mime="text/csv"
    )
