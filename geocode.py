import csv
import json
import time
import requests
import ssl
import certifi
from geopy.geocoders import ArcGIS, Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable


def geocode_address(address):
    # Use ArcGIS as primary
    # Use Nominatim API for geocoding as fallback
    # We add a delay to respect the usage policy (handled in main loop for Nominatim, but ArcGIS is faster)
    
    ctx = ssl.create_default_context(cafile=certifi.where())
    
    geocodes = [
        (ArcGIS(timeout=10, ssl_context=ctx), "ArcGIS"),
        (Nominatim(user_agent="KulkepviseletiSzavazasWebapp/1.0", timeout=10, ssl_context=ctx), "Nominatim")
    ]
    
    for geocoder, name in geocodes:
        try:
            location = geocoder.geocode(address)
            if location:
                return float(location.latitude), float(location.longitude)
        except (GeocoderTimedOut, GeocoderUnavailable) as e:
            print(f"Error geocoding {address} with {name}: {e}")
        except Exception as e:
            print(f"Unexpected error geocoding {address} with {name}: {e}")
            
    return None, None

def main():
    with open('data.csv', newline='', encoding='utf-8') as f:
        reader = list(csv.DictReader(f))
    
    results = []
    
    for row in reader:
        city_country = row["Ország, település"]
        geocodable_address = row["Geocodable Address"]
        original_address = row["Szavazóhely címe"]
        
        # 1. Try Geocodable Address (Manually cleaned address)
        print(f"Geocoding (1/3): {geocodable_address}")
        lat, lon = geocode_address(geocodable_address)
        
        # 2. Try Szavazóhely címe (Polling station address name + address)
        if lat is None:
            print(f"Failed geocodable, geocoding (2/3): {original_address}")
            lat, lon = geocode_address(original_address)

        # 3. Try City, Country (Fallback)
        if lat is None:
            print(f"Failed address, geocoding (3/3) city_country: {city_country}")
            lat, lon = geocode_address(city_country)
            
        row["lat"] = lat
        row["lon"] = lon
        results.append(row)
        
        # Sleep to be nice to OSM
        time.sleep(1.1)
        
    # Write to data.js
    with open("data.js", "w") as f:
        f.write("const KULKEPVISELETEK = ")
        json.dump(results, f, indent=2, ensure_ascii=False)
        f.write(";")

if __name__ == "__main__":
    main()
