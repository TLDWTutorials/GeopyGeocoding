# Geocode Locations and Create an Interactive Map

This script reads city, state, and country data from an Excel file, geocodes the locations using Nominatim, and creates an interactive map with Folium.

## Installation

1. Install Python.
2. Install the required libraries:

   pip install pandas geopy folium openpyxl

3. Create an Excel file named `data.xlsx` with the following columns (or use example provided):

   City | State_or_Province | Country
   ---- | ---------------- | -------
   New York | NY | USA
   London | England | UK
   Tokyo | Tokyo | Japan

## Usage

Run the script:

```python
import pandas as pd
import time
from geopy.geocoders import Nominatim
import folium

data = pd.read_excel("data.xlsx")

geolocator = Nominatim(user_agent="your_unique_app_name", timeout=10)

def geocode_address(row):
    try:
        location = geolocator.geocode(f"{row['City']}, {row['State_or_Province']}, {row['Country']}")
        return (location.latitude, location.longitude) if location else (None, None)
    except:
        return None, None

data['Latitude'], data['Longitude'] = zip(*data.apply(geocode_address, axis=1))
time.sleep(1)

map_center = [data['Latitude'].mean(), data['Longitude'].mean()]
mymap = folium.Map(location=map_center, zoom_start=4)

for _, row in data.iterrows():
    if row['Latitude'] and row['Longitude']:
        folium.Marker([row['Latitude'], row['Longitude']], popup=row['City']).add_to(mymap)

mymap.save("geocoded_map.html")
print("Map saved as 'geocoded_map.html'")
```

## Troubleshooting

- Error 443 (Blocked Requests)? Change user_agent="your_unique_app_name" to something unique.
- No locations found? Double-check city and country names for typos.

## License
MIT License.  Free to use as needed. 
