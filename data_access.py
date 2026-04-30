import requests
from datetime import datetime, timezone


API_BASE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

def fetch_earthquakes(start_date, end_date, min_magnitude = None, max_magnitude = None, latitude = None, longitude = None, max_radius_km = None):
    """
    Fetches eqrthquake data from the USGS Earthquak Hazards API 

    Parameters:
        start_date (str): Start date in 'YYYY-MM-DD' Format
        end_date (str): End date in 'YYYY-MM-DD' Format
        min_magnitude (float, optional): Minimum earthquake magnitude
        max_magnitude (float, optional): Maximum earthquake magnitude
        latitude (float, optional): Latitude for location based search
        longitude (float, optional): Longitude for location based search
        max_radius_km (float, optional): Search radius in km
    
    Returns: 
        dict: Raw GeoJSON response from the USGS API, or None if the request fails

    """
    #must specify at least date for earthquake search 

    params = {
        "format": "geojson",
        "starttime": start_date,
        "endtime": end_date,
    }

    #optional filters for search if provided by user

    if min_magnitude is not None:
        params["minmagnitude"] = min_magnitude
    if max_magnitude is not None:
        params["maxmagnitude"] = max_magnitude
    if latitude is not None:
        params["latitude"] = latitude
    if longitude is not None:
        params["longitude"] = longitude
    if max_radius_km is not None:
        params["maxradiuskm"] = max_radius_km
    
    try:
        response = requests.get(API_BASE_URL, params = params)

        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


def parse_earthquakes(geojson_data):
    """
    Parses raw GeoJSON data from the USGS API and extracts necessary fields

    Parameters:
        geojson_data (dict): Raw GeoJSON response returtned by fetch_earthquake()

    Returns:
        earthquakes (dict): A list of earthquakes contained:
             - time (str): Event time in 'YYYY-MM-DD HH:MM:SS' format (UTC)
             - location (str): Human-readable location description
             - latitude (float): Latitude of the earthquake epicenter
             - longitude (float): longitude of the earthquake epicenter
             - depth_km (float): Depth of the earthquake in kilometers
             - magnitude (float): Earthquake magnitude
        Returns an empty list if data is None or contains no features.
    """

    if geojson_data is None:
        return[]
    
    earthquakes = []

    eq_features = geojson_data.get('features', [])

    for feature in eq_features:
        props = feature.get("properties", {})
        geometry = feature.get("geometry", {})
        coords = geometry.get("coordinates", [None, None, None])
 
        # Convert timestamp from milliseconds to a readable datetime string
        raw_time = props.get("time")
        
        readable_time = None
        if raw_time is not None:
            readable_time = datetime.fromtimestamp(raw_time / 1000, tz = timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
 
        earthquake = {
            "time": readable_time,
            "location": props.get("place", "Unknown"),
            "latitude": coords[1],
            "longitude": coords[0],
            "depth_km": coords[2],
            "magnitude": props.get("mag"),
        }
        earthquakes.append(earthquake)
 
    return earthquakes


