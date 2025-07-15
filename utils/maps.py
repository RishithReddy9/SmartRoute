import requests
import polyline
from dotenv import load_dotenv
import os

load_dotenv()

def get_road_path(origin, destination):
    key = os.getenv("GOOGLE_API_KEY")
    origin_str = f"{origin[0]},{origin[1]}"
    dest_str = f"{destination[0]},{destination[1]}"

    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin_str,
        "destination": dest_str,
        "mode": "driving",
        "key": key
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data['status'] == 'OK':
        encoded_polyline = data['routes'][0]['overview_polyline']['points']
        path = polyline.decode(encoded_polyline)
        return path
    else:
        print(f"Failed to fetch directions: {data}")
        return [origin, destination]  # fallback to straight line
