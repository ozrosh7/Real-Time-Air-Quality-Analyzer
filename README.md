# Real-Time Air Quality Analyzer

A real-time environmental monitoring dashboard that dynamically fetches and processes live Air Quality Index (AQI) metrics across major global metropolitan areas.

## Features
* **Live API Integration**: Built with a robust data pipeline that fetches 48-hour historical time-series data using the Open-Meteo Air Quality REST API.
* **Pandas Data Engineering**: Utilizes Pandas to parse JSON responses, handle missing/invalid readings, and structure the data into analysis-ready dataframes.
* **Statistical Anomaly Detection**: Automatically scans incoming PM2.5 and PM10 concentration data to identify hazardous spikes exceeding standard World Health Organization (WHO) safety thresholds.
* **Interactive Dashboard**: Deployed a fully responsive Streamlit web application featuring interactive Matplotlib visualizations for dynamic environmental exploration.

## Tech Stack
* **Language**: Python
* **Data Processing**: Pandas
* **Visualization**: Matplotlib, Streamlit
* **API/Networking**: Requests, REST API

## How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ozrosh7/Real-Time-Air-Quality-Analyzer.git
   cd Real-Time-Air-Quality-Analyzer
   ```

2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Boot up the Streamlit server:**
   ```bash
   streamlit run app.py
   ```
