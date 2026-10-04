import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['figure.autolayout'] = True

# 1. LOAD DATASET
csv_path = 'strait_of_hormuz_closure_impacts.csv'
df = pd.read_csv(csv_path)

# 2. DATA CLEANING
df_clean = df.copy()
df_clean['Alternative_Route_Availability'] = df_clean['Alternative_Route_Availability'].fillna('None (No Alternate Route)')

region_agg = df_clean.groupby('Region').agg(
    Avg_Dependency=('Hormuz_Transit_Dependency_Pct', 'mean'),
    Total_Volume_Mbd=('Daily_Volume_Affected_Mbd', 'sum'),
    Avg_GDP_Impact=('Estimated_GDP_Impact_Pct', 'mean'),
    Country_Count=('Country', 'count')
).reset_index()

# 5. MATPLOTLIB VISUALIZATIONS
fig, ax = plt.subplots(figsize=(10, 6))
sorted_dep = df_clean.sort_values('Hormuz_Transit_Dependency_Pct', ascending=True)
ax.barh(sorted_dep['Country'], sorted_dep['Hormuz_Transit_Dependency_Pct'], color='#1f77b4', edgecolor='black', alpha=0.85)
ax.set_title('Hormuz Transit Dependency by Country (%)', fontsize=14, fontweight='bold', pad=12)
ax.set_xlabel('Hormuz Dependency Percentage (%)', fontsize=12)
ax.set_ylabel('Country', fontsize=12)
plt.savefig('chart1_dependency_by_country.png', dpi=300)
plt.close()

fig, ax = plt.subplots(figsize=(10, 6))
sorted_vol = df_clean.sort_values('Daily_Volume_Affected_Mbd', ascending=True)
ax.barh(sorted_vol['Country'], sorted_vol['Daily_Volume_Affected_Mbd'], color='#ff7f0e', edgecolor='black', alpha=0.85)
ax.set_title('Daily Hydrocarbon Volume Affected by Country (Million Barrels/Day)', fontsize=14, fontweight='bold', pad=12)
ax.set_xlabel('Daily Volume Affected (Mbd)', fontsize=12)
ax.set_ylabel('Country', fontsize=12)
plt.savefig('chart2_volume_by_country.png', dpi=300)
plt.close()

fig, ax = plt.subplots(figsize=(10, 6))
sorted_gdp = df_clean.sort_values('Estimated_GDP_Impact_Pct', ascending=False)
ax.barh(sorted_gdp['Country'], sorted_gdp['Estimated_GDP_Impact_Pct'], color='#d62728', edgecolor='black', alpha=0.85)
ax.set_title('Estimated GDP Contraction by Country (%)', fontsize=14, fontweight='bold', pad=12)
ax.set_xlabel('Estimated GDP Impact (%)', fontsize=12)
ax.set_ylabel('Country', fontsize=12)
plt.savefig('chart3_gdp_impact_by_country.png', dpi=300)
plt.close()

fig, ax = plt.subplots(figsize=(8, 5))
sorted_reg_vol = region_agg.sort_values('Total_Volume_Mbd', ascending=False)
ax.bar(sorted_reg_vol['Region'], sorted_reg_vol['Total_Volume_Mbd'], color=['#2ca02c', '#9467bd', '#8c564b', '#e377c2'], edgecolor='black', alpha=0.85)
ax.set_title('Total Daily Hydrocarbon Volume Affected by Region (Mbd)', fontsize=14, fontweight='bold', pad=12)
ax.set_xlabel('Region', fontsize=12)
ax.set_ylabel('Total Volume Affected (Mbd)', fontsize=12)
plt.savefig('chart4_volume_by_region.png', dpi=300)
plt.close()

# 6. SEABORN VISUALIZATIONS
fig, ax = plt.subplots(figsize=(9, 6))
sns.scatterplot(data=df_clean, x='Hormuz_Transit_Dependency_Pct', y='Estimated_GDP_Impact_Pct', hue='Role', style='Region', s=140, palette={'Exporter': '#d62728', 'Importer': '#1f77b4'}, ax=ax)
sns.regplot(data=df_clean, x='Hormuz_Transit_Dependency_Pct', y='Estimated_GDP_Impact_Pct', scatter=False, color='gray', line_kws={'linestyle': '--', 'linewidth': 1.5}, ax=ax)
ax.set_title('Hormuz Dependency vs. Estimated GDP Impact by Country Role', fontsize=13, fontweight='bold')
ax.set_xlabel('Hormuz Transit Dependency (%)', fontsize=11)
ax.set_ylabel('Estimated GDP Impact (%)', fontsize=11)
plt.savefig('chart5_scatter_dep_vs_gdp.png', dpi=300)
plt.close()

fig, ax = plt.subplots(figsize=(7, 5))
sns.boxplot(data=df_clean, x='Role', y='Estimated_GDP_Impact_Pct', palette=['#ff9999', '#99ccff'], ax=ax, width=0.4)
sns.stripplot(data=df_clean, x='Role', y='Estimated_GDP_Impact_Pct', color='black', size=7, jitter=0.2, ax=ax)
ax.set_title('Distribution of Estimated GDP Impact: Exporters vs Importers', fontsize=13, fontweight='bold')
ax.set_xlabel('Country Economic Role', fontsize=11)
ax.set_ylabel('Estimated GDP Impact (%)', fontsize=11)
plt.savefig('chart6_boxplot_role_gdp.png', dpi=300)
plt.close()

fig, ax = plt.subplots(figsize=(8, 5))
risk_order = ['Critical', 'High', 'Severe', 'Moderate', 'Low']
sns.countplot(data=df_clean, x='Economic_Impact_Risk', order=risk_order, palette='Reds_r', edgecolor='black', ax=ax)
ax.set_title('Frequency of Economic Impact Risk Severity Levels', fontsize=13, fontweight='bold')
ax.set_xlabel('Risk Classification', fontsize=11)
ax.set_ylabel('Number of Countries', fontsize=11)
plt.savefig('chart7_countplot_risk.png', dpi=300)
plt.close()

fig, ax = plt.subplots(figsize=(7, 5))
corr_df = df_clean[['Hormuz_Transit_Dependency_Pct', 'Daily_Volume_Affected_Mbd', 'Estimated_GDP_Impact_Pct']].corr()
sns.heatmap(corr_df, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt='.2f', linewidths=1, ax=ax)
ax.set_title('Correlation Matrix of Numerical Risk Factors', fontsize=13, fontweight='bold')
plt.savefig('chart8_correlation_heatmap.png', dpi=300)
plt.close()

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=region_agg.sort_values('Avg_Dependency', ascending=False), x='Region', y='Avg_Dependency', palette='Blues_r', edgecolor='black', ax=ax)
ax.set_title('Average Hormuz Transit Dependency by Region (%)', fontsize=13, fontweight='bold')
ax.set_xlabel('Region', fontsize=11)
ax.set_ylabel('Average Dependency (%)', fontsize=11)
plt.savefig('chart9_avg_dependency_by_region.png', dpi=300)
plt.close()

# 7. INTEGRATED PORTFOLIO DASHBOARD
fig = plt.figure(figsize=(18, 12))
gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.3)

kpi_ax = fig.add_subplot(gs[0, :])
kpi_ax.axis('off')
kpi_text = (
    "STRAIT OF HORMUZ CLOSURE IMPACT EXECUTIVE SUMMARY\n"
    "------------------------------------------------------------------------------------------------------------------------\n"
    f"  Total Countries Analyzed: {len(df_clean)}   |   "
    f"Total Daily Volume Affected: {df_clean['Daily_Volume_Affected_Mbd'].sum():.1f} Mbd   |   "
    f"Mean Hormuz Dependency: {df_clean['Hormuz_Transit_Dependency_Pct'].mean():.1f}%   |   "
    f"Mean GDP Contraction: {df_clean['Estimated_GDP_Impact_Pct'].mean():.1f}%"
)
kpi_ax.text(0.5, 0.5, kpi_text, fontsize=13, fontweight='bold', ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.8', facecolor='#f0f4f8', edgecolor='#334e68', linewidth=1.5))

ax1 = fig.add_subplot(gs[1, 0])
sorted_c = df_clean.sort_values('Hormuz_Transit_Dependency_Pct')
ax1.barh(sorted_c['Country'], sorted_c['Hormuz_Transit_Dependency_Pct'], color='#1f77b4', edgecolor='black', alpha=0.85)
ax1.set_title('Hormuz Dependency (%)', fontsize=11, fontweight='bold')
ax1.set_xlabel('% Transit Dependency', fontsize=9)

ax2 = fig.add_subplot(gs[1, 1])
sns.scatterplot(data=df_clean, x='Hormuz_Transit_Dependency_Pct', y='Estimated_GDP_Impact_Pct', hue='Role', s=90, palette={'Exporter': '#d62728', 'Importer': '#1f77b4'}, ax=ax2)
ax2.set_title('Dependency vs. GDP Impact', fontsize=11, fontweight='bold')
ax2.set_xlabel('Dependency (%)', fontsize=9)
ax2.set_ylabel('GDP Impact (%)', fontsize=9)

ax3 = fig.add_subplot(gs[1, 2])
reg_sorted = region_agg.sort_values('Total_Volume_Mbd', ascending=False)
ax3.bar(reg_sorted['Region'], reg_sorted['Total_Volume_Mbd'], color='#2ca02c', edgecolor='black', alpha=0.85)
ax3.set_title('Total Affected Volume by Region (Mbd)', fontsize=11, fontweight='bold')
ax3.set_xlabel('Region', fontsize=9)
ax3.set_ylabel('Volume (Mbd)', fontsize=9)
ax3.tick_params(axis='x', rotation=20)

ax4 = fig.add_subplot(gs[2, 0])
sns.boxplot(data=df_clean, x='Role', y='Estimated_GDP_Impact_Pct', palette=['#ff9999', '#99ccff'], ax=ax4, width=0.4)
ax4.set_title('GDP Impact by Role', fontsize=11, fontweight='bold')
ax4.set_xlabel('Role', fontsize=9)
ax4.set_ylabel('GDP Impact (%)', fontsize=9)

ax5 = fig.add_subplot(gs[2, 1])
sns.countplot(data=df_clean, x='Economic_Impact_Risk', order=['Critical', 'High', 'Severe', 'Moderate', 'Low'], palette='Reds_r', edgecolor='black', ax=ax5)
ax5.set_title('Economic Risk Severity Count', fontsize=11, fontweight='bold')
ax5.set_xlabel('Risk Category', fontsize=9)
ax5.set_ylabel('Count', fontsize=9)
ax5.tick_params(axis='x', rotation=20)

ax6 = fig.add_subplot(gs[2, 2])
sns.heatmap(corr_df, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt='.2f', ax=ax6, cbar=False)
ax6.set_title('Metric Correlations', fontsize=11, fontweight='bold')

plt.suptitle('Strait of Hormuz Closure Risk & Impact Portfolio Dashboard', fontsize=16, fontweight='bold', y=0.98)
plt.savefig('dashboard_portfolio.png', dpi=300)
plt.close()

print('All Python charts generated successfully!')
