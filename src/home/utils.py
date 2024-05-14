import requests


def get_route(departure, destination, api_key):
    url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }
    body = {
        "coordinates": [departure, destination]
    }
    response = requests.post(url, json=body, headers=headers)
    return response.json()
