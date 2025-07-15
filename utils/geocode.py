import requests
from dotenv import load_dotenv
import os

load_dotenv()

def geocode_addresses(df):
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_MAPS_API_KEY not set in environment.")

    locations = df['Address'].tolist()
    latlngs = []
    failed = []

    for addr in locations:
        try:
            response = requests.get("https://maps.googleapis.com/maps/api/geocode/json", params={
                "address": addr,
                "key": GOOGLE_API_KEY
            }).json()

            if response['results']:
                latlng = response['results'][0]['geometry']['location']
                latlngs.append((latlng['lat'], latlng['lng']))
            else:
                failed.append(addr)
                print(f"Geocoding failed for address: {addr}")
                latlngs.append((0, 0))  # or raise an error
        except Exception as e:
            print(f"Failed to geocode {addr}: {e}")
            latlngs.append((0, 0))
    
    return locations, latlngs,failed
