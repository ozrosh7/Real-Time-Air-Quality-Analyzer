import requests
import pandas as pd
from datetime import datetime

# Open-Meteo Air Quality API (No API Key Required)
BASE_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

# WHO Safety Thresholds (µg/m³)
WHO_THRESHOLDS = {
    'pm25': 15.0,
    'pm10': 45.0
}

# City Coordinates for Open-Meteo
CITY_COORDS = {
    "Delhi": {"lat": 28.6139, "lon": 77.2090},
    "Beijing": {"lat": 39.9042, "lon": 116.4074},
    "London": {"lat": 51.5074, "lon": -0.1278},
    "New York": {"lat": 40.7128, "lon": -74.0060},
    "Los Angeles": {"lat": 34.0522, "lon": -118.2437},
    "Paris": {"lat": 48.8566, "lon": 2.3522},
    "Tokyo": {"lat": 35.6762, "lon": 139.6503},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777}
}

def fetch_city_data(city_name, parameter="pm25"):
    """
    Fetches live AQI data for a given city from Open-Meteo Air Quality API.
    """
    if city_name not in CITY_COORDS:
        return pd.DataFrame()
        
    coords = CITY_COORDS[city_name]
    
    # Map parameter to Open-Meteo format
    api_param = "pm2_5" if parameter == "pm25" else "pm10"
    
    params = {
        "latitude": coords["lat"],
        "longitude": coords["lon"],
        "hourly": api_param,
        "timezone": "auto",
        "past_days": 2 # Get last 48 hours of data
    }
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Parse into Pandas DataFrame
        if 'hourly' in data and 'time' in data['hourly']:
            df = pd.DataFrame({
                'timestamp': pd.to_datetime(data['hourly']['time']),
                'value': data['hourly'][api_param]
            })
            
            df['city'] = city_name
            df['location'] = city_name
            df['parameter'] = parameter
            df['unit'] = 'µg/m³'
            
            # Remove NaNs
            df = df.dropna(subset=['value'])
            df = df[df['value'] >= 0]
            
            # Sort descending to get latest first
            df = df.sort_values(by='timestamp', ascending=False)
            
            return df
            
        return pd.DataFrame()
        
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
