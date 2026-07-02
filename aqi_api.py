import requests
import pandas as pd
from datetime import datetime

# OpenAQ API endpoint
BASE_URL = "https://api.openaq.org/v2/measurements"

# WHO Safety Thresholds (µg/m³)
WHO_THRESHOLDS = {
    'pm25': 15.0,
    'pm10': 45.0
}

def fetch_city_data(city_name, parameter="pm25", limit=100):
    """
    Fetches live AQI data for a given city from OpenAQ REST API.
    """
    params = {
        "city": city_name,
        "parameter": parameter,
        "limit": limit,
        "order_by": "datetime",
        "sort": "desc"
    }
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data.get('results'):
            return pd.DataFrame()
            
        # Parse into Pandas DataFrame
        records = []
        for res in data['results']:
            records.append({
                'city': res.get('city'),
                'location': res.get('location'),
                'parameter': res.get('parameter'),
                'value': res.get('value'),
                'unit': res.get('unit'),
                'timestamp': pd.to_datetime(res['date']['utc'])
            })
            
        df = pd.DataFrame(records)
        df = df.dropna(subset=['value'])
        df = df[df['value'] >= 0] # Remove negative invalid readings
        
        return df
        
    except Exception as e:
        print(f"Error fetching data for {city_name}: {e}")
        return pd.DataFrame()

def detect_anomalies(df, parameter):
    """
    Detects concentration spikes exceeding WHO thresholds.
    """
    if df.empty or parameter not in WHO_THRESHOLDS:
        return pd.DataFrame()
        
    threshold = WHO_THRESHOLDS[parameter]
    anomalies = df[df['value'] > threshold].copy()
    
    return anomalies
