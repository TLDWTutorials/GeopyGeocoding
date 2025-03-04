import pandas as pd
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import folium

# Load dataset
data = pd.read_excel("data.xlsx")

# Set up geolocator with a unique user agent
geolocator = Nominatim(user_agent="your_unique_app_name", timeout=10)  # Increase timeout for reliability

# Function to geocode an address with error handling
def geocode_address(row):
    try:
        location = geolocator.geocode(f"{row['City']}, {row['State_or_Province']}, {row['Country']}")
        if location:
            return location.latitude, location.longitude
    except GeocoderTimedOut:
        print(f"Timeout error for {row['City']}, {row['State_or_Province']}, {row['Country']}. Retrying...")
        return geocode_address(row)  # Retry
    except GeocoderServiceError:
        print(f"Service error (Rate limit?) for {row['City']}, {row['State_or_Province']}, {row['Country']}")
        return None, None
    return None, None

# Apply geocoding with delay
latitudes, longitudes = [], []
for index, row in data.iterrows():
    lat, lon = geocode_address(row)
    latitudes.append(lat)
    longitudes.append(lon)
    time.sleep(1)  # Delay to avoid rate limits

# Assign latitudes and longitudes to DataFrame
data['Latitude'] = latitudes
data['Longitude'] = longitudes

# Calculate mean of coordinates for map center
valid_data = data.dropna(subset=['Latitude', 'Longitude'])
if not valid_data.empty:
    map_center = [valid_data['Latitude'].mean(), valid_data['Longitude'].mean()]
else:
    map_center = [0, 0]  # Default to (0,0) if all geocoding fails

# Create folium map
mymap = folium.Map(location=map_center, zoom_start=4)

# Add markers
for index, row in valid_data.iterrows():
    folium.Marker([row['Latitude'], row['Longitude']], popup=row['City']).add_to(mymap)

# Save the map
mymap.save("geocoded_map.html")

print("Map saved as 'geocoded_map.html'. Open this file in a browser.")
