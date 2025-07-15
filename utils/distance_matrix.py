import requests
from dotenv import load_dotenv
import os

load_dotenv()

def build_distance_matrix(latlngs):
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    origins = [f"{lat},{lng}" for lat, lng in latlngs]
    destinations = origins.copy()

    matrix = []
    for i in range(0, len(origins), 25):
        response = requests.post("https://maps.googleapis.com/maps/api/distancematrix/json", params={
            "origins": "|".join(origins[i:i+25]),
            "destinations": "|".join(destinations),
            "key": GOOGLE_API_KEY
        }).json()
        for row in response['rows']:
            matrix.append([elem['distance']['value'] for elem in row['elements']])
    return matrix