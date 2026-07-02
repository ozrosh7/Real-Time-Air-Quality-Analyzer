import streamlit as st
import matplotlib.pyplot as plt
from aqi_api import fetch_city_data, detect_anomalies, WHO_THRESHOLDS

st.set_page_config(page_title="Real-Time Air Quality Analyzer", page_icon="🌍", layout="wide")

st.title("🌍 Real-Time Air Quality Analyzer")
st.markdown("Analyze and visualize live Air Quality Index (AQI) trends and pollution anomalies using the OpenAQ API.")

# Sidebar
st.sidebar.header("Data Pipeline Settings")
cities = ["Delhi", "Beijing", "London", "New York", "Los Angeles", "Paris", "Tokyo", "Mumbai"]
selected_cities = st.sidebar.multiselect("Select Cities for Comparison", cities, default=["Delhi", "New York"])
parameter = st.sidebar.radio("Select Pollutant", ("pm25", "pm10"))

st.sidebar.markdown(f"**WHO Safety Threshold:** {WHO_THRESHOLDS[parameter]} µg/m³")

if not selected_cities:
    st.warning("Please select at least one city from the sidebar.")
    st.stop()

# Fetch Data
st.subheader(f"Time-Series Trend Analysis ({parameter.upper()})")
st.write("Fetching live data from OpenAQ REST API...")

all_data = []
all_anomalies = []

# Create columns for metric cards
cols = st.columns(len(selected_cities))

with st.spinner('Engineering Pandas data pipeline...'):
    for i, city in enumerate(selected_cities):
        df = fetch_city_data(city, parameter)
        
        if not df.empty:
            all_data.append(df)
            
            # Anomaly Detection
            anomalies = detect_anomalies(df, parameter)
            if not anomalies.empty:
                all_anomalies.append(anomalies)
            
            # Metric Card
            latest_val = df['value'].iloc[0]
            delta = 0 if len(df) < 2 else latest_val - df['value'].iloc[1]
            cols[i].metric(label=f"{city} {parameter.upper()} (µg/m³)", value=f"{latest_val:.1f}", delta=f"{delta:.1f}", delta_color="inverse")
            
if not all_data:
    st.error("Could not fetch data. The OpenAQ API might be rate-limiting or cities have no recent sensors online.")
    st.stop()

# Matplotlib Visualization
fig, ax = plt.subplots(figsize=(12, 6))

for df in all_data:
    city_name = df['city'].iloc[0]
    ax.plot(df['timestamp'], df['value'], marker='o', linestyle='-', label=city_name, alpha=0.7)

# Add WHO threshold line
ax.axhline(y=WHO_THRESHOLDS[parameter], color='r', linestyle='--', label=f'WHO Threshold ({WHO_THRESHOLDS[parameter]})')

ax.set_title(f"Live {parameter.upper()} Concentration Spikes Across Major Metropolitan Areas")
ax.set_xlabel("Time (UTC)")
ax.set_ylabel(f"Concentration (µg/m³)")
ax.legend()
ax.grid(True, alpha=0.3)

st.pyplot(fig)

# Statistical Spike Detection (Anomalies)
st.subheader("⚠️ Automated Anomaly Detection")

if all_anomalies:
    st.error(f"Hazardous {parameter.upper()} concentration spikes exceeding WHO safety thresholds detected!")
    
    for anom_df in all_anomalies:
        city_name = anom_df['city'].iloc[0]
        st.write(f"**{city_name}** - {len(anom_df)} hazardous reading(s) detected.")
        st.dataframe(anom_df[['timestamp', 'location', 'value']].head(5), hide_index=True)
else:
    st.success(f"No hazardous {parameter.upper()} spikes exceeding WHO safety thresholds detected in the current timeframe.")
