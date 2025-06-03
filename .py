import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

# Load your sample water quality data
df = pd.read_csv("water_quality_sample.csv")

# Convert timestamp column
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Extract quarter and year for time-based grouping
df['quarter'] = df['timestamp'].dt.to_period('Q')

# Filter for a specific parameter (e.g., Barium)
parameter = "BARIUM_TOTAL"
param_df = df[df['parameter'] == parameter]

# Average Result by Site and Quarter
avg_results = (
    param_df.groupby(['site_id', 'quarter'])['result']
    .mean()
    .reset_index()
)

# Plot time-series trends
plt.figure(figsize=(12, 6))
sns.lineplot(data=avg_results, x='quarter', y='result', hue='site_id', marker="o")
plt.title(f'Quarterly Average {parameter} by Site')
plt.xlabel('Quarter')
plt.ylabel('Avg Result (µg/L)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('parameter_trends.png')
plt.show()

# Create heatmap data pivot
heatmap_data = avg_results.pivot(index='site_id', columns='quarter', values='result')

# Plot heatmap
plt.figure(figsize=(10, 5))
sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="RdYlGn_r", linewidths=0.5)
plt.title(f'Heatmap of Average {parameter} Levels by Site and Quarter')
plt.xlabel('Quarter')
plt.ylabel('Site ID')
plt.tight_layout()
plt.savefig('parameter_heatmap.png')
plt.show()
