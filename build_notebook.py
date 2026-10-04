import json

cells = []

def add_md(text):
    cells.append({
        'cell_type': 'markdown',
        'metadata': {},
        'source': [line + '\n' for line in text.strip().split('\n')]
    })

def add_code(code):
    cells.append({
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [line + '\n' for line in code.strip().split('\n')]
    })

# 1. Title
add_md("""# Project: Strait of Hormuz Closure Impact Analysis
**Author:** Data Analysis Student Portfolio  
**Tools:** Python, NumPy, Pandas, Matplotlib, Seaborn  
**Dataset:** `strait_of_hormuz_closure_impacts.csv`  

---""")

# 2. Introduction
add_md("""## 1. Project Introduction
The **Strait of Hormuz** is widely recognized as the world's most critical maritime oil and LNG transit chokepoint. Located between Oman and Iran, it connects the Persian Gulf with the Gulf of Oman and the Arabian Sea. Approximately 20–30% of global petroleum consumption and massive volumes of LNG pass through this narrow waterway daily.

A prolonged physical disruption or blockade of the Strait would trigger severe shocks to global energy supply chains, sovereign budgets, and international economic stability.

### Purpose of this Analysis
This project provides a comprehensive quantitative evaluation of the geopolitical and macroeconomic risks posed by a potential closure of the Strait of Hormuz across **15 representative nations**. Using Python's core data-science stack (**NumPy, Pandas, Matplotlib, and Seaborn**), we systematically analyze:
* Exposure levels (Transit Dependency %)
* Physical volume at risk (Million Barrels per Day - Mbd)
* Macroeconomic vulnerability (Estimated GDP Impact %)
* Regional disparities and structural differences between **Net Energy Exporters** and **Net Energy Importers**.""")

# 3. Problem Statement
add_md("""## 2. Problem Statement
Disruptions to maritime energy transit corridors do not affect all economies uniformly. While major Persian Gulf producers risk sovereign fiscal collapse if they cannot export their primary revenue generator, importing nations face energy rationing, industrial slowdowns, and soaring inflation.

The analytical problem is to evaluate:
1. **Which nations and geographical regions face existential economic and energy risks during a chokepoint closure?**
2. **How does the presence (or lack) of alternative bypass infrastructure mitigate vulnerability?**
3. **What is the statistical relationship between chokepoint transit dependency, daily hydrocarbon volume, and expected GDP contraction?**""")

# 4. Objectives
add_md("""## 3. Project Objectives
1. **Quantify National Exposure**: Identify the top countries most dependent on the Strait of Hormuz.
2. **Assess Hydrocarbon Volume at Risk**: Calculate the total and national daily volumes (in Mbd) disrupted.
3. **Evaluate Macroeconomic Severity**: Measure and rank estimated national GDP contractions.
4. **Compare Structural Roles**: Statistically contrast the vulnerabilities of energy exporters versus energy importers.
5. **Analyze Regional Disparities**: Aggregate exposure metrics across the Middle East, Asia-Pacific, Europe, and North America.
6. **Investigate Risk Mitigations**: Inspect alternative route infrastructure (bypass pipelines and strategic reserves).
7. **Perform Correlation Analysis**: Examine linear associations between dependency, volume affected, and macroeconomic contraction without assuming causation.
8. **Synthesize Findings into an Executive Dashboard**: Build a unified visual summary suitable for portfolio presentation.""")

# 5. Import Libraries
add_md("""## 4. Import Libraries

### Analytical Question
Which libraries are necessary to perform data manipulation, numerical calculations, and statistical plotting?""")

add_code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Visual formatting configurations
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 11
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

print("Libraries successfully imported!")""")

add_md("""### Interpretation
* `numpy`: High-performance numerical computing and array operations.
* `pandas`: Tabular data structures (`DataFrame`, `Series`) and data manipulation tools.
* `matplotlib.pyplot`: Foundational 2D plotting library for charts and multi-panel dashboards.
* `seaborn`: Statistical data visualization built on Matplotlib with built-in color palettes and aggregation features.""")

# 6. Load Dataset
add_md("""## 5. Load Dataset

### Analytical Question
How do we load the CSV dataset into a Pandas DataFrame and verify its basic dimensions?""")

add_code("""# Load the dataset
csv_path = 'strait_of_hormuz_closure_impacts.csv'
df = pd.read_csv(csv_path)

# Display first 5 rows
df.head()""")

add_code("""# Display last 5 rows
df.tail()""")

add_code("""# Check shape and column names
print(f"Dataset Shape: {df.shape[0]} rows, {df.shape[1]} columns\\n")
print("Columns in Dataset:")
for col in df.columns:
    print(f" - {col}")""")

# 7. Dataset Overview
add_md("""## 6. Dataset Overview

### Analytical Question
What data types and summary statistics describe the dataset?""")

add_code("""# DataFrame structure and data types
df.info()""")

add_code("""# Descriptive statistics for numerical variables
df.describe()""")

add_md("""### Interpretation
* The dataset contains 15 rows (countries) and 9 columns.
* There are 3 numerical features: `Hormuz_Transit_Dependency_Pct`, `Daily_Volume_Affected_Mbd`, and `Estimated_GDP_Impact_Pct`.
* There are 6 categorical features describing country, region, economic role, alternative route availability, risk tier, and primary fuel type.
* The average dependency is **58.20%**, average volume affected is **1.75 Mbd**, and average estimated GDP impact is **-4.38%**.""")

# 8. Data Quality Analysis
add_md("""## 7. Data Quality Analysis

### Analytical Question
Are there missing values, duplicated entries, or anomalies in the dataset? In particular, why does `Alternative_Route_Availability` contain missing values?""")

add_code("""# Check for missing values in each column
print("Missing values per column:")
print(df.isnull().sum())

print(f"\\nTotal duplicate rows: {df.duplicated().sum()}")""")

add_code("""# Inspect the rows with missing Alternative_Route_Availability
missing_routes = df[df['Alternative_Route_Availability'].isnull()]
missing_routes[['Country', 'Region', 'Role', 'Hormuz_Transit_Dependency_Pct', 'Alternative_Route_Availability']]""")

add_md("""### Interpretation & Data Quality Insight
* In the raw CSV file, countries with no alternative routes were recorded as the text string `"None"`.
* When Pandas loads `"None"`, it defaults to treating it as `NaN` (Not a Number / Missing Value).
* In this specific energy security context, `NaN` is not "missing or unknown data" — it explicitly denotes that **no physical bypass pipelines or maritime detours exist** for these nations (e.g., Kuwait and Qatar in the Gulf; Japan, South Korea, and Pakistan in Asia).
* **Cleaning Decision**: We should replace `NaN` with `'None (No Alternate Route)'` rather than dropping rows or imputing with the mode.""")

# 9. Data Cleaning
add_md("""## 8. Data Cleaning

### Analytical Question
How should we clean the dataset while preserving raw data integrity?""")

add_code("""# Create an explicit copy to keep original raw data untouched
df_clean = df.copy()

# Fill missing route availability with an informative string
df_clean['Alternative_Route_Availability'] = df_clean['Alternative_Route_Availability'].fillna('None (No Alternate Route)')

# Verify no missing values remain
print("Missing values in df_clean:")
print(df_clean.isnull().sum())""")

add_md("""### Interpretation
* `df_clean` is now a fully populated, clean DataFrame ready for exploratory data analysis.""")

# 10. Pandas EDA
add_md("""## 9. Exploratory Data Analysis (EDA) with Pandas""")

add_md("""### A. Which 5 countries have the highest Hormuz transit dependency?""")
add_code("""top5_dependency = df_clean.nlargest(5, 'Hormuz_Transit_Dependency_Pct')[
    ['Country', 'Region', 'Role', 'Hormuz_Transit_Dependency_Pct']
]
top5_dependency""")
add_md("""* **Insight**: Kuwait (100%), Qatar (95%), Japan (85%), South Korea (80%), and Pakistan (75%) have extreme dependency on the Strait.""")

add_md("""### B. Which 5 countries have the highest daily volume affected?""")
add_code("""top5_volume = df_clean.nlargest(5, 'Daily_Volume_Affected_Mbd')[
    ['Country', 'Region', 'Role', 'Daily_Volume_Affected_Mbd']
]
top5_volume""")
add_md("""* **Insight**: Saudi Arabia (5.5 Mbd) and China (4.8 Mbd) represent the single largest volumetric exposure on the exporter and importer sides, respectively.""")

add_md("""### C. Which 5 countries have the largest estimated GDP decline?""")
add_code("""# nsmallest finds the most negative GDP impacts (largest economic contractions)
top5_gdp_drop = df_clean.nsmallest(5, 'Estimated_GDP_Impact_Pct')[
    ['Country', 'Region', 'Role', 'Estimated_GDP_Impact_Pct']
]
top5_gdp_drop""")
add_md("""* **Insight**: All top 5 GDP contractions are Middle Eastern exporters: Kuwait (-15%), Iraq (-12%), Qatar (-10%), Iran (-6%), and Saudi Arabia (-4.5%).""")

add_md("""### D & E. Distribution of Countries by Region and Role""")
add_code("""print("--- Countries by Region ---")
print(df_clean['Region'].value_counts())

print("\\n--- Countries by Economic Role ---")
print(df_clean['Role'].value_counts())""")
add_md("""* **Insight**: The dataset focuses on Asia-Pacific consumers (7) and Middle Eastern producers (6), with Europe (1) and North America (1) for global comparison.""")

add_md("""### F, G, H. Regional Summary (Average Dependency, Total Volume, Average GDP Impact)""")
add_code("""region_summary = df_clean.groupby('Region').agg(
    Average_Dependency_Pct=('Hormuz_Transit_Dependency_Pct', 'mean'),
    Total_Volume_Mbd=('Daily_Volume_Affected_Mbd', 'sum'),
    Average_GDP_Impact_Pct=('Estimated_GDP_Impact_Pct', 'mean'),
    Country_Count=('Country', 'count')
).reset_index()

region_summary""")
add_md("""* **Insight**: Middle East (14.8 Mbd) and Asia-Pacific (11.2 Mbd) account for 26.0 Mbd of the 26.3 Mbd total volume at risk (98.8%). Middle Eastern economies face the sharpest GDP contraction (-8.50% avg).""")

add_md("""### I. Exporter vs. Importer Comparison""")
add_code("""role_summary = df_clean.groupby('Role').agg(
    Average_Dependency_Pct=('Hormuz_Transit_Dependency_Pct', 'mean'),
    Total_Volume_Mbd=('Daily_Volume_Affected_Mbd', 'sum'),
    Average_GDP_Impact_Pct=('Estimated_GDP_Impact_Pct', 'mean'),
    Country_Count=('Country', 'count')
).reset_index()

role_summary""")
add_md("""* **Insight**: Exporters face an average GDP contraction of **-8.50%**, more than 5 times greater than importers (**-1.63%**), because oil revenues directly fund national budgets.""")

add_md("""### J. Frequency of Economic Impact Risk Categories""")
add_code("""risk_counts = df_clean['Economic_Impact_Risk'].value_counts()
risk_counts""")
add_md("""* **Insight**: 11 out of 15 countries (73.3%) are classified as `Critical` (7) or `High` (4) risk.""")

# 11. NumPy Analysis
add_md("""## 10. NumPy Numerical Analysis

### Analytical Question
How can we use NumPy arrays to calculate descriptive statistics and correlation matrices from first principles?""")

add_code("""# Convert DataFrame series into 1D NumPy arrays
dep_arr = df_clean['Hormuz_Transit_Dependency_Pct'].to_numpy()
vol_arr = df_clean['Daily_Volume_Affected_Mbd'].to_numpy()
gdp_arr = df_clean['Estimated_GDP_Impact_Pct'].to_numpy()

print("--- NUMPY STATISTICAL ANALYSIS ---")
print(f"Hormuz Dependency (%): Mean={np.mean(dep_arr):.2f}%, Median={np.median(dep_arr):.2f}%, Std={np.std(dep_arr, ddof=1):.2f}%")
print(f"Daily Volume (Mbd):    Mean={np.mean(vol_arr):.2f} Mbd, Median={np.median(vol_arr):.2f} Mbd, Std={np.std(vol_arr, ddof=1):.2f} Mbd, Total={np.sum(vol_arr):.2f} Mbd")
print(f"GDP Impact (%):        Mean={np.mean(gdp_arr):.2f}%, Median={np.median(gdp_arr):.2f}%, Std={np.std(gdp_arr, ddof=1):.2f}%")

# Create a 2D matrix and compute correlation matrix
feature_matrix = np.column_stack((dep_arr, vol_arr, gdp_arr))
numpy_corr = np.corrcoef(feature_matrix, rowvar=False)

print("\\n--- NumPy Correlation Matrix ---")
print("Matrix Shape:", numpy_corr.shape)
print(np.round(numpy_corr, 4))""")

add_md("""### Interpretation
* Total daily volume at risk is **26.30 Mbd**.
* NumPy correlation confirms a negative linear correlation of **-0.6428** between transit dependency and estimated GDP impact.""")

# 12. Matplotlib Visualizations
add_md("""## 11. Matplotlib Visualizations

### Analytical Question
How do national dependency, volume affected, GDP impact, and regional totals rank when visualized with Matplotlib?""")

add_code("""# Chart 1: Dependency by Country
fig, ax = plt.subplots(figsize=(10, 6))
sorted_dep = df_clean.sort_values('Hormuz_Transit_Dependency_Pct', ascending=True)
ax.barh(sorted_dep['Country'], sorted_dep['Hormuz_Transit_Dependency_Pct'], color='#1f77b4', edgecolor='black', alpha=0.85)
ax.set_title('Hormuz Transit Dependency by Country (%)', fontsize=14, fontweight='bold', pad=12)
ax.set_xlabel('Transit Dependency (%)', fontsize=12)
ax.set_ylabel('Country', fontsize=12)
plt.tight_layout()
plt.show()""")

add_code("""# Chart 2: Daily Volume Affected by Country
fig, ax = plt.subplots(figsize=(10, 6))
sorted_vol = df_clean.sort_values('Daily_Volume_Affected_Mbd', ascending=True)
ax.barh(sorted_vol['Country'], sorted_vol['Daily_Volume_Affected_Mbd'], color='#ff7f0e', edgecolor='black', alpha=0.85)
ax.set_title('Daily Volume Affected by Country (Million Barrels/Day)', fontsize=14, fontweight='bold', pad=12)
ax.set_xlabel('Daily Volume (Mbd)', fontsize=12)
ax.set_ylabel('Country', fontsize=12)
plt.tight_layout()
plt.show()""")

add_code("""# Chart 3: Estimated GDP Impact by Country
fig, ax = plt.subplots(figsize=(10, 6))
sorted_gdp = df_clean.sort_values('Estimated_GDP_Impact_Pct', ascending=False)
ax.barh(sorted_gdp['Country'], sorted_gdp['Estimated_GDP_Impact_Pct'], color='#d62728', edgecolor='black', alpha=0.85)
ax.set_title('Estimated GDP Impact by Country (%)', fontsize=14, fontweight='bold', pad=12)
ax.set_xlabel('Estimated GDP Impact (%)', fontsize=12)
ax.set_ylabel('Country', fontsize=12)
plt.tight_layout()
plt.show()""")

add_code("""# Chart 4: Total Volume Affected by Region
fig, ax = plt.subplots(figsize=(8, 5))
sorted_reg_vol = region_summary.sort_values('Total_Volume_Mbd', ascending=False)
ax.bar(sorted_reg_vol['Region'], sorted_reg_vol['Total_Volume_Mbd'], color=['#2ca02c', '#9467bd', '#8c564b', '#e377c2'], edgecolor='black', alpha=0.85)
ax.set_title('Total Daily Hydrocarbon Volume Affected by Region (Mbd)', fontsize=14, fontweight='bold', pad=12)
ax.set_xlabel('Region', fontsize=12)
ax.set_ylabel('Total Volume (Mbd)', fontsize=12)
plt.tight_layout()
plt.show()""")

# 13. Seaborn Visualizations
add_md("""## 12. Seaborn Visualizations

### Analytical Question
How can Seaborn be used to evaluate multi-variable relationships, categorical distributions, and statistical correlation?""")

add_code("""# 1. Scatter Plot: Dependency vs. GDP Impact with Role and Region
fig, ax = plt.subplots(figsize=(9, 6))
sns.scatterplot(
    data=df_clean,
    x='Hormuz_Transit_Dependency_Pct',
    y='Estimated_GDP_Impact_Pct',
    hue='Role',
    style='Region',
    s=140,
    palette={'Exporter': '#d62728', 'Importer': '#1f77b4'},
    ax=ax
)
sns.regplot(
    data=df_clean,
    x='Hormuz_Transit_Dependency_Pct',
    y='Estimated_GDP_Impact_Pct',
    scatter=False,
    color='gray',
    line_kws={'linestyle': '--', 'linewidth': 1.5},
    ax=ax
)
ax.set_title('Hormuz Dependency vs. Estimated GDP Impact', fontsize=13, fontweight='bold')
ax.set_xlabel('Hormuz Transit Dependency (%)', fontsize=11)
ax.set_ylabel('Estimated GDP Impact (%)', fontsize=11)
plt.show()""")

add_code("""# 2. Box Plot: GDP Impact Distribution by Role
fig, ax = plt.subplots(figsize=(7, 5))
sns.boxplot(data=df_clean, x='Role', y='Estimated_GDP_Impact_Pct', palette=['#ff9999', '#99ccff'], ax=ax, width=0.4)
sns.stripplot(data=df_clean, x='Role', y='Estimated_GDP_Impact_Pct', color='black', size=7, jitter=0.2, ax=ax)
ax.set_title('Distribution of Estimated GDP Impact: Exporters vs Importers', fontsize=13, fontweight='bold')
ax.set_xlabel('Economic Role', fontsize=11)
ax.set_ylabel('Estimated GDP Impact (%)', fontsize=11)
plt.show()""")

add_code("""# 3. Count Plot: Frequency of Risk Severity Levels
fig, ax = plt.subplots(figsize=(8, 5))
risk_order = ['Critical', 'High', 'Severe', 'Moderate', 'Low']
sns.countplot(data=df_clean, x='Economic_Impact_Risk', order=risk_order, palette='Reds_r', edgecolor='black', ax=ax)
ax.set_title('Frequency of Economic Impact Risk Severity Levels', fontsize=13, fontweight='bold')
ax.set_xlabel('Risk Classification', fontsize=11)
ax.set_ylabel('Number of Countries', fontsize=11)
plt.show()""")

add_code("""# 4. Correlation Heatmap
fig, ax = plt.subplots(figsize=(7, 5))
corr_df = df_clean[['Hormuz_Transit_Dependency_Pct', 'Daily_Volume_Affected_Mbd', 'Estimated_GDP_Impact_Pct']].corr()
sns.heatmap(corr_df, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt='.2f', linewidths=1, ax=ax)
ax.set_title('Correlation Matrix of Numerical Risk Factors', fontsize=13, fontweight='bold')
plt.show()""")

add_code("""# 5. Average Dependency by Region
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=region_summary.sort_values('Average_Dependency_Pct', ascending=False), x='Region', y='Average_Dependency_Pct', palette='Blues_r', edgecolor='black', ax=ax)
ax.set_title('Average Hormuz Transit Dependency by Region (%)', fontsize=13, fontweight='bold')
ax.set_xlabel('Region', fontsize=11)
ax.set_ylabel('Average Dependency (%)', fontsize=11)
plt.show()""")

# 14. Correlation Analysis
add_md("""## 13. Correlation Analysis

### Analytical Question
What is the strength and meaning of the statistical associations between dependency, volume, and GDP impact?

### Findings
* **Dependency vs. GDP Impact ($r = -0.6428$)**: A moderate-to-strong negative association. Higher dependency **appears related to** deeper GDP contraction.
* **Volume Affected vs. GDP Impact ($r = -0.2602$)**: A weak negative association. Large economies like China absorb volumetric shocks better than small oil-dependent states.
* **Volume Affected vs. Dependency ($r = 0.2716$)**: Weak positive association.

> **Caution**: Correlation does **not** imply causation. These statistical relationships reflect underlying structural factors: fiscal reliance on oil exports, sovereign wealth reserves, and alternative pipeline availability.""")

# 15. Dashboard
add_md("""## 14. Executive Portfolio Dashboard

### Analytical Question
How can we construct an all-in-one visual summary combining high-level KPIs and multi-panel charts?""")

add_code("""# Create 3x3 Grid Dashboard
fig = plt.figure(figsize=(18, 12))
gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.3)

# 1. Header Banner with KPI Cards
kpi_ax = fig.add_subplot(gs[0, :])
kpi_ax.axis('off')
kpi_text = (
    "STRAIT OF HORMUZ CLOSURE IMPACT EXECUTIVE SUMMARY\\n"
    "------------------------------------------------------------------------------------------------------------------------\\n"
    f"  Total Countries Analyzed: {len(df_clean)}   |   "
    f"Total Daily Volume Affected: {df_clean['Daily_Volume_Affected_Mbd'].sum():.1f} Mbd   |   "
    f"Mean Hormuz Dependency: {df_clean['Hormuz_Transit_Dependency_Pct'].mean():.1f}%   |   "
    f"Mean GDP Contraction: {df_clean['Estimated_GDP_Impact_Pct'].mean():.1f}%"
)
kpi_ax.text(0.5, 0.5, kpi_text, fontsize=13, fontweight='bold', ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.8', facecolor='#f0f4f8', edgecolor='#334e68', linewidth=1.5))

# 2. Subplot: Dependency by Country
ax1 = fig.add_subplot(gs[1, 0])
sorted_c = df_clean.sort_values('Hormuz_Transit_Dependency_Pct')
ax1.barh(sorted_c['Country'], sorted_c['Hormuz_Transit_Dependency_Pct'], color='#1f77b4', edgecolor='black', alpha=0.85)
ax1.set_title('Hormuz Dependency (%)', fontsize=11, fontweight='bold')
ax1.set_xlabel('% Transit Dependency', fontsize=9)

# 3. Subplot: Dependency vs GDP Impact Scatter
ax2 = fig.add_subplot(gs[1, 1])
sns.scatterplot(data=df_clean, x='Hormuz_Transit_Dependency_Pct', y='Estimated_GDP_Impact_Pct', 
                hue='Role', s=90, palette={'Exporter': '#d62728', 'Importer': '#1f77b4'}, ax=ax2)
ax2.set_title('Dependency vs. GDP Impact', fontsize=11, fontweight='bold')
ax2.set_xlabel('Dependency (%)', fontsize=9)
ax2.set_ylabel('GDP Impact (%)', fontsize=9)

# 4. Subplot: Total Volume by Region
ax3 = fig.add_subplot(gs[1, 2])
reg_sorted = region_summary.sort_values('Total_Volume_Mbd', ascending=False)
ax3.bar(reg_sorted['Region'], reg_sorted['Total_Volume_Mbd'], color='#2ca02c', edgecolor='black', alpha=0.85)
ax3.set_title('Total Affected Volume by Region (Mbd)', fontsize=11, fontweight='bold')
ax3.set_xlabel('Region', fontsize=9)
ax3.set_ylabel('Volume (Mbd)', fontsize=9)
ax3.tick_params(axis='x', rotation=20)

# 5. Subplot: GDP Impact by Role (Boxplot)
ax4 = fig.add_subplot(gs[2, 0])
sns.boxplot(data=df_clean, x='Role', y='Estimated_GDP_Impact_Pct', palette=['#ff9999', '#99ccff'], ax=ax4, width=0.4)
ax4.set_title('GDP Impact by Role', fontsize=11, fontweight='bold')
ax4.set_xlabel('Role', fontsize=9)
ax4.set_ylabel('GDP Impact (%)', fontsize=9)

# 6. Subplot: Risk Classification Frequencies
ax5 = fig.add_subplot(gs[2, 1])
sns.countplot(data=df_clean, x='Economic_Impact_Risk', order=['Critical', 'High', 'Severe', 'Moderate', 'Low'], 
              palette='Reds_r', edgecolor='black', ax=ax5)
ax5.set_title('Economic Risk Severity Count', fontsize=11, fontweight='bold')
ax5.set_xlabel('Risk Category', fontsize=9)
ax5.set_ylabel('Count', fontsize=9)
ax5.tick_params(axis='x', rotation=20)

# 7. Subplot: Correlation Heatmap
ax6 = fig.add_subplot(gs[2, 2])
sns.heatmap(corr_df, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt='.2f', ax=ax6, cbar=False)
ax6.set_title('Metric Correlations', fontsize=11, fontweight='bold')

plt.suptitle('Strait of Hormuz Closure Risk & Impact Portfolio Dashboard', fontsize=16, fontweight='bold', y=0.98)
plt.savefig('dashboard_portfolio.png', dpi=300)
plt.show()""")

# 16. Key Findings
add_md("""## 15. Key Findings
1. **Critical Sovereign Risk for Gulf Exporters**: Kuwait (-15.0% GDP, 100% dependency) and Iraq (-12.0% GDP, 72% dependency) face severe economic contraction due to zero pipeline bypass capacity.
2. **Asymmetric Volume Concentration**: Global physical volume risk is heavily concentrated in **Saudi Arabia (5.5 Mbd)** and **China (4.8 Mbd)**, comprising **39.2%** of all disrupted flows.
3. **Structural Exporter vs. Importer Divide**: Exporters suffer over **5x higher average GDP contraction (-8.50% vs. -1.63%)** than importers because oil revenues directly fund national budgets.
4. **Asia-Pacific Supply Shock**: The Asia-Pacific region absorbs **11.2 Mbd (42.6%)** of total disrupted volume, with Japan (85%), South Korea (80%), and Pakistan (75%) exhibiting severe dependency.
5. **Mitigation via Bypass Infrastructure**: Saudi Arabia (East-West Pipeline to Yanbu) and UAE (Fujairah Pipeline) limit GDP contraction (-4.5% and -3.5%) relative to Kuwait (-15.0%), demonstrating the critical value of overland bypass infrastructure.
6. **Western Market Insulation**: The United States (-0.1% GDP impact) and Germany (-0.4% GDP impact) have low direct dependency due to domestic production and Atlantic routing.
7. **Pervasive Risk Severity**: 73.3% of analyzed countries fall under `Critical` or `High` economic risk.""")

# 17. Limitations
add_md("""## 16. Limitations
1. **Sample Scope**: Dataset includes 15 key countries; does not model indirect feedback in unlisted economies.
2. **Static Modeling**: Represents a static snapshot rather than a multi-month dynamic inventory drawdown simulation.
3. **Indirect Price Shock Omission**: Estimates direct trade disruption but does not model global crude price spikes ($150+/barrel) on global inflation.
4. **Categorical Risk Discretization**: Risk categories are discrete rather than continuous probability distributions.
5. **Correlation vs. Causation**: Statistical association between dependency and GDP contraction is mediated by sovereign wealth and fiscal buffers.""")

# 18. Conclusion
add_md("""## 17. Conclusion
A closure of the Strait of Hormuz represents an acute dual crisis: a **fiscal collapse for Persian Gulf energy exporters** and an **industrial energy-supply emergency for Asia-Pacific economies**. 

By applying **Pandas** for structured aggregation, **NumPy** for numerical analysis, and **Matplotlib/Seaborn** for visualizations, this study highlights that terrestrial bypass infrastructure (e.g., Saudi Arabia's East-West Pipeline and UAE's Fujairah bypass) is the single most decisive factor mitigating catastrophic GDP contractions.""")

notebook_dict = {
    'cells': cells,
    'metadata': {
        'language_info': {
            'name': 'python',
            'version': '3.14.3'
        },
        'kernelspec': {
            'display_name': 'Python 3',
            'language': 'python',
            'name': 'python3'
        }
    },
    'nbformat': 4,
    'nbformat_minor': 4
}

with open('strait_of_hormuz_analysis.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook_dict, f, indent=2)

print(f"Jupyter Notebook generated successfully with {len(cells)} cells!")
